#!/usr/bin/env python3
"""Reconcile the native skill store with the profile's SKILL.md files.

The store is the canonical record of 3V0's own skill evolution; the profile's
SKILL.md files are the operational view. Reports drift by default; with --write,
converges the two — importing unseen/drifted agent-created skills into the store
and dropping store-decommissioned skills from the profile (and re-materializing
store-active skills the profile lost). Store history is never destroyed.

Usage:
  python3 3v0/scripts/sync_skills.py [--write]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skill_io import profile_skills_dir  # noqa: E402
from core.skills import SkillStore  # noqa: E402
from core.sync_skills import sync_skills  # noqa: E402

# Override for tests: point at a scratch store instead of the real one.
STORE_PATH = Path(
    os.environ.get("THREEV0_SKILL_STORE") or (REPO_ROOT / "3v0" / "data" / "skills.json")
)


def _agent_created(skills_dir: Path) -> set[str]:
    """Skill names whose ``.usage.json`` entry has ``created_by == "agent"``."""
    return {name for name, meta in _usage(skills_dir).items() if meta.get("created_by") == "agent"}


def _curator_states(skills_dir: Path) -> dict[str, str]:
    """Skill name -> operational state (active/stale/archived) from ``.usage.json``."""
    return {
        name: meta.get("state", "active")
        for name, meta in _usage(skills_dir).items()
    }


def _usage(skills_dir: Path) -> dict:
    usage_path = skills_dir / ".usage.json"
    if not usage_path.exists():
        return {}
    return json.loads(usage_path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--write",
        action="store_true",
        help="write reconciled profile files (default: report only)",
    )
    args = ap.parse_args()

    skills_dir = profile_skills_dir()
    store = SkillStore(STORE_PATH)

    with store.mutate():
        report = sync_skills(
            store,
            skills_dir,
            _agent_created(skills_dir),
            args.write,
            curator_states=_curator_states(skills_dir),
        )

    print(
        f"imported={len(report.imported)} edited={len(report.edited)} "
        f"dropped={len(report.dropped)} exported={len(report.exported)} "
        f"unresolved={len(report.unresolved)} state_changes={len(report.state_changes)}"
    )
    for e in report.imported:
        print(f"  +import  {e}")
    for e in report.edited:
        print(f"  ~edit    {e}")
    for e in report.dropped:
        print(f"  -drop    {e}")
    for e in report.exported:
        print(f"  ->export {e}")
    for e in report.unresolved:
        print(f"  ?unres   {e}")
    for e in report.state_changes:
        print(f"  ^state   {e}")

    if args.write:
        print("Wrote reconciled skills.json / SKILL.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
