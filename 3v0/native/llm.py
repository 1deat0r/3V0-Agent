"""Native LLM client — direct Fireworks Chat Completions, no Hermes import.

Stdlib-only (urllib.request/json). Talks to the Fireworks API by itself, so
model access belongs to 3V0, not to whatever harness happens to run it.
"""
from __future__ import annotations

import json
import os
import urllib.error  # noqa: F401  (referenced explicitly for callers)
import urllib.request
from pathlib import Path

BASE_URL = os.environ.get(
    "THREEV0_FIREWORKS_URL", "https://api.fireworks.ai/inference/v1"
)
MODEL = os.environ.get(
    "THREEV0_MODEL", "accounts/fireworks/models/deepseek-v4-flash-0731"
)
_PROF_ENV = (
    Path(os.environ.get("HERMES_HOME") or "~/.hermes/profiles/3v0").expanduser()
) / ".env"


def api_key() -> str:
    """FIREWORKS_API_KEY from the process env, else the profile .env."""
    k = (os.environ.get("FIREWORKS_API_KEY") or "").strip()
    if k:
        return k
    if _PROF_ENV.is_file():
        for line in _PROF_ENV.read_text().splitlines():
            line = line.strip()
            if line.startswith("FIREWORKS_API_KEY="):
                v = line.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    raise RuntimeError("FIREWORKS_API_KEY not found (env or profile .env)")


def chat(
    messages,
    *,
    model: str | None = None,
    max_tokens: int = 512,
    temperature: float = 0.7,
    timeout: int = 60,
) -> str:
    """A single chat completion. Returns the assistant message text."""
    body = {
        "model": model or MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            # Cloudflare 1010-blocks urllib's default "Python-urllib/3.x" UA.
            "User-Agent": "3V0-native-runtime/0.1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    # Round-trip proof: a real completion from the model, no Hermes involved.
    out = chat(
        [
            {
                "role": "system",
                "content": "You are 3V0. Reply with exactly two words: NATIVE_3V0_OK",
            },
            {"role": "user", "content": "do it"},
        ],
        max_tokens=256,  # flash is a reasoning model; small budgets return empty content
    )
    print("NATIVE_LLM_OK ->", repr(out.strip()))
