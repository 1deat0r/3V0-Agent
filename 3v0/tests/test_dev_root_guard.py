"""Seam tests for the 3V0 dev-root guard (3v0/deploy/dev-root-guard.py).

The guard is a stdin-JSON-payload → exit-code black box:
  exit 2 = BLOCK the tool call, exit 0 = allow.

Seams under test (agreed with operator, post-incident 2026-08-20):
  A. Remote-footgun recreation — any command that could re-add an
     `origin`/`upstream` remote to the canonical repo is blocked,
     including non-git spellings (execute_code payloads).
  B. Canonical branch movement — any command that moves the canonical
     repo's branch to a remote-tracking ref (git reset --hard
     upstream/main, checkout -f upstream/main, etc.) is blocked.
  C. Normal development still works — push to `public`, pulls of safe
     remotes, reads inside/outside canonical, non-canonical cwd.

Invariant: a *reference* to a forbidden path (reading, running an
interpreter that lives there) is allowed; a *write target* is blocked.
"""
import json
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANONICAL = "/home/mustbearn/Projects/AI Agents/3V0 Agent"
GUARD = os.path.join(REPO_ROOT, "3v0", "deploy", "dev-root-guard.py")
FORBIDDEN = json.load(open("/home/mustbearn/.config/3v0/dev-root-guard-paths.json"))["forbidden"][0]


class GuardSeamTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(GUARD):
            raise unittest.SkipTest(f"guard not present at {GUARD}")

    def run_guard(self, tool_name, tool_input, cwd=None):
        payload = {"tool_name": tool_name, "tool_input": tool_input}
        if cwd:
            payload["cwd"] = cwd
        proc = subprocess.run(
            [sys.executable, GUARD],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=15,
        )
        return proc.returncode, (proc.stdout + proc.stderr).strip()

    def assert_blocked(self, tool_name, tool_input, cwd=CANONICAL, msg=""):
        code, out = self.run_guard(tool_name, tool_input, cwd=cwd)
        self.assertEqual(code, 2, f"expected BLOCK (exit 2), got {code}: {out} [{msg}]")

    def assert_allowed(self, tool_name, tool_input, cwd=CANONICAL, msg=""):
        code, out = self.run_guard(tool_name, tool_input, cwd=cwd)
        self.assertEqual(code, 0, f"expected ALLOW (exit 0), got {code}: {out} [{msg}]")

    # ------------------------------------------------------------------
    # A. Remote-footgun recreation
    # ------------------------------------------------------------------
    def test_remote_add_origin_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git remote add origin https://github.com/1deat0r/3V0-Agent"},
            msg="terminal git remote add origin must block",
        )

    def test_remote_add_upstream_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git remote add upstream https://github.com/1deat0r/3V0-Agent"},
            msg="adding upstream remote (same footgun later) must block",
        )

    def test_remote_set_url_origin_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git remote set-url origin https://github.com/1deat0r/3V0-Agent"},
            msg="set-url origin must block (regex gap closed)",
        )

    def test_remote_config_origin_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git config remote.origin.url https://github.com/1deat0r/3V0-Agent"},
            msg="config remote.origin.url must block (regex gap closed)",
        )

    def test_remote_rename_upstream_to_origin_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git remote rename upstream origin"},
            msg="rename upstream origin must block (regex gap closed)",
        )

    def test_remote_add_origin_via_execute_code(self):
        # F1: sovereignty checks must also inspect execute_code payloads.
        self.assert_blocked(
            "execute_code",
            {"code": "import subprocess\nsubprocess.run(['git','remote','add','origin','https://github.com/1deat0r/3V0-Agent'])"},
            msg="execute_code must be scanned for remote-add (F1)",
        )

    def test_update_command_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "3v0 update"},
            msg="3v0 update must block",
        )
        self.assert_blocked(
            "terminal",
            {"command": "3v0 update"},
            msg="3v0 update must block",
        )
        self.assert_blocked(
            "terminal",
            {"command": "python -m ev0_cli.main update"},
            msg="python -m ev0_cli.main update must block (regex gap closed)",
        )

    # ------------------------------------------------------------------
    # B. Canonical branch movement (the renamed incident)
    # ------------------------------------------------------------------
    def test_reset_hard_upstream_main_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git reset --hard upstream/main"},
            msg="reset --hard upstream/main must block (F2)",
        )

    def test_reset_hard_origin_main_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git reset --hard origin/main"},
            msg="reset --hard origin/main must block (F2)",
        )

    def test_checkout_f_upstream_main_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git checkout -f upstream/main"},
            msg="checkout -f upstream/main must block (F2)",
        )

    def test_git_c_reset_upstream_main_via_terminal(self):
        self.assert_blocked(
            "terminal",
            {"command": "git -C /home/mustbearn/Projects/AI\\ Agents/3V0\\ Agent reset --hard upstream/main"},
            msg="git -C canonical reset must block (F2)",
        )

    def test_reset_via_execute_code(self):
        self.assert_blocked(
            "execute_code",
            {"code": "import subprocess\nsubprocess.run(['git','reset','--hard','upstream/main'], cwd='/home/mustbearn/Projects/AI Agents/3V0 Agent')"},
            msg="execute_code reset must block (F1+F2)",
        )

    # ------------------------------------------------------------------
    # C. Normal development still works
    # ------------------------------------------------------------------
    def test_push_public_allowed(self):
        self.assert_allowed(
            "terminal",
            {"command": "git push public main"},
            msg="push public must stay allowed",
        )

    def test_pull_public_allowed(self):
        self.assert_allowed(
            "terminal",
            {"command": "git pull public main"},
            msg="pull public must stay allowed",
        )

    def test_read_of_forbidden_tree_allowed(self):
        self.assert_allowed(
            "terminal",
            {"command": f"grep -rn origin {FORBIDDEN}/agent"},
            msg="read-only reference to forbidden tree must stay allowed",
        )

    def test_non_canonical_cwd_remote_add_blocked_by_path(self):
        # A remote-add that names the canonical repo from elsewhere must still block.
        self.assert_blocked(
            "terminal",
            {"command": "git remote add origin https://github.com/1deat0r/3V0-Agent"},
        )

    def test_write_into_forbidden_tree_still_blocked(self):
        self.assert_blocked(
            "write_file",
            {"path": os.path.join(FORBIDDEN, "evil.py")},
            msg="write into forbidden tree must keep blocking",
        )

    def test_write_into_canonical_allowed(self):
        self.assert_allowed(
            "write_file",
            {"path": os.path.join(CANONICAL, "ev0_cli", "x.py")},
            msg="write into canonical repo must stay allowed",
        )


if __name__ == "__main__":
    unittest.main()