"""Fault-injection (chaos) validation of the continuity clock's *collection* half.

``test_continuity.py`` covers the pure decision half (each invariant check over
a flat context dict). The collection half — ``scripts/continuity_check.py``
reading real artifacts and computing the deltas — was never exercised
end-to-end, which is exactly why the heal-before-check blindness (grill-found,
2026-08-16) lived in the *sequencing* undetected: no test ever asked "does the
clock actually flag drift when drift exists?"

This file closes that gap. For each fault class we inject the fault against a
hermetic temp artifact and assert the clock flags the matching invariant. This
is the research-backed acceptance criterion for "the clock is trustworthy":
fault injection (chaos engineering), not passive waiting for it to fire.

Every test overrides only the artifact under fault with a temp path; the other
invariants run against the real body (best-effort, never crashes) and are not
asserted on. No network calls except the incidental ``gh`` the github-loops
invariant performs against the real claim registry (unrelated to these
assertions).

Direct run:  python3 3v0/tests/test_continuity_fault.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.continuity import ANCHOR_MARKERS, CANONICAL_MODEL_PATHS  # noqa: E402
from core.memory import MemoryStore  # noqa: E402
from core.profile_io import join_entries  # noqa: E402
from core.skills import SkillStore  # noqa: E402

CONTINUITY_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "continuity_check.py"


def _run_check(**overrides: str) -> dict:
    """Run continuity_check.py --json with env overrides; return the report."""
    env = os.environ.copy()
    for key, value in overrides.items():
        env[key] = str(value)
    proc = subprocess.run(
        [sys.executable, str(CONTINUITY_SCRIPT), "--json"],
        capture_output=True, text=True, timeout=120, env=env,
    )
    if proc.returncode != 0:
        raise AssertionError(f"continuity_check exited {proc.returncode}: {proc.stderr}")
    return json.loads(proc.stdout)


def _invariant(report: dict, name: str) -> dict:
    for inv in report["invariants"]:
        if inv["name"] == name:
            return inv
    raise AssertionError(f"invariant {name!r} missing from report")


def _well_formed_anchor_text() -> str:
    return (
        "# anchor\n\n"
        + "\n".join(ANCHOR_MARKERS)
        + "\n\n"
        + "\n".join(f"- `{p}`" for p in CANONICAL_MODEL_PATHS)
    )


class TestMemoryProfileFault(unittest.TestCase):
    def test_store_ahead_of_profile_drifts(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            store = d / "memory.json"
            MemoryStore(store).add("store-only fact", "memory", "fault-inject")
            prof = d / "profile"
            prof.mkdir()
            (prof / "MEMORY.md").write_text("", encoding="utf-8")
            (prof / "USER.md").write_text("", encoding="utf-8")
            report = _run_check(THREEV0_STORE=str(store), THREEV0_PROFILE_MEM=str(prof))
            inv = _invariant(report, "memory-profile")
            self.assertTrue(inv["drift"], inv)
            self.assertIn("store != profile", inv["detail"])

    def test_profile_ahead_of_store_drifts(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            store = d / "memory.json"
            store.write_text(json.dumps({"version": 1, "facts": []}), encoding="utf-8")
            prof = d / "profile"
            prof.mkdir()
            (prof / "MEMORY.md").write_text(join_entries(["profile-only fact"]), encoding="utf-8")
            (prof / "USER.md").write_text("", encoding="utf-8")
            report = _run_check(THREEV0_STORE=str(store), THREEV0_PROFILE_MEM=str(prof))
            inv = _invariant(report, "memory-profile")
            self.assertTrue(inv["drift"], inv)
            self.assertIn("store != profile", inv["detail"])


class TestSkillsStoreFault(unittest.TestCase):
    def test_store_ahead_of_disk_drifts(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            sstore = d / "skills.json"
            SkillStore(sstore).add("fault-skill", "create", "fault-inject", content="---\nname: fault-skill\n---\n")
            skills_dir = d / "skills"
            skills_dir.mkdir()
            report = _run_check(
                THREEV0_SKILL_STORE=str(sstore), THREEV0_SKILLS_DIR=str(skills_dir)
            )
            inv = _invariant(report, "skills-store")
            self.assertTrue(inv["drift"], inv)


class TestAnchorFault(unittest.TestCase):
    def test_anchor_missing_drifts(self):
        with tempfile.TemporaryDirectory() as d:
            missing = Path(d) / "CONTINUITY.md"  # does not exist
            report = _run_check(THREEV0_ANCHOR=str(missing))
            self.assertTrue(_invariant(report, "anchor")["drift"])

    def test_anchor_malformed_drifts(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "CONTINUITY.md"
            bad.write_text("no markers here\n", encoding="utf-8")
            report = _run_check(THREEV0_ANCHOR=str(bad))
            inv = _invariant(report, "anchor")
            self.assertTrue(inv["drift"], inv)
            self.assertIn("malformed", inv["detail"])


class TestLedgerFault(unittest.TestCase):
    def test_ledger_corrupt_drifts(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "ledger.json"
            bad.write_text("{ not json", encoding="utf-8")
            report = _run_check(THREEV0_LEDGER=str(bad))
            inv = _invariant(report, "ledger")
            self.assertTrue(inv["drift"], inv)


class TestSelfDescribingFault(unittest.TestCase):
    def test_unreachable_model_drifts(self):
        with tempfile.TemporaryDirectory() as d:
            body = Path(d) / "body"
            anchor = body / "3v0" / "CONTINUITY.md"
            anchor.parent.mkdir(parents=True)
            anchor.write_text(_well_formed_anchor_text(), encoding="utf-8")
            # model files deliberately NOT created -> unreachable
            report = _run_check(THREEV0_BODY=str(body), THREEV0_ANCHOR=str(anchor))
            inv = _invariant(report, "self-describing")
            self.assertTrue(inv["drift"], inv)
            self.assertIn("unreachable", inv["detail"])


if __name__ == "__main__":
    unittest.main()
