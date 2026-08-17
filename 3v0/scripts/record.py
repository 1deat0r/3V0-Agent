#!/usr/bin/env python3
"""Record or retract a fact in the native store and export the derived view.

The store-first decision path: supersede an old fact (recoverable via history)
instead of silently rewriting the profile, or retract a fact (mark it removed),
then re-export so the Hermes profile stays a derived view of the store.

This CLI backs the ``threev0_record`` tool (``--json``) and is also the manual
store-first path (human text by default).

Usage:
  # record a new fact (human output)
  python3 3v0/scripts/record.py --kind memory --source foreground \
      --content "new fact text" --write

  # correct a fact store-first (supersede by substring or exact id)
  python3 3v0/scripts/record.py --kind memory --content "..." \
      --supersedes "old text" --write
  python3 3v0/scripts/record.py --kind memory --content "..." \
      --supersedes-id <fact-id> --write

  # retract a fact by id
  python3 3v0/scripts/record.py --retract <fact-id> --write

Default: dry run (prints what would change, writes nothing). Pass --write to
persist to the store and export the profile. --json emits a machine-readable
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

from core.decide import decide  # noqa: E402
from core.memory import MemoryStore  # noqa: E402
from core.project import project_memory  # noqa: E402

# Env overrides (tests / explicit): same convention as ingest.py (THREEV0_STORE);
# THREEV0_PROFILE_MEM redirects the projection target in tests.
STORE_PATH = Path(
    os.environ.get("THREEV0_STORE") or (REPO_ROOT / "3v0" / "data" / "memory.json")
)
PROFILE_MEM = Path(
    os.environ.get("THREEV0_PROFILE_MEM")
    or (Path.home() / ".hermes" / "profiles" / "3v0" / "memories")
)


def _print_human(result: dict) -> None:
    fact = result["fact"]
    print(f"{result['action']} ok: fact id={fact['id']} kind={fact['kind']}")
    if result.get("superseded_ids"):
        print(f"supersedes: {result['superseded_ids']}")
    if result.get("chain"):
        print("chain (oldest -> newest):")
        for f in result["chain"]:
            mark = "*" if f["id"] == fact["id"] else " "
            print(f" {mark} [{f['id']}] {f['content'][:70]}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["memory", "user", "identity", "directive"])
    ap.add_argument("--content", help="the new fact text (record only)")
    ap.add_argument("--source", default="foreground")
    ap.add_argument(
        "--supersedes-id",
        default=None,
        dest="supersedes_id",
        help="supersede the fact with this exact id (record only)",
    )
    ap.add_argument(
        "--supersedes",
        default=None,
        dest="supersedes_contains",
        help="supersede the active fact whose content contains this substring "
        "(exactly one; record only)",
    )
    ap.add_argument(
        "--retract",
        metavar="FACT_ID",
        default=None,
        help="retract (remove) the active fact with this id",
    )
    ap.add_argument(
        "--write",
        action="store_true",
        help="persist to store + export profile (default: dry run)",
    )
    ap.add_argument(
        "--no-export",
        action="store_true",
        help="with --write: persist to the store but skip the profile "
        "projection (store-only sibling projects)",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="emit a machine-readable JSON result on stdout",
    )
    args = ap.parse_args()

    if args.retract is not None and (
        args.content or args.supersedes_id or args.supersedes_contains
    ):
        print("--retract cannot be combined with --content/--supersedes*", file=sys.stderr)
        return 2
    if args.retract is None and not args.content:
        print("either --content (record) or --retract <id> is required", file=sys.stderr)
        return 2

    decision: dict = {
        "action": "retract" if args.retract is not None else "record",
        "source": args.source,
    }
    if args.retract is not None:
        decision["fact_id"] = args.retract
    else:
        decision["kind"] = args.kind
        decision["content"] = args.content
        if args.supersedes_id:
            decision["fact_id"] = args.supersedes_id
        if args.supersedes_contains:
            decision["supersedes"] = args.supersedes_contains

    store = MemoryStore(STORE_PATH)
    with store.mutate():
        result = decide(store, decision, persist=args.write)

    if "error" in result:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"refused: {result['error']}", file=sys.stderr)
        return 1

    if args.write and not args.no_export:
        result["projected"] = project_memory(store, PROFILE_MEM)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_human(result)
        if args.write:
            if args.no_export:
                print("Persisted to store (no profile export — store-only)")
            else:
                print("Exported derived view to profile MEMORY.md / USER.md")
        else:
            print("(dry run — pass --write to persist and export)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
