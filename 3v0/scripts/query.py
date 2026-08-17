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

import os  # noqa: E402

from core.retrieval import inject  # noqa: E402
from core.store import SQLStore, open_store  # noqa: E402
from core.query import (  # noqa: E402
    fact_history,
    facts,
    skill_history,
    skills,
    summary,
)
from core.skills import SkillStore  # noqa: E402

# Env override (tests / explicit): same convention as record.py + ingest.py.
MEM_PATH = Path(
    os.environ.get("THREEV0_STORE") or (REPO_ROOT / "3v0" / "data" / "memory.db")
)
SKILLS_PATH = REPO_ROOT / "3v0" / "data" / "skills.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--action",
        required=True,
        choices=["summary", "facts", "fact_history", "skills", "skill_history",
                 "retrieve"],
    )
    ap.add_argument("--kind", choices=["memory", "user", "identity", "directive"])
    ap.add_argument("--fact-id")
    ap.add_argument("--name")
    ap.add_argument("--query", dest="query_terms",
                    help="space-separated terms for action=retrieve")
    ap.add_argument("--budget", type=int, default=None,
                    help="budget cap for action=retrieve")
    args = ap.parse_args()

    mem = open_store(MEM_PATH)
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
    elif args.action == "retrieve":
        if not isinstance(mem, SQLStore):
            print(
                json.dumps({
                    "error": "retrieve requires the SQLite store (memory.db); "
                             "this project's store has not been rewired yet"}),
                file=sys.stderr,
            )
            return 2
        terms = (args.query_terms or "").split() or None
        kwargs = {"query_terms": terms, "touch": True}
        if args.kind is not None:
            kwargs["kind"] = args.kind
        if args.budget is not None:
            kwargs["budget_chars"] = args.budget
        inj = inject(mem.conn, **kwargs)
        result = {
            "facts": inj.facts,
            "text": inj.text,
            "truncated": inj.truncated,
            "budget_chars": inj.budget_chars,
        }
    else:  # pragma: no cover - argparse choices already constrain this
        print(json.dumps({"error": f"unknown action {args.action!r}"}), file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
