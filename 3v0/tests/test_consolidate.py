"""Deterministic tests for memory consolidation / conflict reconciliation
(MindMemOS "dreaming", arXiv 2608.12428).

Conflict identity is the CHAIN ANCHOR: the lineage root a fact resolves to by
walking its ``supersedes`` link. The canonical pipeline writes every fact
under the container key ('3v0', 'note') — so (subject, predicate) can never
identify "the same assertion". Unlinked facts under one container key are
distinct notes (never reconciled); a chain holding >1 valid member is the
supersession-invariant breach consolidation exists to repair.
"""
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

    def test_container_key_notes_are_not_conflicts(self):
        """THE regression guard: the pipeline writes every note under
        ('3v0','note'); distinct unlinked notes must never read as one
        conflict — reconciliation would destroy 30 distinct memories."""
        for i, text in enumerate(("note one about substrate",
                                  "note two about fiverr",
                                  "note three about gateway")):
            memdb.add_fact(self.conn, "3v0", "note", text, content=text)
        pend = consolidate.pending_consolidations(self.conn)
        self.assertEqual(pend, [])

    def test_no_conflict_single_truth(self):
        memdb.add_fact(self.conn, "gateway", "state", "running",
                       content="gateway state is running")
        self.assertEqual(consolidate.pending_consolidations(self.conn), [])

    def test_no_conflict_unlinked_same_key_same_and_diff_content(self):
        """Unlinked same-key facts are distinct notes in the pipeline model,
        even when their content overlaps — no chain anchor, no conflict."""
        memdb.add_fact(self.conn, "3v0", "note", "a", content="gateway is running")
        memdb.add_fact(self.conn, "3v0", "note", "b", content="gateway is stopped")
        self.assertEqual(consolidate.pending_consolidations(self.conn), [])

    def _broken_chain(self):
        """Two live truths in ONE chain: b supersedes a (closing it), then a
        is reopened — the invariant breach consolidation must repair."""
        a = memdb.add_fact(self.conn, "gateway", "state", "running",
                           content="gateway state is running")
        b = memdb.add_fact(self.conn, "gateway", "state", "stopped",
                           content="gateway state is stopped", supersedes=a)
        # re-open a: both a and b now claim to be the live truth of this chain
        self.conn.execute("UPDATE facts SET valid_to=NULL WHERE id=?", (a,))
        self.conn.commit()
        return a, b

    def test_conflict_detected_in_one_chain(self):
        a, b = self._broken_chain()
        pend = consolidate.pending_consolidations(self.conn)
        self.assertEqual(len(pend), 1)
        self.assertEqual(pend[0].root_id, a)          # anchored at lineage root
        self.assertEqual(pend[0].subject, "gateway")
        self.assertEqual(pend[0].predicate, "state")
        self.assertEqual(pend[0].distinct_contents, 2)
        self.assertTrue(pend[0].conflicting)

    def test_anchor_is_lineage_root_not_member(self):
        """A 3-link chain's pending entry anchors at the root id regardless
        of which member was most recently written."""
        a = memdb.add_fact(self.conn, "model", "substrate", "one",
                           content="substrate is one")
        b = memdb.add_fact(self.conn, "model", "substrate", "two",
                           content="substrate is two", supersedes=a)
        c = memdb.add_fact(self.conn, "model", "substrate", "three",
                           content="substrate is three", supersedes=b)
        # re-open a AND b: three live members of one chain (the violation)
        self.conn.execute("UPDATE facts SET valid_to=NULL WHERE id IN (?, ?)", (a, b))
        self.conn.commit()
        pend = consolidate.pending_consolidations(self.conn)
        self.assertEqual(len(pend), 1)
        self.assertEqual(pend[0].root_id, a)
        self.assertEqual({f["id"] for f in pend[0].facts}, {a, b, c})

    def test_cycle_is_fail_safe(self):
        """A hand-edited cycle (b.supersedes=a, a.supersedes=b) must not hang
        pending — the lineage walk is bounded."""
        a = memdb.add_fact(self.conn, "s", "p", "x", content="text x")
        b = memdb.add_fact(self.conn, "s", "p", "y", content="text y", supersedes=a)
        conn = self.conn
        # close the gap the FK allows us to create by direct SQL
        conn.execute("UPDATE facts SET supersedes=? WHERE id=?", (b, a))
        conn.commit()
        pend = consolidate.pending_consolidations(self.conn)
        self.assertLessEqual(len(pend), 1)


class ReconcileTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(f"{self._tmp.name}/m.db")

    def _broken_chain(self):
        a = memdb.add_fact(self.conn, "model", "substrate", "fireworks",
                           content="model substrate is fireworks",
                           domain="benchmark")
        b = memdb.add_fact(self.conn, "model", "substrate", "bitdeer",
                           content="model substrate is bitdeer",
                           domain="benchmark", supersedes=a)
        self.conn.execute("UPDATE facts SET valid_to=NULL WHERE id=?", (a,))
        self.conn.commit()
        return a, b

    def test_reconcile_unknown_root_is_noop(self):
        """A dangling/unknown anchor id must not crash and must close nothing
        — the missing-parent path of the lineage walk."""
        memdb.add_fact(self.conn, "s", "p", "x", content="text x")
        res = consolidate.reconcile(self.conn, 999999)
        self.assertFalse(res.reconciled)
        self.assertEqual(res.closed, [])
        self.assertIsNone(res.kept_content)
        alive = [f["id"] for f in memdb.valid_facts(self.conn)]
        self.assertEqual(len(alive), 1)

    def test_reconcile_on_cyclic_chain_is_bounded(self):
        """Reconciling a hand-edited cycle (a.sup=b, b.sup=a) terminates —
        the member walk's seen-guard breaks the loop. It may collapse one
        member (both claim to be live truth) but must not hang or crash."""
        a = memdb.add_fact(self.conn, "s", "p", "x", content="text x")
        b = memdb.add_fact(self.conn, "s", "p", "y", content="text y", supersedes=a)
        conn = self.conn
        conn.execute("UPDATE facts SET supersedes=? WHERE id=?", (b, a))
        conn.commit()
        res = consolidate.reconcile(conn, a)
        self.assertLessEqual(len(res.closed), 1)

    def test_reconcile_keeps_newest_closes_rest(self):
        a, b = self._broken_chain()  # b is newest (higher id)
        root = consolidate.pending_consolidations(self.conn)[0].root_id
        res = consolidate.reconcile(self.conn, root)
        self.assertTrue(res.reconciled)
        self.assertEqual(res.keeper_id, b)
        self.assertEqual(set(res.closed), {a})
        remaining = [f for f in memdb.valid_facts(self.conn, domain="benchmark") if f["subject"] == "model"]
        self.assertEqual([f["content"] for f in remaining], ["model substrate is bitdeer"])

    def test_reconciled_fact_cannot_be_injected(self):
        a, b = self._broken_chain()
        root = consolidate.pending_consolidations(self.conn)[0].root_id
        consolidate.reconcile(self.conn, root)
        # The superseded-away fact (a) is inactive: valid_to set, so
        # retrieval's valid_facts gate excludes it (fail-close holds).
        allf = memdb.valid_facts(self.conn, domain="benchmark")
        self.assertNotIn(a, [f["id"] for f in allf])

    def test_noop_when_chain_holds_one_truth(self):
        memdb.add_fact(self.conn, "s", "p", "x", content="same text")
        pend = consolidate.pending_consolidations(self.conn)
        if pend:  # no broken chain -> nothing to reconcile
            res = consolidate.reconcile(self.conn, pend[0].root_id)
            self.assertFalse(res.reconciled)
            self.assertEqual(res.closed, [])

    def test_reconcile_reversible(self):
        a, b = self._broken_chain()
        root = consolidate.pending_consolidations(self.conn)[0].root_id
        res = consolidate.reconcile(self.conn, root)
        closed_id = res.closed[0]
        # Restore the closed fact's validity -> it is valid again (no content lost).
        self.conn.execute("UPDATE facts SET valid_to = NULL WHERE id = ?", (closed_id,))
        self.conn.commit()
        allf = memdb.valid_facts(self.conn, domain="benchmark")
        ids = [f["id"] for f in allf]
        self.assertIn(closed_id, ids)

    def test_reconcile_never_touches_other_chains(self):
        a1 = memdb.add_fact(self.conn, "k1", "p", "one", content="key one keeps its truth")
        b1 = memdb.add_fact(self.conn, "k1", "p", "two", content="key one newer truth", supersedes=a1)
        self.conn.execute("UPDATE facts SET valid_to=NULL WHERE id=?", (a1,))
        memdb.add_fact(self.conn, "k2", "p", "solo", content="key two: a distinct note")
        pend = consolidate.pending_consolidations(self.conn)
        self.assertEqual(len(pend), 1)   # only the broken chain is pending
        self.assertEqual(pend[0].root_id, a1)
        res = consolidate.reconcile(self.conn, a1)
        self.assertIn(a1, res.closed)
        # k2's note still valid, untouched
        k2 = [f for f in memdb.valid_facts(self.conn) if f["subject"] == "k2"]
        self.assertEqual(len(k2), 1)


if __name__ == "__main__":
    unittest.main()