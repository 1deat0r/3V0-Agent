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
    verdicts: [{id, band, verdict in {PASS,FAIL,INCONCLUSIVE}}]"""
    per: dict[str, list] = {}
    for v in verdicts:
        per.setdefault(v.get("band"), []).append(v.get("verdict") == "PASS")
    out = {}
    for band, marks in per.items():
        n = len(marks)
        out[band] = {"n": n, "passed": sum(marks), "rate": (sum(marks) / n) if n else None}
    return out


def composite(verdicts: list[dict]) -> float | None:
    marks = [v.get("verdict") == "PASS" for v in verdicts]
    return sum(marks) / len(marks) if marks else None


def calibrate(repeats: list[list[dict]]) -> dict:
    """Noise floor: mean/std of per-band pass rates across K runs (§3).
    Returns {band: {mean, sd, n}} for bands present in all repeats."""
    import statistics
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


def apply_trend(current: dict, baseline: dict, th: dict, min_repeats: int = 2) -> dict:
    """Advisory trend. A band registers a shift only if current rate is outside
    [mean-base..]: uses th bounds from calibration, and requires con-firm via the
    caller having >= min_repeats consistent runs (flag, not gate)."""
    per: dict[str, dict] = {}
    for band, s in current.items():
        if band not in th:
            per[band] = {"note": "no calibrated threshold (uncalibrated band)"}
            continue
        r = s["rate"]
        if r is None:
            per[band] = {"note": "no rate"}
            continue
        lo, hi = th[band]["lo"], th[band]["hi"]
        if r < lo:
            per[band] = {"signal": "regression-suspect", "rate": r, "lo": round(lo, 3)}
        elif r > hi:
            per[band] = {"signal": "growth-hint", "rate": r, "hi": round(hi, 3)}
        else:
            per[band] = {"signal": "within-noise", "rate": r}
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
