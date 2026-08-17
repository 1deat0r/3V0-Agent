"""Git collection — best-effort live facts for a ledger entry's repo.

The collection half of the drift clock: shell out to ``git`` and read store
bytes, degrading to error flags rather than crashes. Split from
``core/drift.py`` so that module stays pure (decision-only), matching the
continuity/handoff split where the collection half lives apart from the
decision half.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

from .drift import GitState
from .projects import LedgerEntry


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
