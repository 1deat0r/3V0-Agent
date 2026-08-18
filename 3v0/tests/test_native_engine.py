"""Deterministic tests for the native engine handler (LLM/tools/send mocked)."""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from native import agent, engine, tools  # noqa: E402


def _up(chat=123, text="hi"):
    return {"update_id": 1, "message": {"message_id": 1, "chat": {"id": chat}, "text": text}}


class GateTest(unittest.TestCase):
    def test_allows_explicit_user(self):
        with mock.patch.object(engine, "allowed_user_ids", return_value=[123]):
            self.assertTrue(engine.is_allowed(_up(123)))
            self.assertFalse(engine.is_allowed(_up(999)))

    def test_denies_unknown_when_restricted(self):
        sent = []

        def send(cid, txt):
            sent.append((cid, txt))

        with mock.patch.object(engine, "allowed_user_ids", return_value=[123]):
            engine.handler(_up(999, "tools"), send)
        self.assertEqual(sent, [(999, "unauthorized")])


class SystemCommandTest(unittest.TestCase):
    def test_tools_list(self):
        out = engine.system_command("tools")
        self.assertIn("read_file", out)
        self.assertIn("run_script", out)

    def test_exec_runs_via_registry(self):
        with mock.patch.object(tools, "execute", return_value={"exit_code": 0, "stdout": "gate ok"}):
            out = engine.system_command("exec verify.sh")
        self.assertIn("exit=0", out)
        self.assertIn("gate ok", out)

    def test_benign_text_not_a_command(self):
        self.assertIsNone(engine.system_command("hello world"))


class HandlerTest(unittest.TestCase):
    def test_normal_text_routes_to_agent(self):
        sent = []

        def send(cid, txt):
            sent.append((cid, txt))

        with mock.patch.object(engine, "allowed_user_ids", return_value=[123]), mock.patch.object(
            agent, "respond", return_value="HELLO_REPLY"
        ), mock.patch.object(agent, "default_context", return_value="CTX"):
            engine.handler(_up(123, "hello"), send)
        self.assertEqual(sent, [(123, "HELLO_REPLY")])

    def test_empty_text_gets_question(self):
        sent = []
        with mock.patch.object(engine, "allowed_user_ids", return_value=[123]):
            engine.handler(_up(123, ""), lambda c, t: sent.append((c, t)))
        self.assertEqual(sent, [(123, "?")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
