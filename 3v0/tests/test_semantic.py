"""Deterministic tests for the semantic retrieval tier (core/semantic.py).

No network: a stub embed_fn hashes words into a fixed-dim vector and aliases
synonyms (sea->ocean...) so we can simulate "semantic closeness" cleanly and
prove the hybrid merge lifts a high-cosine fact even when lexical overlap is 0.
"""
import hashlib
import re
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import memdb, retrieval, backoff, semantic  # noqa: E402

ALIASES = {"sea": "ocean", "dawn": "sunrise", "purchase": "buy", "near": "next_to",
           "turns": "flips", "gently": "softly"}


def fake_embed(texts):
    out = []
    for t in texts:
        v = [0.0] * 32
        for w in re.findall(r"[a-z0-9]+", t.lower()):
            w = ALIASES.get(w, w)
            k = int(hashlib.md5(w.encode()).hexdigest()[:8], 16) % 32
            v[k] += 1.0
        out.append(v)
    return out


class SemanticStoreTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(f"{self._tmp.name}/m.db")
        self.calls = {"n": 0}
        self.store = semantic.SemanticStore(self.conn,
                                            embed_fn=lambda ts: (
                                                self.calls.__setitem__("n", self.calls["n"] + 1)
                                                or fake_embed(ts)))

    def test_store_caches_and_dedupes(self):
        f1 = memdb.add_fact(self.conn, "a", "b", "o", domain="benchmark", content="warm sea")
        f2 = memdb.add_fact(self.conn, "c", "d", "p", domain="benchmark", content="cool night")
        facts = [dict(r) for r in self.conn.execute(
            "SELECT * FROM facts WHERE id IN (?,?)", (f1, f2))]
        self.store.ensure(facts)
        vecs = self.store.vectors()
        self.assertEqual(len(vecs), 2)
        first = self.calls["n"]
        self.store.ensure(facts)          # all cached -> no new embed call
        self.assertEqual(self.calls["n"], first)


class SemanticRankerTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(f"{self._tmp.name}/m.db")

    def _seed(self):
        memdb.add_fact(self.conn, "scene", "x", "y", domain="benchmark",
                       content="sunrise over the ocean horizon MEM1")
        memdb.add_fact(self.conn, "scene", "x", "y", domain="benchmark",
                       content="market buys fresh produce daily MEM2")
        memdb.add_fact(self.conn, "scene", "x", "y", domain="benchmark",
                       content="router forwards packets all day MEM3")

    def test_hybrid_lifts_alias_target(self):
        self._seed()
        store = semantic.SemanticStore(self.conn, embed_fn=fake_embed)
        ranker = semantic.SemanticRanker(store)
        facts = [dict(r) for r in self.conn.execute(
            "SELECT * FROM facts WHERE domain='benchmark'")]
        # lexically disjoint from the target (dawn/near/the/sea)
        ranked = ranker.rerank(facts, "dawn near the sea")
        self.assertIn("MEM1", ranked[0]["content"])  # alias sea->ocean raises it

    def test_gate_token_sharing_competitor_not_outranked(self):
        """Regression: the old alpha-weight blend gave a +0.4 lexical bonus to
        any competitor sharing a token, swamping a zero-overlap paraphrase
        target's high cosine (0.19 vs 0.81 pure). The gate must rate the
        high-cosine target first despite a token-sharing rival."""
        conn = self.conn
        memdb.add_fact(conn, "scene", "x", "y", domain="benchmark",
                       content="the keeper turns the page gently MEMT")
        memdb.add_fact(conn, "scene", "x", "y", domain="benchmark",
                       content="cash registers page loudly MEMC")
        store = semantic.SemanticStore(conn, embed_fn=fake_embed)
        ranker = semantic.SemanticRanker(store)
        facts = [dict(r) for r in conn.execute(
            "SELECT * FROM facts WHERE domain='benchmark'")]
        ranked = ranker.rerank(facts, "flips the page softly")
        self.assertIn("MEMT", ranked[0]["content"])

    def test_gate_typo_keeps_corrected_query_on_top(self):
        """The fuzzy tier rewrites foverr->fiverr upstream; inject therefore
        embeds+lex-scores the CORRECTED terms. A misspelled keyword must keep
        the true fact topped despite the raw query sharing no cosine signal."""
        conn = self.conn
        memdb.add_fact(conn, "gig", "pricing", "list", domain="benchmark",
                       content="fiverr gig pricing MEMF")
        memdb.add_fact(conn, "service", "list", "x", domain="benchmark",
                       content="fiverr service MEMS")
        memdb.add_fact(conn, "delivery", "sys", "x", domain="benchmark",
                       content="delivery gig MEMD")
        store = semantic.SemanticStore(conn, embed_fn=fake_embed)
        ranker = semantic.SemanticRanker(store)
        facts = [dict(r) for r in conn.execute(
            "SELECT * FROM facts WHERE domain='benchmark'")]
        # 'foverr gig' corrected upstream to 'fiverr gig'
        ranked = ranker.rerank(facts, "fiverr gig", lex_terms=["fiverr", "gig"])
        self.assertIn("MEMF", ranked[0]["content"])

    def test_inject_semantic_surfaces_target(self):
        self._seed()
        store = semantic.SemanticStore(self.conn, embed_fn=fake_embed)
        ranker = semantic.SemanticRanker(store)
        inj = retrieval.inject(self.conn, domains=("benchmark",),
                               query_terms=["dawn", "sea+purchase"],
                               budget_chars=2000, touch=False, semantic=ranker,
                               query="dawn near the sea")
        self.assertIn("MEM1", inj.facts[0]["content"])

    def test_inject_fail_open_on_poison(self):
        self._seed()

        class Poison:
            def rerank(self, facts, query):
                raise backoff.ProviderError(0, "boom", retryable=True)

        inj = retrieval.inject(self.conn, domains=("benchmark",),
                               query_terms=["router", "packets"],
                               budget_chars=2000, touch=False, semantic=Poison())
        # lexical path still works; no exception
        self.assertTrue(inj.facts)


if __name__ == "__main__":
    unittest.main()