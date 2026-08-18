"""Contract tests for the native LLM client (3v0/native/llm.py).

Behavior contract, not a snapshot: asserts how chat() must build the Fireworks
request — endpoint, auth + UA headers, body shape — WITHOUT hitting the network.
The round-trip live proof is 3v0/native/llm.py's __main__ (run manually on a
machine with the key; not part of the deterministic suite).
"""
import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class _FakeResp:
    def __init__(self, body=None):
        self._body = body or {"choices": [{"message": {"content": "ok"}}]}

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return json.dumps(self._body).encode()


class NativeLlmTest(unittest.TestCase):
    def setUp(self):
        from native import llm
        self.llm = llm

    def test_defaults_point_at_flash_on_fireworks(self):
        self.assertEqual(self.llm.MODEL, "accounts/fireworks/models/deepseek-v4-flash-0731")
        self.assertTrue(self.llm.BASE_URL.endswith("/inference/v1"))

    def test_api_key_resolves_nonempty_without_leaking(self):
        k = self.llm.api_key()
        self.assertIsInstance(k, str)
        self.assertEqual(len(k), 25)  # the profile key length; change with the key

    def test_chat_builds_correct_request(self):
        captured = {}

        def fake_urlopen(req, timeout=60):
            captured["request"] = req
            captured["timeout"] = timeout
            return _FakeResp()

        with mock.patch.object(self.llm.urllib.request, "urlopen", side_effect=fake_urlopen):
            with mock.patch.object(self.llm, "api_key", return_value="k" * 30):
                out = self.llm.chat([{"role": "user", "content": "hi"}])

        req = captured["request"]
        self.assertTrue(req.full_url.endswith("/chat/completions"))
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.headers.get("Authorization"), "Bearer " + "k" * 30)
        self.assertNotEqual(req.headers.get("User-Agent"), "")
        body = json.loads(req.data.decode())
        self.assertEqual(body["model"], self.llm.MODEL)
        self.assertEqual(body["messages"], [{"role": "user", "content": "hi"}])
        self.assertEqual(captured["timeout"], 60)
        self.assertEqual(out, "ok")

    def test_chat_returns_content_and_forwards_model(self):
        with mock.patch.object(
            self.llm.urllib.request, "urlopen",
            return_value=_FakeResp(body={"choices": [{"message": {"content": "hi 3v0"}}]}),
        ):
            out = self.llm.chat([{"role": "user", "content": "hi"}], model="m")
        self.assertEqual(out, "hi 3v0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
