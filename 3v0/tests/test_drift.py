"""Tests for drift computation (3v0/core/drift.py) — Stone 16.

The *decision* half (``compute_drift``) is pure and tested without git; the
*collection* half (``collect_git_state``) is tested against a real throwaway
git repo plus non-repo paths.

Direct run:  python3 3v0/tests/test_drift.py
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.drift import GitState, compute_drift  # noqa: E402
from core.gitstate import collect_git_state, store_hash  # noqa: E402
from core.projects import LedgerEntry  # noqa: E402


def _entry(**kw) -> LedgerEntry:
    defaults: dict[str, Any] = dict(
        name="x",
        title="X",
        repo=Path("/r"),
        upstream="origin",
        upstream_ref="main",
        track_upstream=True,
        store=Path("/s"),
        primary=False,
    )
    defaults.update(kw)
    return LedgerEntry(**defaults)


def _git(**kw) -> GitState:
    return GitState(**kw)


class TestComputeDrift(unittest.TestCase):
    def test_clean_tracked_project_is_ok(self):
        e = _entry(store_head="deadbeef")
        g = _git(head="abc", upstream_head="up", behind=0, ahead=5, dirty=False)
        r = compute_drift(e, g, "deadbeef")
        self.assertFalse(r["drifting"])
        self.assertFalse(r["head_moved"])
        self.assertFalse(r["store_changed"])
        self.assertTrue(r["store_present"])

    def test_behind_upstream_drifts_when_tracked(self):
        e = _entry(track_upstream=True)
        g = _git(head="abc", upstream_head="up", behind=7, ahead=0, dirty=False)
        r = compute_drift(e, g, "h")
        self.assertTrue(r["drifting"])
        self.assertTrue(any("behind" in reason for reason in r["reasons"]))

    def test_behind_upstream_is_not_drift_when_pinned(self):
        e = _entry(track_upstream=False)
        g = _git(head="abc", upstream_head="up", behind=700, ahead=0, dirty=False)
        r = compute_drift(e, g, "h")
        self.assertFalse(r["drifting"])

    def test_missing_upstream_ref_drifts_when_tracked(self):
        e = _entry(track_upstream=True)
        g = _git(head="abc", upstream_head=None, dirty=False)
        r = compute_drift(e, g, "h")
        self.assertTrue(r["drifting"])
        self.assertTrue(any("not found" in reason for reason in r["reasons"]))

    def test_dirty_worktree_drifts(self):
        e = _entry()
        g = _git(head="abc", upstream_head="up", behind=0, ahead=0, dirty=True)
        r = compute_drift(e, g, "h")
        self.assertTrue(r["drifting"])
        self.assertTrue(any("uncommitted" in reason for reason in r["reasons"]))

    def test_missing_store_drifts(self):
        e = _entry(store=Path("/s"))
        g = _git(head="abc", upstream_head="up", behind=0, ahead=0, dirty=False)
        r = compute_drift(e, g, None)
        self.assertTrue(r["drifting"])
        self.assertFalse(r["store_present"])

    def test_store_changed_is_informational_not_drift(self):
        e = _entry(store_head="old")
        g = _git(head="abc", upstream_head="up", behind=0, ahead=0, dirty=False)
        r = compute_drift(e, g, "new")
        self.assertTrue(r["store_changed"])
        self.assertFalse(r["drifting"])

    def test_head_moved_is_informational_not_drift(self):
        e = _entry(head="old")
        g = _git(head="new", upstream_head="up", behind=0, ahead=0, dirty=False)
        r = compute_drift(e, g, "h")
        self.assertTrue(r["head_moved"])
        self.assertFalse(r["drifting"])

    def test_git_error_drifts(self):
        e = _entry()
        g = _git(error="not a git repo")
        r = compute_drift(e, g, "h")
        self.assertTrue(r["drifting"])
        self.assertTrue(any("not a git repo" in reason for reason in r["reasons"]))


class TestStoreHash(unittest.TestCase):
    def test_hash_real_file(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "m.json"
            p.write_text("hello", encoding="utf-8")
            self.assertEqual(store_hash(p), hashlib.sha256(b"hello").hexdigest())

    def test_hash_missing_file_is_none(self):
        self.assertIsNone(store_hash(Path("/nonexistent/x.json")))

    def test_hash_none_path_is_none(self):
        self.assertIsNone(store_hash(None))


def _init_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@example.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "t"], check=True)
    (path / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-qm", "init"], check=True)


class TestCollectGitState(unittest.TestCase):
    def test_clean_repo_has_head_and_no_dirt(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "r"
            _init_repo(repo)
            entry = LedgerEntry(name="r", title="R", repo=repo, upstream="origin")
            gs = collect_git_state(entry)
            self.assertIsNone(gs.error)
            self.assertRegex(gs.head or "", r"^[0-9a-f]{40}$")
            self.assertFalse(gs.dirty)
            self.assertIsNone(gs.upstream_head)  # no remote configured

    def test_dirty_repo_reports_dirt(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "r"
            _init_repo(repo)
            (repo / "f.txt").write_text("changed", encoding="utf-8")
            entry = LedgerEntry(name="r", title="R", repo=repo, upstream="origin")
            gs = collect_git_state(entry)
            self.assertIsNone(gs.error)
            self.assertTrue(gs.dirty)

    def test_non_repo_directory_reports_error(self):
        with tempfile.TemporaryDirectory() as td:
            entry = LedgerEntry(name="r", title="R", repo=Path(td), upstream="origin")
            gs = collect_git_state(entry)
            self.assertIsNotNone(gs.error)

    def test_missing_repo_reports_error(self):
        entry = LedgerEntry(name="r", title="R", repo=Path("/nonexistent/xyz"), upstream="origin")
        gs = collect_git_state(entry)
        self.assertIsNotNone(gs.error)


if __name__ == "__main__":
    unittest.main()
