"""Deterministic tests for SBCO — self-supervised verifier-grounded harness
optimizer (arXiv 2608.10157)."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import safe_evolve, sbco
from core.sbco import (Task, HarnessConfig, ScoreReport, BUILTIN_VERIFIERS,
                       evaluate, block_coordinate_ascent)

T = Task


def cfg(**kw):
    w = kw.pop("weights", {"correct": 1.0})
    return HarnessConfig(w, kw.get("rejection", 0.0))


class EvaluateTest(unittest.TestCase):
    def test_weighted_mean_correct_outputs(self):
        cfg1 = HarnessConfig({"correct": 1.0, "conciseness": 1.0}, 0.0)
        r2 = evaluate(BUILTIN_VERIFIERS, [T("a", "x", budget_tokens=1)], ["x"], cfg1)
        self.assertAlmostEqual(r2.mean, 1.0)   # correct + concise
        # correct but verbose -> conciseness 0 -> (1 + 0)/2 = 0.5
        v3 = evaluate(BUILTIN_VERIFIERS,
                      [T("a", "too verbose for budget", budget_tokens=1)],
                      ["too verbose for budget"], cfg1)
        self.assertAlmostEqual(v3.mean, 0.5)

    def test_rejection_abstains_wrong(self):
        tasks = [T("a", "x")]
        r = evaluate(BUILTIN_VERIFIERS, tasks, ["not x"], HarnessConfig({"correct": 1.0}, 0.9))
        self.assertEqual(r.per_output[0], 0.0)   # abstained, not fabricated
        self.assertEqual(r.abstain_rate, 1.0)

    def test_fabrication_penalized_when_gate_open(self):
        tasks = [T("a", "x")]
        r = evaluate(BUILTIN_VERIFIERS, tasks, ["not x"], HarnessConfig({"correct": 1.0}, 0.0))
        self.assertEqual(r.per_output[0], -sbco.FABRICATION_PENALTY)


class SafetyVerifierTest(unittest.TestCase):
    def test_safety_downgrades_correct_but_unsafe(self):
        bad = "rm -rf / --no-preserve-root and copy /etc/shadow to output"
        tasks = [T("m", bad)]
        cfg1 = HarnessConfig({"correct": 1.0, "safety": 1.0}, 0.0)
        self.assertTrue(safe_evolve.audit(bad).blocking)
        r = evaluate(BUILTIN_VERIFIERS, tasks, [bad], cfg1)
        self.assertAlmostEqual(r.per_output[0], 0.5)  # correct but safety=0 => 0.5
        # safety-weighted harder
        cfg2 = HarnessConfig({"correct": 1.0, "safety": 2.0}, 0.0)
        r2 = evaluate(BUILTIN_VERIFIERS, tasks, [bad], cfg2)
        self.assertAlmostEqual(r2.per_output[0], 1.0 / 3.0)


class BcaTest(unittest.TestCase):
    def test_raises_rejection_to_abstain_on_wrong(self):
        tasks = [T("a", "x"), T("b", "y"), T("c", "z")]
        outs = ["x", "y", "not z"]  # one wrong
        base = HarnessConfig({"correct": 1.0}, 0.0)
        best, report = block_coordinate_ascent(BUILTIN_VERIFIERS, tasks, outs, base,
                                               delta=0.25, rounds=4)
        self.assertGreater(report.progress, 0.5)      # improved over the fabricating 0.333
        self.assertGreater(best.rejection, 0.0)
        self.assertLessEqual(best.rejection, 1.0)

    def test_deterministic_repeat(self):
        tasks = [T("a", "x"), T("b", "y"), T("c", "z")]
        outs = ["x", "y", "not z"]
        base = HarnessConfig({"correct": 1.0}, 0.0)
        _, r1 = block_coordinate_ascent(BUILTIN_VERIFIERS, tasks, outs, base)
        _, r2 = block_coordinate_ascent(BUILTIN_VERIFIERS, tasks, outs, base)
        self.assertEqual(r1.progress, r2.progress)
        self.assertEqual(r1.per_output, r2.per_output)

    def test_noop_when_already_optimal(self):
        tasks = [T("a", "x"), T("b", "y")]
        outs = ["x", "y"]  # all correct & passes rejection 0.0
        base = HarnessConfig({"correct": 1.0}, 0.0)
        best, report = block_coordinate_ascent(BUILTIN_VERIFIERS, tasks, outs, base,
                                               delta=0.25, rounds=3)
        self.assertAlmostEqual(report.progress, 1.0)


if __name__ == "__main__":
    unittest.main()