"""Tests for the store-first bridge (3V0 memory-tool op -> store mapping).

Run directly:
  python3 3v0/tests/test_bridge.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.bridge import apply_ops  # noqa: E402
from core.memory import RETRACTED, MemoryStore  # noqa: E402


class TestRetract(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "mem.json")
        self.store = MemoryStore(self.path)

    def test_retract_marks_inactive_and_recovers(self) -> None:
        f = self.store.add("old fact", "memory", "test")
        r = self.store.retract(f.id, source="background_review")
        self.assertIsNotNone(r)
        self.assertFalse(f.active)
        self.assertEqual(f.superseded_by, RETRACTED)
        self.assertNotIn("old fact", {x.content for x in self.store.active("memory")})
        # still recoverable by id + history terminates at the retraction
        recovered = self.store.get(f.id)
        assert recovered is not None
        self.assertEqual(recovered.content, "old fact")
        self.assertEqual([x.content for x in self.store.history(f.id)], ["old fact"])
        self.assertIn("retracted by background_review", f.note)

    def test_retract_missing_or_inactive_returns_none(self) -> None:
        self.assertIsNone(self.store.retract("nope"))
        f = self.store.add("x", "memory", "test")
        self.store.retract(f.id)
        self.assertIsNone(self.store.retract(f.id))  # already inactive

    def test_retract_persists(self) -> None:
        f = self.store.add("gone", "memory", "test")
        self.store.retract(f.id, source="test")
        s2 = MemoryStore(self.path)
        self.assertNotIn("gone", {x.content for x in s2.active("memory")})


class TestBridge(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "mem.json")
        self.store = MemoryStore(self.path)

    def test_add(self) -> None:
        n = apply_ops(self.store, "memory", [{"action": "add", "content": "new fact"}], "background_review")
        self.assertEqual(n, 1)
        f = self.store.active("memory")[0]
        self.assertEqual(f.content, "new fact")
        self.assertEqual(f.source, "background_review")

    def test_add_idempotent(self) -> None:
        apply_ops(self.store, "memory", [{"action": "add", "content": "dup"}], "a")
        n = apply_ops(self.store, "memory", [{"action": "add", "content": "dup"}], "b")
        self.assertEqual(n, 0)
        self.assertEqual(len(self.store.active("memory")), 1)

    def test_replace_supersedes_exactly_one(self) -> None:
        old = self.store.add("gh = mustbearnold", "memory", "test")
        n = apply_ops(
            self.store, "memory",
            [{"action": "replace", "old_text": "mustbearnold", "content": "gh = 1deat0r"}],
            "background_review",
        )
        self.assertEqual(n, 1)
        self.assertFalse(old.active)
        self.assertEqual(old.superseded_by, self.store.active("memory")[0].id)
        self.assertEqual(
            [x.content for x in self.store.history(self.store.active("memory")[0].id)],
            ["gh = mustbearnold", "gh = 1deat0r"],
        )

    def test_replace_new_text_alias_supersedes(self) -> None:
        # The memory tool documents `new_text` as an alias for `content`; the
        # bridge must honor it so an aliased replace supersedes rather than
        # degrading to a duplicate at the wake sync.
        old = self.store.add("gh = mustbearnold", "memory", "test")
        n = apply_ops(
            self.store, "memory",
            [{"action": "replace", "old_text": "mustbearnold", "new_text": "gh = 1deat0r"}],
            "background_review",
        )
        self.assertEqual(n, 1)
        self.assertFalse(old.active)
        self.assertEqual(old.superseded_by, self.store.active("memory")[0].id)

    def test_add_new_text_alias(self) -> None:
        n = apply_ops(self.store, "memory", [{"action": "add", "new_text": "aliased"}], "a")
        self.assertEqual(n, 1)
        self.assertEqual(self.store.active("memory")[0].content, "aliased")

    def test_replace_without_match_plain_adds(self) -> None:
        self.store.add("existing", "memory", "test")
        n = apply_ops(
            self.store, "memory",
            [{"action": "replace", "old_text": "nonexistent", "content": "brand new"}],
            "background_review",
        )
        self.assertEqual(n, 1)
        active = {x.content for x in self.store.active("memory")}
        self.assertIn("existing", active)
        self.assertIn("brand new", active)

    def test_replace_ambiguous_skips_without_guessing(self) -> None:
        self.store.add("apples are red", "memory", "test")
        self.store.add("applesauce is wet", "memory", "test")
        n = apply_ops(
            self.store, "memory",
            [{"action": "replace", "old_text": "apple", "content": "replacement"}],
            "background_review",
        )
        self.assertEqual(n, 0)  # skipped, no guessed supersession
        self.assertEqual(len(self.store.active("memory")), 2)

    def test_remove_retracts(self) -> None:
        f = self.store.add("delete me", "memory", "test")
        n = apply_ops(self.store, "memory", [{"action": "remove", "old_text": "delete me"}], "background_review")
        self.assertEqual(n, 1)
        self.assertFalse(f.active)
        self.assertEqual(f.superseded_by, RETRACTED)

    def test_remove_ambiguous_skips(self) -> None:
        self.store.add("a one", "memory", "test")
        self.store.add("a two", "memory", "test")
        n = apply_ops(self.store, "memory", [{"action": "remove", "old_text": "a"}], "background_review")
        self.assertEqual(n, 0)
        self.assertEqual(len(self.store.active("memory")), 2)

    def test_batch_mixed(self) -> None:
        old = self.store.add("old", "memory", "test")
        n = apply_ops(
            self.store, "memory",
            [
                {"action": "add", "content": "added"},
                {"action": "replace", "old_text": "old", "content": "replaced"},
                {"action": "remove", "old_text": "added"},
            ],
            "background_review",
        )
        self.assertEqual(n, 3)
        active = {x.content for x in self.store.active("memory")}
        self.assertEqual(active, {"replaced"})
        self.assertFalse(old.active)

    def test_bad_target_refused(self) -> None:
        with self.assertRaises(ValueError):
            apply_ops(self.store, "identity", [{"action": "add", "content": "x"}], "a")

    def test_unknown_action_ignored(self) -> None:
        n = apply_ops(self.store, "memory", [{"action": "frobnicate", "content": "x"}], "a")
        self.assertEqual(n, 0)

    def test_separator_content_skipped_not_raised(self) -> None:
        # record() refuses '§'; the bridge must skip, not crash the batch.
        n = apply_ops(self.store, "memory", [{"action": "add", "content": "bad § fact"}], "a")
        self.assertEqual(n, 0)
        self.assertEqual(self.store.active("memory"), [])


class TestMutate(unittest.TestCase):
    def test_mutate_reloads_latest_under_lock(self) -> None:
        path = os.path.join(tempfile.mkdtemp(), "mem.json")
        s2 = MemoryStore(path)  # constructed while store is empty
        s1 = MemoryStore(path)
        s1.add("from s1", "memory", "test")  # writes to disk after s2 loaded
        # s2's in-memory facts are stale; mutate() re-reads under the lock
        self.assertNotIn("from s1", {f.content for f in s2.active("memory")})
        with s2.mutate():
            self.assertIn("from s1", {f.content for f in s2.active("memory")})


if __name__ == "__main__":
    unittest.main(verbosity=2)
