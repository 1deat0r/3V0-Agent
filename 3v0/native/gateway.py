"""Native Telegram gateway — Bot API long-polling. Stdlib-only, zero Hermes.

N4: hermes-independent messaging. getUpdates (allowed_updates=['message'],
long-poll timeout) -> handler(update) -> send_message. The handler is a plain
callable, so the loop is testable without a live bot.

SAFETY: never run a SECOND poller on the live bot while the Hermes gateway is
active — two getUpdates consumers steal each other's messages. The live proof
uses getMe (identity; consumes nothing).
"""
from __future__ import annotations

import json
import time
import urllib.request
import urllib.error

try:
    from native import config          # normal: import native.gateway
except ImportError:
    import config                      # direct execution: python3 native/gateway.py

API = config.get("TELEGRAM_API", "https://api.telegram.org")
_UA = "3V0-native-gateway/0.1.0"


def token() -> str:
    return config.require("TELEGRAM_BOT_TOKEN")


def _api(method: str, params: dict | None = None, timeout: int = 30) -> dict:
    url = f"{API}/bot{token()}/{method}"
    body = json.dumps(params or {}).encode()
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": _UA},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"telegram {method} http {e.code}: {e.read().decode(errors='replace')[:200]}") from e
    if not data.get("ok"):
        raise RuntimeError(f"telegram {method} not ok: {data}")
    return data.get("result", {})


def get_me() -> dict:
    # safe identity probe -- consumes no updates, safe alongside a live poller
    return _api("getMe")


def get_updates(offset: int | None = None, long_poll: int = 25) -> list:
    params = {"timeout": long_poll, "allowed_updates": ["message"]}
    if offset:
        params["offset"] = offset
    res = _api("getUpdates", params, timeout=long_poll + 10)
    return res if isinstance(res, list) else []


def send_message(chat_id: int | str, text: str, timeout: int = 30) -> dict:
    if not text or not str(text).strip():
        return {}
    return _api("sendMessage", {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}, timeout=timeout)


def run_forever(handler, long_poll: int = 25, idle: float = 1.0) -> None:
    """Long-poll the bot and feed each message to handler(update, send).

    handler(update, send) -> may call send(chat_id, text). Returns nothing.
    Blocking. Catches transient errors and keeps polling.
    """
    offset: int | None = None
    while True:
        try:
            updates = get_updates(offset, long_poll)
        except Exception:
            time.sleep(idle)
            continue
        for up in updates:
            update_id = up.get("update_id")
            if update_id:
                offset = update_id + 1  # ack *after* handling increments below
            msg = up.get("message", {})
            if not msg:
                continue
            chat_id = msg.get("chat", {}).get("id")
            try:
                handler(up, lambda cid, txt: send_message(cid or chat_id, txt))
            except Exception:
                continue
        time.sleep(idle)  # pace the poll loop; keeps a hot-loop impossible


if __name__ == "__main__":
    # SAFE live proof (getMe consumes no updates; no second poller started).
    me = get_me()
    print("NATIVE_GATEWAY_OK -> getMe result fields:", sorted(k for k in me.keys()))
