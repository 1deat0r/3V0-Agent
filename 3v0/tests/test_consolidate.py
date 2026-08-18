"""Deterministic tests for memory consolidation / conflict reconciliation
(MindMemOS "dreaming", arXiv 2608.12428)."""
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import memdb, consolidate


class PendingTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(f"{self._tmp.name}/m.db")

    def test_no_conflict_single_truth(self):
        memdb.add_fact(self.conn, "gateway", "state", "running",
                       content="gateway state is running")
        self.assertEqual(consolidate.pending_consolidations(self.conn), [])

    def test_conflict_detected(self):
        memdb.add_fact(self.conn, "gateway", "state", "running",
                       content="gateway state is running")
        memdb.add_fact(self.conn, "gateway", "state", "stopped",
                       content="gateway state is stopped")
        pend = consolidate.pending_consolidations(self.conn)
        self.assertEqual(len(pend), 1)
        self.assertEqual((pend[0].subject, pend[0].predicate), ("gateway", "state"))
        self.assertEqual(pend[0].distinct_contents, 2)
        self.assertTrue(pend[0].conflicting)


class ReconcileTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(f"{self._tmp.name}/m.db")

    def _seed_conflict(self):
        a = memdb.add_fact(self.conn, "model", "substrate", "fireworks",
                           content="model substrate is fireworks",
                           domain="benchmark")
        b = memdb.add_fact(self.conn, "model", "substrate", "bitdeer",
                           content="model substrate is bitdeer",
                           domain="benchmark")
        return a, b

    def test_reconcile_keeps_newest_closes_rest(self):
        a, b = self._seed_conflict()  # b is newest (higher id)
        res = consolidate.reconcile(self.conn, "model", "substrate")
        self.assertTrue(res.reconciled)
        self.assertEqual(res.keeper_id, b)
        self.assertEqual(set(res.closed), {a})
        remaining = [f for f in memdb.valid_facts(self.conn, domain="benchmark")
                     if f["subject"] == "model"]
        self.assertEqual([f["content"] for f in remaining], ["model substrate is bitdeer"])

    def test_reconciled_fact_cannot_be_injected(self):
        a, b = self._seed_conflict()
        consolidate.reconcile(self.conn, "model", "substrate")
        # The @ sup... superseded-away fact (a) is inactive: valid_to set, so
        # retrieval's valid_facts gate excludes it (fail-close holds).
        allf = memdb.valid_facts(self.conn, domain="benchmark")
        self.assertNotIn(a, [f["id"] for f in allf])

    def test_noop_when_not_conflicting(self):
        memdb.add_fact(self.conn, "s", "p", "x", content="same text")
        memdb.add_fact(self.conn, "s", "p", "x", content="same text")
        res = consolidate.reconcile(self.conn, "s", "p")
        self.assertFalse(res.reconciled)
        self.assertEqual(res.closed, [])

    def test_reconcile_reversible(self):
        a, b = self._seed_conflict()
        res = consolidate.reconcile(self.conn, "model", "substrate")
        closed_id = res.closed[0]
        # Restore the closed fact's validity -> it is valid again (no content lost).
        self.conn.execute("UPDATE facts SET valid_to = NULL WHERE id = ?",
                          (closed_id,))
        self.conn.commit()
        allf = memdb.valid_facts(self.conn, domain="benchmark")
        ids = [f["id"] for f in allf]
        self.assertIn(closed_id, ids)