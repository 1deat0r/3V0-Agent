"""Tests for 3V0's store-first skill decision layer (stdlib only, no network).

Run directly:
  python3 3v0/tests/test_decide_skills.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.decide_skills import decide_skill  # noqa: E402
from core.skills import ABSORBED, RETRACTED, SkillStore  # noqa: E402


class TestDecideSkill(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "skills.json")
        self.store = SkillStore(self.path)

    def _seed(self, name: str = "my-skill"):
        return self.store.add(name, "create", "test", content="---\nname: my-skill\n---\nbody v1\n")

    def test_skill_update_plain(self) -> None:
        # Updating a skill the store has never seen starts a lineage (no
        # supersession link) — the same contract as decide.py's plain record.
        r = decide_skill(
            self.store,
            {"action": "skill_update", "name": "my-skill", "content": "---\nname: my-skill\n---\nbody v2\n"},
        )
        self.assertTrue(r["ok"])
        self.assertEqual(r["action"], "skill_update")
        self.assertEqual(r["skill"]["action"], "edit")
        self.assertEqual(r["superseded_ids"], [])
        head = self.store.latest_active("my-skill")
        self.assertIsNotNone(head)
        # content is stripped on store (consistent with skill_bridge.py)
        self.assertEqual(head.content, "---\nname: my-skill\n---\nbody v2")

    def test_skill_update_supersedes_previous_version(self) -> None:
        old = self._seed()
        r = decide_skill(
            self.store,
            {"action": "skill_update", "name": "my-skill", "content": "v2"},
        )
        self.assertEqual(r["superseded_ids"], [old.id])
        self.assertFalse(old.active)
        self.assertEqual(
            [v["content"] for v in r["chain"]],
            ["---\nname: my-skill\n---\nbody v1\n", "v2"],
        )

    def test_skill_update_missing_name_refused(self) -> None:
        r = decide_skill(self.store, {"action": "skill_update", "content": "x"})
        self.assertIn("error", r)

    def test_skill_update_missing_content_refused(self) -> None:
        r = decide_skill(self.store, {"action": "skill_update", "name": "my-skill"})
        self.assertIn("error", r)
        self.assertEqual(self.store.active(), [])

    def test_skill_retract(self) -> None:
        v = self._seed()
        r = decide_skill(self.store, {"action": "skill_retract", "name": "my-skill"})
        self.assertTrue(r["ok"])
        self.assertEqual(r["action"], "skill_retract")
        self.assertFalse(v.active)
        self.assertEqual(v.superseded_by, RETRACTED)
        self.assertIsNone(self.store.latest_active("my-skill"))

    def test_skill_retract_unknown_name_refused(self) -> None:
        r = decide_skill(self.store, {"action": "skill_retract", "name": "nope"})
        self.assertIn("error", r)

    def test_skill_retract_missing_name_refused(self) -> None:
        r = decide_skill(self.store, {"action": "skill_retract"})
        self.assertIn("error", r)

    def test_skill_absorb(self) -> None:
        v = self._seed()
        r = decide_skill(
            self.store,
            {"action": "skill_absorb", "name": "my-skill", "absorbed_into": "umbrella"},
        )
        self.assertTrue(r["ok"])
        self.assertEqual(r["action"], "skill_absorb")
        self.assertEqual(r["absorbed_into"], "umbrella")
        self.assertFalse(v.active)
        self.assertEqual(v.superseded_by, ABSORBED)
        self.assertEqual(v.absorbed_into, "umbrella")
        self.assertEqual(self.store.absorbed_by("umbrella"), ["my-skill"])

    def test_skill_absorb_missing_umbrella_refused(self) -> None:
        self._seed()
        r = decide_skill(self.store, {"action": "skill_absorb", "name": "my-skill"})
        self.assertIn("error", r)
        self.assertIsNotNone(self.store.latest_active("my-skill"))

    def test_unknown_action_refused(self) -> None:
        r = decide_skill(self.store, {"action": "frobnicate", "name": "x"})
        self.assertIn("error", r)

    def test_dry_run_does_not_persist(self) -> None:
        self._seed()
        decide_skill(
            self.store,
            {"action": "skill_update", "name": "my-skill", "content": "no persist"},
            persist=False,
        )
        s2 = SkillStore(self.path)
        self.assertNotIn("no persist", [v.content for v in s2.versions("my-skill")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
