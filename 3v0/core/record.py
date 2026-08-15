"""Record a fact into the store — including provenance-tracked correction.

This is the write path that makes the store the live origin of 3V0's memory.
Unlike the Hermes `memory` tool (which silently rewrites the profile), a
correction here SUPERSEDES the old fact: the old fact is marked inactive and
linked to its successor, so the full thread stays recoverable via
MemoryStore.history(). After recording, the caller re-exports the derived view
to the profile so the two stay in sync.

Supersession target is precise by design:
- supersede_id: supersede the fact with this exact id.
- supersede_contains: supersede the active fact whose content contains this
  substring, requiring EXACTLY one match (ambiguity or absence refuses).

Never destroys: superseded facts remain in the store, recoverable by history.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .memory import Fact, MemoryStore


class RecordError(Exception):
    """A correction couldn't be applied — target missing or ambiguous."""


@dataclass
class RecordResult:
    fact: Fact
    superseded_ids: list[str] = field(default_factory=list)
    chain: list[Fact] = field(default_factory=list)


def record(
    store: MemoryStore,
    content: str,
    kind: str,
    source: str,
    supersede_id: str | None = None,
    supersede_contains: str | None = None,
    persist: bool = True,
) -> RecordResult:
    """Add a fact, optionally superseding an existing one.

    With persist=False the in-memory store is updated but nothing is written
    to disk (dry-run). The caller must still re-export the profile separately
    to keep it a derived view of the store.
    """
    if supersede_id is not None and supersede_contains is not None:
        raise RecordError("give at most one of supersede_id / supersede_contains")

    targets: list[Fact] = []
    if supersede_id is not None:
        target = store.get(supersede_id)
        if target is None:
            raise RecordError(f"no fact with id {supersede_id!r}")
        if not target.active:
            raise RecordError(f"fact {supersede_id!r} is already superseded")
        targets = [target]
    elif supersede_contains is not None:
        matches = [f for f in store.active(kind=kind) if supersede_contains in f.content]
        if len(matches) != 1:
            raise RecordError(
                f"need exactly one active {kind} fact containing "
                f"{supersede_contains!r}, found {len(matches)}"
            )
        targets = matches

    fact = store.add(
        content, kind, source, supersedes=[t.id for t in targets], persist=persist
    )
    return RecordResult(
        fact=fact,
        superseded_ids=[t.id for t in targets],
        chain=store.history(fact.id),
    )
