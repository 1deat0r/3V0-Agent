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
             content=None, now=None):
    """Insert a fact; if it supersedes another, close the old one's validity."""
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
                              created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (subject, predicate, object_, domain, valid_from, valid_to,
         confidence, source, supersedes, content, now),
    )
    conn.commit()
    return cur.lastrowid


def valid_facts(conn, domain=None, now=None):
    """Facts currently true (valid_to IS NULL), optionally scoped to a domain."""
    now = now if now is not None else time.time()
    sql = ("SELECT * FROM facts WHERE (valid_to IS NULL OR valid_to > ?)"
           " AND valid_from <= ?")
    params = [now, now]
    if domain is not None:
        sql += " AND domain = ?"
        params.append(domain)
    sql += " ORDER BY created_at DESC"
    return [dict(r) for r in conn.execute(sql, params)]


def migrate_from_json(conn, facts, domain="3v0", now=None):
    """Tolerant import of legacy memory.json facts (list of dicts).

    Maps flexible keys (content/text/object, source) onto the triple schema.
    Returns the number of facts inserted. Wiring to the live memory.json is
    part of the pipeline-rewire stone; this is the tolerant core.
    """
    now = now if now is not None else time.time()
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
            supersedes=f.get("supersedes"),
            content=str(content) if content is not None else None,
            now=now,
        )
        n += 1
    return n
