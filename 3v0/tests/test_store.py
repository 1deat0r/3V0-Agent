"""SQLStore facade parity — the rewire's canonical store behind the old interface.

The pipeline (record/bridge/sync/decide/review) speaks one store interface:
add/retract/active/matching/get/history/export/mutate with Fact-shaped
results. SQLStore must satisfy that contract over the memdb triple substrate,
so the rewire swaps the substrate without touching the callers' logic.

Run directly:
  python3 3v0/tests/test_store.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.memory import RETRACTED, MemoryStore  # noqa: E402
from core.store import SQLStore, open_store  # noqa: E402


class SQLStoreTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "mem.db")
        self.store = SQLStore(self.path)
        self.addCleanup(
            lambda: self.store.conn.close() if self.store.conn is not None else None)


class TestAddAndActive(SQLStoreTest):
    def test_add_and_active_by_kind(self):
        self.store.add("fact one", "memory", "test")
        self.store.add("fact two", "user", "test")
        self.assertEqual({f.content for f in self.store.active()}, {"fact one", "fact two"})
        self.assertEqual([f.content for f in self.store.active("memory")], ["fact one"])
        self.assertEqual(self.store.active("memory")[0].kind, "memory")

    def test_invalid_kind_rejected(self):
        with self.assertRaises(ValueError):
            self.store.add("x", "bogus", "test")

    def test_persistence_roundtrip(self):
        self.store.add("persisted", "memory", "test")
        s2 = SQLStore(self.path)
        try:
            self.assertEqual([f.content for f in s2.active()], ["persisted"])
        finally:
            s2.conn.close()

    def test_dry_run_does_not_persist(self):
        self.store.add("not persisted", "memory", "test", persist=False)
        s2 = SQLStore(self.path)
        try:
            self.assertNotIn("not persisted", {f.content for f in s2.active("memory")})
        finally:
            s2.conn.close()


class TestSupersession(SQLStoreTest):
    def test_supersede_flags_never_destroys(self):
        old = self.store.add("gh account is mustbearnold", "memory", "test")
        new = self.store.add("gh account is 1deat0r", "memory", "test",
                             supersedes=[old.id])
        self.assertFalse(old.active)
        self.assertEqual(old.superseded_by, new.id)
        self.assertEqual([f.content for f in self.store.active("memory")],
                         ["gh account is 1deat0r"])
        chain = self.store.history(new.id)
        self.assertEqual([f.content for f in chain],
                         ["gh account is mustbearnold", "gh account is 1deat0r"])
        # temporal validity is the supersession mechanism
        row = self.store.conn.execute(
            "SELECT valid_to FROM facts WHERE id=?", (int(old.id),)).fetchone()
        self.assertIsNotNone(row["valid_to"])

    def test_matching_uses_content(self):
        self.store.add("fact about apples", "memory", "test")
        self.store.add("fact about applesauce", "memory", "test")
        hits = self.store.matching("memory", "apple")
        self.assertEqual(len(hits), 2)

    def test_unknown_supersede_target_is_ignored(self):
        f = self.store.add("solo", "memory", "test", supersedes=["999999"])
        self.assertEqual(f.supersedes, [])
        self.assertEqual([x.content for x in self.store.active("memory")], ["solo"])


class TestRetract(SQLStoreTest):
    def test_retract_marks_inactive_and_recovers(self):
        f = self.store.add("old fact", "memory", "test")
        r = self.store.retract(f.id, source="background_review")
        self.assertIsNotNone(r)
        self.assertFalse(f.active)
        self.assertEqual(f.superseded_by, RETRACTED)
        self.assertNotIn("old fact", {x.content for x in self.store.active("memory")})
        recovered = self.store.get(f.id)
        assert recovered is not None
        self.assertEqual(recovered.content, "old fact")
        self.assertEqual([x.content for x in self.store.history(f.id)], ["old fact"])
        self.assertIn("retracted by background_review", f.note)

    def test_retract_missing_or_inactive_returns_none(self):
        self.assertIsNone(self.store.retract("nope"))
        f = self.store.add("x", "memory", "test")
        self.store.retract(f.id)
        self.assertIsNone(self.store.retract(f.id))


class TestExportAndFacade(SQLStoreTest):
    def test_export_groups_by_kind(self):
        self.store.add("m1", "memory", "test")
        self.store.add("u1", "user", "test")
        self.store.add("d1", "directive", "test")
        out = self.store.export()
        self.assertEqual(out["memory"], ["m1"])
        self.assertEqual(out["user"], ["u1"])
        self.assertEqual(out["directive"], ["d1"])

    def test_facts_property_and_clear(self):
        self.store.add("a", "memory", "test")
        self.store.add("b", "memory", "test")
        self.assertEqual(len(self.store.facts), 2)
        self.store.clear()
        self.assertEqual(self.store.facts, [])

    def test_open_store_factory(self):
        db = open_store(os.path.join(self.dir, "s.db"))
        try:
            self.assertIsInstance(db, SQLStore)
        finally:
            if db.conn is not None:
                db.conn.close()
        js = open_store(os.path.join(self.dir, "s.json"))
        self.assertIsInstance(js, MemoryStore)

    def test_mutate_context_yields_store(self):
        with self.store.mutate() as s:
            self.assertIs(s, self.store)
            s.add("under mutate", "memory", "test")


if __name__ == "__main__":
    unittest.main()
