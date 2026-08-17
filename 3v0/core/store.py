"""SQLStore — the canonical store facade over the memdb triple substrate.

The rewire stone's write half: the pipeline (record/bridge/sync/decide/review)
already speaks one store interface — add/retract/active/matching/get/history/
export/mutate with ``Fact``-shaped results. SQLStore satisfies that contract
with the SQLite triple store behind it, so the callers' logic is untouched
while the store gains temporal validity, domains, kinds, and retrieval
feedback. ADR-0004's seam (``core.retrieval.inject``) is the read half.

Facade mapping:
- A pipeline fact is the triple (subject='3v0', predicate='note', object=<content>)
  plus its kind, source, and supersession links; the ``content`` column carries
  the natural-language form retrieval ranks over.
- Supersession closes the old row's ``valid_to`` at the new fact's timestamp;
  ``history()`` rebuilds the chain by following the ``supersedes`` FK both ways.
- Retraction is a row whose ``valid_to`` closed with no successor — the JSON
  RETRACTED sentinel, expressed as a fact that is simply no longer valid.
- ``mutate()`` yields the store under SQLite's own transaction discipline (no
  cross-process file lock needed); ``persist=False`` leaves changes
  uncommitted — visible to this connection only, the dry-run contract.
- Missing store = empty store, JSON parity: reads degrade to empty, the first
  write creates the file (like ``MemoryStore._save``'s mkdir).

Lineage semantics (kind validity, retraction tagging, the supersession walk,
the export grouping) are owned by ``core.lineage`` — the single source shared
with ``MemoryStore`` so the two backends cannot drift on meaning. The sqlite
connection is an implementation detail: production callers project through
``retrieve()``, never ``_conn``.
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from pathlib import Path

from . import memdb
from .lineage import (
    KINDS,
    RETRACTED,
    _VALID_KINDS,
    export_shape,
    history_chain,
    iso_time,
    retraction_note,
    validate_kind,
)
from .memory import Fact, MemoryStore
from .retrieval import Injection, inject


class SQLStore:
    """The canonical store: the pipeline's interface, memdb's substrate."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        # Lazy connect: an absent store is an empty store until first write.
        self._conn = memdb.connect(str(self.path)) if self.path.exists() else None
        # Live Fact registry: like the JSON store, Fact objects are mutated in
        # place when superseded/retracted, so a caller's held reference flips
        # active -> inactive the moment a later write closes it.
        #
        # CONTRACT (mutable views): a Fact returned by any query is a live
        # view refreshed in place. Three sharp edges callers must not lean on:
        #   1. dry-run writes (persist=False) still refresh held refs even
        #      though the committed DB is unchanged until a later re-read;
        #   2. the registry is never evicted (bounded only by ``clear()``) —
        #      fine for the short-lived, per-session stores the daemon uses;
        #   3. a held ref does NOT refresh when *another* process supersedes
        #      its row (no cross-connection invalidation) until the id passes
        #      through ``_fact`` again.
        # Nothing in production relies on held-reference mutation; if a caller
        # ever does, the deeper fix is to return fresh snapshots and delete the
        # registry (a behavior change, deferred — see EVOLUTION_LOOP Stone 24).
        self._live: dict[int, Fact] = {}

    def close(self) -> None:
        """Close the underlying connection (idempotent)."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _ensure(self):
        """Create the store file on first write (read paths never create)."""
        if self._conn is None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = memdb.connect(str(self.path))
        return self._conn

    # -- row -> Fact shaping ------------------------------------------------
    def _row(self, fact_id: str):
        if self._conn is None:
            return None
        try:
            i = int(fact_id)
        except (TypeError, ValueError):
            return None
        return self._conn.execute("SELECT * FROM facts WHERE id=?", (i,)).fetchone()

    def _supersedes(self, row_id: int) -> list[int]:
        row = self._conn.execute(
            "SELECT supersedes FROM facts WHERE id=?", (row_id,)).fetchone()
        return [row["supersedes"]] if row and row["supersedes"] is not None else []

    def _fact(self, row) -> Fact:
        """The registered Fact for this row, refreshed in place (JSON parity)."""
        successor = self._conn.execute(
            "SELECT id FROM facts WHERE supersedes=?", (row["id"],)).fetchone()
        if successor is not None:
            superseded_by = str(successor["id"])
        elif row["valid_to"] is not None:
            superseded_by = RETRACTED
        else:
            superseded_by = ""
        f = self._live.get(row["id"])
        if f is None:
            f = Fact(id=str(row["id"]), content="", kind="memory", source="",
                     created_at=iso_time(row["created_at"]))
            self._live[row["id"]] = f
        f.content = row["content"] if row["content"] is not None else row["object"]
        f.kind = row["kind"] or "memory"
        f.source = row["source"] or ""
        f.created_at = iso_time(row["created_at"])
        f.supersedes = [str(s) for s in self._supersedes(row["id"])]
        f.superseded_by = superseded_by
        f.note = row["note"] or ""
        return f

    # -- mutations -----------------------------------------------------------
    def add(self, content, kind, source, supersedes=None, note="", persist=True) -> Fact:
        validate_kind(kind)
        conn = self._ensure()
        now = time.time()
        targets = []
        for sid in supersedes or []:
            row = self._row(sid)
            if row is not None and row["valid_to"] is None:
                targets.append(int(sid))
        if len(targets) > 1:
            # The schema's single supersedes FK cannot link a fact to several
            # predecessors; the JSON store can, so silently collapsing would
            # mislabel the extras as retracted. No caller produces this
            # (record/bridge enforce exactly-one) — fail loudly instead.
            raise ValueError(
                f"supersedes may list at most one active fact id, "
                f"got {[str(t) for t in targets]}")
        row_id = memdb.add_fact(
            conn, "3v0", "note", content,
            kind=kind, source=source, content=content, note=note,
            supersedes=targets[0] if targets else None,
            now=now, persist=False,
        )
        for old in targets[1:]:  # extra links close validity without the FK
            conn.execute(
                "UPDATE facts SET valid_to=? WHERE id=? AND valid_to IS NULL",
                (now, old))
        if persist:
            conn.commit()
        # Refresh every superseded target's registered Fact so the caller's
        # held reference flips inactive (JSON-store in-place semantics).
        for old in targets:
            self._fact(self._row(str(old)))
        return self._fact(self._row(row_id))

    def retract(self, fact_id: str, source: str = "", persist: bool = True) -> Fact | None:
        row = self._row(fact_id)
        if row is None or row["valid_to"] is not None:
            return None
        now = time.time()
        note = retraction_note(row["note"] or "", source)
        self._conn.execute(
            "UPDATE facts SET valid_to=?, note=? WHERE id=?",
            (now, note, row["id"]))
        if persist:
            self._conn.commit()
        return self._fact(self._row(fact_id))

    # -- queries -------------------------------------------------------------
    def active(self, kind: str | None = None) -> list[Fact]:
        if self._conn is None:
            return []
        rows = memdb.valid_facts(self._conn, kind=kind, now=time.time())
        return [self._fact(r) for r in rows]

    def inactive(self, kind: str | None = None) -> list[Fact]:
        """Superseded/retracted facts (closed validity), still recoverable."""
        if self._conn is None:
            return []
        sql = "SELECT * FROM facts WHERE valid_to IS NOT NULL"
        params = []
        if kind is not None:
            sql += " AND kind = ?"
            params.append(kind)
        sql += " ORDER BY created_at, id"
        return [self._fact(r) for r in self._conn.execute(sql, params)]

    @property
    def facts(self) -> list[Fact]:
        if self._conn is None:
            return []
        rows = self._conn.execute(
            "SELECT * FROM facts ORDER BY created_at, id").fetchall()
        return [self._fact(r) for r in rows]

    def clear(self) -> None:
        conn = self._ensure()
        conn.execute("DELETE FROM facts")
        conn.commit()
        self._live.clear()

    def matching(self, kind: str | None, substring: str) -> list[Fact]:
        """Active facts whose content contains ``substring``.

        Case-sensitive literal containment, like the JSON store's — NOT SQL
        LIKE (which is case-insensitive and treats %/_ as wildcards). This is
        the single substring-resolution algorithm behind record/bridge, so a
        parity drift here silently changes supersede/retract targeting.
        """
        if self._conn is None:
            return []
        rows = memdb.valid_facts(self._conn, kind=kind, now=time.time())
        return [self._fact(r) for r in rows if substring in
                (r["content"] if r["content"] is not None else r["object"])]

    def get(self, fact_id: str) -> Fact | None:
        row = self._row(fact_id)
        return self._fact(row) if row is not None else None

    def history(self, fact_id: str) -> list[Fact]:
        """The full supersession chain, oldest -> newest (see lineage)."""
        return history_chain(self.get, fact_id)

    def retrieve(self, *, kind=None, query_terms=None, budget_chars=2000,
                 touch=True, now=None, sep="\n") -> Injection:
        """The retrieval seam, owned by the store (hides the sqlite connection).

        Projects the retrieval-chosen working set under a budget; the store
        fronting an as-yet-absent file projects the empty view. ``touch`` and
        ``sep`` mirror ``core.retrieval.inject``.
        """
        if self._conn is None:
            return Injection(facts=[], ids=[], text="", truncated=False,
                             budget_chars=budget_chars, budget_used=0)
        return inject(self._conn, kind=kind, query_terms=query_terms,
                      budget_chars=budget_chars, touch=touch, now=now, sep=sep)

    # -- export --------------------------------------------------------------
    def export(self) -> dict[str, list[str]]:
        return export_shape(_VALID_KINDS, self.active)

    # -- lock / dry-run parity ------------------------------------------------
    @contextmanager
    def mutate(self):
        """Yield the store (SQLite serializes itself; parity with the JSON store)."""
        yield self


def open_store(path: str | Path) -> MemoryStore | SQLStore:
    """The store for ``path``: SQLite (.db) -> SQLStore, JSON -> MemoryStore.

    The rewire makes the .db canonical for the primary project; sibling
    projects keep their JSON stores until their own rewire.
    """
    p = Path(path)
    if p.suffix == ".db":
        return SQLStore(p)
    return MemoryStore(p)
