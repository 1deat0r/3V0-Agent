"""Native engine — compose context + LLM + tools + gateway into one handler.

Stdlib-only, zero Hermes. N5: the piece that makes the native runtime a
complete agent over Telegram.

  handler(update, send)   -- the single entry point fed by gateway.run_forever.
      * allowed-user gate (TELEGRAM_ALLOWED_USERS)
      * deterministic commands: "tools" (list) and "exec <script> <args>" (run)
      * otherwise: context from SOUL+memory -> agent.respond (LLM) -> reply sent

  server() -- run_forever(handler), for the (future, deliberate) cutover.

SAFETY: server() is not started here. Starting a SECOND getUpdates poller on
the live bot while the Hermes gateway runs would steal this very conversation's
updates. The proof below is a one-shot: it captures what would be sent (no
Telegram POST, no polling).
"""
from __future__ import annotations

from . import agent, gateway, tools

_MAX_REPLY = 512


def allowed_user_ids() -> list[int]:
    raw = gateway._read_prof_env("TELEGRAM_ALLOWED_USERS") or ""
    return [int(p) for p in (x.strip() for x in raw.split(",")) if p.strip().isdigit()]


def is_allowed(update: dict) -> bool:
    chat_id = update.get("message", {}).get("chat", {}).get("id")
    ids = allowed_user_ids()
    return (not ids) or (chat_id in ids)


def system_command(text: str) -> str | None:
    """Deterministic, safe command handling (no shell, validated script names)."""
    t = (text or "").strip()
    if t == "tools":
        return "TOOLS: " + ", ".join(sorted(tools.list_tools()))
    if t.startswith("exec "):
        parts = t.split()
        if len(parts) < 2:
            return "usage: exec <script> [args...]"
        res = tools.execute("run_script", {"name": parts[1], "args": parts[2:]})
        if "error" in res:
            return f"ERROR {res['error']}"
        return f"exit={res.get('exit_code')}\n{res.get('stdout', '')}"
    return None


def handler(update: dict, send) -> None:
    msg = update.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    if chat_id is None:
        return
    if not is_allowed(update):
        send(chat_id, "unauthorized")
        return
    text = msg.get("text") or ""
    cmd = system_command(text)
    if cmd is not None:
        send(chat_id, cmd)
        return
    if not text.strip():
        send(chat_id, "?")
        return
    reply = agent.respond(
        [{"role": "user", "content": text}],
        system=agent.default_context(),
        max_tokens=_MAX_REPLY,
    )
    send(chat_id, reply)


def server(long_poll: int = 25, idle: float = 1.0) -> None:
    gateway.run_forever(handler, long_poll=long_poll, idle=idle)


if __name__ == "__main__":
    # one-shot end-to-end proof: real LLM + context + tools, captured reply.
    # No Telegram POST, no polling -- safe alongside the live Hermes gateway.
    home = gateway._read_prof_env("TELEGRAM_HOME_CHANNEL")
    chat_id = int(home) if home and home.strip().isdigit() else 0
    captured = []
    fake = {
        "update_id": 1,
        "message": {"message_id": 1, "chat": {"id": chat_id}, "text": "Who are you?"},
    }
    handler(fake, lambda cid, txt: captured.append((cid, txt)))
    print("NATIVE_ENGINE_OK (would-send, NOT posted):")
    for cid, txt in captured:
        print(f"  -> chat {cid}: {txt.strip()[:200]}")
