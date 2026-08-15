"""Tests for 3V0's read-only store query layer (stdlib only, no network).

Run directly:
  python3 3v0/tests/test_query.py
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
from core.query import (  # noqa: E402
    fact_history,
    facts,
    skill_history,
    skills,
    summary,
)
from core.skills import STATE_STALE, SkillStore  # noqa: E402


class TestQuery(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.mem = MemoryStore(os.path.join(self.dir, "mem.json"))
        self.skl = SkillStore(os.path.join(self.dir, "skills.json"))

    def test_facts_and_summary(self) -> None:
        self.mem.add("one", "memory", "test")
        self.mem.add("two", "memory", "test")
        self.mem.add("who", "user", "test")
        fs = facts(self.mem, "memory")
        self.assertEqual({f["content"] for f in fs}, {"one", "two"})
        s = summary(self.mem, self.skl)
        self.assertEqual(s["facts"], {"memory": 2, "user": 1})
        self.assertEqual(s["fact_versions"], 3)

    def test_fact_history_recovers_supersession(self) -> None:
        old = self.mem.add("gh is mustbearnold", "memory", "test")
        new = self.mem.add("gh is 1deat0r", "memory", "test", supersedes=[old.id])
        chain = fact_history(self.mem, new.id)
        self.assertEqual(
            [f["content"] for f in chain],
            ["gh is mustbearnold", "gh is 1deat0r"],
        )
        self.assertFalse(chain[0]["active"])
        self.assertTrue(chain[1]["active"])

    def test_fact_history_unknown_id_is_empty(self) -> None:
        self.assertEqual(fact_history(self.mem, "nope"), [])

    def test_skills_list_is_metadata_only_and_carries_state(self) -> None:
        self.skl.add("alpha", "create", "test", content="frontmatter...")
        self.skl.set_state("alpha", STATE_STALE, source="test")
        out = skills(self.skl, None)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["name"], "alpha")
        self.assertEqual(out[0]["state"], STATE_STALE)
        self.assertNotIn("content", out[0])  # list view is metadata-only
        self.assertEqual(out[0]["content_len"], len("frontmatter..."))

    def test_skill_history_includes_bounded_content(self) -> None:
        body = "x" * 5000
        self.skl.add("big", "create", "test", content=body)
        hist = skill_history(self.skl, "big")
        self.assertEqual(len(hist), 1)
        self.assertTrue(hist[0]["truncated"])
        self.assertEqual(hist[0]["content_len"], 5000)
        self.assertLess(len(hist[0]["content"]), 5000)

    def test_skill_history_short_content_not_truncated(self) -> None:
        self.skl.add("small", "create", "test", content="hello")
        hist = skill_history(self.skl, "small")
        self.assertFalse(hist[0]["truncated"])
        self.assertEqual(hist[0]["content"], "hello")


if __name__ == "__main__":
    unittest.main(verbosity=2)
