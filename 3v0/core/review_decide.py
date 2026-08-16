"""3V0 review decision half — the pure core extracted from the review driver.

The own-clock session reviewer (``scripts/review_session.py``) splits into a
pure *decision* half and a shell that resolves config, reads the session DB,
calls the LLM, and orchestrates subprocesses. This module is that decision
half, moved out so it is unit-testable without importing the driver — whose
module load runs ``_resolve_project()``, a side effect that drags in
env/ledger/SQLite scaffolding (see the review driver's own test loader).

Every function here is pure over its arguments (plus the store objects handed
to it): no globals, no I/O, no subprocess. The canonical vocabularies are
imported from their owners rather than re-declared, so the decision schema has
one source.
"""

from __future__ import annotations

import calendar
import json
import time
from typing import Any, Dict, List, Optional

from .decide_skills import SKILL_DECISION_ACTIONS
from .memory import MemoryStore
from .skills import SkillStore

DEFAULT_TRANSCRIPT_CAP = 40000
DEFAULT_STORE_BLOCK_CAP = 8000
DEFAULT_SKILL_BLOCK_CAP = 4000


def tolerant_json(text: str) -> Optional[Dict[str, Any]]:
    """Parse the model's answer: strip code fences, take the JSON object."""
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[-1]
        if stripped.rstrip().endswith("```"):
            stripped = stripped.rstrip()[:-3]
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(stripped[start : end + 1])
    except json.JSONDecodeError:
        return None


def parse_created_ts(created_at: str) -> Optional[float]:
    """Parse a Fact ``created_at`` (UTC ``YYYY-MM-DDTHH:MM:SSZ``) to a Unix
    timestamp; None when absent/unparseable."""
    try:
        return calendar.timegm(time.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, TypeError):
        return None


def build_transcript(
    messages: List[Dict[str, str]], cap: int = DEFAULT_TRANSCRIPT_CAP
) -> str:
    """Compact the session into review text: user/assistant text, tool calls
    as names, tool outputs truncated; head+tail trim under the char cap."""
    lines: List[str] = []
    first_user: Optional[str] = None
    for m in messages:
        role = m["role"]
        content = m["content"].strip()
        if role == "user" and content:
            if first_user is None:
                first_user = content
            lines.append(f"USER: {content}")
        elif role == "assistant":
            if m["tool_name"]:
                lines.append(f"ASSISTANT[tool {m['tool_name']} returned]")
            elif content:
                lines.append(f"ASSISTANT: {content[:1500]}")
        elif role == "tool":
            if content:
                lines.append(f"TOOL OUTPUT: {content[:300]}")
    if not lines:
        return "(no transcript)"
    text = "\n".join(lines)
    if len(text) <= cap:
        return text
    head_keep = min(2000, cap // 2)
    tail_keep = cap - head_keep
    head = text[:head_keep]
    tail = text[-tail_keep:] if tail_keep > 0 else ""
    return head + "\n… [middle truncated] …\n" + tail


def store_block(store: MemoryStore, cap: int = DEFAULT_STORE_BLOCK_CAP) -> str:
    """Active facts with ids + timestamps — the decision context (capped)."""
    rows = []
    for fact in store.active():
        rows.append(f"- {fact.id} | {fact.kind} | {fact.created_at} | {fact.content}")
    block = "ACTIVE FACTS (id | kind | created_at | content):\n" + (
        "\n".join(rows) or "(store empty)"
    )
    if len(block) > cap:
        block = block[: cap - 40] + "\n… [store block truncated] …"
    return block


def skills_block(skill_store: SkillStore, cap: int = DEFAULT_SKILL_BLOCK_CAP) -> str:
    """Active 3V0-authored skills — the skill-decision context (capped)."""
    rows = []
    for v in skill_store.active():
        rows.append(
            f"- {v.name} | {skill_store.state(v.name)} | {v.created_at} "
            f"| last {v.action} by {v.source}"
        )
    block = (
        "ACTIVE SKILLS (name | curator state | created_at | last action by source):\n"
        + ("\n".join(rows) or "(no 3V0-authored skills)")
    )
    if len(block) > cap:
        block = block[: cap - 40] + "\n… [skills block truncated] …"
    return block


def temporal_refusal(
    decision: Dict[str, Any], store: MemoryStore, session_as_of: Optional[float]
) -> Optional[str]:
    """Refuse a decision that would supersede/retract a fact NEWER than the
    session under review — a session predating a fact cannot disprove it.

    Returns a refusal reason string, or None when the decision is temporally
    safe (or the session timestamp is unknown, in which case the guard is a
    no-op — the minimal test fixture has no ``ended_at`` column)."""
    if session_as_of is None:
        return None
    action = str(decision.get("action") or "").strip()
    if action == "retract":
        target = store.get(str(decision.get("fact_id") or "").strip())
    elif action == "record":
        supersedes_id = str(decision.get("supersedes_id") or "").strip()
        if supersedes_id:
            target = store.get(supersedes_id)
        elif decision.get("supersedes"):
            sub = str(decision["supersedes"]).strip()
            target = next(
                (f for f in store.active() if sub and sub in f.content), None
            )
        else:
            return None
    else:
        return None
    if target is None:
        return None
    ts = parse_created_ts(target.created_at)
    if ts is not None and ts > session_as_of:
        return "fact newer than session under review"
    return None


def skill_temporal_refusal(
    decision: Dict[str, Any],
    skill_store: Optional[SkillStore],
    session_as_of: Optional[float],
) -> Optional[str]:
    """Refuse a skill decision that would decommission or replace a skill whose
    ACTIVE version is NEWER than the session under review — a session predating
    the current version cannot disprove it. The symmetric counterpart of
    ``temporal_refusal`` for the skill axis.

    Returns a refusal reason string, or None when the decision is temporally
    safe (or the session timestamp is unknown, in which case the guard is a
    no-op — the minimal test fixture has no ``ended_at`` column). A skill name
    with no active version is not guarded: the backend either refuses
    (retract/absorb of an unknown name) or creates a fresh version (update of a
    new name), neither of which is a temporal regression."""
    if session_as_of is None or skill_store is None:
        return None
    action = str(decision.get("action") or "").strip()
    if action not in SKILL_DECISION_ACTIONS:
        return None
    name = str(decision.get("name") or "").strip()
    if not name:
        return None
    target = skill_store.latest_active(name)
    if target is None:
        return None
    ts = parse_created_ts(target.created_at)
    if ts is not None and ts > session_as_of:
        return "skill version newer than session under review"
    return None
