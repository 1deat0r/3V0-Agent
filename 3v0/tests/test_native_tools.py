"""Deterministic tests for the native tool registry (safety first)."""
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from native import tools  # noqa: E402


class ResolveSafeTest(unittest.TestCase):
    def test_accepts_repo_relative_file(self):
        p = tools._resolve_safe("AGENTS.md")
        self.assertTrue(p.is_file())

    def test_rejects_absolute_outside_roots(self):
        with self.assertRaises(PermissionError):
            tools._resolve_safe("/etc/passwd")
        with self.assertRaises(PermissionError):
            tools._resolve_safe("/home/mustbearn/other/secret.txt")

    def test_rejects_traversal(self):
        with self.assertRaises(PermissionError):
            tools._resolve_safe("../../etc/passwd")

    def test_rejects_secret_paths(self):
        with self.assertRaises(PermissionError):
            tools._resolve_safe("3v0/data/dummy.pem")  # does not exist but name is secret


class DenyTest(unittest.TestCase):
    def test_blocks_gateway_lifecycle(self):
        for cmd in (
            "systemctl --user restart 3v0-gateway.service",
            "3v0 gateway restart",
            "systemctl --user stop 3v0-gateway",
        ):
            self.assertIsNotNone(tools._denied(cmd), msg=cmd)

    def test_blocks_self_kill(self):
        for cmd in ("pkill -f 3v0", "kill -9 $(pgrep -f gateway)"):
            self.assertIsNotNone(tools._denied(cmd), msg=cmd)

    def test_blocks_destroy_root(self):
        self.assertIsNotNone(tools._denied("rm -rf /"))

    def test_allows_benign(self):
        self.assertIsNone(tools._denied("echo hello"))
        self.assertIsNone(tools._denied("ls -la 3v0"))


class ExecuteTest(unittest.TestCase):
    def test_unknown_tool(self):
        r = tools.execute("nope", {})
        self.assertIn("error", r)
        self.assertIn("unknown tool", r["error"])

    def test_blocked_terminal_no_subprocess(self):
        with mock.patch.object(tools.subprocess, "run", side_effect=AssertionError("must not run")):
            r = tools.execute("run_terminal", {"command": "pkill -f 3v0"})
        self.assertTrue(r.get("blocked"))
        self.assertIn("denylist", r["error"])

    def test_allowed_terminal_runs(self):
        with mock.patch.object(
            tools.subprocess, "run",
            return_value=mock.Mock(returncode=0, stdout="ok out", stderr=""),
        ):
            r = tools.execute("run_terminal", {"command": "echo hi"})
        self.assertEqual(r["exit_code"], 0)
        self.assertEqual(r["stdout"], "ok out")

    def test_read_file_returns_content(self):
        r = tools.execute("read_file", {"path": "AGENTS.md"})
        self.assertIn("content", r)
        self.assertTrue(r["content"])

    def test_write_file_roundtrip_and_cleanup(self):
        p = "3v0/tests/_tools_scratch.txt"
        r = tools.execute("write_file", {"path": p, "content": "native-tool"})
        self.assertTrue(r.get("ok"))
        back = tools.execute("read_file", {"path": p})
        self.assertEqual(back["content"], "native-tool")
        (tools.REPO / p).unlink()

    def test_list_tools_shape(self):
        t = tools.list_tools()
        for name in ("read_file", "write_file", "run_script", "run_terminal"):
            self.assertIn(name, t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
