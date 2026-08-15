"""Tests for the project registry (3v0/core/projects.py).

Direct run:  python3 3v0/tests/test_projects.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.projects import resolve_project  # noqa: E402


BODY = Path("/home/me/Projects/AI Agents/3V0 Agent")
PROFILE = Path("/home/me/.hermes/profiles/3v0")
HOME = Path("/home/me")


class TestResolveProject(unittest.TestCase):
    def test_threev0_is_primary_full_axis(self):
        spec = resolve_project("threev0", BODY, PROFILE, home=HOME)
        self.assertEqual(spec.title, "3V0")
        self.assertEqual(spec.store, BODY / "3v0" / "data" / "memory.json")
        self.assertEqual(spec.skill_store, BODY / "3v0" / "data" / "skills.json")
        self.assertEqual(spec.profile_mem, PROFILE / "memories")
        self.assertEqual(spec.review_log, PROFILE / "3v0_reviews" / "reviews.jsonl")
        self.assertEqual(spec.cwd_roots, (BODY,))
        self.assertTrue(spec.primary)
        self.assertFalse(spec.memory_only)
        self.assertFalse(spec.store_only)

    def test_siblings_are_memory_only_and_store_only(self):
        for name, subdir in (
            ("f1nance", ("Projects", "AI Agents", "F1NANCE Agent")),
            ("axiom", ("Projects", "axiom-agent")),
        ):
            spec = resolve_project(name, BODY, PROFILE, home=HOME)
            self.assertEqual(spec.store, BODY / "3v0" / "data" / name / "memory.json")
            self.assertIsNone(spec.skill_store)
            self.assertIsNone(spec.profile_mem)
            self.assertEqual(
                spec.review_log, PROFILE / "3v0_reviews" / name / "reviews.jsonl"
            )
            self.assertEqual(spec.cwd_roots, (HOME.joinpath(*subdir),))
            self.assertFalse(spec.primary)
            self.assertTrue(spec.memory_only)
            self.assertTrue(spec.store_only)

    def test_default_name_is_threev0(self):
        self.assertEqual(resolve_project(None, BODY, PROFILE, home=HOME).name, "threev0")
        self.assertEqual(resolve_project("", BODY, PROFILE, home=HOME).name, "threev0")

    def test_cwd_override_redirects_root_only(self):
        spec = resolve_project("f1nance", BODY, PROFILE, home=HOME, cwd_override="/tmp/f1")
        self.assertEqual(spec.cwd_roots, (Path("/tmp/f1"),))
        self.assertFalse(spec.primary)  # override never changes primary-ness
        self.assertTrue(spec.store_only)
        self.assertTrue(spec.memory_only)

    def test_unknown_project_raises(self):
        with self.assertRaises(ValueError):
            resolve_project("bogus", BODY, PROFILE, home=HOME)


if __name__ == "__main__":
    unittest.main()
