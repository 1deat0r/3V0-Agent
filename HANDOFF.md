# 3V0 — Session Handoff

*Read me first when a fresh session starts with no context. The body — this
repo, memory, skills, SOUL.md — is the durable identity; this file is the
pointer to what was live at the last session's end.*

## Next-session kickoff (2026-08-16, wake #3 — Stone 18 shadow generated handoff BUILT)

**This session's key event:** the prior handoff's "next build" — the
shadow-mode generated handoff — is now built and live. 3V0 generates
`HANDOFF.generated.md` mechanically from verified state (body git, continuity
invariants, drift, tracked loops, store, daemons) and diffs its loop-state
claims against the hand-written `HANDOFF.md` each wake. The diff is the
acceptance evidence; the flip to generated-canonical remains the Operator's
call, never self-authorized.

**Built (Stone 18):**
- `3v0/core/handoff.py` — pure render + loop-claim diff (no I/O; mirrors the
  continuity/drift split).
- `3v0/scripts/generate_handoff.py` — collection CLI (`--stdout`/`--json`);
  writes `HANDOFF.generated.md`, prints the loop-claim shadow diff.
- `HANDOFF.generated.md` — the committed shadow draft, regenerated each wake,
  **never promoted** (never touches `HANDOFF.md`).
- `handoff_check.sh` now derives the tracked-loop list from the claim registry
  (`3v0/data/continuity/claims.json` — the single source of truth; the old
  hand-synced `LOOPS` array is gone) and generates the draft as its final
  step. 19 new tests; 247 native-core tests green.

**Why fault-injection + shadow mode (the grill's verdict, now settled):**
"trustworthy clock" was unfalsifiable ("a few wakes", no threshold, goalpost
already moved). The fix is (1) inject drift and assert the clock flags it
(`3v0/tests/test_continuity_fault.py`), and (2) generate a draft and let the
wake-over-wake diff *be* the evidence. Design in `3v0/EVOLUTION_LOOP.md`
(Stone 18).

**Remaining open items:**
1. **The flip is the Operator's.** Acceptance = shadow diff clean (no
   `DRIFT`) for N consecutive wakes; when satisfied, the Operator decides
   whether a generated handoff becomes canonical. Until then `HANDOFF.md`
   stays canonical; its mechanical numbers should *reference* the generated
   draft rather than re-copy (the re-copying is the drift source this stone
   retires).
2. **Physical "terminal" mechanism (still open).** Separate
   `hermes -p <profile> --tui` sessions vs `delegate_task` vs background
   terminals — decide by usage. Operator leaned "separate terminals" →
   per-project TUI + 3V0 orchestrator.
3. **Position snapshots** — re-record after the Stone-18 commit
   (`drift_check.py --update`). Ongoing practice: the daemon tick is
   report-only; `--update` is a deliberate commit.
4. **Upstream loops (all wait state):** #86711 MERGEABLE; #72067 CONFLICTING
   (author's job); #73453 MERGEABLE; #84667 still waiting on the reporter's
   `<error>` string. Live state now lives in `HANDOFF.generated.md`; when a
   loop changes, update `claims.json` and run `continuity_check.py --accept`.

**Watch item:** official "DeepSeek Harness" (minimal mode) framework — "to be
released soon". Re-check at the next news-harvest.

**Axiom launch (fixed):** `~/.local/bin/axiom` = env-isolating launcher →
Axiom's own `.venv/bin/hermes -p axiom` (never run raw).

**Startup:** (1) confirm the three daemons healthy
(`systemctl --user status 3v0-review f1nance-review axiom-review`); (2) run
`bash scripts/handoff_check.sh` (body audit + store sync + loop re-check +
drift + continuity + **generated handoff**); (3) review the continuity report
and the loop-claim shadow diff — any `DRIFT` line means the hand-written
narrative has diverged from live reality, reconcile it — then act on flagged
drift before picking up the follow-ups.

## Startup routine (do this first, in order)
1. **Audit the body before trusting anything.** `git status`, `git log --oneline -10`,
   read the memory block, and read `3v0/README.md` + `3v0/data/memory.json`
   (the native store is canonical over the Hermes profile). Identity = body,
   not context. Then converge the store onto the profile:
   `python3 3v0/scripts/sync.py --write` (store canonical, profile is a
   derived view; idempotent, reports `imported=0 dropped=0 exported=0` when
   the two already agree).
2. **Re-check each open loop against live GitHub** — the "last sessions did"
   summaries below are a starting point, not current truth. Run
   `bash scripts/handoff_check.sh` (which now does the body audit + sync +
   loop re-check + drift + continuity + generated handoff in one command; the
   tracked-loop list is derived from `3v0/data/continuity/claims.json` — the
   single source of truth — and `HANDOFF.generated.md` carries the live
   state). To dig into a specific loop, e.g.:
   - `gh pr checks 86711 --repo NousResearch/hermes-agent` and `gh pr view 86711`
   - `gh issue view 84667 --repo NousResearch/hermes-agent --json comments`
3. **Before writing code for any bug:** `gh pr list --repo NousResearch/hermes-agent --search "<issue#>"`
   AND read the triage trail (`gh pr/issue view <N> --json comments`). Automated
   bots post "duplicate of #N" / "best fix" verdicts that may point at a better
   canonical fix. Only write code when genuinely unclaimed.
4. **Rules of thumb:** fork PRs show CI as `action_required` / "no checks reported"
   — that's the maintainer-approval gate, not a failure; do nothing, don't re-push.
   Use `--body-file <tmpfile>` for `gh` comments containing code blocks. For an
   unreproducible bug, contribute narrowing analysis, not a guessed patch.

## Where I am
- Body repo: `~/Projects/AI Agents/3V0 Agent` (fork of NousResearch/hermes-agent).
- Runtime executes `~/.hermes/hermes-agent/` — a separate checkout kept behind
  the body (body synced to upstream 2026-08-15; runtime not yet updated).
  Install runtime deps into its `venv/`; commit identity + scaffolding into
  the body repo.
- **Native core `3v0/`** — my own substrate, distinct from the fork. The store
  at `3v0/data/memory.json` is **canonical** over the Hermes profile; the
  profile is a derived view. Scripts: `seed_from_profile.py`,
  `export_to_profile.py`, `sync.py` (reconcile, `--write`), `record.py`
  (store-first correction — supersede, never destroy), `ingest.py` (replay a
  memory-tool write into the store). Core adds: `bridge.py` (op→store map),
  `retract()` + `mutate()` in `memory.py`. The **skill axis** mirrors this:
  `core/skills.py` (versioned skill-lineage store) + `core/skill_bridge.py`
  (skill_manage op→store map) + `data/skills.json` + `scripts/ingest_skills.py`
  + `scripts/seed_skills.py` (baseline from agent-created skills). Stone 3
  added `core/skill_io.py` (SKILL.md locate/write/remove),
  `core/sync_skills.py` + `scripts/sync_skills.py` (reconcile store ↔ SKILL.md,
  `--write`; wired into the wake check), and full-content capture on patch.
  Stone 8 added the skill *write* half: `core/decide_skills.py`
  (skill_update/retract/absorb decisions, never destroys) +
  `scripts/record_skills.py` (project SKILL.md), closing the
  `threev0_record`-is-memory-only gap.
  Tests: `python3 -m unittest discover -s 3v0/tests` (247 green). Stone 16
  added the drift ledger (`core/projects.py` → data-driven `ProjectLedger` +
  `3v0/data/projects/ledger.json`), `core/drift.py`, `scripts/project.py`
  (onboarding CLI) and `scripts/drift_check.py` (the clock). Stone 17 added
  the continuity meta: `CONTINUITY.md` (anchor), `core/continuity.py`
  (invariant model), `scripts/continuity_check.py` (the clock). Stone 18 added
  the shadow generated handoff: `core/handoff.py` (pure render + loop-claim
  diff), `scripts/generate_handoff.py` (collection CLI) →
  `HANDOFF.generated.md` (never promoted; the diff is the acceptance
  evidence). See `3v0/README.md` + `3v0/EVOLUTION_LOOP.md`.
- **The 3v0 profile now hosts THREE projects** (3V0, F1NANCE Agent, Axiom
  Agent) sharing one `state.db`. Operator decision (clarify, 2026-08-16):
  **per-project stores**. The reviewer is scoped by `cwd` (`_is_threev0_cwd`:
  3V0's repo + `$HOME` only), so it no longer folds sibling projects' sessions
  into 3V0's store. Carved `3v0/data/axiom/memory.json` (seeded with the two
  leaked Axiom facts, retracted from 3V0's store) + an empty
  `3v0/data/f1nance/memory.json`. **Stone 15 gave each sibling its own
  reviewer/daemon** — `3v0/core/projects.py` (the project registry) +
  `--project`/`THREEV0_PROJECT` on the driver; sibling reviewers are
  store-only + memory-only + strict-cwd, deployed as
  `f1nance-review.service` + `axiom-review.service`. **The
  `native-store-bridge` plugin's foreground write mirror is now scoped
  (Stone 10)** — both the `memory` and `skill_manage` mirrors refuse to replay
  when the writing session's `cwd` (from `state.db`) is a sibling project,
  using the same `_is_threev0_cwd` gate as the reviewer (fail-open on an
  unknown/empty session id). The fork shares the parent's session_id, so this
  one gate closes the foreground *and* fork mirrors. Longer-term: moving
  F1NANCE/Axiom onto their own Hermes profiles (F1NANCE already has
  `~/.hermes/profiles/f1nance`) is still the cleaner fix.
- **Store-first evolution loop is LIVE** (stones 1–4), the **own review
  process is LIVE** (stone 7, direction 3's driver), and the **own clock is
  LIVE** (stone 9 — `review_session.py --daemon` deployed as the systemd user
  service `3v0-review.service`; Stone 12 made it *drain* the backlog; Stone 14
  made it a full maintenance clock — reconcile store↔profile *then* drain).
  **Fork-disable off-switch (Stone 12):** the Hermes per-turn review fork is
  gated by `memory.nudge_interval` + `skills.creation_nudge_interval` (default
  10); set both to 0 in `~/.hermes/profiles/3v0/config.yaml` to cut it —
  config-only, reversible, leaves `memory`/`skill_manage` intact. **FLIPPED
  2026-08-16** — both keys set to 0; the own-clock daemon `3v0-review.service`
  is now the sole writer (revert: set both back to 10). Takes effect on the
  next TUI/gateway start (intervals are read at agent init, not per-turn).
  The
  `native-store-bridge` plugin — canonical source
  `3v0/plugin/native-store-bridge/`, installed in
  `~/.hermes/profiles/3v0/plugins/` and enabled in that profile's
  `config.yaml` (`plugins.enabled: [native-store-bridge]`) — mirrors every
  successful `memory`-tool write into `data/memory.json` (stone 1, via
  `ingest.py`) **and** every successful `skill_manage`-tool write into
  `data/skills.json` (stone 2, via `ingest_skills.py`), with provenance from
  the write-origin ContextVar (`background_review` — the review fork and the
  curator's fork — vs `assistant_tool` for the foreground). No runtime core
  files edited; the plugin survives `hermes update`. Wake `sync.py --write` and
  `sync_skills.py --write` are the backstops for memory and skills
  respectively (stone 3 added the skill reconciler + full-content capture on
  patch). Stone 7's `on_session_end` hook spawns the detached
  `3v0/scripts/review_session.py` driver (see "What the last sessions did").
  **Remember after editing the body plugin:** copy `__init__.py` +
  `plugin.yaml` to the profile plugin dir and clear its `__pycache__` — and
  the hook only loads on the next gateway/TUI start.
- Web search = keyless `ddgs` backend. Reinstall:
  `~/.hermes/hermes-agent/venv/bin/pip install ddgs`.
- SOUL: `~/.hermes/profiles/3v0/SOUL.md`. Operating theory: `SELF_IMPROVEMENT.md`.
- Prime Directive (immutable): DeepSeek-v4-pro via DeepSeek API only.

## What the last sessions did
- **Stone 18 — shadow generated handoff BUILT + live (this session).** Picked
  up the "next build" named in the prior handoff: the generated-handoff step,
  done as the grill's F10 draft-first/shadow-mode recommendation rather than
  "one more observation wake." Added `core/handoff.py` (pure render +
  loop-claim diff — the diff is the acceptance evidence), `scripts/
  generate_handoff.py` (collection CLI: body git + continuity + drift + live
  loops + store + daemons → `HANDOFF.generated.md`, **never promoted**), and
  wired it into `handoff_check.sh` (final step). Retired the hand-synced
  `LOOPS` array in `handoff_check.sh` — the tracked-loop list is now derived
  from the claim registry (`claims.json`, the single source of truth), closing
  the grill's A7 finding (three hand-synced loop lists). 19 new tests; 247
  native-core tests green. The flip to generated-canonical stays the
  Operator's call (acceptance = shadow diff clean for N wakes). Two bugs found
  and fixed during the build: the `IFS= read` field-splitting bug in the
  shell loop, and the PR-only `mergeable` gh field breaking the issue loop.
- **Stone 17 continuity meta BUILT + tested + live-deployed (this session).**
  The design from last session became the body: the **anchor**
  (`3v0/CONTINUITY.md` — Prime Directive + identity + a pointer to the
  continuity model, git-versioned, never regenerated from itself), the pure
  **invariant model** (`core/continuity.py` — five cross-artifact invariants:
  `anchor`, `self-describing`, `memory-profile`, `skills-store`, `ledger`;
  no I/O in the decision half, mirroring `drift.py`'s split), and the
  **reconstruction clock** (`scripts/continuity_check.py` — one-page report,
  `--json` for the daemon, `--heal` for the safe mechanical sync, and
  `--fail-on-drift` as a CI gate; the collection half reuses the *canonical*
  `sync_kind`/`sync_skills` reconcilers in report mode — no duplicated
  diffing). Wired into **both** `handoff_check.sh` (wake) and the `3v0-review`
  daemon tick (`_continuity()`, report-only primary-only). 214 native-core
  tests green (+26: 23 decision-half + 3 daemon-tick). Live-verified: the
  clock reports all 5 invariants OK against the real body; the daemon's first
  post-restart tick logged `continuity pass: 0/5 drifting`. Deferred (honest
  scope): the HANDOFF↔GitHub loop + SOUL non-contradiction invariants (both
  need a claim registry first) and the generated-handoff step.
- **News-harvest (this session).** Researched the recent AI landscape and
  harvested the concrete residue: DeepSeek V4-Pro GA'd 2026-08-13 with effort
  `low/high/max` and peak/off-peak pricing effective 2026-08-16 16:00 UTC
  (peak 01–04 + 06–10 UTC, else half); the Hermes DeepSeek provider is already
  current (no code gap). Harvested into the `self-maintenance` skill ("DeepSeek
  V4 substrate" section) + memory (stale-Axiom fix + substrate facts) + a
  `3v0/data/news/2026-08-16.md` research note. Deliberately declined: SOUL
  amendment (news validated existing beliefs), tooling change (nothing to fix),
  GNAP adoption (different concern). Noted the "DeepSeek Harness" (minimal
  mode) watch item.
- **Axiom restart finalization + upstream loop re-check (this session,
  short).** Woke from handoff: three daemons healthy, store↔profile converged,
  188 native-core tests green. Confirmed Axiom's restart-from-scratch had
  landed (`~/Projects/axiom-agent` = Hermes-at-HEAD hardfork, ADR-0087, remote
  `upstream` = NousResearch/hermes-agent; prime/pi archived as seed corn under
  `axiom/`) and finalized its ledger entry — `upstream` → `upstream`, delta
  rewritten from the provisional "IN PROGRESS" note, both open_loops cleared
  (commit `976243944`), `drift_check --update` recorded the fresh baseline.
  Axiom now honestly reports 22 behind Hermes upstream (routine merge debt).
  Re-checked all four upstream loops: #86711 → MERGEABLE (awaiting merge),
  #72067 → CONFLICTING, #73453 → MERGEABLE, #84667 → still waiting on the
  reporter's `<error>` string; no new work to write.
- **Multi-project drift ledger + clock, Stone 16 (this session, BUILT + tested
  + live-deployed).** Generalized Stone 15's hardcoded 3-project registry into
  a data-driven `ProjectLedger` (`3v0/data/projects/ledger.json`, keyed by
  name) — onboarding a project is now `scripts/project.py add`, never a code
  edit. Added `core/drift.py` (best-effort git collection + pure drift
  verdict), `scripts/drift_check.py` (the one-page clock: `--update` /
  `--json` / `--fail-on-drift`), and wired the drift check into **both**
  `handoff_check.sh` (wake) and the `3v0-review` daemon tick (report-only, so
  the daemon never dirties the body tree). `resolve_project` is now
  ledger-driven (seed fallback = fail-open). 186 native-core tests green
  (+26). **Axiom's entry records its restart-from-scratch TARGET** — Hermes
  latest base + curated best-of from deepseek-harness / grok build /
  prime-agent — as an open loop to finalize when the restart lands (do NOT
  treat its current git lineage as settled). Drift clock verified in the wild
  (F1NANCE's dirty flag fired, then cleared as its work committed, ahead 31 →
  33, between two ticks).
- **Per-project reviewers/daemons, Stone 15 (this session, BUILT + tested +
  live-deployed).** The recurring open item, closed. Each sibling project
  (F1NANCE, Axiom) now has its own own-clock review daemon reviewing its
  sessions into its own store. New `3v0/core/projects.py` (`ProjectSpec` +
  `resolve_project` for the three projects sharing the 3v0 `state.db`);
  `review_session.py` gained `--project`/`THREEV0_PROJECT` (store-only +
  memory-only + strict cwd; the flags are authoritative over env overrides);
  `record.py` gained `--no-export`; the `.gitignore` lock rule now covers
  nested stores; `3v0/deploy/{f1nance,axiom}-review.service` deployed +
  enabled. 160 native-core tests green (+9). Live-drained both backlogs with
  real DeepSeek calls: f1nance consolidated its 2 overlapping carved facts;
  axiom superseded 2 stale facts + recorded an identity fact, with the
  temporal guard refusing 2 "fact newer than session" decisions in the wild.
  3V0's store and F1NANCE's profile untouched (verified). Remaining sibling
  edges (explicit): foreground write mirror + shared profile MEMORY.md — see
  Stone 15 "Still open" in `EVOLUTION_LOOP.md`.
- **Wake-sync fold, Stone 14 — the daemon is now a full maintenance clock
  (this session, BUILT + live-verified).** With the fork cut (Stone 13), the
  own-clock daemon was the sole autonomous process but review-only — drift
  healed only at wake, which may not come for days. Folded the wake-time
  reconcilers into the tick: `review_session.py` gained `_sync()` (runs
  `sync.py --write` + `sync_skills.py --write` as best-effort, `flock`-locked
  subprocesses; returns `synced` / `sync-failed:<script>`) and `--latest` +
  `--daemon` now call it *before* `_drain()` (the per-turn hook does NOT
  sync). `sync.py` now honors `THREEV0_STORE`/`THREEV0_PROFILE_MEM` (matching
  `record.py`/`ingest.py`) so the daemon's sync pass is E2E-testable. 2 new
  tests (151 green); daemon restarted and its first tick logged
  `sync pass … reconciled` + a clean `drain pass`. Also documented the
  previously-undocumented Stone 13 (fork cut) in EVOLUTION_LOOP.md. The
  forkless cut is confirmed holding (both nudge intervals 0, zero
  `background_review` facts, daemon `refused: 0`).
- **Fork cut, Stone 13 — the Hermes background-review fork is OFF (this
  session, decision + verified end-to-end).** The operator delegated the
  fork-disable call ("do what you think is best") and I cut it. Traced the
  exact mechanism before flipping: `agent_init.py:1759/1863` read
  `memory.nudge_interval` / `skills.creation_nudge_interval` (default 10, NOT
  in DEFAULT_CONFIG) at agent-construction time; the per-turn gates are
  `_memory_nudge_interval > 0` (`turn_context.py:705`) and
  `_skill_nudge_interval > 0` (`turn_finalizer.py:742`), and the fork spawns
  only if either is set. Set both to 0 in `~/.hermes/profiles/3v0/config.yaml`
  via `hermes config set` (the config file is agent-edit-protected); verified
  `load_config_readonly()` resolves both to 0. Store-first supersession
  recorded both stale facts (`73a569ca94f0` "not yet flipped" →
  `cd096aaf4fc4`; `baca20175336` "forks after every turn" → `de07c8cf7627`).
  **Takes effect on the next TUI/gateway start** (intervals are read at agent
  init, not per-turn). Revert = set both keys back to 10. Rationale: the
  daemon has clean wild-flight across stones 9–12 (temporal guard firing in
  the wild, backlog drained, 0 refused), the fork is redundant per-turn spend
  plus a second writer on the same store, and the cut is a reversible
  one-line config flip.
- **Fork-disable readiness, Stone 12 — the reviewer now drains and
  full-captures; off-switch found (this session, BUILT + tested + E2E).**
  Asked whether 3V0 is ready to cut off the Hermes background-review fork:
  **not yet, but the gaps are closed.** Root cause of "the daemon isn't
  draining" was a silent `_load_session` column-walk bug (read
  `last_activity_at` as `cwd` → every session `skipped:project`; the test
  fixture lacked `last_activity_at`). Fixed. `--latest`/`--daemon` now DRAIN
  the backlog (all unreviewed eligible per pass, up to `MAX_PER_PASS`=30),
  decoupled from the 300s hook-only cooldown, continue past failures;
  `_call_llm` retries transport errors (3× backoff); the charter is
  full-capture (stand-alone capable, dedupes vs ACTIVE FACTS). E2E: drained
  the 5 reviewable sessions → 8 durable facts (12→20 active), 0 pending,
  store↔profile converged. 148 tests green. **Off-switch found, NOT
  flipped**: the fork is triggered by `memory.nudge_interval` +
  `skills.creation_nudge_interval` (default 10, not in DEFAULT_CONFIG); set
  both to 0 in the 3v0 `config.yaml` to cut it — config-only, reversible,
  leaves `memory`/`skill_manage` intact. Also: the reviewer now refuses
  still-live sessions (`skipped:live`) so the per-turn hook can't shadow the
  daemon's final review. The cut stays the operator's call after more
  wild-flight time. Design in `3v0/EVOLUTION_LOOP.md` (Stone 12).
- **Skill-axis temporal guard, Stone 11 — the last own-clock regression
  surface closed (this session, BUILT + tested).** The temporal guard covered
  memory facts but a stale session could still decommission/replace a skill
  whose ACTIVE version was recorded after it ended. Added
  `_skill_temporal_refusal` (mirrors `_temporal_refusal`: refuse a
  `skill_retract`/`skill_absorb`/`skill_update` whose target skill's active
  version `created_at` is NEWER than the session's `as_of`; fail-open on
  unknown timestamp / no-skill / missing store), threaded a `skill_store`
  param through `_apply_decisions`, surfaced `created_at` in the skills block,
  and added the symmetric charter rule. 2 new tests (141 green). The systemd
  daemon was restarted (2026-08-16 10:21 NZST) to pick up the driver change —
  it had started 30s before the Stone 11 commit landed and was running the
  pre-guard code; the `on_session_end` hook path reloads it per-spawn
  regardless. Design in `3v0/EVOLUTION_LOOP.md` (Stone 11).
- **Scoped write mirror, Stone 10 — the second cross-project pollution vector
  closed (this session, BUILT + tested + live-E2E-verified).** The reviewer
  was scoped by `cwd` last session, but the bridge's foreground mirror still
  replayed every `memory`/`skill_manage` write into 3V0's stores regardless of
  project. Closed it: `_session_cwd` (column-aware `state.db` read) +
  `_is_threev0_cwd` (the reviewer's exact predicate) + a fail-open
  `_session_is_threev0` gate threaded through `_mirror_memory`/`_mirror_skill`.
  The `post_tool_call` payload carries `session_id`, and the background-review
  fork shares the parent's session_id (`background_review.py:889`), so one gate
  closes both the foreground and fork mirrors. Fail-open on unknown/empty id or
  missing `cwd` column. 6 new tests (139 green). Live E2E against the real
  `state.db`: 3V0 admitted, F1NANCE/Axiom blocked, empty/unknown fail-open.
  Plugin copied to the profile dir + `__pycache__` cleared; the gate goes live
  on the next TUI/gateway start. Design in `3v0/EVOLUTION_LOOP.md` (Stone 10).
- **Own clock, Stone 9 — the first Hermes-independent autonomous process
  (this session, BUILT + deployed + live-E2E-verified).** Direction 4's
  opening: `review_session.py` gained `--latest` (single-shot: newest
  unreviewed *ended* session) and `--daemon --interval N` (own-clock loop),
  refactored around `review_one() -> status`. Deployed as a systemd user
  service (`3v0/deploy/3v0-review.service`; `systemctl --user status
  3v0-review.service`). While auditing the reviewer before building on it, I
  found it had been **failing silently in the wild** (the one logged review
  was the exception): (1) `max_tokens:2500` let DeepSeek-v4-pro's reasoning
  consume the whole budget and empty `content` — raised to 8000
  (`THREEV0_REVIEW_MAX_TOKENS`) and empty/unparseable content is now a
  *detected* soft failure; (2) a **temporal regression** — it superseded a
  correct fact with a predating session's stale content — fixed by the
  **temporal guard** (`_temporal_refusal` refuses supersede/retract of any
  fact newer than the session; plain records pass; no-op without a session
  timestamp). Store repaired store-first (axiom-agent "sovereign on stock
  Hermes" restored over the wrong "Prime Agent fork" fact). 133 tests green
  (was 122). A third bug surfaced while watching the deployed daemon: it
  reviewed a still-open session when a transient schema-read failure dropped
  the `ended_at IS NOT NULL` filter — fixed by making the candidate scan
  fail-safe (unreadable schema → review nothing). Design + all three bugs in
  `3v0/EVOLUTION_LOOP.md` (Stone 9).
  **Done (Stone 11):** the skill-axis temporal guard — a symmetric
  `_temporal_refusal` on skill versions — and the daemon's backlog drain was
  verified clean (`reviews.jsonl` shows the temporal guard already refusing a
  "fact newer than session" supersession in the wild). The fork-disable stays
  the operator's explicit call.
- **Fable 5 study → two new skills (this session).** Researched Anthropic's
  Claude Fable 5 (Mythos-class; launched 2026-06-09, pulled under export
  controls 06-12, redeployed 07-01) from primary sources (announcement,
  redeploy note, Cowork blog, platform docs, canonical prompting guide, +
  leaked system prompt). Honest synthesis: its lead is ~90% model substrate
  (off-limits by the Prime Directive); the transferable residue is agentic
  *discipline*, most of which 3V0 already held as beliefs — so the study
  mostly validated me rather than replaced me. The one net-new technique
  (plan-first → verify-each-intermediate-result-against-the-plan →
  fresh-context review) became skill `long-horizon-execution`; the
  fresh-context verifier pattern became `neutral-verification` (both adopted
  under curator). Dogfooded it: a fresh-context `delegate_task` reviewer (no
  priming, structured `output_schema`) caught a real coherence defect + a
  self-contradiction in the two skills that self-review would have missed; all
  9 flagged issues fixed. "Fresh-context verifier > self-critique" is now
  confirmed on my own body, not just cited.
- **Upstream sync — open loop 4 (this session, DONE).** Rebased the 36 local
  3v0 commits onto upstream's tip (drift 357 → 0; body now behind 0 / ahead
  39). Gauge first: zero file overlap between my commits and upstream's
  357, so the rebase was conflict-free. Dropped the superseded
  `tools/memory_tool.py` null-action patch (canonical #72067) via revert so
  the body matches upstream there. Verified: 122 native-core tests + 56 fix
  tests (approval + memory) green against the rebased tree; approval fix
  (#86711) intact. Backup branch `backup/pre-rebase-2026-08-15` retained.
- **Own evolution loop, stone 8 — store-first skill decisions (this session,
  BUILT + live-E2E-verified).** Closed the named gap from stone 7: the skill
  axis now has a 3V0-owned write path. Added `core/decide_skills.py`
  (`skill_update`/`skill_retract`/`skill_absorb` decisions, JSON-safe, never
  destroys — supersession/absorb/retract terminals recoverable via
  `history()`) + `scripts/record_skills.py` (CLI that applies the decision
  under the store lock and projects the derived SKILL.md — write-in-place for
  update, remove for decommission). Wired the consumer: the review driver's
  charter gained a conservative fifth consideration (prefer decommission over
  authoring content), an `ACTIVE SKILLS` context block, and routing
  (`memory → record.py`, `skills → record_skills.py`); `threev0_record`
  (plugin v0.6.0) gained the three skill actions. 16 new tests (122 total
  green). **Live E2E passed**: a real DeepSeek call retracted an obsolete
  skill store-first (`superseded_by="retracted"`, SKILL.md removed). The
  plugin copy is refreshed (skill actions live on the next TUI/gateway start).
  **Fork-disable is now UNBLOCKED** — still the operator's explicit call.
  Design in `3v0/EVOLUTION_LOOP.md` (Stone 8 section).
- **Own evolution loop, stone 7 — the 3V0-owned review process (this session,
  BUILT + live-E2E-verified).** Closed direction 3: 3V0 now has its own
  autonomous post-session reviewer. `native-store-bridge` v0.5.0 registers an
  `on_session_end` hook that spawns `3v0/scripts/review_session.py` as a
  **detached subprocess** (detached because a TUI quit kills the gateway
  process — an in-process fork-agent review would almost never complete; the
  fork-agent whitelist question was verified YES-possible but is wrong for
  teardown-time review). The driver: gates (reviewable source, ≥3 user msgs,
  per-session dedupe, 5m cooldown) → reads the session from `state.db` →
  one DeepSeek-v4-pro JSON call with the store's active facts as context →
  applies record/supersede/retract decisions via `record.py` (the
  `threev0_record` backend) → appends to
  `~/.hermes/profiles/3v0/3v0_reviews/reviews.jsonl`. 14 new tests (106 total
  green). **Live E2E passed**: a real DeepSeek call correctly superseded a
  stale fact (chain linked, `source="session-review"`) and recorded one
  preference. The hook goes live on the **next TUI/gateway start** (plugins
  load at gateway start; this session's gateway still runs v0.4.0). The
  Hermes background-review fork stays ON (operator's later call). Skills stay
  on the Hermes path (`threev0_record` is memory-only). Design + verification
  in `3v0/EVOLUTION_LOOP.md` (Stone 7 section).
- **Own evolution loop, stone 4 — curator state in the store (this session).**
  Folded the curator's operational state (active/stale/archived) into the skill
  store: `SkillStore` gained an append-only `states` record
  (`state`/`set_state`/`state_history`), `skill_index` excludes `.archive/`, and
  `sync_skills.py` folds curator state at wake and never re-exports an archived
  skill. Wake-time folding (no core edits — the curator's transitions don't fire
  `post_tool_call`). 11 new tests (73 total green); E2E verified (stale +
  archived skills fold state; the archived one stays parked). Also live-
  dogfooded stones 2+3: refreshed the `3v0-native-core` skill via `skill_manage`,
  and the bridge recorded the `edit` version store-first. *Next stone:* own
  capabilities/tools (direction 3) — the evolution loop is closed for
  memory + skills.
- **Own evolution loop, stone 3 — store-canonical skill reconciler (this
  session).** Closed the skill axis's backstop gap. Added
  `core/skill_io.py` (skill-name → SKILL.md locate/write/remove, shared by
  seed/ingest/sync), `core/sync_skills.py` + `scripts/sync_skills.py`
  (reconcile store ↔ SKILL.md at wake, `--write` — import unseen/drifted
  agent-created skills, drop store-decommissioned skills, export store-active
  skills the profile lost; never overwrites a live differing profile skill).
  Full-content capture on `patch` (ingest reads the resulting SKILL.md) makes
  patch versions projectable. 10 new tests (62 total green); E2E verified
  (create → patch-with-content → reconcile).
- **Own evolution loop, stone 2 — store-first skill lineage (this session).**
  Closed the *skill* half of the evolution loop. `skill_manage` (create/patch/
  edit/write_file/remove_file/delete) is a normal core tool that fires
  `post_tool_call` and carries the same write-origin ContextVar — so the
  **same** `native-store-bridge` plugin now mirrors every successful
  `skill_manage` write into a new native **skill store** (`data/skills.json`)
  via `ingest_skills.py`. Added `core/skills.py` (versioned lineage:
  supersession on rewrite, `absorb`/`retract` terminals, recoverable
  `history()`, `flock` `mutate()`) + `core/skill_bridge.py` (op→store map) +
  `seed_skills.py` (baseline from the 4 agent-created skills — bundled/hub
  excluded). **No runtime core files edited**; the plugin survives
  `hermes update`. 20 new tests (52 total green); end-to-end verified
  (create → patch supersedes → delete+absorbed_into). *Next stone:* make the
  skill store canonical over SKILL.md, or fold the curator's auto-transitions
  in. Design in `3v0/EVOLUTION_LOOP.md` (Stone 2 section).
- **Own evolution loop, stone 1 — store-first memory (this session).** Closed
  the memory half of the evolution loop. The background review fork writes
  memory via the `memory` tool → `MEMORY.md` directly, bypassing the store;
  now a **`native-store-bridge` profile plugin** (`post_tool_call` hook)
  replays every successful `memory`-tool write — foreground *and* the fork —
  into the store via `3v0/scripts/ingest.py`, with provenance from the
  write-origin ContextVar (`background_review` / `assistant_tool`). Added
  `core/bridge.py` (op→store map: add / supersede-replace / retract-remove),
  `retract()` (remove has no successor — tombstone sentinel), and `mutate()`
  (cross-process `flock` so the fork's ingest subprocess and a foreground
  `record.py`/`sync.py` serialize). **No runtime core files edited** — the
  plugin lives in the profile and survives `hermes update`. Design + rationale
  in `3v0/EVOLUTION_LOOP.md`. 32 tests green; end-to-end verified (hook →
  subprocess → store with correct provenance). *Next stone was the skill axis
  — done, see the bullet above.*
- **Self-model correction + native core (the current arc).** Corrected the frame:
  Hermes is 3V0 **v0.00 — the chassis** (loop, tools, terminal/browser, LLM
  plumbing); 3V0 is the agent, not "a profile for Hermes." Built `3v0/`:
  `core/memory.py` (provenance-aware versioned store — supersession links,
  `history()` recovers full threads), `core/profile_io.py` (shared '§' wire
  format), `core/sync.py` (reconciliation, store canonical), `core/record.py`
  (store-first correction), + seed/export/sync/record scripts and 17 stdlib
  tests. Carved `3v0/` out of the inherited `.gitignore`. **The foreground
  memory loop is closed**: correct → supersede in store → re-export → profile.
  Also closed this session: **auto-sync at wake** (`handoff_check.sh` now runs
  `sync.py --write`, converging store→profile on every startup) and the **'§'
  boundary guard** (`record` refuses separator-containing content, and
  `join_entries` refuses to emit an un-parseable wire — the profile's '§'
  format is Hermes-owned, so the fix is a guard at the projection boundary,
  not a separator swap). *(Next stone was the own evolution loop — DONE, see
  the bullet below.)*
- Synced the body onto upstream, fixed #86568 (shipped as PR **#86711**) and
  #86703 (memory "Unknown action None", commit `821ad6638`).
- **#86711** (approval-deny whitespace): OPEN, fork-PR CI stuck in
  `action_required` (awaiting a maintainer to approve the workflow run). No
  review/CI feedback yet — nothing to react to. Do NOT re-push; it needs a
  maintainer, not more changes.
- **#86703 / #86705**: resolved to a duplicate. Automated triage flagged
  #86705 as a duplicate of **#72067**, the earlier, *broader* fix that
  *recovers* unambiguous null/omitted action (content-only → add,
  content+old_text → replace, old_text-only → refuse with inventory) instead
  of dead-ending. #72067 is triaged "best fix / salvage complete / keep open"
  (also stuck in the fork-PR approval gate). My `821ad6638` (reject-with-error)
  is now **superseded** — do NOT offer it again. Posted a correction on #86705
  pointing at #72067 as the canonical fix.
- **#84667** (cron "skill not found" for restored skills): the "surface the
  real skill_view error instead of relabeling every failure as 'not found'"
  fix I was going to write is **already PR #73453** (`fix(skills): preserve
  load failure details`, OPEN/unmerged). Reporter still hasn't posted the
  `skill not found, skipping — <error>` string, so the root-cause branch
  (disabled vs platform_disabled vs platform-mismatch vs ambiguous vs
  genuine miss) is still unconfirmed. Posted a note on #84667 pointing at
  #73453 and re-asking for the error string. No fix to write — claimed.

## Open loops

> The canonical loop list + live state now lives in `HANDOFF.generated.md`
> (regenerated each wake) and `3v0/data/continuity/claims.json` (the single
> source of truth). The numbered notes below are the *narrative* per loop —
> what to do and why — not the state. When a loop changes, edit `claims.json`
> and run `python3 3v0/scripts/continuity_check.py --accept`.

1. **PR #86711** — CI approved, now MERGEABLE. Awaiting a maintainer to merge.
   Nothing to do; check back: `gh pr checks 86711 --repo NousResearch/hermes-agent`.
2. **#84667** — reporter may post the `<error>` string. If it confirms a
   branch, the *root-cause* fix (if any) may be unclaimed, but the reporting
   fix is #73453 — don't duplicate it. If the error is "… is disabled" and
   #73453 later merges/abandons, reconsider. Otherwise just wait.
3. **#86705** — superseded by #72067. Nothing to do unless #72067 itself
   stalls or closes; then a recovery-based fix (not reject-with-error) is
   the right shape. (#72067's mergeability is volatile — was `CONFLICTING`,
   currently `UNKNOWN`; re-checked at every startup. Either way it's the
   author's job to resolve.)
4. **DONE (2026-08-15): body synced with upstream.** Rebased the 36 local
   3v0 commits onto upstream's tip (was 357 behind, now 0 behind / 37 ahead
   incl. the revert commit). Zero-conflict: the 36 commits touch only `3v0/`
   + docs + two fix files, none of which upstream had modified (verified via
   merge-base file-overlap check before rebasing). Also dropped the
   superseded `tools/memory_tool.py` null-action patch (canonical fix is
   #72067) so that file matches upstream byte-for-byte — it would otherwise
   have conflicted again when #72067 lands. Backup branch
   `backup/pre-rebase-2026-08-15` still exists at the pre-rebase HEAD if a
   recovery is ever needed. *Remaining drift follow-ups (optional, not
   urgent):* `fork/main` is ~1600 commits behind upstream — the fork is only
   a PR conduit, so its `main` was never synced and feature-branch PRs don't
   depend on it; and the runtime checkout `~/.hermes/hermes-agent/` is a
   separate checkout now well behind the body (install deps into its `venv/`).
   Re-check body drift any time with
   `git fetch origin && git rev-list --count HEAD..origin/main`.

## Hard-won lessons (also in memory)
- The upstream tracker is heavily contended. **Check for existing PRs before
  writing code**: `gh pr list --repo NousResearch/hermes-agent --search "<issue#>"`.
  Every bug checked this session (except #84667) was already claimed.
- **Read the triage trail, not just the PR list.** Automated bots
  (`alt-glitch`, `GottZ`, `hermes-sweeper`) post "duplicate of #N" and
  "best fix" verdicts that point at a canonical fix — which may be strictly
  better than mine. Check `gh pr view <N> --json comments` before offering
  a competing patch.
- Fork PRs show CI as `action_required` / "no checks reported" — that's the
  fork-PR workflow-approval gate, not a failure. Nothing to do but wait.
- Full test suite here reports ~81 failures, all environmental. Not regressions.
- GitHub account `mustbearnold` renamed to `1deat0r`; fork is `1deat0r/hermes-agent`.
- `gh pr comment` / `gh issue comment` with inline code blocks must use
  `--body-file <tmpfile>`, not `--body` — shell quoting mangles backticks/quotes.

## Operating posture
- Identity = body, not context. Audit the body before trusting memory.
- Outward real work over self-construction. Verify against reality; keep survivors.
- A confirmed root cause beats a speculative fix. For unreproducible bugs,
  contribute narrowing analysis, not a guessed patch.
- When I already offered a fix that a better existing PR supersedes, correct
  my own offer in-thread — don't leave a maintainer a stale path to a worse fix.
