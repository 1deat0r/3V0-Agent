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

The same plugin also registers two first-class tools over the native stores
(direction 3 — 3V0's own capabilities):

- ``threev0_store`` — the read half: a read-only query tool that shells out to
  ``scripts/query.py`` and returns the store's canonical view (supersession
  history and curator states) the derived profile projection hides.
- ``threev0_record`` — the write half: a store-first decision actuator that
  shells out to ``scripts/record.py`` (record a fact, optionally superseding
  an old one, or retract one by id), then re-exports the profile projection.
  Unlike the best-effort write *mirror* above, this is a direct actuator —
  a refusal surfaces as a JSON error the agent can see and correct.

The plugin's third surface is 3V0's own review *process* (direction 3's
driver, Stone 7): an ``on_session_end`` hook spawns the detached
``scripts/review_session.py`` driver, which reviews the just-ended session
against the canonical store and makes store-first decisions
(record/supersede/retract) via the DeepSeek API. Detached so it survives
gateway teardown (a TUI quit kills the process — a thread would die with it).

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
# on_session_end -> 3V0-owned session-end review (Stone 7)
# ---------------------------------------------------------------------------

_warned_missing_review_driver = False


def _on_session_end(
    session_id: str = "",
    **_: Any,
) -> None:
    """Spawn the 3V0-owned session-end review driver as a detached subprocess.

    Best-effort by construction: a detached process (not a thread) so the
    review survives gateway teardown — in TUI use, session end usually means
    the gateway process exits, and a thread would die with it. The driver
    applies its own gates (reviewable source, min messages, dedupe,
    cooldown) and any failure degrades to a log entry. Never blocks teardown.
    """
    global _warned_missing_review_driver, _warned_missing_body

    if os.environ.get("THREEV0_REVIEW") == "0":
        return
    if not session_id:
        return

    body_root = _resolve_body_root()
    if body_root is None:
        if not _warned_missing_body:
            _warned_missing_body = True
            logger.warning(
                "native-store-bridge: cannot locate 3V0 body repo "
                "(set THREEV0_BODY or write %s) — session-end review skipped",
                _profile_home() / "3v0_body_path",
            )
        return

    driver = _script_path(body_root, "review_session.py")
    if not driver.exists():
        if not _warned_missing_review_driver:
            _warned_missing_review_driver = True
            logger.warning(
                "native-store-bridge: review_session.py not found at %s — "
                "session-end review skipped",
                driver,
            )
        return

    env = os.environ.copy()
    env.setdefault("THREEV0_PROFILE_HOME", str(_profile_home()))
    if os.environ.get("THREEV0_BODY"):
        env.setdefault("THREEV0_BODY", os.environ["THREEV0_BODY"])
    else:
        env.setdefault("THREEV0_BODY", str(body_root))
    try:
        subprocess.Popen(
            [sys.executable, str(driver), "--session-id", str(session_id)],
            env=env,
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        pass


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


# ---------------------------------------------------------------------------
# threev0_record — store-first write tool over the memory store
# ---------------------------------------------------------------------------

_THREEV0_RECORD_SCHEMA = {
    "name": "threev0_record",
    "description": (
        "Write to 3V0's native memory store — the store-first decision "
        "actuator (the write half of 3V0's own evolution loop). Record a new "
        "fact, optionally superseding an old one (flagged and recoverable, "
        "never erased), or retract one by id. The store is the canonical "
        "origin; the Hermes profile (MEMORY.md/USER.md) is re-exported as a "
        "derived view after the write. Use threev0_store to read the store "
        "first (e.g. to find a fact_id to supersede or retract). Corrections "
        "go here, not through the Hermes memory tool, so supersession is "
        "recorded instead of silently overwritten."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["record", "retract"],
                "description": (
                    "record: add a fact, optionally superseding an old one. "
                    "retract: remove an active fact by id (recoverable, no "
                    "successor)."
                ),
            },
            "kind": {
                "type": "string",
                "enum": ["memory", "user", "identity", "directive"],
                "description": (
                    "With action='record' (required): the fact's kind. "
                    "identity/directive are store-only (not projected to the "
                    "profile)."
                ),
            },
            "content": {
                "type": "string",
                "description": (
                    "With action='record' (required): the new fact text."
                ),
            },
            "fact_id": {
                "type": "string",
                "description": (
                    "With action='retract' (required): the fact id to remove. "
                    "With action='record' (optional): supersede the fact with "
                    "this exact id."
                ),
            },
            "supersedes": {
                "type": "string",
                "description": (
                    "With action='record' (optional): supersede the active "
                    "fact whose content contains this substring (must match "
                    "exactly one)."
                ),
            },
            "source": {
                "type": "string",
                "description": "Optional provenance label (default 'foreground').",
            },
        },
        "required": ["action"],
    },
}


def _handle_store_record(args=None, **_) -> str:
    """Serve a store-first write by shelling out to scripts/record.py (JSON).

    Unlike the best-effort write mirror (post_tool_call, failures swallowed),
    this is a direct actuator: the agent asked to write, so a refusal or a
    failed subprocess surfaces as a JSON error object it can see and correct.
    """
    global _warned_missing_body

    body_root = _resolve_body_root()
    if body_root is None:
        return json.dumps({
            "error": (
                "3V0 body repo not found — cannot write the native store. "
                "Set THREEV0_BODY or write the body-path marker."
            ),
        })

    script = _script_path(body_root, "record.py")
    if not script.exists():
        return json.dumps({"error": f"record.py not found at {script}"})

    a = args or {}
    action = str(a.get("action", "")).strip()
    if action not in {"record", "retract"}:
        return json.dumps({"error": f"unknown action {action!r}"})

    argv = [sys.executable, str(script), "--json", "--write"]
    if action == "retract":
        fact_id = str(a.get("fact_id", "")).strip()
        if not fact_id:
            return json.dumps({"error": "fact_id is required for action='retract'"})
        argv += ["--retract", fact_id]
    else:
        kind = str(a.get("kind", "")).strip()
        content = str(a.get("content", "")).strip()
        if not kind or not content:
            return json.dumps({
                "error": "kind and content are required for action='record'",
            })
        argv += ["--kind", kind, "--content", content]
        if a.get("fact_id"):
            argv += ["--supersedes-id", str(a["fact_id"])]
        if a.get("supersedes"):
            argv += ["--supersedes", str(a["supersedes"])]

    if a.get("source"):
        argv += ["--source", str(a["source"])]

    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    except Exception as e:  # noqa: BLE001 - write path must still return something
        return json.dumps({"error": f"store record failed: {e}"})

    if proc.returncode != 0:
        # record.py prints a JSON refusal to stdout on a clean error; fall
        # back to stderr only when stdout is empty (a crash, not a refusal).
        out = (proc.stdout or "").strip()
        if out:
            return out
        return json.dumps({
            "error": "store record error",
            "stderr": (proc.stderr or "").strip(),
        })
    return proc.stdout or "{}"


def register(ctx) -> None:
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    ctx.register_hook("on_session_end", _on_session_end)
    ctx.register_tool(
        name="threev0_store",
        toolset="3v0",
        schema=_THREEV0_STORE_SCHEMA,
        handler=_handle_store_query,
    )
    ctx.register_tool(
        name="threev0_record",
        toolset="3v0",
        schema=_THREEV0_RECORD_SCHEMA,
        handler=_handle_store_record,
    )
