#!/usr/bin/env python3
"""Apply a store-first skill-ranking assignment (skill_promote / skill_demote).

Backs the ``threev0_record`` tool's ``skill_promote`` / ``skill_demote``
actions. Each sets a skill's ``meta.rank_mode`` (the display posture the
usage-aware ranker reads): ``skill_promote <name>`` => ``by_usage`` (the
skill stays full/ranked by usage; an explicit keep), ``skill_demote <name>``
=> ``default`` (the skill sinks to the names-only tail regardless of usage).

Mirrors ``scripts/record_skills.py``: env override ``THREEV0_SKILL_STORE``,
store-first under the cross-process ``mutate()`` lock, and the same
``--json`` / ``--write`` contract.

Usage:
  python3 3v0/scripts/record_skill_ranking.py --action skill_promote --name my-skill --write
  python3 3v0/scripts/record_skill_ranking.py --action skill_demote --name my-skill --write
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skills import SkillStore, META_RANK_MODE  # noqa: E402
from core.skill_outcome import set_skill_ranks  # noqa: E402

# Override for tests: point at a scratch store instead of the real one.
STORE_PATH = Path(
    os.environ.get("THREEV0_SKILL_STORE")
    or (REPO_ROOT / "3v0" / "data" / "skills.json")
)

_MODE = {"skill_promote": "by_usage", "skill_demote": "default"}


def main() -> int:
    ap = argparse.ArgumentParser(description="store-first skill-ranking assignment")
    ap.add_argument(
        "--action", required=True, choices=sorted(_MODE),
        help="skill_promote (by_usage) | skill_demote (default)",
    )
    ap.add_argument("--name", required=True, help="skill name (as shown by threev0_store)")
    ap.add_argument("--json", action="store_true", help="emit a machine-readable result")
    ap.add_argument("--write", action="store_true", help="persist (default is a dry run)")
    ap.add_argument("--source", default="threev0_record")
    args = ap.parse_args()

    store = SkillStore(STORE_PATH)
    mode = _MODE[args.action]
    # Check existence under a (non-locking) read first; set_skill_ranks takes
    # the cross-process lock itself — never nest mutate() (flock is not
    # reentrant in this process and would deadlock).
    if store.latest_active(args.name) is None:
        print(json.dumps({
            "error": f"skill '{args.name}' has no active version — nothing to rank",
        }))
        return 1
    if not args.write:
        print(json.dumps({
            "dry_run": True,
            "action": args.action,
            "name": args.name,
            "rank_mode": mode,
            "current": store.skill_meta(args.name).get(META_RANK_MODE, ""),
        }))
        return 0
    result = set_skill_ranks(store, {args.name: mode}, source=args.source)
    if args.json:
        print(json.dumps({"applied": bool(result), "name": args.name, "rank_mode": mode}))
    else:
        print(f"ranked {args.name} -> {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())