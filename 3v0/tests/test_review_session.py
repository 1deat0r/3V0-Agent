"""Tests for the Stone 7 session-end review driver (3v0/scripts/review_session.py).

Offline by construction: the LLM is faked via THREEV0_REVIEW_LLM=fake +
THREEV0_REVIEW_DECISIONS=<json file>, so no network call happens. The driver's
full CLI path (gating -> transcript -> fake model -> record.py subprocess ->
log entry) runs against temp stores/db/logs via the THREEV0_* env overrides,
the same convention as the rest of the native core.

Direct run:  python3 3v0/tests/test_review_session.py
"""

from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
THREEV0 = REPO_ROOT / "3v0"
sys.path.insert(0, str(THREEV0))
sys.path.insert(0, str(THREEV0 / "core"))

from core.memory import MemoryStore  # noqa: E402
from core.skills import ABSORBED, RETRACTED, SkillStore  # noqa: E402

DRIVER = THREEV0 / "scripts" / "review_session.py"
PLUGIN_INIT = THREEV0 / "plugin" / "native-store-bridge" / "__init__.py"


def _load_driver():
    spec = importlib.util.spec_from_file_location("review_session", DRIVER)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DRIVER_MOD = _load_driver()


def _seed_store(path: Path) -> dict:
    """A temp store with: a stale fact (to supersede), a fact to retract,
    and a healthy fact that must survive."""
    store = MemoryStore(path)
    with store.mutate():
        stale = store.add(
            "Operator prefers verbose reports.", kind="memory", source="test"
        ).id
        doomed = store.add(
            "The moon is made of cheese (wrong, superseded later).",
            kind="memory",
            source="test",
        ).id
        keeper = store.add(
            "Operator works from ~/work.", kind="user", source="test"
        ).id
    return {"stale": stale, "doomed": doomed, "keeper": keeper}


def _seed_session_db(path: Path, source: str, user_messages: int) -> str:
    """A minimal state.db with one session and a small transcript."""
    conn = sqlite3.connect(str(path))
    conn.executescript(
        """
        CREATE TABLE sessions (
            id TEXT PRIMARY KEY, source TEXT NOT NULL, title TEXT
        );
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT,
            tool_name TEXT,
            active INTEGER NOT NULL DEFAULT 1
        );
        """
    )
    sid = "test_session_01"
    conn.execute(
        "INSERT INTO sessions (id, source, title) VALUES (?, ?, ?)",
        (sid, source, "fixture session"),
    )
    for i in range(user_messages):
        conn.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, 'user', ?)",
            (sid, f"user message {i}"),
        )
    conn.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, 'assistant', ?)",
        (sid, "assistant reply"),
    )
    conn.commit()
    conn.close()
    return sid


def _seed_skill(skill_store_path: Path, skills_dir: Path, name: str, category: str = "") -> str:
    """Seed a skill into a temp skill store + project its SKILL.md into a temp
    profile skills dir. Returns the version id."""
    store = SkillStore(skill_store_path)
    content = f"---\nname: {name}\n---\n# {name} body\n"
    with store.mutate():
        v = store.add(name, "create", "test", content=content, category=category)
    target = skills_dir / category / name if category else skills_dir / name
    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(content, encoding="utf-8")
    return v.id


def _run_driver(sid: str, env: dict, expect_code: int = 0) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        [sys.executable, str(DRIVER), "--session-id", sid],
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == expect_code, (
        f"exit={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
    )
    return proc


class Env(unittest.TestCase):
    """Shared fixture scaffolding."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.store_path = base / "memory.json"
        self.ids = _seed_store(self.store_path)
        self.db_path = base / "state.db"
        self.review_log = base / "reviews" / "reviews.jsonl"
        self.profile_mem = base / "profile_memories"
        self.skill_store_path = base / "skills.json"
        self.skills_dir = base / "profile_skills"
        self.decisions_file = base / "decisions.json"
        self.env = os.environ.copy()
        self.env.update(
            {
                "THREEV0_REVIEW_STATE_DB": str(self.db_path),
                "THREEV0_STORE": str(self.store_path),
                "THREEV0_PROFILE_MEM": str(self.profile_mem),
                "THREEV0_SKILL_STORE": str(self.skill_store_path),
                "THREEV0_SKILLS_DIR": str(self.skills_dir),
                "THREEV0_REVIEW_LOG": str(self.review_log),
                "THREEV0_REVIEW_LLM": "fake",
                "THREEV0_REVIEW_DECISIONS": str(self.decisions_file),
                "THREEV0_REVIEW_COOLDOWN_S": "300",
            }
        )

    def tearDown(self):
        self.tmp.cleanup()

    def log_entries(self):
        if not self.review_log.exists():
            return []
        return [
            json.loads(line)
            for line in self.review_log.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]


class TestGating(Env):
    def test_too_few_user_messages_skips(self):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=2)
        _run_driver(sid, self.env)
        self.assertEqual(self.log_entries(), [])

    def test_non_reviewable_source_skips(self):
        sid = _seed_session_db(self.db_path, source="cron", user_messages=5)
        _run_driver(sid, self.env)
        self.assertEqual(self.log_entries(), [])

    def test_kill_switch_skips(self):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=5)
        env = dict(self.env, THREEV0_REVIEW="0")
        _run_driver(sid, env)
        self.assertEqual(self.log_entries(), [])

    def test_dedupe_skips_already_reviewed_session(self):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=5)
        self.review_log.parent.mkdir(parents=True)
        self.review_log.write_text(
            json.dumps({"session_id": sid, "at": time.time()}) + "\n",
            encoding="utf-8",
        )
        _run_driver(sid, self.env)
        entries = self.log_entries()
        self.assertEqual(len(entries), 1)  # only the pre-existing entry

    def test_cooldown_skips_recent_other_review(self):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=5)
        self.review_log.parent.mkdir(parents=True)
        self.review_log.write_text(
            json.dumps({"session_id": "other_session", "at": time.time()}) + "\n",
            encoding="utf-8",
        )
        _run_driver(sid, self.env)
        self.assertEqual(len(self.log_entries()), 1)

    def test_missing_session_skips(self):
        _run_driver("nonexistent_session", self.env)
        self.assertEqual(self.log_entries(), [])


class TestFakeLLMDecisions(Env):
    def test_record_supersede_retract(self):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=4)
        self.decisions_file.write_text(
            json.dumps(
                {
                    "summary": "corrections from the session",
                    "decisions": [
                        {
                            "action": "record",
                            "kind": "user",
                            "content": "Operator prefers terse, bulleted reports.",
                            "supersedes_id": self.ids["stale"],
                        },
                        {
                            "action": "retract",
                            "fact_id": self.ids["doomed"],
                        },
                        {
                            "action": "record",
                            "kind": "memory",
                            "content": "A new durable environment fact.",
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        _run_driver(sid, self.env)

        store = MemoryStore(self.store_path)
        active = {f.content: f for f in store.active()}
        # superseded + retracted facts are gone from the active set
        self.assertNotIn("Operator prefers verbose reports.", active)
        self.assertNotIn(
            "The moon is made of cheese (wrong, superseded later).", active
        )
        # the new facts + keeper are active
        self.assertIn("Operator prefers terse, bulleted reports.", active)
        self.assertIn("A new durable environment fact.", active)
        self.assertIn("Operator works from ~/work.", active)
        # supersession link recorded on the stale fact
        stale = next(
            f for f in store.facts if f.id == self.ids["stale"]
        )
        self.assertTrue(stale.superseded_by)
        # provenance is the review fork's own label
        new_fact = active["Operator prefers terse, bulleted reports."]
        self.assertEqual(new_fact.source, "session-review")

        # profile projection written (memory + user views)
        mem_md = (self.profile_mem / "MEMORY.md").read_text(encoding="utf-8")
        self.assertIn("A new durable environment fact.", mem_md)
        self.assertNotIn("verbose reports", mem_md)
        user_md = (self.profile_mem / "USER.md").read_text(encoding="utf-8")
        self.assertIn("terse, bulleted reports", user_md)

        entries = self.log_entries()
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["session_id"], sid)
        self.assertEqual(entry["applied"], 3)
        self.assertEqual(entry["refused"], 0)

    def test_invalid_decisions_refused_without_touching_store(self):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=4)
        before = MemoryStore(self.store_path)
        before_active = {f.id: f.content for f in before.active()}
        self.decisions_file.write_text(
            json.dumps(
                {
                    "summary": "no-op",
                    "decisions": [
                        {
                            "action": "record",
                            "kind": "not-a-kind",
                            "content": "bad kind",
                        },
                        {"action": "retract", "fact_id": ""},
                        {
                            "action": "record",
                            "kind": "memory",
                            "content": "bad § separator",
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        _run_driver(sid, self.env)

        after = MemoryStore(self.store_path)
        self.assertEqual(
            {f.id: f.content for f in after.active()}, before_active
        )
        entries = self.log_entries()
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["applied"], 0)
        self.assertEqual(entry["refused"], 3)

    def test_decisions_capped_at_three(self):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=4)
        self.decisions_file.write_text(
            json.dumps(
                {
                    "summary": "no-op",
                    "decisions": [
                        {"action": "record", "kind": "memory", "content": f"fact {i}"}
                        for i in range(5)
                    ],
                }
            ),
            encoding="utf-8",
        )
        _run_driver(sid, self.env)
        entries = self.log_entries()
        self.assertEqual(entries[0]["decisions_requested"], 5)
        self.assertEqual(entries[0]["applied"], 3)

    def test_missing_decisions_file_is_llm_failure(self):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=4)
        env = dict(self.env)
        env.pop("THREEV0_REVIEW_DECISIONS")
        _run_driver(sid, env, expect_code=1)
        self.assertEqual(self.log_entries(), [])


class TestFakeLLMSkillDecisions(Env):
    """Stone 8: the driver emits store-first skill decisions, applied through
    record_skills.py (store mutation + SKILL.md projection)."""

    def _run_skill_decisions(self, decisions, user_messages=4):
        sid = _seed_session_db(self.db_path, source="tui", user_messages=user_messages)
        self.decisions_file.write_text(
            json.dumps({"summary": "skill decisions", "decisions": decisions}),
            encoding="utf-8",
        )
        _run_driver(sid, self.env)
        return sid

    def test_skill_retract_decommissions_and_projects(self):
        _seed_skill(self.skill_store_path, self.skills_dir, "obsolete-skill")
        self._run_skill_decisions(
            [{"action": "skill_retract", "name": "obsolete-skill"}]
        )
        store = SkillStore(self.skill_store_path)
        versions = store.versions("obsolete-skill")
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0].superseded_by, RETRACTED)
        self.assertIsNone(store.latest_active("obsolete-skill"))
        # projection removed the live SKILL.md
        self.assertFalse((self.skills_dir / "obsolete-skill" / "SKILL.md").exists())
        entries = self.log_entries()
        self.assertEqual(entries[0]["applied"], 1)
        self.assertEqual(entries[0]["refused"], 0)

    def test_skill_absorb_records_umbrella(self):
        _seed_skill(self.skill_store_path, self.skills_dir, "old-skill")
        _seed_skill(self.skill_store_path, self.skills_dir, "umbrella")
        self._run_skill_decisions(
            [{"action": "skill_absorb", "name": "old-skill", "absorbed_into": "umbrella"}]
        )
        store = SkillStore(self.skill_store_path)
        self.assertEqual(store.versions("old-skill")[0].superseded_by, ABSORBED)
        self.assertEqual(store.absorbed_by("umbrella"), ["old-skill"])
        self.assertIsNotNone(store.latest_active("umbrella"))

    def test_skill_update_projects_new_content(self):
        _seed_skill(self.skill_store_path, self.skills_dir, "live-skill")
        new_content = "---\nname: live-skill\n---\n# v2\n"
        self._run_skill_decisions(
            [{"action": "skill_update", "name": "live-skill", "content": new_content}]
        )
        store = SkillStore(self.skill_store_path)
        head = store.latest_active("live-skill")
        assert head is not None  # narrow Optional for the type checker
        self.assertEqual(head.action, "edit")
        self.assertEqual(head.content, new_content.strip())
        md = (self.skills_dir / "live-skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(md, new_content)

    def test_unknown_skill_retract_refused(self):
        self._run_skill_decisions([{"action": "skill_retract", "name": "does-not-exist"}])
        entries = self.log_entries()
        self.assertEqual(entries[0]["applied"], 0)
        self.assertEqual(entries[0]["refused"], 1)


class TestUnitHelpers(unittest.TestCase):
    def test_tolerant_json_fences_and_prose(self):
        mod = DRIVER_MOD
        self.assertEqual(
            mod._tolerant_json('```json\n{"a": 1}\n```')["a"], 1
        )
        self.assertEqual(
            mod._tolerant_json('sure, here you go: {"b": 2} trailing')["b"], 2
        )
        self.assertIsNone(mod._tolerant_json("no json here"))

    def test_decision_argv_shapes(self):
        mod = DRIVER_MOD
        self.assertIsNone(mod._decision_argv({"action": "record", "kind": "x"}))
        self.assertIsNone(mod._decision_argv({"action": "retract"}))
        self.assertIsNone(mod._decision_argv({"action": "frobnicate"}))
        argv = mod._decision_argv(
            {"action": "record", "kind": "directive", "content": "stay honest"}
        )
        self.assertIn("--kind", argv)
        self.assertIn("directive", argv)
        argv = mod._decision_argv(
            {"action": "record", "kind": "memory", "content": "x",
             "supersedes_id": "abc"}
        )
        self.assertIn("--supersedes-id", argv)
        argv = mod._decision_argv(
            {"action": "record", "kind": "memory", "content": "x",
             "supersedes": "sub"}
        )
        self.assertIn("--supersedes", argv)

    def test_skill_decision_argv_shapes(self):
        mod = DRIVER_MOD
        self.assertIsNone(mod._skill_decision_argv({"action": "record"}))
        self.assertIsNone(mod._skill_decision_argv({"action": "skill_retract"}))
        self.assertIsNone(mod._skill_decision_argv({"action": "skill_update", "name": "x"}))
        self.assertIsNone(mod._skill_decision_argv({"action": "skill_absorb", "name": "x"}))
        argv = mod._skill_decision_argv({"action": "skill_retract", "name": "obsolete-skill"})
        self.assertIn("--action", argv)
        self.assertIn("skill_retract", argv)
        self.assertIn("obsolete-skill", argv)
        argv = mod._skill_decision_argv(
            {"action": "skill_absorb", "name": "a", "absorbed_into": "b"}
        )
        self.assertIn("--absorbed-into", argv)
        self.assertIn("b", argv)
        argv = mod._skill_decision_argv(
            {"action": "skill_update", "name": "a", "content": "full", "category": "cat"}
        )
        self.assertIn("--content", argv)
        self.assertIn("--category", argv)
        self.assertIn("cat", argv)

    def test_transcript_compaction(self):
        mod = DRIVER_MOD
        msgs = [
            {"role": "user", "content": "hello", "tool_name": ""},
            {"role": "assistant", "content": "hi there", "tool_name": ""},
            {"role": "assistant", "content": "", "tool_name": "terminal"},
            {"role": "tool", "content": "x" * 5000, "tool_name": ""},
        ]
        # Fits under the cap -> no trimming; tool calls appear as names and
        # tool outputs are truncated per-message.
        text = mod._build_transcript(msgs, cap=1000)
        self.assertIn("USER: hello", text)
        self.assertIn("ASSISTANT[tool terminal returned]", text)
        # tool output truncated to 300 chars -> every line stays bounded
        self.assertTrue(all(len(line) <= 320 for line in text.splitlines()))
        # Over the cap -> head+tail trim.
        big = [
            {"role": "user", "content": f"m{i}", "tool_name": ""} for i in range(200)
        ]
        text = mod._build_transcript(big, cap=500)
        self.assertIn("middle truncated", text)
        self.assertIn("USER: m0", text)          # head kept
        self.assertIn("USER: m199", text)        # tail kept
        self.assertLessEqual(len(text), 500 + 200)  # trim allowance


class TestHookSpawn(unittest.TestCase):
    """The plugin's on_session_end hook spawns the detached driver and the
    driver completes end-to-end (fake LLM)."""

    def test_hook_spawns_driver_and_logs_entry(self):
        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            store_path = base / "memory.json"
            _seed_store(store_path)
            db_path = base / "state.db"
            sid = _seed_session_db(db_path, source="tui", user_messages=4)
            review_log = base / "reviews" / "reviews.jsonl"
            decisions_file = base / "decisions.json"
            decisions_file.write_text(
                json.dumps({"summary": "hook e2e", "decisions": []}),
                encoding="utf-8",
            )

            os.environ["THREEV0_BODY"] = str(REPO_ROOT)
            os.environ["THREEV0_REVIEW_LLM"] = "fake"
            os.environ["THREEV0_REVIEW_DECISIONS"] = str(decisions_file)
            os.environ["THREEV0_REVIEW_STATE_DB"] = str(db_path)
            os.environ["THREEV0_STORE"] = str(store_path)
            os.environ["THREEV0_PROFILE_MEM"] = str(base / "profile_memories")
            os.environ["THREEV0_REVIEW_LOG"] = str(review_log)
            try:
                spec = importlib.util.spec_from_file_location(
                    "native_store_bridge", PLUGIN_INIT
                )
                assert spec is not None and spec.loader is not None
                plugin = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin)
                plugin._on_session_end(session_id=sid)

                deadline = time.time() + 15
                entries = []
                while time.time() < deadline:
                    if review_log.exists():
                        entries = [
                            json.loads(line)
                            for line in review_log.read_text(
                                encoding="utf-8"
                            ).splitlines()
                            if line.strip()
                        ]
                        if entries:
                            break
                    time.sleep(0.2)
                self.assertEqual(len(entries), 1, "hook review never logged")
                self.assertEqual(entries[0]["session_id"], sid)
                self.assertEqual(entries[0]["applied"], 0)
            finally:
                for key in (
                    "THREEV0_BODY",
                    "THREEV0_REVIEW_LLM",
                    "THREEV0_REVIEW_DECISIONS",
                    "THREEV0_REVIEW_STATE_DB",
                    "THREEV0_STORE",
                    "THREEV0_PROFILE_MEM",
                    "THREEV0_REVIEW_LOG",
                ):
                    os.environ.pop(key, None)
        finally:
            tmp.cleanup()


def _seed_rich_sessions(path: Path, rows) -> None:
    """A state.db with the *real* sessions schema shape (ended_at,
    parent_session_id, hidden, archived) and multiple sessions, so the
    --latest candidate filters can be exercised against a faithful schema."""
    conn = sqlite3.connect(str(path))
    conn.executescript(
        """
        CREATE TABLE sessions (
            id TEXT PRIMARY KEY, source TEXT NOT NULL, title TEXT,
            ended_at REAL, parent_session_id TEXT,
            hidden INTEGER NOT NULL DEFAULT 0, archived INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT,
            tool_name TEXT,
            active INTEGER NOT NULL DEFAULT 1
        );
        """
    )
    for row in rows:
        sid = row["id"]
        conn.execute(
            "INSERT INTO sessions (id, source, title, ended_at, parent_session_id, hidden, archived) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                sid,
                row.get("source", "tui"),
                row.get("title", "fixture"),
                row.get("ended_at", 1.0),
                row.get("parent_session_id"),
                row.get("hidden", 0),
                row.get("archived", 0),
            ),
        )
        for i in range(row.get("user_messages", 4)):
            conn.execute(
                "INSERT INTO messages (session_id, role, content) VALUES (?, 'user', ?)",
                (sid, f"user message {i}"),
            )
        conn.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, 'assistant', ?)",
            (sid, "assistant reply"),
        )
    conn.commit()
    conn.close()


def _run_latest(env: dict, expect_code: int = 0) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        [sys.executable, str(DRIVER), "--latest"],
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == expect_code, (
        f"exit={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
    )
    return proc


class TestLatestSelection(Env):
    """Stone 9: --latest picks the newest unreviewed *eligible* session,
    skipping live / subagent / non-reviewable / already-reviewed rows, and
    degrades to a clean no-op when nothing is eligible."""

    def _noop_decisions(self):
        self.decisions_file.write_text(
            json.dumps({"summary": "no-op", "decisions": []}), encoding="utf-8"
        )

    def _preseed_reviewed(self, sid: str):
        self.review_log.parent.mkdir(parents=True, exist_ok=True)
        self.review_log.write_text(
            # a PAST timestamp: it must dedupe without tripping the cooldown
            json.dumps({"session_id": sid, "at": time.time() - 3600}) + "\n",
            encoding="utf-8",
        )

    def test_latest_reviews_newest_unreviewed_eligible(self):
        _seed_rich_sessions(
            self.db_path,
            [
                {"id": "99999999_999999_sub", "parent_session_id": "x", "source": "tui"},
                {"id": "88888888_888888_live", "ended_at": None, "source": "tui"},
                {"id": "77777777_777777_cron", "source": "cron"},
                {"id": "66666666_666666_done", "source": "tui"},
                {"id": "55555555_555555_new", "source": "tui"},
            ],
        )
        self._noop_decisions()
        self._preseed_reviewed("66666666_666666_done")
        _run_latest(self.env)
        entries = self.log_entries()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[-1]["session_id"], "55555555_555555_new")

    def test_latest_noop_when_only_ineligible(self):
        _seed_rich_sessions(
            self.db_path,
            [
                {"id": "99999999_999999_sub", "parent_session_id": "x", "source": "tui"},
                {"id": "88888888_888888_live", "ended_at": None, "source": "tui"},
                {"id": "77777777_777777_cron", "source": "cron"},
            ],
        )
        self._noop_decisions()
        _run_latest(self.env)
        self.assertEqual(self.log_entries(), [])

    def test_latest_noop_when_all_reviewed(self):
        _seed_rich_sessions(self.db_path, [{"id": "55555555_555555_done", "source": "tui"}])
        self._noop_decisions()
        self._preseed_reviewed("55555555_555555_done")
        _run_latest(self.env)
        self.assertEqual(len(self.log_entries()), 1)  # only the pre-existing entry

    def test_latest_minimal_schema_reviews_session(self):
        # The minimal fixture has no ended_at/parent columns; the
        # column-existence-aware query must still surface the session.
        sid = _seed_session_db(self.db_path, source="tui", user_messages=4)
        self._noop_decisions()
        _run_latest(self.env)
        self.assertEqual([e["session_id"] for e in self.log_entries()], [sid])

    def test_candidate_scan_failsafe_on_unreadable_schema(self):
        # An unreadable schema must yield NO candidates — never fall through
        # to an unfiltered query that would surface still-open (live) sessions.
        os.environ["THREEV0_REVIEW_STATE_DB"] = str(self.db_path)
        os.environ["THREEV0_REVIEW_LOG"] = str(self.review_log)
        try:
            mod = _load_driver()
            with mock.patch.object(mod, "_session_columns", return_value=None):
                self.assertEqual(mod._candidate_sessions(), [])
        finally:
            os.environ.pop("THREEV0_REVIEW_STATE_DB", None)
            os.environ.pop("THREEV0_REVIEW_LOG", None)


class TestTemporalGuard(Env):
    """A review of a session that PREDATES a fact must not supersede/retract
    that fact — the reviewer cannot disprove something recorded after the
    session ended (the own-clock regression bug)."""

    def test_supersede_of_newer_fact_refused_e2e(self):
        _seed_rich_sessions(
            self.db_path,
            [{"id": "55555555_555555_old", "source": "tui", "ended_at": time.time() - 3600}],
        )
        self.decisions_file.write_text(
            json.dumps(
                {
                    "summary": "regression attempt",
                    "decisions": [
                        {"action": "record", "kind": "memory", "content": "regressed",
                         "supersedes_id": self.ids["stale"]},
                    ],
                }
            ),
            encoding="utf-8",
        )
        _run_driver("55555555_555555_old", self.env)
        entries = self.log_entries()
        self.assertEqual(entries[0]["applied"], 0)
        self.assertEqual(entries[0]["refused"], 1)
        self.assertIn("newer than session", entries[0]["refused_details"][0]["reason"])
        store = MemoryStore(self.store_path)
        self.assertTrue(store.get(self.ids["stale"]).active)  # not superseded

    def test_temporal_refusal_truth_table(self):
        mod = DRIVER_MOD
        store = MemoryStore(self.store_path)
        past, future = time.time() - 3600, time.time() + 3600
        # retract a fact NEWER than the session -> refuse
        self.assertIsNotNone(
            mod._temporal_refusal({"action": "retract", "fact_id": self.ids["stale"]}, store, past)
        )
        # retract a fact OLDER than the session -> allow
        self.assertIsNone(
            mod._temporal_refusal({"action": "retract", "fact_id": self.ids["stale"]}, store, future)
        )
        # no session timestamp -> guard off (minimal fixture path)
        self.assertIsNone(
            mod._temporal_refusal({"action": "retract", "fact_id": self.ids["stale"]}, store, None)
        )
        # supersede-by-id of a newer fact -> refuse
        self.assertIsNotNone(
            mod._temporal_refusal({"action": "record", "supersedes_id": self.ids["stale"]}, store, past)
        )
        # a plain record (no supersede) is never temporally refused
        self.assertIsNone(
            mod._temporal_refusal({"action": "record", "kind": "memory", "content": "x"}, store, past)
        )


class TestLLMEmptyContent(unittest.TestCase):
    """Stone 9 bug-fix: a reasoning model that empties ``content`` (its
    thinking consumed the token budget) must be detected and logged, not
    fail silently as a generic 'llm call failed'."""

    def test_empty_content_is_detected_and_logged(self):
        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            os.environ["THREEV0_REVIEW_LOG"] = str(base / "reviews" / "reviews.jsonl")
            os.environ["DEEPSEEK_API_KEY"] = "fake-key"
            try:
                # Fresh module load so RUN_LOG is bound to the temp path.
                mod = _load_driver()
            finally:
                pass

            fake_resp = mock.MagicMock()
            fake_resp.read.return_value = json.dumps(
                {"choices": [{"message": {"content": ""}, "finish_reason": "length"}]}
            ).encode()
            fake_resp.__enter__ = mock.MagicMock(return_value=fake_resp)
            fake_resp.__exit__ = mock.MagicMock(return_value=False)

            with mock.patch("urllib.request.urlopen", return_value=fake_resp):
                result = mod._call_llm("some prompt")

            self.assertIsNone(result)
            run_log = (base / "reviews" / "run.log").read_text(encoding="utf-8")
            self.assertIn("empty content", run_log)
            self.assertIn("finish_reason=length", run_log)
        finally:
            os.environ.pop("THREEV0_REVIEW_LOG", None)
            os.environ.pop("DEEPSEEK_API_KEY", None)
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
