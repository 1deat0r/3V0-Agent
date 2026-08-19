"""Deterministic tests for the watermark-driven consolidation (core/coalesce.py).

NOTE on the clock: facts are seeded with ``valid_from = now`` at runtime, and a
supersede close writes ``valid_to = now`` at reconcile time. Tests must therefore
evaluate with a *fresh* ``time.time()`` taken *after* seeding (a future or stale
clock leaves just-closed facts temporarily valid and makes reconciles no-op).
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

    def _seed_conflict(self):
        memdb.add_fact(self.conn, "model", "substrate", "fireworks",
                       content="primary model runs on fireworks")
        memdb.add_fact(self.conn, "model", "substrate", "bitdeer",
                       content="primary model runs on bitdeer deepseek")

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

    def test_force_fires_and_reconciles_conflict(self):
        self._seed_conflict()
        now = time.time()  # fresh, AFTER seeding
        rep = coalesce.run(self.conn, now=now, interval_s=3600, force=True,
                           watermark=self.wm)
        self.assertTrue(rep.fired)
        self.assertGreaterEqual(rep.reconciled, 1)
        self.assertEqual(len(consolidate.pending_consolidations(self.conn)), 0)
        self.assertGreater(coalesce.load_watermark(self.wm), 0)

    def test_reconciled_fact_cannot_be_injected(self):
        self._seed_conflict()
        now = time.time()  # fresh, AFTER seeding
        coalesce.run(self.conn, now=now, interval_s=3600, force=True, watermark=self.wm)
        from core.retrieval import inject
        inj = inject(self.conn, domains=("3v0",), query_terms=["substrate"],
                     budget_chars=100000, touch=False)
        self.assertTrue(any("bitdeer" in (f.get("content") or "") for f in inj.facts))
        self.assertFalse(any("fireworks" in (f.get("content") or "")
                             and "bitdeer" not in (f.get("content") or "") for f in inj.facts))

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