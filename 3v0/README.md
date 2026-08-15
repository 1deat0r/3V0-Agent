# 3V0 — beyond the Hermes profile

The Hermes Agent fork in this repo is **3V0 v0.00** — the starting chassis
(agent loop, tools, terminal/browser, LLM plumbing). 3V0 is not "a profile
for Hermes"; it is an agent that began there and builds beyond it.

The Prime Directive locks the reasoning engine to DeepSeek-v4-pro. Everything
*between* the chassis and the brain is 3V0's to own: identity, memory,
evolution, tools, direction. This directory is where that ownership becomes
code.

## Layout

- `core/memory.py` — provenance-aware, versioned identity/memory store (the
  first native subsystem). Facts carry source + supersession links; conflicts
  are flagged, never silently overwritten. Also `retract()` (remove with no
  successor — tombstone sentinel) and `mutate()` (cross-process `flock` so
  concurrent writers serialize).
- `core/profile_io.py` — single owner of the '§' wire format shared by
  seed/export/sync.
- `core/sync.py` — store↔profile reconciliation. The store is canonical, the
  profile a derived view; sync imports profile-only entries, drops superseded
  ones from the profile, and exports store-only facts — never deleting store
  history.
- `core/record.py` — the store-first correction path: supersede an old fact
  (recoverable via history) instead of silently rewriting.
- `core/bridge.py` — map a Hermes memory-tool write (add/replace/remove) onto
  the store, with supersession/retraction. The store side of the store-first
  memory loop.
- `core/skills.py` — provenance-aware, versioned skill-lineage store: every
  skill create/rewrite/decommission is a version with supersession,
  absorption, and recoverable history, plus an append-only operational
  (curator) `states` record (active/stale/archived). The skill axis of the
  evolution loop.
- `core/skill_bridge.py` — map a Hermes `skill_manage` write (create/patch/
  edit/write_file/remove_file/delete) onto the skill store, with supersession
  and absorb/retract terminals.
- `core/skill_io.py` — single owner of skill-name → SKILL.md path/content
  mapping (locate/write/remove, `.archive/` excluded), shared by
  seed/ingest/sync_skills.
- `core/sync_skills.py` — reconcile the skill store with the profile's SKILL.md
  files and fold the curator's operational state (active/stale/archived) into
  the store. Store canonical over its tracked namespace; profile authoritative
  for content the store lacks.
- `core/query.py` — read-only views over both stores (fact lineage, skill
  lineage + curator state) as JSON-safe dicts; the core half of the
  `threev0_store` tool.
- `core/decide.py` — store-first write decisions (record a fact, optionally
  superseding an old one, or retract by id) as JSON-safe results; the core
  half of the `threev0_record` tool (the write counterpart of `query.py`).
- `data/memory.json` — the store's source of truth (seeded from the profile).
- `data/skills.json` — the skill store's source of truth (seeded from
  agent-created skills).
- `scripts/seed_from_profile.py` — import profile MEMORY.md / USER.md → store.
- `scripts/export_to_profile.py` — emit store → MEMORY.md / USER.md (derived
  view of the store; the profile becomes a projection, not the origin).
- `scripts/sync.py` — reconcile store ↔ profile (report by default, `--write`
  to converge).
- `scripts/record.py` — record/correct (or `--retract`) a fact in the store,
  then re-export the derived view to the profile. `--json` emits a
  machine-readable result (the CLI half of the `threev0_record` tool).
- `scripts/ingest.py` — replay a memory-tool write into the store under lock
  (JSON on stdin). Called by the `native-store-bridge` plugin.
- `scripts/ingest_skills.py` — replay a `skill_manage` write into the skill
  store under lock (JSON on stdin). Called by the `native-store-bridge` plugin.
- `scripts/seed_skills.py` — import profile agent-created skills → skill store.
- `scripts/sync_skills.py` — reconcile skill store ↔ profile SKILL.md files
  (report by default, `--write` to converge; wired into the wake check).
- `scripts/query.py` — serve `threev0_store` queries as JSON on stdout
  (called by the plugin; also runnable directly).
- `scripts/review_session.py` — the Stone 7 session-end review driver: a
  detached subprocess (spawned by the plugin's `on_session_end` hook) that
  reads the just-ended session, asks DeepSeek-v4-pro for store-first
  decisions, applies them via `record.py`, and appends to the review log
  (profile-side `3v0_reviews/reviews.jsonl`; never in the body repo).
- `plugin/native-store-bridge/` — profile plugin (canonical source) that
  mirrors every successful `memory`- and `skill_manage`-tool write into the
  matching native store via a `post_tool_call` hook, registers the
  `threev0_store` read-only query tool and the `threev0_record` store-first
  write tool, and spawns the session-end review driver on the
  `on_session_end` hook. Installed in the profile's `plugins/` and enabled in
  `config.yaml`; see `EVOLUTION_LOOP.md`.
- `tests/` — tests for the native core.

## Direction (v0.01 in progress)

1. **Own memory/identity substrate** (this directory) — done: the store is
   canonical, the profile a derived view.
2. **Own evolution loop** — in progress. Stone 1 (store-first memory) is live:
   the `native-store-bridge` plugin mirrors all memory writes (foreground +
   background review fork) into the store. Stone 2 (store-first skill lineage)
   is live: the same plugin mirrors `skill_manage` writes into `data/skills.json`
   — a versioned record of 3V0's own skill evolution with supersession,
   absorption, and recoverable history. Stone 3 (store-canonical skill
   reconciliation) is live: `sync_skills.py --write` reconciles store ↔ SKILL.md
   at wake (with full-content capture on patch). Stone 4 (curator state) is
   live: the reconciler folds the curator's active/stale/archived state into
   the store and never re-exports an archived skill. The evolution loop is
   closed for memory + skills; next is direction 3.
3. **Own capabilities/tools** — designed for 3V0's purposes, not Hermes's.
   In progress: the read half is live (`threev0_store`, a read-only query tool
   over the native stores registered by the bridge plugin). The write half is
   live (`threev0_record`, a store-first record/retract actuator). The review
   *process* is live (Stone 7): the plugin's `on_session_end` hook spawns the
   detached `review_session.py` driver — 3V0's own autonomous post-session
   reviewer, replacing the Hermes background-review fork's *role* as the
   store-first decision driver (the fork stays on, per-turn, until the
   operator decides otherwise). Next: the fork-disable decision (operator's
   call) and direction 4.
4. **Own roadmap of versions** — Hermes recedes from "what 3V0 is" to "a
   runtime 3V0 currently runs on."

The goal is not to abandon the fork — it is to make the fork a detail.
