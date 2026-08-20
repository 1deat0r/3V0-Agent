#!/usr/bin/env python3
"""Ingest a 3V0 memory-tool write into the native store (store-first).

Reads a JSON payload on stdin describing one memory-tool write and replays it
against the store under the cross-process lock. Called by the
``native-store-bridge`` profile plugin's ``post_tool_call`` hook as a
best-effort subprocess: every failure is reported on stderr with a non-zero
exit so the caller can swallow it, and the wake-time ``sync.py --write``
remains the backstop reconciler.

Payload shape (a single JSON object):

    {
      "target": "memory",                 # or "user"
      "source": "background_review",      # write origin (provenance)
      "ops": [
        {"action": "add", "content": "..."},
        {"action": "replace", "old_text": "...", "content": "..."},
        {"action": "remove", "old_text": "..."}
      ]
    }

Usage:
  echo '<json>' | python3 3v0/scripts/ingest.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.bridge import apply_ops  # noqa: E402
from core.store import open_store  # noqa: E402

# Override for tests: point at a scratch store instead of the real one.
STORE_PATH = Path(
    os.environ.get("THREEV0_STORE") or (REPO_ROOT / "3v0" / "data" / "memory.db")
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.parse_args()  # reserved for future flags

    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"ingest: bad JSON payload: {e}", file=sys.stderr)
        return 2

    target = payload.get("target")
    source = str(payload.get("source") or "assistant_tool")
    ops = payload.get("ops")
    if target not in {"memory", "user"}:
        print(f"ingest: bad target {target!r}", file=sys.stderr)
        return 2
    if not isinstance(ops, list):
        print("ingest: 'ops' must be a list", file=sys.stderr)
        return 2

    store = open_store(STORE_PATH)
    try:
        with store.mutate():
            applied = apply_ops(store, target, ops, source)
    except Exception as e:  # noqa: BLE001 - best-effort subprocess
        print(f"ingest failed: {e}", file=sys.stderr)
        return 1

    print(json.dumps({"applied": applied, "target": target, "source": source}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
