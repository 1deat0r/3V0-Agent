"""Provider registry — the model-agnostic / multi-provider seam.

3V0 must be model-agnostic and able to hold several providers connected
simultaneously, routing tasks across them by deliberate choice — the
architecture that makes the prime directive's "LLM substrate is mine to
choose" real. That means provider+model resolve ONCE here from config/env and
no module hard-codes a substrate as if it were identity.

Each named provider is a frozen ``Provider`` (base_url + api key name + model
+ optional embedding dims). Values layer: process env > profile `.env` >
built-in default, all through the single ``native.config`` seam. Enable more
providers / swap substrates by setting env keys — no code change.

Built-ins:
  * main   — the primary substrate (bitdeer DeepSeek-V4-Flash today)
  * aux    — cheap auxiliary tasks (Fireworks deepseek-v4-flash today)
  * embed  — embedding model (bitdeer BAAI/bge-m3, 1024-d today)
Resolve-time secrets (API keys) are read lazily via ``Provider.api_key()`` so
importing this module never touches the network or a secret.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import cast as _tcast

try:
    from native import config          # normal: import native.providers
except ImportError:
    import config                      # direct execution: python3 native/providers.py


@dataclass(frozen=True)
class Provider:
    """A named connected provider. ``api_key()`` resolves the secret lazily."""
    name: str
    base_url: str
    api_key_name: str
    model: str
    dims: int | None = None

    def api_key(self) -> str:
        return config.require(self.api_key_name)


# Built-in defaults. These are 3V0's CURRENT deliberate substrate choices,
# overridable via env — not identity, just where the arrows point today.
_BUILTINS: dict[str, Provider] = {
    "main": Provider("main",
                     "https://api-inference.bitdeer.ai/v1",
                     "BITDEER_API_KEY",
                     "deepseek-ai/DeepSeek-V4-Flash"),
    "aux": Provider("aux",
                    "https://api.fireworks.ai/inference/v1",
                    "FIREWORKS_API_KEY",
                    "accounts/fireworks/models/deepseek-v4-flash-0731"),
    "embed": Provider("embed",
                      "https://api-inference.bitdeer.ai/v1",
                      "BITDEER_API_KEY",
                      "BAAI/bge-m3",
                      dims=1024),
}

# env-key -> field for layering overrides onto each built-in.
_CONFIG: dict[str, tuple[tuple[str, str], ...]] = {
    "main": (("THREEV0_MAIN_URL", "base_url"),
             ("THREEV0_MAIN_MODEL", "model"),
             ("THREEV0_MAIN_KEY", "api_key_name")),
    "aux": (("THREEV0_AUX_URL", "base_url"),
            ("THREEV0_AUX_MODEL", "model"),
            ("THREEV0_AUX_KEY", "api_key_name")),
    "embed": (("THREEV0_EMBED_URL", "base_url"),
              ("THREEV0_EMBED_MODEL", "model"),
              ("THREEV0_EMBED_KEY", "api_key_name"),
              ("THREEV0_EMBED_DIM", "dims")),
}


def names() -> list[str]:
    return list(_BUILTINS)


def resolve(name: str) -> Provider:
    """Resolve provider ``name``, layering config/env over its built-in default.

    ``config.get(envkey, base)`` gives precedence: process env > profile .env
    > built-in, so swapping a provider is a config change, never a code edit.
    Raises KeyError for an unknown name (a config typo must fail loudly).
    """
    base = _BUILTINS[name]
    overrides: dict[str, object] = {}
    for envkey, field in _CONFIG[name]:
        value = config.get(envkey, None)
        if value is not None:
            overrides[field] = _tcast(int, int(value)) if field == "dims" else value
    return replace(base, **overrides) if overrides else base


if __name__ == "__main__":
    # Round-trip proof, no secrets touched.
    for n in names():
        p = resolve(n)
        print(f"{n:6s} url={p.base_url} model={p.model}"
              f"{(' dims='+str(p.dims)) if p.dims else ''}")