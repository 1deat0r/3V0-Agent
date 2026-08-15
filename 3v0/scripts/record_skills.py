#!/usr/bin/env python3
"""Apply a store-first skill decision and project the derived SKILL.md.

Mirrors ``scripts/record.py`` for the skill axis: update a skill (append a
content version, superseding the active one), retract it (prune, recoverable),
or absorb it into an umbrella — then project the profile's SKILL.md so the
profile stays the operational (derived) view of the store.

This CLI backs the skill actions of the ``threev0_record`` tool (``--json``)
and is also the manual store-first skill path.

Usage:
  # update a skill (full replacement content, store-first)
  python3 3v0/scripts/record_skills.py --action skill_update \\
      --name my-skill --content "$(cat SKILL.md)" --write

  # decommission a skill (recoverable prune)
  python3 3v0/scripts/record_skills.py --action skill_retract \\
      --name my-skill --write

  # fold a skill into an umbrella
  python3 3v0/scripts/record_skills.py --action skill_absorb \\
      --name old-skill --absorbed-into umbrella --write

Default: dry run (prints what would change, writes nothing). Pass --write to
persist to the store and project the profile. --json emits a machine-readable
result on stdout (used by the tool).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.decide_skills import decide_skill  # noqa: E402
from core.skill_io import (  # noqa: E402
    find_skill_md,
    profile_skills_dir,
    remove_skill,
    write_skill_md,
)
from core.skills import SkillStore  # noqa: E402

# Env override (tests / explicit), same convention as sync_skills.py /
# ingest_skills.py / seed_skills.py. THREEV0_SKILLS_DIR redirects the
# projection target (honored by core/skill_io.py).
SKILL_STORE = Path(
    os.environ.get("THREEV0_SKILL_STORE")
    or (REPO_ROOT / "3v0" / "data" / "skills.json")
)


def _project(name: str, action: str, content: str, category: str) -> str:
    """Project the derived view onto the profile's SKILL.md.

    ``skill_update`` overwrites the existing SKILL.md in place (found by name,
    so a category move never orphans a duplicate) or writes a new one;
    ``skill_retract`` / ``skill_absorb`` remove the live skill directory.
    """
    skills_dir = profile_skills_dir()
    if action == "skill_update":
        existing = find_skill_md(skills_dir, name)
        if existing is not None:
            existing.path.write_text(content, encoding="utf-8")
            return str(existing.path)
        return str(write_skill_md(skills_dir, name, content, category or ""))
    removed = remove_skill(skills_dir, name)
    return "removed" if removed else "absent"


def _print_human(result: dict) -> None:
    skill = result["skill"]
    print(f"{result['action']} ok: name={skill['name']} version={skill['id']}")
    if result.get("superseded_ids"):
        print(f"supersedes: {result['superseded_ids']}")
    if result.get("absorbed_into"):
        print(f"absorbed into: {result['absorbed_into']}")
    chain = result.get("chain") or []
    if chain:
        print("chain (oldest -> newest):")
        for v in chain:
            mark = "*" if v["id"] == skill["id"] else " "
            print(f" {mark} [{v['id']}] {v['action']} by {v['source']}")


def main() -> int:
    ap = argparse.ArgumentParser(description="store-first skill decisions")
    ap.add_argument(
        "--action",
        choices=["skill_update", "skill_retract", "skill_absorb"],
        required=True,
    )
    ap.add_argument("--name", required=True)
    ap.add_argument("--content", help="full SKILL.md text (skill_update only)")
    ap.add_argument(
        "--category",
        default="",
        help="category subdir for a NEW skill (skill_update only)",
    )
    ap.add_argument(
        "--absorbed-into",
        default="",
        dest="absorbed_into",
        help="umbrella skill name (skill_absorb only)",
    )
    ap.add_argument("--source", default="foreground")
    ap.add_argument(
        "--write",
        action="store_true",
        help="persist to store + project profile (default: dry run)",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="emit a machine-readable JSON result on stdout",
    )
    args = ap.parse_args()

    decision: dict = {"action": args.action, "source": args.source, "name": args.name}
    if args.action == "skill_update":
        if not (args.content or "").strip():
            print("--content is required for skill_update", file=sys.stderr)
            return 2
        decision["content"] = args.content
        decision["category"] = args.category
    elif args.action == "skill_absorb":
        if not args.absorbed_into.strip():
            print("--absorbed-into is required for skill_absorb", file=sys.stderr)
            return 2
        decision["absorbed_into"] = args.absorbed_into

    store = SkillStore(SKILL_STORE)
    with store.mutate():
        result = decide_skill(store, decision, persist=args.write)

    if "error" in result:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"refused: {result['error']}", file=sys.stderr)
        return 1

    if args.write:
        result["projected"] = _project(
            args.name, args.action, args.content or "", args.category
        )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_human(result)
        if args.write:
            print(f"Projected to {result['projected']}")
        else:
            print("(dry run — pass --write to persist and project)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
