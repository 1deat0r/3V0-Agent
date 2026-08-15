"""Tests for 3V0's native memory core (stdlib only, no network).

Run directly:
  python3 3v0/tests/test_memory_core.py
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


class TestMemoryCore(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "mem.json")

    def test_add_and_active(self) -> None:
        s = MemoryStore(self.path)
        s.add("fact one", "memory", "test")
        s.add("fact two", "user", "test")
        self.assertEqual({f.content for f in s.active()}, {"fact one", "fact two"})
        self.assertEqual([f.content for f in s.active("memory")], ["fact one"])

    def test_supersede_flags_never_destroys(self) -> None:
        s = MemoryStore(self.path)
        old = s.add("gh account is mustbearnold", "memory", "test")
        new = s.add("gh account is 1deat0r", "memory", "test", supersedes=[old.id])
        self.assertFalse(old.active)
        self.assertEqual(old.superseded_by, new.id)
        self.assertEqual([f.content for f in s.active("memory")], ["gh account is 1deat0r"])
        # provenance chain recovers the full thread, oldest -> newest
        chain = s.history(new.id)
        self.assertEqual(
            [f.content for f in chain],
            ["gh account is mustbearnold", "gh account is 1deat0r"],
        )

    def test_persistence_roundtrip(self) -> None:
        s = MemoryStore(self.path)
        s.add("persisted", "memory", "test")
        s2 = MemoryStore(self.path)
        self.assertEqual([f.content for f in s2.active()], ["persisted"])

    def test_invalid_kind_rejected(self) -> None:
        s = MemoryStore(self.path)
        with self.assertRaises(ValueError):
            s.add("x", "bogus", "test")


if __name__ == "__main__":
    unittest.main(verbosity=2)
