"""native-store-bridge — mirror the Hermes memory + skill tools into 3V0's native stores.

A ``post_tool_call`` observer. Every time the ``memory`` or ``skill_manage``
tool performs a successful write (foreground, background review fork, gateway,
cron), this plugin replays the same operation against the matching native store
in ``<body>/3v0/data/``:

- ``memory``       -> ``data/memory.json``  (facts; canonical, profile is a projection)
- ``skill_manage`` -> ``data/skills.json``  (skill lineage; store canonical over SKILL.md)

so the stores stay the auditable record of 3V0's own evolution and the profile
remains a derived / operational view.

This is the store-first half of 3V0's own evolution loop (see
``3v0/EVOLUTION_LOOP.md``). It is best-effort by construction: any failure is
swallowed and the wake-time reconcilers ``sync.py --write`` (memory) and
``sync_skills.py --write`` (skills) are the backstop.

The same plugin also registers ``threev0_store``, a read-only query tool over
the native stores (the read half of direction 3 — 3V0's own capabilities). It
shells out to ``scripts/query.py`` and returns the store's canonical view: the
supersession history and curator states the derived profile projection hides.

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

_warned_missing_body = False
_warned_missing_memory_ingest = False
_warned_missing_skill_ingest = False


def _profile_home() -> Path:
    """The active profile's home (HERMES_HOME), or the 3v0 profile path."""
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env)
    return Path.home() / ".hermes" / "profiles" / "3v0"


def _resolve_body_root() -> Optional[Path]:
    """Locate the body repo (source of the native stores + ingest scripts)."""
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


def _script_path(body_root: Path, name: str) -> Path:
    return body_root / "3v0" / "scripts" / name


def _write_origin() -> str:
    """The active write origin: 'background_review' on the fork (incl. the
    curator's review fork), else 'assistant_tool' (the foreground agent's
    origin, set by turn_context.py from agent._memory_write_origin)."""
    try:
        from tools.skill_provenance import get_current_write_origin

        return get_current_write_origin()
    except Exception:
        return "assistant_tool"


def _result_ok(result: Any) -> bool:
    """True when the tool reported a successful write (JSON with success:true)."""
    data: Any = result
    if isinstance(result, str):
        try:
            data = json.loads(result)
        except json.JSONDecodeError:
            return False
    return isinstance(data, dict) and bool(data.get("success"))


def _run_ingest(script: Path, payload: dict) -> None:
    """Run an ingest script as a best-effort subprocess; swallow every failure."""
    try:
        subprocess.run(
            [sys.executable, str(script)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=30,
        )
    except Exception as e:  # noqa: BLE001 - best-effort observer
        logger.debug("native-store-bridge ingest failed: %s", e)


# ---------------------------------------------------------------------------
# memory -> store
# ---------------------------------------------------------------------------

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


def _mirror_memory(args: Dict[str, Any], result: Any) -> None:
    global _warned_missing_body, _warned_missing_memory_ingest

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
        if not _warned_missing_body:
            _warned_missing_body = True
            logger.warning(
                "native-store-bridge: cannot locate 3V0 body repo "
                "(set THREEV0_BODY or write %s) — writes will not be "
                "mirrored to the stores; wake sync remains the backstop",
                _profile_home() / "3v0_body_path",
            )
        return

    ingest = _script_path(body_root, "ingest.py")
    if not ingest.exists():
        if not _warned_missing_memory_ingest:
            _warned_missing_memory_ingest = True
            logger.warning(
                "native-store-bridge: ingest.py not found at %s — memory "
                "writes will not be mirrored to the store",
                ingest,
            )
        return

    _run_ingest(ingest, {"target": target, "source": _write_origin(), "ops": ops})


# ---------------------------------------------------------------------------
# skill_manage -> skill store
# ---------------------------------------------------------------------------

def _mirror_skill(args: Dict[str, Any], result: Any) -> None:
    global _warned_missing_body, _warned_missing_skill_ingest

    if not isinstance(args, dict):
        return
    if not _result_ok(result):
        return
    name = (args.get("name") or "").strip()
    if not name:
        return

    body_root = _resolve_body_root()
    if body_root is None:
        if not _warned_missing_body:
            _warned_missing_body = True
            logger.warning(
                "native-store-bridge: cannot locate 3V0 body repo "
                "(set THREEV0_BODY or write %s) — writes will not be "
                "mirrored to the stores; wake sync remains the backstop",
                _profile_home() / "3v0_body_path",
            )
        return

    ingest = _script_path(body_root, "ingest_skills.py")
    if not ingest.exists():
        if not _warned_missing_skill_ingest:
            _warned_missing_skill_ingest = True
            logger.warning(
                "native-store-bridge: ingest_skills.py not found at %s — "
                "skill writes will not be mirrored to the store",
                ingest,
            )
        return

    _run_ingest(ingest, {"source": _write_origin(), "args": args})


def _on_post_tool_call(
    tool_name: str = "",
    args: Optional[Dict[str, Any]] = None,
    result: Any = None,
    **_: Any,
) -> None:
    if tool_name == "memory":
        _mirror_memory(args or {}, result)
    elif tool_name == "skill_manage":
        _mirror_skill(args or {}, result)


# ---------------------------------------------------------------------------
# threev0_store — read-only query tool over the native stores
# ---------------------------------------------------------------------------

_THREEV0_STORE_SCHEMA = {
    "name": "threev0_store",
    "description": (
        "Read 3V0's native stores — the canonical, lineage-bearing record of "
        "3V0's own memory and skill evolution, not the derived profile "
        "projection. Use it to see what was superseded and what replaced it "
        "(memory facts carry provenance + supersession history; skills carry "
        "version lineage + curator active/stale/archived state). Read-only."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["summary", "facts", "fact_history", "skills", "skill_history"],
                "description": (
                    "summary: overview of both stores. facts: active facts "
                    "(optionally filter by kind). fact_history: full "
                    "supersession lineage of one fact (needs fact_id). "
                    "skills: active skills with version, source, and curator "
                    "state (optionally filter by name). skill_history: full "
                    "version lineage of one skill (needs name)."
                ),
            },
            "kind": {
                "type": "string",
                "enum": ["memory", "user", "identity", "directive"],
                "description": "With action='facts': restrict to this fact kind.",
            },
            "fact_id": {
                "type": "string",
                "description": "With action='fact_history': the fact id to trace.",
            },
            "name": {
                "type": "string",
                "description": (
                    "With action='skill_history' (required) or 'skills' "
                    "(optional filter): the skill name."
                ),
            },
        },
        "required": ["action"],
    },
}


def _handle_store_query(args=None, **_) -> str:
    """Serve a read query by shelling out to scripts/query.py (JSON out).

    Unlike the write mirror (best-effort, failures swallowed), a read MUST
    return a useful result to the agent, so failures surface as a JSON error
    object rather than being dropped silently.
    """
    global _warned_missing_body

    body_root = _resolve_body_root()
    if body_root is None:
        return json.dumps({
            "error": (
                "3V0 body repo not found — cannot read the native stores. "
                "Set THREEV0_BODY or write the body-path marker."
            ),
        })

    query = _script_path(body_root, "query.py")
    if not query.exists():
        return json.dumps({"error": f"query.py not found at {query}"})

    a = args or {}
    argv = [sys.executable, str(query), "--action", str(a.get("action", ""))]
    if a.get("kind"):
        argv += ["--kind", str(a["kind"])]
    if a.get("fact_id"):
        argv += ["--fact-id", str(a["fact_id"])]
    if a.get("name"):
        argv += ["--name", str(a["name"])]

    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    except Exception as e:  # noqa: BLE001 - read path must still return something
        return json.dumps({"error": f"store query failed: {e}"})

    if proc.returncode != 0:
        return json.dumps({
            "error": "store query error",
            "stderr": (proc.stderr or "").strip(),
        })
    return proc.stdout or "{}"


def register(ctx) -> None:
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    ctx.register_tool(
        name="threev0_store",
        toolset="3v0",
        schema=_THREEV0_STORE_SCHEMA,
        handler=_handle_store_query,
    )
