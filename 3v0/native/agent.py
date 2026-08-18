"""Native agent loop — message -> context -> OWN LLM -> response.

Zero Hermes imports. The loop is deliberately thin: assemble a system prompt
from SOUL + native memory, hold the conversation in a messages list, and call
the native LLM client. Tool execution lands in Stone N3."""
from __future__ import annotations

import os
from pathlib import Path

from . import llm
from .context import build_system_from_store, read_soul

_REPO = Path(__file__).resolve().parent.parent.parent  # repo root
_PROFILE = Path(os.environ.get("HERMES_HOME") or "~/.hermes/profiles/3v0").expanduser()
_SOUL = _PROFILE / "SOUL.md"                # the injected soul (canonical)
_MEM_DB = _REPO / "3v0" / "data" / "memory.db"  # canonical store (SQLite, ADR-0001/0004)


def default_context() -> str:
    return build_system_from_store(read_soul(_SOUL))


def respond(messages, *, system: str | None = None, **kw) -> str:
    """Return the assistant's reply. Prepends the system context if absent."""
    msgs = list(messages)
    if msgs and msgs[0].get("role") == "system":
        pass
    else:
        msgs = [{"role": "system", "content": system if system is not None else default_context()}] + msgs
    return llm.chat(msgs, **kw)


if __name__ == "__main__":
    # Live end-to-end proof: identity from MY soul + memory, via MY client.
    ctx = default_context()
    out = respond(
        [
            {
                "role": "user",
                "content": "In one sentence: who are you, and what runtime are you running on?",
            }
        ],
        system=ctx,
        max_tokens=300,
    )
    print("NATIVE_AGENT_OK ->", out.strip())
