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
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from pathlib import Path

from . import memdb
from .memory import KINDS, RETRACTED, Fact, MemoryStore

_VALID_KINDS = set(KINDS)


def _iso(t: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


class SQLStore:
    """The canonical store: the pipeline's interface, memdb's substrate."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        # Lazy connect: an absent store is an empty store until first write.
        self._conn = memdb.connect(str(self.path)) if self.path.exists() else None
        # Live Fact registry: like the JSON store, Fact objects are mutated in
        # place when superseded/retracted, so a caller's held reference flips
        # active -> inactive the moment a later write closes it.
        self._live: dict[int, Fact] = {}

    @property
    def conn(self):
        return self._conn

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
                     created_at=_iso(row["created_at"]))
            self._live[row["id"]] = f
        f.content = row["content"] if row["content"] is not None else row["object"]
        f.kind = row["kind"] or "memory"
        f.source = row["source"] or ""
        f.created_at = _iso(row["created_at"])
        f.supersedes = [str(s) for s in self._supersedes(row["id"])]
        f.superseded_by = superseded_by
        f.note = row["note"] or ""
        return f

    # -- mutations -----------------------------------------------------------
    def add(self, content, kind, source, supersedes=None, note="", persist=True) -> Fact:
        if kind not in _VALID_KINDS:
            raise ValueError(f"kind must be one of {sorted(_VALID_KINDS)}, got {kind!r}")
        conn = self._ensure()
        now = time.time()
        targets = []
        for sid in supersedes or []:
            row = self._row(sid)
            if row is not None and row["valid_to"] is None:
                targets.append(int(sid))
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
        note = row["note"] or ""
        if source:
            tag = f"retracted by {source}"
            note = f"{note} {tag}".strip() if note else tag
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
        if self._conn is None:
            return []
        rows = self._conn.execute(
            """SELECT * FROM facts
               WHERE (valid_to IS NULL OR valid_to > ?) AND valid_from <= ?
                 AND COALESCE(content, object) LIKE ?""",
            (time.time(), time.time(), f"%{substring}%"),
        ).fetchall()
        out = [self._fact(r) for r in rows]
        if kind is not None:
            out = [f for f in out if f.kind == kind]
        return out

    def get(self, fact_id: str) -> Fact | None:
        row = self._row(fact_id)
        return self._fact(row) if row is not None else None

    def history(self, fact_id: str) -> list[Fact]:
        """The full supersession chain, oldest -> newest (like the JSON store).

        Walks ``superseded_by`` forward to the newest link, then ``supersedes``
        backward to the oldest, so an audit of any fact recovers the whole
        thread of what it replaced and what replaced it.
        """
        cur = self.get(fact_id)
        if cur is None:
            return []
        seen: set[str] = set()
        while cur.superseded_by and cur.superseded_by != RETRACTED \
                and cur.id not in seen:
            seen.add(cur.id)
            nxt = self.get(cur.superseded_by)
            if nxt is None:
                break
            cur = nxt
        out: list[Fact] = []
        seen = set()
        while cur is not None and cur.id not in seen:
            seen.add(cur.id)
            out.append(cur)
            pred = self.get(cur.supersedes[0]) if cur.supersedes else None
            cur = pred
        out.reverse()
        return out

    # -- export --------------------------------------------------------------
    def export(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for kind in sorted(_VALID_KINDS):
            lines = [f.content for f in self.active(kind=kind)]
            if lines:
                out[kind] = lines
        return out

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
