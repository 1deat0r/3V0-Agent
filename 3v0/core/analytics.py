"""Pure analytics aggregation for 3V0's self-instrumentation.

Reads *data* (lists of dicts) and returns metrics. No I/O here — the DB
reads and file writes live in scripts/analytics.py (invariant #4: pure
decision logic in core/, I/O at the edges).

Metrics computed:
  - session totals (tokens, cost, counts, active days) — incl. cache-hit
    ratio and output-token share (the two levers named in TOKEN_EFFICIENCY.md)
  - per-model mix (tokens, cost, api calls, distinct sessions, cache-hit ratio)
  - per-task × per-model mix (surfaces aux routing: policy requires
    compression/approval to run on deepseek-v4-flash, not the primary model)
  - per-tool frequency, heuristic success rate, and latency distribution
  - per-day activity buckets (burn trend, incl. per-day cache-hit ratio)
  - body health (compression failures, rewinds, end reasons)
"""

import datetime
import json
import statistics


# --------------------------------------------------------------------------
# Tool success classification (heuristic)
# --------------------------------------------------------------------------

_LEADING_ERROR = (
    "traceback", "error:", "error ", "no such file", "permission denied",
    "connection refused", "command not found", "usage:", "fatal:",
    "exception:",
)


def classify_tool_result(content):
    """Classify a tool result as 'success' | 'failure' | 'unknown'.

    Best-effort, NOT ground truth (the runtime does not yet populate
    effect_disposition). A result is 'failure' only if it carries an
    explicit error signal:
      1. JSON boolean `success` == false
      2. JSON `exit_code` != 0
      3. JSON truthy `error`
      4. non-JSON text with a leading error signature
    Otherwise 'success' (a result returned with no explicit error signal);
    None -> 'unknown'. Content-bearing tools (read_file, search_files,
    browser_exec …) are classified by the JSON envelope, never by scanning
    the embedded content for the word "error".
    """
    if content is None:
        return "unknown"
    text = str(content)
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            if isinstance(data.get("success"), bool):
                return "success" if data["success"] else "failure"
            if "exit_code" in data:
                try:
                    return "success" if int(data["exit_code"]) == 0 else "failure"
                except (TypeError, ValueError):
                    pass
            if data.get("error"):
                return "failure"
            return "success"  # structured result, no error signal
    except (ValueError, TypeError):
        pass
    low = text.lower().lstrip()
    for sig in _LEADING_ERROR:
        if low.startswith(sig):
            return "failure"
    return "success"


# --------------------------------------------------------------------------
# Tool aggregation
# --------------------------------------------------------------------------

def aggregate_tools(events):
    """Aggregate tool events into per-tool metrics (sorted by count desc).

    Each event: {'name': str, 'latency_ms': float|None, 'status': str}.
    success_rate is computed over classified events only (unknown excluded).
    """
    by_name = {}
    for ev in events:
        name = ev.get("name") or "unknown"
        rec = by_name.setdefault(name, {
            "count": 0, "success": 0, "failure": 0, "unknown": 0,
            "latencies": [],
        })
        rec["count"] += 1
        status = ev.get("status") or "unknown"
        rec[status] = rec.get(status, 0) + 1
        if ev.get("latency_ms") is not None:
            rec["latencies"].append(ev["latency_ms"])

    out = []
    for name, rec in by_name.items():
        classified = rec["success"] + rec["failure"]
        rate = (rec["success"] / classified) if classified else None
        lat = sorted(rec["latencies"])

        def pct(p):
            if not lat:
                return None
            idx = min(len(lat) - 1, int(p * (len(lat) - 1)))
            return round(lat[idx], 1)

        out.append({
            "name": name,
            "count": rec["count"],
            "success": rec["success"],
            "failure": rec["failure"],
            "unknown": rec["unknown"],
            "success_rate": round(rate, 3) if rate is not None else None,
            "latency_avg_ms": round(statistics.mean(lat), 1) if lat else None,
            "latency_median_ms": round(statistics.median(lat), 1) if lat else None,
            "latency_p95_ms": pct(0.95),
        })
    out.sort(key=lambda r: r["count"], reverse=True)
    return out


# --------------------------------------------------------------------------
# Session / model / task / daily / health
# --------------------------------------------------------------------------

def _sum(key, rows):
    return sum((r.get(key) or 0) for r in rows)


def _day(ts):
    if not ts:
        return None
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d")


def _cache_hit_ratio(cache_read, fresh_input):
    total = cache_read + fresh_input
    return round(cache_read / total, 4) if total else None


def _accumulate_usage(usage, key_fn, with_sessions=False):
    """Sum the canonical usage-row field set into per-key accumulators.

    The ONE place the token/cost field list is encoded for
    `session_model_usage` rows. Callers (model_mix, task_mix) project their
    own output shape and sort order. `reasoning_tokens` is always summed
    (harmless — a caller that doesn't emit it simply omits the field).
    """
    agg = {}
    for r in usage:
        rec = agg.setdefault(key_fn(r), {
            "api_calls": 0, "input_tokens": 0, "output_tokens": 0,
            "cache_read_tokens": 0, "reasoning_tokens": 0,
            "estimated_cost_usd": 0.0,
        })
        if with_sessions:
            rec.setdefault("session_ids", set())
            if r.get("session_id"):
                rec["session_ids"].add(r["session_id"])
        rec["api_calls"] += r.get("api_call_count") or 0
        rec["input_tokens"] += r.get("input_tokens") or 0
        rec["output_tokens"] += r.get("output_tokens") or 0
        rec["cache_read_tokens"] += r.get("cache_read_tokens") or 0
        rec["reasoning_tokens"] += r.get("reasoning_tokens") or 0
        rec["estimated_cost_usd"] += r.get("estimated_cost_usd") or 0.0
    return agg


def session_totals(sessions):
    """Totals across all sessions (tokens, cost, counts, active days).

    cache_hit_ratio = cache_read / (cache_read + fresh input) — the policy's
    #1 cost lever (cache-hit $0.022 vs cache-miss $0.66 per 1M).
    output_token_share = output / (cache_read + input + output) — normalizes
    the other lever (output is 90× cache-hit input).
    """
    sessions = list(sessions)
    cache_read = _sum("cache_read_tokens", sessions)
    input_fresh = _sum("input_tokens", sessions)
    output = _sum("output_tokens", sessions)
    all_tokens = cache_read + input_fresh + output
    return {
        "sessions": len(sessions),
        "messages": _sum("message_count", sessions),
        "tool_calls": _sum("tool_call_count", sessions),
        "api_calls": _sum("api_call_count", sessions),
        "input_tokens": input_fresh,
        "output_tokens": output,
        "cache_read_tokens": cache_read,
        "reasoning_tokens": _sum("reasoning_tokens", sessions),
        "cache_hit_ratio": _cache_hit_ratio(cache_read, input_fresh),
        "output_token_share": round(output / all_tokens, 4) if all_tokens else None,
        "estimated_cost_usd": round(_sum("estimated_cost_usd", sessions), 4),
        "active_days": len({_day(r.get("started_at")) for r in sessions if r.get("started_at")}),
    }


def model_mix(usage):
    """Per-model totals (tokens, cost, api calls, distinct sessions), sorted by cost desc.

    `sessions` counts distinct session_ids (the usage table has a `task`
    dimension, so one session can contribute several rows per model).
    """
    agg = _accumulate_usage(
        usage, key_fn=lambda r: r.get("model") or "unknown", with_sessions=True,
    )
    out = []
    for model, rec in agg.items():
        out.append({
            "model": model,
            "sessions": len(rec["session_ids"]),
            "api_calls": rec["api_calls"],
            "input_tokens": rec["input_tokens"],
            "output_tokens": rec["output_tokens"],
            "cache_read_tokens": rec["cache_read_tokens"],
            "cache_hit_ratio": _cache_hit_ratio(rec["cache_read_tokens"], rec["input_tokens"]),
            "estimated_cost_usd": round(rec["estimated_cost_usd"], 4),
        })
    out.sort(key=lambda r: r["estimated_cost_usd"], reverse=True)
    return out


def task_mix(usage):
    """Per-task × per-model cost/tokens, sorted by cost desc.

    `task` is '' (main), 'compression', or 'approval'. TOKEN_EFFICIENCY.md
    requires aux tasks to route to deepseek-v4-flash; this view makes any
    primary-model aux spend visible instead of silently dropped.
    """
    agg = _accumulate_usage(
        usage, key_fn=lambda r: (r.get("task") or "main", r.get("model") or "unknown"),
    )
    out = []
    for (task, model), rec in agg.items():
        out.append({
            "task": task,
            "model": model,
            "api_calls": rec["api_calls"],
            "input_tokens": rec["input_tokens"],
            "output_tokens": rec["output_tokens"],
            "cache_read_tokens": rec["cache_read_tokens"],
            "reasoning_tokens": rec["reasoning_tokens"],
            "estimated_cost_usd": round(rec["estimated_cost_usd"], 4),
        })
    out.sort(key=lambda r: r["estimated_cost_usd"], reverse=True)
    return out


def daily_buckets(sessions, last_n=30):
    """Per-day activity buckets (most recent `last_n` days), incl. per-day cache-hit ratio."""
    buckets = {}
    for r in sessions:
        day = _day(r.get("started_at"))
        if not day:
            continue
        b = buckets.setdefault(day, {
            "sessions": 0, "messages": 0, "tool_calls": 0,
            "input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0,
            "estimated_cost_usd": 0.0,
        })
        b["sessions"] += 1
        b["messages"] += r.get("message_count") or 0
        b["tool_calls"] += r.get("tool_call_count") or 0
        b["input_tokens"] += r.get("input_tokens") or 0
        b["output_tokens"] += r.get("output_tokens") or 0
        b["cache_read_tokens"] += r.get("cache_read_tokens") or 0
        b["estimated_cost_usd"] += r.get("estimated_cost_usd") or 0.0
    out = []
    for d in sorted(buckets.keys())[-last_n:]:
        b = buckets[d]
        out.append({
            "date": d,
            "sessions": b["sessions"],
            "messages": b["messages"],
            "tool_calls": b["tool_calls"],
            "input_tokens": b["input_tokens"],
            "output_tokens": b["output_tokens"],
            "cache_read_tokens": b["cache_read_tokens"],
            "cache_hit_ratio": _cache_hit_ratio(b["cache_read_tokens"], b["input_tokens"]),
            "estimated_cost_usd": round(b["estimated_cost_usd"], 4),
        })
    return out


def health(sessions):
    """Body-health signals: compression failures, rewinds, end reasons."""
    reasons = {}
    for r in sessions:
        er = r.get("end_reason") or "unknown"
        reasons[er] = reasons.get(er, 0) + 1
    return {
        "compression_failure_errors": sum(1 for r in sessions if r.get("compression_failure_error")),
        "compression_ineffective_count": _sum("compression_ineffective_count", sessions),
        "compression_fallback_streak_max": max((r.get("compression_fallback_streak") or 0) for r in sessions) if sessions else 0,
        "rewinds": _sum("rewind_count", sessions),
        "end_reasons": dict(sorted(reasons.items())),
    }


# --------------------------------------------------------------------------
# Summary
# --------------------------------------------------------------------------

def summarize(sessions, usage, events, last_n=30):
    """The full analytics report (no `generated_at` — the caller stamps it).

    `generated_at` is a collection-time concern, so it lives in the script
    (mirrors scripts/insights.py), keeping this core module pure/deterministic.
    """
    return {
        "totals": session_totals(sessions),
        "models": model_mix(usage),
        "tasks": task_mix(usage),
        "tools": aggregate_tools(events),
        "daily": daily_buckets(sessions, last_n=last_n),
        "health": health(sessions),
        "notes": [
            "success_rate = share of results with no explicit error signal (JSON success=false / exit_code!=0 / error field, or leading error text) — heuristic, not ground truth",
            "cost figures are 'estimated' (DeepSeek pricing), not invoice-actual",
            "cache_hit_ratio = cache_read / (cache_read + fresh input); output_token_share = output / all tokens — the two levers named in TOKEN_EFFICIENCY.md",
        ],
    }
