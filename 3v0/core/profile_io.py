"""Wire format for the Hermes profile's MEMORY.md / USER.md.

Entries are separated by '§'. This module is the single owner of that format
so seed/export/sync never disagree on how the profile is parsed or written.

Known boundary: an entry containing a literal '§' or leading/trailing
whitespace does not survive a round-trip. The current store contains neither;
swap to a structured separator before the store grows enough for it to matter.
"""

from __future__ import annotations

SEPARATOR = "§"


def split_entries(md: str) -> list[str]:
    """Split a memories .md body on '§' into non-empty, trimmed entries."""
    return [p.strip() for p in md.split(SEPARATOR) if p.strip()]


def join_entries(entries: list[str]) -> str:
    """Join entries into a memories .md body (inverse of split_entries)."""
    return f"\n{SEPARATOR}\n".join(entries)
