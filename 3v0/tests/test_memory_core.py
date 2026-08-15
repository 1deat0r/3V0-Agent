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
from core.profile_io import join_entries, split_entries  # noqa: E402


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

    def test_profile_derived_view_roundtrip(self) -> None:
        """seed→export contract: the §-joined derived view splits back exactly.

        Locks the "profile is a derived view" claim made by
        seed_from_profile.py / export_to_profile.py: active facts, joined on
        '§', must re-split into the identical ordered list. Known boundary:
        facts containing a literal '§' or leading/trailing whitespace do not
        survive the delimiter — that is the separator's contract, and the
        record path now refuses '§' before it reaches the store.
        """
        s = MemoryStore(self.path)
        contents = [
            "fact one",
            "fact with (parens) and commas, fine",
            "multi\nline\nfact",
        ]
        for c in contents:
            s.add(c, "memory", "test")
        mem = join_entries([f.content for f in s.active("memory")])
        self.assertEqual(split_entries(mem), contents)

    def test_join_refuses_separator_in_content(self) -> None:
        """The wire-format owner refuses to emit an un-parseable profile."""
        with self.assertRaises(ValueError):
            join_entries(["fine", "contains § separator"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
