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

- ``--session-id <id>``  the hook path (review the just-ended session; the
  global cooldown throttles this per-turn hook so it does not fire a review
  on every turn);
- ``--latest``           own-clock single shot (reconcile store<->profile
  drift, then drain the backlog: review every unreviewed *eligible* session —
  ended, top-level, reviewable source, not in the log — up to
  ``MAX_PER_PASS``);
- ``--daemon [--interval N]``  own-clock loop (reconcile + drain every N
  seconds, default 600), surviving transient failures — 3V0's first
  Hermes-independent autonomous process. Stone 14 folded the wake-time
  reconcilers into the tick, so the daemon is now a full maintenance clock:
  it heals drift between sessions, not just at wake.

Env knobs (tests / explicit tuning — defaults are the live profile):
  THREEV0_PROFILE_HOME    profile home (state.db, .env, default review log)
  THREEV0_BODY            body repo root (default: this repo, two levels up)
  THREEV0_PROJECT         project to review: threev0 (default) | f1nance | axiom
  THREEV0_PROJECT_CWD     override the project's repo cwd root (tests/migration)
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
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.memory import MemoryStore  # noqa: E402
from core.projects import ProjectSpec, resolve_project  # noqa: E402
from core.skills import SkillStore  # noqa: E402

PROFILE_HOME = Path(
    os.environ.get("THREEV0_PROFILE_HOME")
    or (Path.home() / ".hermes" / "profiles" / "3v0")
)
STATE_DB = Path(os.environ.get("THREEV0_REVIEW_STATE_DB") or (PROFILE_HOME / "state.db"))
RECORD_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "record.py"
RECORD_SKILLS_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "record_skills.py"
SYNC_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "sync.py"
SYNC_SKILLS_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "sync_skills.py"
DRIFT_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "drift_check.py"

# Project-scoped paths/state — resolved from THREEV0_PROJECT (default:
# threev0) and rebound by _resolve_project() (also called when --project is
# given). The THREEV0_* env overrides (tests) still win over project defaults.
PROJECT = ""
PROJECT_SPEC: Optional[ProjectSpec] = None
CWD_ROOTS: Tuple[Path, ...] = ()
PRIMARY = False
MEMORY_ONLY = False
STORE_ONLY = False
STORE_PATH: Path = Path()
PROFILE_MEM: Optional[Path] = None
SKILL_STORE_PATH: Optional[Path] = None
SKILLS_DIR: Path = Path()
REVIEW_LOG: Path = Path()
RUN_LOG: Path = Path()

MODEL = os.environ.get("THREEV0_REVIEW_MODEL") or "deepseek-v4-pro"
BASE_URL = (os.environ.get("THREEV0_REVIEW_BASE_URL") or "https://api.deepseek.com/v1").rstrip("/")
MIN_MESSAGES = int(os.environ.get("THREEV0_REVIEW_MIN_MESSAGES") or "3")
COOLDOWN_S = int(os.environ.get("THREEV0_REVIEW_COOLDOWN_S") or "300")
TRANSCRIPT_CAP = int(os.environ.get("THREEV0_REVIEW_TRANSCRIPT_CAP") or "40000")
MAX_TOKENS = int(os.environ.get("THREEV0_REVIEW_MAX_TOKENS") or "8000")
STORE_BLOCK_CAP = 8000
SKILL_BLOCK_CAP = 4000
MAX_DECISIONS = 3
MAX_PER_PASS = int(os.environ.get("THREEV0_REVIEW_MAX_PER_PASS") or "30")
NETWORK_RETRIES = 3
BACKOFF_SECONDS = float(os.environ.get("THREEV0_REVIEW_BACKOFF_S") or "2.0")

# Interactive surfaces whose sessions are worth a session-end review. Sessions
# from cron/kanban/subagent sources are short-lived harness runs, not 3V0's
# own work with the operator.
REVIEWABLE_SOURCES = {
    "", "tui", "cli", "desktop", "webui", "acp", "webhook",
    "api_server", "local", "test",
}

REVIEW_PROVENANCE = "session-review"


def _is_project_cwd(cwd: Optional[str]) -> bool:
    """True when a session's cwd belongs to the active project.

    The active project's repo roots (and subdirs) are admitted. The primary
    project (3V0) additionally treats ``$HOME`` as its own and fails open on an
    empty/unknown cwd; sibling projects are strict — an empty/unknown cwd is
    skipped, never folded into a sibling's store."""
    if not cwd:
        return PRIMARY
    cwd = str(cwd)
    for root in CWD_ROOTS:
        root_s = str(root).rstrip("/")
        if cwd == root_s or cwd.startswith(root_s + "/"):
            return True
    if PRIMARY and cwd == str(Path.home()):
        return True
    return False

# ---------------------------------------------------------------------------
# The review charter — the system prompt the reviewer model gets.
# ---------------------------------------------------------------------------

_CHARTER_TEMPLATE = """You are {project}'s own session-end memory reviewer — the decision driver \
of the store-first evolution loop. A session of {project} working with its Operator \
just ended; you review it against {project}'s canonical memory store and decide which \
store-first corrections to make.

The store is append-only and provenance-aware. Corrections SUPERSEDE (the old \
fact stays recoverable via history) or RETRACT (marked removed, recoverable). \
Never erased. The Hermes profile (MEMORY.md/USER.md) is a derived view.

Your job is the store-first capture layer — the durable-memory writer for a
session. Capture everything durable the session revealed, and do NOT duplicate
anything already correctly represented in ACTIVE FACTS. Act only on what is
not already there:

1. OPERATOR FACT / PREFERENCE: the user revealed something about themselves —
persona, preferences, work style, personal details — or an expectation about
how 3V0 should behave. Record it (kind 'memory' or 'user').
2. OPERATOR CORRECTION: the session proves a stored fact wrong or outdated.
Supersede it (prefer the exact fact_id) or retract it.
3. ENVIRONMENT CHANGE: a durable change to 3V0's environment, conventions, or
setup (paths, versions, architecture decisions, mechanisms) — record it.
4. CONSOLIDATION: two or more active facts overlap and should collapse into
one (supersede the weaker ones with the consolidated fact).
5. DIRECTIVE/IDENTITY: a durable self-commitment or self-truth the session
established — record with kind 'directive' or 'identity' (store-only kinds).
6. SKILL DECISION: the session proved a 3V0-authored skill (in ACTIVE SKILLS)
wrong or obsolete. Decommission it store-first: 'skill_retract' (pure prune)
or 'skill_absorb' (fold into a live umbrella via 'absorbed_into').
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
never on a hunch. NEVER decommission or replace a skill whose ACTIVE \
version's created_at is NEWER than the session under review. 'skill_absorb' \
requires the umbrella to be a live ACTIVE SKILL (it must already exist).

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

# Default charter binding; _resolve_project() rebinds it to the active project.
CHARTER = _CHARTER_TEMPLATE.replace("{project}", "3V0")


def _path_or(env_key: str, default: Optional[Path]) -> Optional[Path]:
    """Resolve a THREEV0_* path override; fall back to the project default."""
    val = os.environ.get(env_key)
    return Path(val) if val else default


def _path_or_required(env_key: str, default: Path) -> Path:
    """Resolve a THREEV0_* path override whose project default is always set."""
    val = os.environ.get(env_key)
    return Path(val) if val else default


def _resolve_project() -> None:
    """(Re)bind the project-scoped globals from THREEV0_PROJECT.

    Called once at import and again from main() when --project is given. The
    THREEV0_* env overrides (tests) still win over the project defaults, but
    the MEMORY_ONLY / STORE_ONLY / PRIMARY flags are pure project properties
    (they are never affected by a path override)."""
    global PROJECT, PROJECT_SPEC, CWD_ROOTS, PRIMARY, MEMORY_ONLY, STORE_ONLY
    global STORE_PATH, PROFILE_MEM, SKILL_STORE_PATH, SKILLS_DIR, REVIEW_LOG, RUN_LOG
    global CHARTER
    PROJECT = os.environ.get("THREEV0_PROJECT") or "threev0"
    PROJECT_SPEC = resolve_project(
        PROJECT,
        REPO_ROOT,
        PROFILE_HOME,
        cwd_override=os.environ.get("THREEV0_PROJECT_CWD"),
    )
    CWD_ROOTS = PROJECT_SPEC.cwd_roots
    PRIMARY = PROJECT_SPEC.primary
    MEMORY_ONLY = PROJECT_SPEC.memory_only
    STORE_ONLY = PROJECT_SPEC.store_only
    STORE_PATH = _path_or_required("THREEV0_STORE", PROJECT_SPEC.store)
    PROFILE_MEM = _path_or("THREEV0_PROFILE_MEM", PROJECT_SPEC.profile_mem)
    SKILL_STORE_PATH = _path_or("THREEV0_SKILL_STORE", PROJECT_SPEC.skill_store)
    SKILLS_DIR = _path_or_required("THREEV0_SKILLS_DIR", PROFILE_HOME / "skills")
    REVIEW_LOG = _path_or_required("THREEV0_REVIEW_LOG", PROJECT_SPEC.review_log)
    RUN_LOG = REVIEW_LOG.parent / "run.log"
    # The memory-only / store-only flags are authoritative over any stray env
    # override: a memory-only project has no skill axis, and a store-only
    # project has no profile projection, full stop.
    if MEMORY_ONLY:
        SKILL_STORE_PATH = None
    if STORE_ONLY:
        PROFILE_MEM = None
    CHARTER = _CHARTER_TEMPLATE.replace("{project}", PROJECT_SPEC.title)


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
        if "cwd" in cols:
            select.append("cwd")
        row = conn.execute(
            f"SELECT {', '.join(select)} FROM sessions WHERE id = ?",
            (session_id,),
        ).fetchone()
        if row is None:
            return None
        source, title = row[0] or "", row[1] or ""
        as_of: Optional[float] = None
        ended: Optional[bool] = None  # None = no ended_at column (unknown)
        idx = 2
        if "ended_at" in cols:
            ended = row[idx] is not None
            if isinstance(row[idx], (int, float)):
                as_of = float(row[idx])
            idx += 1
        if "last_activity_at" in cols:
            if as_of is None and isinstance(row[idx], (int, float)):
                as_of = float(row[idx])
            idx += 1  # always advance: the column is always selected, even when
                      # as_of was already set from ended_at (the cwd mis-scope bug)
        cwd = ""
        if "cwd" in cols:
            cwd = row[idx] or ""
            idx += 1
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
        "ended": ended,
        "cwd": cwd,
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
        rows.append(f"- {v.name} | {store.state(v.name)} | {v.created_at} | last {v.action} by {v.source}")
    block = (
        "ACTIVE SKILLS (name | curator state | created_at | last action by source):\n"
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
        for retry in range(NETWORK_RETRIES):
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
            except (urllib.error.URLError, TimeoutError) as e:
                # Transient transport failure — back off and retry this label.
                last_reason = repr(e)
                if retry < NETWORK_RETRIES - 1:
                    _log_run(f"llm {label} transport error, retry {retry + 1}: {e}")
                    time.sleep(BACKOFF_SECONDS * retry)
                    continue
                break  # retries exhausted for this label -> try the next
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                last_reason = repr(e)
                break  # malformed payload — not worth retrying this label
            if not content:
                last_reason = f"empty content (finish_reason={finish})"
                _log_run(f"llm {label} attempt: {last_reason}")
                break
            parsed = _tolerant_json(content)
            if parsed is not None:
                return parsed
            last_reason = "unparseable content"
            _log_run(f"llm {label} attempt: unparseable content")
            break
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


def _skill_temporal_refusal(
    decision: Dict[str, Any],
    skill_store: Optional[SkillStore],
    session_as_of: Optional[float],
) -> Optional[str]:
    """Refuse a skill decision that would decommission or replace a skill whose
    ACTIVE version is NEWER than the session under review — a session predating
    the current version cannot disprove it. The symmetric counterpart of
    ``_temporal_refusal`` for the skill axis.

    Returns a refusal reason string, or None when the decision is temporally
    safe (or the session timestamp is unknown, in which case the guard is a
    no-op — the minimal test fixture has no ``ended_at`` column). A skill name
    with no active version is not guarded: the backend either refuses
    (retract/absorb of an unknown name) or creates a fresh version (update of a
    new name), neither of which is a temporal regression.
    """
    if session_as_of is None or skill_store is None:
        return None
    action = str(decision.get("action") or "").strip()
    if action not in _SKILL_ACTIONS:
        return None
    name = str(decision.get("name") or "").strip()
    if not name:
        return None
    target = skill_store.latest_active(name)
    if target is None:
        return None
    ts = _parse_created_ts(target.created_at)
    if ts is not None and ts > session_as_of:
        return "skill version newer than session under review"
    return None


def _apply_decisions(
    decisions: List[Dict[str, Any]],
    store: MemoryStore,
    session_as_of: Optional[float],
    skill_store: Optional[SkillStore] = None,
) -> Dict[str, Any]:
    """Run each decision through record.py / record_skills.py (the threev0_record
    backend): memory actions -> record.py, skill actions -> record_skills.py.
    A supersede/retract targeting a fact or skill version NEWER than the
    session is refused by the temporal guard before it reaches the backend."""
    applied: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    env = os.environ.copy()
    env.setdefault("THREEV0_STORE", str(STORE_PATH))
    if not STORE_ONLY:
        env.setdefault("THREEV0_PROFILE_MEM", str(PROFILE_MEM))
    if not MEMORY_ONLY:
        env.setdefault("THREEV0_SKILL_STORE", str(SKILL_STORE_PATH))
        env.setdefault("THREEV0_SKILLS_DIR", str(SKILLS_DIR))
    for decision in decisions[:MAX_DECISIONS]:
        action = str(decision.get("action") or "").strip()
        if action in _SKILL_ACTIONS and skill_store is None:
            refused.append(
                {"reason": "skill axis disabled (memory-only project)", "decision": decision}
            )
            continue
        temporal = (
            _skill_temporal_refusal(decision, skill_store, session_as_of)
            if action in _SKILL_ACTIONS
            else _temporal_refusal(decision, store, session_as_of)
        )
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
        if STORE_ONLY:
            argv += ["--no-export"]
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


def _session_columns() -> Optional[set]:
    """Column names of the sessions table, or None when the schema cannot be
    inspected (a transient lock / missing DB). Callers MUST treat None as "do
    not proceed" — never as "no columns", which would silently drop the
    ended_at filter and let a review touch a still-open session."""
    if not STATE_DB.exists():
        return set()
    try:
        conn = sqlite3.connect(str(STATE_DB), timeout=5)
        try:
            return {r[1] for r in conn.execute("PRAGMA table_info(sessions)")}
        finally:
            conn.close()
    except sqlite3.Error:
        return None


def _candidate_sessions() -> List[tuple]:
    """Session ``(id, source)`` rows, newest first, that are 3V0's own *ended*
    top-level sessions worth considering. Column-existence-aware so it works
    against the real state.db AND the minimal test-fixture schema.

    FAIL-SAFE: if the schema cannot be inspected (``_session_columns`` returns
    None), return [] — never fall through to an unfiltered query that would
    surface still-open (live) sessions."""
    cols = _session_columns()
    if cols is None:
        _log_run("candidate scan aborted: sessions schema unreadable")
        return []
    where = []
    if "ended_at" in cols:
        where.append("ended_at IS NOT NULL")      # skip the live session
    if "parent_session_id" in cols:
        where.append("parent_session_id IS NULL")  # skip delegated subagents
    if "hidden" in cols:
        where.append("hidden = 0")
    if "archived" in cols:
        where.append("archived = 0")
    select = ["id", "source"]
    if "cwd" in cols:
        select.append("cwd")
    sql = f"SELECT {', '.join(select)} FROM sessions"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id DESC"
    try:
        conn = sqlite3.connect(str(STATE_DB), timeout=5)
        try:
            rows = conn.execute(sql).fetchall()
        finally:
            conn.close()
    except sqlite3.Error:
        return []
    out = []
    for row in rows:
        sid, source = row[0], row[1] or ""
        if "cwd" in cols and not _is_project_cwd(row[2]):
            continue  # a sibling project's session — not 3V0's own work
        out.append((sid, source))
    return out


def review_one(session_id: str, *, respect_cooldown: bool = True) -> str:
    """Run the full gating + review for one session id.

    Returns a status string: ``"reviewed"``, ``"failed"``, or
    ``"skipped:<reason>"`` (reason in killswitch/lock/dedupe/cooldown/missing/
    source/min_messages). The hook's ``--session-id`` path maps these to exit
    codes; the own-clock paths interpret them to pick the next candidate.

    ``respect_cooldown`` gates the 300s global throttle. The per-turn hook
    (``--session-id``) sets it True so a session-end review does not fire on
    every turn; the own-clock drain passes False so a backlog drains
    back-to-back (the per-session flock + dedupe still prevent double-review).
    """
    if os.environ.get("THREEV0_REVIEW") == "0":
        return "skipped:killswitch"

    lock_fd = _acquire_session_lock(session_id)
    if lock_fd is None:
        return "skipped:lock"

    try:
        # Dedupe + (optional) cooldown from the review log.
        now = time.time()
        for entry in _log_entries():
            if entry.get("session_id") == session_id:
                return "skipped:dedupe"
            if respect_cooldown:
                at = entry.get("at")
                if isinstance(at, (int, float)) and (now - at) < COOLDOWN_S:
                    return "skipped:cooldown"

        session = _load_session(session_id)
        if session is None:
            return "skipped:missing"
        if session.get("ended") is False:
            # A still-live session (ended_at is NULL): the per-turn hook must
            # not review it — a mid-transcript review would be incomplete and
            # its dedupe entry would shadow the daemon's final review, so the
            # session's late-turn facts would never be captured. Only the
            # own-clock drain reviews (ended) sessions.
            return "skipped:live"
        if session["source"] not in REVIEWABLE_SOURCES:
            return "skipped:source"
        if not _is_project_cwd(session.get("cwd")):
            return "skipped:project"
        n_user = sum(1 for m in session["messages"] if m["role"] == "user")
        if n_user < MIN_MESSAGES:
            return "skipped:min_messages"

        transcript = _build_transcript(session["messages"])
        store = MemoryStore(STORE_PATH)
        skill_store = SkillStore(SKILL_STORE_PATH) if SKILL_STORE_PATH else None
        skills_part = (
            _skills_block(skill_store)
            if skill_store
            else "ACTIVE SKILLS: (none — memory-only project)\n"
        )
        prompt = (
            f"Session {session_id} (title: {session['title'] or 'untitled'}) "
            f"just ended.\n\n"
            f"{_store_block(store)}\n\n"
            f"{skills_part}\n\n"
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
        result = _apply_decisions(decisions, store, session.get("as_of"), skill_store)

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


def _sync() -> str:
    """Heal store<->profile drift (memory + skills) by running the wake-time
    reconcilers, best-effort.

    Stone 14 (the wake-sync fold): with the Hermes background-review fork cut,
    the own clock is the sole autonomous writer — so it must also heal drift,
    not just review. The reconcilers are idempotent, ``flock``-locked (via
    ``mutate()``), and cheap (no LLM). Returns ``"synced"`` or
    ``"sync-failed:<script>"``; a failure is a log line, never a crash, and
    the next tick retries.

    This runs only on the own-clock paths (``--latest`` / ``--daemon``), not
    the per-turn ``--session-id`` hook — sync there would be redundant churn.

    Store-only projects (siblings) have no Hermes profile projection to
    reconcile, so their sync pass is a clean no-op (``skipped:store-only``).
    """
    if STORE_ONLY:
        _log_run("sync skipped (store-only project)")
        return "skipped:store-only"
    env = os.environ.copy()
    env.setdefault("THREEV0_STORE", str(STORE_PATH))
    env.setdefault("THREEV0_PROFILE_MEM", str(PROFILE_MEM))
    env.setdefault("THREEV0_SKILL_STORE", str(SKILL_STORE_PATH))
    env.setdefault("THREEV0_SKILLS_DIR", str(SKILLS_DIR))
    for script in (SYNC_SCRIPT, SYNC_SKILLS_SCRIPT):
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--write"],
                capture_output=True, text=True, timeout=120, env=env,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            _log_run(f"sync {script.name} failed: {e}")
            return f"sync-failed:{script.name}"
        if proc.returncode != 0:
            tail = (proc.stderr or "").strip().replace("\n", " ")[:200]
            _log_run(f"sync {script.name} returned {proc.returncode}: {tail}")
            return f"sync-failed:{script.name}"
    _log_run("sync pass: store<->profile reconciled (memory + skills)")
    return "synced"


def _drain() -> int:
    """Drain the unreviewed backlog: review every eligible unreviewed session
    (newest first) in one pass, up to ``MAX_PER_PASS`` LLM attempts.

    Back-to-back by design — the 300s cooldown belongs to the per-turn hook
    path, not the own clock; the per-session flock + dedupe still prevent
    double-review. A failed review is logged and left unreviewed for the next
    pass; it does not abort the drain (the daemon survives per-session
    failures). Returns 0 always.
    """
    reviewed_ids = {e.get("session_id") for e in _log_entries()}
    reviewed = 0
    failed = 0
    skipped = 0
    attempted = 0
    for sid, _source in _candidate_sessions():
        if sid in reviewed_ids:
            continue
        status = review_one(sid, respect_cooldown=False)
        if status == "reviewed":
            reviewed += 1
            attempted += 1
        elif status == "failed":
            failed += 1
            attempted += 1
        else:  # skipped:dedupe / lock / missing / source / min_messages / project
            skipped += 1
        if attempted >= MAX_PER_PASS:
            break
    if reviewed or failed or skipped:
        _log_run(f"drain pass: reviewed={reviewed} failed={failed} skipped={skipped}")
    return 0


def _drift() -> str:
    """Run the multi-project drift check (Stone 16's clock) and log a summary.

    Report-only: it never writes the ledger — position snapshots are deliberate
    commits, not per-tick churn (the daemon must not dirty the body repo's
    working tree). Only the primary project's daemon (3V0, the orchestrator)
    runs it; sibling daemons are store-only reviewers, not the ledger's keeper.
    Best-effort: a drift failure is a log line, never a crash.
    """
    if not PRIMARY:
        return "skipped:not-primary"
    try:
        proc = subprocess.run(
            [sys.executable, str(DRIFT_SCRIPT), "--json"],
            capture_output=True, text=True, timeout=120,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        _log_run(f"drift check failed: {e}")
        return f"drift-failed:{e}"
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().replace("\n", " ")[:200]
        _log_run(f"drift check returned {proc.returncode}: {tail}")
        return "drift-failed"
    try:
        result = json.loads(proc.stdout) if proc.stdout.strip() else {}
    except json.JSONDecodeError:
        _log_run("drift check output unparseable")
        return "drift-failed"
    total = result.get("total", 0)
    drifting = result.get("drifting", 0)
    names = [
        r.get("name", "?")
        for r in result.get("projects", [])
        if isinstance(r, dict) and r.get("drifting")
    ]
    suffix = f" ({', '.join(names)})" if names else ""
    _log_run(f"drift pass: {drifting}/{total} drifting{suffix}")
    return "drift-ok"


def main() -> int:
    ap = argparse.ArgumentParser(description="3V0-owned session review driver")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--session-id", help="review this exact session (the hook path)"
    )
    group.add_argument(
        "--latest", action="store_true",
        help="drain the unreviewed backlog (own-clock single shot)",
    )
    group.add_argument(
        "--daemon", action="store_true",
        help="own-clock loop: drain the backlog every --interval seconds",
    )
    ap.add_argument(
        "--interval", type=int, default=600,
        help="seconds between daemon passes (default 600)",
    )
    ap.add_argument(
        "--project", default=None,
        help="project to review: threev0 (default) | f1nance | axiom; "
        "overrides THREEV0_PROJECT",
    )
    args = ap.parse_args()

    if args.project:
        os.environ["THREEV0_PROJECT"] = args.project
        _resolve_project()

    if os.environ.get("THREEV0_REVIEW") == "0":
        return 0

    if args.session_id:
        status = review_one(args.session_id)
        return 1 if status == "failed" else 0

    if args.latest:
        _sync()  # heal drift first, so the review sees the reconciled store
        return _drain()

    # --daemon: 3V0's own clock — reconcile + drain the backlog every interval
    # forever, surviving transient failures (a tick error is a log line, not a
    # crash).
    _log_run(f"daemon started (interval={args.interval}s)")
    try:
        while True:
            try:
                _sync()
                _drain()
                _drift()
            except Exception as e:  # noqa: BLE001 - a daemon must not die on a tick error
                _log_run(f"daemon tick error: {e}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        _log_run("daemon stopped (keyboard interrupt)")
        return 0


_resolve_project()


if __name__ == "__main__":
    raise SystemExit(main())
