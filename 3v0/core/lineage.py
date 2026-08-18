"""Shared pure lineage semantics — the decision layer of the memory store.

The rewire's two collection backends (JSON ``MemoryStore``, SQLite ``SQLStore``)
must never drift on the *meaning* of facts: which kinds exist, how retractions
are tagged, how a supersession chain is walked. This module owns those pure
algorithms once, parameterized so each backend supplies only its lookup.

Contract: nothing here touches a file, a lock, or a sqlite connection — pure
functions over ``Fact``-shaped objects (or their ids), importable and testable
in isolation (invariant #4: decision logic testable without a DB).
"""

from __future__ import annotations

import time

KINDS = ("memory", "user", "identity", "directive")  # canonical fact kinds
_VALID_KINDS = set(KINDS)  # set for O(1) membership + sorted() in the error message

# ``superseded_by`` sentinel for a fact that was REMOVED (no successor exists).
# Distinct from a real fact id, so ``history_chain`` terminates at the retracted
# fact and ``active()``/``export()`` exclude it.
RETRACTED = "retracted"


def validate_kind(kind: str) -> str:
    """Return ``kind`` if it is a canonical fact kind, else raise ValueError."""
    if kind not in _VALID_KINDS:
        raise ValueError(f"kind must be one of {sorted(_VALID_KINDS)}, got {kind!r}")
    return kind


def iso_time(t: float) -> str:
    """UTC ISO-8601 timestamp for epoch seconds ``t``."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def retraction_note(note: str, source: str) -> str:
    """The note with the retraction provenance tag appended (or ``note`` alone).

    ``source`` empty means no tag: retraction from an unknown source leaves the
    note untouched, so a caller can distinguish "retracted by X" from a bare
    removal.
    """
    if not source:
        return note
    tag = f"retracted by {source}"
    return f"{note} {tag}".strip() if note else tag


def content_matches(content: str, substring: str) -> bool:
    """Case-sensitive literal containment — the single matching semantics.

    Both stores match by ``substring in content``, NOT SQL LIKE (which is
    case-insensitive and treats ``%``/``_`` as wildcards). One owner, so a
    drift here cannot silently change supersede/retract targeting.
    """
    return substring in content


def history_chain(get_by_id, start_id):
    """Reconstruct a fact's full supersession chain, oldest -> newest.

    ``get_by_id`` maps a fact id (str) to a ``Fact``-shaped object or ``None``
    (a dict lookup for JSON, a row fetch for SQLite). Walks ``superseded_by``
    forward to the newest link, then ``supersedes`` backward to the oldest, so
    an audit of any fact recovers the whole thread of what it replaced and what
    replaced it. Cycle-guarded, and tolerant of dangling links (a missing id
    terminates the walk exactly like the ``RETRACTED`` sentinel does).
    """
    cur = get_by_id(start_id)
    if cur is None:
        return []
    # Forward to the newest link.
    seen: set = set()
    while cur.superseded_by and cur.superseded_by != RETRACTED and cur.id not in seen:
        seen.add(cur.id)
        nxt = get_by_id(cur.superseded_by)
        if nxt is None:
            break
        cur = nxt
    # Backward through the predecessors to the oldest.
    out = []
    seen = set()
    while cur is not None and cur.id not in seen:
        seen.add(cur.id)
        out.append(cur)
        prev = None
        for fid in cur.supersedes or []:
            prev = get_by_id(fid)
            if prev is not None:
                break
        cur = prev
    out.reverse()
    return out


def export_shape(kinds, active):
    """Active facts grouped by kind, as ``{kind: [content, ...]}`` (derived view).

    ``active`` is a callable ``kind -> list[Fact]`` (the store's own scoped
    active query). The grouping is a pure lineage view: kinds in stable order,
    empty kinds omitted.
    """
    out = {}
    for kind in sorted(kinds):
        lines = [f.content for f in active(kind)]
        if lines:
            out[kind] = lines
    return out
