#!/usr/bin/env python3
"""Reconcile the native store with the 3V0 profile (store is canonical).

Reports drift by default; with --write, converges the profile to the store's
active facts — importing profile-only entries into the store and dropping
superseded entries from the profile. Store history is never destroyed.

Usage:
  python3 3v0/scripts/sync.py [--write]
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.store import open_store  # noqa: E402
from core.project import project_memory  # noqa: E402
from core.sync import SyncReport, sync_kind  # noqa: E402

# Env overrides (tests / explicit): same convention as record.py + ingest.py.
# The own-clock daemon passes these so its sync pass operates on the same
# resolved paths it reviews (and E2E tests can redirect off the real profile).
STORE_PATH = Path(
    os.environ.get("THREEV0_STORE") or (REPO_ROOT / "3v0" / "data" / "memory.db")
)
PROFILE_MEM = Path(
    os.environ.get("THREEV0_PROFILE_MEM")
    or (Path.home() / ".3V0" / "profiles" / "3v0" / "memories")
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--write",
        action="store_true",
        help="write reconciled profile files (default: report only)",
    )
    args = ap.parse_args()

    store = open_store(STORE_PATH)
    mem_md = (PROFILE_MEM / "MEMORY.md").read_text(encoding="utf-8")
    user_md = (PROFILE_MEM / "USER.md").read_text(encoding="utf-8")

    reports: dict[str, SyncReport] = {}
    with store.mutate():
        reports = {
            "memory": sync_kind(store, mem_md, "memory", args.write),
            "user": sync_kind(store, user_md, "user", args.write),
        }
        if args.write:
            project_memory(store, PROFILE_MEM)

    for kind, r in reports.items():
        print(
            f"[{kind}] imported={len(r.imported)} "
            f"dropped={len(r.dropped)} exported={len(r.exported)}"
        )
        for e in r.imported:
            print(f"  +import  {e[:60]!r}")
        for e in r.dropped:
            print(f"  -drop    {e[:60]!r}")
        for e in r.exported:
            print(f"  ->export {e[:60]!r}")

    if args.write:
        print("Wrote reconciled MEMORY.md / USER.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
