from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.memdb import add_fact, connect  # noqa: E402
from core.retrieval import inject, rank, render  # noqa: E402

NOW = 1_800_000_000.0


class RetrievalTest(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        self.addCleanup(self.conn.close)


class TestRank(RetrievalTest):
    def test_keyword_match_scores_higher(self):
        facts = [
            {"subject": "a", "predicate": "p", "object": "deepseek api", "content": "", "created_at": NOW, "access_count": 0, "last_accessed": None},
            {"subject": "b", "predicate": "p", "object": "unrelated", "content": "", "created_at": NOW, "access_count": 0, "last_accessed": None},
        ]
        self.assertEqual(rank(facts, query_terms=["deepseek"], now=NOW)[0]["subject"], "a")

    def test_recency_scores_higher(self):
        facts = [
            {"subject": "old", "predicate": "p", "object": "x", "content": "", "created_at": NOW - 86400 * 30, "access_count": 0, "last_accessed": NOW - 86400 * 30},
            {"subject": "new", "predicate": "p", "object": "x", "content": "", "created_at": NOW, "access_count": 0, "last_accessed": NOW},
        ]
        self.assertEqual(rank(facts, now=NOW)[0]["subject"], "new")

    def test_frequency_scores_higher(self):
        facts = [
            {"subject": "rare", "predicate": "p", "object": "x", "content": "", "created_at": NOW, "access_count": 0, "last_accessed": None},
            {"subject": "hot", "predicate": "p", "object": "x", "content": "", "created_at": NOW, "access_count": 100, "last_accessed": NOW},
        ]
        self.assertEqual(rank(facts, now=NOW)[0]["subject"], "hot")


class TestRender(RetrievalTest):
    def test_render(self):
        facts = [{"subject": "3v0", "predicate": "model", "object": "deepseek-v4-pro", "content": "the LLM substrate"}]
        text = render(facts)
        self.assertIn("3v0 model deepseek-v4-pro", text)
        self.assertIn("the LLM substrate", text)


class TestInject(RetrievalTest):
    def test_caps_by_budget_and_reports_truncation(self):
        for content in ("aaaa", "bbbb", "cccc", "dddd", "eeee"):
            add_fact(self.conn, "s", "p", content, content=content, now=NOW)
        inj = inject(self.conn, budget_chars=11, touch=False, now=NOW)
        # two lines fit in 11 chars; ties rank newest-first (created_at DESC,
        # id DESC), so the two newest facts are chosen
        self.assertEqual(inj.text, "eeee\ndddd")
        self.assertTrue(inj.truncated)
        self.assertLessEqual(len(inj.text), 11)
        self.assertEqual(inj.ids, [f["id"] for f in inj.facts])

    def test_touch_writes_feedback_only_for_chosen(self):
        for content in ("aaaa", "bbbb", "cccc"):
            add_fact(self.conn, "s", "p", content, content=content, now=NOW)
        inj = inject(self.conn, budget_chars=11, touch=True, now=NOW)
        self.assertEqual(len(inj.ids), 2)
        total = self.conn.execute("SELECT SUM(access_count) FROM facts").fetchone()[0]
        self.assertEqual(total, 2)
        for fid in inj.ids:
            row = self.conn.execute(
                "SELECT last_accessed FROM facts WHERE id=?", (fid,)).fetchone()
            self.assertEqual(row["last_accessed"], NOW)

    def test_touch_false_is_pure_preview(self):
        add_fact(self.conn, "s", "p", "v", now=NOW)
        inject(self.conn, touch=False, now=NOW)
        total = self.conn.execute("SELECT SUM(access_count) FROM facts").fetchone()[0]
        self.assertEqual(total, 0)

    def test_domain_priority(self):
        add_fact(self.conn, "3v0", "repo", "3V0 Agent", domain="3v0", now=NOW)
        add_fact(self.conn, "axiom", "repo", "axiom-agent", domain="axiom", now=NOW)
        inj = inject(self.conn, domains=("axiom", "3v0"), touch=False, now=NOW)
        self.assertEqual([f["domain"] for f in inj.facts], ["axiom", "3v0"])

    def test_default_domain_is_3v0_only(self):
        add_fact(self.conn, "3v0", "repo", "3V0 Agent", domain="3v0", now=NOW)
        add_fact(self.conn, "env", "repo", "elsewhere", domain="env", now=NOW)
        inj = inject(self.conn, touch=False, now=NOW)
        self.assertEqual(len(inj.facts), 1)
        self.assertEqual(inj.facts[0]["domain"], "3v0")

    def test_oversized_fact_is_skipped_not_blocking(self):
        # A huge low-value line must not starve later small facts: budget fill
        # skips it and keeps going (whole-fact granularity).
        add_fact(self.conn, "huge", "p", "v", content="v" * 500, now=NOW - 10)
        add_fact(self.conn, "small", "p", "v", content="small content", now=NOW)
        inj = inject(self.conn, budget_chars=50, touch=False, now=NOW)
        self.assertEqual([f["subject"] for f in inj.facts], ["small"])
        self.assertTrue(inj.truncated)

    def test_empty_store(self):
        inj = inject(self.conn, touch=False, now=NOW)
        self.assertEqual(inj.facts, [])
        self.assertEqual(inj.text, "")
        self.assertFalse(inj.truncated)

    def test_amnesia(self):
        # A fact whose valid_to has passed must never be injected: forgetting
        # is the store's mechanism and injection follows it automatically.
        add_fact(self.conn, "old", "p", "v", valid_to=NOW - 1, now=NOW - 10)
        inj = inject(self.conn, touch=False, now=NOW)
        self.assertEqual(inj.facts, [])


if __name__ == "__main__":
    unittest.main()
