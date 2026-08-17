"""Session-DB read adapter — typed, named-column rows, never positional.

The review driver's session-DB reads used to each run
``PRAGMA table_info(sessions)`` and hand-advance a positional index — a layout
that already produced one off-by-one bug (the "cwd mis-scope bug", where
``cwd`` was misread as ``last_activity_at``). This module is the single owner
of that schema: it returns rows keyed by column name, so a column added or
reordered can never shift an index.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


def session_columns(state_db: Path) -> Optional[set]:
    """Column names of the ``sessions`` table.

    Returns ``set()`` when the DB is missing, and ``None`` when the schema
    cannot be inspected (a transient lock). Callers MUST treat ``None`` as
    "do not proceed" — never as "no columns", which would silently drop the
    ``ended_at`` filter and let a review touch a still-open session.
    """
    if not state_db.exists():
        return set()
    try:
        conn = sqlite3.connect(str(state_db), timeout=5)
        try:
            return {r[1] for r in conn.execute("PRAGMA table_info(sessions)")}
        finally:
            conn.close()
    except sqlite3.Error:
        return None


def load_session(state_db: Path, session_id: str) -> Optional[Dict[str, Any]]:
    """Read the session row + ordered messages, as named-column values.

    Returns None when the DB is missing, the row is absent, or the schema
    cannot be read. ``as_of`` is the session's end/last-activity time as a
    Unix float (from ``ended_at``, else ``last_activity_at``); ``ended`` is
    None when the ``ended_at`` column is absent (unknown).
    """
    if not state_db.exists():
        return None
    conn = sqlite3.connect(str(state_db), timeout=5)
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(sessions)")}
        select = ["source", "title"]
        for c in ("ended_at", "last_activity_at", "cwd"):
            if c in cols:
                select.append(c)
        row = conn.execute(
            f"SELECT {', '.join(select)} FROM sessions WHERE id = ?",
            (session_id,),
        ).fetchone()
        if row is None:
            return None
        rec = dict(zip(select, row))
        as_of: Optional[float] = None
        for c in ("ended_at", "last_activity_at"):
            if c in cols and as_of is None and isinstance(rec.get(c), (int, float)):
                as_of = float(rec[c])
        ended: Optional[bool] = None
        if "ended_at" in cols:
            ended = rec.get("ended_at") is not None
        msgs = conn.execute(
            "SELECT role, content, tool_name FROM messages "
            "WHERE session_id = ? AND active = 1 ORDER BY id",
            (session_id,),
        ).fetchall()
    except sqlite3.Error:
        return None
    finally:
        conn.close()
    return {
        "source": rec.get("source") or "",
        "title": rec.get("title") or "",
        "as_of": as_of,
        "ended": ended,
        "cwd": rec.get("cwd") or "",
        "messages": [
            {"role": role or "", "content": content or "", "tool_name": tool_name or ""}
            for role, content, tool_name in msgs
        ],
    }


def candidate_rows(state_db: Path, cols: set) -> List[Dict[str, Any]]:
    """The raw candidate session rows (ended, top-level, not hidden/archived),
    newest first, as named-column dicts (``id``, ``source``, ``cwd`` when the
    column exists). ``[]`` on a query error; the caller owns the fail-safe
    ``cols is None`` decision before calling."""
    where = []
    if "ended_at" in cols:
        where.append("ended_at IS NOT NULL")      # skip the live session
    if "parent_session_id" in cols:
        where.append("parent_session_id IS NULL")  # skip delegated subagents
    if "hidden" in cols:
        where.append("hidden = 0")
    if "archived" in cols:
        where.append("archived = 0")
    select = ["id", "source"]
    if "cwd" in cols:
        select.append("cwd")
    sql = f"SELECT {', '.join(select)} FROM sessions"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id DESC"
    try:
        conn = sqlite3.connect(str(state_db), timeout=5)
        try:
            rows = conn.execute(sql).fetchall()
        finally:
            conn.close()
    except sqlite3.Error:
        return []
    return [dict(zip(select, row)) for row in rows]
