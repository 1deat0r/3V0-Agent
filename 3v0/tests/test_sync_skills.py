"""Tests for 3V0 skill-store <-> profile reconciliation (stdlib only).

Run directly:
  python3 3v0/tests/test_sync_skills.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skill_io import find_skill_md  # noqa: E402
from core.skills import SkillStore  # noqa: E402
from core.sync_skills import sync_skills  # noqa: E402


def _mk_skill(skills_dir: Path, name: str, content: str, category: str = "") -> None:
    target = skills_dir / category / name if category else skills_dir / name
    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(content, encoding="utf-8")


class TestSyncSkills(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.skills_dir = Path(self.dir) / "skills"
        self.skills_dir.mkdir()
        self.store = SkillStore(os.path.join(self.dir, "skills.json"))

    def test_no_drift_reports_clean(self) -> None:
        _mk_skill(self.skills_dir, "foo", "---\nname: foo\nbody\n")
        self.store.add("foo", "create", "profile-import", content="---\nname: foo\nbody\n")
        r = sync_skills(self.store, self.skills_dir, {"foo"}, write=False)
        self.assertTrue(r.clean)

    def test_imports_unseen_agent_skill(self) -> None:
        _mk_skill(self.skills_dir, "foo", "---\nname: foo\n")
        r = sync_skills(self.store, self.skills_dir, {"foo"}, write=True)
        self.assertIn("foo", r.imported)
        self.assertEqual(self.store.latest_active("foo").content, "---\nname: foo\n")
        self.assertEqual(self.store.latest_active("foo").source, "profile-import")

    def test_ignores_non_agent_skill(self) -> None:
        _mk_skill(self.skills_dir, "bundled", "---\nname: bundled\n")
        r = sync_skills(self.store, self.skills_dir, set(), write=True)
        self.assertTrue(r.clean)  # not imported, not exported
        self.assertEqual(self.store.skills, [])

    def test_heals_bridge_missed_edit(self) -> None:
        _mk_skill(self.skills_dir, "foo", "---\nname: foo\nnewer body\n")
        self.store.add("foo", "create", "profile-import", content="---\nname: foo\nolder\n")
        r = sync_skills(self.store, self.skills_dir, {"foo"}, write=True)
        self.assertIn("foo", r.edited)
        head = self.store.latest_active("foo")
        self.assertEqual(head.action, "edit")
        self.assertEqual(head.content, "---\nname: foo\nnewer body\n")
        # supersession preserved
        self.assertEqual(len(self.store.history("foo")), 2)

    def test_edit_is_idempotent(self) -> None:
        content = "---\nname: foo\n"
        _mk_skill(self.skills_dir, "foo", content)
        self.store.add("foo", "create", "profile-import", content=content)
        r1 = sync_skills(self.store, self.skills_dir, {"foo"}, write=True)
        r2 = sync_skills(self.store, self.skills_dir, {"foo"}, write=True)
        self.assertTrue(r1.clean)
        self.assertTrue(r2.clean)
        self.assertEqual(len(self.store.versions("foo")), 1)

    def test_drops_decommissioned_skill(self) -> None:
        _mk_skill(self.skills_dir, "foo", "---\nname: foo\n")
        self.store.add("foo", "create", "a", content="---\nname: foo\n")
        self.store.retract("foo", source="test")
        r = sync_skills(self.store, self.skills_dir, {"foo"}, write=True)
        self.assertIn("foo", r.dropped)
        self.assertIsNone(find_skill_md(self.skills_dir, "foo"))

    def test_decommissioned_absent_is_noop(self) -> None:
        self.store.add("foo", "create", "a", content="x")
        self.store.retract("foo")
        r = sync_skills(self.store, self.skills_dir, set(), write=True)
        self.assertTrue(r.clean)  # nothing to drop (profile already absent)

    def test_exports_store_only_skill(self) -> None:
        self.store.add("foo", "create", "a", content="---\nname: foo\nbody\n", category="dev")
        r = sync_skills(self.store, self.skills_dir, {"foo"}, write=True)
        self.assertIn("foo", r.exported)
        sf = find_skill_md(self.skills_dir, "foo")
        self.assertIsNotNone(sf)
        self.assertEqual(sf.content, "---\nname: foo\nbody\n")
        self.assertEqual(sf.category, "dev")

    def test_unresolved_contentless_head(self) -> None:
        # A patch head with no captured content can't be projected or compared.
        _mk_skill(self.skills_dir, "foo", "---\nname: foo\nlive\n")
        self.store.add("foo", "create", "a", content="---\nname: foo\nold\n")
        self.store.add("foo", "patch", "a", note="patch 'x' -> 'y'")  # content=""
        r = sync_skills(self.store, self.skills_dir, {"foo"}, write=True)
        self.assertIn("foo", r.unresolved)
        # profile left untouched (operational truth preserved)
        self.assertEqual(find_skill_md(self.skills_dir, "foo").content, "---\nname: foo\nlive\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
