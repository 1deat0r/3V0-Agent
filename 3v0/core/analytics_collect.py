"""Collection half of self-analytics (Stone 22 architecture pass).

Reads the 3V0 state DB and turns raw rows into the inputs
`core.analytics.summarize` consumes. Collection-at-the-edge, mirroring
`core/session_db.py` / `core/gitstate.py`: every function takes the DB path as
a parameter — no profile/global I/O, no environment reads, no CLI coupling.
"""

from __future__ import annotations

import json
import sqlite3

from core.analytics import classify_tool_result


def _rows(db, sql):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql)]
    finally:
        conn.close()


def load_sessions(db):
    return _rows(db, """
        SELECT started_at, ended_at, end_reason, message_count, tool_call_count,
               api_call_count, input_tokens, output_tokens, cache_read_tokens,
               reasoning_tokens, estimated_cost_usd, rewind_count,
               compression_failure_error, compression_ineffective_count,
               compression_fallback_streak
        FROM sessions
    """)


def load_usage(db):
    return _rows(db, """
        SELECT session_id, model, task, api_call_count, input_tokens, output_tokens,
               cache_read_tokens, reasoning_tokens, estimated_cost_usd
        FROM session_model_usage
    """)


def build_events(db):
    """Match tool results to their issuing call for latency; classify success.

    The subtle bit: an assistant message carries `tool_calls` (JSON list with
    `id`/`call_id` + `name`); the matching tool result carries the same
    `tool_call_id`. Latency = (result.timestamp - call.timestamp) × 1000, with
    a negative-latency guard (clock skew / reordering → None).
    """
    rows = _rows(db, """
        SELECT role, tool_name, tool_call_id, tool_calls, content, timestamp
        FROM messages
        WHERE role IN ('tool', 'assistant')
    """)
    call_time = {}
    for m in rows:
        if m["role"] == "assistant" and m.get("tool_calls"):
            try:
                calls = json.loads(m["tool_calls"])
            except (ValueError, TypeError):
                continue
            for c in calls:
                cid = c.get("id") or c.get("call_id")
                if cid:
                    call_time[cid] = m.get("timestamp")
    events = []
    for m in rows:
        if m["role"] != "tool":
            continue
        lat = None
        t0 = call_time.get(m.get("tool_call_id"))
        if t0 is not None and m.get("timestamp") is not None:
            lat = (m["timestamp"] - t0) * 1000.0
            if lat < 0:
                lat = None
        events.append({
            "name": m.get("tool_name") or "unknown",
            "latency_ms": lat,
            "status": classify_tool_result(m.get("content")),
        })
    return events
