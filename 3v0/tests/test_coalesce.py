"""Deterministic tests for the watermark-driven consolidation (core/coalesce.py).

NOTE on the clock: facts are seeded with ``valid_from = now`` at runtime, and a
supersede close writes ``valid_to = now`` at reconcile time. Tests must therefore
evaluate with a *fresh* ``time.time()`` taken *after* seeding (a future or stale
clock leaves just-closed facts temporarily valid and makes reconciles no-op).

The invariant coalesce protects: a consolidation pass is *complete* (100%
coverage) when it reaches fixed point — every chain examined, zero pending
conflicts remaining — without ever closing a distinct note (the container-key
shape). Both halves are asserted here.
"""
import tempfile
import time
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import memdb, consolidate, coalesce  # noqa: E402


class CoalesceTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(f"{self._tmp.name}/m.db")
        self.wm = Path(self._tmp.name) / "wm.json"

    def _seed_container_notes(self):
        """The pipeline's real shape: N distinct notes, one container key."""
        for text in ("note about substrate pricing",
                     "note about fiverr gigs",
                     "note about gateway service",
                     "note about tui palette"):
            memdb.add_fact(self.conn, "3v0", "note", text, content=text)

    def _seed_broken_chain(self):
        a = memdb.add_fact(self.conn, "model", "substrate", "fireworks",
                           content="primary model runs on fireworks")
        b = memdb.add_fact(self.conn, "model", "substrate", "bitdeer",
                           content="primary model runs on bitdeer deepseek",
                           supersedes=a)
        self.conn.execute("UPDATE facts SET valid_to=NULL WHERE id=?", (a,))
        self.conn.commit()

    def test_watermark_roundtrip(self):
        coalesce.save_watermark(5000.0, self.wm)
        self.assertEqual(coalesce.load_watermark(self.wm), 5000.0)

    def test_not_due_within_interval(self):
        now = time.time()
        coalesce.save_watermark(now - 10, self.wm)
        rep = coalesce.run(self.conn, now=now, interval_s=3600, force=False,
                           watermark=self.wm)
        self.assertFalse(rep.fired)
        self.assertTrue(rep.reason.startswith("not due"))

    def test_force_fires_and_reconciles_chain_conflict(self):
        self._seed_broken_chain()
        now = time.time()  # fresh, AFTER seeding
        rep = coalesce.run(self.conn, now=now, interval_s=3600, force=True,
                           watermark=self.wm)
        self.assertTrue(rep.fired)
        self.assertGreaterEqual(rep.reconciled, 1)
        self.assertEqual(len(consolidate.pending_consolidations(self.conn)), 0)
        self.assertEqual(rep.pending_remaining, 0)   # fixed point = 100% coverage
        self.assertGreater(coalesce.load_watermark(self.wm), 0)

    def test_container_notes_survive_a_forced_pass(self):
        """100% coverage WITHOUT destruction: the pipeline shape must pass
        with zero closes — distinct notes are not conflicts."""
        self._seed_container_notes()
        before = {f["id"]: f["content"] for f in memdb.valid_facts(self.conn)}
        now = time.time()
        rep = coalesce.run(self.conn, now=now, interval_s=3600, force=True,
                           watermark=self.wm)
        self.assertTrue(rep.fired)
        self.assertEqual(rep.reconciled, 0)
        self.assertEqual(rep.merged, 0)
        self.assertEqual(rep.superseded_ids, [])
        after = {f["id"]: f["content"] for f in memdb.valid_facts(self.conn)}
        self.assertEqual(after, before)              # every note intact
        self.assertEqual(rep.pending_remaining, 0)   # and the pass is complete

    def test_reconciled_fact_cannot_be_injected(self):
        self._seed_broken_chain()
        now = time.time()
        coalesce.run(self.conn, now=now, interval_s=3600, force=True, watermark=self.wm)
        from core.retrieval import inject
        inj = inject(self.conn, domains=("3v0",), query_terms=["substrate"],
                     budget_chars=100000, touch=False)
        self.assertTrue(any("bitdeer" in (f.get("content") or "") for f in inj.facts))
        self.assertFalse(any("fireworks" in (f.get("content") or "")
                             and "bitdeer" not in (f.get("content") or "") for f in inj.facts))

    def test_natural_cadence_fires_when_due(self):
        """The non-force arm: an old watermark + elapsed interval fires via
        cadence alone (this is the path the wake runner actually uses)."""
        now = time.time()
        self._seed_broken_chain()
        coalesce.save_watermark(now - 10000, self.wm)  # long overdue
        rep = coalesce.run(self.conn, now=now, interval_s=60, force=False,
                           watermark=self.wm)
        self.assertTrue(rep.fired)
        self.assertGreaterEqual(rep.reconciled, 1)
        self.assertEqual(rep.pending_remaining, 0)

    def test_token_overlap_empty_content_guard(self):
        """Punctuation/empty content never merges: the token-overlap guard
        returns 0.0, so co-occurrence alone can't collapse distinct notes."""
        self.assertEqual(coalesce._token_overlap("hello world", ""), 0.0)
        self.assertEqual(coalesce._token_overlap("", "hello world"), 0.0)
        a = memdb.add_fact(self.conn, "3v0", "note", "???", content="???:;")
        b = memdb.add_fact(self.conn, "3v0", "note", "???2", content="???:;")
        merged, closed = coalesce._merge_near_duplicates(self.conn, threshold=0.5)
        self.assertEqual(merged, 0)
        self.assertEqual(closed, [])
        alive = [f["id"] for f in memdb.valid_facts(self.conn)]
        self.assertIn(a, alive)
        self.assertIn(b, alive)

    def test_natural_cadence_with_no_watermark(self):
        """First-ever run (no watermark file) is treated as due so bootstrap
        consolidation happens on the first wake."""
        missing = Path(self._tmp.name) / "wm-missing.json"
        rep = coalesce.run(self.conn, now=time.time() + 10, interval_s=3600,
                           force=False, watermark=missing)
        self.assertTrue(rep.fired)

    def test_near_duplicate_merge_and_reversibility(self):
        a = memdb.add_fact(self.conn, "gw", "substrate", "bitdeer",
                           content="3v0 gateway runs as a systemd service")
        b = memdb.add_fact(self.conn, "gw", "substrate", "bitdeer",
                           content="gateway 3v0 runs systemd service")
        merged, closed = coalesce._merge_near_duplicates(self.conn, threshold=0.7)
        self.assertGreaterEqual(merged, 1)
        self.assertIn(a, closed)  # older id superseded; newest (b) kept
        self.conn.execute("UPDATE facts SET valid_to=NULL WHERE id=?", (a,))
        self.conn.commit()
        self.assertEqual(len([f for f in memdb.valid_facts(self.conn) if f["id"] == a]), 1)


if __name__ == "__main__":
    unittest.main()