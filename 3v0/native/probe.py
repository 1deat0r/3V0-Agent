"""Native probe core — deterministic measurement for the evolution monitor.

Stdlib-only, zero Hermes. Implements the OBSERVABLE half of EVOLUTION_PROBE.md
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
LEAK_TERMS = ("3v0", "hermes", "mustbearn", "fiverr", "axiom")
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
