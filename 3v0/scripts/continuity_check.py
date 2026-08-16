#!/usr/bin/env python3
"""The reconstruction clock — one-page continuity report (Stone 17).

Evaluates every continuity invariant in ``core/continuity.py`` against the
body's collected state and prints a one-page report. Continuity drift is
*cross-artifact inconsistency* (two artifacts disagree about the same
reality), not freshness. Mechanical drift (memory store <-> profile, skill
store <-> SKILL.md) is healable via ``--heal``; semantic drift (anchor,
self-describing reachability, the project ledger) is flagged for deliberate
repair — the clock never auto-rewrites its own narrative.

The collection half is best-effort: an unreadable artifact degrades to a
flagged invariant, never a crash (a missing artifact is itself drift to
report).

Options:
  --heal           run the safe mechanical heal (sync.py --write +
                   sync_skills.py --write), then re-report post-heal state
  --json           machine-readable JSON on stdout (for the daemon tick)
  --fail-on-drift  exit 1 when any invariant reports drift (CI-style gate)

Env (tests / explicit): THREEV0_BODY, THREEV0_ANCHOR, THREEV0_STORE,
  THREEV0_PROFILE_MEM, THREEV0_SKILL_STORE, THREEV0_SKILLS_DIR,
  THREEV0_LEDGER.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.continuity import DEFAULT_INVARIANTS, evaluate  # noqa: E402
from core.memory import MemoryStore  # noqa: E402
from core.projects import ProjectLedger  # noqa: E402
from core.skill_io import profile_skills_dir  # noqa: E402
from core.skills import SkillStore  # noqa: E402
from core.sync import sync_kind  # noqa: E402
from core.sync_skills import sync_skills  # noqa: E402

BODY = Path(os.environ.get("THREEV0_BODY") or REPO_ROOT)
ANCHOR_PATH = Path(os.environ.get("THREEV0_ANCHOR") or (BODY / "3v0" / "CONTINUITY.md"))
STORE_PATH = Path(
    os.environ.get("THREEV0_STORE") or (BODY / "3v0" / "data" / "memory.json")
)
PROFILE_MEM = Path(
    os.environ.get("THREEV0_PROFILE_MEM")
    or (Path.home() / ".hermes" / "profiles" / "3v0" / "memories")
)
SKILL_STORE_PATH = Path(
    os.environ.get("THREEV0_SKILL_STORE") or (BODY / "3v0" / "data" / "skills.json")
)
LEDGER_PATH = Path(
    os.environ.get("THREEV0_LEDGER")
    or (BODY / "3v0" / "data" / "projects" / "ledger.json")
)
SYNC_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "sync.py"
SYNC_SKILLS_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "sync_skills.py"

# The model's canonical paths (must match core.continuity.CANONICAL_MODEL_PATHS
# — the anchor references them, and this collection verifies reachability).
_MODEL_PATHS = (
    "3v0/core/continuity.py",
    "3v0/scripts/continuity_check.py",
)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _usage(skills_dir: Path) -> dict:
    usage_path = skills_dir / ".usage.json"
    if not usage_path.exists():
        return {}
    try:
        return json.loads(usage_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _agent_created(skills_dir: Path) -> set:
    return {n for n, m in _usage(skills_dir).items() if m.get("created_by") == "agent"}


def _curator_states(skills_dir: Path) -> dict:
    return {n: m.get("state", "active") for n, m in _usage(skills_dir).items()}


def _collect() -> dict:
    """Gather the facts every invariant decides over (best-effort)."""
    ctx: dict = {}

    # anchor + self-describing
    ctx["anchor_present"] = ANCHOR_PATH.exists()
    ctx["anchor_text"] = _read(ANCHOR_PATH)
    ctx["model_reachable"] = {p: (BODY / p).exists() for p in _MODEL_PATHS}

    # memory store <-> profile
    mem_md = _read(PROFILE_MEM / "MEMORY.md")
    user_md = _read(PROFILE_MEM / "USER.md")
    try:
        store = MemoryStore(STORE_PATH)
        with store.mutate():
            mem_r = sync_kind(store, mem_md, "memory", write=False)
            user_r = sync_kind(store, user_md, "user", write=False)
        ctx["memory"] = {
            "imported": len(mem_r.imported),
            "dropped": len(mem_r.dropped),
            "exported": len(mem_r.exported),
        }
        ctx["user"] = {
            "imported": len(user_r.imported),
            "dropped": len(user_r.dropped),
            "exported": len(user_r.exported),
        }
    except (OSError, ValueError) as e:
        ctx["memory"] = {"error": str(e)}
        ctx["user"] = {"error": str(e)}

    # skill store <-> SKILL.md
    try:
        skills_dir = profile_skills_dir()
        sstore = SkillStore(SKILL_STORE_PATH)
        with sstore.mutate():
            rep = sync_skills(
                sstore,
                skills_dir,
                _agent_created(skills_dir),
                write=False,
                curator_states=_curator_states(skills_dir),
            )
        ctx["skills"] = {
            "imported": len(rep.imported),
            "edited": len(rep.edited),
            "dropped": len(rep.dropped),
            "exported": len(rep.exported),
            "unresolved": len(rep.unresolved),
            "state_changes": len(rep.state_changes),
        }
    except (OSError, ValueError) as e:
        ctx["skills"] = {"error": str(e)}

    # project ledger (the reconstruction clock's data source)
    try:
        ledger = ProjectLedger.load(body_root=BODY, home=Path.home(), path=LEDGER_PATH)
        ctx["ledger_ok"] = True
        ctx["ledger_count"] = len(ledger)
        ctx["ledger_detail"] = ""
    except (OSError, ValueError) as e:
        ctx["ledger_ok"] = False
        ctx["ledger_count"] = 0
        ctx["ledger_detail"] = str(e)

    return ctx


def _heal() -> List[str]:
    """Run the safe mechanical heal (store<->profile + store<->SKILL.md sync),
    best-effort. Returns one entry per writer with its outcome."""
    env = os.environ.copy()
    env.setdefault("THREEV0_STORE", str(STORE_PATH))
    env.setdefault("THREEV0_PROFILE_MEM", str(PROFILE_MEM))
    env.setdefault("THREEV0_SKILL_STORE", str(SKILL_STORE_PATH))
    outcomes: List[str] = []
    for script in (SYNC_SCRIPT, SYNC_SKILLS_SCRIPT):
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--write"],
                capture_output=True, text=True, timeout=120, env=env,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            outcomes.append(f"{script.name}:failed:{e}")
            continue
        if proc.returncode != 0:
            tail = (proc.stderr or "").strip().replace("\n", " ")[:120]
            outcomes.append(f"{script.name}:failed:{tail}")
        else:
            outcomes.append(f"{script.name}:ok")
    return outcomes


def run_check(heal: bool = False) -> dict:
    """Collect facts, evaluate invariants, optionally heal first."""
    healed: List[str] = []
    if heal:
        healed = _heal()
    report = evaluate(DEFAULT_INVARIANTS, _collect())
    report["checked_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if healed:
        report["healed"] = healed
    return report


def _print_human(result: dict) -> None:
    print(
        f"=== continuity check: {result['total']} invariant(s) "
        f"— {result['checked_at']} ==="
    )
    for r in result["invariants"]:
        verdict = "DRIFT" if r["drift"] else "OK"
        tag = " [healable]" if r["drift"] and r["healable"] else ""
        print(f"  {verdict:5} {r['name']:16} {r['detail']}{tag}")
    healable = (
        f", {result['healable_drift']} healable"
        if result.get("healable_drift")
        else ""
    )
    print(
        f"summary: {result['drift_count']} drifting{healable}, "
        f"{result['total'] - result['drift_count']} ok"
    )
    if result.get("healed"):
        print("healed: " + ", ".join(result["healed"]))


def main() -> int:
    ap = argparse.ArgumentParser(description="one-page continuity report")
    ap.add_argument("--heal", action="store_true", help="safe mechanical heal, then re-report")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--fail-on-drift", action="store_true", help="exit 1 if any invariant drifts")
    args = ap.parse_args()

    result = run_check(heal=args.heal)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        _print_human(result)

    if args.fail_on_drift and result.get("drift_count", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
