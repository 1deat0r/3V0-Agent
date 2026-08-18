"""Deterministic tests for the native Telegram gateway (network mocked)."""
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from native import gateway as gw  # noqa: E402


def _fake_resp(body):
    class R:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps(body).encode()

    return R()


class ApiTest(unittest.TestCase):
    def test_token_resolves_nonempty_without_leaking(self):
        t = gw.token()
        self.assertIsInstance(t, str)
        self.assertTrue(len(t) >= 30)

    def test_api_posts_with_ua_and_returns_result(self):
        captured = {}

        def fake_urlopen(req, timeout=30):
            captured["req"] = req
            captured["timeout"] = timeout
            return _fake_resp({"ok": True, "result": {"x": 1}})

        with mock.patch.object(gw.urllib.request, "urlopen", side_effect=fake_urlopen):
            out = gw._api("getMe")
        self.assertEqual(out, {"x": 1})
        req = captured["req"]
        self.assertTrue(req.full_url.startswith(gw.API + "/bot"))
        self.assertTrue(req.full_url.endswith("/getMe"))
        self.assertEqual(req.get_method(), "POST")
        self.assertNotEqual(req.headers.get("User-Agent"), "")

    def test_api_raises_on_not_ok(self):
        with mock.patch.object(
            gw.urllib.request, "urlopen", return_value=_fake_resp({"ok": False})
        ):
            with self.assertRaises(RuntimeError):
                gw._api("getMe")


class UpdatesTest(unittest.TestCase):
    def test_get_updates_passes_offset_and_allowed(self):
        seen = {}

        def fake_urlopen(req, timeout=30):
            seen["url"] = req.full_url
            seen["method"] = req.get_method()
            body = json.loads(req.data.decode())
            seen["timeout_param"] = body.get("timeout")
            seen["allowed"] = body.get("allowed_updates")
            seen["offset"] = body.get("offset")
            return _fake_resp({"ok": True, "result": [{"update_id": 9}]})

        with mock.patch.object(gw, "token", return_value="t" * 40), mock.patch.object(
            gw.urllib.request, "urlopen", side_effect=fake_urlopen
        ):
            out = gw.get_updates(offset=5, long_poll=20)
        self.assertEqual(out, [{"update_id": 9}])
        self.assertEqual(seen["method"], "POST")
        self.assertEqual(seen["timeout_param"], 20)
        self.assertEqual(seen["allowed"], ["message"])
        self.assertEqual(seen["offset"], 5)


class SendTest(unittest.TestCase):
    def test_send_message_posts_chat_and_text(self):
        seen = {}

        def fake_urlopen(req, timeout=30):
            seen["body"] = json.loads(req.data.decode())
            return _fake_resp({"ok": True, "result": {}})

        with mock.patch.object(gw, "token", return_value="t" * 40), mock.patch.object(
            gw.urllib.request, "urlopen", side_effect=fake_urlopen
        ):
            gw.send_message(123, "hello")
        self.assertEqual(seen["body"]["chat_id"], 123)
        self.assertEqual(seen["body"]["text"], "hello")

    def test_send_message_skips_empty(self):
        self.assertEqual(gw.send_message(1, ""), {})


class RunForeverTest(unittest.TestCase):
    def test_delivers_update_to_handler_and_replies(self):
        batches = [
            [{"update_id": 5, "message": {"message_id": 1, "chat": {"id": 999}, "text": "hi"}}],
            [],
        ]
        seen = {"handler": [], "sent": []}

        def fake_updates(offset=None, long_poll=25):
            return batches.pop(0) if batches else [999]  # sentinel never reached

        def fake_send(cid, txt):
            seen["sent"].append((cid, txt))

        def handler(up, send):
            seen["handler"].append(up)
            send(up["message"]["chat"]["id"], "reply here")

        with mock.patch.object(gw, "get_updates", side_effect=fake_updates), mock.patch.object(
            gw, "send_message", side_effect=fake_send
        ), mock.patch.object(gw.time, "sleep", side_effect=StopIteration):
            with self.assertRaises(StopIteration):  # bounds the infinite loop
                gw.run_forever(handler)

        self.assertEqual(len(seen["handler"]), 1)
        self.assertEqual(seen["handler"][0]["update_id"], 5)
        self.assertEqual(seen["sent"], [(999, "reply here")])

    def test_handler_error_is_reported_and_notifies_chat(self):
        batches = [[{"update_id": 9, "message": {"message_id": 2, "chat": {"id": 55}, "text": "boom"}}]]
        errors, sent = [], []

        def fake_updates(offset=None, long_poll=25):
            return batches.pop(0) if batches else [999]

        def fake_send(cid, txt):
            sent.append((cid, txt))

        def on_error(e, up):
            errors.append((type(e).__name__, up.get("update_id")))

        def handler(up, send):
            raise RuntimeError("kaboom")

        with mock.patch.object(gw, "get_updates", side_effect=fake_updates), mock.patch.object(
            gw, "send_message", side_effect=fake_send
        ), mock.patch.object(gw.time, "sleep", side_effect=StopIteration):
            with self.assertRaises(StopIteration):
                gw.run_forever(handler, on_error=on_error)

        self.assertEqual(errors, [("RuntimeError", 9)])  # reported, not masked
        self.assertTrue(any(cid == 55 and txt.startswith("⚠️") for cid, txt in sent),
                        "error notice should reach the originating chat")

    def test_handler_error_without_chat_does_not_send(self):
        batches = [[{"update_id": 11, "message": {"message_id": 3}}]]  # no chat
        errors, sent = [], []
        seen_handler = []

        def fake_updates(offset=None, long_poll=25):
            return batches.pop(0) if batches else [999]

        def fake_send(cid, txt):
            sent.append((cid, txt))

        def handler(up, send):
            seen_handler.append(up)
            raise ValueError("no chat")

        with mock.patch.object(gw, "get_updates", side_effect=fake_updates), mock.patch.object(
            gw, "send_message", side_effect=fake_send
        ), mock.patch.object(gw.time, "sleep", side_effect=StopIteration):
            with self.assertRaises(StopIteration):
                gw.run_forever(handler)

        self.assertEqual(errors, [])
        self.assertEqual(len(seen_handler), 1)  # handler was reached, then raised
        self.assertEqual(seen_handler[0], {"update_id": 11, "message": {"message_id": 3}})
        self.assertEqual(sent, [])  # no chat to notify -> nothing attempted


if __name__ == "__main__":
    unittest.main(verbosity=2)
