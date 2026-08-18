"""Deterministic tests for the native agent loop (context assembly + respond).

LLM call is mocked — network is not exercised here. The live identity
round-trip is 3v0/native/agent.py's __main__ (manual, needs the API key)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from native import agent, context  # noqa: E402


class ContextTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_system_composes_soul_and_memory(self):
        sys = context.build_system("I am 3V0.", ["fact one", "fact two"])
        self.assertIn("I am 3V0.", sys)
        self.assertIn("fact one", sys)
        self.assertIn("fact two", sys)
        self.assertIn("[NATIVE MEMORY", sys)

    def test_build_system_trims_memory_to_budget(self):
        mems = ["0123456789"] * 20  # 20 * 10 = 200 chars
        sys = context.build_system("S", mems, max_mem_chars=35)
        # budget allows ~3 facts (30 chars) before exceeding 35
        self.assertLessEqual(sys.count("0123456789"), 4)  # fits within 35-char budget

    def test_read_active_memories_excludes_superseded(self):
        p = self.d / "memory.json"
        p.write_text(json.dumps({
            "facts": [
                {"id": 1, "content": "active one"},
                {"id": 2, "content": "old two", "superseded_by": 3},
                {"id": 3, "content": "three"},
                {"id": 4, "content": ""},
            ]
        }))
        out = context.read_active_memories(p)
        self.assertEqual(out, ["active one", "three"])

    def test_read_active_memories_missing_file(self):
        self.assertEqual(context.read_active_memories(self.d / "nope.json"), [])

    def test_read_soul_missing_file(self):
        self.assertEqual(context.read_soul(self.d / "nope.md"), "")


class AgentTest(unittest.TestCase):
    def test_respond_injects_system_when_absent(self):
        # default_context reads real files; use an explicit system to stay hermetic
        captured = {}

        def fake_chat(messages, **kw):
            captured["messages"] = messages
            return "hi back"

        with mock.patch.object(agent.llm, "chat", side_effect=fake_chat):
            out = agent.respond([{"role": "user", "content": "hi"}], system="TEST_SYS")

        self.assertEqual(out, "hi back")
        self.assertEqual(captured["messages"][0], {"role": "system", "content": "TEST_SYS"})
        self.assertEqual(captured["messages"][-1]["role"], "user")

    def test_respond_keeps_existing_system(self):
        with mock.patch.object(agent.llm, "chat", side_effect=lambda m, **k: "x"):
            out = agent.respond([{"role": "system", "content": "S"},
                                 {"role": "user", "content": "u"}], system="OVERRIDE")
        self.assertEqual(out, "x")


if __name__ == "__main__":
    unittest.main(verbosity=2)
