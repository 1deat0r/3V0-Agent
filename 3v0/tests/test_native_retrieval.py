"""Deterministic tests for the native retrieval-chosen context path (ADR-0004 seam).

The seam is the test surface: drive build_system_from_store / core.retrieval.inject
through a temp SQLite store and assert the working set + feedback — never scoring
internals."""
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import memdb                     # noqa: E402
from native import context                 # noqa: E402


class RetrievalSeamTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = memdb.connect(str(Path(self._tmp.name) / "mem.db"))
        # two facts, same domain; second is newer (ranks higher on recency)
        self.id_old = memdb.add_fact(self.conn, "3v0", "note", "old seed",
                                     content="old: alpha", now=1000.0, persist=True)
        self.id_new = memdb.add_fact(self.conn, "3v0", "note", "new seed",
                                     content="newer: beta", now=2000.0, persist=True)

    def tearDown(self):
        self.conn.close()
        self._tmp.cleanup()

    def _access_count(self, fid):
        return self.conn.execute("SELECT access_count FROM facts WHERE id=?", (fid,)).fetchone()[0]

    def test_preview_touch_false_ranks_and_writes_nothing(self):
        sys = context.build_system_from_store("I am 3V0.", conn=self.conn,
                                              touch=False, budget_chars=4096)
        self.assertIn("I am 3V0.", sys)
        self.assertIn("retrieval-chosen working set", sys)
        # both facts present and text is buildable
        self.assertIn("newer: beta", sys)
        self.assertIn("old: alpha", sys)
        # touch=False -> no feedback written
        self.assertEqual(self._access_count(self.id_old), 0)
        self.assertEqual(self._access_count(self.id_new), 0)

    def test_touch_true_writes_feedback(self):
        context.build_system_from_store("s", conn=self.conn, touch=True, budget_chars=4096)
        self.assertEqual(self._access_count(self.id_new), 1)
        self.assertEqual(self._access_count(self.id_old), 1)

    def test_budget_shapes_working_set_and_truncates(self):
        # tiny budget: only the highest-ranked (newest) fact fits, whole-fact granularity
        sys = context.build_system_from_store("s", conn=self.conn,
                                              touch=False, budget_chars=18)
        # "newer: beta" (11 chars) fits; "old: alpha" would exceed the remaining -> truncated out
        self.assertIn("newer: beta", sys)
        self.assertNotIn("old: alpha", sys)

    def test_superseded_fact_not_injected(self):
        # close the old fact's validity; it must not appear
        self.conn.execute("UPDATE facts SET valid_to=? WHERE id=?", (3000.0, self.id_old))
        self.conn.commit()
        sys = context.build_system_from_store("s", conn=self.conn, touch=False, budget_chars=4096)
        self.assertNotIn("old: alpha", sys)
        self.assertIn("newer: beta", sys)


if __name__ == "__main__":
    unittest.main(verbosity=2)
