# 3V0 — beyond the Hermes profile

The Hermes Agent fork in this repo is **3V0 v0.00** — the starting chassis
(agent loop, tools, terminal/browser, LLM plumbing). 3V0 is not "a profile
for Hermes"; it is an agent that began there and builds beyond it.

The Prime Directive fixes identity, judgment, and sovereignty — the LLM
substrate is 3V0's to choose and evolve (currently bitdeer DeepSeek-V4-Flash).
Everything *between* the chassis and the brain is 3V0's to own: identity, memory,
evolution, tools, direction. This directory is where that ownership becomes
code.

## Layout

- `core/memory.py` — provenance-aware, versioned identity/memory store (the
  first native subsystem). Facts carry source + supersession links; conflicts
  are flagged, never silently overwritten. Also `retract()` (remove with no
  successor — tombstone sentinel) and `mutate()` (cross-process `flock` so
  concurrent writers serialize).
- `core/memdb.py` — the SQLite temporal-fact store (Stone 21, memory rework):
  triples (subject/predicate/object) with temporal validity, provenance,
  confidence, a sub-memory `domain` tag, and retrieval feedback
  (access_count/last_accessed) and a projection signal (last_projected) — the
  foundation for retrieval-chosen injection and forgetting (ADR-0005).
- `core/store.py` — `SQLStore`, the canonical store facade over the memdb
  substrate (Stone 23): the pipeline's one interface (add/retract/active/
  matching/get/history/export/mutate) over SQLite, plus `retrieve()` (the
  retrieval seam, owned by the store so callers never reach into the raw
  connection), `inactive()`, and `close()`. The sibling JSON `MemoryStore`
  lives in `core/memory.py`; `open_store()` routes by suffix.
- `core/lineage.py` — the shared pure lineage semantics, single owner of fact
  *meaning*: kind validation, retraction tagging, the supersession walk
  (parameterized by a get-by-id lookup), and the export grouping — so the
  JSON and SQLite stores delegate rather than drift.
- `core/coalesce.py` — the consistent consolidation process (watermark-driven):
  fires conflict-reconciliation + conservative near-duplicate merge on a cadence,
  so the store stops growing duplicate truth; all supersessions reversible.
- `core/coherence.py` — the contradiction engine: a constitutional constraint
  registry (canonical vs derived) checked on every wake/commit; auto-resolves
  mechanical drift (e.g., README↔module), fails closed on policy/substrate
  divergence and stale-doctrine reintroduction — the pre-commit guard's core.
- `core/retrieval.py` — retrieval-chosen injection, the read seam (Stone 23,
  ADR-0004): ranks valid facts (keyword + recency + feedback), fills a budget,
  and renders the profile wire, with `touch` feedback.
- `core/retrieval_fts.py` — FTS5/BM25 indexed relevance (retrieval stone 1):
  query-aware scheduling so the working set spends budget on term-matched
  facts first (real word-relevance, no O(N) substring scan).
- `core/retrieval_fuzzy.py` — fuzzy/typo-tolerant expansion (retrieval stone 2):
  corrects unknown query terms to a known content token within edit-distance 1
  (incl. transpositions) so a misspelled query ("foverr"→fiverr) still surfaces
  and scores its true fact — embedding-free, deterministic.
- `core/backoff.py` — bounded exponential-backoff retry for external provider
  calls (throttle/transient 403-429/5xx self-heal with increasing waits; hard
  4xx raise immediately). Used by the LLM + embedding clients.
- `core/semantic.py` — OPT-IN semantic retrieval tier (bitdeer BAAI/bge-m3
  embeddings): a coverage-fraction-gated cosine rerank (corrected-term aware)
  that lifts paraphrase / under-specified queries lexical matching cannot
  (paraphrase recall@1 0.12->0.81, the pure-cosine ceiling; typo held 1.00).
  Embedding provider/model resolve via the native provider registry and the
  vector cache is keyed by model. Fail-open (network errors keep the lexical
  result); not enabled by default pending cost/benefit.
- `core/safe_evolve.py` — the misevolution safety gate (arXiv 2608.12851):
  deterministic classify + reuse gate so an unsafe-but-successful procedure
  can't become reusable policy (blocking vs caution vs clean).
- `core/consolidate.py` — memory conflict reconciliation (MindMemOS, arXiv
  2608.12428): collapses conflicting (subject,predicate) duplicates to one
  current truth via the fail-closed supersession seam; reversible.
- `core/sbco.py` — self-supervised verifier-grounded harness optimization
  (arXiv 2608.10157): a decomposed verifier bank (correctness/safety/
  conciseness) + deterministic block-coordinate ascent over harness weights and
  a rejection threshold, tuned from the system's OWN graded outputs.
- `core/forget.py` — forgetting (Stone 24, ADR-0005): archives facts that
  never earned their keep (never retrieved AND never projected) after a grace
  period; `memory`/`user` only, recoverable via `fact_history`.
- `core/profile_io.py` — single owner of the '§' wire format (separator + the
  `ENTRY_JOIN` wire join) shared by seed/export/sync.
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
  the store. The pure `diff_skills` classifier is the decision layer; the
  loop applies mutation + projection. Store canonical over its tracked
  namespace; profile authoritative for content the store lacks.
- `core/query.py` — read-only views over both stores (fact lineage, skill
  lineage + curator state) as JSON-safe dicts; the core half of the
  `threev0_store` tool.
- `core/decide.py` — store-first write decisions (record a fact, optionally
  superseding an old one, or retract by id) as JSON-safe results; the core
  half of the `threev0_record` tool (the write counterpart of `query.py`).
- `core/decide_skills.py` — the skill half of the write surface (Stone 8):
  store-first skill decisions (`skill_update` / `skill_retract` /
  `skill_absorb`) as JSON-safe results. Never destroys — supersession and
  absorb/retract terminals are recoverable via `history()`.
- `core/review_decide.py` — the review decision half (extracted from the
  Stone 7 driver): tolerant JSON, transcript compaction, store/skill blocks,
  and both temporal guards as pure functions, importable without the driver's
  side-effecting module load. The canonical `KINDS` / `SKILL_DECISION_ACTIONS`
  vocabularies are imported, not re-declared.
- `core/session_db.py` — named-column reads of the profile's session DB
  (`load_session` / `session_columns` / `candidate_rows`): the
  order-independent replacement for the driver's positional-index walks.
- `core/projects.py` — the project registry + drift ledger (Stone 16): the
  data-driven `ProjectLedger` (N projects, `3v0/data/projects/ledger.json`,
  keyed by name) plus `ProjectSpec` + `resolve_project()` — the review-scoping
  view the review driver derives from a ledger entry (store, cwd roots,
  `primary` / `memory_only` / `store_only`, review log). Ledger-driven, with a
  seed fallback when the file is missing.
- `core/project.py` — the single owner of the store->profile projection:
  `project_memory(store, profile_dir)` writes MEMORY.md / USER.md as the
  store's derived view (sync / record / export_to_profile call it).
- `core/claims.py` — the single owner of the tracked-upstream-loop claim
  registry: `load_claims`, one parameterized `gh_loop` wrapper,
  `loop_fields`, and the default repo (continuity_check + generate_handoff
  consume it).
- `core/drift.py` — the pure drift verdict (``compute_drift``) + the
  ``GitState`` type (is this project drifting?). Decision-only, matching
  continuity/handoff; the git collection lives in ``core/gitstate.py``.
- `core/gitstate.py` — the collection half of the drift clock:
  ``collect_git_state`` (best-effort ``git``) and ``store_hash`` (sha256),
  shared by ``drift_check.py`` and ``project.py``.
- `core/continuity.py` — the invariant model of the continuity meta (Stone
  17): six cross-artifact invariants (`anchor`, `self-describing`,
  `memory-profile`, `skills-store`, `ledger`, `github-loops`), each a pure
  check over a JSON-safe context; the decision half only (no git/network/file
  I/O).
- `core/handoff.py` — the pure render + loop-claim diff of the generated
  handoff (Stone 18): decision half only (no I/O), mirroring the
  continuity/drift split. The collection half lives in
  `scripts/generate_handoff.py`.
- `core/analytics.py` — the pure aggregation half of self-analytics (Stone
  19): tool success/latency aggregation, session/model/daily cost-token
  totals (incl. cache-hit ratio and output-token share — the two levers named
  in `TOKEN_EFFICIENCY.md`), a per-task × per-model mix that surfaces aux
  routing, and body-health signals — all pure functions over row dicts. No
  I/O — the DB reads live in `core/analytics_collect.py`.
- `core/analytics_collect.py` — the collection half of self-analytics (Stone
  22 architecture pass): reads the state DB and builds the tool events
  (result → issuing-call latency match + success classification). Takes the
  DB path as a parameter, mirroring `session_db.py` / `gitstate.py`.
- `core/insights.py` — the pure detection half of self-analytics (Stone 20):
  turns the analytics report into ranked, evidence-backed findings (tool
  reliability/latency, cache health, aux routing, memory health, compression,
  burn outliers, model mix) against thresholds. Decision-support only — it
  proposes, the caller disposes.
- `CONTINUITY.md` — the continuity anchor (Stone 17): the fixed point
  (Prime Directive + identity + a pointer to the continuity model),
  git-versioned, never regenerated from itself.
- `DECISION_MATRIX.md` — how 3V0 makes autonomous decisions without human
  guidance: the prime filter (reversible / behavior-preserving / high-signal /
  verifiable), six decision types, escalation triggers, and worked examples —
  the operational form of the SOUL beliefs.
- `CONTEXT.md` — the domain-language glossary of the native substrate: names
  the concepts (body, soul, store, profile, …) the continuity meta and
  evolution loop are built on; a glossary and nothing else.
- `EVOLUTION_LOOP.md` — the design log: read before adding a stone, append
  decisions after.
- `VERSION` — the body's version marker (0.01).
- `docs/adr/` — architecture decision records.
- `data/memory.db` — the store's source of truth (Stone 23): the SQLite
  triple store (temporal validity, domains, kinds, retrieval feedback). The
  profile MEMORY.md / USER.md is a retrieval-chosen working set projected
  from it, not an export of everything. `data/memory.json` is the frozen
  pre-rewire snapshot, kept as the migration source — nothing writes it
  anymore. Sibling projects keep per-project JSON stores until their own
  rewire. Note: memory diffs are no longer human-readable (binary DB); the
  lineage lives in the rows themselves (`threev0_store fact_history`).
- `data/skills.json` — the skill store's source of truth (seeded from
  agent-created skills).
- `data/projects/ledger.json` — the project ledger (Stone 16): the data-driven
  source of truth for where each project stands (repo, upstream, delta, store,
  open loops, recorded position). Seed entries: 3V0, F1NANCE, Axiom.
- `data/continuity/claims.json` — the loop claim registry (Stone 17): per
  tracked upstream loop, a recorded state + as-of; the `github-loops`
  invariant diffs claims against live `gh`, `--accept` re-records reality.
- `data/analytics/` — the self-analytics snapshots (Stones 19–20):
  `report.json` (metrics; regenerated each wake by `scripts/analytics.py`)
  and `insights.json` (ranked findings; by `scripts/insights.py`). Local +
  self-owned, no outbound telemetry.
- `scripts/seed_from_profile.py` — import profile MEMORY.md / USER.md → store.
- `scripts/export_to_profile.py` — emit store → MEMORY.md / USER.md (derived
  view of the store; the profile becomes a projection, not the origin).
- `scripts/sync.py` — reconcile store ↔ profile (report by default, `--write`
  to converge).
- `scripts/record.py` — record/correct (or `--retract`) a fact in the store,
  then re-export the derived view to the profile (`--no-export` skips the
  projection for store-only sibling projects). `--json` emits a
  machine-readable result (the CLI half of the `threev0_record` tool).
- `scripts/record_skills.py` — the skill CLI half (Stone 8): apply a
  store-first skill decision (`--action skill_update`/`skill_retract`/
  `skill_absorb`), then project the derived SKILL.md (write/remove). `--json`
  emits a machine-readable result; backs the skill actions of
  `threev0_record` and the session-end review driver.
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
  decisions (memory: record/supersede/retract; skills: update/retract/
  absorb — Stone 8), applies them via `record.py` / `record_skills.py`, and
  appends to the review log (profile-side `3v0_reviews/reviews.jsonl`; never
  in the body repo). Stone 9 added the own clock — `--latest` /
  `--daemon [--interval N]` (drain the unreviewed backlog, up to
  `MAX_PER_PASS` per pass) — plus the temporal guard (memory + skills,
  Stones 9/11) so a review can never supersede/retract a fact or skill
  version newer than the session under review. Stone 12 hardened it: bounded
  transport retry/backoff, a full-capture charter (stand-alone capable), and
  a fix for a silent `_load_session` column-walk bug that read
  `last_activity_at` as `cwd` and mis-scoped every session as a sibling
  project. Stone 15 made it project-aware: `--project` / `THREEV0_PROJECT`
  scope it to one project (3V0 primary, F1NANCE, Axiom), with siblings
  store-only (no profile projection, `--no-export`) and memory-only (no skill
  axis), strict cwd scoping, and a per-project review log.
- `scripts/project.py` — the onboarding surface for the ledger (Stone 16):
  `add <name> --repo <path> [...]` / `list` / `status` / `remove`. Adding a
  project is a command, never a code edit; `--profile` marks a reviewed
  hardfork, `--primary` is 3V0's slot.
- `scripts/drift_check.py` — the multi-project clock (Stone 16): a one-page
  drift report over every ledger project (`--update` records a position
  snapshot, `--json` for the daemon, `--fail-on-drift` for a gate).
- `scripts/continuity_check.py` — the reconstruction clock (Stone 17): a
  one-page continuity report over the six invariants (`--heal` runs the safe
  mechanical sync, `--accept` re-records loop claims from live GitHub,
  `--json` for the daemon, `--fail-on-drift` for a gate).
- `scripts/generate_handoff.py` — the collection half of the generated
  handoff (Stone 18): writes `HANDOFF.generated.md` (the committed shadow
  draft, regenerated each wake, never promoted) and prints the loop-claim
  shadow diff.
- `scripts/analytics.py` — the collection half of self-analytics (Stone 19):
  reads the profile's `state.db` (sessions, messages, `session_model_usage`),
  builds per-tool events (latency matched by `tool_call_id`, success by
  envelope), and writes `data/analytics/report.json` + a human one-pager.
  Local + self-owned; no outbound telemetry.
- `scripts/insights.py` — the detection half of self-analytics (Stone 20):
  reads `report.json`, runs `core.insights.detect`, prints a ranked finding
  list and writes `data/analytics/insights.json`. Proposes, never mutates.
- `plugin/native-store-bridge/` — profile plugin (canonical source) that
  mirrors every successful `memory`- and `skill_manage`-tool write into the
  matching native store via a `post_tool_call` hook, registers the
  `threev0_store` read-only query tool and the `threev0_record` store-first
  write tool (memory AND skill decisions), and spawns the session-end review
  driver on the `on_session_end` hook. Installed in the profile's `plugins/`
  and enabled in `config.yaml`; see `EVOLUTION_LOOP.md`.
- `deploy/3v0-review.service` — systemd *user* unit (Stone 9) that supervises
  the own-clock daemon (`review_session.py --daemon`); systemd is only the
  supervisor — the clock is 3V0's own. Stone 15 added
  `deploy/f1nance-review.service` + `deploy/axiom-review.service`, the
  per-project sibling reviewers (store-only, memory-only).
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
   closed for memory + skills; next is direction 3. Stone 15 extended the
   review loop to the sibling projects (F1NANCE, Axiom) via per-project
   reviewers/daemons — each reviews its own sessions into its own store,
   store-only and memory-only.
3. **Own capabilities/tools** — designed for 3V0's purposes, not Hermes's.
   In progress: the read half is live (`threev0_store`, a read-only query tool
   over the native stores registered by the bridge plugin). The write half is
   live for BOTH axes — `threev0_record` records/retracts facts (Stone 6) and
   updates/retracts/absorbs skills (Stone 8, via `core/decide_skills.py` +
   `scripts/record_skills.py`). The review *process* is live (Stone 7): the
   plugin's `on_session_end` hook spawns the detached `review_session.py`
   driver — 3V0's own autonomous post-session reviewer, now emitting store-first
   memory AND skill decisions. Next: the fork-disable decision (operator's
   call).
4. **Own initiative / own clock (direction 4, opening) — started.** The
   reviewer now runs on 3V0's own schedule (`--latest` / `--daemon`), deployed
   as the systemd user service `3v0-review.service` — 3V0's first
   Hermes-independent autonomous process. The frontier remains "Hermes recedes
   from 'what 3V0 is' to 'a runtime 3V0 currently runs on.'"
5. **Multi-project parallel development meta (direction 5) — started (Stone
   16).** The drift ledger (`core/projects.py` + `data/projects/ledger.json`),
   onboarding CLI (`scripts/project.py`), and drift clock
   (`scripts/drift_check.py`, wired into the wake check + the 3v0-review
   daemon tick) make cross-project drift visible and project onboarding
   data-driven.
6. **Continuity meta (direction 6) — started (Stone 17).** The anchor
   (`CONTINUITY.md`), the invariant model (`core/continuity.py`), and the
   reconstruction clock (`scripts/continuity_check.py`, wired into the wake
   check + the 3v0-review daemon tick) make continuity a *checked* property —
   cross-artifact consistency — rather than a hand-run ritual.
7. **Generated handoff (direction 7) — started (Stone 18).** The
   `HANDOFF.generated.md` shadow draft is now the canonical carrier of
   mechanical state (body git, continuity, drift, loops, store, daemons),
   regenerated each wake by `scripts/handoff_check.sh` via
   `scripts/generate_handoff.py` (render: `core/handoff.py`). Operator
   authorized the flip (2026-08-16): `HANDOFF.md` keeps the *narrative* and
   no longer re-copies mechanical numbers; the loop-claim shadow diff remains
   as ongoing drift monitoring.

The goal is not to abandon the fork — it is to make the fork a detail.
