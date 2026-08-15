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
from dataclasses import dataclass, field, asdict
from pathlib import Path

_VALID_KINDS = {"memory", "user", "identity", "directive"}


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
