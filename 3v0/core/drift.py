"""Drift computation — the pure decision half (is this project drifting?).

``compute_drift`` is a pure function over collected inputs, unit-testable
without a real git repo. The *collection* half (``collect_git_state`` /
``store_hash`` and the ``git`` subprocess calls) lives in ``core/gitstate.py``
— this module only decides, matching ``core/continuity.py`` and
``core/handoff.py``.

A project **drifts** (needs a decision) when, for a project that tracks its
upstream, it is behind upstream; when the upstream ref can't be resolved; when
the working tree has uncommitted changes; or when a configured store is
missing. Everything else — ahead of upstream, HEAD moved, store changed since
the last snapshot — is *informational* (reported, not flagged as drift).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .projects import LedgerEntry


@dataclass(frozen=True)
class GitState:
    """Live git facts for one repo (all Optional — None means unknown)."""

    head: Optional[str] = None
    upstream_head: Optional[str] = None
    behind: Optional[int] = None       # commits behind upstream (None unknown)
    ahead: Optional[int] = None        # commits ahead of upstream
    dirty: Optional[bool] = None       # uncommitted work in the working tree
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None


def compute_drift(
    entry: LedgerEntry, git: GitState, current_store_head: Optional[str]
) -> Dict:
    """The pure drift verdict: collected git facts + stored position → a
    JSON-safe report dict (the shape ``drift_check.py`` prints)."""
    reasons: List[str] = []
    if git.error:
        reasons.append(f"git: {git.error}")
    if git.dirty:
        reasons.append("uncommitted changes")
    if entry.track_upstream:
        if git.upstream_head is None:
            reasons.append(
                f"upstream ref {entry.upstream}/{entry.upstream_ref} not found (fetch?)"
            )
        elif git.behind is not None and git.behind > 0:
            reasons.append(f"{git.behind} commit(s) behind upstream")
    if entry.store is not None and current_store_head is None:
        reasons.append("store missing/unreadable")

    # Informational deltas vs the recorded snapshot.
    head_moved = bool(entry.head and git.head and entry.head != git.head)
    store_changed: Optional[bool] = None
    if entry.store is not None and entry.store_head and current_store_head:
        store_changed = current_store_head != entry.store_head

    return {
        "name": entry.name,
        "title": entry.title,
        "repo": str(entry.repo),
        "upstream": entry.upstream,
        "upstream_ref": entry.upstream_ref,
        "track_upstream": entry.track_upstream,
        "delta": entry.delta,
        "profile": entry.profile,
        "primary": entry.primary,
        "head": git.head,
        "upstream_head": git.upstream_head,
        "behind": git.behind,
        "ahead": git.ahead,
        "dirty": git.dirty,
        "store_present": (
            None if entry.store is None else (current_store_head is not None)
        ),
        "store_changed": store_changed,
        "head_moved": head_moved,
        "open_loops": list(entry.open_loops),
        "error": git.error,
        "drifting": bool(reasons),
        "reasons": reasons,
    }
