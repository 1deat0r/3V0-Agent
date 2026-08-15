"""native-store-bridge — mirror the Hermes memory tool into 3V0's native store.

A ``post_tool_call`` observer. Every time the ``memory`` tool performs a
successful write (foreground, background review fork, gateway, cron), this
plugin replays the same add/replace/remove operation against the native store
at ``<body>/3v0/data/memory.json``, so the store stays the canonical origin and
the profile MEMORY.md / USER.md remain a derived projection.

This is the store-first half of 3V0's own evolution loop (see
``3v0/EVOLUTION_LOOP.md``). It is best-effort by construction: any failure is
swallowed and the wake-time ``sync.py --write`` reconciles as the backstop.

No runtime core files are edited. The plugin lives in the profile
(``~/.hermes/profiles/3v0/plugins/``) and survives ``hermes update``.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Fallback when neither 3V0_BODY nor the profile marker file resolves.
BODY_DEFAULT = "/home/mustbearn/Projects/AI Agents/3V0 Agent"

_warned_missing = False


def _profile_home() -> Path:
    """The active profile's home (HERMES_HOME), or the 3v0 profile path."""
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env)
    return Path.home() / ".hermes" / "profiles" / "3v0"


def _resolve_body_root() -> Optional[Path]:
    """Locate the body repo (source of the native store + ingest.py)."""
    # 1. Explicit env override.
    env = os.environ.get("THREEV0_BODY")
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            return p
    # 2. Marker file written by the body repo's setup (durable across sessions).
    marker = _profile_home() / "3v0_body_path"
    try:
        if marker.exists():
            p = Path(marker.read_text(encoding="utf-8").strip()).expanduser()
            if p.is_dir():
                return p
    except OSError:
        pass
    # 3. Default.
    p = Path(BODY_DEFAULT).expanduser()
    return p if p.is_dir() else None


def _ingest_path(body_root: Path) -> Path:
    return body_root / "3v0" / "scripts" / "ingest.py"


def _write_origin() -> str:
    """The active write origin: 'background_review' on the fork, else 'assistant_tool'."""
    try:
        from tools.skill_provenance import get_current_write_origin

        return get_current_write_origin()
    except Exception:
        return "assistant_tool"


def _result_ok(result: Any) -> bool:
    """True when the memory tool reported a successful write."""
    data: Any = result
    if isinstance(result, str):
        try:
            data = json.loads(result)
        except json.JSONDecodeError:
            return False
    return isinstance(data, dict) and bool(data.get("success"))


def _ops_from_args(args: Dict[str, Any]) -> Optional[list]:
    """Extract the memory-tool operations (single-op or batch) from the args."""
    target = (args.get("target") or "memory")
    if target not in {"memory", "user"}:
        return None

    ops = args.get("operations")
    if isinstance(ops, list) and ops:
        return [
            {
                "action": (op or {}).get("action"),
                "content": (op or {}).get("content"),
                "old_text": (op or {}).get("old_text"),
            }
            for op in ops
            if isinstance(op, dict)
        ]

    action = args.get("action")
    if action not in {"add", "replace", "remove"}:
        return None
    return [{
        "action": action,
        "content": args.get("content"),
        "old_text": args.get("old_text"),
    }]


def _on_post_tool_call(
    tool_name: str = "",
    args: Optional[Dict[str, Any]] = None,
    result: Any = None,
    **_: Any,
) -> None:
    global _warned_missing

    if tool_name != "memory":
        return
    if not isinstance(args, dict):
        return
    if not _result_ok(result):
        return

    target = (args.get("target") or "memory")
    if target not in {"memory", "user"}:
        return
    ops = _ops_from_args(args)
    if not ops:
        return

    body_root = _resolve_body_root()
    if body_root is None:
        if not _warned_missing:
            _warned_missing = True
            logger.warning(
                "native-store-bridge: cannot locate 3V0 body repo "
                "(set THREEV0_BODY or write %s) — memory writes will not be "
                "mirrored to the store; wake sync remains the backstop",
                _profile_home() / "3v0_body_path",
            )
        return

    ingest = _ingest_path(body_root)
    if not ingest.exists():
        if not _warned_missing:
            _warned_missing = True
            logger.warning(
                "native-store-bridge: ingest.py not found at %s — memory "
                "writes will not be mirrored to the store",
                ingest,
            )
        return

    payload = json.dumps({
        "target": target,
        "source": _write_origin(),
        "ops": ops,
    })
    try:
        subprocess.run(
            [sys.executable, str(ingest)],
            input=payload,
            text=True,
            capture_output=True,
            timeout=30,
        )
    except Exception as e:  # noqa: BLE001 - best-effort observer
        logger.debug("native-store-bridge ingest failed: %s", e)


def register(ctx) -> None:
    ctx.register_hook("post_tool_call", _on_post_tool_call)
