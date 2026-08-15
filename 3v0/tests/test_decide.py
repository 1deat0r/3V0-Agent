"""Tests for 3V0's store-first decision actuator (stdlib only, no network).

Run directly:
  python3 3v0/tests/test_decide.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.decide import decide  # noqa: E402
from core.memory import RETRACTED, MemoryStore  # noqa: E402


class TestDecide(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "mem.json")
        self.store = MemoryStore(self.path)

    def test_record_plain(self) -> None:
        r = decide(self.store, {"action": "record", "kind": "memory", "content": "new fact"})
        self.assertTrue(r["ok"])
        self.assertEqual(r["action"], "record")
        self.assertEqual(r["fact"]["content"], "new fact")
        self.assertEqual(r["superseded_ids"], [])
        self.assertIn("new fact", {f.content for f in self.store.active("memory")})

    def test_record_supersede_by_id_recovers_chain(self) -> None:
        old = self.store.add("gh = mustbearnold", "memory", "test")
        r = decide(
            self.store,
            {"action": "record", "kind": "memory", "content": "gh = 1deat0r", "fact_id": old.id},
        )
        self.assertEqual(r["superseded_ids"], [old.id])
        self.assertFalse(old.active)
        self.assertEqual(
            [f["content"] for f in r["chain"]],
            ["gh = mustbearnold", "gh = 1deat0r"],
        )

    def test_record_supersede_by_substring(self) -> None:
        old = self.store.add("runtime is ~11 commits behind", "memory", "test")
        r = decide(
            self.store,
            {
                "action": "record",
                "kind": "memory",
                "content": "runtime is current",
                "supersedes": "11 commits behind",
            },
        )
        self.assertEqual(r["superseded_ids"], [old.id])
        self.assertFalse(old.active)

    def test_record_bad_kind_refused(self) -> None:
        r = decide(self.store, {"action": "record", "kind": "nope", "content": "x"})
        self.assertIn("error", r)
        self.assertEqual(self.store.active("memory"), [])

    def test_record_missing_content_refused(self) -> None:
        r = decide(self.store, {"action": "record", "kind": "memory", "content": ""})
        self.assertIn("error", r)

    def test_record_separator_content_refused(self) -> None:
        r = decide(self.store, {"action": "record", "kind": "memory", "content": "bad § fact"})
        self.assertIn("error", r)

    def test_record_ambiguous_substring_refused(self) -> None:
        self.store.add("apples are red", "memory", "test")
        self.store.add("applesauce is wet", "memory", "test")
        r = decide(
            self.store,
            {"action": "record", "kind": "memory", "content": "x", "supersedes": "apple"},
        )
        self.assertIn("error", r)

    def test_retract(self) -> None:
        f = self.store.add("old fact", "memory", "test")
        r = decide(self.store, {"action": "retract", "fact_id": f.id})
        self.assertTrue(r["ok"])
        self.assertEqual(r["action"], "retract")
        self.assertFalse(f.active)
        self.assertEqual(f.superseded_by, RETRACTED)
        self.assertEqual([x["content"] for x in r["chain"]], ["old fact"])

    def test_retract_unknown_id_refused(self) -> None:
        r = decide(self.store, {"action": "retract", "fact_id": "nope"})
        self.assertIn("error", r)

    def test_retract_missing_id_refused(self) -> None:
        r = decide(self.store, {"action": "retract"})
        self.assertIn("error", r)

    def test_retract_inactive_refused(self) -> None:
        f = self.store.add("x", "memory", "test")
        self.store.retract(f.id)
        r = decide(self.store, {"action": "retract", "fact_id": f.id})
        self.assertIn("error", r)

    def test_unknown_action_refused(self) -> None:
        r = decide(self.store, {"action": "frobnicate"})
        self.assertIn("error", r)

    def test_dry_run_does_not_persist(self) -> None:
        decide(
            self.store,
            {"action": "record", "kind": "memory", "content": "no persist"},
            persist=False,
        )
        s2 = MemoryStore(self.path)
        self.assertNotIn("no persist", {f.content for f in s2.active("memory")})


if __name__ == "__main__":
    unittest.main(verbosity=2)
