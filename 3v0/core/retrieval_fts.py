"""FTS5-backed relevance for retrieval (stone 1: indexed, BM25, fast).

Replaces the naive Python substring scan ('term in hay') with a SQLite FTS5
virtual table over the fact's searchable text, ranked by SQLite's BM25 rank.
This gives (a) REAL word-level relevance instead of substring presence and
(b) speed: a MATCH query narrows candidates without an O(N) Python pass, so
retrieval stays cheap as the store grows huge.

The FTS table lives ON the memdb connection (in-memory) and is refreshed only
when the fact set changes (fingerprint cache) — so repeated injects on a live
connection do not rebuild it every call. A persistent sidecar can come later
if the store outgrows a per-connection build.
"""
from __future__ import annotations

_TABLE = "fts_facts"
_META = "fts_meta"


def _fingerprint(facts) -> tuple:
    """Cheap staleness key for the FTS cache: count + max id + max updated."""
    return (len(facts), max((f.get("id", 0) for f in facts), default=0))


def _token(fact) -> str:
    """The searchable text of a fact (fields a query might mean)."""
    return " ".join(str(fact.get(k) or "") for k in
                    ("subject", "predicate", "object", "content"))


def _has_table(conn, table: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone() is not None


def _stored_fingerprint(conn):
    if not _has_table(conn, _META):
        return None
    row = conn.execute(f"SELECT value FROM {_META} WHERE key='fp'").fetchone()
    return eval(row[0]) if row else None  # noqa: S307 - internal small tuple


def ensure_index(conn, facts, searchable_filter=None) -> bool:
    """Create/refresh the FTS index on ``conn`` over ``facts`` (id + text).

    Returns True when the index was (re)built this call, False when cached and
    reused. Rebuilds only when the fact fingerprint changed.
    """
    fp = _fingerprint(facts)
    if _stored_fingerprint(conn) == fp and _has_table(conn, _TABLE):
        return False
    if _has_table(conn, _TABLE):
        conn.execute(f"DROP TABLE {_TABLE}")
    conn.execute(f"CREATE VIRTUAL TABLE {_TABLE} USING fts5(id UNINDEXED, body)")
    for f in facts:
        body = _token(f)
        if searchable_filter and not searchable_filter(body):
            continue
        conn.execute(f"INSERT INTO {_TABLE} (id, body) VALUES (?, ?)",
                     (f.get("id"), body))
    conn.execute(f"CREATE TABLE IF NOT EXISTS {_META} (key TEXT PRIMARY KEY, value TEXT)")
    conn.execute(f"INSERT OR REPLACE INTO {_META} (key, value) VALUES ('fp', ?)",
                 (repr(fp),))
    conn.commit()
    return True


def match(conn, terms, limit: int = 100) -> list[tuple]:
    """Top-N facts (id, bm25) matching ANY quoted term, best BM25 first.

    bm25() in SQLite returns NEGATIVE scores with more-negative = better match,
    so ORDER BY bm25 ASC returns best-first. Returns [] when no term is usable.
    """
    usable = [t for t in terms if isinstance(t, str) and len(t.strip()) >= 2]
    if not usable:
        return []
    query = " OR ".join(f'"{t.strip()}"' for t in usable)
    try:
        rows = conn.execute(
            f"SELECT id, bm25({_TABLE}) FROM {_TABLE} "
            f"WHERE {_TABLE} MATCH ? ORDER BY 2 ASC LIMIT ?",
            (query, limit),
        ).fetchall()
    except Exception:
        return []
    return [(fid, bm25) for fid, bm25 in rows]


def candidate_ids(conn, terms, limit: int = 200) -> set:
    """Set of fact ids that word-match any query term (fast narrowing)."""
    return {fid for fid, _ in match(conn, terms, limit)}
