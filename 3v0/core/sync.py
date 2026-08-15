"""Reconcile the native store with the Hermes profile (store is canonical).

The store is the origin; the profile is a derived view. `sync_kind` converges
the two without ever destroying store history:

- A profile entry with no matching store fact is imported into the store as a
  new fact (source="profile-import").
- A profile entry that matches a SUPERSEDED (inactive) store fact is dropped
  from the profile, because the store has already corrected it.
- An active store fact missing from the profile is exported to the profile.

After a write-sync, the profile equals the store's active facts exactly, and
the store's full supersession history is intact. Sync never deletes from the
store; the only removals are from the profile (the derived view).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .memory import MemoryStore
from .profile_io import join_entries, split_entries


@dataclass
class SyncReport:
    kind: str
    imported: list[str] = field(default_factory=list)  # profile -> store (new facts)
    dropped: list[str] = field(default_factory=list)   # profile entries removed (superseded)
    exported: list[str] = field(default_factory=list)  # store -> profile (new to profile)

    @property
    def clean(self) -> bool:
        return not (self.imported or self.dropped or self.exported)


def sync_kind(store: MemoryStore, profile_md: str, kind: str, write: bool) -> SyncReport:
    """Diff store vs profile for one kind; with write=True, converge them."""
    profile_entries = split_entries(profile_md)
    active = {f.content for f in store.active(kind=kind)}
    inactive = {f.content for f in store.facts if f.kind == kind and not f.active}

    imported = [e for e in profile_entries if e not in active and e not in inactive]
    dropped = [e for e in profile_entries if e in inactive]
    exported = [
        f.content for f in store.active(kind=kind) if f.content not in set(profile_entries)
    ]

    if write:
        for entry in imported:
            store.add(entry, kind, "profile-import")
    return SyncReport(kind=kind, imported=imported, dropped=dropped, exported=exported)


def profile_text(store: MemoryStore, kind: str) -> str:
    """The derived view of the store for one kind, as profile .md text."""
    return join_entries([f.content for f in store.active(kind=kind)])
