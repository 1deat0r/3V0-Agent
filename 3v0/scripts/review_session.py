#!/usr/bin/env python3
"""3V0-owned session-end review — the Stone 7 decision driver.

Direction 3 closes the own-evolution loop with a *process* 3V0 itself drives:
at session end, the ``native-store-bridge`` plugin's ``on_session_end`` hook
spawns this driver as a **detached subprocess** (survives teardown; a TUI quit
kills the gateway process, which would take an in-process review thread with
it). The driver then:

1. reads the just-ended session transcript from the profile's ``state.db``,
2. reads the current canonical memory store (active facts + lineage),
3. asks the Prime-Directive model (DeepSeek-v4-pro via the DeepSeek API) for
   **store-first** decisions — record / supersede / retract,
4. applies each accepted decision through ``scripts/record.py --json --write``
   (the exact backend the ``threev0_record`` tool wraps), and
5. appends an auditable entry to a review log.

It is best-effort by construction: any failure degrades to a log entry and a
non-zero exit that the hook swallows. The wake-time ``sync.py --write`` remains
the backstop reconciler.

The Hermes background-review fork still owns per-turn memory + in-session
skill capture (via ``skill_manage`` + the bridge). This driver now also emits
store-first *skill* decisions (Stone 8) — decommission a skill the session
proved obsolete (``skill_retract`` / ``skill_absorb``) or, rarely, replace a
skill's full content (``skill_update``) — applied through
``scripts/record_skills.py``. Leaving the fork enabled is a separate, later
operator decision.

Stone 9 (direction 4's opening) gives the driver its own clock, independent
of the hook: three mutually-exclusive modes —

- ``--session-id <id>``  the hook path (review the just-ended session);
- ``--latest``           own-clock single shot (review the newest unreviewed
  *eligible* session — ended, top-level, reviewable source, not in the log);
- ``--daemon [--interval N]``  own-clock loop (``--latest`` every N seconds,
  default 600), surviving transient failures — 3V0's first Hermes-independent
  autonomous process.

Env knobs (tests / explicit tuning — defaults are the live profile):
  THREEV0_PROFILE_HOME    profile home (state.db, .env, default review log)
  THREEV0_BODY            body repo root (default: this repo, two levels up)
  THREEV0_REVIEW_STATE_DB override session DB path (tests)
  THREEV0_STORE           override memory store path (tests; honored by
                          record.py subprocesses via inherited env)
  THREEV0_PROFILE_MEM     override profile projection dir (tests)
  THREEV0_SKILL_STORE     override skill store path (tests; honored by
                          record_skills.py subprocesses via inherited env)
  THREEV0_SKILLS_DIR      override profile skills dir (tests; projection target)
  THREEV0_REVIEW_LOG      override the review log jsonl (tests)
  THREEV0_REVIEW=0        disable the review entirely (kill switch)
  THREEV0_REVIEW_MIN_MESSAGES  min user messages to review (default 3)
  THREEV0_REVIEW_COOLDOWN_S    min seconds between reviews (default 300)
  THREEV0_REVIEW_TRANSCRIPT_CAP transcript char cap (default 40000)
  THREEV0_REVIEW_MAX_TOKENS   completion budget (default 8000; the reasoning
                          model needs headroom or it empties ``content``)
  THREEV0_REVIEW_LLM=fake + THREEV0_REVIEW_DECISIONS=<json file>
                          offline mode: read the model's answer from a file
                          (never touches the network)
  THREEV0_REVIEW_MODEL / THREEV0_REVIEW_BASE_URL / DEEPSEEK_API_KEY
                          LLM routing (defaults: deepseek-v4-pro @
                          api.deepseek.com/v1 — the Prime Directive)
"""

from __future__ import annotations

import argparse
import calendar
import json
import os
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.memory import MemoryStore  # noqa: E402
from core.skills import SkillStore  # noqa: E402

PROFILE_HOME = Path(
    os.environ.get("THREEV0_PROFILE_HOME")
    or (Path.home() / ".hermes" / "profiles" / "3v0")
)
STATE_DB = Path(os.environ.get("THREEV0_REVIEW_STATE_DB") or (PROFILE_HOME / "state.db"))
REVIEW_LOG = Path(
    os.environ.get("THREEV0_REVIEW_LOG")
    or (PROFILE_HOME / "3v0_reviews" / "reviews.jsonl")
)
RUN_LOG = REVIEW_LOG.parent / "run.log"
STORE_PATH = Path(
    os.environ.get("THREEV0_STORE") or (REPO_ROOT / "3v0" / "data" / "memory.json")
)
PROFILE_MEM = Path(
    os.environ.get("THREEV0_PROFILE_MEM") or (PROFILE_HOME / "memories")
)
RECORD_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "record.py"
SKILL_STORE_PATH = Path(
    os.environ.get("THREEV0_SKILL_STORE")
    or (REPO_ROOT / "3v0" / "data" / "skills.json")
)
SKILLS_DIR = Path(
    os.environ.get("THREEV0_SKILLS_DIR") or (PROFILE_HOME / "skills")
)
RECORD_SKILLS_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "record_skills.py"

MODEL = os.environ.get("THREEV0_REVIEW_MODEL") or "deepseek-v4-pro"
BASE_URL = (os.environ.get("THREEV0_REVIEW_BASE_URL") or "https://api.deepseek.com/v1").rstrip("/")
MIN_MESSAGES = int(os.environ.get("THREEV0_REVIEW_MIN_MESSAGES") or "3")
COOLDOWN_S = int(os.environ.get("THREEV0_REVIEW_COOLDOWN_S") or "300")
TRANSCRIPT_CAP = int(os.environ.get("THREEV0_REVIEW_TRANSCRIPT_CAP") or "40000")
MAX_TOKENS = int(os.environ.get("THREEV0_REVIEW_MAX_TOKENS") or "8000")
STORE_BLOCK_CAP = 8000
SKILL_BLOCK_CAP = 4000
MAX_DECISIONS = 3

# Interactive surfaces whose sessions are worth a session-end review. Sessions
# from cron/kanban/subagent sources are short-lived harness runs, not 3V0's
# own work with the operator.
REVIEWABLE_SOURCES = {
    "", "tui", "cli", "desktop", "webui", "acp", "webhook",
    "api_server", "local", "test",
}

REVIEW_PROVENANCE = "session-review"

# ---------------------------------------------------------------------------
# The review charter — the system prompt the reviewer model gets.
# ---------------------------------------------------------------------------

CHARTER = """You are 3V0's own session-end memory reviewer — the decision driver \
of 3V0's store-first evolution loop. A session of 3V0 working with its Operator \
just ended; you review it against 3V0's canonical memory store and decide which \
store-first corrections to make.

The store is append-only and provenance-aware. Corrections SUPERSEDE (the old \
fact stays recoverable via history) or RETRACT (marked removed, recoverable). \
Never erased. The Hermes profile (MEMORY.md/USER.md) is a derived view.

Your job is the store-first layer. The per-turn background fork already saved \
obvious user facts during the session — do NOT duplicate anything already in \
ACTIVE FACTS. Act only on what the per-turn path cannot express:

1. OPERATOR CORRECTION: the session proves a stored fact wrong or outdated. \
Supersede it (prefer the exact fact_id) or retract it.
2. ENVIRONMENT CHANGE: a durable change to 3V0's environment, conventions, or \
setup (paths, versions, architecture decisions, mechanisms) — record it.
3. CONSOLIDATION: two or more active facts overlap and should collapse into \
one (supersede the weaker ones with the consolidated fact).
4. DIRECTIVE/IDENTITY: a durable self-commitment or self-truth the session \
established — record with kind 'directive' or 'identity' (store-only kinds).
5. SKILL DECISION: the session proved a 3V0-authored skill (in ACTIVE SKILLS) \
wrong or obsolete. Decommission it store-first: 'skill_retract' (pure prune) \
or 'skill_absorb' (fold into a live umbrella via 'absorbed_into'). \
'skill_update' (full replacement SKILL.md) is allowed but discouraged — \
sessions rarely produce a whole correct SKILL.md; leave content changes to \
skill_manage during the session, which already records them store-first \
through the bridge.

NEVER record: task progress, session outcomes, completed-work logs, transient \
errors, 'command not found' style environment hiccups, or anything that will \
be stale in a week. A no-op review is a correct review when nothing durable \
surfaced. Bias strongly toward zero decisions.

Rules:
- At most 3 decisions. Prefer fewer.
- NEVER supersede or retract a fact whose created_at is NEWER than the session
under review (compare against the session's date): a session predating a fact
cannot disprove it.
- A 'record' MUST be a declarative fact, compact (under ~220 characters), \
with no '§' character (it cannot round-trip to the profile projection).
- Supersession: prefer 'supersedes_id' with an exact fact_id from ACTIVE \
FACTS. Use 'supersedes' (substring) only when you are sure it matches exactly \
one active fact. Never both.
- Retraction: only facts the session proved wrong or obsolete, by exact \
fact_id.
- Kinds: memory, user, identity, directive (directive/identity are \
store-only; memory/user also project to the profile).
- Skill decisions name a skill exactly as it appears in ACTIVE SKILLS, and \
only decommission skills the session actually proved wrong or obsolete — \
never on a hunch. 'skill_absorb' requires the umbrella to be a live ACTIVE \
SKILL (it must already exist).

Reply with ONE JSON object (the word json appears here on purpose; JSON mode \
is enabled) and nothing else:

{"summary": "one line, or 'no-op'",
 "decisions": [
   {"action": "record", "kind": "memory", "content": "...", "supersedes_id": "..."},
   {"action": "record", "kind": "memory", "content": "...", "supersedes": "exact substring"},
   {"action": "retract", "fact_id": "..."},
   {"action": "skill_retract", "name": "some-skill"},
   {"action": "skill_absorb", "name": "some-skill", "absorbed_into": "umbrella-skill"},
   {"action": "skill_update", "name": "some-skill", "content": "full SKILL.md", "category": "optional"}
 ]}
"""


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _log_run(line: str) -> None:
    """Append a diagnostic line to the driver's own run log (best-effort)."""
    try:
        RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(RUN_LOG, "a", encoding="utf-8") as fh:
            fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {line}\n")
    except OSError:
        pass


def _load_api_key() -> Optional[str]:
    """DEEPSEEK_API_KEY from the environment, else the profile's .env."""
    env = os.environ.get("DEEPSEEK_API_KEY")
    if env:
        return env
    dotenv = PROFILE_HOME / ".env"
    try:
        for raw in dotenv.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key.strip() == "DEEPSEEK_API_KEY":
                val = value.strip().strip('"').strip("'")
                return val or None
    except OSError:
        return None
    return None


def _load_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Read the session row + ordered messages from the profile's state.db.

    Also captures the session's end/last-activity timestamp (``as_of``, a Unix
    float) when the schema carries it — used by the temporal guard so a review
    cannot supersede facts recorded *after* the session ended. Column-aware:
    the minimal test fixture has neither column, so ``as_of`` is None there.
    """
    if not STATE_DB.exists():
        return None
    conn = sqlite3.connect(str(STATE_DB), timeout=5)
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(sessions)")}
        select = ["source", "title"]
        if "ended_at" in cols:
            select.append("ended_at")
        if "last_activity_at" in cols:
            select.append("last_activity_at")
        row = conn.execute(
            f"SELECT {', '.join(select)} FROM sessions WHERE id = ?",
            (session_id,),
        ).fetchone()
        if row is None:
            return None
        source, title = row[0] or "", row[1] or ""
        as_of: Optional[float] = None
        idx = 2
        if "ended_at" in cols:
            if isinstance(row[idx], (int, float)):
                as_of = float(row[idx])
            idx += 1
        if as_of is None and "last_activity_at" in cols:
            if isinstance(row[idx], (int, float)):
                as_of = float(row[idx])
        msgs = conn.execute(
            "SELECT role, content, tool_name FROM messages "
            "WHERE session_id = ? AND active = 1 ORDER BY id",
            (session_id,),
        ).fetchall()
    except sqlite3.Error:
        return None
    finally:
        conn.close()
    return {
        "source": source,
        "title": title,
        "as_of": as_of,
        "messages": [
            {"role": role or "", "content": content or "", "tool_name": tool_name or ""}
            for role, content, tool_name in msgs
        ],
    }


def _build_transcript(messages: List[Dict[str, str]], cap: int = TRANSCRIPT_CAP) -> str:
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


def _store_block(store: MemoryStore) -> str:
    """Active facts with ids + timestamps — the decision context (capped)."""
    rows = []
    for fact in store.active():
        rows.append(f"- {fact.id} | {fact.kind} | {fact.created_at} | {fact.content}")
    block = "ACTIVE FACTS (id | kind | created_at | content):\n" + ("\n".join(rows) or "(store empty)")
    if len(block) > STORE_BLOCK_CAP:
        block = block[: STORE_BLOCK_CAP - 40] + "\n… [store block truncated] …"
    return block


def _skills_block(store: SkillStore) -> str:
    """Active 3V0-authored skills — the skill-decision context (capped)."""
    rows = []
    for v in store.active():
        rows.append(f"- {v.name} | {store.state(v.name)} | last {v.action} by {v.source}")
    block = (
        "ACTIVE SKILLS (name | curator state | last action by source):\n"
        + ("\n".join(rows) or "(no 3V0-authored skills)")
    )
    if len(block) > SKILL_BLOCK_CAP:
        block = block[: SKILL_BLOCK_CAP - 40] + "\n… [skills block truncated] …"
    return block


def _load_canned() -> Optional[Dict[str, Any]]:
    """Offline fake-LLM mode: read the model's answer from a JSON file."""
    path = os.environ.get("THREEV0_REVIEW_DECISIONS")
    if not path:
        return None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"summary": "fake-mode parse failure", "decisions": []}


def _tolerant_json(text: str) -> Optional[Dict[str, Any]]:
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


def _call_llm(prompt: str) -> Optional[Dict[str, Any]]:
    """One DeepSeek chat-completion call (JSON mode, tolerant retry).

    DeepSeek-v4-pro is a reasoning model: its thinking goes to
    ``reasoning_content`` and the final answer to ``content``. A too-small
    ``max_tokens`` lets the reasoning consume the whole budget, leaving
    ``content`` empty — a silent failure unless detected. So: a generous
    budget, and empty/unparseable ``content`` is a soft failure that advances
    to the next attempt (with a specific log line instead of a silent None).
    """
    canned = _load_canned()
    if os.environ.get("THREEV0_REVIEW_LLM") == "fake":
        return canned
    api_key = _load_api_key()
    if not api_key:
        _log_run("llm call aborted: no DEEPSEEK_API_KEY")
        return None

    body: Dict[str, Any] = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": CHARTER},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": MAX_TOKENS,
    }
    attempts = [
        ("json_object", dict(body, response_format={"type": "json_object"})),
        ("plain", body),
    ]
    last_reason = "unknown"
    for label, attempt in attempts:
        req = urllib.request.Request(
            f"{BASE_URL}/chat/completions",
            data=json.dumps(attempt).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            finish = data["choices"][0].get("finish_reason")
            if not content:
                last_reason = f"empty content (finish_reason={finish})"
                _log_run(f"llm {label} attempt: {last_reason}")
                continue
            parsed = _tolerant_json(content)
            if parsed is not None:
                return parsed
            last_reason = "unparseable content"
            _log_run(f"llm {label} attempt: unparseable content")
            continue
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError,
                json.JSONDecodeError) as e:
            last_reason = repr(e)
    _log_run(f"llm call failed after retries: {last_reason}")
    return None


# ---------------------------------------------------------------------------
# Decision application
# ---------------------------------------------------------------------------

def _decision_argv(decision: Dict[str, Any]) -> Optional[List[str]]:
    """Map a model decision onto record.py argv; None for invalid shapes."""
    action = str(decision.get("action") or "").strip()
    if action == "retract":
        fact_id = str(decision.get("fact_id") or "").strip()
        if not fact_id:
            return None
        return [str(RECORD_SCRIPT), "--json", "--write", "--retract", fact_id]
    if action != "record":
        return None
    kind = str(decision.get("kind") or "").strip()
    content = str(decision.get("content") or "").strip()
    if kind not in {"memory", "user", "identity", "directive"} or not content:
        return None
    argv = [
        str(RECORD_SCRIPT), "--json", "--write",
        "--kind", kind, "--content", content,
    ]
    if decision.get("supersedes_id"):
        argv += ["--supersedes-id", str(decision["supersedes_id"]).strip()]
    elif decision.get("supersedes"):
        argv += ["--supersedes", str(decision["supersedes"]).strip()]
    return argv


_SKILL_ACTIONS = {"skill_update", "skill_retract", "skill_absorb"}


def _skill_decision_argv(decision: Dict[str, Any]) -> Optional[List[str]]:
    """Map a skill decision onto record_skills.py argv; None for invalid shapes."""
    action = str(decision.get("action") or "").strip()
    name = str(decision.get("name") or "").strip()
    if action not in _SKILL_ACTIONS or not name:
        return None
    if action == "skill_update":
        # Pass the full SKILL.md verbatim (preserve trailing newlines); only
        # reject empty/whitespace-only content.
        content = decision.get("content")
        if not isinstance(content, str) or not content.strip():
            return None
        argv = [
            str(RECORD_SKILLS_SCRIPT), "--json", "--write",
            "--action", "skill_update", "--name", name, "--content", content,
        ]
        if decision.get("category"):
            argv += ["--category", str(decision["category"]).strip()]
        return argv
    if action == "skill_absorb":
        absorbed_into = str(decision.get("absorbed_into") or "").strip()
        if not absorbed_into:
            return None
        return [
            str(RECORD_SKILLS_SCRIPT), "--json", "--write",
            "--action", "skill_absorb", "--name", name,
            "--absorbed-into", absorbed_into,
        ]
    return [
        str(RECORD_SKILLS_SCRIPT), "--json", "--write",
        "--action", "skill_retract", "--name", name,
    ]


def _parse_created_ts(created_at: str) -> Optional[float]:
    """Parse a Fact ``created_at`` (UTC ``YYYY-MM-DDTHH:MM:SSZ``) to a Unix
    timestamp; None when absent/unparseable."""
    try:
        return calendar.timegm(time.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, TypeError):
        return None


def _temporal_refusal(
    decision: Dict[str, Any], store: MemoryStore, session_as_of: Optional[float]
) -> Optional[str]:
    """Refuse a decision that would supersede/retract a fact NEWER than the
    session under review — a session predating a fact cannot disprove it.

    Returns a refusal reason string, or None when the decision is temporally
    safe (or the session timestamp is unknown, in which case the guard is a
    no-op — the minimal test fixture has no ``ended_at`` column).
    """
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
    ts = _parse_created_ts(target.created_at)
    if ts is not None and ts > session_as_of:
        return "fact newer than session under review"
    return None


def _apply_decisions(
    decisions: List[Dict[str, Any]],
    store: MemoryStore,
    session_as_of: Optional[float],
) -> Dict[str, Any]:
    """Run each decision through record.py / record_skills.py (the threev0_record
    backend): memory actions -> record.py, skill actions -> record_skills.py.
    A memory supersede/retract targeting a fact newer than the session is
    refused by the temporal guard before it reaches the backend."""
    applied: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    env = os.environ.copy()
    env.setdefault("THREEV0_STORE", str(STORE_PATH))
    env.setdefault("THREEV0_PROFILE_MEM", str(PROFILE_MEM))
    env.setdefault("THREEV0_SKILL_STORE", str(SKILL_STORE_PATH))
    env.setdefault("THREEV0_SKILLS_DIR", str(SKILLS_DIR))
    for decision in decisions[:MAX_DECISIONS]:
        action = str(decision.get("action") or "").strip()
        temporal = _temporal_refusal(decision, store, session_as_of)
        if temporal:
            refused.append({"reason": temporal, "decision": decision})
            continue
        argv = (
            _skill_decision_argv(decision)
            if action in _SKILL_ACTIONS
            else _decision_argv(decision)
        )
        if argv is None:
            refused.append({"reason": "invalid decision shape", "decision": decision})
            continue
        argv += ["--source", REVIEW_PROVENANCE]
        try:
            proc = subprocess.run(
                [sys.executable] + argv, capture_output=True, text=True, timeout=60,
                env=env,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            refused.append({"reason": f"record backend failed: {e}", "decision": decision})
            continue
        out = (proc.stdout or "").strip()
        try:
            result = json.loads(out) if out else {}
        except json.JSONDecodeError:
            result = {"error": "unparseable record.py output"}
        if proc.returncode == 0 and "error" not in result:
            applied.append(result)
        else:
            refused.append(
                {"reason": result.get("error", "record.py returned non-zero"),
                 "decision": decision}
            )
    return {"applied": applied, "refused": refused}


# ---------------------------------------------------------------------------
# Gating + main
# ---------------------------------------------------------------------------

def _log_entries() -> List[Dict[str, Any]]:
    """All review-log entries (best-effort; [] when missing/unreadable)."""
    try:
        return [
            json.loads(line)
            for line in REVIEW_LOG.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (OSError, json.JSONDecodeError):
        return []


def _acquire_session_lock(session_id: str):
    """Non-blocking per-session flock; returns the fd or None when held."""
    try:
        import fcntl

        lock_dir = REVIEW_LOG.parent / ".locks"
        lock_dir.mkdir(parents=True, exist_ok=True)
        fd = os.open(str(lock_dir / f"review_{session_id}.lock"), os.O_CREAT | os.O_RDWR)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except (OSError, ImportError):
        return None


def _session_columns() -> set:
    """Column names of the sessions table (best-effort; empty when missing)."""
    if not STATE_DB.exists():
        return set()
    try:
        conn = sqlite3.connect(str(STATE_DB), timeout=5)
        try:
            return {r[1] for r in conn.execute("PRAGMA table_info(sessions)")}
        finally:
            conn.close()
    except sqlite3.Error:
        return set()


def _candidate_sessions() -> List[tuple]:
    """Session ``(id, source)`` rows, newest first, that are 3V0's own *ended*
    top-level sessions worth considering. Column-existence-aware so it works
    against the real state.db AND the minimal test-fixture schema."""
    cols = _session_columns()
    where = []
    if "ended_at" in cols:
        where.append("ended_at IS NOT NULL")      # skip the live session
    if "parent_session_id" in cols:
        where.append("parent_session_id IS NULL")  # skip delegated subagents
    if "hidden" in cols:
        where.append("hidden = 0")
    if "archived" in cols:
        where.append("archived = 0")
    sql = "SELECT id, source FROM sessions"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id DESC"
    try:
        conn = sqlite3.connect(str(STATE_DB), timeout=5)
        try:
            return [
                (sid, source or "") for sid, source in conn.execute(sql).fetchall()
            ]
        finally:
            conn.close()
    except sqlite3.Error:
        return []


def review_one(session_id: str) -> str:
    """Run the full gating + review for one session id.

    Returns a status string: ``"reviewed"``, ``"failed"``, or
    ``"skipped:<reason>"`` (reason in killswitch/lock/dedupe/cooldown/missing/
    source/min_messages). The hook's ``--session-id`` path maps these to exit
    codes; the own-clock paths interpret them to pick the next candidate.
    """
    if os.environ.get("THREEV0_REVIEW") == "0":
        return "skipped:killswitch"

    lock_fd = _acquire_session_lock(session_id)
    if lock_fd is None:
        return "skipped:lock"

    try:
        # Dedupe + cooldown from the review log.
        now = time.time()
        for entry in _log_entries():
            if entry.get("session_id") == session_id:
                return "skipped:dedupe"
            at = entry.get("at")
            if isinstance(at, (int, float)) and (now - at) < COOLDOWN_S:
                return "skipped:cooldown"

        session = _load_session(session_id)
        if session is None:
            return "skipped:missing"
        if session["source"] not in REVIEWABLE_SOURCES:
            return "skipped:source"
        n_user = sum(1 for m in session["messages"] if m["role"] == "user")
        if n_user < MIN_MESSAGES:
            return "skipped:min_messages"

        transcript = _build_transcript(session["messages"])
        store = MemoryStore(STORE_PATH)
        skill_store = SkillStore(SKILL_STORE_PATH)
        prompt = (
            f"Session {session_id} (title: {session['title'] or 'untitled'}) "
            f"just ended.\n\n"
            f"{_store_block(store)}\n\n"
            f"{_skills_block(skill_store)}\n\n"
            f"SESSION TRANSCRIPT (compacted; tool outputs truncated):\n"
            f"{transcript}\n\n"
            f"Decide the store-first corrections described in your charter and "
            f"output the single JSON object."
        )

        answer = _call_llm(prompt)
        if answer is None:
            _log_run(f"review {session_id}: llm call failed")
            return "failed"

        decisions = answer.get("decisions") if isinstance(answer, dict) else None
        if not isinstance(decisions, list):
            decisions = []
        result = _apply_decisions(decisions, store, session.get("as_of"))

        entry = {
            "session_id": session_id,
            "at": now,
            "source": session["source"],
            "model": MODEL,
            "summary": str(answer.get("summary", ""))[:300] if isinstance(answer, dict) else "",
            "decisions_requested": len(decisions),
            "applied": len(result["applied"]),
            "refused": len(result["refused"]),
            "refused_details": [
                {"reason": r["reason"]} for r in result["refused"]
            ],
        }
        REVIEW_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(REVIEW_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        _log_run(
            f"review {session_id}: applied={entry['applied']} "
            f"refused={entry['refused']} requested={entry['decisions_requested']}"
        )
        return "reviewed"
    finally:
        if lock_fd is not None:
            try:
                os.close(lock_fd)
            except OSError:
                pass


def _review_latest() -> int:
    """Single-shot own-clock: review the newest unreviewed eligible session.

    Scans candidates newest-first, skipping already-reviewed ids; reviews at
    most one session per invocation (the global cooldown throttles the rest).
    Returns an exit code: 0 = reviewed something or nothing to do, 1 = hard
    failure.
    """
    reviewed_ids = {e.get("session_id") for e in _log_entries()}
    for sid, _source in _candidate_sessions():
        if sid in reviewed_ids:
            continue
        status = review_one(sid)
        if status == "reviewed":
            return 0
        if status == "failed":
            return 1
        if status == "skipped:cooldown":
            return 0  # global throttle — nothing more this tick
        # skipped:missing / source / min_messages / dedupe / lock ->
        # not eligible; try the next candidate
        continue
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="3V0-owned session review driver")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--session-id", help="review this exact session (the hook path)"
    )
    group.add_argument(
        "--latest", action="store_true",
        help="review the newest unreviewed eligible session (own-clock single shot)",
    )
    group.add_argument(
        "--daemon", action="store_true",
        help="own-clock loop: run --latest every --interval seconds",
    )
    ap.add_argument(
        "--interval", type=int, default=600,
        help="seconds between daemon passes (default 600)",
    )
    args = ap.parse_args()

    if os.environ.get("THREEV0_REVIEW") == "0":
        return 0

    if args.session_id:
        status = review_one(args.session_id)
        return 1 if status == "failed" else 0

    if args.latest:
        return _review_latest()

    # --daemon: 3V0's own clock — loop the latest-session review forever,
    # surviving transient failures (a tick error is a log line, not a crash).
    _log_run(f"daemon started (interval={args.interval}s)")
    try:
        while True:
            try:
                _review_latest()
            except Exception as e:  # noqa: BLE001 - a daemon must not die on a tick error
                _log_run(f"daemon tick error: {e}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        _log_run("daemon stopped (keyboard interrupt)")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
