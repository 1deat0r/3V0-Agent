#!/usr/bin/env python3
"""Seed 3V0's native memory store from the 3V0 profile.

Reads the profile's MEMORY.md (entries split on '§') and USER.md and writes
them as provenance-carrying facts into 3v0/data/memory.json. Refuses to run
if the store is already populated unless --force is given (re-running must be
deliberate, not accidental).

Usage:
  python3 3v0/scripts/seed_from_profile.py [--force]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.store import open_store  # noqa: E402
from core.profile_io import split_entries  # noqa: E402

PROFILE = Path.home() / ".3V0" / "profiles" / "3v0"
STORE_PATH = REPO_ROOT / "3v0" / "data" / "memory.db"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    store = open_store(STORE_PATH)
    if store.facts and not args.force:
        print(
            f"Store already has {len(store.facts)} facts; pass --force to re-seed.",
            file=sys.stderr,
        )
        return 1

    if args.force:
        store.clear()

    n = 0
    mem = (PROFILE / "memories" / "MEMORY.md").read_text(encoding="utf-8")
    for entry in split_entries(mem):
        store.add(entry, "memory", "profile-seed")
        n += 1

    user = (PROFILE / "memories" / "USER.md").read_text(encoding="utf-8")
    for entry in split_entries(user):
        store.add(entry, "user", "profile-seed")
        n += 1

    print(f"Seeded {n} facts -> {STORE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
