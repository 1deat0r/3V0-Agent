#!/usr/bin/env python3
"""Seed 3V0's native skill store from the profile's agent-created skills.

Reads the profile's ``skills/.usage.json`` and, for every skill the agent
itself created (``created_by == "agent"``), records its SKILL.md as a ``create``
version in ``3v0/data/skills.json`` with ``source="profile-import"``. Bundled /
hub-installed skills are deliberately excluded — this store is the record of
3V0's *own* evolution, not the inherited catalog.

Refuses to run if the store is already populated unless ``--force`` is given
(re-running must be deliberate, not accidental), mirroring ``seed_from_profile.py``.

Usage:
  python3 3v0/scripts/seed_skills.py [--force]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skills import SkillStore  # noqa: E402

PROFILE = Path.home() / ".hermes" / "profiles" / "3v0"
SKILLS_DIR = PROFILE / "skills"
STORE_PATH = REPO_ROOT / "3v0" / "data" / "skills.json"


def _find_skill_md(name: str) -> tuple[str, str]:
    """Return (content, category) for ``name``'s SKILL.md, or ("", "")."""
    for md in SKILLS_DIR.rglob("SKILL.md"):
        if md.parent.name == name:
            rel = md.parent.relative_to(SKILLS_DIR)
            category = "" if rel.parent == Path(".") else str(rel.parent)
            try:
                return md.read_text(encoding="utf-8"), category
            except OSError:
                return "", ""
    return "", ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    store = SkillStore(STORE_PATH)
    if store.skills and not args.force:
        print(
            f"Skill store already has {len(store.skills)} versions; pass --force to re-seed.",
            file=sys.stderr,
        )
        return 1

    if args.force:
        store.skills = []

    usage_path = SKILLS_DIR / ".usage.json"
    if not usage_path.exists():
        print(f"No {usage_path} — nothing to seed.", file=sys.stderr)
        return 1
    usage = json.loads(usage_path.read_text(encoding="utf-8"))

    n = 0
    for name, meta in usage.items():
        if meta.get("created_by") != "agent":
            continue
        content, category = _find_skill_md(name)
        if not content:
            continue  # archived / moved off the live path — skip
        created_at = meta.get("created_at", "")
        note = f"seeded from profile" + (f" (created {created_at})" if created_at else "")
        store.add(name, "create", "profile-import", content=content, category=category, note=note)
        n += 1

    print(f"Seeded {n} agent-created skills -> {STORE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
