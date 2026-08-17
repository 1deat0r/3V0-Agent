"""Tests for the project ledger (3v0/core/projects.py) — Stone 16.

Direct run:  python3 3v0/tests/test_ledger.py
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
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.projects import LedgerEntry, ProjectLedger, resolve_project  # noqa: E402


BODY = Path("/home/me/Projects/AI Agents/3V0 Agent")
PROFILE = Path("/home/me/.hermes/profiles/3v0")
HOME = Path("/home/me")


class TestSeed(unittest.TestCase):
    def test_seed_has_three_projects_with_review_scoping(self):
        ledger = ProjectLedger.seed(BODY, HOME)
        self.assertEqual(ledger.names(), ["axiom", "f1nance", "threev0"])
        threev0 = ledger["threev0"]
        self.assertTrue(threev0.primary)
        self.assertEqual(threev0.store, BODY / "3v0" / "data" / "memory.db")
        self.assertEqual(threev0.skill_store, BODY / "3v0" / "data" / "skills.json")
        self.assertFalse(threev0.memory_only)
        self.assertFalse(threev0.store_only)
        self.assertEqual(threev0.repo, BODY)
        for name, subdir in (
            ("f1nance", ("Projects", "AI Agents", "F1NANCE Agent")),
            ("axiom", ("Projects", "axiom-agent")),
        ):
            e = ledger[name]
            self.assertFalse(e.primary)
            self.assertEqual(e.store, BODY / "3v0" / "data" / name / "memory.json")
            self.assertIsNone(e.skill_store)
            self.assertTrue(e.memory_only)
            self.assertTrue(e.store_only)
            self.assertEqual(e.repo, HOME.joinpath(*subdir))


class TestRoundTrip(unittest.TestCase):
    def test_save_load_roundtrip_preserves_resolved_paths_and_fields(self):
        with tempfile.TemporaryDirectory() as td:
            body = Path(td) / "body"
            home = Path(td) / "home"
            (body / "3v0" / "data" / "projects").mkdir(parents=True)
            entry = LedgerEntry(
                name="foo",
                title="Foo",
                repo=body,
                upstream="origin",
                upstream_ref="main",
                delta="d",
                track_upstream=False,
                profile="foo",
                store=body / "3v0" / "data" / "foo" / "memory.json",
                skill_store=None,
                primary=False,
                head="abc123",
                store_head="deadbeef",
                open_loops=("loop one", "loop two"),
                last_seen_at="2026-08-16T00:00:00Z",
            )
            ledger = ProjectLedger({"foo": entry})
            path = body / "3v0" / "data" / "projects" / "ledger.json"
            ledger.save(body_root=body, home=home, path=path)
            raw = json.loads(path.read_text(encoding="utf-8"))["projects"]["foo"]
            # portable serialized form
            self.assertEqual(raw["repo"], ".")
            self.assertEqual(raw["store"], "3v0/data/foo/memory.json")
            self.assertIsNone(raw["skill_store"])
            self.assertEqual(raw["open_loops"], ["loop one", "loop two"])
            # reload resolves back to absolute
            loaded = ProjectLedger.load(body_root=body, home=home, path=path)
            e = loaded["foo"]
            self.assertEqual(e.repo, body)
            self.assertEqual(e.store, body / "3v0" / "data" / "foo" / "memory.json")
            self.assertIsNone(e.skill_store)
            self.assertFalse(e.track_upstream)
            self.assertEqual(e.head, "abc123")
            self.assertEqual(e.open_loops, ("loop one", "loop two"))


class TestPathResolution(unittest.TestCase):
    def test_load_resolves_dot_tilde_and_absolute(self):
        with tempfile.TemporaryDirectory() as td:
            body = Path(td) / "body"
            home = Path(td) / "home"
            (body / "3v0" / "data" / "projects").mkdir(parents=True)
            path = body / "3v0" / "data" / "projects" / "ledger.json"
            path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "projects": {
                            "a": {"title": "A", "repo": ".", "store": "3v0/data/a/memory.json"},
                            "b": {"title": "B", "repo": "~/x/b", "store": None},
                            "c": {"title": "C", "repo": str(body / "c"), "store": str(body / "s.json")},
                        },
                    }
                ),
                encoding="utf-8",
            )
            ledger = ProjectLedger.load(body_root=body, home=home, path=path)
            self.assertEqual(ledger["a"].repo, body)
            self.assertEqual(ledger["a"].store, body / "3v0" / "data" / "a" / "memory.json")
            self.assertEqual(ledger["b"].repo, home / "x" / "b")
            self.assertIsNone(ledger["b"].store)
            self.assertEqual(ledger["c"].repo, body / "c")
            self.assertEqual(ledger["c"].store, body / "s.json")

    def test_load_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                ProjectLedger.load(body_root=Path(td) / "body")

    def test_load_malformed_raises(self):
        with tempfile.TemporaryDirectory() as td:
            body = Path(td) / "body"
            path = body / "3v0" / "data" / "projects" / "ledger.json"
            path.parent.mkdir(parents=True)
            path.write_text('"just a string"', encoding="utf-8")
            with self.assertRaises(ValueError):
                ProjectLedger.load(body_root=body)


class TestAddRemove(unittest.TestCase):
    def test_add_and_remove_mutate_by_name(self):
        ledger = ProjectLedger.seed(BODY, HOME)
        entry = LedgerEntry(name="new", title="New", repo=BODY)
        ledger.add(entry)
        self.assertIn("new", ledger)
        self.assertEqual(ledger["new"].title, "New")
        ledger.remove("new")
        self.assertNotIn("new", ledger)
        with self.assertRaises(KeyError):
            ledger.remove("new")


class TestResolveProjectFromLedger(unittest.TestCase):
    def test_ledger_driven_resolve_matches_seed_scoping(self):
        ledger = ProjectLedger.seed(BODY, HOME)
        spec = resolve_project("threev0", BODY, PROFILE, home=HOME, ledger=ledger)
        self.assertEqual(spec.title, "3V0")
        self.assertEqual(spec.cwd_roots, (BODY,))
        self.assertTrue(spec.primary)
        self.assertEqual(spec.review_log, PROFILE / "3v0_reviews" / "reviews.jsonl")
        self.assertEqual(spec.profile_mem, PROFILE / "memories")
        spec_f = resolve_project("f1nance", BODY, PROFILE, home=HOME, ledger=ledger)
        self.assertEqual(spec_f.review_log, PROFILE / "3v0_reviews" / "f1nance" / "reviews.jsonl")
        self.assertIsNone(spec_f.profile_mem)
        self.assertTrue(spec_f.store_only)
        self.assertTrue(spec_f.memory_only)

    def test_storeless_entry_is_not_reviewable(self):
        ledger = ProjectLedger(
            {"x": LedgerEntry(name="x", title="X", repo=BODY, store=None)}
        )
        with self.assertRaises(ValueError):
            resolve_project("x", BODY, PROFILE, home=HOME, ledger=ledger)

    def test_unknown_raises(self):
        with self.assertRaises(ValueError):
            resolve_project("bogus", BODY, PROFILE, home=HOME, ledger=ProjectLedger.seed(BODY, HOME))


class TestProjectCLI(unittest.TestCase):
    def test_add_list_remove_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            body = Path(td) / "body"
            repo = Path(td) / "repo"
            repo.mkdir()
            ledger_path = body / "3v0" / "data" / "projects" / "ledger.json"
            env = dict(os.environ, THREEV0_BODY=str(body), THREEV0_LEDGER=str(ledger_path))
            script = str(REPO_ROOT / "3v0" / "scripts" / "project.py")
            add = subprocess.run(
                [sys.executable, script, "add", "demo", "--repo", str(repo), "--delta", "test delta"],
                env=env, capture_output=True, text=True,
            )
            self.assertEqual(add.returncode, 0, add.stderr)
            self.assertTrue(ledger_path.exists())
            raw = json.loads(ledger_path.read_text(encoding="utf-8"))
            self.assertIn("demo", raw["projects"])
            self.assertEqual(raw["projects"]["demo"]["delta"], "test delta")
            # add refuses a duplicate name
            dup = subprocess.run(
                [sys.executable, script, "add", "demo", "--repo", str(repo)],
                env=env, capture_output=True, text=True,
            )
            self.assertEqual(dup.returncode, 1)
            # list shows it
            lst = subprocess.run(
                [sys.executable, script, "list"], env=env, capture_output=True, text=True
            )
            self.assertIn("demo", lst.stdout)
            # remove drops it
            rm = subprocess.run(
                [sys.executable, script, "remove", "demo"], env=env, capture_output=True, text=True
            )
            self.assertEqual(rm.returncode, 0, rm.stderr)
            raw = json.loads(ledger_path.read_text(encoding="utf-8"))
            self.assertNotIn("demo", raw["projects"])


if __name__ == "__main__":
    unittest.main()
