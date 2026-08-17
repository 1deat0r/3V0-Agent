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
# Self-imposed daily budget: ~$90/mo, the top of the real $15–100/mo
# DeepSeek-v4-pro run-rate. NOT derived from per-token prices — the token
# policy (TOKEN_EFFICIENCY.md) has no dollar budget, only $/1M prices. Kept
# flat (not peak-adjusted) on purpose: this is an absolute ceiling, not a
# scheduling hint.
BURN_DAILY_MAX_USD = 3.0
MODEL_MIN_COST_USD = 0.50
PRIMARY_MODEL = "deepseek-v4-pro"
AUX_MODEL = "deepseek-v4-flash"   # policy-mandated target for aux/background LLM work
INTENDED_MODELS = {PRIMARY_MODEL, AUX_MODEL}
CACHE_HIT_MIN = 0.90              # TOKEN_EFFICIENCY.md's #1 lever; below this the prefix is breaking
# Cheap-aux tasks the policy pins to flash. ``approval`` is DELIBERATELY
# absent: the smart-approval security guard stays on the primary model
# (TOKEN_EFFICIENCY.md) — flagging it would be a false positive.
AUX_TASKS = {"compression"}
MEMORY_SUCCESS_MIN = 0.80
COMPRESSION_FAILURES_MAX = 0
RELIABILITY_EXCLUDE = {"memory"}  # memory has its own dedicated detector
# Inherently long-running tools — their p95 "latency" is wall-clock wait
# (background process, browser, subagents), not a fixable slowdown.
LATENCY_EXCLUDE = {"process", "browser_exec", "delegate_task"}

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
        if t.get("name") in LATENCY_EXCLUDE:
            continue  # wall-clock wait semantics; latency isn't a defect here
        p95 = t.get("latency_p95_ms")
        if p95 is not None and p95 > TOOL_LATENCY_P95_MAX_MS:
            out.append(_finding(
                "tool_latency", "medium",
                f"{t['name']} p95 latency is {p95 / 1000:.1f}s",
                {"name": t["name"], "count": count, "p95_ms": p95},
                f"investigate {t['name']}: find slow calls/patterns, then cache or parallelize",
            ))
    return out


def cache_health(report):
    """Flag a degraded prompt-cache-hit ratio (the policy's #1 cost lever)."""
    ratio = report.get("totals", {}).get("cache_hit_ratio")
    if ratio is not None and ratio < CACHE_HIT_MIN:
        return [_finding(
            "cache", "high",
            f"cache-hit ratio {ratio:.2f} below {CACHE_HIT_MIN} — the prompt prefix is being broken",
            {"cache_hit_ratio": ratio},
            "protect the prefix (TOKEN_EFFICIENCY.md): avoid mid-conversation system-prompt/toolset edits",
        )]
    return []


def aux_routing(report):
    """Flag cheap-aux tasks (compression) running on a non-flash model.

    ``approval`` is deliberately exempt: the smart-approval security guard
    stays on the primary model by design (TOKEN_EFFICIENCY.md).

    TOKEN_EFFICIENCY.md routes background/aux LLM work to deepseek-v4-flash;
    any primary-model aux spend is a policy violation, however small.
    """
    out = []
    for tsk in report.get("tasks", []):
        if tsk.get("task") in AUX_TASKS and tsk.get("model") != AUX_MODEL:
            cost = tsk.get("estimated_cost_usd", 0.0)
            if cost > 0:
                out.append(_finding(
                    "aux_routing", "low",
                    f"aux task '{tsk['task']}' ran on {tsk['model']} (${cost:.2f}); policy routes aux → {AUX_MODEL}",
                    {"task": tsk["task"], "model": tsk["model"], "cost_usd": cost},
                    "pin aux/background LLM tasks to deepseek-v4-flash (TOKEN_EFFICIENCY.md)",
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
    """Flag *unintended* models consuming non-trivial cost.

    deepseek-v4-pro (primary) and deepseek-v4-flash (policy-mandated aux) are
    intended; anything else spending >= MODEL_MIN_COST_USD is a finding.
    """
    out = []
    for m in report.get("models", []):
        if m.get("model") in INTENDED_MODELS:
            continue
        if m.get("estimated_cost_usd", 0.0) >= MODEL_MIN_COST_USD:
            out.append(_finding(
                "model_mix", "low",
                f"{m['model']} consumed ${m['estimated_cost_usd']:.2f} (unintended model)",
                {"model": m["model"], "cost_usd": m["estimated_cost_usd"],
                 "api_calls": m.get("api_calls")},
                "confirm this model is authorized (Prime Directive: DeepSeek-v4-pro only)",
            ))
    return out


def memory_health(report):
    """Flag a low memory-tool success rate (do NOT assume a single root cause)."""
    for t in report.get("tools", []):
        if t.get("name") == "memory":
            rate = t.get("success_rate")
            if rate is not None and rate < MEMORY_SUCCESS_MIN:
                return [_finding(
                    "memory_health", "high",
                    f"memory writes succeed only {rate * 100:.0f}% — diagnose the cause, don't assume 'full'",
                    {"success_rate": rate, "count": t.get("count")},
                    "memory failures are a mix: char-budget rejection / stale replace-target / malformed call shape. Inspect which, then fix accordingly (prune only if budget-bound).",
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
    findings += cache_health(report)
    findings += aux_routing(report)
    findings += memory_health(report)
    findings += compression_health(report)
    findings += burn_outliers(report)
    findings += model_mix_findings(report)
    order = {s: i for i, s in enumerate(SEVERITY)}
    findings.sort(key=lambda f: order.get(f["severity"], 99))
    return findings
