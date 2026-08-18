"""The derived view is retrieval-chosen (ADR-0004) — exporter + sync tests.

With the rewire, MEMORY.md / USER.md stop being an export of *all* active
facts and become the budgeted working set ``retrieval.inject`` selects. This
locks the new contract at the seam: bounded view, feedback not inflated by
wake exports, and sync semantics that diff against the working set.

Run directly:
  python3 3v0/tests/test_export_injection.py
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

from core.project import project_memory  # noqa: E402
from core.profile_io import split_entries  # noqa: E402
from core.store import SQLStore  # noqa: E402
from core.sync import profile_text, sync_kind  # noqa: E402


class ExportInjectionTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.store = SQLStore(os.path.join(self.dir, "mem.db"))
        self.profile_dir = Path(self.dir) / "profile"
        self.addCleanup(self.store.close)

    def test_profile_text_is_working_set_not_export_all(self):
        for i in range(200):
            self.store.add(f"fact number {i:03d}", "memory", "test")
        text = profile_text(self.store, "memory")
        self.assertLessEqual(len(text), 2000)           # the budget holds
        self.assertLess(len(split_entries(text)), 200)  # not everything fits
        # the view splits back to exactly the chosen entries (wire roundtrip),
        # newest first
        self.assertEqual(split_entries(text)[0], "fact number 199")

    def test_kind_scoping_separates_memory_and_user(self):
        self.store.add("a memory fact", "memory", "test")
        self.store.add("a user fact", "user", "test")
        self.assertIn("a memory fact", profile_text(self.store, "memory"))
        self.assertNotIn("a user fact", profile_text(self.store, "memory"))
        self.assertIn("a user fact", profile_text(self.store, "user"))

    def test_project_memory_writes_working_sets(self):
        for i in range(10):
            self.store.add(f"m {i}", "memory", "test")
        self.store.add("u fact", "user", "test")
        written = project_memory(self.store, self.profile_dir)
        self.assertEqual(written, ["MEMORY.md", "USER.md"])
        mem = (self.profile_dir / "MEMORY.md").read_text()
        user = (self.profile_dir / "USER.md").read_text()
        self.assertIn("m 9", mem)
        self.assertEqual(split_entries(user), ["u fact"])
        self.assertLessEqual(len(mem), 2000)

    def test_export_does_not_inflate_feedback(self):
        # Wake exports are mechanical syncs, not real retrieval: exporting the
        # view must not touch access_count, or the view would reinforce itself
        # into permanence (rich-get-richer).
        self.store.add("f", "memory", "test")
        project_memory(self.store, self.profile_dir)
        total = self.store._conn.execute(
            "SELECT SUM(access_count) FROM facts").fetchone()[0]
        self.assertEqual(total, 0)

    def test_projection_stamps_last_projected(self):
        # Projection is a distinct, non-ranking usage signal (ADR-0005): the
        # export records which facts were projected, so forgetting can tell
        # "projected" from "never used" — without touching access_count.
        self.store.add("f", "memory", "test")
        project_memory(self.store, self.profile_dir)
        last_proj = self.store._conn.execute(
            "SELECT last_projected FROM facts").fetchone()[0]
        self.assertIsNotNone(last_proj)

    def test_sync_exported_is_working_set_not_in_profile(self):
        for i in range(200):
            self.store.add(f"sync fact {i:03d}", "memory", "test")
        md = "profile only entry"
        r = sync_kind(self.store, md, "memory", write=False)
        self.assertIn("profile only entry", r.imported)
        # exported = chosen working-set entries absent from the profile, not
        # every active fact (the old export-all contract is retired)
        self.assertLess(len(r.exported), 200)
        self.assertTrue(r.exported)
        view = split_entries(profile_text(self.store, "memory"))
        for e in r.exported:
            self.assertIn(e, view)


if __name__ == "__main__":
    unittest.main()
