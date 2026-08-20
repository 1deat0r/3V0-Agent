"""Native LLM client — direct chat completions, no 3V0 import.

Stdlib-only (urllib.request/json). Provider-agnostic: the endpoint, auth key
and model come from the named-provider registry (native.providers), so 3V0 can
hold several providers connected simultaneously and route a call to any of
them. Defaults to the ``aux`` provider (Fireworks deepseek-v4-flash) exactly as
it did before the registry — passing ``provider="main"`` routes to the primary
substrate (bitdeer), etc. Model access belongs to 3V0, not to whatever harness
happens to run it.
"""
from __future__ import annotations

import json
import urllib.error  # noqa: F401  (referenced explicitly for callers)
import urllib.request

try:
    from native import providers            # normal: import native.llm
except ImportError:
    import providers                        # direct execution: python3 native/llm.py

_current = providers.resolve("aux")
BASE_URL = _current.base_url
MODEL = _current.model


def api_key() -> str:
    """API key for the default (aux) provider, via the config seam."""
    return _current.api_key()


def chat(
    messages,
    *,
    model: str | None = None,
    provider: str | None = None,
    max_tokens: int = 512,
    temperature: float = 0.7,
    timeout: int = 60,
) -> str:
    """A single chat completion. Returns the assistant message text.

    ``provider`` selects which connected provider to route to (e.g. "main" for
    the primary substrate); ``model`` overrides that provider's default model.
    Both default to the aux provider / its model, preserving prior behaviour.
    """
    p = providers.resolve(provider) if provider is not None else _current
    body = {
        "model": model or p.model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    req = urllib.request.Request(
        f"{p.base_url}/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {p.api_key()}",
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
    # Round-trip proof: a real completion from the model, no 3V0 involved.
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