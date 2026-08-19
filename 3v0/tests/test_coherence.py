"""Deterministic tests for the coherence engine (core/coherence.py)."""
import unittest
from pathlib import Path
from unittest import mock
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import coherence, insights  # noqa: E402


class CoherenceTest(unittest.TestCase):
    def test_model_ids_self_consistent(self):
        self.assertEqual(coherence.check_model_ids_consistent(), [])

    def test_model_mismatch_fails_closed(self):
        with mock.patch.object(insights, "AUX_MODEL", "gpt-9-utterly-unintended"):
            conflicts = coherence.check_model_ids_consistent()
        self.assertTrue(any(c.kind == "fail_close" for c in conflicts))
        self.assertFalse(any(c.kind == "auto_resolve" for c in conflicts))

    def test_stale_phrases_are_defined(self):
        self.assertGreater(len(coherence.STALE_PHRASES), 0)

    def test_run_no_open_on_coherent_body(self):
        r = coherence.run(apply=False)
        self.assertGreaterEqual(r.checked, 1)
        self.assertEqual(r.open, [])  # the body must be coherent (fail-closed = nothing open)

    def test_conflict_dataclass_fields(self):
        c = coherence.Conflict("x", "fail_close", "detail")
        self.assertFalse(c.resolved)
        self.assertEqual(c.kind, "fail_close")
        self.assertIn(c, coherence.Report(conflicts=[c]).conflicts)


if __name__ == "__main__":
    unittest.main()