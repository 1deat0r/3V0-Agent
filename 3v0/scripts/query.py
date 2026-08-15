#!/usr/bin/env python3
"""Serve read-only queries against 3V0's native stores as JSON on stdout.

The CLI half of the ``threev0_store`` tool (registered by the
``native-store-bridge`` profile plugin). The plugin shells out here rather than
importing ``core.*`` into the Hermes runtime, keeping the runtime env clean and
matching the existing ingest pattern.

Usage:
  python3 3v0/scripts/query.py --action summary
  python3 3v0/scripts/query.py --action facts [--kind memory]
  python3 3v0/scripts/query.py --action fact_history --fact-id <id>
  python3 3v0/scripts/query.py --action skills [--name <skill>]
  python3 3v0/scripts/query.py --action skill_history --name <skill>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.memory import MemoryStore  # noqa: E402
from core.query import (  # noqa: E402
    fact_history,
    facts,
    skill_history,
    skills,
    summary,
)
from core.skills import SkillStore  # noqa: E402

MEM_PATH = REPO_ROOT / "3v0" / "data" / "memory.json"
SKILLS_PATH = REPO_ROOT / "3v0" / "data" / "skills.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--action",
        required=True,
        choices=["summary", "facts", "fact_history", "skills", "skill_history"],
    )
    ap.add_argument("--kind", choices=["memory", "user", "identity", "directive"])
    ap.add_argument("--fact-id")
    ap.add_argument("--name")
    args = ap.parse_args()

    mem = MemoryStore(MEM_PATH)
    skl = SkillStore(SKILLS_PATH)

    if args.action == "summary":
        result = summary(mem, skl)
    elif args.action == "facts":
        result = {"facts": facts(mem, args.kind)}
    elif args.action == "fact_history":
        if not args.fact_id:
            print(
                json.dumps({"error": "fact_history requires --fact-id"}),
                file=sys.stderr,
            )
            return 2
        result = {"fact_id": args.fact_id, "history": fact_history(mem, args.fact_id)}
    elif args.action == "skills":
        result = {"skills": skills(skl, args.name)}
    elif args.action == "skill_history":
        if not args.name:
            print(
                json.dumps({"error": "skill_history requires --name"}),
                file=sys.stderr,
            )
            return 2
        result = {"name": args.name, "history": skill_history(skl, args.name)}
    else:  # pragma: no cover - argparse choices already constrain this
        print(json.dumps({"error": f"unknown action {args.action!r}"}), file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
