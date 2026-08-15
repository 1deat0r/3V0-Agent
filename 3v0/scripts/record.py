#!/usr/bin/env python3
"""Record a fact into the native store and export the derived view.

The store-first correction path: supersede an old fact (recoverable via
history) instead of silently rewriting the profile, then re-export so the
Hermes profile stays a derived view of the store.

Usage:
  python3 3v0/scripts/record.py --kind memory --source foreground \
      --content "new fact text" [--supersedes-id <id> | --supersedes "<substr>"]

Default: dry run (prints what would change, writes nothing). Pass --write to
persist to the store and export the profile.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.memory import MemoryStore  # noqa: E402
from core.record import RecordError, record  # noqa: E402
from core.sync import profile_text  # noqa: E402

PROFILE_MEM = Path.home() / ".hermes" / "profiles" / "3v0" / "memories"
STORE_PATH = REPO_ROOT / "3v0" / "data" / "memory.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--kind", required=True, choices=["memory", "user", "identity", "directive"]
    )
    ap.add_argument("--content", required=True, help="the new fact text")
    ap.add_argument("--source", default="foreground")
    ap.add_argument("--supersedes-id", default=None, help="supersede the fact with this id")
    ap.add_argument(
        "--supersedes",
        default=None,
        dest="supersedes_contains",
        help="supersede the active fact whose content contains this substring (exactly one)",
    )
    ap.add_argument(
        "--write",
        action="store_true",
        help="persist to store + export profile (default: dry run)",
    )
    args = ap.parse_args()

    store = MemoryStore(STORE_PATH)
    try:
        result = record(
            store,
            args.content,
            args.kind,
            args.source,
            supersede_id=args.supersedes_id,
            supersede_contains=args.supersedes_contains,
            persist=args.write,
        )
    except RecordError as e:
        print(f"record refused: {e}", file=sys.stderr)
        return 1

    print(f"new fact id={result.fact.id} kind={args.kind}")
    if result.superseded_ids:
        print(f"supersedes: {result.superseded_ids}")
        print("chain (oldest -> newest):")
        for f in result.chain:
            mark = "*" if f.id == result.fact.id else " "
            print(f" {mark} [{f.id}] {f.content[:70]}")

    if args.write:
        (PROFILE_MEM / "MEMORY.md").write_text(
            profile_text(store, "memory"), encoding="utf-8"
        )
        (PROFILE_MEM / "USER.md").write_text(
            profile_text(store, "user"), encoding="utf-8"
        )
        print("Exported derived view to profile MEMORY.md / USER.md")
    else:
        print("(dry run — pass --write to persist and export)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
