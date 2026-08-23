"""Tests for the skill curation module (3V0 outcome->action).

Run directly:
  python3 3v0/tests/test_skill_curate.py
"""

from __future__ import annotations

import os
import sys
import unittest

REPO_ROOT = __import__("pathlib").Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skill_curate import (  # noqa: E402
    curation_decision,
    failing_skills,
    FailingSkill,
)


def _meta(outcomes: list[tuple[str, int]]) -> dict:
    """Build a skill meta with an outcome_history, most-recent-first."""
    return {
        "outcome_history": [
            {"outcome": o, "at": f"2026-08-{i:02d}T00:00:00Z", "session": f"s{i}"}
            for i, (o, _) in enumerate(outcomes)
        ]
    }


class TestFailingSkills(unittest.TestCase):
    def test_ignores_empty_and_unknown_only(self) -> None:
        recs = {
            "none": {},
            "untested": _meta([("unknown", 1), ("unknown", 2)]),
        }
        self.assertEqual(failing_skills(recs), [])

    def test_under_min_failures_not_failing(self) -> None:
        recs = {"foo": _meta([("failure", 1), ("success", 2)])}
        self.assertEqual(failing_skills(recs), [])

    def test_failure_trend_flags(self) -> None:
        recs = {"foo": _meta([("failure", 1), ("failure", 2), ("success", 3)])}
        fs = failing_skills(recs)
        self.assertEqual(len(fs), 1)
        self.assertEqual(fs[0].name, "foo")
        self.assertEqual(fs[0].failures, 2)
        self.assertEqual(fs[0].successes, 1)
        self.assertEqual(fs[0].rate, 2 / 3)

    def test_sorts_worst_first(self) -> None:
        recs = {
            "ok": _meta([("failure", 1), ("success", 2)]),
            "bad": _meta([("failure", 1), ("failure", 2), ("success", 3)]),
            "worst": _meta([("failure", 1), ("failure", 2), ("failure", 3)]),
        }
        names = [f.name for f in failing_skills(recs)]
        # worst (rate 1.0) first, then bad (0.67), ok below threshold
        self.assertEqual(names, ["worst", "bad"])

    def test_threshold_parameter(self) -> None:
        recs = {"foo": _meta([("failure", 1), ("failure", 2), ("success", 3)])}
        self.assertEqual(failing_skills(recs, threshold=0.9), [])  # 0.67 < 0.9
        self.assertEqual(len(failing_skills(recs, threshold=0.5)), 1)


class TestCurationDecision(unittest.TestCase):
    def test_rewrite_when_ever_succeeded(self) -> None:
        recs = {"foo": _meta([("failure", 1), ("failure", 2), ("success", 3)])}
        self.assertEqual(curation_decision(recs)["foo"], "rewrite")

    def test_retire_when_never_succeeded(self) -> None:
        recs = {"broken": _meta([("failure", 1), ("failure", 2), ("failure", 3)])}
        self.assertEqual(curation_decision(recs)["broken"], "retire")


if __name__ == "__main__":
    unittest.main(verbosity=2)