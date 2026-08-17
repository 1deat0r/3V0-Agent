"""Tests for 3V0 store<->profile sync (stdlib only, no network).

Run directly:
  python3 3v0/tests/test_sync.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.memory import MemoryStore  # noqa: E402
from core.profile_io import join_entries, split_entries  # noqa: E402
from core.sync import diff_kind, profile_text, sync_kind  # noqa: E402


class TestSync(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "mem.json")
        self.store = MemoryStore(self.path)

    def test_no_drift_reports_clean(self) -> None:
        self.store.add("fact a", "memory", "test")
        r = sync_kind(self.store, join_entries(["fact a"]), "memory", write=False)
        self.assertTrue(r.clean)
        self.assertEqual(r.imported, [])
        self.assertEqual(r.dropped, [])
        self.assertEqual(r.exported, [])

    def test_imports_profile_only_entry(self) -> None:
        self.store.add("fact a", "memory", "test")
        md = join_entries(["fact a", "brand new from profile"])
        r = sync_kind(self.store, md, "memory", write=True)
        self.assertIn("brand new from profile", r.imported)
        active = {f.content for f in self.store.active("memory")}
        self.assertIn("brand new from profile", active)

    def test_drops_superseded_entry(self) -> None:
        old = self.store.add("gh = mustbearnold", "memory", "test")
        self.store.add("gh = 1deat0r", "memory", "test", supersedes=[old.id])
        md = join_entries(["gh = mustbearnold"])  # stale profile
        r = sync_kind(self.store, md, "memory", write=False)
        self.assertIn("gh = mustbearnold", r.dropped)
        self.assertEqual(r.imported, [])
        self.assertEqual(profile_text(self.store, "memory"), join_entries(["gh = 1deat0r"]))

    def test_exports_store_only_fact(self) -> None:
        self.store.add("store only fact", "memory", "test")
        md = join_entries(["profile only fact"])
        r = sync_kind(self.store, md, "memory", write=True)
        self.assertIn("store only fact", r.exported)
        self.assertIn("profile only fact", r.imported)
        self.assertEqual(
            split_entries(profile_text(self.store, "memory")),
            ["store only fact", "profile only fact"],
        )


class TestDiffKind(unittest.TestCase):
    def test_classifies_import_drop_export(self):
        imported, dropped, exported = diff_kind(
            profile_entries=["a", "b", "c"],
            active_contents=["a"],
            inactive_contents=["b"],
            view_contents=["a", "d"],
        )
        self.assertEqual(imported, ["c"])     # in profile, not in store
        self.assertEqual(dropped, ["b"])      # in profile, superseded in store
        self.assertEqual(exported, ["d"])     # in store view, not in profile


if __name__ == "__main__":
    unittest.main(verbosity=2)
