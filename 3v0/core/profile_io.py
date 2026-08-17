"""Wire format for the Hermes profile's MEMORY.md / USER.md.

Entries are separated by '§'. This module is the single owner of that format
so seed/export/sync never disagree on how the profile is parsed or written.

The '§' separator is Hermes-owned — it is how the host's own memory tool reads
and writes the profile, so 3V0 cannot swap it unilaterally. The store
(data/memory.db) can hold anything; the profile is a *projection* of the
store, and a fact containing a literal '§' (or leading/trailing whitespace)
cannot round-trip through it. The guard lives here, at the
boundary: join_entries refuses to emit an un-parseable wire, and the record
path refuses such content before it enters the store.
"""

from __future__ import annotations

SEPARATOR = "§"

# The wire join between entries: a separator flanked by newlines. Single source
# of truth for how entries are joined on the profile wire — shared by
# join_entries() below and retrieval's inject(sep=...) budget accounting, so a
# re-typed literal cannot drift from the emitted wire.
ENTRY_JOIN = f"\n{SEPARATOR}\n"


def contains_separator(content: str) -> bool:
    """True if content contains the profile entry separator (cannot round-trip)."""
    return SEPARATOR in content


def split_entries(md: str) -> list[str]:
    """Split a memories .md body on '§' into non-empty, trimmed entries."""
    return [p.strip() for p in md.split(SEPARATOR) if p.strip()]


def join_entries(entries: list[str]) -> str:
    """Join entries into a memories .md body (inverse of split_entries).

    Refuses any entry containing the separator: emitting it would produce a
    wire the next split_entries (and Hermes's own memory tool) mis-parses.
    """
    for entry in entries:
        if contains_separator(entry):
            raise ValueError(
                f"entry contains the '{SEPARATOR}' separator and cannot be "
                f"projected to the profile: {entry[:40]!r}"
            )
    return ENTRY_JOIN.join(entries)
