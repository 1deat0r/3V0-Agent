"""Pure insight detection over the analytics report (Stone 20).

Turns the metrics in report.json into ranked, evidence-backed findings.
Decision-support only: this PROPOSES; the caller DISPOSES through the normal
disciplined pipeline (prime filter → test → review → commit). It never
mutates anything — it reads a report dict and returns findings.
"""

from __future__ import annotations

# Thresholds (single source of truth for the detection rules). Tunable here;
# they are heuristics over 3V0's own operating envelope, not universal truth.
TOOL_SUCCESS_MIN = 0.80
TOOL_MIN_CALLS = 20
TOOL_LATENCY_P95_MAX_MS = 10_000.0
BURN_DAILY_MAX_USD = 3.0
MODEL_MIN_COST_USD = 0.50
PRIMARY_MODEL = "deepseek-v4-pro"
MEMORY_SUCCESS_MIN = 0.80
COMPRESSION_FAILURES_MAX = 0
RELIABILITY_EXCLUDE = {"memory"}  # memory has its own dedicated detector

SEVERITY = ("critical", "high", "medium", "low")


def _finding(category, severity, message, evidence, action):
    return {
        "category": category,
        "severity": severity,
        "message": message,
        "evidence": evidence,
        "suggested_action": action,
    }


def tool_reliability(report):
    """Flag tools with low success rate or high p95 latency (enough calls)."""
    out = []
    for t in report.get("tools", []):
        if t.get("name") in RELIABILITY_EXCLUDE:
            continue  # that signal has its own dedicated detector
        count = t.get("count", 0)
        if count < TOOL_MIN_CALLS:
            continue
        rate = t.get("success_rate")
        if rate is not None and rate < TOOL_SUCCESS_MIN:
            out.append(_finding(
                "tool_reliability", "high",
                f"{t['name']} succeeds only {rate * 100:.0f}% of the time",
                {"name": t["name"], "count": count, "success_rate": rate,
                 "failure": t.get("failure"), "unknown": t.get("unknown")},
                f"investigate {t['name']}: inspect failing call sites, then fix or avoid",
            ))
        p95 = t.get("latency_p95_ms")
        if p95 is not None and p95 > TOOL_LATENCY_P95_MAX_MS:
            out.append(_finding(
                "tool_latency", "medium",
                f"{t['name']} p95 latency is {p95 / 1000:.1f}s",
                {"name": t["name"], "count": count, "p95_ms": p95},
                f"investigate {t['name']}: find slow calls/patterns, then cache or parallelize",
            ))
    return out


def burn_outliers(report):
    """Flag daily burn above the absolute cap."""
    out = []
    for d in report.get("daily", []):
        cost = d.get("estimated_cost_usd", 0.0)
        if cost > BURN_DAILY_MAX_USD:
            out.append(_finding(
                "burn", "medium",
                f"{d['date']} burned ${cost:.2f} (over ${BURN_DAILY_MAX_USD:.2f})",
                {"date": d["date"], "cost_usd": cost, "tool_calls": d.get("tool_calls")},
                "review that day's sessions for token-heavy patterns (large reads, re-fetching)",
            ))
    return out


def model_mix_findings(report):
    """Flag non-primary models consuming non-trivial cost."""
    out = []
    for m in report.get("models", []):
        if m.get("model") != PRIMARY_MODEL and m.get("estimated_cost_usd", 0.0) >= MODEL_MIN_COST_USD:
            out.append(_finding(
                "model_mix", "low",
                f"{m['model']} consumed ${m['estimated_cost_usd']:.2f} (non-primary)",
                {"model": m["model"], "cost_usd": m["estimated_cost_usd"],
                 "api_calls": m.get("api_calls")},
                "confirm non-primary model usage is intended (e.g. flash for compaction)",
            ))
    return out


def memory_health(report):
    """Flag a low memory-tool success rate (usually means the store is full)."""
    for t in report.get("tools", []):
        if t.get("name") == "memory":
            rate = t.get("success_rate")
            if rate is not None and rate < MEMORY_SUCCESS_MIN:
                return [_finding(
                    "memory_health", "high",
                    f"memory writes succeed only {rate * 100:.0f}% — likely full",
                    {"success_rate": rate, "count": t.get("count")},
                    "prune stale memory entries to free the char budget",
                )]
    return []


def compression_health(report):
    """Flag compression failures (context is being lost)."""
    n = report.get("health", {}).get("compression_failure_errors", 0)
    if n > COMPRESSION_FAILURES_MAX:
        return [_finding(
            "compression", "high",
            f"{n} session(s) had compression failures",
            {"count": n},
            "inspect compression failure errors; context is being lost",
        )]
    return []


def detect(report):
    """Run all detectors and return findings ranked by severity (high → low)."""
    findings = []
    findings += tool_reliability(report)
    findings += memory_health(report)
    findings += compression_health(report)
    findings += burn_outliers(report)
    findings += model_mix_findings(report)
    order = {s: i for i, s in enumerate(SEVERITY)}
    findings.sort(key=lambda f: order.get(f["severity"], 99))
    return findings
