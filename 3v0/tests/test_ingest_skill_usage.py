"""Tests for the skill-usage ingest script (3V0 read-feedback loop).

Run directly:
  python3 3v0/tests/test_ingest_skill_usage.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skills import SkillStore  # noqa: E402

SCRIPT = REPO_ROOT / "3v0" / "scripts" / "ingest_skill_usage.py"


def _run(payload: dict, store_path: Path) -> subprocess.CompletedProcess:
    """Run the ingest script with a scratch store, returning the process."""
    env = dict(os.environ)
    env["THREEV0_SKILL_STORE"] = str(store_path)
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env=env,
        timeout=30,
    )


class TestIngestSkillUsage(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.mkdtemp()
        self.path = os.path.join(self._tmp, "skills.json")
        # A pre-seeded skill to mirror what the store looks like after a write.
        store = SkillStore(self.path)
        store.add("foo", "create", "assistant_tool", content="---\nname: foo\n")
        del store

    def test_loaded_event_touches_store_and_syncs_counter(self) -> None:
        proc = _run({"skill_name": "foo", "event": "loaded", "source": "assistant_tool", "use_count": 3}, self.path)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["skill_name"], "foo")
        self.assertEqual(out["meta"]["uses"], 3)
        # The store now carries the usage and the by_usage bookmark (M3 reads it).
        s = SkillStore(self.path)
        self.assertEqual(s.skill_meta("foo")["uses"], 3)
        self.assertEqual(s.skill_meta("foo")["rank_mode"], "by_usage")

    def test_missing_skill_is_a_noop(self) -> None:
        proc = _run({"skill_name": "nope", "event": "loaded", "source": "assistant_tool", "use_count": 1}, self.path)
        self.assertEqual(proc.returncode, 0)
        self.assertIsNone(json.loads(proc.stdout)["meta"])
        # no boom, no partial state
        s = SkillStore(self.path)
        self.assertEqual(s.skill_meta("nope"), {})

    def test_missing_skill_name_rejected(self) -> None:
        proc = _run({"event": "loaded", "source": "assistant_tool", "use_count": 1}, self.path)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("skill_name", proc.stderr)

    def test_bad_json_rejected(self) -> None:
        env = dict(os.environ)
        env["THREEV0_SKILL_STORE"] = self.path
        proc = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="{not-json",
            text=True,
            capture_output=True,
            env=env,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 2)

    def test_patch_only_does_not_record_a_use(self) -> None:
        # A lone patch/edit is authoring, not usage — the curator never counts
        # it as a load. The store carries the diagnostic provenance but no
        # use-count bump and no by_usage flip.
        proc = _run({"skill_name": "foo", "event": "patched", "source": "assistant_tool"}, self.path)
        self.assertEqual(proc.returncode, 0)
        s = SkillStore(self.path)
        meta = s.skill_meta("foo")
        self.assertNotIn("uses", meta)
        self.assertNotIn("rank_mode", meta)
        self.assertEqual(meta.get("last_used_source"), "assistant_tool")

    def test_loaded_event_creates_no_new_lineage_version(self) -> None:
        proc = _run({"skill_name": "foo", "event": "loaded", "source": "assistant_tool", "use_count": 1}, self.path)
        self.assertEqual(proc.returncode, 0)
        s = SkillStore(self.path)
        # Still the single create; the head is active; meta gained usage only.
        self.assertEqual(len(s.versions("foo")), 1)
        self.assertTrue(s.latest_active("foo").active)


if __name__ == "__main__":
    unittest.main(verbosity=2)