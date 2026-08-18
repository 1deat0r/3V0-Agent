"""Deterministic tests for the FTS5/BM25 retrieval upgrade (stone 1).

Test-surface rule (ADR-0004): drive core.retrieval.inject through a temp store
and assert the working set — never the scoring internals.
"""
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import memdb, retrieval, retrieval_fts


class FTSRetrievalTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(str(Path(self._tmp.name) / "mem.db"))
        # fact A: matches query terms as real words
        self.id_a = memdb.add_fact(self.conn, "3v0", "note", "alpha service",
                                   content="deploy the alpha service with beta config",
                                   now=1000.0, persist=True)
        # fact B: newer, but does NOT match the query terms
        self.id_b = memdb.add_fact(self.conn, "3v0", "note", "grocery run",
                                   content="milk eggs bread list",
                                   now=2000.0, persist=True)

    def tearDown(self):
        self.conn.close()
        self._tmp.cleanup()

    A_CONTENT = "deploy the alpha service with beta config"
    B_CONTENT = "milk eggs bread list"
    A_LEN = len(A_CONTENT)      # the rendered fact line is the CONTENT, not the object
    B_LEN = len(B_CONTENT)

    def test_query_aware_budget_spends_on_relevant(self):
        # Budget fits ONLY fact A's content line. Query-aware scheduling puts
        # the matching fact first, so A fills the budget and B (no match) is cut.
        inj = retrieval.inject(self.conn, domains=("3v0",),
                               query_terms=["alpha", "beta"],
                               budget_chars=self.A_LEN, touch=False, now=3000.0)
        self.assertEqual(inj.ids, [self.id_a], "non-matching fact must not steal the budget")
        self.assertNotIn(self.id_b, inj.ids)
        self.assertIn("alpha", inj.text)
        self.assertTrue(inj.truncated, "B left out under a tight budget")

    def test_query_schedules_matching_first_when_both_fit(self):
        inj = retrieval.inject(self.conn, domains=("3v0",),
                               query_terms=["alpha"],
                               budget_chars=self.A_LEN + self.B_LEN + 1,
                               touch=False, now=3000.0)
        self.assertEqual(inj.ids, [self.id_a, self.id_b])
        self.assertLess(inj.text.index("alpha"), inj.text.index("milk"))

    def test_no_query_schedules_by_recency(self):
        inj = retrieval.inject(self.conn, domains=("3v0",),
                               budget_chars=2000, touch=False, now=3000.0)
        # no query terms -> plain ordered rank; B is newer -> first
        self.assertEqual(inj.ids[0], self.id_b)

    def test_term_matching_nothing_is_safe(self):
        inj = retrieval.inject(self.conn, domains=("3v0",),
                               query_terms=["zzznomatch"], budget_chars=2000,
                               touch=False, now=3000.0)
        # no FTS candidate -> falls back to score ordering without crashing
        self.assertEqual(set(inj.ids), {self.id_a, self.id_b})


class FTSCacheTest(unittest.TestCase):
    def test_index_cache_reused_and_rebuilt(self):
        with tempfile.TemporaryDirectory() as d:
            conn = memdb.connect(str(Path(d) / "mem.db"))
            memdb.add_fact(conn, "3v0", "note", "hello",
                           content="hello world", now=1000.0, persist=True)
            facts = memdb.valid_facts(conn)
            self.assertTrue(retrieval_fts.ensure_index(conn, facts), "first build is fresh")
            self.assertFalse(retrieval_fts.ensure_index(conn, memdb.valid_facts(conn)),
                             "same facts -> cached, no rebuild")
            memdb.add_fact(conn, "3v0", "note", "bye", content="bye now",
                           now=2000.0, persist=True)
            self.assertTrue(retrieval_fts.ensure_index(conn, memdb.valid_facts(conn)),
                            "facts changed -> rebuild")
            conn.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
