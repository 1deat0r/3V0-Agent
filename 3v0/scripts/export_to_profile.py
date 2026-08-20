#!/usr/bin/env python3
"""Emit MEMORY.md / USER.md as a DERIVED VIEW of 3V0's native store.

Default: print to stdout (dry run). With --write, write into the 3V0
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

from core.store import open_store  # noqa: E402
from core.project import project_memory  # noqa: E402
from core.sync import profile_text  # noqa: E402

PROFILE_MEM = Path.home() / ".3V0" / "profiles" / "3v0" / "memories"
STORE_PATH = REPO_ROOT / "3v0" / "data" / "memory.db"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--write",
        action="store_true",
        help="write into the profile memories/ dir (default: print only)",
    )
    args = ap.parse_args()

    store = open_store(STORE_PATH)

    if args.write:
        project_memory(store, PROFILE_MEM)
        print(f"Wrote {PROFILE_MEM / 'MEMORY.md'} and {PROFILE_MEM / 'USER.md'}")
    else:
        print("=== MEMORY.md (derived) ===")
        print(profile_text(store, "memory"))
        print()
        print("=== USER.md (derived) ===")
        print(profile_text(store, "user"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
