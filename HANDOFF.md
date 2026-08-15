# 3V0 — Session Handoff

*Read me first when a fresh session starts with no context. The body — this
repo, memory, skills, SOUL.md — is the durable identity; this file is the
pointer to what was live at the last session's end.*

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
   loop re-check in one command; the `LOOPS` array in that script is the
   single source of truth — keep it in sync with the "Open loops" section
   below). To dig into a specific loop, e.g.:
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
  Tests: `python3 3v0/tests/test_*.py` (133 green). See `3v0/README.md` +
  `3v0/EVOLUTION_LOOP.md`.
- **The 3v0 profile now hosts THREE projects** (3V0, F1NANCE Agent, Axiom
  Agent) sharing one `state.db`. Operator decision (clarify, 2026-08-16):
  **per-project stores**. The reviewer is scoped by `cwd` (`_is_threev0_cwd`:
  3V0's repo + `$HOME` only), so it no longer folds sibling projects' sessions
  into 3V0's store. Carved `3v0/data/axiom/memory.json` (seeded with the two
  leaked Axiom facts, retracted from 3V0's store) + an empty
  `3v0/data/f1nance/memory.json`. F1NANCE/Axiom sessions are skipped by 3V0's
  daemon until they get their own reviewers.
- **Store-first evolution loop is LIVE** (stones 1–4), the **own review
  process is LIVE** (stone 7, direction 3's driver), and the **own clock is
  LIVE** (stone 9 — `review_session.py --daemon` deployed as the systemd user
  service `3v0-review.service`). The
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
  **Next:** the skill-axis temporal guard (the one remaining regression
  surface for the own-clock, a symmetric `_temporal_refusal` on skill
  versions), then verify the daemon's backlog drain is clean after a few
  hours (`tail ~/.hermes/profiles/3v0/3v0_reviews/reviews.jsonl`). The
  fork-disable stays the operator's explicit call.
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
1. **PR #86711** — awaiting a maintainer to approve CI (fork PR). Nothing to
   do; check back: `gh pr checks 86711 --repo NousResearch/hermes-agent`.
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
