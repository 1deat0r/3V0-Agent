"""Memory consolidation & conflict reconciliation ("MindMemOS", arXiv 2608.12428).

MindMemOS's consolidation ("dreaming") phase merges redundant records and
resolves conflicts so the store holds one coherent current truth. This module
implements the deterministic reconciliation half on the existing memdb seam.

Conflict identity is the **chain anchor** — not the (subject, predicate) key.
The canonical pipeline writes every fact under the container key
(('3v0', 'note'), see ``SQLStore.add``), so a (subject, predicate) pair never
identifies "the same assertion": 31 distinct notes under one container key
would read as one 31-way conflict and reconciliation would destroy 30 of them.
The schema's only honest same-assertion signal is the ``supersedes`` link — a
correction points at the fact it replaces, and distinct notes never link. A
fact's chain anchor is the root of its ``supersedes`` lineage; unlinked facts
anchor to themselves.

- ``chain_anchor(conn, fact_id)`` — the lineage root of a fact (walk
  ``supersedes`` to the oldest ancestor; unlinked facts anchor to themselves).
- ``pending_consolidations(conn)`` — every chain currently holding **more than
  one valid member** (the supersession invariant breach), for reporting /
  scheduling a dreaming pass. Distinct unlinked notes are singleton chains and
  are never reported.
- ``reconcile(conn, root_id, *, keep="newest", now=None)`` — repair one broken
  chain by closing (valid_to = now) every valid member except the keeper, so
  exactly one current truth survives per chain. Reuses the memdb convention
  "inactive iff valid_to IS NOT NULL", so reconciled-away facts can never be
  injected (governance fail-close holds automatically).

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
    root_id: int          # the chain anchor (lineage root) of these facts
    subject: str          # the anchor's subject (reporting; container-key-aware)
    predicate: str        # the anchor's predicate (reporting)
    facts: list[dict]     # VALID members of the chain, id DESC
    distinct_contents: int

    @property
    def conflicting(self) -> bool:
        return self.distinct_contents > 1


def chain_anchor(conn, fact_id) -> int:
    """The lineage root of ``fact_id``: walk ``supersedes`` to the oldest
    ancestor; an unlinked fact anchors to itself. Cycle-bounded (a hand-edited
    cycle terminates at a member, never hangs)."""
    seen = set()
    cur = fact_id
    while cur is not None and cur not in seen:
        row = conn.execute(
            "SELECT supersedes FROM facts WHERE id=?", (cur,)).fetchone()
        if row is None or row["supersedes"] is None:
            return cur
        seen.add(cur)
        cur = row["supersedes"]
    return cur


def _chain_members(conn, root_id) -> list[dict]:
    """The full lineage of a chain: ``root_id`` plus every descendant via
    ``supersedes`` (bounded; the store is small, so an in-memory pass is fine)."""
    rows = [dict(r) for r in conn.execute("SELECT * FROM facts").fetchall()]
    parents = {r["id"]: r for r in rows}
    children: dict[int, list[dict]] = {}
    for r in rows:
        if r["supersedes"] is not None:
            children.setdefault(r["supersedes"], []).append(r)
    members: list[dict] = []
    seen = set()
    stack = [root_id]
    while stack:
        fid = stack.pop()
        if fid in seen:
            continue
        seen.add(fid)
        parent = parents.get(fid)
        if parent is not None:
            members.append(parent)
            stack.extend(r["id"] for r in children.get(fid, []))
    return members


def pending_consolidations(conn, *, now=None) -> list[KeyState]:
    """All chains currently holding more than one valid member — the
    supersession-invariant breach consolidation repairs. Distinct unlinked
    notes anchor to themselves and are never reported."""
    groups: dict[int, list[dict]] = {}
    for f in memdb.valid_facts(conn, now=now):
        groups.setdefault(chain_anchor(conn, f["id"]), []).append(f)
    out = []
    for anchor, facts in sorted(groups.items()):
        facts = sorted(facts, key=lambda r: r.get("id") or 0, reverse=True)
        if len(facts) > 1:
            row = conn.execute(
                "SELECT subject, predicate FROM facts WHERE id=?",
                (anchor,)).fetchone()
            out.append(KeyState(
                root_id=anchor,
                subject=str(row["subject"]) if row else "",
                predicate=str(row["predicate"]) if row else "",
                facts=facts,
                distinct_contents=len({f.get("content") for f in facts}),
            ))
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


def reconcile(conn, root_id, *, keep: str = "newest",
              now=None) -> ReconcileResult:
    """Repair one chain: close every VALID member except the keeper.

    ``root_id`` is the chain anchor returned by ``pending_consolidations``.
    ``keep``: "newest" → keep the highest-id valid member (latest assertion).
    Returns the closed ids; a no-op when the chain already holds one truth.
    Commits the writes (mirrors memdb.add_fact's persist=True default).
    """
    now = now if now is not None else time.time()
    members = _chain_members(conn, root_id)
    valid = [m for m in members if m.get("valid_to") is None]
    root_row = next((m for m in members if m.get("id") == root_id), None)
    if len(valid) <= 1:
        keeper = valid[0] if valid else None
        return ReconcileResult(
            subject=str(root_row.get("subject") or "") if root_row else "",
            predicate=str(root_row.get("predicate") or "") if root_row else "",
            keeper_id=keeper.get("id") if keeper else None,
            closed=[],
            kept_content=keeper.get("content") if keeper else None,
        )

    ordered = sorted(valid, key=lambda r: r.get("id") or 0, reverse=True)
    keeper = ordered[0]
    close_ids = [m["id"] for m in ordered[1:] if m.get("id") != keeper.get("id")]
    if close_ids:
        conn.executemany(
            "UPDATE facts SET valid_to = ? WHERE id = ? AND valid_to IS NULL",
            [(now, cid) for cid in close_ids])
        conn.commit()
    return ReconcileResult(
        subject=str(root_row.get("subject") or "") if root_row else "",
        predicate=str(root_row.get("predicate") or "") if root_row else "",
        keeper_id=keeper.get("id"),
        closed=close_ids,
        kept_content=keeper.get("content"),
    )