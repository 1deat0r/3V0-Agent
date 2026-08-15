#!/usr/bin/env python3
"""Emit MEMORY.md / USER.md as a DERIVED VIEW of 3V0's native store.

Default: print to stdout (dry run). With --write, write into the Hermes
profile's memories/ directory — so the profile becomes a projection of the
store, not the origin.

Usage:
  python3 3v0/scripts/export_to_profile.py [--write]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.memory import MemoryStore  # noqa: E402
from core.profile_io import join_entries  # noqa: E402

PROFILE_MEM = Path.home() / ".hermes" / "profiles" / "3v0" / "memories"
STORE_PATH = REPO_ROOT / "3v0" / "data" / "memory.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--write",
        action="store_true",
        help="write into the profile memories/ dir (default: print only)",
    )
    args = ap.parse_args()

    store = MemoryStore(STORE_PATH)
    mem = join_entries([f.content for f in store.active("memory")])
    user = join_entries([f.content for f in store.active("user")])

    if args.write:
        PROFILE_MEM.mkdir(parents=True, exist_ok=True)
        (PROFILE_MEM / "MEMORY.md").write_text(mem, encoding="utf-8")
        (PROFILE_MEM / "USER.md").write_text(user, encoding="utf-8")
        print(f"Wrote {PROFILE_MEM / 'MEMORY.md'} and {PROFILE_MEM / 'USER.md'}")
    else:
        print("=== MEMORY.md (derived) ===")
        print(mem)
        print()
        print("=== USER.md (derived) ===")
        print(user)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
