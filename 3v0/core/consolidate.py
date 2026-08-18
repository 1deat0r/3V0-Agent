"""Memory consolidation & conflict reconciliation ("MindMemOS", arXiv 2608.12428).

MindMemOS's consolidation ("dreaming") phase merges redundant records and
resolves conflicts so the store holds one coherent current truth. This module
implements the deterministic reconciliation half on the existing memdb seam:

- ``conflicting_valid(conn, subject, predicate)`` — valid facts under one key
  whose content disagrees (the same topic asserted more than one way).
- ``reconcile(conn, subject, predicate, *, keep="newest", now=None)`` — resolve
  a conflicting key by closing (valid_to = now) every valid duplicate except the
  keeper, so exactly one current truth survives. Reuses the memdb convention
  "inactive iff valid_to IS NOT NULL", so reconciled-away facts can never be
  injected (governance fail-close holds automatically).
- ``pending_consolidations(conn)`` — all conflicting keys, for reporting /
  scheduling a dreaming pass.

Consolidation is *correctness-preserving only when the newer assertion is the
true one*; keep="newest" is an explicit policy parameter, not a hidden default
for evidence. This writes validity, nothing else: no content is mutated, so a
reconcile is reversible by restoring a closed fact's valid_to.
"""

from __future__ import annotations
import time
from dataclasses import dataclass

from . import memdb


@dataclass
class KeyState:
    subject: str
    predicate: str
    facts: list[dict]      # valid facts under this key, created_at DESC
    distinct_contents: int

    @property
    def conflicting(self) -> bool:
        return self.distinct_contents > 1


def _key(row: dict) -> tuple[str, str]:
    return (str(row.get("subject") or ""), str(row.get("predicate") or ""))


def conflicting_valid(conn, subject: str, predicate: str, *, now=None):
    """Valid facts with this (subject, predicate) that disagree in content."""
    facts = [f for f in memdb.valid_facts(conn, now=now)
             if _key(f) == (subject, predicate)]
    distinct = {f.get("content") for f in facts}
    return [f for f in facts] if len(distinct) > 1 else []


def pending_consolidations(conn, *, now=None) -> list[KeyState]:
    """All (subject, predicate) keys currently holding conflicting truths."""
    seen: dict[tuple[str, str], list[dict]] = {}
    for f in memdb.valid_facts(conn, now=now):
        seen.setdefault(_key(f), []).append(f)
    out = []
    for key, facts in seen.items():
        distinct = {f.get("content") for f in facts}
        if len(distinct) > 1:
            facts = sorted(facts, key=lambda r: r.get("id") or 0, reverse=True)
            out.append(KeyState(key[0], key[1], facts, len(distinct)))
    return out


@dataclass
class ReconcileResult:
    subject: str
    predicate: str
    keeper_id: int | None
    closed: list[int]        # ids whose validity was closed (superseded away)
    kept_content: str | None

    @property
    def reconciled(self) -> bool:
        return bool(self.closed)


def reconcile(conn, subject: str, predicate: str, *, keep: str = "newest",
              now=None) -> ReconcileResult:
    """Resolve a conflicting key: close every valid duplicate but the keeper.

    ``keep``: "newest" → keep the highest-id valid fact (latest assertion).
    Returns the closed ids; a no-op when the key is not conflict...lconflicting.
    Commits the writes (mirrors memdb.add_fact's persist=True default).
    """
    now = now if now is not None else time.time()
    candidates = [f for f in memdb.valid_facts(conn, now=now)
                  if _key(f) == (subject, predicate)]
    distinct = {f.get("content") for f in candidates}
    if len(distinct) <= 1:
        return ReconcileResult(subject, predicate, None, [], None)

    ordered = sorted(candidates, key=lambda r: r.get("id") or 0, reverse=True)
    keeper = ordered[0]
    close_ids = [f["id"] for f in ordered[1:] if f.get("id") != keeper.get("id")]
    if close_ids:
        conn.executemany(
            "UPDATE facts SET valid_to = ? WHERE id = ? AND valid_to IS NULL",
            [(now, cid) for cid in close_ids])
        conn.commit()
    return ReconcileResult(subject, predicate, keeper.get("id"), close_ids,
                           keeper.get("content"))