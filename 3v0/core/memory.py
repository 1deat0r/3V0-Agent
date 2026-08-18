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
  body repo, not hidden in a host profile. (Stone 23: the primary project's
  canonical store is now `data/memory.db` via `core.store.SQLStore`; this
  JSON store remains the substrate for sibling projects until their rewire.)

Deliberately small. This is the seed of 3V0's own memory — not a
reimplementation of Hermes's MEMORY.md mechanism, but the first piece of the
substrate that will eventually host identity, memory, and evolution.

Lineage semantics (kind validity, retraction tagging, the supersession walk,
the export grouping) live in ``core.lineage`` — the single owner shared with
``SQLStore`` so the two backends cannot drift on meaning.
"""

from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from pathlib import Path

from .lineage import (
    KINDS,
    RETRACTED,
    _VALID_KINDS,
    content_matches,
    export_shape,
    history_chain,
    iso_time,
    retraction_note,
    validate_kind,
)

# fcntl is Unix-only; on Windows there is no equivalent advisory lock exposed
# by the stdlib, so locking degrades to a no-op there (the store is single-host
# by design — see EVOLUTION_LOOP.md).
try:
    import fcntl
except ImportError:  # pragma: no cover - Windows
    fcntl = None

PROFILE_KINDS = ("memory", "user")  # the kinds that project to the Hermes profile


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
        validate_kind(kind)
        fact = Fact(
            id=uuid.uuid4().hex[:12],
            content=content,
            kind=kind,
            source=source,
            created_at=iso_time(time.time()),
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
        f.note = retraction_note(f.note, source)
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

    def inactive(self, kind: str | None = None) -> list[Fact]:
        """Superseded/retracted facts (still recoverable, excluded from views)."""
        out = [f for f in self.facts if not f.active]
        if kind is not None:
            out = [f for f in out if f.kind == kind]
        return out

    def matching(self, kind: str | None, substring: str) -> list[Fact]:
        """Active facts whose content contains ``substring``.

        The single substring-resolution algorithm. Callers branch their own
        0/1/many policy: ``record`` refuses ambiguity; the bridge skips or
        plain-adds. One place to change match semantics.
        """
        return [f for f in self.active(kind=kind) if content_matches(f.content, substring)]

    def get(self, fact_id: str) -> Fact | None:
        for f in self.facts:
            if f.id == fact_id:
                return f
        return None

    def history(self, fact_id: str) -> list[Fact]:
        """Reconstruct a fact's full chain, oldest -> newest (see lineage)."""
        by_id = {f.id: f for f in self.facts}
        return history_chain(by_id.get, fact_id)

    # -- export ------------------------------------------------------------
    def export(self) -> dict[str, list[str]]:
        """Active facts grouped by kind, as plain text lines (derived view)."""
        return export_shape(_VALID_KINDS, self.active)
