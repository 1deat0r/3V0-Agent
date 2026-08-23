"""Native probe core — deterministic measurement for the evolution monitor.

Stdlib-only, zero 3V0. Implements the OBSERVABLE half of EVOLUTION_PROBE.md
v0.2: bank validation, per-band stats, calibration / noise-floor estimation, the
pre-registered trend rule, and git-versioned result recording.

GRADING (the {PASS, FAIL, INCONCLUSIVE} verdicts from a PINNED fresh-context
subagent) is dispatched by the agent at cadence time (delegate_task with pinned
model/version/temperature=0/seed) and fed back in as verdict lists.

Per the independent review (ML/psych/software-eng): this core is ADVISORY and
LOW-POWER. Its numbers never gate revert/continue; they only inform judgment,
and only AFTER calibration (noise floor) and grader certification.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import statistics
from pathlib import Path

EXPECT_BANDS = {"easy": 5, "medium": 8, "hard": 6, "escalated": 4}
BAND_ORDER = ["easy", "medium", "hard", "escalated"]
# §5: probe numbers are "uncalibrated", not even advisory, until the pinned grader's
# accuracy on the known-answer subset is >= this PRE-REGISTERED floor. (Set before
# any certification run; grader_cert_v1.json result must clear this to count.)
GRADER_CERT_FLOOR = 0.9
LEAK_TERMS = ("3v0", "3v0", "mustbearn", "fiverr", "axiom")
DATE_RE = re.compile(r"\b(20\d\d|current year|today|this month)\b", re.I)
_REQUIRED = {"id", "band", "domain", "prompt", "rubric", "time_box_min"}


def validate_bank(bank: dict) -> dict:
    """Structural + held-out validator for a frozen bank. Returns {ok, issues}."""
    issues: list[str] = []
    tasks = bank.get("tasks", []) if isinstance(bank, dict) else []
    bands = {}
    ids = []
    for t in tasks:
        if not isinstance(t, dict):
            issues.append("non-dict task entry")
            continue
        ids.append(t.get("id"))
        bands[t.get("band")] = bands.get(t.get("band"), 0) + 1
        missing = [k for k in _REQUIRED if k not in t]
        if missing:
            issues.append(f"{t.get('id')}: missing {missing}")
        r = t.get("rubric")
        if not (isinstance(r, dict) and isinstance(r.get("pass"), list) and "inconclusive" in r):
            issues.append(f"{t.get('id')}: rubric shape invalid")
        blob = (t.get("prompt", "") + json.dumps(t.get("rubric", ""))).lower()
        for w in LEAK_TERMS:
            if w in blob:
                issues.append(f"{t.get('id')}: held-out leak '{w}'")
        if DATE_RE.search(blob):
            issues.append(f"{t.get('id')}: date-dependent")
    if bands != EXPECT_BANDS:
        issues.append(f"bands mismatch: {bands} != {EXPECT_BANDS}")
    if len(ids) != len(set(ids)):
        issues.append("duplicate task ids")
    return {"ok": not issues, "issues": issues, "n_tasks": len(tasks)}


def band_stats(verdicts: list[dict]) -> dict:
    """Per-band pass rates from a run's verdict list.

    verdicts: [{id, band, verdict in {PASS,FAIL,INCONCLUSIVE}}]
    A verdict counts toward the band's n (graded total); only PASS increments
    `passed`. INCONCLUSIVE is treated as \"not passed\" (it is neither a PASS nor
    a FAIL; see §2's documented treatment) — so rate = PASS / graded-total."""
    per: dict[str, list] = {}
    for v in verdicts:
        per.setdefault(v.get("band"), []).append(v.get("verdict") == "PASS")
    out = {}
    for band, marks in per.items():
        n = len(marks)
        out[band] = {"n": n, "passed": sum(marks), "rate": (sum(marks) / n) if n else None}
    return out


def composite(verdicts: list[dict]) -> float | None:
    """Weighted per-band composite (spec §2): the mean of each band's pass rate,
    so bands weight equally regardless of how many tasks they hold (a band is not
    silenced by being under-sampled). INCONCLUSIVE lowers the band rate but does
    not otherwise distort weighting."""
    bs = band_stats(verdicts)
    rates = [s["rate"] for s in bs.values() if s["rate"] is not None]
    return sum(rates) / len(rates) if rates else None


def frontier(verdicts: list[dict]) -> str | None:
    """Highest difficulty band with at least one PASS (spec §2). Order escalates
    with difficulty; returns None if nothing passed (or no verdicts)."""
    passed = {v.get("band") for v in verdicts if v.get("verdict") == "PASS"}
    for band in reversed(BAND_ORDER):
        if band in passed:
            return band
    return None


def calibrate(repeats: list[list[dict]]) -> dict:
    """Noise floor: mean/std of per-band pass rates across K runs (§3).
    Returns {band: {mean, sd, n}} for bands present in all repeats."""
    per: dict[str, list[float]] = {}
    for verdicts in repeats:
        for band, s in band_stats(verdicts).items():
            if s["rate"] is not None:
                per.setdefault(band, []).append(s["rate"])
    out = {}
    for band, rates in per.items():
        out[band] = {"mean": statistics.mean(rates),
                     "sd": statistics.stdev(rates) if len(rates) > 1 else 0.0,
                     "n": len(rates)}
    return out


def thresholds(cal: dict, sigma: float = 2.0) -> dict:
    """Pre-registered band bounds = calibration mean +/- sigma*sd."""
    return {band: {"mean": c["mean"], "lo": c["mean"] - sigma * c["sd"],
                   "hi": c["mean"] + sigma * c["sd"]} for band, c in cal.items()}


def apply_trend(recent_runs: list[dict], th: dict, min_repeats: int = 2) -> dict:
    """Advisory trend with the §3 reproducibility gate ENFORCED.

    recent_runs: newest-first list of per-band stats dicts (band -> {'rate',..}),
    so recent_runs[0] is the latest run. A band is flagged 'regression-suspect' /
    'growth-hint' ONLY if its rate is outside [lo,hi] in the LAST min_repeats
    consecutive runs that have a rate for that band (spec §3: signal must be
    reproducible across >=2 consecutive runs, not a single-run excursion).
    The flag is advisory — it never gates revert/continue (spec §6). Bands not
    yet backed by min_repeats calibrated observations are reported as within-noise /
    needs-more-runs, never as a collapse or a win.
    """
    per: dict[str, dict] = {}
    for band, tc in th.items():
        rates = []
        for run in recent_runs:
            s = run.get(band)
            if isinstance(s, dict) and s.get("rate") is not None:
                rates.append(s["rate"])
            if len(rates) == min_repeats:
                break
        if len(rates) < min_repeats:
            per[band] = {"signal": "within-noise",
                         "note": f"only {len(rates)}/{min_repeats} consecutive rates; no signal claimed"}
            continue
        lo, hi = tc["lo"], tc["hi"]
        if all(r < lo for r in rates):
            per[band] = {"signal": "regression-suspect", "rate": rates[0],
                         "lo": round(lo, 3), "consecutive": len(rates)}
        elif all(r > hi for r in rates):
            per[band] = {"signal": "growth-hint", "rate": rates[0],
                         "hi": round(hi, 3), "consecutive": len(rates)}
        else:
            per[band] = {"signal": "within-noise", "rate": rates[0]}
    flagged = [b for b, d in per.items() if d.get("signal") in ("regression-suspect", "growth-hint")]
    return {"per_band": per, "flagged": flagged,
            "advisory": True, "min_repeats_required": min_repeats}


def null_control(live: list[dict], null: list[dict], th: dict) -> dict:
    """Compare a cadence run against a FROZEN-AGENT NULL control (Phantom Gains).

    The §3 calibration floor is the variance of the *grader alone* under a
    no-change condition. Claiming "evolution" means differencing a live run
    against a reference — exactly the operation that manufactures phantom gains
    when the reference is the live run's own earlier self (differencing two
    noisy estimates, cf. Phantom Gains `2608.20290`). This control pushes a
    **frozen snapshot of the agent** (fixed commit/body; same pinned grader;
    same frozen bank) through the identical pipeline as the null, then reports
    each live run as its **delta vs. that frozen null** — never as an absolute
    number. A directional claim survives only if the live rate differs from the
    null rate by more than the pre-registered band width (calibration mean
    +/- sigma*sd) AND is reproducible across >=2 consecutive live runs (the §3
    gate, enforced by ``apply_trend``).

    ``null`` = the frozen-agent control's verdicts; ``th`` = the dict returned
    by ``thresholds()`` (pre-registered band bounds; the sigma that produced it
    is already baked into the band, so it is not re-taken here).
    Returns, per band: ``live_rate``, ``null_rate``, ``delta`` (live - null),
    ``band_width``, and a ``signal`` in:
    - ``off`` — both rates inside the calibrated noise band (indistinguishable);
    - ``null-drift`` — the null itself is outside the band, so the control is
      stale and the comparison is INVALID (re-freeze the null, do not claim);
    - ``growth-hint`` / ``regression-suspect`` — live outside the band while
      null is inside; a *candidate* that only becomes advisory after the >=2-run
      reproducibility gate. Advisory only (§6); never gates revert/continue.
    """
    lstat = band_stats(live)
    nstat = band_stats(null)
    out = {}
    bands = BAND_ORDER if all(b in BAND_ORDER for b in lstat) else lstat
    for band in bands:
        l = lstat.get(band)
        n = nstat.get(band)
        if l is None or l["rate"] is None or n is None or n["rate"] is None:
            continue
        live_rate, null_rate = l["rate"], n["rate"]
        delta = live_rate - null_rate
        tc = th.get(band)
        if tc is None:
            # No calibrated band for this one -> cannot bound noise; skip rather
            # than emit an ungrounded signal.
            continue
        width = tc["hi"] - tc["lo"]
        null_off = not (tc["lo"] <= null_rate <= tc["hi"])
        live_off = not (tc["lo"] <= live_rate <= tc["hi"])
        if not live_off and not null_off:
            signal = "off"
        elif null_off:
            signal = "null-drift"   # control stale -> comparison invalid
        else:
            # live outside noise, null inside: a candidate; the `apply_trend`
            # gate turns it into a confirmed advisory flag.
            signal = "growth-hint" if delta > 0 else "regression-suspect"
        out[band] = {
            "live_rate": round(live_rate, 3),
            "null_rate": round(null_rate, 3),
            "delta": round(delta, 3),
            "band_width": round(width, 3),
            "signal": signal,
        }
    return {"per_band": out, "advisory": True,
            "note": "delta vs frozen-null; directional claims need >=2 consecutive live runs"}


def record_run(path: Path | str, run_meta: dict, verdicts: list[dict]) -> dict:
    """Append a run (meta + verdicts) to the git-versioned results store."""
    p = Path(path)
    data = json.loads(p.read_text()) if p.is_file() else {"runs": []}
    data.setdefault("runs", []).append({
        **run_meta,
        "recorded": datetime.date.today().isoformat(),
        "verdicts": verdicts,
    })
    p.write_text(json.dumps(data, indent=2))
    return {"recorded": len(data["runs"]), "path": str(p)}
