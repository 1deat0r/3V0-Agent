#!/usr/bin/env python3
"""Ingest a Hermes skill_manage write into the native skill store.

Reads a JSON payload on stdin describing one skill_manage write and replays it
against the skill store under the cross-process lock. Called by the
``native-store-bridge`` profile plugin's ``post_tool_call`` hook as a
best-effort subprocess: every failure is reported on stderr with a non-zero
exit so the caller can swallow it.

For a ``patch`` the tool args carry only the old/new snippets; the resulting
SKILL.md is resolved from the profile (which the tool has already written) so
the recorded version carries full content and can be projected back by
``sync_skills.py``. If the file can't be read, the version degrades to
note-only.

Payload shape (a single JSON object):

    {
      "source": "background_review",   # write origin (provenance)
      "args": {
        "action": "create",            # create|patch|edit|write_file|remove_file|delete
        "name": "my-skill",
        "content": "---\\n...",         # create/edit full SKILL.md
        "category": "software-development",
        "file_path": "references/x.md",  # write_file/remove_file
        "file_content": "...",           # write_file
        "old_string": "...", "new_string": "...",  # patch
        "absorbed_into": "umbrella"      # delete (consolidation)
      }
    }

Usage:
  echo '<json>' | python3 3v0/scripts/ingest_skills.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skill_bridge import apply_skill_op  # noqa: E402
from core.skill_io import find_skill_md, profile_skills_dir  # noqa: E402
from core.skills import SkillStore  # noqa: E402

# Override for tests: point at a scratch store instead of the real one.
STORE_PATH = Path(
    os.environ.get("THREEV0_SKILL_STORE") or (REPO_ROOT / "3v0" / "data" / "skills.json")
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.parse_args()  # reserved for future flags

    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"ingest_skills: bad JSON payload: {e}", file=sys.stderr)
        return 2

    source = str(payload.get("source") or "assistant_tool")
    args = payload.get("args")
    if not isinstance(args, dict):
        print("ingest_skills: 'args' must be an object", file=sys.stderr)
        return 2

    # A patch's tool args carry only old/new snippets; resolve the resulting
    # SKILL.md from the profile so the recorded version is projectable.
    if args.get("action") == "patch":
        sf = find_skill_md(profile_skills_dir(), (args.get("name") or "").strip())
        if sf is not None:
            args = {**args, "content": sf.content}

    store = SkillStore(STORE_PATH)
    try:
        with store.mutate():
            applied = apply_skill_op(store, args, source)
    except Exception as e:  # noqa: BLE001 - best-effort subprocess
        print(f"ingest_skills failed: {e}", file=sys.stderr)
        return 1

    print(json.dumps({"applied": applied, "source": source}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
