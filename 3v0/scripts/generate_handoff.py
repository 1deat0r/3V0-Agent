#!/usr/bin/env python3
"""Generate the mechanical handoff draft (``HANDOFF.generated.md``) — Stone 18.

The collection half of the shadow-mode generated handoff. It gathers the
mechanical state a fresh session must know — body git state, the continuity
invariant report, the project-ledger drift report, the tracked upstream loops
(claim registry + live GitHub), store counts, and daemon health — renders the
``HANDOFF.generated.md`` draft via ``core/handoff.py``, and reports the shadow
diff (how far the hand-written ``HANDOFF.md``'s loop-state assertions have
drifted from live reality).

The draft is the **canonical carrier of mechanical state** (operator-
authorized flip, 2026-08-16): it writes only ``HANDOFF.generated.md`` and
never touches the narrative ``HANDOFF.md``. The loop-claim diff is ongoing
drift monitoring between the hand-written narrative and live reality.

Modes:
  (default)     collect + render + write HANDOFF.generated.md + print the
                loop-claim shadow diff + a short banner
  --stdout      render the draft to stdout instead of writing (no diff)
  --json        emit the collected context + loop diff as JSON (tests / scripts)

Env (tests / explicit): THREEV0_BODY (body root), THREEV0_STORE,
  THREEV0_SKILL_STORE, THREEV0_CLAIMS (claims.json path). THREEV0_LEDGER /
  THREEV0_ANCHOR etc. flow through to the continuity/drift subprocesses via the
  inherited environment.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.handoff import diff_loop_claims, render_handoff  # noqa: E402
from core.memory import MemoryStore  # noqa: E402
from core.query import summary  # noqa: E402
from core.skills import SkillStore  # noqa: E402

BODY = Path(os.environ.get("THREEV0_BODY") or REPO_ROOT)
STORE_PATH = Path(
    os.environ.get("THREEV0_STORE") or (BODY / "3v0" / "data" / "memory.json")
)
SKILL_STORE_PATH = Path(
    os.environ.get("THREEV0_SKILL_STORE") or (BODY / "3v0" / "data" / "skills.json")
)
CLAIMS_PATH = Path(
    os.environ.get("THREEV0_CLAIMS")
    or (BODY / "3v0" / "data" / "continuity" / "claims.json")
)
GENERATED_PATH = BODY / "HANDOFF.generated.md"
HANDOFF_PATH = BODY / "HANDOFF.md"

CONTINUITY_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "continuity_check.py"
DRIFT_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "drift_check.py"

# The own-clock review daemons (systemd user services). Mirrors the trio named
# in HANDOFF.md / memory; add a service here when onboarding a new project.
DAEMONS = ("3v0-review", "f1nance-review", "axiom-review")


def _git(args: list, cwd: Path = BODY) -> tuple:
    """Run a git command; returns (ok, stripped_stdout)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(cwd), *args], capture_output=True, text=True, timeout=30
        )
    except (subprocess.TimeoutExpired, OSError):
        return False, ""
    return proc.returncode == 0, (proc.stdout or "").strip()


def _git_num(args: list, cwd: Path = BODY) -> str:
    ok, out = _git(args, cwd)
    return out if ok and out else "?"


def collect_git() -> dict:
    """Body git state: branch, ahead/behind (vs origin/main), dirty, recent."""
    branch = _git_num(["rev-parse", "--abbrev-ref", "HEAD"])
    head = _git_num(["rev-parse", "--short", "HEAD"])
    ahead = _git_num(["rev-list", "--count", "origin/main..HEAD"])
    behind = _git_num(["rev-list", "--count", "HEAD..origin/main"])
    ok, porc = _git(["status", "--porcelain"])
    dirty = bool(porc) if ok else None
    ok, log = _git(["log", "--oneline", "-10"])
    recent = log.splitlines() if ok else []
    return {
        "branch": branch,
        "ahead": ahead,
        "behind": behind,
        "dirty": dirty,
        "recent": recent,
        "head": head,
    }


def _run_json(script: Path) -> dict:
    """Run a 3v0 report script with ``--json``; returns the parsed dict ({} on
    any failure — the generator is best-effort, like every other collector)."""
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "--json"],
            capture_output=True, text=True, timeout=180,
        )
    except (subprocess.TimeoutExpired, OSError):
        return {}
    if proc.returncode != 0 or not proc.stdout.strip():
        return {}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {}


def _load_claims() -> dict:
    """The loop claim registry (single source of truth for tracked loops)."""
    try:
        data = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {"error": str(e)}
    if not isinstance(data, dict) or not isinstance(data.get("loops"), dict):
        return {"error": f"malformed claim registry: {CLAIMS_PATH}"}
    return data


def _gh_loop(kind: str, num: str, repo: str) -> tuple:
    """Live fields for one loop via ``gh``; (ok, dict, error).

    Fetches the fields the handoff table needs. ``mergeable`` is PR-only, so
    the field list is kind-aware (an issue query for ``mergeable`` is an error,
    not a None). ``continuity_check._gh_loop_state`` fetches only ``state`` —
    same command family, different shape; keep the two in sync if the command
    changes."""
    fields = "state,mergeable,updatedAt,title" if kind == "pr" else "state,updatedAt,title"
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


def collect_loops() -> list:
    """Tracked upstream loops: claim registry merged with live GitHub state."""
    claims = _load_claims()
    if "error" in claims:
        return []
    repo = claims.get("repo") or "NousResearch/hermes-agent"
    specs = claims.get("loops") or {}
    loops = []
    for num in sorted(specs, key=lambda n: int(n) if str(n).isdigit() else 0):
        spec = specs[num] if isinstance(specs[num], dict) else {}
        kind = (spec.get("kind") or "pr")
        ok, live, err = _gh_loop(kind, str(num), repo)
        loops.append(
            {
                "num": str(num),
                "kind": kind,
                "claimed_state": spec.get("state"),
                "as_of": spec.get("as_of"),
                "note": spec.get("note"),
                "live_state": (live or {}).get("state") if ok else None,
                "live_ok": ok,
                "live_error": err,
                "mergeable": (live or {}).get("mergeable") if ok else None,
                "updated_at": (live or {}).get("updatedAt") if ok else None,
                "title": (live or {}).get("title") if ok else None,
            }
        )
    return loops


def collect_store() -> dict:
    """Store counts (active facts by kind + skill/version counts), best-effort."""
    try:
        mem = MemoryStore(STORE_PATH)
        skl = SkillStore(SKILL_STORE_PATH)
        return summary(mem, skl)
    except (OSError, ValueError) as e:
        return {"error": str(e)}


def collect_daemons() -> dict:
    """``systemctl --user is-active`` for the own-clock review daemons."""
    try:
        proc = subprocess.run(
            ["systemctl", "--user", "is-active", *DAEMONS],
            capture_output=True, text=True, timeout=30,
        )
    except (subprocess.TimeoutExpired, OSError):
        return {}
    if proc.returncode not in (0, 3):  # 3 = at least one unit inactive (still ran)
        return {}
    states = [line.strip() for line in (proc.stdout or "").splitlines() if line.strip()]
    return {name: (states[i] if i < len(states) else "unknown") for i, name in enumerate(DAEMONS)}


def build_context() -> dict:
    """Collect every mechanical fact and shape it into the render context."""
    git = collect_git()
    loops = collect_loops()
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_head": git.get("head"),
        "git": git,
        "continuity": _run_json(CONTINUITY_SCRIPT),
        "drift": _run_json(DRIFT_SCRIPT),
        "loops": loops,
        "store": collect_store(),
        "daemons": collect_daemons(),
    }


def _handwritten() -> str:
    try:
        return HANDOFF_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""


def _print_loop_diff(loop_diff: list) -> None:
    print("Loop-claim drift (HANDOFF.md narrative vs live):")
    for d in loop_diff:
        mark = {"drift": "DRIFT", "agree": "agree", "unmentioned": "unmentioned", "unverifiable": "unverifiable"}[d["status"]]
        print(
            f"  {mark:12} #{d['num']}: asserted {d['asserted'] or '[]'} "
            f"vs truth {d['truth'] or '?'}"
        )


def main() -> int:
    ap = argparse.ArgumentParser(description="generate the mechanical handoff draft")
    ap.add_argument("--stdout", action="store_true", help="render to stdout instead of writing")
    ap.add_argument("--json", action="store_true", help="emit context + diff as JSON")
    args = ap.parse_args()

    ctx = build_context()
    loop_diff = diff_loop_claims(ctx["loops"], _handwritten())
    rendered = render_handoff(ctx)

    if args.json:
        print(json.dumps({"context": ctx, "loop_diff": loop_diff}, ensure_ascii=False, indent=2))
        return 0

    if args.stdout:
        print(rendered)
        return 0

    try:
        GENERATED_PATH.write_text(rendered, encoding="utf-8")
    except OSError as e:
        print(f"write failed: {e}", file=sys.stderr)
        return 1

    print(f"wrote {GENERATED_PATH}")
    print(rendered.splitlines()[0] if rendered else "(empty)")
    _print_loop_diff(loop_diff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
