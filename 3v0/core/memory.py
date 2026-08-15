"""3V0 core memory — a provenance-aware, versioned identity/memory store.

This is the first native subsystem of 3V0, distinct from the Hermes fork that
is its v0.00 chassis. It applies one lesson from the "context engineering"
cluster (semantica, OpenViking): facts carry provenance, and conflicts are
FLAGGED and linked, never silently overwritten.

Design:
- Every fact has an id, kind, source, and creation timestamp.
- A new fact that contradicts an old one SUPERSEDES it: the old fact is marked
  inactive (still queryable via history()) and linked to its successor.
  Nothing is ever destroyed — the audit trail is the point.
- Plain JSON on disk (stdlib only) so the source of truth is auditable in the
  body repo, not hidden in a host profile.

Deliberately small. This is the seed of 3V0's own memory — not a
reimplementation of Hermes's MEMORY.md mechanism, but the first piece of the
substrate that will eventually host identity, memory, and evolution.
"""

from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from pathlib import Path

# fcntl is Unix-only; on Windows there is no equivalent advisory lock exposed
# by the stdlib, so locking degrades to a no-op there (the store is single-host
# by design — see EVOLUTION_LOOP.md).
try:
    import fcntl
except ImportError:  # pragma: no cover - Windows
    fcntl = None

_VALID_KINDS = {"memory", "user", "identity", "directive"}

# ``superseded_by`` sentinel for a fact that was REMOVED (no successor exists).
# Distinct from a real fact id, so ``history()`` terminates the chain at the
# retracted fact, and ``active()``/``export()`` exclude it.
RETRACTED = "retracted"


@contextmanager
def locked(path: str | Path):
    """Serialize cross-process read-modify-write on the store at ``path``.

    An advisory ``flock`` on a ``<store>.lock`` sidecar so the background
    review fork's ``ingest.py`` subprocess and a foreground ``record.py`` /
    ``sync.py`` cannot interleave load→mutate→save on the same JSON file.
    Degrades to a no-op where ``fcntl`` is unavailable.
    """
    lock_path = Path(path).with_suffix(Path(path).suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    if fcntl is None:
        yield
        return
    fd = open(lock_path, "a+", encoding="utf-8")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        except OSError:
            pass
        fd.close()


@dataclass
class Fact:
    id: str
    content: str
    kind: str                  # memory | user | identity | directive
    source: str                # e.g. "foreground", "background-review", "operator"
    created_at: str
    supersedes: list[str] = field(default_factory=list)
    superseded_by: str = ""    # non-empty => inactive
    note: str = ""

    @property
    def active(self) -> bool:
        return not self.superseded_by


class MemoryStore:
    """Append-only memory with supersession (no silent overwrite)."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.facts: list[Fact] = []
        if self.path.exists():
            self._load()

    # -- persistence -------------------------------------------------------
    def _load(self) -> None:
        if not self.path.exists():
            self.facts = []
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.facts = [Fact(**f) for f in raw.get("facts", [])]

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": 1, "facts": [asdict(f) for f in self.facts]}
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    # -- mutations ---------------------------------------------------------
    def add(
        self,
        content: str,
        kind: str,
        source: str,
        supersedes: list[str] | None = None,
        note: str = "",
        persist: bool = True,
    ) -> Fact:
        if kind not in _VALID_KINDS:
            raise ValueError(f"kind must be one of {sorted(_VALID_KINDS)}, got {kind!r}")
        fact = Fact(
            id=uuid.uuid4().hex[:12],
            content=content,
            kind=kind,
            source=source,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            supersedes=list(supersedes or []),
            note=note,
        )
        self.facts.append(fact)
        # Link superseded facts to their successor (conflict flagged, not erased).
        for target_id in fact.supersedes:
            for old in self.facts:
                if old.id == target_id and old.active:
                    old.superseded_by = fact.id
        if persist:
            self._save()
        return fact

    def retract(self, fact_id: str, source: str = "", persist: bool = True) -> Fact | None:
        """Mark an active fact as removed (no successor exists).

        A removal has no successor, so we cannot link it to one; instead
        ``superseded_by`` is set to the ``RETRACTED`` sentinel, which excludes
        the fact from ``active()``/``export()`` and makes ``history()`` stop
        at it as a terminal. Nothing is destroyed — the retracted fact remains
        in the store and is recoverable by id/history.
        """
        f = self.get(fact_id)
        if f is None or not f.active:
            return None
        f.superseded_by = RETRACTED
        if source:
            tag = f"retracted by {source}"
            f.note = f"{f.note} {tag}".strip() if f.note else tag
        if persist:
            self._save()
        return f

    def reload(self) -> None:
        """Re-read the store from disk, replacing in-memory facts.

        Used inside ``mutate()`` so a writer operating under the cross-process
        lock always applies its mutation to the latest facts (picking up any
        concurrent writer that committed between construction and lock
        acquisition).
        """
        self._load()

    @contextmanager
    def mutate(self):
        """Acquire the cross-process lock, reload latest facts, then yield.

        The canonical pattern for a store writer::

            store = MemoryStore(path)
            with store.mutate():
                ...  # add/retract/record(...) — each mutation persists

        Ensures concurrent writers (background fork's ingest.py vs foreground
        record.py/sync.py) cannot interleave load→mutate→save on the JSON file.
        """
        with locked(self.path):
            self.reload()
            yield self

    # -- queries -----------------------------------------------------------
    def active(self, kind: str | None = None) -> list[Fact]:
        out = [f for f in self.facts if f.active]
        if kind is not None:
            out = [f for f in out if f.kind == kind]
        return out

    def get(self, fact_id: str) -> Fact | None:
        for f in self.facts:
            if f.id == fact_id:
                return f
        return None

    def history(self, fact_id: str) -> list[Fact]:
        """Reconstruct a fact's full chain, oldest -> newest.

        Walks superseded_by forward to the newest link, then supersedes
        backward to the oldest, so an audit of any fact recovers the whole
        thread of what it replaced and what replaced it.
        """
        by_id = {f.id: f for f in self.facts}
        cur = by_id.get(fact_id)
        if cur is None:
            return []
        while cur.superseded_by and cur.superseded_by in by_id:
            cur = by_id[cur.superseded_by]
        chain: list[Fact] = []
        seen: set[str] = set()
        while cur is not None and cur.id not in seen:
            chain.append(cur)
            seen.add(cur.id)
            prev = None
            for fid in cur.supersedes:
                if fid in by_id:
                    prev = by_id[fid]
                    break
            cur = prev
        chain.reverse()
        return chain

    # -- export ------------------------------------------------------------
    def export(self) -> dict[str, list[str]]:
        """Active facts grouped by kind, as plain text lines (derived view)."""
        out: dict[str, list[str]] = {}
        for kind in sorted(_VALID_KINDS):
            lines = [f.content for f in self.active(kind=kind)]
            if lines:
                out[kind] = lines
        return out
