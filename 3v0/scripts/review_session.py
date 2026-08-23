#!/usr/bin/env python3
"""3V0-owned session-end review — the Stone 7 decision driver.

Direction 3 closes the own-evolution loop with a *process* 3V0 itself drives:
at session end, the ``native-store-bridge`` plugin's ``on_session_end`` hook
spawns this driver as a **detached subprocess** (survives teardown; a TUI quit
kills the gateway process, which would take an in-process review thread with
it). The driver then:

1. reads the just-ended session transcript from the profile's ``state.db``,
2. reads the current canonical memory store (active facts + lineage),
3. asks the configured primary model (currently bitdeer DeepSeek-V4-Flash) for
   **store-first** decisions — record / supersede / retract,
4. applies each accepted decision through ``scripts/record.py --json --write``
   (the exact backend the ``threev0_record`` tool wraps), and
5. appends an auditable entry to a review log.

It is best-effort by construction: any failure degrades to a log entry and a
non-zero exit that the hook swallows. The wake-time ``sync.py --write`` remains
the backstop reconciler.

The 3V0 background-review fork still owns per-turn memory + in-session
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
  ``CONFIG.max_per_pass``);
- ``--daemon [--interval N]``  own-clock loop (reconcile + drain every N
  seconds, default 600), surviving transient failures — 3V0's first
  3V0-independent autonomous process. Stone 14 folded the wake-time
  reconcilers into the tick, so the daemon is now a full maintenance clock:
  it heals drift between sessions, not just at wake. Stone 16 added the
  multi-project drift check (``_drift()``); Stone 17 added the continuity
  invariant check (``_continuity()``) — both report-only, primary-project
  only.

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
  THREEV0_REVIEW_MODEL / THREEV0_REVIEW_BASE_URL / BITDEER_API_KEY
                          LLM routing (defaults: deepseek-ai/DeepSeek-V4-Flash @
                          api-inference.bitdeer.ai/v1 — the current substrate)
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.memory import KINDS  # noqa: E402
from core.store import open_store  # noqa: E402
from core.projects import ProjectSpec, resolve_project  # noqa: E402
from core.skills import SkillStore  # noqa: E402
from core.skill_outcome import extract_loaded_skills, mark_skill_outcome  # noqa: E402
from core.decide_skills import SKILL_DECISION_ACTIONS  # noqa: E402
from core.session_db import candidate_rows, load_session, session_columns  # noqa: E402
from core.review_decide import (  # noqa: E402
    build_transcript,
    parse_created_ts,
    skill_temporal_refusal,
    skills_block,
    store_block,
    temporal_refusal,
    tolerant_json,
)

# The review decision functions now live in core/review_decide.py; the
# underscore aliases keep this driver's own call sites and its tests (which
# reach into this module's namespace) unchanged. _build_transcript is a thin
# wrapper so the env-tunable CONFIG.transcript_cap default is preserved.
_tolerant_json = tolerant_json
_parse_created_ts = parse_created_ts
_temporal_refusal = temporal_refusal
_skill_temporal_refusal = skill_temporal_refusal
_store_block = store_block
_skills_block = skills_block
_SKILL_ACTIONS = SKILL_DECISION_ACTIONS


def _loaded_outcomes_block(loaded: List[str]) -> str:
    """The LOADED SKILLS (outcome) section fed to the review model.

    Lists the skills actually loaded this session (via skill_view) so the
    model can mark each success/failure/unknown from the transcript evidence.
    Empty when nothing was loaded or when there's no skill axis.
    """
    if not loaded:
        return ""
    lines = "\n".join(f"  - {name}" for name in loaded)
    return (
        "7. SKILL OUTCOME: the session loaded these skills via skill_view. "
        "From the transcript, for each, judge whether it SUCCEEDED (the task "
        "it guides completed), FAILED (the skill was wrong, misleading, or "
        "obsolete and cost the session), or was UNKNOWN (no clear signal). "
        "Emit a parallel 'skill_outcomes' object {\"skill_name\": "
        "\"success\"|\"failure\"|\"unknown\"}. Be conservative: default to "
        "unknown when unsure — this feeds durable curation, not a grade.\n\n"
        "LOADED SKILLS (outcome):\n"
        f"{lines}\n"
    )


def _build_transcript(messages: List[Dict[str, str]], cap: Optional[int] = None) -> str:
    """Compact the session into review text (env-tunable default; see
    core.review_decide.build_transcript)."""
    return build_transcript(messages, cap=CONFIG.transcript_cap if cap is None else cap)

PROFILE_HOME = Path(
    os.environ.get("THREEV0_PROFILE_HOME")
    or (Path.home() / ".3V0" / "profiles" / "3v0")
)
STATE_DB = Path(os.environ.get("THREEV0_REVIEW_STATE_DB") or (PROFILE_HOME / "state.db"))
RECORD_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "record.py"
RECORD_SKILLS_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "record_skills.py"
SYNC_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "sync.py"
SYNC_SKILLS_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "sync_skills.py"
DRIFT_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "drift_check.py"
CONTINUITY_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "continuity_check.py"

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

@dataclass(frozen=True)
class ReviewConfig:
    """The driver's knobs, resolved once from env (see the module docstring).

    One typed home for what were ten module-level globals. Frozen + built via
    ``from_env`` so a test can parse a custom environ without touching the
    live process env. The store/skill block caps now live in
    ``core.review_decide`` as ``DEFAULT_STORE_BLOCK_CAP`` /
    ``DEFAULT_SKILL_BLOCK_CAP`` (function defaults there) and no longer
    appear here.
    """

    model: str = "deepseek-ai/DeepSeek-V4-Flash"
    base_url: str = "https://api-inference.bitdeer.ai/v1"
    min_messages: int = 3
    cooldown_s: int = 300
    transcript_cap: int = 40000
    max_tokens: int = 8000
    max_decisions: int = 3
    max_per_pass: int = 30
    network_retries: int = 3
    backoff_seconds: float = 2.0

    @classmethod
    def from_env(cls, environ: Optional[Mapping[str, str]] = None) -> "ReviewConfig":
        """Build a config from env, overriding field defaults only where set.

        The dataclass field defaults are the single source of truth; this only
        layers env-provided values on top, so a default edited in one place
        can't silently disagree with a literal here.
        """
        env = os.environ if environ is None else environ
        overrides: Dict[str, Any] = {}

        def put(key: str, field: str, cast) -> None:
            value = env.get(key)
            if value:  # non-empty only; "" falls through to the field default
                overrides[field] = cast(value)

        put("THREEV0_REVIEW_MODEL", "model", str)
        put("THREEV0_REVIEW_BASE_URL", "base_url", lambda v: v.rstrip("/"))
        put("THREEV0_REVIEW_MIN_MESSAGES", "min_messages", int)
        put("THREEV0_REVIEW_COOLDOWN_S", "cooldown_s", int)
        put("THREEV0_REVIEW_TRANSCRIPT_CAP", "transcript_cap", int)
        put("THREEV0_REVIEW_MAX_TOKENS", "max_tokens", int)
        put("THREEV0_REVIEW_MAX_PER_PASS", "max_per_pass", int)
        put("THREEV0_REVIEW_BACKOFF_S", "backoff_seconds", float)
        return cls(**overrides)


CONFIG = ReviewConfig.from_env()

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
Never erased. The 3V0 profile (MEMORY.md/USER.md) is a derived view.

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
    """Bitdeer/DeepSeek API key, env-first, then the profile's .env.

    Prefers ``BITDEER_API_KEY`` (the current substrate); falls back to
    ``DEEPSEEK_API_KEY`` so older deployments still run. First found wins.
    """
    for name in ("BITDEER_API_KEY", "DEEPSEEK_API_KEY"):
        val = os.environ.get(name)
        if val:
            return val
    try:
        dotenv = PROFILE_HOME / ".env"
        for raw in dotenv.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key.strip() in ("BITDEER_API_KEY", "DEEPSEEK_API_KEY"):
                return value.strip().strip('"').strip("'") or None
    except OSError:
        pass
    return None


def _load_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Read the session row + ordered messages from the profile's state.db.

    The named-column read lives in ``core.session_db.load_session``; this
    wrapper binds the driver's ``STATE_DB``.
    """
    return load_session(STATE_DB, session_id)


def _load_canned() -> Optional[Dict[str, Any]]:
    """Offline fake-LLM mode: read the model's answer from a JSON file."""
    path = os.environ.get("THREEV0_REVIEW_DECISIONS")
    if not path:
        return None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"summary": "fake-mode parse failure", "decisions": []}


def _call_llm(prompt: str) -> Optional[Dict[str, Any]]:
    """One DeepSeek chat-completion call (JSON mode, tolerant retry).

    The review model is a reasoning model: its thinking goes to
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
        "model": CONFIG.model,
        "messages": [
            {"role": "system", "content": CHARTER},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": CONFIG.max_tokens,
    }
    attempts = [
        ("json_object", dict(body, response_format={"type": "json_object"})),
        ("plain", body),
    ]
    last_reason = "unknown"
    for label, attempt in attempts:
        for retry in range(CONFIG.network_retries):
            req = urllib.request.Request(
                f"{CONFIG.base_url}/chat/completions",
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
                if retry < CONFIG.network_retries - 1:
                    _log_run(f"llm {label} transport error, retry {retry + 1}: {e}")
                    time.sleep(CONFIG.backoff_seconds * retry)
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
    if kind not in KINDS or not content:
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
    for decision in decisions[:CONFIG.max_decisions]:
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
    inspected (a transient lock / missing DB). See
    ``core.session_db.session_columns``; this wrapper binds ``STATE_DB``."""
    return session_columns(STATE_DB)


def _candidate_sessions() -> List[tuple]:
    """Session ``(id, source)`` rows, newest first, that are 3V0's own *ended*
    top-level sessions worth considering. The DB query lives in
    ``core.session_db.candidate_rows``; this wrapper owns the fail-safe abort
    and the project-cwd filter.

    FAIL-SAFE: if the schema cannot be inspected (``_session_columns`` returns
    None), return [] — never fall through to an unfiltered query that would
    surface still-open (live) sessions."""
    cols = _session_columns()
    if cols is None:
        _log_run("candidate scan aborted: sessions schema unreadable")
        return []
    out = []
    for r in candidate_rows(STATE_DB, cols):
        if "cwd" in r and not _is_project_cwd(r["cwd"]):
            continue  # a sibling project's session — not 3V0's own work
        out.append((r["id"], r["source"] or ""))
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
                if isinstance(at, (int, float)) and (now - at) < CONFIG.cooldown_s:
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
        if n_user < CONFIG.min_messages:
            return "skipped:min_messages"

        transcript = _build_transcript(session["messages"])
        store = open_store(STORE_PATH)
        skill_store = SkillStore(SKILL_STORE_PATH) if SKILL_STORE_PATH else None
        skills_part = (
            _skills_block(skill_store)
            if skill_store
            else "ACTIVE SKILLS: (none — memory-only project)\n"
        )
        # Outcome capture: which skills did this session actually load? The
        # model marks success/failure/unknown from the transcript evidence
        # (advisory — the same discipline as the rest of the review), and the
        # driver persists it onto the store's meta.
        loaded = extract_loaded_skills(session["messages"])
        outcomes_part = (
            _loaded_outcomes_block(loaded) if (skill_store and loaded) else ""
        )
        prompt = (
            f"Session {session_id} (title: {session['title'] or 'untitled'}) "
            f"just ended.\n\n"
            f"{_store_block(store)}\n\n"
            f"{skills_part}\n\n"
            f"{outcomes_part}"
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

        # Persist the model's skill-outcome judgments (best-effort; a failure
        # here is a log line, never a review failure).
        raw_outcomes = answer.get("skill_outcomes") if isinstance(answer, dict) else None
        skill_outcomes: Dict[str, str] = {}
        if isinstance(raw_outcomes, dict) and skill_store is not None:
            skill_outcomes = {
                str(k): str(v) for k, v in raw_outcomes.items() if isinstance(v, str)
            }
            try:
                mark_skill_outcome(skill_store, session_id, skill_outcomes)
            except Exception as e:  # noqa: BLE001 - best-effort observer
                _log_run(f"review {session_id}: outcome capture failed: {e}")

        entry = {
            "session_id": session_id,
            "at": now,
            "skill_outcomes": skill_outcomes,
            "loaded_skills": loaded,
            "source": session["source"],
            "model": CONFIG.model,
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

    Stone 14 (the wake-sync fold): with the 3V0 background-review fork cut,
    the own clock is the sole autonomous writer — so it must also heal drift,
    not just review. The reconcilers are idempotent, ``flock``-locked (via
    ``mutate()``), and cheap (no LLM). Returns ``"synced"`` or
    ``"sync-failed:<script>"``; a failure is a log line, never a crash, and
    the next tick retries.

    This runs only on the own-clock paths (``--latest`` / ``--daemon``), not
    the per-turn ``--session-id`` hook — sync there would be redundant churn.

    Store-only projects (siblings) have no 3V0 profile projection to
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
    (newest first) in one pass, up to ``CONFIG.max_per_pass`` LLM attempts.

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
        if attempted >= CONFIG.max_per_pass:
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


def _continuity() -> str:
    """Run the continuity invariant check (Stone 17's clock) and log a summary.

    Report-only: it never heals and never writes any artifact — mechanical
    heal is a deliberate ``--heal`` (or wake) act, and semantic drift is a
    deliberate-repair flag. Same posture as ``_drift()``: primary-project
    only, best-effort, a failure is a log line, never a crash.

    Runs *before* ``_sync()`` in the tick so the two healable invariants
    observe pre-heal drift — check-after-heal makes them structurally
    self-fulfilling (Stone 17 fix, found by an adversarial grill 2026-08-16).
    """
    if not PRIMARY:
        return "skipped:not-primary"
    try:
        proc = subprocess.run(
            [sys.executable, str(CONTINUITY_SCRIPT), "--json"],
            capture_output=True, text=True, timeout=120,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        _log_run(f"continuity check failed: {e}")
        return f"continuity-failed:{e}"
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().replace("\n", " ")[:200]
        _log_run(f"continuity check returned {proc.returncode}: {tail}")
        return "continuity-failed"
    try:
        result = json.loads(proc.stdout) if proc.stdout.strip() else {}
    except json.JSONDecodeError:
        _log_run("continuity check output unparseable")
        return "continuity-failed"
    total = result.get("total", 0)
    drifting = result.get("drift_count", 0)
    names = [
        r.get("name", "?")
        for r in result.get("invariants", [])
        if isinstance(r, dict) and r.get("drift")
    ]
    suffix = f" ({', '.join(names)})" if names else ""
    _log_run(f"continuity pass: {drifting}/{total} drifting{suffix}")
    return "continuity-ok"


def _tick() -> None:
    """One maintenance-clock pass (Stone 17 fix): report continuity invariants
    BEFORE healing, so the clock can observe pre-heal drift.

    Order is load-bearing: ``_continuity()`` first — the two healable
    invariants (``memory-profile``, ``skills-store``) must see the
    store/profile state as it stands before ``_sync()`` reconciles it,
    otherwise they are structurally self-fulfilling and can never fire.
    ``_sync()`` then heals, ``_drain()`` reviews against the reconciled store,
    and ``_drift()`` reports the multi-project ledger (independent of the
    store/profile axis)."""
    _continuity()
    _sync()
    _drain()
    _drift()


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

    # --daemon: 3V0's own clock — report continuity invariants (pre-heal),
    # reconcile, drain the backlog, and report drift every interval forever,
    # surviving transient failures (a tick error is a log line, not a crash).
    _log_run(f"daemon started (interval={args.interval}s)")
    try:
        while True:
            try:
                _tick()
            except Exception as e:  # noqa: BLE001 - a daemon must not die on a tick error
                _log_run(f"daemon tick error: {e}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        _log_run("daemon stopped (keyboard interrupt)")
        return 0


_resolve_project()


if __name__ == "__main__":
    raise SystemExit(main())
