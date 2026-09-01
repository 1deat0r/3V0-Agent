"""Tests for the generated handoff (3v0/core/handoff.py) — Stone 18.

The *decision* half is pure: ``render_handoff`` (context -> markdown) and
``extract_loop_state_claims`` / ``diff_loop_claims`` (narrative vs live truth)
read a flat dict and a string, so they are tested without git / network /
file I/O. The collection half (``scripts/generate_handoff.py``) is exercised
live at wake, not here — same split as Stone 17's continuity meta.

Direct run:  python3 3v0/tests/test_handoff.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.handoff import (  # noqa: E402
    GENERATED_BANNER,
    diff_loop_claims,
    extract_loop_state_claims,
    render_handoff,
)


def _loops() -> list:
    """A four-loop context matching the live claim registry's shape."""
    return [
        {"num": "86711", "kind": "pr", "claimed_state": "OPEN",
         "live_state": "OPEN", "live_ok": True, "note": "approval fix"},
        {"num": "72067", "kind": "pr", "claimed_state": "OPEN",
         "live_state": "OPEN", "live_ok": True, "note": "memory null-action"},
        {"num": "73453", "kind": "pr", "claimed_state": "OPEN",
         "live_state": "MERGED", "live_ok": True, "note": "skill load details"},
        {"num": "84667", "kind": "issue", "claimed_state": "OPEN",
         "live_state": "OPEN", "live_ok": False, "live_error": "gh timeout",
         "note": "cron skill-not-found"},
    ]


def _ctx(**kw) -> dict:
    base = {
        "generated_at": "2026-08-16T04:30:00Z",
        "git_head": "18e3f64e4",
        "git": {
            "branch": "main", "ahead": "87", "behind": "0",
            "dirty": False, "recent": ["18e3f64e4 docs: handoff", "30f87785f test: fault"],
            "head": "18e3f64e4",
        },
        "continuity": {
            "total": 6, "drift_count": 0, "healable_drift": 0,
            "invariants": [
                {"name": "anchor", "drift": False, "detail": "anchor present"},
                {"name": "github-loops", "drift": False, "detail": "4 loops agree"},
            ],
        },
        "drift": {
            "drifting": 0, "total": 3,
            "projects": [
                {"name": "threev0", "title": "3V0", "drifting": False,
                 "behind": 0, "ahead": 87, "dirty": False, "head_moved": True},
                {"name": "f1nance", "title": "F1NANCE", "drifting": False,
                 "behind": 0, "ahead": 41, "dirty": False, "head_moved": True},
                {"name": "axiom", "title": "Axiom", "drifting": False,
                 "behind": 0, "ahead": 22, "dirty": False, "head_moved": True},
            ],
        },
        "loops": _loops(),
        "store": {
            "facts": {"memory": 6, "user": 2, "directive": 1},
            "fact_versions": 25, "active_skills": 8, "skill_versions": 30,
            "skill_states": {},
        },
        "daemons": {"3v0-review": "active", "axiom-review": "active", "f1nance-review": "active"},
    }
    base.update(kw)
    return base


class TestRenderHandoff(unittest.TestCase):
    def test_renders_all_sections(self):
        md = render_handoff(_ctx())
        for header in ("## Body", "## Continuity", "## Drift (project ledger)",
                       "## Open loops", "## Store", "## Daemons", "## Startup (canonical)"):
            self.assertIn(header, md, header)

    def test_no_daemons_omits_section_and_systemctl_step(self):
        # The operator consolidation retired the review-daemon trio: with an
        # empty daemon set the section disappears and the canonical startup
        # drops the systemctl probe instead of naming dead units.
        md = render_handoff(_ctx(daemons={}))
        self.assertNotIn("## Daemons", md)
        self.assertNotIn("systemctl --user status", md)
        self.assertIn("handoff_check.sh", md)

    def test_banner_marks_mechanical_state_canonical(self):
        md = render_handoff(_ctx())
        self.assertIn(GENERATED_BANNER, md)
        # The flip is operator-authorized: the draft is canonical for
        # mechanical state, and the narrative stays hand-written.
        self.assertIn("canonical since 2026-08-16", GENERATED_BANNER)
        self.assertIn("HANDOFF.md", GENERATED_BANNER)

    def test_includes_loop_numbers_and_states(self):
        md = render_handoff(_ctx())
        self.assertIn("#86711", md)
        self.assertIn("claim OPEN", md)

    def test_includes_body_git_state(self):
        md = render_handoff(_ctx())
        self.assertIn("ahead 87", md)
        self.assertIn("behind 0", md)
        self.assertIn("working tree clean", md)

    def test_partial_context_does_not_crash(self):
        md = render_handoff({})
        self.assertIn("## Body", md)
        self.assertIn("(continuity report unavailable)", md)

    def test_drift_verdict_rendered(self):
        ctx = _ctx(continuity={
            "total": 6, "drift_count": 1,
            "invariants": [{"name": "anchor", "drift": True, "detail": "anchor missing"}],
        })
        self.assertIn("DRIFT", render_handoff(ctx))

    def test_unverifiable_loop_rendered(self):
        md = render_handoff(_ctx())
        self.assertIn("unverifiable", md)  # loop 84667 has live_ok=False

    def test_loop_renders_mergeable_and_title_when_present(self):
        loops = [{
            "num": "86711", "kind": "pr", "claimed_state": "OPEN",
            "live_state": "OPEN", "live_ok": True, "mergeable": "MERGEABLE",
            "updated_at": "2026-08-15T05:08:16Z", "title": "fix(approval): whitespace",
            "note": "awaiting merge",
        }]
        md = render_handoff(_ctx(loops=loops))
        self.assertIn("mergeable MERGEABLE", md)
        self.assertIn("fix(approval): whitespace", md)
        self.assertIn("awaiting merge", md)


class TestExtractLoopStateClaims(unittest.TestCase):
    def test_finds_state_word_near_number(self):
        text = "PR #86711 is OPEN and awaiting merge."
        self.assertEqual(extract_loop_state_claims(text, ["86711"]), {"86711": {"OPEN"}})

    def test_no_state_word_is_empty(self):
        text = "see #86711 for details"
        self.assertEqual(extract_loop_state_claims(text, ["86711"]), {"86711": set()})

    def test_does_not_match_embedded_number(self):
        # "12386711456" contains "86711" but is a longer number — must not match.
        text = "commit 12386711456 is OPEN"
        self.assertEqual(extract_loop_state_claims(text, ["86711"]), {"86711": set()})

    def test_mergeable_is_not_a_state(self):
        # "MERGEABLE" is the mergeable field, not the state field — must not be
        # collected as a state assertion (it is consistent with state=OPEN).
        text = "PR #86711 is MERGEABLE"
        self.assertEqual(extract_loop_state_claims(text, ["86711"]), {"86711": set()})

    def test_collects_multiple_distinct_states(self):
        text = "#86711 OPEN here ... and CLOSED over there"
        self.assertEqual(
            extract_loop_state_claims(text, ["86711"]), {"86711": {"OPEN", "CLOSED"}}
        )


class TestDiffLoopClaims(unittest.TestCase):
    def test_agree_when_narrative_matches_live(self):
        text = "PR #86711 is OPEN."
        d = diff_loop_claims([_loops()[0]], text)
        self.assertEqual(d[0]["status"], "agree")

    def test_drift_when_narrative_says_merged_but_live_open(self):
        text = "PR #86711 was MERGED."
        d = diff_loop_claims([_loops()[0]], text)
        self.assertEqual(d[0]["status"], "drift")
        self.assertIn("MERGED", d[0]["asserted"])

    def test_drift_when_narrative_says_open_but_live_merged(self):
        # loop 73453 has live_state=MERGED; narrative claims OPEN -> drift.
        text = "PR #73453 is OPEN."
        d = diff_loop_claims([_loops()[2]], text)
        self.assertEqual(d[0]["status"], "drift")

    def test_unmentioned_when_number_absent(self):
        d = diff_loop_claims([_loops()[0]], "nothing about that PR here")
        self.assertEqual(d[0]["status"], "unmentioned")

    def test_unverifiable_when_no_truth(self):
        loop = {"num": "99999", "kind": "pr", "claimed_state": None,
                "live_state": None, "live_ok": False}
        d = diff_loop_claims([loop], "PR #99999 is OPEN")
        self.assertEqual(d[0]["status"], "unverifiable")

    def test_truth_falls_back_to_claim_when_live_unverifiable(self):
        # 84667: live_ok=False but claimed_state=OPEN -> truth OPEN, narrative
        # says CLOSED -> drift against the claim.
        d = diff_loop_claims([_loops()[3]], "issue #84667 is CLOSED")
        self.assertEqual(d[0]["status"], "drift")
        self.assertEqual(d[0]["truth"], "OPEN")


if __name__ == "__main__":
    unittest.main()
