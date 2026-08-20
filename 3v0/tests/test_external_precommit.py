"""Tests for the reset-proof external pre-commit hook (F6, post-incident).

The hook lives OUTSIDE the repo (canonical hooksPath = ~/.3V0/githooks) so
a git reset/clobber of the working tree cannot delete the protection.

Invariants:
  I1. A commit fails (non-zero exit) when the repo carries a remote named
      `origin` — the 2026-08-20 footgun.
  I2. The hook must not fail commits on a healthy repo (no origin remote,
      only public/upstream/fork remotes).
  I3. The hook must not run the wiki auto-sync (that stays in-repo) — this
      external hook is sovereignty-only: origin check + noisy-state guard.
  I4. Malformed/no .git -> pass (never false-block a non-repo dir).
"""
import os
import subprocess
import tempfile
import unittest

HOOK = os.path.expanduser("~/.3V0/githooks/pre-commit")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True,
    )


class ExternalPreCommitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(HOOK):
            raise unittest.SkipTest(f"external hook not present: {HOOK}")

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.repo = self._td.name
        git(self.repo, "init", "-q", ".")
        git(self.repo, "config", "user.email", "test@3v0.local")
        git(self.repo, "config", "user.name", "3V0 Test")
        with open(os.path.join(self.repo, "f.txt"), "w") as f:
            f.write("x\n")
        git(self.repo, "add", "f.txt")

    def tearDown(self):
        self._td.cleanup()

    def run_hook(self):
        return subprocess.run(
            ["/bin/bash", HOOK],
            cwd=self.repo,
            capture_output=True, text=True,
            timeout=30,
        )

    def test_commit_fails_when_origin_remote_exists(self):
        git(self.repo, "remote", "add", "origin", "https://github.com/1deat0r/3V0-Agent")
        git(self.repo, "remote", "add", "public", "https://github.com/1deat0r/3V0-Agent.git")
        proc = self.run_hook()
        self.assertNotEqual(proc.returncode, 0, f"hook must fail with origin present: {proc.stdout}")

    def test_commit_succeeds_when_no_origin(self):
        git(self.repo, "remote", "add", "public", "https://github.com/1deat0r/3V0-Agent.git")
        git(self.repo, "remote", "add", "upstream", "https://github.com/1deat0r/3V0-Agent")
        proc = self.run_hook()
        self.assertEqual(proc.returncode, 0, f"hook must pass without origin: {proc.stdout}")

    def test_commit_succeeds_when_no_remotes(self):
        proc = self.run_hook()
        self.assertEqual(proc.returncode, 0)

    def test_non_repo_dir_passes(self):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "junk.txt"), "w") as f:
                f.write("no git here\n")
            proc = subprocess.run(
                ["/bin/bash", HOOK], cwd=td, capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()