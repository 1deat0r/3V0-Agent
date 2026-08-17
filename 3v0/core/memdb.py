"""SQLite-backed memory: a temporal knowledge graph for 3V0 (Stone 21).

The first stone of the memory rework. Replaces the flat JSON fact list with a
queryable triple-store so memory scales past the injected-2KB bottleneck:

  - every fact is a (subject, predicate, object) triple
  - temporal validity (valid_from / valid_to) — a fact can *stop being true*
  - provenance (source) + confidence
  - a sub-memory `domain` tag (3v0 / f1nance / axiom / money / env / …)
  - retrieval feedback (access_count / last_accessed) so retrieval can rank
    by what's actually used, and forgetting/consolidation has a signal

The profile MEMORY.md is meant to become a *derived, retrieval-chosen view*
of this store — not the source of truth. This module is storage only; ranking
and selection live in ``core/retrieval.py`` (pure and importable without a DB
— invariant #4: decision logic testable in isolation).

I/O lives here (sqlite3); the thin CLI + the pipeline rewire are later stones.
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS facts (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    subject       TEXT NOT NULL,
    predicate     TEXT NOT NULL,
    object        TEXT NOT NULL,
    domain        TEXT NOT NULL DEFAULT '3v0',
    valid_from    REAL NOT NULL,
    valid_to      REAL,              -- NULL = still valid
    confidence    REAL NOT NULL DEFAULT 1.0,
    source        TEXT,              -- provenance (session id / operator / inference)
    supersedes    INTEGER,           -- FK -> facts.id this fact replaces
    kind          TEXT NOT NULL DEFAULT 'memory',  -- memory | user | identity | directive
    note          TEXT NOT NULL DEFAULT '',        -- provenance note (retractions etc.)
    content       TEXT,              -- natural-language form (for retrieval/embedding later)
    access_count  INTEGER NOT NULL DEFAULT 0,
    last_accessed REAL,
    created_at    REAL NOT NULL,
    FOREIGN KEY (supersedes) REFERENCES facts(id)
);
CREATE INDEX IF NOT EXISTS idx_facts_domain ON facts(domain, valid_from);
CREATE INDEX IF NOT EXISTS idx_facts_subject ON facts(subject);
"""

# Absolute (repo-relative via __file__), not CWD-relative: a caller that
# imports memdb from any working directory still lands the DB in 3v0/data/.
DEFAULT_PATH = str(Path(__file__).resolve().parent.parent / "data" / "memory.db")


def connect(path=DEFAULT_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    # Enforce the supersedes FK — without this, add_fact(..., supersedes=<bad id>)
    # inserts silently instead of failing.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def add_fact(conn, subject, predicate, object_, domain="3v0", valid_from=None,
             valid_to=None, confidence=1.0, source=None, supersedes=None,
             content=None, kind="memory", note="", now=None, persist=True):
    """Insert a fact; if it supersedes another, close the old one's validity.

    ``persist=False`` leaves the insert (and the supersession close)
    uncommitted — visible to this connection only, so a dry-run caller can
    report the result without writing disk.
    """
    now = now if now is not None else time.time()
    if valid_from is None:
        valid_from = now
    if supersedes is not None:
        conn.execute(
            "UPDATE facts SET valid_to = ? WHERE id = ? AND valid_to IS NULL",
            (now, supersedes),
        )
    cur = conn.execute(
        """INSERT INTO facts (subject, predicate, object, domain, valid_from,
                              valid_to, confidence, source, supersedes, content,
                              kind, note, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (subject, predicate, object_, domain, valid_from, valid_to,
         confidence, source, supersedes, content, kind, note, now),
    )
    if persist:
        conn.commit()
    return cur.lastrowid


def valid_facts(conn, domain=None, kind=None, now=None):
    """Facts currently true (valid_to IS NULL), optionally scoped."""
    now = now if now is not None else time.time()
    sql = ("SELECT * FROM facts WHERE (valid_to IS NULL OR valid_to > ?)"
           " AND valid_from <= ?")
    params = [now, now]
    if domain is not None:
        sql += " AND domain = ?"
        params.append(domain)
    if kind is not None:
        sql += " AND kind = ?"
        params.append(kind)
    sql += " ORDER BY created_at DESC, id DESC"
    return [dict(r) for r in conn.execute(sql, params)]


def _parse_iso(iso):
    """ISO-8601 UTC ('2026-08-10T00:00:00Z') -> epoch, or None."""
    import calendar
    try:
        return float(calendar.timegm(time.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")))
    except (ValueError, TypeError):
        return None


def migrate_from_json(conn, facts, domain="3v0", now=None):
    """Tolerant import of legacy facts (list of dicts), two shapes.

    Fact-shaped (the live memory.json): id/kind/source/created_at/supersedes/
    superseded_by. Two passes so supersession links survive the hex->row-id
    remap: every row is inserted with its original created_at preserved, then
    each superseded fact's valid_to is closed at its successor's created_at
    and the successor's ``supersedes`` FK points at it. A ``retracted``
    tombstone closes valid_to at its own created_at — the JSON sentinel has
    no timestamp of its own, so the row becomes never-valid, kept for audit.

    Loose dicts (the tolerant core): subject/predicate/object/domain
    heuristics, no links.
    """
    now = now if now is not None else time.time()
    shaped = [f for f in facts if isinstance(f, dict) and "id" in f and "kind" in f]
    if shaped:
        return _migrate_shaped(conn, shaped, domain, now)
    n = 0
    for f in facts:
        content = f.get("content") or f.get("text") or f.get("object")
        object_ = f.get("object") or content or ""
        add_fact(
            conn,
            subject=f.get("subject") or "3v0",
            predicate=f.get("predicate") or "note",
            object_=str(object_),
            domain=f.get("domain") or domain,
            valid_from=f.get("valid_from") or f.get("timestamp") or now,
            confidence=f.get("confidence", 1.0),
            source=f.get("source"),
            content=str(content) if content is not None else None,
            now=now,
            persist=False,
        )
        n += 1
    conn.commit()
    return n


def _migrate_shaped(conn, facts, domain, now):
    """Fact-shaped migration: hex ids remapped, lineage + validity preserved."""
    hex_to_row: dict[str, int] = {}
    pending = []  # (row_id, supersedes hex ids, superseded_by, created_at)
    for f in facts:
        content = f.get("content") or ""
        created = _parse_iso(f.get("created_at")) or now
        row_id = add_fact(
            conn, "3v0", "note", str(content), domain=domain,
            valid_from=created,
            source=f.get("source"),
            content=str(content) if content else None,
            kind=f.get("kind") or "memory",
            note=f.get("note") or "",
            now=created,
            persist=False,
        )
        hex_to_row[f["id"]] = row_id
        pending.append((row_id, f.get("supersedes") or [],
                        f.get("superseded_by") or "", created))
    for row_id, sups, sup_by, created in pending:
        if sups:
            for hex_id in sups:
                old = hex_to_row.get(hex_id)
                if old is not None:
                    conn.execute(
                        "UPDATE facts SET valid_to=? WHERE id=? AND valid_to IS NULL",
                        (created, old))
            first = hex_to_row.get(sups[0])
            if first is not None:
                conn.execute("UPDATE facts SET supersedes=? WHERE id=?",
                             (first, row_id))
        if sup_by == "retracted":
            conn.execute("UPDATE facts SET valid_to=? WHERE id=?", (created, row_id))
    conn.commit()
    return len(pending)
