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

The store -> profile direction is the retrieval-chosen working set (ADR-0004):
``exported`` is the view entries absent from the profile, not every active
fact. The diff itself is pure — ``diff_kind`` — so the classification is
testable without any store.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .memory import MemoryStore
from .profile_io import ENTRY_JOIN, join_entries, split_entries
from .store import SQLStore


@dataclass
class SyncReport:
    kind: str
    imported: list[str] = field(default_factory=list)  # profile -> store (new facts)
    dropped: list[str] = field(default_factory=list)   # profile entries removed (superseded)
    exported: list[str] = field(default_factory=list)  # store -> profile (new to profile)

    @property
    def clean(self) -> bool:
        return not (self.imported or self.dropped or self.exported)


def diff_kind(profile_entries, active_contents, inactive_contents, view_contents):
    """Pure: classify the profile/store diff for one kind.

    Returns ``(imported, dropped, exported)``:
    - ``imported`` — profile entries with no store fact (new to the store)
    - ``dropped``  — profile entries matching a superseded (inactive) fact
    - ``exported`` — view entries absent from the profile (new to the profile)
    """
    active = set(active_contents)
    inactive = set(inactive_contents)
    profile_set = set(profile_entries)
    imported = [e for e in profile_entries if e not in active and e not in inactive]
    dropped = [e for e in profile_entries if e in inactive]
    exported = [c for c in view_contents if c not in profile_set]
    return imported, dropped, exported


def sync_kind(store: MemoryStore | SQLStore, profile_md: str, kind: str,
              write: bool) -> SyncReport:
    """Diff store vs profile for one kind; with write=True, converge them."""
    profile_entries = split_entries(profile_md)
    active = {f.content for f in store.active(kind=kind)}
    inactive = {f.content for f in store.inactive(kind=kind)}
    view = split_entries(profile_text(store, kind))
    imported, dropped, exported = diff_kind(profile_entries, active, inactive, view)
    if write:
        for entry in imported:
            store.add(entry, kind, "profile-import")
    return SyncReport(kind=kind, imported=imported, dropped=dropped, exported=exported)


def profile_text(store: MemoryStore | SQLStore, kind: str) -> str:
    """The derived view of the store for one kind, as profile .md text.

    A SQLStore projects the retrieval-chosen working set under the budget —
    touch=False, because a wake export is mechanical sync, not evidence the
    facts were used. The legacy JSON store keeps export-all (sibling projects,
    pre-rewire).
    """
    if isinstance(store, SQLStore):
        return store.retrieve(kind=kind, touch=False, sep=ENTRY_JOIN).text
    return join_entries([f.content for f in store.active(kind=kind)])
