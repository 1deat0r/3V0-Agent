"""Tests for the Stone 7 session-end review driver (3v0/scripts/review_session.py).

Offline by construction: the LLM is faked via THREEV0_REVIEW_LLM=fake +
THREEV0_REVIEW_DECISIONS=<json file>, so no network call happens. The driver's
full CLI path (gating -> transcript -> fake model -> record.py subprocess ->
log entry) runs against temp stores/db/logs via the THREEV0_* env overrides,
the same convention as the rest of the native core.

Direct run:  python3 3v0/tests/test_review_session.py
"""

from __future__ import annotations

import dataclasses
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
    # @dataclass resolves cls.__module__ via sys.modules; without this the
    # driver's ReviewConfig dataclass fails at class creation.
    sys.modules["review_session"] = mod
    spec.loader.exec_module(mod)
    return mod


DRIVER_MOD = _load_driver()


class TestReviewConfig(unittest.TestCase):
    """Ten module-level config globals -> one typed ReviewConfig (the Stone-18
    deepening that closed architecture candidate #1a)."""

    def test_defaults(self):
        cfg = DRIVER_MOD.ReviewConfig.from_env({})
        self.assertEqual(cfg.model, "deepseek-v4-pro")
        self.assertEqual(cfg.base_url, "https://api.deepseek.com/v1")
        self.assertEqual(cfg.min_messages, 3)
        self.assertEqual(cfg.cooldown_s, 300)
        self.assertEqual(cfg.transcript_cap, 40000)
        self.assertEqual(cfg.max_tokens, 8000)
        self.assertEqual(cfg.max_decisions, 3)
        self.assertEqual(cfg.max_per_pass, 30)
        self.assertEqual(cfg.network_retries, 3)
        self.assertEqual(cfg.backoff_seconds, 2.0)

    def test_env_override_and_strip(self):
        cfg = DRIVER_MOD.ReviewConfig.from_env({
            "THREEV0_REVIEW_MODEL": "test-model",
            "THREEV0_REVIEW_BASE_URL": "https://example.com/v1/",
            "THREEV0_REVIEW_MAX_TOKENS": "1234",
            "THREEV0_REVIEW_MAX_PER_PASS": "5",
            "THREEV0_REVIEW_BACKOFF_S": "1.5",
        })
        self.assertEqual(cfg.model, "test-model")
        self.assertEqual(cfg.base_url, "https://example.com/v1")  # trailing / stripped
        self.assertEqual(cfg.max_tokens, 1234)
        self.assertEqual(cfg.max_per_pass, 5)
        self.assertEqual(cfg.backoff_seconds, 1.5)

    def test_empty_env_falls_through_to_default(self):
        cfg = DRIVER_MOD.ReviewConfig.from_env({"THREEV0_REVIEW_MAX_TOKENS": ""})
        self.assertEqual(cfg.max_tokens, 8000)

    def test_frozen(self):
        cfg = DRIVER_MOD.ReviewConfig.from_env({})
        with self.assertRaises(dataclasses.FrozenInstanceError):
            cfg.max_tokens = 9999


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
            hidden INTEGER NOT NULL DEFAULT 0, archived INTEGER NOT NULL DEFAULT 0,
            cwd TEXT NOT NULL DEFAULT ''
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
            "INSERT INTO sessions (id, source, title, ended_at, parent_session_id, hidden, archived, cwd) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                sid,
                row.get("source", "tui"),
                row.get("title", "fixture"),
                row.get("ended_at", 1.0),
                row.get("parent_session_id"),
                row.get("hidden", 0),
                row.get("archived", 0),
                row.get("cwd", ""),
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


class TestSkillTemporalGuard(Env):
    """A review of a session that PREDATES a skill's active version must not
    decommission/replace that skill — the reviewer cannot disprove something
    recorded after the session ended (the skill-axis counterpart of the memory
    temporal guard)."""

    def test_skill_temporal_refusal_truth_table(self):
        mod = DRIVER_MOD
        _seed_skill(self.skill_store_path, self.skills_dir, "some-skill")
        skill_store = SkillStore(self.skill_store_path)
        past, future = time.time() - 3600, time.time() + 3600
        # decommission/replace a skill NEWER than the session -> refuse
        self.assertIsNotNone(
            mod._skill_temporal_refusal(
                {"action": "skill_retract", "name": "some-skill"}, skill_store, past
            )
        )
        self.assertIsNotNone(
            mod._skill_temporal_refusal(
                {"action": "skill_absorb", "name": "some-skill", "absorbed_into": "u"},
                skill_store, past,
            )
        )
        self.assertIsNotNone(
            mod._skill_temporal_refusal(
                {"action": "skill_update", "name": "some-skill", "content": "x"},
                skill_store, past,
            )
        )
        # a skill OLDER than the session -> allow
        self.assertIsNone(
            mod._skill_temporal_refusal(
                {"action": "skill_retract", "name": "some-skill"}, skill_store, future
            )
        )
        # no session timestamp -> guard off (minimal fixture path)
        self.assertIsNone(
            mod._skill_temporal_refusal(
                {"action": "skill_retract", "name": "some-skill"}, skill_store, None
            )
        )
        # a non-skill action is not guarded here (handled by _temporal_refusal)
        self.assertIsNone(
            mod._skill_temporal_refusal(
                {"action": "record", "kind": "memory", "content": "x"}, skill_store, past
            )
        )
        # a skill with no active version is not guarded (backend refuses/creates)
        self.assertIsNone(
            mod._skill_temporal_refusal(
                {"action": "skill_retract", "name": "no-such-skill"}, skill_store, past
            )
        )
        # no skill store -> guard off
        self.assertIsNone(
            mod._skill_temporal_refusal(
                {"action": "skill_retract", "name": "some-skill"}, None, past
            )
        )

    def test_skill_retract_of_newer_version_refused_e2e(self):
        _seed_skill(self.skill_store_path, self.skills_dir, "fresh-skill")
        _seed_rich_sessions(
            self.db_path,
            [{"id": "55555555_555555_old", "source": "tui",
              "ended_at": time.time() - 3600, "user_messages": 4}],
        )
        self.decisions_file.write_text(
            json.dumps(
                {
                    "summary": "regression attempt",
                    "decisions": [{"action": "skill_retract", "name": "fresh-skill"}],
                }
            ),
            encoding="utf-8",
        )
        _run_driver("55555555_555555_old", self.env)
        entries = self.log_entries()
        self.assertEqual(entries[0]["applied"], 0)
        self.assertEqual(entries[0]["refused"], 1)
        self.assertIn("newer than session", entries[0]["refused_details"][0]["reason"])
        store = SkillStore(self.skill_store_path)
        self.assertIsNotNone(store.latest_active("fresh-skill"))  # not retracted
        # projection untouched
        self.assertTrue((self.skills_dir / "fresh-skill" / "SKILL.md").exists())


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


class TestProjectScoping(Env):
    """3V0's reviewer must not fold sibling projects' sessions (F1NANCE,
    Axiom) into 3V0's store — sessions are scoped by cwd."""

    def test_is_project_cwd_truth_table(self):
        mod = DRIVER_MOD
        root = str(mod.REPO_ROOT)
        self.assertTrue(mod._is_project_cwd(root))
        self.assertTrue(mod._is_project_cwd(root + "/sub"))
        self.assertTrue(mod._is_project_cwd(str(Path.home())))
        self.assertTrue(mod._is_project_cwd(""))
        self.assertTrue(mod._is_project_cwd(None))
        self.assertFalse(mod._is_project_cwd("/home/mustbearn/Projects/axiom-agent"))
        self.assertFalse(
            mod._is_project_cwd("/home/mustbearn/Projects/AI Agents/F1NANCE Agent")
        )

    def test_candidate_scan_excludes_sibling_projects(self):
        _seed_rich_sessions(
            self.db_path,
            [
                {"id": "88888888_888888_axiom", "source": "tui", "cwd": "/home/mustbearn/Projects/axiom-agent"},
                {"id": "77777777_777777_fin", "source": "tui", "cwd": "/home/mustbearn/Projects/AI Agents/F1NANCE Agent"},
                {"id": "66666666_666666_3v0", "source": "tui", "cwd": str(REPO_ROOT)},
                {"id": "55555555_555555_home", "source": "tui", "cwd": str(Path.home())},
            ],
        )
        os.environ["THREEV0_REVIEW_STATE_DB"] = str(self.db_path)
        os.environ["THREEV0_REVIEW_LOG"] = str(self.review_log)
        try:
            mod = _load_driver()
            ids = [sid for sid, _ in mod._candidate_sessions()]
            self.assertIn("66666666_666666_3v0", ids)
            self.assertIn("55555555_555555_home", ids)
            self.assertNotIn("88888888_888888_axiom", ids)
            self.assertNotIn("77777777_777777_fin", ids)
        finally:
            os.environ.pop("THREEV0_REVIEW_STATE_DB", None)
            os.environ.pop("THREEV0_REVIEW_LOG", None)

    def test_review_skips_sibling_project_session(self):
        _seed_rich_sessions(
            self.db_path,
            [{"id": "88888888_888888_axiom", "source": "tui",
              "cwd": "/home/mustbearn/Projects/axiom-agent", "user_messages": 4}],
        )
        self.decisions_file.write_text(
            json.dumps({"summary": "no-op", "decisions": []}), encoding="utf-8"
        )
        _run_driver("88888888_888888_axiom", self.env)
        self.assertEqual(self.log_entries(), [])  # cwd guard skips it


class TestSiblingProjects(Env):
    """Stone 15: per-project reviewers. A sibling project's own ``--project``
    pass reviews its sessions into its own store, store-only (no profile
    projection) and memory-only (no skill axis), and is strict about cwd (no
    fail-open — an empty/unknown cwd is skipped, never folded in)."""

    def _f1_env(self, f1_root: Path) -> dict:
        return dict(
            self.env,
            THREEV0_PROJECT="f1nance",
            THREEV0_PROJECT_CWD=str(f1_root),
        )

    def test_sibling_reviews_own_session_store_only(self):
        f1_root = Path(self.tmp.name) / "F1NANCE Agent"
        f1_root.mkdir(parents=True)
        _seed_rich_sessions(
            self.db_path,
            [{"id": "11111111_111111_f1", "source": "tui", "cwd": str(f1_root)}],
        )
        self.decisions_file.write_text(
            json.dumps(
                {
                    "summary": "capture a F1NANCE fact",
                    "decisions": [
                        {
                            "action": "record",
                            "kind": "memory",
                            "content": "F1NANCE: market-data stack is yfinance+FRED+EDGAR.",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        _run_driver("11111111_111111_f1", self._f1_env(f1_root))

        store = MemoryStore(self.store_path)
        active = {f.content for f in store.active()}
        self.assertIn("F1NANCE: market-data stack is yfinance+FRED+EDGAR.", active)
        # store-only: no profile projection was written
        self.assertFalse((self.profile_mem / "MEMORY.md").exists())
        self.assertFalse((self.profile_mem / "USER.md").exists())
        entry = self.log_entries()[0]
        self.assertEqual(entry["session_id"], "11111111_111111_f1")
        self.assertEqual(entry["applied"], 1)

    def test_sibling_skips_primary_project_session(self):
        f1_root = Path(self.tmp.name) / "F1NANCE Agent"
        f1_root.mkdir(parents=True)
        _seed_rich_sessions(
            self.db_path,
            [{"id": "22222222_222222_3v0", "source": "tui", "cwd": str(REPO_ROOT)}],
        )
        self.decisions_file.write_text(
            json.dumps({"summary": "no-op", "decisions": []}), encoding="utf-8"
        )
        _run_driver("22222222_222222_3v0", self._f1_env(f1_root))
        self.assertEqual(self.log_entries(), [])  # skipped:project

    def test_sibling_is_strict_on_empty_cwd(self):
        # A session with no cwd is NOT the sibling's — strict (no fail-open),
        # unlike the primary reviewer.
        f1_root = Path(self.tmp.name) / "F1NANCE Agent"
        f1_root.mkdir(parents=True)
        _seed_rich_sessions(
            self.db_path,
            [{"id": "33333333_333333_nocwd", "source": "tui", "cwd": ""}],
        )
        self.decisions_file.write_text(
            json.dumps({"summary": "no-op", "decisions": []}), encoding="utf-8"
        )
        _run_driver("33333333_333333_nocwd", self._f1_env(f1_root))
        self.assertEqual(self.log_entries(), [])

    def test_sibling_refuses_skill_decisions(self):
        # Memory-only: a skill_retract emitted by the model is refused, never
        # routed to record_skills.py (which would hit 3V0's skill store).
        f1_root = Path(self.tmp.name) / "F1NANCE Agent"
        f1_root.mkdir(parents=True)
        _seed_rich_sessions(
            self.db_path,
            [{"id": "44444444_444444_skill", "source": "tui", "cwd": str(f1_root)}],
        )
        self.decisions_file.write_text(
            json.dumps(
                {
                    "summary": "bogus skill decision",
                    "decisions": [
                        {"action": "skill_retract", "name": "some-skill"},
                        {
                            "action": "record",
                            "kind": "memory",
                            "content": "F1NANCE fact.",
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        _run_driver("44444444_444444_skill", self._f1_env(f1_root))
        entry = self.log_entries()[0]
        self.assertEqual(entry["applied"], 1)      # the memory record
        self.assertEqual(entry["refused"], 1)      # the skill decision
        self.assertIn("skill axis disabled", entry["refused_details"][0]["reason"])


class TestMirrorScoping(unittest.TestCase):
    """Stone 10: the write mirror is scoped to 3V0's own sessions by cwd.

    The plugin's ``_on_post_tool_call`` mirrors ``memory``/``skill_manage``
    writes into 3V0's native stores. That must only happen for 3V0's own
    sessions — sibling projects (F1NANCE, Axiom) share this profile's
    state.db and their sessions must not leak facts into 3V0's stores.
    """

    def _load_plugin(self):
        spec = importlib.util.spec_from_file_location(
            "native_store_bridge_scoping", PLUGIN_INIT
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_is_threev0_cwd_pure(self):
        mod = self._load_plugin()
        body = Path("/home/me/Projects/AI Agents/3V0 Agent")
        # fail-open on empty/None (primary project)
        self.assertTrue(mod._is_threev0_cwd("", body))
        self.assertTrue(mod._is_threev0_cwd(None, body))
        # 3V0's own: the repo, a subdir, or $HOME
        self.assertTrue(mod._is_threev0_cwd(str(body), body))
        self.assertTrue(mod._is_threev0_cwd(str(body) + "/3v0/data", body))
        self.assertTrue(mod._is_threev0_cwd(str(Path.home()), body))
        # sibling projects must be rejected
        self.assertFalse(mod._is_threev0_cwd("/home/me/Projects/axiom-agent", body))
        self.assertFalse(
            mod._is_threev0_cwd("/home/me/Projects/AI Agents/F1NANCE Agent", body)
        )

    def test_session_cwd_lookup_and_gate(self):
        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            body = base / "3V0 Agent"
            db = base / "state.db"
            conn = sqlite3.connect(str(db))
            conn.executescript(
                "CREATE TABLE sessions (id TEXT PRIMARY KEY, source TEXT NOT NULL, cwd TEXT);"
            )
            conn.execute(
                "INSERT INTO sessions (id, source, cwd) VALUES ('s_3v0', 'tui', ?)",
                (str(body),),
            )
            conn.execute(
                "INSERT INTO sessions (id, source, cwd) VALUES ('s_sibling', 'tui', ?)",
                (str(base / "axiom-agent"),),
            )
            conn.execute(
                "INSERT INTO sessions (id, source, cwd) VALUES ('s_empty', 'tui', '')"
            )
            conn.commit()
            conn.close()

            mod = self._load_plugin()
            with mock.patch.object(mod, "_profile_home", return_value=base), \
                 mock.patch.object(mod, "_resolve_body_root", return_value=body):
                # fail-open: no id, unknown id, or empty cwd -> treated as 3V0
                self.assertTrue(mod._session_is_threev0(""))
                self.assertTrue(mod._session_is_threev0("s_missing"))
                self.assertTrue(mod._session_is_threev0("s_empty"))
                # 3V0's own repo -> admitted
                self.assertTrue(mod._session_is_threev0("s_3v0"))
                # sibling repo -> blocked
                self.assertFalse(mod._session_is_threev0("s_sibling"))
        finally:
            tmp.cleanup()

    def test_session_cwd_missing_column_fails_open(self):
        # The minimal test-fixture schema has no cwd column -> fail-open.
        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            db = base / "state.db"
            conn = sqlite3.connect(str(db))
            conn.executescript(
                "CREATE TABLE sessions (id TEXT PRIMARY KEY, source TEXT NOT NULL);"
            )
            conn.execute("INSERT INTO sessions (id, source) VALUES ('s', 'tui')")
            conn.commit()
            conn.close()
            mod = self._load_plugin()
            with mock.patch.object(mod, "_profile_home", return_value=base):
                self.assertIsNone(mod._session_cwd("s"))
                self.assertTrue(mod._session_is_threev0("s"))
        finally:
            tmp.cleanup()

    def test_mirror_memory_skips_sibling_session(self):
        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            body = base / "3V0 Agent"
            db = base / "state.db"
            conn = sqlite3.connect(str(db))
            conn.executescript(
                "CREATE TABLE sessions (id TEXT PRIMARY KEY, source TEXT NOT NULL, cwd TEXT);"
            )
            conn.execute(
                "INSERT INTO sessions (id, source, cwd) VALUES ('s_sibling', 'tui', ?)",
                (str(base / "F1NANCE Agent"),),
            )
            conn.commit()
            conn.close()

            mod = self._load_plugin()
            with mock.patch.object(mod, "_profile_home", return_value=base), \
                 mock.patch.object(mod, "_resolve_body_root", return_value=body), \
                 mock.patch.object(mod, "_run_ingest") as run_ingest:
                mod._mirror_memory(
                    {"target": "memory", "action": "add", "content": "leak me"},
                    json.dumps({"success": True}),
                    session_id="s_sibling",
                )
                run_ingest.assert_not_called()
        finally:
            tmp.cleanup()

    def test_mirror_skill_skips_sibling_session(self):
        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            body = base / "3V0 Agent"
            db = base / "state.db"
            conn = sqlite3.connect(str(db))
            conn.executescript(
                "CREATE TABLE sessions (id TEXT PRIMARY KEY, source TEXT NOT NULL, cwd TEXT);"
            )
            conn.execute(
                "INSERT INTO sessions (id, source, cwd) VALUES ('s_sibling', 'tui', ?)",
                (str(base / "axiom-agent"),),
            )
            conn.commit()
            conn.close()

            mod = self._load_plugin()
            with mock.patch.object(mod, "_profile_home", return_value=base), \
                 mock.patch.object(mod, "_resolve_body_root", return_value=body), \
                 mock.patch.object(mod, "_run_ingest") as run_ingest:
                mod._mirror_skill(
                    {"name": "some-skill", "action": "create"},
                    json.dumps({"success": True}),
                    session_id="s_sibling",
                )
                run_ingest.assert_not_called()
        finally:
            tmp.cleanup()

    def test_mirror_memory_fail_open_still_mirrors(self):
        # A missing session id must NOT block the primary project's mirror.
        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            body = base / "body"
            scripts = body / "3v0" / "scripts"
            scripts.mkdir(parents=True)
            (scripts / "ingest.py").write_text("", encoding="utf-8")

            mod = self._load_plugin()
            with mock.patch.object(mod, "_profile_home", return_value=base), \
                 mock.patch.object(mod, "_resolve_body_root", return_value=body), \
                 mock.patch.object(mod, "_run_ingest") as run_ingest:
                mod._mirror_memory(
                    {"target": "memory", "action": "add", "content": "a fact"},
                    json.dumps({"success": True}),
                    session_id="",
                )
                run_ingest.assert_called_once()
        finally:
            tmp.cleanup()


class TestDrainBacklog(Env):
    """Stone 12: the own clock drains the unreviewed backlog back-to-back
    (no global cooldown), up to a per-pass cap, and survives per-session
    failures instead of aborting."""

    def _noop_decisions(self):
        self.decisions_file.write_text(
            json.dumps({"summary": "no-op", "decisions": []}), encoding="utf-8"
        )

    def test_drain_reviews_all_unreviewed_newest_first(self):
        _seed_rich_sessions(
            self.db_path,
            [
                {"id": "77777777_777777_s3", "source": "tui"},
                {"id": "66666666_666666_s2", "source": "tui"},
                {"id": "55555555_555555_s1", "source": "tui"},
            ],
        )
        self._noop_decisions()
        _run_latest(self.env)
        self.assertEqual(
            [e["session_id"] for e in self.log_entries()],
            ["77777777_777777_s3", "66666666_666666_s2", "55555555_555555_s1"],
        )

    def test_drain_respects_per_pass_cap(self):
        _seed_rich_sessions(
            self.db_path,
            [
                {"id": "88888888_888888_s4", "source": "tui"},
                {"id": "77777777_777777_s3", "source": "tui"},
                {"id": "66666666_666666_s2", "source": "tui"},
                {"id": "55555555_555555_s1", "source": "tui"},
            ],
        )
        self._noop_decisions()
        env = dict(self.env, THREEV0_REVIEW_MAX_PER_PASS="2")
        _run_latest(env)
        self.assertEqual(len(self.log_entries()), 2)

    def test_drain_continues_after_failure(self):
        _seed_rich_sessions(
            self.db_path,
            [
                {"id": "77777777_777777_b", "source": "tui"},
                {"id": "66666666_666666_a", "source": "tui"},
            ],
        )
        os.environ["THREEV0_REVIEW_STATE_DB"] = str(self.db_path)
        os.environ["THREEV0_REVIEW_LOG"] = str(self.review_log)
        try:
            mod = _load_driver()
            with mock.patch.object(
                mod, "review_one", side_effect=["failed", "reviewed"]
            ) as review_one:
                self.assertEqual(mod._drain(), 0)
            self.assertEqual(review_one.call_count, 2)  # did not abort after the failure
        finally:
            os.environ.pop("THREEV0_REVIEW_STATE_DB", None)
            os.environ.pop("THREEV0_REVIEW_LOG", None)


class TestSyncFold(Env):
    """Stone 14: the own clock now heals store<->profile drift — the wake-time
    reconcilers (sync.py + sync_skills.py) are folded into the maintenance
    tick, run before the drain. With the Hermes fork cut, this makes the
    daemon a full maintenance clock (heal + review), not a review-only loop."""

    def _noop_decisions(self):
        self.decisions_file.write_text(
            json.dumps({"summary": "no-op", "decisions": []}), encoding="utf-8"
        )

    def test_latest_imports_profile_only_fact(self):
        # A profile MEMORY.md entry the store lacks (a bridge-missed write)
        # must be imported into the store by the own-clock sync pass. This is
        # also the guard that sync.py honors the THREEV0_STORE /
        # THREEV0_PROFILE_MEM overrides — without them the import would land
        # in the real store and the temp store would stay untouched.
        self.profile_mem.mkdir(parents=True, exist_ok=True)
        (self.profile_mem / "MEMORY.md").write_text(
            "Operator drives a manual-shift car.\n", encoding="utf-8"
        )
        (self.profile_mem / "USER.md").write_text("", encoding="utf-8")
        _seed_rich_sessions(
            self.db_path, [{"id": "55555555_555555_s1", "source": "tui"}]
        )
        self._noop_decisions()
        _run_latest(self.env)

        store = MemoryStore(self.store_path)
        active = {f.content for f in store.active()}
        self.assertIn("Operator drives a manual-shift car.", active)

    def test_sync_fails_gracefully_on_bad_script(self):
        # A sync subprocess that fails to launch must not crash the tick —
        # _sync returns a 'sync-failed' status and the drain still runs.
        # Load a fresh driver with the review log redirected to a temp path so
        # the failure's _log_run call does not write to the real run.log.
        os.environ["THREEV0_REVIEW_LOG"] = str(self.review_log)
        try:
            mod = _load_driver()
            with mock.patch.object(
                mod.subprocess, "run", side_effect=OSError("no such script")
            ):
                status = mod._sync()
            self.assertEqual(status, "sync-failed:sync.py")
        finally:
            os.environ.pop("THREEV0_REVIEW_LOG", None)


class TestContinuityTick(Env):
    """Stone 17: the own clock also runs the continuity invariant check
    (report-only, primary-project only). The wrapper is a thin subprocess
    mirror of ``_drift()``; its decision logic is tested in
    ``test_continuity.py`` — here we lock the tick's two safety properties:
    primary-only, and a failure is a status string, never a crash."""

    def test_not_primary_skips(self):
        os.environ["THREEV0_REVIEW_LOG"] = str(self.review_log)
        try:
            mod = _load_driver()
            setattr(mod, "PRIMARY", False)
            self.assertEqual(mod._continuity(), "skipped:not-primary")
        finally:
            os.environ.pop("THREEV0_REVIEW_LOG", None)

    def test_clean_report_is_ok(self):
        os.environ["THREEV0_REVIEW_LOG"] = str(self.review_log)
        try:
            mod = _load_driver()
            clean = json.dumps({"total": 5, "drift_count": 0, "invariants": []})
            with mock.patch.object(
                mod.subprocess, "run",
                return_value=mock.Mock(returncode=0, stdout=clean, stderr=""),
            ):
                status = mod._continuity()
            self.assertEqual(status, "continuity-ok")
        finally:
            os.environ.pop("THREEV0_REVIEW_LOG", None)

    def test_bad_script_fails_gracefully(self):
        os.environ["THREEV0_REVIEW_LOG"] = str(self.review_log)
        try:
            mod = _load_driver()
            with mock.patch.object(
                mod.subprocess, "run", side_effect=OSError("no such script")
            ):
                status = mod._continuity()
            self.assertTrue(status.startswith("continuity-failed"))
        finally:
            os.environ.pop("THREEV0_REVIEW_LOG", None)


class TestTickOrder(Env):
    """Stone 17 fix: the tick must report continuity BEFORE healing, so the two
    healable invariants observe pre-heal drift instead of being structurally
    self-fulfilling (check-after-heal — found by an adversarial grill,
    2026-08-16)."""

    def test_tick_checks_continuity_before_syncing(self):
        os.environ["THREEV0_REVIEW_LOG"] = str(self.review_log)
        try:
            mod = _load_driver()
            order = []

            def rec(name):
                return lambda: order.append(name)

            with mock.patch.object(mod, "_continuity", side_effect=rec("continuity")), \
                    mock.patch.object(mod, "_sync", side_effect=rec("sync")), \
                    mock.patch.object(mod, "_drain", side_effect=rec("drain")), \
                    mock.patch.object(mod, "_drift", side_effect=rec("drift")):
                mod._tick()
            self.assertEqual(order, ["continuity", "sync", "drain", "drift"])
        finally:
            os.environ.pop("THREEV0_REVIEW_LOG", None)


class TestLLMRetry(unittest.TestCase):
    """Stone 12: transient transport errors are retried with backoff inside a
    single review; malformed payloads and empty content are not retried as
    transport errors."""

    def _fresh_driver(self, base):
        os.environ["THREEV0_REVIEW_LOG"] = str(base / "reviews" / "reviews.jsonl")
        os.environ["DEEPSEEK_API_KEY"] = "fake-key"
        os.environ["THREEV0_REVIEW_BACKOFF_S"] = "0"
        return _load_driver()

    def _cleanup(self):
        os.environ.pop("THREEV0_REVIEW_LOG", None)
        os.environ.pop("DEEPSEEK_API_KEY", None)
        os.environ.pop("THREEV0_REVIEW_BACKOFF_S", None)

    def test_transport_error_retries_then_succeeds(self):
        import urllib.error

        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            mod = self._fresh_driver(base)
            good = json.dumps(
                {"choices": [{"message": {"content": '{"summary":"ok","decisions":[]}'},
                              "finish_reason": "stop"}]}
            ).encode()
            calls = []

            def side_effect(*a, **kw):
                calls.append(1)
                if len(calls) <= 2:
                    raise urllib.error.URLError("boom")
                resp = mock.MagicMock()
                resp.read.return_value = good
                resp.__enter__ = mock.MagicMock(return_value=resp)
                resp.__exit__ = mock.MagicMock(return_value=False)
                return resp

            with mock.patch("urllib.request.urlopen", side_effect=side_effect):
                result = mod._call_llm("prompt")

            self.assertIsNotNone(result)
            self.assertEqual(result["summary"], "ok")
            self.assertEqual(len(calls), 3)  # 2 failures + 1 success
        finally:
            self._cleanup()
            tmp.cleanup()

    def test_transport_error_exhausts_retries(self):
        import urllib.error

        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            mod = self._fresh_driver(base)
            calls = []

            def side_effect(*a, **kw):
                calls.append(1)
                raise urllib.error.URLError("boom")

            with mock.patch("urllib.request.urlopen", side_effect=side_effect):
                result = mod._call_llm("prompt")

            self.assertIsNone(result)
            # 2 labels (json_object, plain) x network_retries each
            self.assertEqual(len(calls), mod.CONFIG.network_retries * 2)
            run_log = (base / "reviews" / "run.log").read_text(encoding="utf-8")
            self.assertIn("llm call failed after retries", run_log)
        finally:
            self._cleanup()
            tmp.cleanup()


class TestLoadSessionFullSchema(Env):
    """Stone 12 regression: the real state.db has ended_at AND last_activity_at
    AND cwd; _load_session's column walk must consume last_activity_at even
    when as_of was already set from ended_at — otherwise cwd is read from the
    wrong column (the last_activity_at timestamp) and every 3V0 session is
    mis-scoped as a sibling project, silently skipping it."""

    def _seed_full_schema(self, cwd):
        conn = sqlite3.connect(str(self.db_path))
        conn.executescript(
            """
            CREATE TABLE sessions (
                id TEXT PRIMARY KEY, source TEXT NOT NULL, title TEXT,
                ended_at REAL, last_activity_at REAL, cwd TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL, role TEXT NOT NULL,
                content TEXT, tool_name TEXT, active INTEGER NOT NULL DEFAULT 1
            );
            """
        )
        conn.execute(
            "INSERT INTO sessions (id, source, title, ended_at, last_activity_at, cwd) "
            "VALUES ('s_full', 'tui', 't', 100.0, 200.0, ?)",
            (cwd,),
        )
        for i in range(4):
            conn.execute(
                "INSERT INTO messages (session_id, role, content) VALUES ('s_full','user',?)",
                (f"m{i}",),
            )
        conn.commit()
        conn.close()

    def test_full_schema_session_reviewed_not_skipped(self):
        self._seed_full_schema(str(REPO_ROOT))
        self.decisions_file.write_text(
            json.dumps({"summary": "no-op", "decisions": []}), encoding="utf-8"
        )
        _run_driver("s_full", self.env)
        entries = self.log_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["session_id"], "s_full")

    def test_load_session_reads_cwd_not_last_activity(self):
        self._seed_full_schema(str(REPO_ROOT))
        os.environ["THREEV0_REVIEW_STATE_DB"] = str(self.db_path)
        try:
            mod = _load_driver()
            sess = mod._load_session("s_full")
        finally:
            os.environ.pop("THREEV0_REVIEW_STATE_DB", None)
        self.assertIsNotNone(sess)
        self.assertEqual(sess["cwd"], str(REPO_ROOT))
        self.assertEqual(sess["as_of"], 100.0)  # ended_at, not last_activity_at

    def test_live_session_skipped_by_hook_path(self):
        # ended_at NULL -> a still-live session; the per-turn hook must not
        # review it (a mid-transcript review would be incomplete and its dedupe
        # entry would shadow the daemon's final review). Only the own-clock
        # drain reviews ended sessions.
        conn = sqlite3.connect(str(self.db_path))
        conn.executescript(
            """
            CREATE TABLE sessions (
                id TEXT PRIMARY KEY, source TEXT NOT NULL, title TEXT,
                ended_at REAL, last_activity_at REAL, cwd TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL, role TEXT NOT NULL,
                content TEXT, tool_name TEXT, active INTEGER NOT NULL DEFAULT 1
            );
            """
        )
        conn.execute(
            "INSERT INTO sessions (id, source, title, ended_at, last_activity_at, cwd) "
            "VALUES ('s_live', 'tui', 't', NULL, 200.0, ?)",
            (str(REPO_ROOT),),
        )
        for i in range(4):
            conn.execute(
                "INSERT INTO messages (session_id, role, content) VALUES ('s_live','user',?)",
                (f"m{i}",),
            )
        conn.commit()
        conn.close()
        self.decisions_file.write_text(
            json.dumps({"summary": "no-op", "decisions": []}), encoding="utf-8"
        )
        _run_driver("s_live", self.env)
        self.assertEqual(self.log_entries(), [])  # live -> skipped:live


if __name__ == "__main__":
    unittest.main()
