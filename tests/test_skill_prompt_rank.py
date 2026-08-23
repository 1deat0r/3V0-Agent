"""Tests for the usage-aware skill-index ranker (M3).

Run directly:
  python3 tests/test_skill_prompt_rank.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from agent.skill_prompt_rank import should_apply, rank_and_demote, fit_budget  # noqa: E402
from agent.skill_prompt_rank import _entry_chars  # noqa: E402  (test helper)

USAGE_NEVER = {}
USAGE_USED = {
    "alpha": {"use_count": 3, "last_used_at": "2026-08-20T10:00:00Z"},
}
USAGE_RECENT = {
    "alpha": {"use_count": 3, "last_used_at": "2026-08-20T10:00:00Z"},
    "beta": {"use_count": 1, "last_used_at": "2026-08-22T10:00:00Z"},
}


def _entry(name: str, desc: str = "d") -> dict:
    return {"skill_name": name, "frontmatter_name": name, "description": desc}


class TestShouldApply(unittest.TestCase):
    def test_empty_usage_is_false(self) -> None:
        self.assertFalse(should_apply({}))
        self.assertFalse(should_apply({"alpha": {"use_count": 0}}))

    def test_any_real_use_is_true(self) -> None:
        self.assertTrue(should_apply(USAGE_USED))


class TestRankAndDemote(unittest.TestCase):
    def test_returns_names_only_for_never_used(self) -> None:
        used, names_only = rank_and_demote([_entry("alpha")], USAGE_NEVER)
        self.assertEqual(used, [])
        self.assertIsNotNone(names_only)
        names_joined, note = names_only
        self.assertIn("alpha", names_joined)
        self.assertIn("not used recently", note)

    def test_used_skill_not_demoted(self) -> None:
        used, names_only = rank_and_demote([_entry("alpha")], USAGE_USED)
        self.assertEqual(len(used), 1)
        self.assertEqual(used[0]["name"], "alpha")
        self.assertIsNone(names_only)

    def test_recency_ordering(self) -> None:
        entries = [_entry("alpha"), _entry("beta")]
        used, _ = rank_and_demote(entries, USAGE_RECENT)
        # beta used more recently sorts first
        self.assertEqual([u["name"] for u in used], ["beta", "alpha"])

    def test_ties_break_alphabetically(self) -> None:
        entries = [_entry("beta"), _entry("alpha")]
        usage = {
            "beta": {"use_count": 1, "last_used_at": "2026-08-20T10:00:00Z"},
            "alpha": {"use_count": 1, "last_used_at": "2026-08-20T10:00:00Z"},
        }
        used, _ = rank_and_demote(entries, usage)
        self.assertEqual([u["name"] for u in used], ["alpha", "beta"])

    def test_mixed_used_and_never(self) -> None:
        entries = [_entry("alpha"), _entry("gamma"), _entry("beta")]
        usage = {"beta": {"use_count": 1, "last_used_at": "2026-08-20T10:00:00Z"}}
        used, names_only = rank_and_demote(entries, usage)
        self.assertEqual([u["name"] for u in used], ["beta"])
        # alpha/gamma are the never-used tail, sorted
        names_joined, _ = names_only
        self.assertEqual(sorted(names_joined.split(", ")), ["alpha", "gamma"])

    def test_missing_or_invalid_usage_never_crashes(self) -> None:
        entries = [_entry("alpha"), _entry("beta"), _entry("gamma")]
        # not a dict / wrong types / garbage timestamp
        usage = {
            "alpha": "not-a-dict",
            "beta": {"use_count": None, "last_used_at": "garbage"},
            "gamma": {"use_count": 2, "last_used_at": "not-a-date"},
        }
        used, names_only = rank_and_demote(entries, usage)
        # only gamma (valid count) is used; alpha+beta fall to the tail
        self.assertEqual([u["name"] for u in used], ["gamma"])
        self.assertIsNotNone(names_only)
        names_joined, _ = names_only
        self.assertEqual(sorted(names_joined.split(", ")), ["alpha", "beta"])

    def test_sidecar_roundtrip_reads_valid_use(self) -> None:
        # The real sidecar is a JSON file; make sure our parsing of it lines up.
        path = os.path.join(tempfile.mkdtemp(), ".usage.json")
        Path(path).write_text(json.dumps(USAGE_RECENT), encoding="utf-8")
        usage = json.loads(Path(path).read_text(encoding="utf-8"))
        used, names_only = rank_and_demote([_entry("alpha"), _entry("beta")], usage)
        self.assertEqual([u["name"] for u in used], ["beta", "alpha"])
        self.assertIsNone(names_only)


class TestFitBudget(unittest.TestCase):
    def _used(self, names: list[str], usage: dict) -> list:
        return rank_and_demote([_entry(n) for n in names], usage)[0]

    def test_keeps_top_value_under_budget(self) -> None:
        usage = {
            "recent": {"use_count": 1, "last_used_at": "2026-08-22T10:00:00Z"},
            "old": {"use_count": 1, "last_used_at": "2026-08-10T10:00:00Z"},
        }
        used = self._used(["recent", "old"], usage)
        # A budget that fits only the recent entry.
        budget = _entry_chars(used[0])
        kept, demoted = fit_budget(used, budget)
        self.assertEqual([u["name"] for u in kept], ["recent"])
        self.assertEqual(demoted, ["old"])

    def test_failure_penalized_below_success(self) -> None:
        # same usage recency, but beta has a failure in its outcome history
        usage = {
            "alpha": {"use_count": 1, "last_used_at": "2026-08-20T10:00:00Z",
                      "outcome_history": [{"outcome": "success"}]},
            "beta": {"use_count": 1, "last_used_at": "2026-08-20T10:00:00Z",
                     "outcome_history": [{"outcome": "failure"}]},
        }
        used = self._used(["alpha", "beta"], usage)
        # fit_budget keeps the highest value (alpha, failure-free) first.
        budget = _entry_chars(used[0])
        kept, demoted = fit_budget(used, budget)
        self.assertEqual([u["name"] for u in kept], ["alpha"])
        self.assertEqual(demoted, ["beta"])

    def test_nonpositive_budget_keeps_nothing(self) -> None:
        usage = {"alpha": {"use_count": 1, "last_used_at": "2026-08-20T10:00:00Z"}}
        used = self._used(["alpha"], usage)
        kept, demoted = fit_budget(used, 0)
        self.assertEqual(kept, [])
        self.assertEqual(demoted, ["alpha"])

    def test_empty_used(self) -> None:
        kept, demoted = fit_budget([], 1000)
        self.assertEqual(kept, [])
        self.assertEqual(demoted, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)