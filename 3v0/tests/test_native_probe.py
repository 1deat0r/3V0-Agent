"""Deterministic tests for the native probe core (measurement math)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from native import probe  # noqa: E402


def verdicts(spec):
    """Build a verdict list from {band: [.. 'PASS'/'FAIL' ..]}."""
    out = []
    for band, marks in spec.items():
        for i, m in enumerate(marks):
            out.append({"id": f"{band}{i}", "band": band, "verdict": m})
    return out


class ValidateTest(unittest.TestCase):
    def test_real_frozen_bank_passes(self):
        repo = Path(__file__).resolve().parent.parent.parent
        with open(repo / "3v0" / "data" / "probe_bank_v1.json") as f:
            bank = json.load(f)
        r = probe.validate_bank(bank)
        self.assertTrue(r["ok"])

    def test_bad_bank_flags_issues(self):
        bad = {"tasks": [
            {"id": "x1", "band": "easy", "domain": "coding", "prompt": "hello",
             "rubric": {"pass": [], "inconclusive": ""}},  # missing time_box_min
            {"id": "x1", "band": "easy", "domain": "coding", "prompt": "system says 3v0",
             "rubric": {"pass": [], "inconclusive": ""}, "time_box_min": 1},
        ]}
        r = probe.validate_bank(bad)
        self.assertFalse(r["ok"])
        blob = " ".join(r["issues"])
        self.assertIn("bands mismatch", blob)
        self.assertIn("duplicate", blob.replace("duplicate task ids", "duplicate"))
        self.assertIn("3v0", blob)


class StatsTest(unittest.TestCase):
    def test_band_stats_math(self):
        vs = verdicts({"easy": ["PASS", "PASS", "FAIL"], "hard": ["PASS", "INCONCLUSIVE"]})
        s = probe.band_stats(vs)
        self.assertEqual(s["easy"], {"n": 3, "passed": 2, "rate": 2 / 3})
        self.assertEqual(s["hard"]["n"], 2)
        self.assertEqual(s["hard"]["rate"], 0.5)

    def test_composite_weighted_per_band(self):
        # two bands, each 1.0 -> composite 1.0 (not silenced by per-task counts)
        vs = verdicts({"easy": ["PASS", "PASS", "PASS"], "hard": ["PASS"]})
        self.assertEqual(probe.composite(vs), 1.0)
        # single band 50% -> 0.5
        self.assertEqual(probe.composite(verdicts({"a": ["PASS", "FAIL"]})), 0.5)
        # unequal band sizes weight by band, not by task
        vs2 = verdicts({"easy": ["PASS", "PASS", "PASS", "FAIL"], "hard": ["PASS"]})
        self.assertAlmostEqual(probe.composite(vs2), (0.75 + 1.0) / 2)

    def test_frontier_highest_band_passed(self):
        self.assertEqual(probe.frontier(verdicts({"easy": ["PASS"], "hard": ["FAIL"]})), "easy")
        self.assertEqual(probe.frontier(verdicts({"easy": ["FAIL"], "hard": ["PASS"]})), "hard")
        self.assertEqual(probe.frontier(verdicts({"escalated": ["PASS"]})), "escalated")
        self.assertIsNone(probe.frontier(verdicts({"easy": ["FAIL"]})))

    def test_calibrate_and_thresholds(self):
        # repeat1: all PASS, repeat2: 1 fail per 4 easy, 2 fail per 4 hard
        r1 = verdicts({"easy": ["PASS"] * 4, "hard": ["PASS"] * 4})
        r2 = verdicts({"easy": ["PASS"] * 3 + ["FAIL"], "hard": ["PASS"] * 2 + ["FAIL"] * 2})
        cal = probe.calibrate([r1, r2])
        self.assertEqual(cal["easy"]["mean"], (1.0 + 0.75) / 2)
        self.assertGreater(cal["easy"]["sd"], 0)
        th = probe.thresholds(cal, sigma=2.0)
        self.assertLessEqual(th["easy"]["lo"], th["easy"]["hi"])
        self.assertAlmostEqual(th["easy"]["mean"], 0.875)


class TrendTest(unittest.TestCase):
    TH = {"easy": {"lo": 0.5, "hi": 1.0}, "hard": {"lo": 0.0, "hi": 0.6},
          "medium": {"lo": 0.0, "hi": 1.0}}

    def test_single_run_excursion_not_flagged(self):
        # §3 gate: one out-of-band run is NOT reproducible -> no signal claimed
        one = [{"easy": {"rate": 0.1}, "hard": {"rate": 1.0}, "medium": {"rate": 0.5}}]
        tr = probe.apply_trend(one, self.TH, min_repeats=2)
        self.assertEqual(tr["flagged"], [])
        self.assertEqual(tr["per_band"]["easy"]["signal"], "within-noise")

    def test_two_consecutive_runs_flag(self):
        run = {"easy": {"rate": 0.1}, "hard": {"rate": 1.0}, "medium": {"rate": 0.5}}
        tr = probe.apply_trend([run, run], self.TH, min_repeats=2)
        self.assertIn("easy", tr["flagged"])
        self.assertIn("hard", tr["flagged"])
        self.assertNotIn("medium", tr["flagged"])
        self.assertEqual(tr["per_band"]["easy"]["signal"], "regression-suspect")
        self.assertEqual(tr["per_band"]["hard"]["signal"], "growth-hint")
        self.assertEqual(tr["per_band"]["easy"]["consecutive"], 2)

    def test_trend_within_noise(self):
        run = {"easy": {"rate": 0.8}, "hard": {"rate": 0.5}}
        tr = probe.apply_trend([run, run], self.TH, min_repeats=2)
        self.assertEqual(tr["flagged"], [])


class NullControlTest(unittest.TestCase):
    """Frozen-agent null control (Phantom Gains): a live run is asserted only
    as its delta vs. a frozen null, gated by the calibrated noise band."""

    def test_live_identical_to_null_is_off(self):
        # Wide-open calibration band makes every rate inside noise.
        th = {b: {"mean": 0.5, "lo": 0.0, "hi": 1.0} for b in probe.BAND_ORDER}
        live = verdicts({"easy": ["PASS", "PASS"], "hard": ["PASS"]})
        null = verdicts({"easy": ["PASS", "PASS"], "hard": ["PASS"]})
        r = probe.null_control(live, null, th)
        for band, d in r["per_band"].items():
            self.assertEqual(d["signal"], "off", band)
        self.assertAlmostEqual(r["per_band"]["easy"]["delta"], 0.0)
        self.assertTrue(r["advisory"])

    def test_live_growth_beyond_null_is_candidate(self):
        th = {b: {"mean": 0.5, "lo": 0.4, "hi": 0.6} for b in probe.BAND_ORDER}
        null = verdicts({"easy": ["PASS", "FAIL"]})     # 0.5 inside band
        live = verdicts({"easy": ["PASS", "PASS"]})     # 1.0 outside band
        r = probe.null_control(live, null, th)
        self.assertEqual(r["per_band"]["easy"]["signal"], "growth-hint")
        self.assertAlmostEqual(r["per_band"]["easy"]["delta"], 0.5)

    def test_live_regression_beyond_null_is_candidate(self):
        th = {b: {"mean": 0.5, "lo": 0.4, "hi": 0.6} for b in probe.BAND_ORDER}
        null = verdicts({"easy": ["PASS", "FAIL"]})     # 0.5 inside band
        live = verdicts({"easy": ["FAIL", "FAIL"]})     # 0.0 below band
        r = probe.null_control(live, null, th)
        self.assertEqual(r["per_band"]["easy"]["signal"], "regression-suspect")
        self.assertAlmostEqual(r["per_band"]["easy"]["delta"], -0.5)

    def test_null_drift_invalidates_comparison(self):
        # If the FROZEN NULL itself falls outside the calibrated band, the
        # control is stale -> comparison invalid, never a directional claim.
        th = {b: {"mean": 0.5, "lo": 0.4, "hi": 0.6} for b in probe.BAND_ORDER}
        null = verdicts({"easy": ["PASS", "PASS"]})     # 1.0, drifted
        live = verdicts({"easy": ["PASS", "FAIL"]})     # 0.5 inside
        r = probe.null_control(live, null, th)
        self.assertEqual(r["per_band"]["easy"]["signal"], "null-drift")

    def test_uncalibrated_band_is_skipped(self):
        # A band with no thresholds entry cannot bound noise -> skip, no signal.
        live = verdicts({"easy": ["PASS", "PASS"]})
        null = verdicts({"easy": ["PASS", "FAIL"]})
        th = {"easy": {"mean": 0.5, "lo": 0.0, "hi": 1.0}}   # no "hard" entry
        r = probe.null_control(live, null, th)
        self.assertIn("per_band", r)
        self.assertNotIn("hard", r["per_band"])
        self.assertEqual(r["per_band"]["easy"]["signal"], "off")

    def test_composes_with_calibrate_and_thresholds(self):
        # Rollout shape: calibrate -> thresholds -> null_control.
        repeats = [verdicts({"easy": ["PASS", "PASS", "PASS", "PASS"]}),
                   verdicts({"easy": ["PASS", "PASS", "PASS", "FAIL"]})]
        cal = probe.calibrate(repeats)
        th = probe.thresholds(cal)
        null = verdicts({"easy": ["PASS", "PASS", "PASS", "PASS"]})
        live = verdicts({"easy": ["PASS", "PASS", "PASS", "PASS"]})
        r = probe.null_control(live, null, th)
        self.assertEqual(r["per_band"]["easy"]["signal"], "off")


class RecordTest(unittest.TestCase):
    def test_record_run_appends(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "probe_results.json"
            m1 = probe.record_run(p, {"grader": "g1", "commit": "abc"}, verdicts({"easy": ["PASS"]}))
            m2 = probe.record_run(p, {"grader": "g1", "commit": "def"}, verdicts({"easy": ["FAIL"]}))
            self.assertEqual((m1["recorded"], m2["recorded"]), (1, 2))
            data = json.loads(p.read_text())
            self.assertEqual(len(data["runs"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
