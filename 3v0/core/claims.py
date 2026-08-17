"""Tracked-upstream-loop claim registry — the one owner of claim load/validate
and the ``gh`` view wrapper.

The loop/claim concept (a tracked upstream GitHub PR/issue whose state 3V0 is
waiting on) used to be spread across ``continuity_check.py`` and
``generate_handoff.py`` with two byte-identical ``_load_claims`` functions and
two divergent ``gh view`` wrappers held together by a literal "keep in sync"
comment. This module is that concept's single home: load/validate, the one
``gh`` wrapper (parameterized field set), and the default repo.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

DEFAULT_REPO = "NousResearch/hermes-agent"


def load_claims(claims_path: Path) -> Dict[str, Any]:
    """Load the loop claim registry; ``{"error": ...}`` when missing/bad."""
    try:
        data = json.loads(claims_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {"error": str(e)}
    if not isinstance(data, dict) or not isinstance(data.get("loops"), dict):
        return {"error": f"malformed claim registry: {claims_path}"}
    return data


def repo_of(claims: Dict[str, Any]) -> str:
    """The registry's repo, or the default upstream."""
    return claims.get("repo") or DEFAULT_REPO


def gh_loop(
    kind: str, num: str, repo: str, fields: str
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Live fields for one loop via ``gh``; returns (ok, data, error).

    ``fields`` is a comma-separated ``--json`` field list. ``data`` is the
    parsed JSON dict (None on failure). Callers extract the field(s) they need;
    a field valid for only one kind (``mergeable`` is PR-only) is the caller's
    choice to include.
    """
    cmd = ["gh", kind, "view", num, "--repo", repo, "--json", fields]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, OSError) as e:
        return False, None, str(e)
    if proc.returncode != 0:
        return False, None, (proc.stderr or "").strip().replace("\n", " ")[:120]
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return False, None, "gh output unparseable"
    return True, data, None
