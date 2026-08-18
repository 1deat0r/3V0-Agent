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
from core.sync_skills import (  # noqa: E402
    DROP,
    EDIT,
    EXPORT,
    IMPORT,
    NOOP,
    UNRESOLVED,
    diff_skills,
    sync_skills,
)


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

    def test_folds_curator_state(self) -> None:
        _mk_skill(self.skills_dir, "foo", "---\nname: foo\n")
        self.store.add("foo", "create", "a", content="---\nname: foo\n")
        r = sync_skills(
            self.store, self.skills_dir, {"foo"}, write=True, curator_states={"foo": "stale"}
        )
        self.assertIn("foo: active->stale", r.state_changes)
        self.assertEqual(self.store.state("foo"), "stale")
        # content in agreement -> no other drift
        self.assertEqual(r.imported, [])
        self.assertEqual(r.edited, [])

    def test_state_fold_is_idempotent(self) -> None:
        _mk_skill(self.skills_dir, "foo", "---\nname: foo\n")
        self.store.add("foo", "create", "a", content="---\nname: foo\n")
        cs = {"foo": "stale"}
        sync_skills(self.store, self.skills_dir, {"foo"}, write=True, curator_states=cs)
        r2 = sync_skills(self.store, self.skills_dir, {"foo"}, write=True, curator_states=cs)
        self.assertEqual(r2.state_changes, [])
        self.assertTrue(r2.clean)

    def test_archived_skill_not_exported(self) -> None:
        # Store has it, live profile lacks it, curator says archived -> not
        # "missing", so it must NOT be re-materialized.
        self.store.add("foo", "create", "a", content="---\nname: foo\nbody\n", category="dev")
        r = sync_skills(
            self.store, self.skills_dir, {"foo"}, write=True, curator_states={"foo": "archived"}
        )
        self.assertEqual(r.exported, [])
        self.assertIn("foo: active->archived", r.state_changes)
        self.assertIsNone(find_skill_md(self.skills_dir, "foo"))  # stayed archived

    def test_archive_dir_excluded_from_live_index(self) -> None:
        # A skill whose directory lives only under .archive/ is not seen as live,
        # and with curator state archived it folds state without re-exporting.
        _mk_skill(self.skills_dir, "foo", "---\nname: foo\n", category=".archive")
        self.store.add("foo", "create", "a", content="---\nname: foo\n")
        r = sync_skills(
            self.store, self.skills_dir, {"foo"}, write=True, curator_states={"foo": "archived"}
        )
        self.assertEqual(r.exported, [])
        self.assertEqual(r.imported, [])
        self.assertEqual(self.store.state("foo"), "archived")


class TestDiffSkills(unittest.TestCase):
    def _d(self, **kw):
        base = dict(head_content="body", has_terminals=False,
                    profile_content="body", in_agent_created=True,
                    curator_state="active", old_state="active")
        base.update(kw)
        return diff_skills(**base)

    def test_no_drift(self):
        self.assertEqual(self._d(), (NOOP, False))

    def test_import_unseen_agent_skill(self):
        self.assertEqual(self._d(head_content=None), (IMPORT, False))

    def test_ignore_non_agent_skill(self):
        self.assertEqual(self._d(head_content=None, in_agent_created=False), (NOOP, False))

    def test_heal_bridge_missed_edit(self):
        self.assertEqual(self._d(head_content="old", profile_content="new"), (EDIT, False))

    def test_drop_decommissioned_present(self):
        self.assertEqual(self._d(head_content=None, has_terminals=True), (DROP, False))

    def test_decommissioned_absent_is_noop(self):
        self.assertEqual(self._d(head_content=None, has_terminals=True,
                                 profile_content=None), (NOOP, False))

    def test_export_store_only(self):
        self.assertEqual(self._d(profile_content=None), (EXPORT, False))

    def test_unresolved_contentless_head(self):
        self.assertEqual(self._d(head_content="", profile_content="live"), (UNRESOLVED, False))

    def test_archived_not_exported(self):
        self.assertEqual(self._d(profile_content=None, curator_state="archived"),
                         (NOOP, True))

    def test_state_change_reported(self):
        self.assertEqual(self._d(curator_state="stale"), (NOOP, True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
