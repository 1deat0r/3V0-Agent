"""Skill outcome capture — the read-feedback signal for skill curation.

Closes the skill-axis loop beyond "was it used": for each skill loaded in a
session (via ``skill_view``), the session-end review records whether it
*worked* (success) or was proved wrong/obsolete (failure), so the store's
usage ``meta`` carries an outcome axis the ranker/curator can weight.

Pure + deterministic (no I/O, no LLM):

- ``extract_loaded_skills(messages)`` — walk the session transcript's tool
  messages, pull every ``skill_view`` call in order, and return the resolved
  skill names (deduped, preserving first-load order). The tool result is a
  JSON string whose ``name`` field is the resolved name (qualified forms
  resolve to the canonical name); when absent, we fall back to the requested
  name.
- Outcome decisions are applied via ``mark_skill_outcome`` — the store side
  (under ``mutate()``), writing ``last_outcome``/``last_outcome_at``/
  ``outcome_source`` plus a bounded ``outcome_history`` onto the active head's
  ``meta``.

The outcome itself is measured by the review driver's model from the session
transcript (advisory, never self-judged) and passed in as ``outcomes`` — this
module stays independent of any grader.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

VALID_OUTCOMES = {"success", "failure", "unknown"}
_RESERVED = {"last_outcome", "last_outcome_at", "outcome_source", "outcome_history"}

# Bounded outcome-history length kept on the active head.
_MAX_OUTCOME_HISTORY = 12


def extract_loaded_skills(messages: List[Dict[str, Any]]) -> List[str]:
    """Ordered, deduped skill names loaded this session via ``skill_view``.

    Each ``skill_view`` message's ``content`` is a JSON tool result. The
    resolved ``name`` field wins (a qualified/aliased query resolves to the
    canonical name); otherwise the tool-call ``name`` argument — parsed from
    the message's ``tool_calls`` when available, else the msg text — is used.
    Malformed/missing entries are skipped. Repeated loads coalesce to the
    first occurrence.
    """
    loaded: List[str] = []
    seen: set = set()

    for msg in messages:
        if not isinstance(msg, dict):
            continue
        if msg.get("tool_name") != "skill_view":
            continue

        name = _resolved_name(msg)
        if not name:
            continue
        name = name.strip()
        if not name or name in seen:
            continue
        # A bare 'plugin:skill' fallback resolves to the canonical plugin name;
        # normalize 'plugin:skill' to its last segment for the store lookup
        # (the store stores skill names, not qualified plugin paths).
        if ":" in name:
            name = name.split(":")[-1]
        if name in seen:
            continue
        seen.add(name)
        loaded.append(name)
    return loaded


def _resolved_name(msg: Dict[str, Any]) -> str:
    """The resolved skill name for a ``skill_view`` tool message."""
    content = msg.get("content") or ""
    # Prefer the result's resolved 'name' (most accurate for qualified forms).
    if isinstance(content, str) and content.strip():
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict) and parsed.get("name"):
                return str(parsed["name"]).strip()
        except (json.JSONDecodeError, TypeError):
            pass
    # Fall back to the tool-call arguments (name=...), if recorded.
    tool_calls = msg.get("tool_calls")
    if isinstance(tool_calls, list):
        for tc in tool_calls:
            if not isinstance(tc, dict):
                continue
            try:
                args = (tc.get("function") or {}).get("arguments") or {}
            except AttributeError:
                continue
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except (json.JSONDecodeError, TypeError):
                    args = {}
            name = (args or {}).get("name")
            if isinstance(name, str) and name.strip():
                return name.strip()
    return ""


def mark_skill_outcome(
    store: Any,
    session_id: str,
    outcomes: Dict[str, str],
    *,
    source: str = "review_session",
) -> Dict[str, Dict[str, Any]]:
    """Persist per-skill outcome decisions onto the store's active heads.

    ``store`` carries ``mutate()``/``set_skill_meta``/``latest_active`` (the
    SkillStore). ``outcomes`` maps skill name -> "success"|"failure"|"unknown".
    Writes ``last_outcome``/``last_outcome_at``/``outcome_source`` and pushes
    onto a bounded ``outcome_history`` [{outcome, at, session} ...] (most
    recent first). Returns ``{skill: meta_after}`` for skills that have an
    active head; unknown/no-head skills are skipped (never crash).
    """
    result: Dict[str, Dict[str, Any]] = {}
    if not outcomes:
        return result
    with store.mutate():
        for name, outcome in outcomes.items():
            if outcome not in VALID_OUTCOMES:
                continue
            head = store.latest_active(name)
            if head is None:
                continue
            now = _now_iso()
            meta = head.meta
            history = list(meta.get("outcome_history") or [])
            history.insert(0, {"outcome": outcome, "at": now, "session": session_id})
            del history[_MAX_OUTCOME_HISTORY:]
            fields = {
                "last_outcome": outcome,
                "last_outcome_at": now,
                "outcome_source": source,
                "outcome_history": history,
            }
            store.set_skill_meta(name, **fields)
            result[name] = dict(head.meta)
    return result


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")