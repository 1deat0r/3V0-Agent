"""Tests for the native skill store + skill bridge (3V0 skill-lineage axis).

Run directly:
  python3 3v0/tests/test_skills.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skill_bridge import apply_skill_op  # noqa: E402
from core.skills import ABSORBED, RETRACTED, SkillStore  # noqa: E402


def _store() -> tuple[SkillStore, str]:
    path = os.path.join(tempfile.mkdtemp(), "skills.json")
    return SkillStore(path), path


class TestSkillStore(unittest.TestCase):
    def test_add_starts_lineage(self) -> None:
        s, _ = _store()
        v = s.add("foo", "create", "assistant_tool", content="---\nname: foo\n")
        self.assertTrue(v.active)
        self.assertEqual(v.supersedes, [])
        self.assertEqual(s.active_names(), {"foo"})

    def test_patch_supersedes_previous(self) -> None:
        s, _ = _store()
        v1 = s.add("foo", "create", "assistant_tool", content="v1")
        v2 = s.add("foo", "patch", "background_review", note="patch 'a' -> 'b'")
        self.assertFalse(v1.active)
        self.assertEqual(v1.superseded_by, v2.id)
        self.assertEqual(v2.supersedes, [v1.id])
        self.assertEqual(s.latest_active("foo"), v2)

    def test_history_returns_full_lineage(self) -> None:
        s, _ = _store()
        v1 = s.add("foo", "create", "a", content="v1")
        v2 = s.add("foo", "edit", "b", content="v2")
        v3 = s.add("foo", "edit", "c", content="v3")
        hist = s.history("foo")
        self.assertEqual([x.id for x in hist], [v1.id, v2.id, v3.id])

    def test_retract_is_terminal_and_recoverable(self) -> None:
        s, _ = _store()
        v = s.add("foo", "create", "a", content="x")
        r = s.retract("foo", source="background_review")
        self.assertEqual(r, v)
        self.assertFalse(v.active)
        self.assertEqual(v.superseded_by, RETRACTED)
        self.assertEqual(s.active_names(), set())
        self.assertIsNone(s.latest_active("foo"))
        # still recoverable via history (audit trail preserved)
        self.assertEqual([x.id for x in s.history("foo")], [v.id])

    def test_absorb_records_umbrella(self) -> None:
        s, _ = _store()
        v = s.add("old-skill", "create", "a", content="x")
        r = s.absorb("old-skill", "umbrella", source="curator")
        self.assertEqual(r, v)
        self.assertEqual(v.superseded_by, ABSORBED)
        self.assertEqual(v.absorbed_into, "umbrella")
        self.assertIsNone(s.latest_active("old-skill"))
        self.assertEqual(s.absorbed_by("umbrella"), ["old-skill"])

    def test_recreate_after_retract_starts_fresh_chain(self) -> None:
        s, _ = _store()
        v1 = s.add("foo", "create", "a", content="v1")
        s.retract("foo")
        v2 = s.add("foo", "create", "b", content="v2")
        # new chain has no supersession link back to the retracted version
        self.assertEqual(v2.supersedes, [])
        self.assertTrue(v2.active)
        self.assertFalse(v1.active)
        # but history still surfaces both chains
        self.assertEqual({x.id for x in s.history("foo")}, {v1.id, v2.id})

    def test_retract_missing_returns_none(self) -> None:
        s, _ = _store()
        self.assertIsNone(s.retract("nope"))
        self.assertIsNone(s.absorb("nope", "x"))

    def test_add_rejects_terminal_action(self) -> None:
        s, _ = _store()
        with self.assertRaises(ValueError):
            s.add("foo", "delete", "a")

    def test_add_rejects_unknown_action(self) -> None:
        s, _ = _store()
        with self.assertRaises(ValueError):
            s.add("foo", "frobnicate", "a")

    def test_active_excludes_absorbed(self) -> None:
        s, _ = _store()
        s.add("keep", "create", "a", content="k")
        s.add("gone", "create", "a", content="g")
        s.absorb("gone", "keep")
        self.assertEqual(s.active_names(), {"keep"})

    def test_persists_and_mutate_reloads(self) -> None:
        s1, path = _store()
        s1.add("foo", "create", "a", content="v1")
        s2 = SkillStore(path)  # constructed; holds v1
        s1.add("foo", "edit", "b", content="v2")
        # s2 is stale until mutate() re-reads under the lock
        self.assertEqual(s2.latest_active("foo").content, "v1")
        with s2.mutate():
            self.assertEqual(s2.latest_active("foo").content, "v2")


class TestSkillBridge(unittest.TestCase):
    def test_create(self) -> None:
        s, _ = _store()
        n = apply_skill_op(s, {"action": "create", "name": "foo", "content": "---\nname: foo\n"}, "assistant_tool")
        self.assertEqual(n, 1)
        v = s.latest_active("foo")
        self.assertEqual(v.action, "create")
        self.assertEqual(v.source, "assistant_tool")
        self.assertIn("name: foo", v.content)

    def test_create_idempotent(self) -> None:
        s, _ = _store()
        apply_skill_op(s, {"action": "create", "name": "foo", "content": "c"}, "a")
        n = apply_skill_op(s, {"action": "create", "name": "foo", "content": "c"}, "b")
        self.assertEqual(n, 0)
        self.assertEqual(len(s.versions("foo")), 1)

    def test_patch_records_note_not_content(self) -> None:
        s, _ = _store()
        apply_skill_op(s, {"action": "create", "name": "foo", "content": "v1"}, "a")
        n = apply_skill_op(
            s, {"action": "patch", "name": "foo", "old_string": "old", "new_string": "new"}, "background_review"
        )
        self.assertEqual(n, 1)
        v = s.latest_active("foo")
        self.assertEqual(v.action, "patch")
        self.assertEqual(v.content, "")
        self.assertIn("old", v.note)
        self.assertIn("new", v.note)

    def test_patch_carries_resolved_content_when_supplied(self) -> None:
        s, _ = _store()
        apply_skill_op(s, {"action": "create", "name": "foo", "content": "v1"}, "a")
        n = apply_skill_op(
            s,
            {"action": "patch", "name": "foo", "old_string": "old", "new_string": "new", "content": "v1-patched"},
            "background_review",
        )
        self.assertEqual(n, 1)
        v = s.latest_active("foo")
        self.assertEqual(v.action, "patch")
        self.assertEqual(v.content, "v1-patched")

    def test_edit_records_full_content(self) -> None:
        s, _ = _store()
        apply_skill_op(s, {"action": "create", "name": "foo", "content": "v1"}, "a")
        apply_skill_op(s, {"action": "edit", "name": "foo", "content": "v2"}, "b")
        self.assertEqual(s.latest_active("foo").content, "v2")

    def test_write_file_records_content_and_path(self) -> None:
        s, _ = _store()
        apply_skill_op(s, {"action": "create", "name": "foo", "content": "c"}, "a")
        n = apply_skill_op(
            s, {"action": "write_file", "name": "foo", "file_path": "scripts/x.py", "file_content": "print(1)"}, "a"
        )
        self.assertEqual(n, 1)
        v = s.latest_active("foo")
        self.assertEqual(v.file_path, "scripts/x.py")
        self.assertEqual(v.content, "print(1)")

    def test_remove_file_records_path(self) -> None:
        s, _ = _store()
        apply_skill_op(s, {"action": "create", "name": "foo", "content": "c"}, "a")
        apply_skill_op(s, {"action": "remove_file", "name": "foo", "file_path": "scripts/x.py"}, "a")
        v = s.latest_active("foo")
        self.assertEqual(v.action, "remove_file")
        self.assertIn("scripts/x.py", v.note)

    def test_delete_without_target_retracts(self) -> None:
        s, _ = _store()
        v = s.add("foo", "create", "a", content="c")
        n = apply_skill_op(s, {"action": "delete", "name": "foo"}, "background_review")
        self.assertEqual(n, 1)
        self.assertEqual(v.superseded_by, RETRACTED)

    def test_delete_with_absorbed_into_absorbs(self) -> None:
        s, _ = _store()
        v = s.add("foo", "create", "a", content="c")
        n = apply_skill_op(s, {"action": "delete", "name": "foo", "absorbed_into": "bar"}, "curator")
        self.assertEqual(n, 1)
        self.assertEqual(v.superseded_by, ABSORBED)
        self.assertEqual(v.absorbed_into, "bar")
        self.assertEqual(s.absorbed_by("bar"), ["foo"])

    def test_missing_name_or_bad_action_skipped(self) -> None:
        s, _ = _store()
        self.assertEqual(apply_skill_op(s, {"action": "create"}, "a"), 0)
        self.assertEqual(apply_skill_op(s, {"action": "nope", "name": "foo"}, "a"), 0)
        self.assertEqual(apply_skill_op(s, "not a dict", "a"), 0)
        self.assertEqual(s.skills, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
