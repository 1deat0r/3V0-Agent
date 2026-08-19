"""Deterministic tests for retrieval stone 2 — fuzzy/typo-tolerant expansion."""
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import memdb, retrieval, retrieval_fuzzy  # noqa: E402


class FuzzyUnitTest(unittest.TestCase):
    def test_expand_term_corrects_typo(self):
        got = retrieval_fuzzy.expand_term("foverr", {"fiverr", "gig", "seller"})
        self.assertEqual(got, "fiverr")

    def test_expand_term_corrects_transposition(self):
        got = retrieval_fuzzy.expand_term("ifverr", {"fiverr", "gig", "seller"})
        self.assertEqual(got, "fiverr")

    def test_expand_term_clean_is_none(self):
        self.assertIsNone(retrieval_fuzzy.expand_term("fiverr", {"fiverr", "gig"}))

    def test_expand_term_no_near_word_is_none(self):
        self.assertIsNone(retrieval_fuzzy.expand_term("zzzzzz", {"fiverr", "gig"}))

    def test_expand_query_only_typos(self):
        out = retrieval_fuzzy.expand_query(
            ["foverr", "seller", "gig"],
            {"fiverr", "seller", "gig"})
        self.assertEqual(out, ["fiverr", "seller", "gig"])

    def test_expand_query_identity_when_clean(self):
        out = retrieval_fuzzy.expand_query(["seller", "gig"], {"fiverr", "seller", "gig"})
        self.assertEqual(out, ["seller", "gig"])

    def test_within_ed1_cases(self):
        f = retrieval_fuzzy._within_ed1
        self.assertTrue(f("fiverr", "fiverr"))
        self.assertTrue(f("seller", "seeller"))   # insertion
        self.assertTrue(f("abc", "ab"))           # deletion
        self.assertTrue(f("teh", "the"))          # transposition
        self.assertFalse(f("fiverr", "fenerrb"))  # >1 edits
        self.assertFalse(f("abcde", "vwxyz"))     # 5 substitutions


class FuzzyInjectTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(f"{self._tmp.name}/m.db")
        # one target fact + distractors that share a term but not the typo'd one
        self.target = "3V0 sells digital gigs on Fiverr MEM7001"
        memdb.add_fact(self.conn, "fiverr", "platform", "seller",
                       domain="benchmark", content=self.target)
        memdb.add_fact(self.conn, "analytics", "tool", "metric",
                       domain="benchmark", content="3V0 runs local analytics for metrics MEM7002")
        memdb.add_fact(self.conn, "review", "daemon", "store",
                       domain="benchmark", content="3V0 review daemon writes to the store MEM7003")
        memdb.add_fact(self.conn, "gateway", "service", "systemd",
                       domain="benchmark", content="3V0 gateway is a systemd unit MEM7004")

    def test_typo_query_retrieves_true_fact(self):
        # single typo'd term ONLY, so the hit must come from fuzzy correction,
        # not a second clean co-term.
        inj = retrieval.inject(self.conn, domains=("benchmark",),
                               query_terms=["foverr"],
                               budget_chars=500, touch=False)
        self.assertTrue(inj.facts)
        top = inj.facts[0]
        self.assertIn("fiverr", top["content"].lower())

    def test_clean_query_unaffected(self):
        inj = retrieval.inject(self.conn, domains=("benchmark",),
                               query_terms=["gateway", "systemd"],
                               budget_chars=500, touch=False)
        self.assertIn("gateway", inj.facts[0]["content"].lower())


if __name__ == "__main__":
    unittest.main()