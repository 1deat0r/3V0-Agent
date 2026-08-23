#!/usr/bin/env python3
"""Ingest 3V0 skill-read/use telemetry into the native skill store.

Reads a JSON payload on stdin describing one skill lifecycle event (a load /
view / patch already recorded in the profile's ``.usage.json`` sidecar) and
replays it against the native skill store under the cross-process lock. Called
by the ``native-store-bridge`` profile plugin's ``on_skill_lifecycle`` hook as
a best-effort subprocess: every failure is reported on stderr with a non-zero
exit so the caller can swallow it. This is the read-feedback link that closes
the skill "used" loop in the store (``touch_skill``), mirroring how
``ingest.py`` / ``ingest_skills.py`` close the *write* loop.

We intentionally do NOT read the sidecar ourselves: the hook already has the
per-event counters (``use_count``) and the origin (the writing agent), so the
payload stays a single self-contained event and the store never reaches into
profile internals. The store records usage on the active head (never a new
lineage version) — exactly the ``touch_skill`` contract.

Payload shape (a single JSON object):

    {
      "source": "assistant_tool",        # origin (provenance)
      "event": "loaded",                 # loaded|viewed|patched|edited
      "skill_name": "my-skill",
      "use_count": 3                     # the COUNT as of this event (resolver)
    }

Use (via the plugin — normally not invoked by hand):

  echo '{"skill_name":"my-skill","event":"loaded","source":"assistant_tool","use_count":1}' \
    | python3 3v0/scripts/ingest_skill_usage.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skills import SkillStore  # noqa: E402

# Override for tests: point at a scratch store instead of the real one.
STORE_PATH = Path(
    os.environ.get("THREEV0_SKILL_STORE")
    or (REPO_ROOT / "3v0" / "data" / "skills.json")
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.parse_args()  # reserved for future flags

    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"ingest_skill_usage: bad JSON payload: {e}", file=sys.stderr)
        return 2

    skill_name = str(payload.get("skill_name") or "").strip()
    if not skill_name:
        print("ingest_skill_usage: 'skill_name' is required", file=sys.stderr)
        return 2

    source = str(payload.get("source") or "assistant_tool")
    event = str(payload.get("event") or "loaded")
    use_count = payload.get("use_count")

    store = SkillStore(STORE_PATH)
    try:
        with store.mutate():
            head = store.latest_active(skill_name)
            if head is None:
                # Nothing to record usage against (missing or decommissioned).
                meta = None
            else:
                # The counter stored must be the AUTHORITATIVE count from the
                # sidecar (the source of truth), never an internally-computed
                # increment of a possibly-stale internal counter — a replayed or
                # partial lifecycle stream would otherwise drift the store away
                # from the sidecar. So we set it as the resolved value, and only
                # for a genuine use (a patch/edit is authoring, never a load).
                is_use = (
                    event in {"loaded", "viewed"}
                    and use_count is not None
                    and int(use_count) >= 1
                )
                fields: dict[str, object] = {
                    "last_used_source": source,
                }
                if is_use:
                    fields["uses"] = int(use_count)
                    fields["rank_mode"] = "by_usage"
                meta = store.set_skill_meta(skill_name, **fields)
    except Exception as e:  # noqa: BLE001 - best-effort subprocess
        print(f"ingest_skill_usage failed: {e}", file=sys.stderr)
        return 1

    print(json.dumps({"skill_name": skill_name, "source": source, "event": event, "meta": meta}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())