"""Tests for the continuity meta (3v0/core/continuity.py) — Stone 17.

The *decision* half is pure: each invariant check is a function over a flat
context dict, so it is tested without git / network / file I/O. The collection
half (``scripts/continuity_check.py``) is exercised live, not here.

Direct run:  python3 3v0/tests/test_continuity.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.continuity import (  # noqa: E402
    ANCHOR_MARKERS,
    CANONICAL_MODEL_PATHS,
    DEFAULT_INVARIANTS,
    check_anchor,
    check_github_loops,
    check_ledger,
    check_memory_profile,
    check_self_describing,
    check_skills_store,
    evaluate,
)


def _ctx(**kw) -> dict:
    """A fully-consistent baseline context; override with kwargs."""
    base = {
        "anchor_present": True,
        "anchor_text": (
            "# anchor\n\n"
            + "\n".join(ANCHOR_MARKERS)
            + "\n\n"
            + "\n".join(f"- `{p}`" for p in CANONICAL_MODEL_PATHS)
        ),
        "model_reachable": {p: True for p in CANONICAL_MODEL_PATHS},
        "memory": {"imported": 0, "dropped": 0, "exported": 0},
        "user": {"imported": 0, "dropped": 0, "exported": 0},
        "skills": {
            "imported": 0, "edited": 0, "dropped": 0,
            "exported": 0, "unresolved": 0, "state_changes": 0,
        },
        "github_loops": {
            "86711": {"kind": "pr", "claimed_state": "OPEN", "live_state": "OPEN", "live_ok": True},
            "84667": {"kind": "issue", "claimed_state": "OPEN", "live_state": "OPEN", "live_ok": True},
        },
        "ledger_ok": True,
        "ledger_count": 3,
        "ledger_detail": "",
    }
    base.update(kw)
    return base


class TestAnchor(unittest.TestCase):
    def test_anchor_missing_drifts(self):
        r = check_anchor(_ctx(anchor_present=False))
        self.assertTrue(r.drift)

    def test_anchor_malformed_drifts(self):
        r = check_anchor(_ctx(anchor_text="no markers here"))
        self.assertTrue(r.drift)
        self.assertIn("malformed", r.detail)

    def test_anchor_well_formed_ok(self):
        r = check_anchor(_ctx())
        self.assertFalse(r.drift)

    def test_anchor_not_healable(self):
        inv = next(i for i in DEFAULT_INVARIANTS if i.name == "anchor")
        self.assertFalse(inv.healable)


class TestSelfDescribing(unittest.TestCase):
    def test_ok_when_referenced_and_reachable(self):
        self.assertFalse(check_self_describing(_ctx()).drift)

    def test_unreachable_drifts(self):
        reachable = {p: False for p in CANONICAL_MODEL_PATHS}
        r = check_self_describing(_ctx(model_reachable=reachable))
        self.assertTrue(r.drift)
        self.assertIn("unreachable", r.detail)

    def test_not_referenced_drifts(self):
        r = check_self_describing(_ctx(anchor_text="# anchor\n## Prime Directive\n"))
        self.assertTrue(r.drift)
        self.assertIn("not referenced", r.detail)

    def test_missing_anchor_drifts(self):
        r = check_self_describing(_ctx(anchor_present=False))
        self.assertTrue(r.drift)


class TestMemoryProfile(unittest.TestCase):
    def test_clean_ok(self):
        self.assertFalse(check_memory_profile(_ctx()).drift)

    def test_import_drifts_and_healable(self):
        r = check_memory_profile(_ctx(memory={"imported": 2, "dropped": 0, "exported": 0}))
        self.assertTrue(r.drift)
        inv = next(i for i in DEFAULT_INVARIANTS if i.name == "memory-profile")
        self.assertTrue(inv.healable)

    def test_user_export_drifts(self):
        r = check_memory_profile(_ctx(user={"imported": 0, "dropped": 0, "exported": 1}))
        self.assertTrue(r.drift)
        self.assertIn("user:1", r.detail)

    def test_unreadable_store_drifts(self):
        r = check_memory_profile(_ctx(memory={"error": "boom"}))
        self.assertTrue(r.drift)
        self.assertIn("unreadable", r.detail)

    def test_undeployed_profile_is_ok(self):
        # No profile memories dir = no second artifact to disagree with the
        # store; the check is n/a, not drift (the store is canonical).
        r = check_memory_profile(_ctx(profile_deployed=False))
        self.assertFalse(r.drift)
        self.assertIn("not deployed", r.detail)

    def test_undeployed_profile_overrides_store_diff(self):
        # Even a full store-vs-nothing delta must not flag when the profile
        # is deliberately absent.
        r = check_memory_profile(
            _ctx(profile_deployed=False,
                 memory={"imported": 0, "dropped": 0, "exported": 14})
        )
        self.assertFalse(r.drift)


class TestSkillsStore(unittest.TestCase):
    def test_clean_ok(self):
        self.assertFalse(check_skills_store(_ctx()).drift)

    def test_edited_drifts_and_healable(self):
        ctx = _ctx(skills={"imported": 0, "edited": 1, "dropped": 0,
                           "exported": 0, "unresolved": 0, "state_changes": 0})
        r = check_skills_store(ctx)
        self.assertTrue(r.drift)
        self.assertIn("edited=1", r.detail)
        inv = next(i for i in DEFAULT_INVARIANTS if i.name == "skills-store")
        self.assertTrue(inv.healable)

    def test_state_change_drifts(self):
        ctx = _ctx(skills={"imported": 0, "edited": 0, "dropped": 0,
                           "exported": 0, "unresolved": 0, "state_changes": 2})
        self.assertTrue(check_skills_store(ctx).drift)

    def test_unreadable_store_drifts(self):
        self.assertTrue(check_skills_store(_ctx(skills={"error": "boom"})).drift)

    def test_undeployed_skills_dir_is_ok(self):
        ctx = _ctx(
            skills_profile_deployed=False,
            skills={"imported": 0, "edited": 0, "dropped": 0,
                    "exported": 10, "unresolved": 0, "state_changes": 0},
        )
        r = check_skills_store(ctx)
        self.assertFalse(r.drift)
        self.assertIn("absent", r.detail)


class TestLedger(unittest.TestCase):
    def test_ok(self):
        self.assertFalse(check_ledger(_ctx()).drift)

    def test_unreadable_drifts(self):
        r = check_ledger(_ctx(ledger_ok=False, ledger_detail="malformed"))
        self.assertTrue(r.drift)
        self.assertIn("malformed", r.detail)

    def test_ledger_not_healable(self):
        inv = next(i for i in DEFAULT_INVARIANTS if i.name == "ledger")
        self.assertFalse(inv.healable)


class TestGithubLoops(unittest.TestCase):
    def test_clean_ok(self):
        self.assertFalse(check_github_loops(_ctx()).drift)

    def test_state_change_drifts(self):
        loops = {
            "86711": {"kind": "pr", "claimed_state": "OPEN", "live_state": "MERGED", "live_ok": True},
        }
        r = check_github_loops(_ctx(github_loops=loops))
        self.assertTrue(r.drift)
        self.assertIn("OPEN->MERGED", r.detail)

    def test_unverifiable_drifts(self):
        loops = {
            "86711": {"kind": "pr", "claimed_state": "OPEN", "live_state": None,
                      "live_ok": False, "live_error": "gh timeout"},
        }
        r = check_github_loops(_ctx(github_loops=loops))
        self.assertTrue(r.drift)
        self.assertIn("unverifiable", r.detail)

    def test_empty_registry_is_ok(self):
        # Empty is a steady state: no tracked claim can disagree with live.
        r = check_github_loops(_ctx(github_loops={}))
        self.assertFalse(r.drift)
        self.assertIn("empty", r.detail)

    def test_unreadable_registry_drifts(self):
        r = check_github_loops(_ctx(github_loops={}, github_loops_error="no such file"))
        self.assertTrue(r.drift)
        self.assertIn("claim registry unreadable", r.detail)

    def test_not_healable(self):
        inv = next(i for i in DEFAULT_INVARIANTS if i.name == "github-loops")
        self.assertFalse(inv.healable)


class TestEvaluate(unittest.TestCase):
    def test_all_clean_no_drift(self):
        report = evaluate(DEFAULT_INVARIANTS, _ctx())
        self.assertEqual(report["drift_count"], 0)
        self.assertEqual(report["healable_drift"], 0)
        self.assertEqual(report["total"], len(DEFAULT_INVARIANTS))

    def test_single_healable_drift_counted(self):
        ctx = _ctx(memory={"imported": 1, "dropped": 0, "exported": 0})
        report = evaluate(DEFAULT_INVARIANTS, ctx)
        self.assertEqual(report["drift_count"], 1)
        self.assertEqual(report["healable_drift"], 1)

    def test_semantic_drift_not_healable(self):
        ctx = _ctx(anchor_present=False)
        report = evaluate(DEFAULT_INVARIANTS, ctx)
        self.assertGreaterEqual(report["drift_count"], 1)
        self.assertEqual(report["healable_drift"], 0)

    def test_every_invariant_reports_a_detail(self):
        report = evaluate(DEFAULT_INVARIANTS, _ctx())
        for inv in report["invariants"]:
            self.assertIn("name", inv)
            self.assertIn("detail", inv)
            self.assertIsInstance(inv["drift"], bool)


if __name__ == "__main__":
    unittest.main()
