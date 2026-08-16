"""Drift computation — the pure logic + git collection behind ``drift_check.py``
and ``project.py status``.

Split so the *decision* (is this project drifting?) is a pure function over
collected inputs, unit-testable without a real git repo, while the *collection*
shells out to ``git`` best-effort: a missing repo / git / upstream degrades to
an error flag, never a crash.

A project **drifts** (needs a decision) when, for a project that tracks its
upstream, it is behind upstream; when the upstream ref can't be resolved; when
the working tree has uncommitted changes; or when a configured store is
missing. Everything else — ahead of upstream, HEAD moved, store changed since
the last snapshot — is *informational* (reported, not flagged as drift).
"""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core.projects import LedgerEntry


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


def _run(cmd: List[str], cwd: Path, timeout: int = 30) -> Tuple[int, str, str]:
    """Run a command; return (rc, stdout, stderr). Never raises."""
    try:
        proc = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode, (proc.stdout or "").strip(), (proc.stderr or "").strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, "", str(e)


def _rev_parse(cwd: Path, ref: str) -> Optional[str]:
    rc, out, _ = _run(["git", "rev-parse", ref], cwd)
    return out if rc == 0 and out else None


def collect_git_state(entry: LedgerEntry) -> GitState:
    """Collect live git facts for a ledger entry. Best-effort; errors surface
    as ``GitState.error``, not exceptions."""
    repo = entry.repo
    if not repo.exists():
        return GitState(error=f"repo missing: {repo}")
    if not (repo / ".git").exists():
        return GitState(error=f"not a git repo: {repo}")

    head = _rev_parse(repo, "HEAD")
    if head is None:
        return GitState(error="git rev-parse HEAD failed")

    upstream_head = _rev_parse(
        repo, f"refs/remotes/{entry.upstream}/{entry.upstream_ref}"
    )
    if upstream_head is None:
        # Fall back to the remote's symbolic HEAD (e.g. origin/HEAD -> main).
        upstream_head = _rev_parse(repo, f"refs/remotes/{entry.upstream}/HEAD")

    behind = ahead = None
    if upstream_head:
        rc, out, _ = _run(
            ["git", "rev-list", "--left-right", "--count", f"{upstream_head}...HEAD"],
            repo,
        )
        if rc == 0:
            parts = out.split()
            if len(parts) == 2 and all(p.isdigit() for p in parts):
                behind, ahead = int(parts[0]), int(parts[1])

    rc, out, _ = _run(["git", "status", "--porcelain"], repo)
    dirty = rc == 0 and bool(out)
    return GitState(
        head=head, upstream_head=upstream_head, behind=behind, ahead=ahead, dirty=dirty
    )


def store_hash(path: Optional[Path]) -> Optional[str]:
    """SHA-256 of a store's on-disk bytes; None when unconfigured/unreadable."""
    if path is None:
        return None
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


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
