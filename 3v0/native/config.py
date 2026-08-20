"""Native config seam — ONE place the runtime resolves env.

Process env first, profile `.env` second (the precedence the old code re-implemented
inconsistently across llm.py / gateway.py / engine.py). Small interface, memoized
parse, dotenv-lite format: bare or `export ` NAME=value, optional inline ` # comment`,
quote stripping. Stdlib-only, zero 3V0.

Interface: get(name, default=None) / require(name) / load(env_file=None) / clear_cache().
"""
from __future__ import annotations

import os
import re
from pathlib import Path

_PROFILE = Path(os.environ.get("EV0_HOME") or "~/.3V0/profiles/3v0").expanduser()
_DEFAULT_ENV_FILE = _PROFILE / ".env"

_cache: dict[str, str] = {}
_cached_path: str | None = None
_loaded: bool = False

# strip inline comments only when a `#` is preceded by whitespace (so a token value
# like `name=abc#def` survives; `name=abc # note` drops the note).
_INLINE_COMMENT = re.compile(r"\s+#.*$")


def _parse(text: str) -> dict[str, str]:
    """Dotenv-lite parser: returns {NAME: value}. Pure, testable."""
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        line = _INLINE_COMMENT.sub("", line).rstrip()
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k:
            out[k] = v
    return out


def load(env_file: str | Path | None = None) -> dict[str, str]:
    """Parse and memoize the env file. Returns the loaded {NAME: value} map.

    Pass env_file to point at a non-default path (tests use a temp file). Memoized
    until clear_cache()/a different path is requested — the runtime reloads on restart."""
    global _cache, _cached_path, _loaded
    path = str(env_file) if env_file is not None else str(_DEFAULT_ENV_FILE)
    if _loaded and _cached_path == path:
        return _cache
    data: dict[str, str] = {}
    p = Path(path)
    if p.is_file():
        data = _parse(p.read_text())
    _cache, _cached_path, _loaded = data, path, True
    return data


def get(name: str, default: str | None = None,
        env_file: str | Path | None = None) -> str | None:
    """Value for `name`: process env (non-empty) wins, else the loaded `.env`, else default."""
    v = os.environ.get(name)
    if v is not None and v.strip() != "":
        return v.strip()
    v = load(env_file).get(name)
    if v is not None and v != "":
        return v
    return default


def require(name: str, env_file: str | Path | None = None) -> str:
    """get() but raise RuntimeError when the value is absent — for critical secrets."""
    v = get(name, None, env_file)
    if v is None:
        raise RuntimeError(f"{name} not found (env or profile .env)")
    return v


def clear_cache() -> None:
    """Drop the memoized parse (for tests or secret rotation in a long-lived process)."""
    global _cache, _cached_path, _loaded
    _cache, _cached_path, _loaded = {}, None, False
