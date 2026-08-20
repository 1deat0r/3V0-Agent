"""Tests for 3V0's provenance-tracked correction path (stdlib only).

Run directly:
  python3 3v0/tests/test_record.py
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
from core.record import RecordError, record  # noqa: E402


class TestRecord(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "mem.json")
        self.store = MemoryStore(self.path)

    def test_plain_record(self) -> None:
        r = record(self.store, "new fact", "memory", "test")
        self.assertEqual(r.superseded_ids, [])
        self.assertIn("new fact", {f.content for f in self.store.active("memory")})

    def test_supersede_by_id_recovers_chain(self) -> None:
        old = self.store.add("gh = mustbearnold", "memory", "test")
        r = record(self.store, "gh = 1deat0r", "memory", "test", supersede_id=old.id)
        self.assertEqual(r.superseded_ids, [old.id])
        self.assertFalse(old.active)
        self.assertEqual(
            [f.content for f in r.chain],
            ["gh = mustbearnold", "gh = 1deat0r"],
        )

    def test_supersede_by_substring(self) -> None:
        old = self.store.add("runtime is ~11 commits behind", "memory", "test")
        r = record(
            self.store,
            "runtime is now current",
            "memory",
            "test",
            supersede_contains="11 commits behind",
        )
        self.assertEqual(r.superseded_ids, [old.id])
        self.assertFalse(old.active)

    def test_ambiguous_substring_refused(self) -> None:
        self.store.add("fact about apples", "memory", "test")
        self.store.add("fact about applesauce", "memory", "test")
        with self.assertRaises(RecordError):
            record(self.store, "x", "memory", "test", supersede_contains="apple")

    def test_missing_id_refused(self) -> None:
        with self.assertRaises(RecordError):
            record(self.store, "x", "memory", "test", supersede_id="doesnotexist")

    def test_rejects_profile_separator_in_content(self) -> None:
        # '§' cannot round-trip through the 3V0 profile's wire format,
        # so the record path refuses it before it enters the store.
        with self.assertRaises(RecordError):
            record(self.store, "bad § fact", "memory", "test")

    def test_dry_run_does_not_persist(self) -> None:
        record(self.store, "not persisted", "memory", "test", persist=False)
        s2 = MemoryStore(self.path)  # reload from disk
        self.assertNotIn("not persisted", {f.content for f in s2.active("memory")})


if __name__ == "__main__":
    unittest.main(verbosity=2)
