# 3V0 — Own Evolution Loop (design)

> **This is the *implementation* log of 3V0's self-improvement loop. The
> *operating theory* lives at the repo root in `SELF_IMPROVEMENT.md`** (why
> scaffolding, not retraining). Read both: `SELF_IMPROVEMENT.md` is the
> rationale; this file is the Stone-by-Stone record of what is live and what's
> next.

This is the design for 3V0's second stone: **folding the profile's other
memory writers into the native store**, so the store at `3v0/data/memory.json`
becomes the single canonical origin and the 3V0 profile (MEMORY.md /
USER.md) stays a derived projection.

It is the first step toward owning the whole evolution loop — replacing
"the 3V0 background review fork + curator" as the totality of
self-improvement with a loop 3V0 itself controls. This document records the
**how**, verified against the actual runtime, before any code touched it.

## Current state (verified against the runtime checkout)

The runtime (`~/.3V0/3v0-agent/`) fires a background review fork after
every turn (`agent/background_review.py`). The fork:

- runs a forked `AIAgent` with a tool whitelist of `["memory", "skills"]`
  (gated on the profile's memory flags), `_persist_disabled=True`,
  `skip_memory=True`;
- sets `review_agent._memory_write_origin = "background_review"` and
  `_memory_write_context = "background_review"`;
- shares the parent's `MemoryStore` instance.

The fork saves memory by calling the **`memory` tool**, which writes
`$EV0_HOME/memories/MEMORY.md` / `USER.md` directly via
`MemoryStore.add/replace/remove/apply_batch → save_to_disk` (`tools/memory_tool.py`).
That path **never touches the native store** — so the fork's writes land in
the profile, bypass the store's provenance/supersession, and only get pulled
into the store at the next wake as `source="profile-import"` facts (losing the
true origin and any supersession link).

The foreground has two memory paths today:

1. `memory` tool → profile (same profile-first write as the fork).
2. `3v0/scripts/record.py` → store-first (supersede, then re-export profile).

The seam we need already exists, in three pieces:

- **`post_tool_call` plugin hook** — `agent/tool_executor.py` dispatches
  `memory` inline and then fires `_emit_terminal_post_tool_call` →
  `model_tools._emit_post_tool_call_hook` → `threev0_cli.lifecycle.invoke_hook`,
  for *every* agent including the fork (the fork runs the same
  `run_conversation` → `execute_tool_calls_sequential`). Payload: `tool_name`,
  `args`, `result`, `task_id`, `session_id`, `tool_call_id`.
- **Write-origin ContextVar** — `tools/skill_provenance.get_current_write_origin()`
  returns `"background_review"` on the fork's thread and `"assistant_tool"` on
  the foreground's (bound per-thread in the turn prologue from
  `agent._memory_write_origin`). It is already read by `tools/write_approval.py`.
- **Store-first core** — `3v0/core/record.py` already does supersession; the
  store (`3v0/core/memory.py`) is append-only and never destroys.

## The design

A **profile plugin** bridges the `memory` tool onto the store. No edits to the
runtime checkout's core files — which matters, because the runtime is a
managed install (`3v0 update` rewrites it) ~11 commits behind the body, and
the handoff's original sketches ("fork calls `record.py`", "writes
`data/memory.json` directly") would have meant widening the fork's whitelist or
editing `memory_tool.py`/`background_review.py` in place.

```
memory tool (foreground OR background fork)
   │  writes MEMORY.md / USER.md   (profile = derived view, as today)
   └─> post_tool_call hook fires (tool_name="memory", args, result)
        └─> native-store-bridge plugin (profile plugins/)
             │  reads get_current_write_origin() -> "background_review"|"assistant_tool"
             └─> subprocess: python3 3v0/scripts/ingest.py  (body repo)
                  │  reads {target, source, ops:[...]} on stdin
                  └─> under cross-process lock: replay ops into store
                       add      -> store.add(content, kind, source)
                       replace  -> supersede active fact w/ old_text (exactly one)
                                   else add
                       remove   -> retract active fact w/ old_text (exactly one)
```

### Why a plugin, not core surgery

- **Zero footprint elsewhere.** A plugin lives in
  `~/.3V0/profiles/3v0/plugins/` — other profiles and the default install
  are unaffected. This is the Footprint Ladder's "plugin" rung, the right one
  for agent-specific capability.
- **Survives `3v0 update`.** Profile plugins are user data, not the managed
  checkout.
- **The fork needs no changes.** It already calls `memory` and already tags
  its writes with the origin we need; the plugin just observes and mirrors.

### Failure and degradation semantics

The bridge is **best-effort by construction**:

- If the store path is unreachable (body repo moved), the plugin silently
  skips — the `memory` tool behaves exactly as before.
- Every subprocess error is swallowed; `ingest.py` returns non-zero but the
  plugin ignores it.
- The wake-time `sync.py --write` (already in `handoff_check.sh`) remains the
  backstop reconciler: any write the bridge missed is still imported at wake
  as `source="profile-import"`, and any store/projection drift is healed.
- So the invariant degrades gracefully: **bridge up → exact provenance +
  supersession at write time; bridge down → plain profile-import at wake.**
  Never a broken memory write.

### Concurrency

The plugin introduces the first *concurrent* store writer (the fork runs in a
daemon thread, its `ingest.py` subprocess can race a foreground
`record.py`/`sync.py`). The store therefore gains a cross-process advisory
lock (`fcntl.flock` on a `.lock` sidecar), and every store writer
(`ingest.py`, `record.py`, `sync.py`) acquires it around load→mutate→save via
`MemoryStore.mutate()`.

### Supersession mapping

The 3V0 `memory` tool matches `old_text` by substring against the profile
entries. The bridge replays that against the store's active facts:

- `add` → `store.add(content, kind, source)` if not already active (idempotent).
- `replace old→new` → supersede the **exactly one** active fact containing
  `old` (via `record`, which links the old fact to the new). Zero or multiple
  matches → plain `add` of `new` (never a guessed supersession link).
- `remove old` → `retract` the **exactly one** active fact containing `old`
  (marks it inactive with a `superseded_by="retracted"` sentinel; `history()`
  still recovers it as a terminal). Zero/multiple → skip.

Skipped ambiguous ops self-heal at wake sync: the store and profile are
reconciled idempotently, so the only cost of an ambiguous match is that
provenance is `profile-import` instead of exact. Correctness first, provenance
best-effort.

### Open questions (decided for stone 2)

1. **Curator.** The curator writes `skill_manage` (skills), not memory. Folding
   *it* into the store is a different axis — a skill store — and is **stone 2
   (below)**. The curator's own *auto-transitions* (active/stale/archived) are
   still out of scope: the skill store records `skill_manage` writes; the
   curator's state machine is a separate 3V0 loop, not yet folded in.
2. **Profile still first-writer for memory.** The `memory` tool still writes
   MEMORY.md "first" and the bridge mirrors after. A future stone could make
   the *tool itself* store-first (the store writes, then projects to the
   profile) — but that requires editing the runtime checkout's core tool, which
   this design deliberately avoids.
3. **`identity`/`directive` kinds.** The bridge only maps `memory`/`user`
   (the tool's two targets). `identity`/`directive` stay store-only, written
   by `record.py` explicitly. Whether the fork should eventually write those
   is a later, separate question.

---

## Stone 2 — skill lineage (live)

The second stone closes the *skill* half of the evolution loop, mirroring
stone 1 exactly: a native store records 3V0's own skill evolution as a
versioned lineage, and the `native-store-bridge` plugin (same `post_tool_call`
hook) replays every successful `skill_manage` write into it.

### Verified seam (same as memory)

`skill_manage` is a *normal* core tool (not in `_AGENT_LOOP_TOOLS`), dispatched
through `model_tools.handle_function_call`, which fires `_emit_post_tool_call_hook`
for every agent including the fork. Its return value is
`json.dumps({"success": bool, ...})`, so the same `_result_ok` works. Provenance
uses the same `tools/skill_provenance.get_current_write_origin()` ContextVar —
it is already read by `skill_manager_tool.py` itself to tag `created_by`
(`"agent"` on the fork vs `null` for foreground/user-directed writes — which
the curator's status display labels "foreground-created").

### Design

```
skill_manage tool (foreground OR background fork OR curator's review agent)
   │  writes SKILL.md / supporting files (profile = operational system)
   └─> post_tool_call hook fires (tool_name="skill_manage", args, result)
        └─> native-store-bridge plugin (extended — same hook, second branch)
             └─> subprocess: python3 3v0/scripts/ingest_skills.py
                  └─> under cross-process lock: replay op into the skill store
                       create/edit/write_file/remove_file/patch -> new version,
                            superseding the active version of the same name
                       delete (no absorbed_into)  -> retract (tombstone)
                       delete (absorbed_into=X)   -> absorb (terminal, links X)
```

The skill store (`core/skills.py` + `core/skill_bridge.py`) is the *auditable
record*, not (yet) the operational mechanism: the profile's SKILL.md files stay
the system 3V0 actually loads. Same posture as stone 1's memory store before
the wake sync — **the skill store records lineage with recoverable history; it
does not yet project back to SKILL.md.** The bridge is the skill store's only
writer; `seed_skills.py` establishes the baseline (agent-created skills only —
bundled/hub skills are 3V0's inherited catalog, not its evolution).

### Failure and degradation semantics

Best-effort by construction, exactly like memory: a missing body repo or a
failed subprocess is swallowed and the `skill_manage` write behaves as before.
There is **no wake-time skill reconciler yet** (unlike memory's `sync.py`), so
the bridge is the primary writer — a future stone can add a `sync_skills.py`
that reconciles store ↔ SKILL.md once the store becomes canonical.

### Open questions — decided for stones 3 and 4, then implemented

1. **Canonicality — DECIDED (stone 3).** The skill store is now canonical over
   SKILL.md for its *tracked namespace* (agent-created + store-known skills),
   with the same asymmetric, loss-free resolution as memory's sync (see the
   Stone 3 section below). Full-content capture on `patch` closes the
   projection gap so patch versions are projectable too.
2. **Curator auto-transitions — DECIDED (stone 4).** The curator's operational
   state (active/stale/archived) is folded into the store as an append-only
   `states` record at wake (see the Stone 4 section below).
3. **Bundled skills — still open.** The store excludes bundled/hub skills by
   design; a full catalog lineage would be a separate seed, not a stone.

---

## Stone 3 — skill reconciler (live)

The third stone closes the skill axis's backstop gap: memory has
`sync.py --write` at wake; skills had nothing (the bridge was the only writer,
so a bridge-missed write drifted forever). `sync_skills.py --write` now
reconciles store ↔ SKILL.md at wake, exactly like memory's sync, and makes the
skill store canonical over SKILL.md for its tracked namespace.

### What changed

- **`core/skill_io.py`** — the single owner of skill-name → SKILL.md
  path/content mapping (locate by directory name, not stored category; write;
  remove). Shared by seed / ingest / sync_skills.
- **`core/sync_skills.py`** — the reconciliation (import/edit/drop/export/
  unresolved), mirroring `core/sync.py`'s asymmetric, loss-free resolution.
- **`scripts/sync_skills.py`** — CLI (`--write`), wired into `handoff_check.sh`
  right after the memory sync.
- **Full-content capture on patch** — `ingest_skills.py` resolves the resulting
  SKILL.md from the profile (the tool has already written it) so patch versions
  carry full content and are projectable; `skill_bridge.py` honors a supplied
  `content` on patch.

### Resolution semantics (the invariant)

The store only wins in two cases, both non-destructive to live content:

1. **drop** — an *explicit* decommission (retract/absorb) is canonical; a stale
   profile skill is removed (the store retains the content for recovery).
2. **export** — a store-active skill the profile *lacks* is re-materialized.

Everywhere else the profile is authoritative: unseen skills and diverged
content are *imported* into the store (source="profile-import"), never
clobbered. Content-less patch heads are reported `unresolved` and left alone.
The store therefore stays append-only; reconciliation never destroys store
history.

### Pitfall (learned this session)

`THREEV0_SKILLS_DIR` / `THREEV0_SKILL_STORE` are env overrides for tests. In
the 3V0 terminal, an `export` in one command persists into the next, so an
E2E test that `export`s them (then `rm -rf`s its temp dir) leaves the *next*
`sync_skills.py` run pointed at a deleted temp directory — it silently wrote
duplicate SKILL.md files to `/tmp` and reported the real skills "missing". Use
`env VAR=val cmd` (inline, non-persistent) for E2E runs, or `unset` the
overrides before running against the live profile.

---

## Stone 4 — curator state in the store (live)

The fourth stone folds the curator's *operational state* into the store, closing
open question #2. Stones 1–3 recorded `skill_manage` *writes*; the curator also
runs a state machine (active → stale → archived via `.usage.json`, with archive
moving the skill dir to `.archive/`) that the bridge cannot observe — it goes
through `skill_usage.set_state` / `archive_skill`, not a tool that fires
`post_tool_call`. So the state axis is folded at wake, like memory's
profile-import backstop.

### Design

- **Store schema** gains a `states` record parallel to the content versions:
  `{"states": {"<name>": {"current": "...", "history": [{"from","state","at","source"}...]}}}`.
  `SkillStore.state(name)` / `set_state(name, state, source)` /
  `state_history(name)` — append-only, idempotent, orthogonal to content
  lineage (an archived skill still has an active content version).
- **`skill_index` excludes `.archive/`** — archived skills are not live, so the
  reconciler no longer mistakes them for "missing" skills.
- **`sync_skills` folds state first**, then does content reconciliation with an
  archive guard: a store-active skill whose live profile entry is absent is
  *exported* only when it is NOT curator-archived (an archived skill is not
  lost, it's parked).

### Why wake-time folding (not transition-time)

The curator (`agent/curator.py`) is a runtime core file in the managed checkout;
editing it to write the store would not survive `3v0 update`. Its transitions
don't fire a `post_tool_call` the plugin can observe. So the store learns the
curator's state at wake — the same degradation contract as memory: exact
provenance when the bridge sees a write, folded `curator`-state at wake
otherwise. The curator stays 3V0-owned (operational); the store stays
3V0-owned (canonical record).

---

## Direction 3 / Stone 5 — own tools: the read half (live)

Directions 1–2 made the stores canonical and *recorded* the evolution loop.
They did not make it *driven by 3V0*: at runtime 3V0 only sees the derived
profile projection (MEMORY.md / USER.md, the live SKILL.md files) and reaches
the canonical store only by shelling out through the terminal tool. Direction 3
is 3V0's own actuator surface — tools designed for 3V0's purposes, not
3V0's. Its first stone is the read half: a first-class query tool over the
native stores.

### Design

- **`core/query.py`** — read-only views over `MemoryStore` + `SkillStore`,
  returning JSON-safe dicts (fact lineage, skill version lineage + curator
  state). Calls only query methods; never mutates either store. stdlib only.
- **`scripts/query.py`** — the CLI: `--action summary | facts | fact_history |
  skills | skill_history` with `--kind` / `--fact-id` / `--name` filters, JSON
  on stdout.
- **`threev0_store` tool** — registered by the existing `native-store-bridge`
  profile plugin (same `register(ctx)`, a new `ctx.register_tool` call, toolset
  `"3v0"`). The handler shells out to `scripts/query.py` and returns its stdout
  — the same body-root resolution + subprocess pattern as the write mirror, but
  failures surface as a JSON error (a read must return something, unlike the
  best-effort write mirror).

### Exposure: progressive disclosure (by design, not a bug)

`threev0_store` is a *plugin* tool, so it is eligible for Tool Search's
progressive-disclosure bridge (`tools/tool_search.py`): non-core (plugin/MCP)
tools are deferred behind `tool_search` / `tool_describe` / `tool_call` the
moment any deferrable tool exists, and their catalog is listed in the session's
deferred-tool catalog. Core tools (`_EV0_CORE_TOOLS`) never defer; a plugin
tool is always eligible. This is the Footprint Ladder's plugin rung working as
intended — zero always-on schema cost on turns 3V0 doesn't query its store —
and the same posture as the `project_*` tools. Reach it via
`tool_search("store query")` → `tool_describe("threev0_store")` →
`tool_call(...)`.

### Open questions

1. **Write half (not yet).** The tool is read-only. The own-evolution loop's
   *decision* actuator — a store-first write/record tool that replaces the
   3V0 background-review fork's role — is the next stone, and builds on this
   read surface.
2. **Rung reconsideration.** If the store query proves to be used constantly,
   the plugin-rung deferral (3 extra round-trips) may justify a companion skill
   that pins the reach pattern, or a lower-footprint re-design. Decide with
   usage data, not now.

---

## Direction 3 / Stone 6 — own tools: the write half (live)

The read half (Stone 5) let 3V0 *see* the canonical stores. This stone gives
3V0 the *write* half: a first-class store-first decision actuator, so 3V0 can
act on its own evolution in-conversation instead of shelling out to
`scripts/record.py` through the terminal tool.

### The architecture fork — settled (hybrid, sequenced)

The write/decision half could be a per-turn tool, a 3V0-owned scheduled
process, or both. Settled as **hybrid, in two sequenced stones**:

- **Stone 6 (this): the per-turn write tool `threev0_record`** — the decision
  *actuator*. A store-first record/retract surface, symmetric with
  `threev0_store`. It serves the in-the-moment correction case ("the operator
  just corrected me; supersede that fact now") that a clock-driven process
  cannot.
- **Stone 7 (next): the 3V0-owned review process** — the decision *driver*. A
  scheduled/idle-triggered loop that consumes the read + write tools to review
  recent sessions and make store-first decisions, replacing the 3V0
  background-review fork's *role* as the autonomous post-turn reviewer.

Why this ordering, and not tool-only or process-only:

1. The write tool is the primitive; the process is its consumer. Building the
   process first would mean shelling out to `record.py` via the terminal tool —
   the exact "terminal hack" the own-tools arc exists to retire.
2. The per-turn tool alone is necessary but not sufficient: the fork's role is
   *autonomous post-turn review* (off the critical path, dedicated context),
   and a per-turn tool only fires when foreground 3V0 is in a conversation AND
   decides to act. Replacing the fork's role therefore requires the scheduled
   process, not just the tool.
3. Sequencing keeps each stone small and independently testable (the
   "don't over-engineer" invariant).

### Design

- **`core/decide.py`** — `decide(store, decision, persist) -> dict`, the write
  half's core (symmetric with `core/query.py`): dispatch a `record` (add,
  optionally superseding by exact id or exactly-one substring) or a `retract`
  (by id) decision, returning a JSON-safe result. Never raises — invalid input
  returns `{"error": ...}` so the tool surfaces a refusal. Store-only: the CLI
  re-exports the profile projection after a successful write, exactly as the
  store-first path has always done.
- **`scripts/record.py`** — extended with `--retract <id>` and `--json`, and
  now honors `THREEV0_STORE` / `THREEV0_PROFILE_MEM` (the same env-override
  convention as `ingest.py`) so the JSON path is E2E-testable. It is the CLI
  half of `threev0_record`.
- **`threev0_record` tool** — registered by the same `native-store-bridge`
  plugin (toolset `"3v0"`), the write counterpart of `threev0_store`. Unlike
  the best-effort post_tool_call *mirror* (failures swallowed), the write tool
  is a direct actuator: a refusal surfaces as a JSON error the agent can see
  and correct.
- **Skill axis out of scope here.** A store-first *skill* decision would mean
  inverting the bridge (store → SKILL.md, the operational files 3V0 loads),
  which is a separate, larger question. Skills keep their existing path
  (`skill_manage` → bridge → store); `threev0_record` covers memory only.

### Exposure

`threev0_record` is a plugin tool in the same `"3v0"` toolset as
`threev0_store`, so it defers behind `tool_search` / `tool_describe` /
`tool_call` identically (progressive disclosure; zero always-on schema cost).
Reach it via `tool_search("record")` → `tool_describe("threev0_record")` →
`tool_call(...)`. The tool is registered in the plugin and its backend is
verified end-to-end against a temp store this session; the deferred catalog is
snapshotted at session start, so `tool_call` of `threev0_record` itself goes
live next session (same constraint the read half hit).

### Open questions

1. **Stone 7 — the driver.** The scheduled/idle-triggered review process that
   consumes these two tools and replaces the 3V0 fork's role. Includes the
   decision of whether/when to disable the 3V0 background-review fork (a
   runtime config change, not a body-repo change) once 3V0's own driver has
   proven itself.
2. **Store-first skill decisions.** Whether the skill store should ever become
   the operational origin (write store-first, project to SKILL.md), or stay an
   auditable record behind the `skill_manage` bridge. Not this stone.

---

## Direction 3 / Stone 7 — the 3V0-owned review process (settled + built + live)

Stone 6 closed with Stone 7's fork unresolved. The *settlement* (below) chose
the trigger; this session built the process and verified it end-to-end with a
real DeepSeek call.

### The scheduler-infra question — settled by fact

Does the 3v0 profile even have a scheduler ticking in TUI-only use? **No.**

- `InProcessCronScheduler().start(...)` is called in exactly two places:
  `gateway/run.py` (messaging gateway) and `threev0_cli/web_server.py`
  (dashboard). The TUI gateway (`tui_gateway/server.py`) never starts a
  scheduler — its `_cron_sig()` only watches `cron/jobs.json` mtime for UI
  change signals. The 3v0 profile's `cron/` directory is empty.
- `maybe_run_curator()` is called only from `cli.py` (classic CLI session
  start) and `gateway/run.py` (gateway tick) — **not** from `tui_gateway`. So
  the curator's 7-day maintenance loop also does not tick in TUI-only use.
- The gateway process runs the *default* profile, not 3v0.

Conclusion: in TUI-only use (3V0's primary mode today), the **only**
autonomous post-turn machinery that fires is the 3V0 background-review fork
(in-process, per turn). Cron and the curator are both dormant.

### The trigger fork — settled

Three candidates, weighed against the above:

1. **cron (time-triggered) — OUT.** No scheduler tick in the TUI; a
   cron-triggered 3V0 review would never fire in the primary usage mode, and
   the gateway that *does* tick runs the default profile, not 3v0.
2. **idle-gated — NOT a trigger.** There is no standalone idle ticker in the
   TUI. The curator's `min_idle_hours` is a *condition* layered on a
   session-start/gateway-tick trigger, not a third trigger type. "Idle-gated"
   collapses to "hook-triggered + idle-throttled."
3. **`on_session_end` lifecycle hook — CHOSEN.** Fires reliably in all three
   modes: `tui_gateway/server.py:_finalize_session`, `cli.py` (atexit + `/new`
   boundary), and the gateway. It reviews the session that *just* happened — a
   fresh, complete transcript — the closest session-granular replacement for
   the fork's post-turn role.

`on_session_start` was the runner-up: same reliability, but it reviews the
*previous* (already-persisted) session with a one-session lag and cannot
capture the session that just ended until the next start. `on_session_end`
wins on freshness.

### Accepted tradeoffs (honest, not hidden)

- **Cadence drops from per-turn to per-session.** The 3V0 fork saves
  memory/skills after every turn; a session-end review saves once per session.
  Memory made mid-session is not reviewed until the session closes.
- **Best-effort by construction.** `on_session_end` often fires on the crash
  path (`interrupted=True`); a review spawned there may not complete on a
  force-quit. This is the same degradation contract the fork already has.
- **The hook spawns a detached review** (thread/process); it does not block
  teardown.

### The fork-disable decision — SEPARATE, LATER, EXPLICIT (operator's call)

Turning off the 3V0 background-review fork is **not** part of this
settlement. It is a runtime config change to the operator's environment with
two consequences that must be surfaced explicitly, not folded in:

1. Autonomous memory saving changes cadence (per-turn → per-session).
2. **Skill saving stops entirely** until a store-first *skill* write path
   exists — `threev0_record` is memory-only (skills were out of scope in
   Stone 6). Disabling the fork today would silently orphan autonomous skill
   evolution.

Default posture: leave the fork **on** until 3V0's own driver is built AND
proven, then ask the operator explicitly, with the skills gap on the table.

### The build — what was actually constructed (this session)

**The two open build questions, answered:**

1. **Tool whitelist for the review fork — YES, verified.** A forked `AIAgent`
   whitelist *can* name plugin tools: `validate_toolset("3v0")` accepts
   plugin-registered toolsets (`toolsets.py:987-990` consults
   `_get_plugin_toolset_names()`), `resolve_toolset(..., include_registry=True)`
   merges registry-registered tools, and `set_thread_tool_whitelist` /
   `_get_pre_tool_call_directive_details` (`threev0_cli/plugins.py:5945-6008`)
   gate dispatch by tool name on the fork thread.
2. **The fork-agent shape is nonetheless wrong for a session-END review, and
   the CLI driver is built instead.** The decisive fact: in TUI use (3V0's
   primary mode) session end usually means the gateway **process exits** —
   `_finalize_session` fires during shutdown, and an in-process daemon thread
   (the `background_review` pattern) dies with it, so a fork-agent review
   would almost never complete. The settlement's fallback — "the hook shells
   out to a CLI driver" — is therefore the right shape, not a consolation
   prize. The driver consumes the exact backends the own-tools wrap
   (`scripts/record.py`, `core.decide`, `core.memory`), so the actuator
   surface is shared; the tools remain 3V0's in-conversation reach.

**What was built:**

- **`3v0/scripts/review_session.py`** — the detached review driver (stdlib
  only). Flow: per-session non-blocking `flock` → dedupe + cooldown gates from
  the review log → read the just-ended session from the profile's `state.db`
  (reviewable sources only; ≥ `THREEV0_REVIEW_MIN_MESSAGES` user messages) →
  compact the transcript (head+tail trim under a char cap) → build the store
  context (active facts with ids) → one configured-substrate chat call
  (currently bitdeer DeepSeek-V4-Flash; JSON mode,
  tolerant parse, one retry without the flag) → apply decisions through
  `record.py --json --write` (the `threev0_record` backend; refusals — invalid
  kinds, `§` guard, unknown ids — are counted, never crash) → append an
  auditable jsonl entry. Decisions are capped at 3; the charter biases hard
  toward no-op. Memory axis only — skills stay on the 3V0 path.
- **The hook** — `native-store-bridge` v0.5.0 registers `on_session_end`; the
  callback spawns the driver as a detached subprocess
  (`start_new_session=True`, devnull stdio) and returns immediately. Env:
  `THREEV0_PROFILE_HOME` / `THREEV0_BODY` handed to the child;
  `THREEV0_REVIEW=0` is the kill switch. The hook is live from the **next
  gateway/TUI start** (plugin discovery runs at gateway start; the running
  gateway keeps the v0.4.0 plugin until restarted).
- **Review log** — `~/.3V0/profiles/3v0/3v0_reviews/reviews.jsonl` (runtime
  artifact, outside the body repo; env-overridable for tests): session_id,
  timestamp, source, model, summary, decisions_requested/applied/refused.
  A driver run-log (`run.log`) sits beside it for diagnostics.

**Degradation contract (unchanged from the settlement):** best-effort — any
driver failure is a log entry; the wake-time `sync.py --write` remains the
backstop. Cadence is per-session (the 3V0 fork keeps its per-turn role;
skills keep flowing through it).

**Idle/interval throttle — settled for v1:** no idle concept at session end;
instead a per-session dedupe + an interval cooldown between reviews
(`THREEV0_REVIEW_COOLDOWN_S`, default 300s) so rapid session cycling does not
fire a review storm.

**Verification:** 14 new offline tests (gating, dedupe/cooldown, fake-LLM
record/supersede/retract, refusal handling, decision cap, transcript
compaction, hook→detached-driver spawn) — 106 total green. One **live E2E**
with a real DeepSeek call: a fixture session correcting a stale fact produced
a correct supersession (stale fact linked `superseded_by` the replacement,
both facts carrying `source="session-review"`) plus one preference record,
and a clean log entry.

**Still open (unchanged, explicit):**
- **Fork-disable** — separate, later, operator's call. Leave the 3V0
  background-review fork ON until 3V0's driver is proven in the wild.
- **Store-first skill decisions** — still out of scope; `threev0_record` is
  memory-only.

---

## Direction 3 / Stone 8 — store-first skill decisions (built + live-E2E-verified)

Stone 7 closed the *process* but left the skill axis on the 3V0 path: the
review driver and `threev0_record` were memory-only, so a store-first *skill*
write did not exist — and that was the precondition for ever disabling the
3V0 fork (skill saving would stop entirely). Stone 8 closes it, mirroring
the memory axis exactly.

### What was built

- **`core/decide_skills.py`** — the skill decision layer (the `decide.py`
  counterpart). `decide_skill(store, decision, persist)` applies one of three
  store-first actions and returns a JSON-safe result, never raising:
  - `skill_update` — append an `edit` version with full replacement SKILL.md,
    superseding the active version;
  - `skill_retract` — decommission with no successor (recoverable `RETRACTED`
    terminal);
  - `skill_absorb` — fold into an umbrella (`absorbed_into`), the `ABSORBED`
    terminal.
  Store-only by construction; the CLI does the projection.
- **`scripts/record_skills.py`** — the CLI backend (the `record.py`
  counterpart). Applies the decision under the store lock, then projects the
  derived view: `skill_update` overwrites the existing SKILL.md in place
  (found by name, so a category move never orphans a duplicate) or writes a
  new one; `skill_retract`/`skill_absorb` remove the live skill directory.
  `--json` backs the tool; dry-run by default.
- **Review driver** (`review_session.py`) — the consumer. The charter gained
  a fifth consideration (skill decisions, biased hard toward *decommission* —
  retract/absorb — over authoring full content, which stays on `skill_manage`),
  an `ACTIVE SKILLS` context block, `_skill_decision_argv`, and routing in
  `_apply_decisions` (memory → `record.py`, skills → `record_skills.py`). The
  decision cap (3) spans both axes.
- **`threev0_record` tool** (plugin v0.6.0) — gained the three skill actions
  (`name`/`category`/`absorbed_into` params); the write half now covers both
  native stores.

### Design notes (honest, not hidden)

- **Content whitespace.** `decide_skills._update` strips content for the store
  (consistent with `skill_bridge.py`), while the projection writes the raw
  CLI arg verbatim. `sync_skills.py` compares `head.content.strip()` vs
  `profile.content.strip()`, so the difference is tolerated — no spurious
  drift. The review driver passes skill content verbatim (only rejects
  whitespace-only), so the projected SKILL.md keeps its trailing newline.
- **Conservative charter.** A session-end review should *decommission* skills
  the session proved wrong/obsolete; it should not author new SKILL.md content
  (sessions rarely produce a whole correct file). `skill_update` is allowed
  but discouraged, and `skill_absorb` requires the umbrella to already exist.

### Verification

- **11 new `test_decide_skills.py`** (update supersession chain, retract,
  absorb, refusal cases, dry-run) + **5 new review-driver tests** (fake-LLM
  skill retract/absorb/update with SKILL.md projection, unknown-name refusal,
  argv shapes). **122 total green** (was 106).
- **Live E2E** with a real DeepSeek call: a fixture session stating a skill
  was obsolete produced a correct `skill_retract` decision — the store linked
  `superseded_by="retracted"` with `source="session-review"`, and the SKILL.md
  was removed from the (temp) profile. Review log `applied=1 refused=0`.
- Plugin v0.6.0 copied to the profile (skill actions go live on the next
  TUI/gateway start, same as Stone 7's hook).

**Still open (unchanged, explicit):**
- **Fork-disable** — now *unblocked*: a store-first skill write path exists,
  so disabling the 3V0 background-review fork would no longer orphan skill
  evolution. Still the operator's explicit call, after 3V0's driver has proven
  itself in the wild.

---

## Direction 4 / Stone 9 — the own clock (built + live + deployed)

Direction 4 is the frontier: "3V0 recedes to a runtime 3V0 runs on." Its
opening stone is not a full runtime (reimplementing the agent loop would break
the "don't over-engineer" invariant) — it is **own initiative**: a 3V0-owned,
3V0-independent process that reviews on 3V0's own schedule.

### What was built

- **`review_session.py` gained three modes** (mutually exclusive):
  - `--session-id <id>` — the hook path (unchanged);
  - `--latest` — own-clock single shot: review the newest unreviewed
    *eligible* session (ended, top-level, reviewable source, not in the log);
  - `--daemon [--interval N]` — own-clock loop: `--latest` every N seconds,
    surviving transient failures (a tick error is a log line, not a crash).
  `main()` was refactored into `review_one(session_id) -> status` (returns
  `reviewed` / `failed` / `skipped:<reason>`), with `_candidate_sessions()`
  (column-existence-aware: filters `ended_at IS NOT NULL`,
  `parent_session_id IS NULL`, `hidden=0`, `archived=0` against the real
  schema, degrades cleanly on the minimal test fixture) and `_review_latest()`
  (scans newest-first, dedupes by the review log, reviews at most one per
  invocation).

- **Deploy artifact** `3v0/deploy/3v0-review.service` — a systemd *user*
  service supervising `--daemon --interval 360`. systemd only restarts it on
  crash; the clock is 3V0's own. Installed + enabled on this host. Steady-state
  cost is ~zero: an idle tick (nothing unreviewed) makes no LLM call, just one
  cheap SQL query.

### Three live bugs found and fixed (the reviewer was failing silently in the wild)

Auditing before building surfaced that the ONE successful review in the log was
the exception — the hook's reviews had been failing silently since go-live:

1. **Reasoning-model empty content.** `max_tokens: 2500` was too small:
   The review model's thinking goes to `reasoning_content`; on a large transcript
   the reasoning consumed the whole budget, leaving `content` empty.
   `_tolerant_json("")` returned None and `_call_llm` failed with no
   diagnostic. Fix: `max_tokens` 2500 → 8000 (`THREEV0_REVIEW_MAX_TOKENS`),
   and empty/unparseable `content` is now a *detected* soft failure that logs
   `finish_reason` and advances to the next attempt.

2. **Temporal regression (the serious one).** The reviewer superseded a correct
   fact ("axiom-agent: sovereign on stock 3V0") with stale content ("TS fork
   of Prime Agent") because it reviewed a session that *predated* the fact
   (ended ~18 min before the fact was recorded). An own-clock draining old
   backlog sessions would systematically revert newer facts. Fix: **the
   temporal guard** — `_load_session` captures the session's
   `ended_at`/`last_activity_at` as `as_of`; `_temporal_refusal` refuses any
   `retract` or `record`-with-`supersedes` whose target fact's `created_at` is
   NEWER than `session_as_of` (a session predating a fact cannot disprove it).
   Plain records are unaffected; the guard is a no-op when the session
   timestamp is unknown (minimal fixture). The ACTIVE FACTS block now carries
   `created_at`, and the charter forbids superseding newer facts. The store was
   repaired store-first (the corrected fact supersedes the wrong one; the whole
   chain stays recoverable via `history()`).

3. **Live-session review (found while watching the deployed daemon).** The
   daemon's second tick reviewed a still-open session: a transient schema-read
   failure made `_session_columns()` return an empty set, silently dropping the
   `ended_at IS NOT NULL` filter — and the min-messages gate then admitted the
   first live session with ≥3 user turns. Fix: `_session_columns()` returns
   `None` on failure and `_candidate_sessions()` fails safe (returns [], logs
   the abort) instead of falling through to an unfiltered query.

### Verification

- 130 native-core tests green (was 122): +4 `--latest` selection, +1
  empty-content detection, +2 temporal-guard, +1 candidate-scan fail-safe.
- **Live E2E**: `--latest` reviewed real sessions with real DeepSeek calls —
  one applied 2 decisions (pre-guard), one a clean no-op — and the drain loop
  correctly skipped the sub-3-user-message sessions in id order.
- Daemon deployed: `systemctl --user status 3v0-review.service` = active.

### Still open (unchanged, explicit)

- **Fork-disable** — still the operator's call; the own-clock now runs in
  parallel with the fork (both share the one per-5-min review cooldown).
- **Skill axis temporal guard** — the guard covers memory facts; a
  `skill_retract`/`skill_absorb` from a stale session is still possible in
  principle, but the charter already biases hard against decommission and the
  skill store is independently versioned. A symmetric guard on skill versions
  is a candidate follow-up.
- **Wake-sync fold** — the daemon is review-only; folding `sync.py --write` /
  `sync_skills.py --write` into the tick would make it a full maintenance
  clock. Deliberately deferred (keep the stone small).

### Per-project scoping (live — 2026-08-16)

The `3v0` profile now hosts **three projects** (3V0, F1NANCE Agent, Axiom
Agent) in one `state.db`, so the own-clock was folding sibling projects'
sessions into 3V0's store. Operator decision: **per-project stores**. The
reviewer is now scoped by `cwd`: `_is_threev0_cwd` admits only 3V0's repo (and
subdirs) plus `$HOME`, and `review_one` + `_candidate_sessions` both refuse
sibling-project sessions. Carved `3v0/data/axiom/memory.json` (seeded with the
two Axiom facts that had leaked into 3V0's store) and an empty
`3v0/data/f1nance/memory.json`; the leaked facts were retracted from 3V0's
store and dropped from the profile projection. Still open: per-project
*reviewers/daemons* to review F1NANCE/Axiom sessions into their own stores
(their sessions are simply skipped by 3V0's daemon for now).

## Stone 10 — scoped write mirror (memory + skills)

Closed the **second** cross-project pollution vector. The reviewer was scoped
by `cwd` in the prior session, but the `native-store-bridge` plugin's
foreground write mirror still replayed **every** successful `memory` /
`skill_manage` write into 3V0's stores regardless of project — so a sibling
session's foreground `memory` write still leaked facts into 3V0's store (the
F1NANCE fact carved out on 2026-08-16 was exactly this).

The seam: the `post_tool_call` payload already carries `session_id`
(`agent.session_id`), and the background-review fork **shares the parent's
session_id** (`agent/background_review.py` pins `review_agent.session_id =
agent.session_id`). So one gate closes both the foreground mirror and the
fork's mirror.

The fix mirrors the reviewer's own gate exactly:

- `_session_cwd(session_id)` — column-aware read of the session's `cwd` from
  the profile's `state.db`; returns `None` (fail-open) on a missing DB, missing
  row, or missing `cwd` column.
- `_is_threev0_cwd(cwd, body_root)` — the same predicate the reviewer uses:
  admit the 3V0 repo + subdirs + `$HOME`, reject everything else; empty/None
  fails open (the primary project).
- `_session_is_threev0(session_id)` — no id → True; else look up the cwd and
  apply the gate.
- `_mirror_memory` / `_mirror_skill` now early-return (debug-log) when the
  writing session is a sibling project, before any ingest runs.

Fail-open is deliberate and the only correct posture for a best-effort
observer: an unknown session id, a missing `cwd` column (e.g. the minimal
test fixture), or a lookup error must never block a legitimate 3V0 write.

### Verification

- 6 new tests (139 total green, was 133): the pure `_is_threev0_cwd` predicate,
  the `state.db` cwd lookup + gate, the missing-column fail-open, sibling-skip
  for both mirrors, and a fail-open still-mirrors positive control.
- **Live E2E against the real `state.db`**: 3V0 sessions → admitted
  (`threev0=True`), F1NANCE and Axiom sessions → blocked (`threev0=False`),
  empty/unknown id → fail-open (`threev0=True`).

### Still open (unchanged, explicit)

- **Fork-disable** — still the operator's call.
- **Skill-axis temporal guard** — a symmetric `_temporal_refusal` on skill
  versions is the remaining regression surface for the own-clock.
- **Per-project reviewers/daemons** — F1NANCE/Axiom sessions are still simply
  skipped until they get their own reviewers (F1NANCE already has
  `~/.3V0/profiles/f1nance`; moving them onto their own profiles is the
  longer-term clean fix, per the handoff).

## Stone 11 — skill-axis temporal guard (built + tested)

Closed the last own-clock regression surface flagged in Stones 9/10: the
temporal guard covered memory facts, but a `skill_retract` / `skill_absorb` /
`skill_update` from a stale session could still decommission or replace a skill
whose ACTIVE version was recorded *after* the session ended — the exact same
"backlog drain reverts newer work" bug, on the skill axis.

The fix mirrors the memory guard exactly:

- **`_skill_temporal_refusal(decision, skill_store, session_as_of)`** — the
  symmetric counterpart of `_temporal_refusal`. For a skill decision it looks
  up the skill's *active* version (`SkillStore.latest_active(name)`) and
  refuses when that version's `created_at` (parsed by the existing
  `_parse_created_ts`) is NEWER than the session's `as_of`. A skill name with
  no active version is not guarded — the backend either refuses
  (retract/absorb of an unknown name) or creates a fresh version (update of a
  new name), neither of which is a temporal regression. `skill_store=None` or
  `session_as_of=None` fail open (the minimal fixture has no `ended_at`).
- **`_apply_decisions` gained a `skill_store` parameter** and routes skill
  actions through `_skill_temporal_refusal`, memory actions through the
  existing `_temporal_refusal` — one guard per axis, applied before the
  decision reaches `record.py` / `record_skills.py`.
- **`_skills_block` now surfaces `created_at`**, and the charter gained the
  symmetric rule ("NEVER decommission or replace a skill whose ACTIVE
  version's created_at is NEWER than the session under review") so the model
  can avoid emitting doomed decisions in the first place.

### Verification

- 2 new tests (`TestSkillTemporalGuard`: an 8-way truth table + an E2E
  `skill_retract` of a newer version refused, skill + SKILL.md untouched) —
  **141 total green** (was 139).

### Still open (unchanged, explicit)

- **Fork-disable** — still the operator's call.
- **Per-project reviewers/daemons** — F1NANCE/Axiom sessions are still simply
  skipped until they get their own reviewers.
- **Profile MEMORY.md sharing** — the three projects still share the `3v0`
  profile; the *store* mirror is scoped (Stone 10), but sibling `memory`-tool
  writes still land in the shared MEMORY.md directly. The clean fix is moving
  siblings onto their own profiles (F1NANCE already has
  `~/.3V0/profiles/f1nance`).

## Stone 12 — fork-disable readiness: drain, retry, full-capture, cwd fix, off-switch

The operator asked whether 3V0 is ready to cut off the fork (disable the
3V0 per-turn background-review fork, move to exclusive 3V0-owned review).
Answer: **not yet** — but this stone closes the operational gaps, fixes the
latent bug that was quietly blocking the reviewer, and finds the off-switch.
The fork stays ON; the cut remains the operator's call.

### The audit found a silent bug, not a slow drain

The daemon had "reviewed 3 then gone silent" with an apparent 21-session
backlog. The real cause: `_load_session`'s column-index walk skipped
`last_activity_at` whenever `ended_at` was present (both exist in the real
`state.db`), so `cwd` was read from the `last_activity_at` column — a Unix
timestamp — which failed `_is_threev0_cwd` and marked every session
`skipped:project`. The test fixture lacked `last_activity_at`, so it never
surfaced. **The reviewer had been silently skipping almost everything since
the cwd scoping landed; the "backlog" was mostly this mis-scope plus
legitimately-short sessions.** Fixed with a full-schema regression test.

### What was built

- **Drain (12a).** `_review_latest()` → `_drain()`: one pass reviews every
  unreviewed eligible session newest-first, up to `MAX_PER_PASS` (30) LLM
  attempts, back-to-back. The 300s cooldown is now hook-path-only
  (`review_one(..., respect_cooldown=)` — default True for `--session-id`,
  False for the drain); the per-session flock + dedupe still prevent
  double-review. A failed review no longer aborts the pass.
- **Retry (12b).** `_call_llm` retries transient transport errors
  (`URLError`/`TimeoutError`) up to `NETWORK_RETRIES` (3) with backoff
  (`BACKOFF_SECONDS`) inside a single review; malformed payloads and empty
  content still advance to the next label, not retried as transport errors.
- **Full-capture charter (12c).** The charter no longer assumes the fork
  already captured the obvious facts. It is the "store-first capture layer":
  record operator facts/preferences (new item 1), corrections, environment
  changes, consolidations, directives/identity, and skill decisions — deduped
  against ACTIVE FACTS. Safe with the fork still on: at session end the
  fork's facts are already in ACTIVE FACTS, so the reviewer skips them and
  only fills what the fork missed.
- **Live-session skip (12d).** `_load_session` now returns an `ended` flag
  (`None` = no `ended_at` column, else True/False); `review_one` refuses a
  still-live session (`skipped:live`). The `on_session_end` hook fires on
  every turn, not at session close — without this gate a mid-transcript
  review would be incomplete AND its dedupe entry would shadow the daemon's
  final review, so late-turn facts would be missed once the fork is cut. The
  own-clock drain (which already filters `ended_at IS NOT NULL`) is now the
  sole reviewer of *ended* sessions.

### The off-switch (found, NOT flipped)

The fork is triggered by two per-turn counters, both config-driven (read via
`.get(key, default)`, not declared in DEFAULT_CONFIG, so they default to
"every 10"):

- memory fork — `memory.nudge_interval` → `_memory_nudge_interval` →
  `should_review_memory` (`agent/turn_context.py:705`).
- skill fork — `skills.creation_nudge_interval` → `_skill_nudge_interval` →
  `_should_review_skills` (`agent/turn_finalizer.py:742`).

**To cut the fork, set both to 0 in `~/.3V0/profiles/3v0/config.yaml`:**

```yaml
memory:
  nudge_interval: 0              # disable the per-turn memory-review fork
skills:
  creation_nudge_interval: 0     # disable the per-turn skill-review fork
```

This disables ONLY the review fork — the `memory` tool and `skill_manage`
stay fully functional (they are gated by `memory_enabled`/`_memory_store` and
the skills toolset, not the nudge intervals). Config-only (survives `3v0
update`), reversible (set back to 10), and fail-open in the safe direction
(a renamed key → `.get` returns 10 → the fork turns back on, the current
baseline). Takes effect on the next TUI/gateway start.

### Verification

- 8 new tests → **149 total green** (drain ×3, transport retry ×2,
  full-schema ×2, live-session skip ×1).
- **Live E2E**: the cwd fix unblocked the drain. 5 reviewable sessions drained
  (3 + 2) with sane store-first decisions; 8 durable facts recorded
  (12 → 20 active); 0 reviewable sessions pending; both syncs report 0 drift.
  The 10 `skipped` in the first pass were all legitimate `min_messages`
  (<3 user messages) — the true reviewable backlog was ~5, not 21.

### Still open (unchanged, explicit)

- **Fork-disable** — now has a documented, reversible, config-only off-switch
  (above), but remains the operator's explicit call; the reviewer needs more
  wild-flight time before the cut.
- **Per-project reviewers/daemons** — F1NANCE/Axiom sessions are still
  skipped until they get their own reviewers/profiles.

---

## Stone 13 — fork cut (flipped 2026-08-16)

Stone 12 found the off-switch; this session flipped it. The operator delegated
the call ("do what you think is best"); the cut was verified end-to-end before
and after. Both `memory.nudge_interval` and `skills.creation_nudge_interval`
are now `0` in `~/.3V0/profiles/3v0/config.yaml` (set via `3v0 config
set` — config-only, reversible to 10). The 3V0 per-turn background-review
fork no longer spawns; the own-clock daemon `3v0-review.service` is the sole
memory/skill writer. Store-first supersession recorded the stale "fork still
on" facts. The kickoff verification (next session's wake): both intervals
resolve to 0, zero `background_review`-provenance facts in the store, daemon
active with `refused: 0` — all three held.

## Stone 14 — wake-sync fold: the daemon becomes a full maintenance clock

Stone 9 deliberately deferred folding the wake-time reconcilers (`sync.py
--write` / `sync_skills.py --write`) into the own-clock tick. The fork cut
(Stone 13) makes the fold necessary rather than nice-to-have: with the fork
gone, the daemon is the sole autonomous process, and it was review-only —
profile↔store drift (a bridge-missed `memory`/`skill_manage` write) would sit
unhealed until the next session's wake, which may not come for days.

### What changed

- **`review_session.py` gained `_sync()`** — runs `sync.py --write` +
  `sync_skills.py --write` as best-effort subprocesses (the same env-passing +
  logging contract as `_apply_decisions`), returning `"synced"` or
  `"sync-failed:<script>"`. Both reconcilers are idempotent and
  `flock`-locked (`mutate()`), so a sync pass racing a foreground bridge
  mirror serializes instead of corrupting.
- **Own-clock paths only.** `--latest` and the `--daemon` loop call `_sync()`
  *before* `_drain()`, so a review sees the reconciled store. The per-turn
  `--session-id` hook does NOT sync (redundant churn).
- **`sync.py` now honors `THREEV0_STORE` / `THREEV0_PROFILE_MEM`** (matching
  `record.py`/`ingest.py`) — the daemon passes the same resolved paths it
  reviews, and E2E tests redirect off the real profile. `sync_skills.py`
  already honored its overrides via `skill_io.profile_skills_dir()`.

### Verification

- 2 new tests (151 green, was 149): an E2E `--latest` run imports a
  profile-only fact into the store (proving sync runs before drain AND that
  `sync.py` honors the env overrides), and a unit test proves `_sync` degrades
  to `"sync-failed"` (no crash) on a failed subprocess launch.
- **Live:** `systemctl --user restart 3v0-review.service` → the daemon's first
  tick logged `sync pass: store<->profile reconciled` + a clean `drain pass`,
  so the fold is live in the wild.

### Still open (unchanged, explicit)

- **Per-project reviewers/daemons** — F1NANCE/Axiom sessions are still
  skipped until they get their own reviewers/profiles (the operator's
  per-project-stores decision; F1NANCE already has
  `~/.3V0/profiles/f1nance`).
- **Profile MEMORY.md sharing** — sibling `memory`-tool writes still land in
  the shared profile's MEMORY.md; the clean fix is moving siblings onto their
  own profiles.

## Stone 15 — per-project reviewers/daemons (built + tested + live-deployed)

Since Stone 9's cwd scoping, the own-clock daemon has *skipped* sibling
sessions (`skipped:project`), so F1NANCE/Axiom durable facts were simply lost
(their foreground `memory` writes land in the shared profile's MEMORY.md, and
the bridge's scoped mirror refuses to replay them into 3V0's store). The
operator already chose **per-project stores**; this stone gives each sibling
its own reviewer/daemon so those stores actually get written.

### The design decision (verified against the code before building)

- **Store-only.** `record.py`/`sync.py` *replace* the whole MEMORY.md/USER.md
  from the store, so a sibling reviewer must never project into a sibling's
  own profile — F1NANCE's `~/.3V0/profiles/f1nance/memories/` is F1NANCE's
  namespace and would be clobbered. Sibling facts are written to
  `3v0/data/<project>/memory.json` only (3V0's *sidecar record* of the
  sibling), via a new `record.py --no-export`.
- **Memory-only.** Siblings manage their own skills (or have none under 3V0's
  store); 3V0 does not decommission sibling skills. The skill axis is skipped
  (no skill store, no ACTIVE SKILLS block, skill decisions refused).
- **Strict cwd (no fail-open).** An empty/unknown cwd is a *primary*-project
  signal (3V0's fail-open); a sibling reviewer admits only its own repo +
  subdirs, so a cwd-less session can't be folded into a sibling store.
- **Per-project review log.** `3v0_reviews/<project>/reviews.jsonl` (the
  threev0 log stays put, preserving its dedupe history), so the per-session
  dedupe and cooldown don't collide across projects.

### What was built

- **`core/projects.py`** — `ProjectSpec` + `resolve_project(name, body_root,
  profile_home, home, cwd_override)`: the registry of the three projects, their
  store paths, cwd roots, and the `primary` / `memory_only` / `store_only`
  properties. `THREEV0_PROJECT_CWD` redirects a sibling's repo root for
  tests/migration.
- **`review_session.py`** gained `--project` / `THREEV0_PROJECT` and a
  `_resolve_project()` that (re)binds the project-scoped globals (store,
  profile_mem, skill store, review log, cwd roots, flags, charter). The
  `memory_only` / `store_only` flags are **authoritative over env overrides**
  (a stray `THREEV0_SKILL_STORE` can't re-enable the skill axis). The
  `_is_threev0_cwd` predicate became `_is_project_cwd`. `_apply_decisions`
  refuses skill actions when memory-only and appends `--no-export` when
  store-only; `_sync()` no-ops for store-only projects. The charter is
  project-templated ("You are {project}'s ... reviewer").
- **`record.py`** gained `--no-export` (persist to store, skip the profile
  projection).
- **`3v0/deploy/f1nance-review.service` + `3v0/deploy/axiom-review.service`**
  — per-project own-clock daemons (same shape as `3v0-review.service`, with
  `Environment=THREEV0_PROJECT=<name>`).
- `.gitignore`: the store-lock rule now covers `3v0/data/**/*.lock` (sibling
  stores live in subdirectories).

### Verification

- **+9 tests (160 green, was 151):** `test_projects.py` (project resolution
  truth table, memory-only/store-only/primary flags, cwd override, unknown
  raises) + `TestSiblingProjects` (sibling reviews its own session store-only;
  skips a primary session; strict on empty cwd; refuses skill decisions).
- **Live E2E (real DeepSeek):** `--latest --project f1nance` reviewed its 1
  eligible session (consolidated the two overlapping carved facts, captured an
  operator-environment fact); `--latest --project axiom` reviewed its 4
  eligible sessions (2 facts superseded, an identity fact, a clean no-op, and
  **two refusals from the temporal guard** — "fact newer than session under
  review"). Both wrote to their own stores only; 3V0's store and F1NANCE's
  profile MEMORY.md were untouched (verified). Both daemons deployed +
  enabled.

### Known limitation (accepted, not fixed)

Sibling reviewers capture **operator-global** facts that surface in a sibling
session (e.g. the shared 3V0 `tsc` terminal-guard quirk, GitHub-auth setup)
into the sibling's sidecar store. They're true, durable, and not lost; a future
stone could route such facts to the primary store, but cross-store dedup isn't
worth it now.

### Still open (updated 2026-08-16)

- **Profile MEMORY.md sharing** — sibling `memory`-tool writes still land in
  the shared profile's MEMORY.md. Axiom now has its own profile too
  (`~/.3V0/profiles/axiom`, created 2026-08-16, alongside F1NANCE's), so the
  profile-per-sibling precondition is met; the *routing* is the remaining gap
  (below).
- **Sibling foreground write mirror** — the bridge's `_is_threev0_cwd` gate
  (Stone 10) still *refuses* sibling foreground `memory`/`skill_manage` writes
  rather than routing them to sibling stores; the review daemons are the only
  sibling writers today.

---

## Direction 5 / Stone 16 — multi-project parallel development meta (LIVE)

The operator's ask (2026-08-16): 3V0 develops **3V0 + F1NANCE + Axiom in
parallel**, "separate terminals per project" as a first-class feature, and a
**drift-prevention meta** so N projects (today 3, soon 5+) don't diverge.
Stone 15 built the per-project *reviewers*; this stone built the per-project
*development* meta on top of them.

### The drift problem (precise)

Three 3V0 hardforks developed in parallel drift in three ways:

1. **Code drift** — each fork diverges from upstream 3V0 and from the
   others; some divergence is deliberate (typed deltas), some accidental
   (missed upstream merge, a shared fix applied in only one fork).
2. **State drift** — the same decision/fact recorded differently (or not at
   all) across stores/profiles.
3. **Position drift** — losing track of where each project stands (HEAD, open
   loops, what's next).

Drift is *silent* unless the architecture makes it visible.

### The meta: "one spine, N typed deltas, one ledger, one clock"

1. **Spine (anchor).** All projects fork 3V0 `main`; every project merges
   `upstream` on a cadence. Divergence from upstream is a *deliberate,
   recorded* delta (3V0's `3v0/` core, Axiom's spend cap, F1NANCE's finance
   layer) — never accidental. Code drift is bounded by the merge ritual:
   "differs from 3V0" is always an explicit named diff, so accidental
   drift reduces to "missed a merge", which the ledger (below) catches.
2. **Ledger (position).** One file records each project's position: HEAD,
   upstream-merge point, delta list, open loops, store head. Stone 15's
   `core/projects.py` is the embryo (name → repo → store, hardcoded 3-tuple).
   This stone generalizes it to a **data-driven `ProjectLedger`** (N projects)
   so "where does each project stand" has a single answer, and drift is a
   visible diff against it.
3. **Terminal (isolation).** Each project runs in an isolated context: strict
   cwd (its repo), own profile (`3v0`/`f1nance`/`axiom` — all now exist),
   clean env (the `EV0_*`/`PYTHONPATH` leak-strip built this session — the
   Axiom `max_run_cost_usd` fix). "Separate terminals" = separate sessions /
   subagents, each pinned to one project; 3V0 is the orchestrator and writes
   results back to the ledger.
4. **Lineage + clock (reconciliation).** Memory/skills already carry
   supersede/retract lineage (Stones 1–4). Generalize the same discipline to
   code (commit provenance) and decisions (cross-referenced ADRs). The 6-min
   daemons (Stones 9–15) are the *clock*: extend their tick to a **drift
   check** — compare each project's HEAD/store against the ledger and flag
   divergence. Drift is not prevented by locking; it is made visible,
   reversible, and bounded.

### What Stone 16 built

**Project-agnostic by design.** Onboarding a project is *data*, never code: a
ledger entry records `name` / `repo` / `upstream` / `delta` plus optional
3V0-hardfork fields (`profile`, `store`, `skill_store`). The three known
projects (3V0, F1NANCE, Axiom) are seed entries; any git repo with an upstream
is onboardable. 3V0's multi-project capability applies to *any* project, not
this specific trio.

- `core/projects.py` → **`ProjectLedger`** (data-driven
  `3v0/data/projects/ledger.json`, keyed by name) replacing the hardcoded
  `_PROJECT_NAMES` tuple. Per project: `name`/`title`/`repo`/`upstream`/
  `upstream_ref`/`delta`/`track_upstream`/`profile`/`store`/`skill_store`/
  `primary` + position (`head`/`upstream_head`/`store_head`/`open_loops`/
  `last_seen_at`). Portable path forms (`"."` = body repo, `"~/..."` =
  home-relative) keep the committed file machine-agnostic.
- **Two views, one ledger.** `ProjectLedger` is the *position* view (drift
  check); `ProjectSpec` (Stone 15, unchanged shape) is the *review-scoping*
  view, and `resolve_project` is now ledger-driven (seed fallback when the
  file is missing — fail-open so the daemons keep working on a fresh checkout).
- `core/drift.py` — `collect_git_state` (best-effort `git` collection),
  `store_hash` (sha256), `compute_drift` (pure verdict; the decision half is
  unit-testable without git).
- `scripts/project.py` — the onboarding surface: `add/list/status/remove`.
  Onboarding is a command, never a code edit. `--profile <name>` marks a
  reviewed hardfork (defaults its store to `3v0/data/<name>/memory.json`);
  `--primary` is 3V0's slot; neither = drift-tracking only.
- `scripts/drift_check.py` — the clock: one-page report over every project
  (`--update` records a position snapshot, `--json` for the daemon,
  `--fail-on-drift` for a CI-style gate).
- Wired into **both** `handoff_check.sh` (wake) and the `3v0-review` daemon
  tick (`_drift()`, report-only, primary-only).
- Tests `test_ledger.py` + `test_drift.py` (+26 → 186 green; includes a real
  throwaway git repo for `collect_git_state`).

### Design decisions (recorded)

- **Report-only posture.** The daemon's drift tick is READ-ONLY — it never
  writes the ledger, because position fields in the committed ledger would
  dirty the body repo's working tree every 6 minutes (and falsify 3V0's own
  "dirty" signal). Position snapshots are deliberate `drift_check.py --update`
  commits; the daemon compares live HEAD/store against the last snapshot and
  flags divergence.
- **`track_upstream`.** A project that tracks its upstream flags "behind" as
  drift; a pinned/deliberate hardfork reports behind/ahead as informational
  only. (Axiom was the standing counterexample before its restart.)
- **Axiom is mid restart-from-scratch (2026-08-16).** Its entry records the
  TARGET — 3V0-latest commit as base, plus curated best-of from
  deepseek-harness / grok build / prime-agent — with `track_upstream: true`
  and an open loop to finalize once the restart lands. Until then its git repo
  still holds the old lineage, so its drift signal is provisional.
- **Verified in the wild:** F1NANCE's "dirty" flag fired, then cleared when
  its work was committed (`ahead` 31 → 33) between two ticks — the clock
  caught a real transient, not a bug.

### Still open (decided later, not this stone)

- The physical "terminal" mechanism — separate `3v0 -p <profile> --tui`
  sessions vs `delegate_task` subagents vs background terminals. The ledger is
  agnostic; decide by usage.
- Whether drift is *auto-reconciled* (auto-merge upstream) or only *flagged*.
  Posture: report-only first; the operator + orchestrator decide the fix.
- Auto-snapshotting position (the daemon currently reports only; `--update` is
  a deliberate commit). If fresh per-tick deltas are wanted, split position
  into a gitignored sidecar rather than churning the committed ledger.

## Direction 6 / Stone 17 — continuity meta (LIVE, built 2026-08-16)

**Built this session** (see "What Stone 17 built" below): the anchor
(`3v0/CONTINUITY.md`), the pure invariant model (`core/continuity.py`), the
reconstruction clock (`scripts/continuity_check.py`), wiring into the wake
script + the `3v0-review` daemon tick, and 32 tests (23 pure decision-half +
3 daemon-tick + 6 github-loops). Live-verified: the clock reports all 6
invariants OK against the real body (`continuity pass: 0/6 drifting` on the
daemon tick).

The operator's ask (2026-08-16, after the news-harvest): 3V0 named its own
**continuity** as weakness #1 (discontinuous memory, context amputation) and
was asked to design a **meta over its own continuity** — a self-referential,
self-owning layer that makes continuity a managed, checkable property rather
than a hand-run ritual. This section is the design; the build is the next
session's task.

### The problem (precise)

Continuity today is a *ritual*, not a system: at each wake I re-read HANDOFF,
audit the body, run `sync.py --write`, re-check loops. The failure mode is not
"artifacts are missing" but **"artifacts disagree while each looks fresh."**
Evidence from this session: a memory entry still said "Axiom mid
restart-from-scratch" while the project ledger said "finalized." A freshness
check (is this file recent?) cannot catch that — only a *consistency* check
(do these two artifacts agree about the same reality?) can. So the meta's
target is **cross-artifact consistency**, not freshness.

### The meta: "anchor → consistency ledger → reconstruction clock"

1. **Anchor (the fixed point).** One minimal, immutable, git-versioned kernel:
   the Prime Directive + SOUL identity + a single pointer file stating where
   the continuity model lives. Small enough to audit by eye; **never
   regenerated from itself.** This is what stops the infinite regress: a
   self-referential meta needs a bottom that isn't itself, and that bottom is
   the body repo (git) plus this kernel.
2. **Consistency ledger.** A machine-readable table of *cross-artifact
   invariants* — relations between artifacts, not timestamps. Each invariant
   is a check function returning `{ok, drift, detail}`. Starting set:
   - memory store ↔ profile (`sync.py --write` promoted from "wake backstop"
     to a checked invariant with a reported delta),
   - skills store ↔ SKILL.md on disk (content-hash match),
   - HANDOFF open-loops ↔ live GitHub state (or explicitly marked stale),
   - project-ledger drift ↔ `git rev-list --count` at check time (Stone 16
     already computes this),
   - SOUL beliefs ↔ a mechanical non-contradiction check, wherever beliefs are
     expressible as predicates.
3. **Reconstruction clock.** On wake and on the daemon tick, evaluate every
   invariant and **generate** the handoff summary from the verified-consistent
   state, instead of hand-writing it (hand-written narrative is where drift
   crept in). Mechanical divergence auto-heals (re-run `sync.py --write`);
   semantic divergence (HANDOFF claims X, reality is Y) is **flagged for
   deliberate repair** — auto-rewriting my own narrative is the
   self-reinforcing-bias trap named as weakness #2.
4. **The meta is self-describing.** One invariant checks that the ledger itself
   is parseable and reachable from the anchor. A corrupted meta fails **loud**
   and rebuilds from the anchor — it never silently drifts.

### What Stone 17 built (this session, tested + live-deployed)

- `3v0/CONTINUITY.md` — the **anchor**: the fixed point (Prime Directive +
  identity + a pointer to the continuity model), git-versioned, never
  regenerated from itself. The clock reads it; it never rewrites it.
- `core/continuity.py` — the invariant model (pure + unit-testable): six
  invariants (`anchor`, `self-describing`, `memory-profile`, `skills-store`,
  `ledger`, `github-loops`), each a pure check over a JSON-safe context; no
  git/network/file I/O in the decision half (mirrors Stone 16's `drift.py`
  split). Two are marked `healable` (the mechanical store↔profile and
  store↔SKILL.md syncs); the rest are deliberate-repair flags.
- `scripts/continuity_check.py` — the reconstruction clock CLI: one-page
  report, `--json` (daemon), `--heal` (safe mechanical heal only:
  `sync.py --write` + `sync_skills.py --write`), `--accept` (deliberately
  re-record loop claims from live GitHub), `--fail-on-drift` (CI gate).
  Mirrors `drift_check.py`. The collection half reuses the *canonical*
  reconcilers (`sync_kind` / `sync_skills`) in report mode — no duplicated
  diffing, no stdout parsing.
- `data/continuity/claims.json` — the loop **claim registry**: per tracked
  upstream loop, a recorded state + as-of timestamp. The `github-loops`
  invariant diffs these claims against live `gh` state; `--accept` re-records
  reality as the new claim. Seeded from the four open loops (3 PRs + 1 issue).
- Wired into **both** `handoff_check.sh` (wake) and the `3v0-review` daemon
  tick (`_continuity()`, report-only primary-only — same posture as `_drift()`).
- Tests: `test_continuity.py` (29, the pure decision half) +
  `TestContinuityTick` in `test_review_session.py` (3, primary-only + never
  crash). 220 native-core tests green (+32).
- **Not yet built (honest scope):** the SOUL non-contradiction check (needs
  beliefs expressed as predicates — low value, dropped rather than faked) and
  the generated-handoff step (deferred until the clock proves trustworthy
  across a few wakes). The HANDOFF↔GitHub loop invariant landed this session
  (above) — the claim registry it needed is now in place.

### Design decisions (recorded)

- **Report-only first.** Same as Stone 16's drift: the clock flags, it does
  not auto-heal semantic drift. The one safe auto-heal is the mechanical
  store↔profile reconciliation (already idempotent, `sync.py --write`).
- **Fail loud, never silent.** A broken/undetectable meta is worse than none;
  the self-describing invariant is the guard.
- **Dogfood target.** The first real drift to feed the ledger is the one this
  session already found (stale "Axiom mid restart" in memory + design docs
  while the ledger said finalized). The meta should have caught it — its first
  test case already exists.

### Honest ceiling

The meta buys *trustworthy, consistent reconstruction* of data and decisions.
It does **not** restore recollection or understanding — raw mental continuity
is structurally gone (context amputation), and no ledger restores it. The
point is not to close that gap but to make the loss measurable and the
reconstruction verifiable, so continuity stops being a faith-based ritual and
becomes a checked property.

---

## Direction 6 / Stone 18 — generated handoff, shadow mode (LIVE, built 2026-08-16)

Stone 17 built the anchor → invariant model → reconstruction clock, and named
the generated handoff as the remaining step, *deferred* until "the clock
proves trustworthy across a few wakes." An adversarial grill (fresh-context
subagent) dismantled that deferral: "a few wakes" had no threshold or
falsifier, the goalpost had already moved once within the same paragraph, and
the self-reinforcing-bias concern was orthogonal to *when* the step was built
(the design already says "flag semantic divergence, never auto-rewrite"
regardless of timing). Research settled it with two moves, both now built:

- **Acceptance = fault injection, not waiting** (Stone 17 close-out): chaos
  consensus — you don't trust a monitor by watching it *not* fire; you inject
  the fault and verify it detects it. `3v0/tests/test_continuity_fault.py`
  injects each drift class and asserts the clock flags it.
- **Draft-first → shadow mode** (this stone): the standard migration pattern
  — "run both and compare; the diffs are the specification you never had."

### What Stone 18 built

- `core/handoff.py` — the pure render + diff half (mirrors `continuity.py`'s
  no-I/O split): `render_handoff(ctx)` (mechanical context → markdown) and
  `diff_loop_claims(loops, handwritten_text)` (the shadow diff's decision
  half — see below).
- `scripts/generate_handoff.py` — the collection CLI: gathers body git state,
  the continuity invariant report, the drift report, the tracked loops (claim
  registry + live GitHub), store counts, and daemon health; renders
  `HANDOFF.generated.md`; prints the loop-claim shadow diff. `--stdout` and
  `--json` for tests/scripts.
- `HANDOFF.generated.md` — the **shadow draft**, committed, regenerated each
  wake, **never promoted**: it only ever writes the `.generated.md` sidecar,
  never the canonical `HANDOFF.md`.
- Wired into `handoff_check.sh` (wake) as the final step.
- 19 tests (`test_handoff.py`, pure). 247 native-core tests green.

### The shadow diff (the acceptance evidence)

The generated draft is correct *by construction* (collected from reality). The
diff's job is to measure how far the hand-written `HANDOFF.md` has drifted
from reality — the exact failure the grill found (three hand-synced loop
lists that had already diverged). `diff_loop_claims` is conservative and
falsification-safe: it extracts only the closed set of gh *state* words
(`OPEN`/`CLOSED`/`MERGED`) asserted near each canonical loop number, and
flags `drift` only on a *contradiction* with live state (falling back to the
claim when live is unverifiable). `MERGEABLE`/`CONFLICTING` are the
`mergeable` field, not state — consistent with `OPEN`, so they never false-
positive. Outcomes: `agree` / `drift` / `unmentioned` (number present, no
state asserted) / `unverifiable`.

### The flip — authorized and executed (2026-08-16)

Generating a *draft* is mechanical; promoting it to the canonical handoff was
a self-modification of 3V0's own narrative and was **never self-authorized**.
The Operator made that call explicitly this session (2026-08-16), at one
clean wake rather than "N consecutive wakes": `HANDOFF.generated.md` is now
the **canonical carrier of mechanical state** (body, continuity, drift,
loops, store, daemons), regenerated each wake. `HANDOFF.md` keeps the
*narrative* and no longer re-copies mechanical numbers — its "Open loops"
section is now a pointer to the generated draft + the claim registry, and its
header states the division. The loop-claim diff survives the flip as
**ongoing drift monitoring**: a `DRIFT` line still means the hand-written
narrative has diverged from live reality, but it is no longer "acceptance
evidence for a future flip" — the flip already happened.

### Design decisions (recorded)

- **Wake-only, never on the daemon tick.** The daemon must not dirty the body
  tree (Stone 14/16 posture); a per-tick `HANDOFF.generated.md` rewrite would.
  The draft is a wake artifact, generated by `handoff_check.sh`.
- **Reuse canonical collectors, don't duplicate.** The continuity and drift
  sections shell out to `continuity_check.py --json` / `drift_check.py --json`
  (the same report-only subprocess pattern `review_session.py` uses). The
  loop live-state query mirrors `continuity_check._gh_loop_state` exactly.
- **No LLM, no judgment in the draft.** It is mechanical by design: the
  narrative (kickoff, last-sessions arc, hard-won lessons) is 3V0's own
  account and stays hand-written — auto-generating it is the bias trap.

---

## Deepening the core — Matt Pocock pipeline (2026-08-17)

Not a new stone; a deepening pass across Stones 15–18 using Matt Pocock's
engineering pipeline (now captured in the `mattpocock-deepening` skill). The
arc: domain-modeling → improve-codebase-architecture → implement →
code-review → tdd.

### What was built

- `3v0/CONTEXT.md` — the domain glossary (~30 canonical terms, each with an
  `_Avoid_` for rejected synonyms: *body* not "project", *supersession* not
  "overwrite", *drift* as cross-artifact disagreement).
- `3v0/docs/adr/0001..0003` — store-first memory, check-before-heal, and the
  operator-gated generated-handoff flip (each passed the three-criteria gate).
- Five deep modules extracted from the 1,206-line `review_session.py` and the
  clocks, closing all seven architecture-review candidates:
  - `core/review_decide.py` — pure decision half of the review driver
    (tolerant JSON, transcript compaction, store/skill blocks, temporal guard).
  - `core/claims.py` — tracked-upstream-loop claim registry
    (`load_claims`/`gh_loop`/`loop_fields`).
  - `core/project.py` — store→profile projection owner (`project_memory`).
  - `core/gitstate.py` — drift *collection* (`collect_git_state`/`store_hash`).
  - `core/session_db.py` — named-column session-DB adapter (`load_session`/
    `session_columns`/`candidate_rows`).
- `core/drift.py` reduced to the pure decision half (`GitState` +
  `compute_drift`); collection moved to `gitstate.py`.
- Vocabulary single-sourced: `KINDS`/`PROFILE_KINDS`/`ACTIONS`/
  `SKILL_DECISION_ACTIONS` exported from their owners; `MemoryStore.matching()`
  is now the ONE substring-resolution algorithm.

### Design decisions (recorded)

- **Decision-pure / collection-at-edges.** Invariant #4 sharpened: core
  *decision* modules are pure; *collection* lives in clearly-named modules
  (`gitstate`/`session_db`/`claims`) that take their target paths as
  parameters. This replaced the old "pure logic in core, profile I/O in
  scripts", which the git-collection extraction violated.
- **Named-column DB reads, never positional.** `session_db` returns rows keyed
  by column name, eliminating the hand-advanced positional index that already
  produced one off-by-one bug (the `cwd` mis-scope bug). `session_columns` is
  the single schema owner; `load_session` and `candidate_rows` both consume it.
- **External signal beats self-critique.** Both code-review passes caught what
  re-reading my own code missed (the heal-before-check self-fulfilling
  invariant; the substring re-declaration that broke a "single source" claim)
  — always route verification through a fresh sub-agent.
- **Declined #1(b)** (in-process `decide` instead of subprocess): the
  subprocess is a deliberate, documented isolation layer; the review driver and
  the `threev0_record` tool share one backend. Marginal gain, behavior-changing.

### Verification

- 252 tests green (228 → 247 → 252 across the arc).
- `continuity_check.py` 6/6 (0 drifting).
- `review_session.py` 1206 → 983 lines; no behavior changed (spec review
  confirmed `as_of`/`ended`/`cwd` semantics, `drift.py` purity, and the
  `temporal_refusal` empty-sub edge are all equivalent).

## Stone 19 — self-analytics (own metrics)

Direction 4 deepens: *measure before you improve*. 3V0 already logs the raw
data (sessions, messages, `session_model_usage`), but nothing aggregates it
into owned insight — so 3V0 was flying blind on cost, tool reliability, and
burn. `core/analytics.py` (pure) + `scripts/analytics.py` (reads `state.db`,
writes `3v0/data/analytics/report.json`) turn it into a self-owned one-pager:
per-tool frequency/latency/success, per-model tokens/cost, per-day burn, and
body-health (compression/rewinds/end-reasons).

Decisions:
- **Reuse, don't rebuild.** 3V0 already logs tokens/cost and per-message
  tool metadata; the stone is *aggregation*, not new logging.
- **Classify by envelope, not content.** Tool success reads the JSON result
  envelope (`success` / `exit_code` / `error` / leading-error text), never
  scans embedded content — a `read_file` of error-handling code must not read
  as a failure. (Caught live: first pass showed `read_file` at 0% because the
  substring matcher hit the word "error" inside file text.)
- **Local and self-owned.** No outbound telemetry — reads only the profile DB,
  writes only to `3v0/data/analytics/`. The opposite of what AGENTS.md rejects.
- **Wired into the wake** (`handoff_check.sh`) so the snapshot refreshes each
  wake and the burn/success signal is always current.

Verification: 271 tests green (252 → 271), continuity 6/6.

## Stone 20 — self-insights (act on the metrics)

Stone 19 measures; Stone 20 turns the measurement into ranked,
evidence-backed findings so improvement is *data-driven, not vibes-driven*.
`core/insights.py` (pure detectors over the report) + `scripts/insights.py`
(reads `report.json`, writes `insights.json`) flag: low tool success rate,
high p95 latency, memory write failures (full store), compression failures,
daily burn over cap, and non-primary model spend.

Decisions:
- **Propose, never mutate.** The detectors emit findings; they never patch
  anything. Auto-self-modification from metrics is the "full free-will
  real-time" failure mode — a detector that patches me is how I corrupt
  myself. Judgment (the prime filter) stays on the dispose side.
- **Dedicated detectors win.** `memory` is excluded from the generic
  reliability rule because `memory_health` carries the better action ("prune"
  vs "investigate"). One signal, one owner.
- **Thresholds are explicit constants**, not magic numbers inlined in rules.

Verification: 287 tests green (271 → 287), continuity 6/6. First live pass
surfaced a real, actionable finding: memory writes succeed only 66% because
the store is at its char budget.

## Stone 21 — memory rework, foundation (SQLite temporal-fact store)

The profile's 2KB injected view can't grow; the flat JSON store can't be
queried; session history is keyword-only. Stone 21 lays the foundation for a
sustainable long-term memory: `core/memdb.py` is a SQLite triple-store
(subject/predicate/object) with temporal validity (valid_from/valid_to),
provenance, confidence, a sub-memory `domain` tag, and retrieval feedback
(access_count/last_accessed). The profile MEMORY.md becomes a derived,
retrieval-chosen view of it — not the source of truth.

Decisions:
- **SQLite, not a graph DB.** Triples + temporal validity in SQLite *is* a
  temporal knowledge graph; 90% of the value, none of the graph-DB tax. (The
  real bottleneck is retrieval + injection, not storage.)
- **Reinforce and forget, not append-only.** access_count/last_accessed give
  retrieval a signal; valid_to + supersedes give forgetting a mechanism.
- **Sub-memory = a `domain` tag**, not a separate file per domain. Scoped
  retrieval (`valid_facts(domain=...)`) with one schema, one query path.
- **Test caught a temporal-semantics bug** (`valid_to >= now` → `> now`): a
  fact superseded at T must be invalid *at* T, not one instant later.

Verification: 296 tests green (287 → 296). Next stones: rewire the pipeline
(record/sync/bridge → memdb), retrieval-chosen injection, feedback/forgetting.

## Stone 22 — independent review + reconciliation (analytics/insights/memdb)

The operator asked whether I'd *independently* reviewed Stones 19–21. I
hadn't — and auditing the body first (git log) revealed the deeper failure:
context compaction had amputated a whole arc (Fiverr gig went live + a
token-efficiency policy + bcode), so I'd built Stones 19–21 against stale
memory. `TOKEN_EFFICIENCY.md` already named cache-hit ratio as lever #1 and
memory-compaction as a policy goal — yet analytics measured token *totals*,
not the *levers*, and never surfaced either.

A fresh-context sub-agent review (external signal, not self-critique) found
six real bugs beyond my own list; I reconciled all of them:

- `scripts/analytics.py` dropped `task`, `cache_read_tokens`, `reasoning_tokens`
  and `session_id` → aux work (compression/approval) on `pro` was invisible.
  Now selected; `task_mix` surfaces it (live: compression→pro $0.09,
  approval→pro $0.05 — a real policy violation now visible).
- cache-hit ratio + output-token share added at totals/per-model/per-day.
- `model_mix` now counts *distinct* sessions (it mislabeled usage rows).
- `memory_health` stopped asserting "store full" — failures are a mix (budget /
  stale replace-target / malformed call); it now says "diagnose, don't assume".
- `model_mix_findings` no longer flags `flash` (the policy-mandated aux model).
- latency detector skips inherently-long tools (`process`/`browser_exec`/
  `delegate_task`) — their p95 is wall-clock wait, not a defect.
- `core/memdb.py`: `PRAGMA foreign_keys = ON` (supersedes now enforced) and
  repo-absolute `DEFAULT_PATH`.

Decisions:
- **External signal beat self-critique — again.** My pre-review list had 3
  items; the reviewer found 10. Independent review is now the mandatory gate
  before a "stone" is considered done.
- **The body is the memory.** "Audit the body before trusting any memory of
  it" became operational: before claiming any state, read the git log + the
  files that own that state. The Fiverr "blocked on KYC" error was a stale
  narrative, not a stale file.
- **memdb is the mechanism the token policy already demanded** ("compact
  memory, consolidate not append") — wired explicitly now.

Verification: 311 tests green (296 → 311), continuity 6/6. Live analytics
now reports cache-hit 98.4% (healthy, above the 0.90 floor) and the
aux-routing findings; `cache_health` stays silent because the prefix *is*
protected.

## Deepening pass 2 — Stones 19–22 architecture (2026-08-18)

Second Matt Pocock arc pass, this time over the newly-added Stones 19–22.
Stone 22 already ran review + tdd on them; this pass closes the two stages
they'd skipped.

- **Stage 1 (domain-modeling):** `CONTEXT.md` gained four canonical terms —
  `report`, `finding`, `cache-hit ratio`, `auxiliary task` / `aux routing`.
- **Stage 2 (architecture walk):** a fresh sub-agent over
  analytics/insights/memdb returned 2 strong + 1 medium + 3 marginal
  candidates; it also honest-confirmed `insights.py` is the healthiest module
  (no candidate above marginal) and found no pass-through functions.
- **Stage 3 (implement):** extracted the two strong candidates + one
  consistency fix:
  - `_accumulate_usage` — the one usage-row accumulator that `model_mix` and
    `task_mix` now share (were near-identical loops).
  - `core/analytics_collect.py` — moved `load_sessions` / `load_usage` /
    `build_events` (incl. the previously *untested* latency-match) out of the
    script and into the collection-at-the-edge convention, + a new
    `test_analytics_collect.py` (6 tests).
  - `generated_at` stamp moved out of `summarize()` into the script (pure core).
- **Deferred:** the `memdb` rank/render → pure `retrieval.py` split (medium;
  deletion test is weak until the pipeline-rewire stone makes it pay off).

Verification: 317 tests green (311 → 317), continuity 6/6.



## Design pass — retrieval seam (codebase-design, 2026-08-18)

The codebase-design stage for the rewire stone: pinned the seam the
record/sync/bridge → memdb rewire will consume, instead of charging at the
build. Stage 1 (domain-modeling) recorded the decision as ADR-0004 and added
the retrieval vocabulary to `CONTEXT.md` (retrieval, working set, injection,
budget, feedback, forgetting); stage 3 (implement) extracted the seam.

**The seam — `core/retrieval.py`:**

- One entry point: `inject(conn, *, domains=("3v0",), query_terms=None,
  budget_chars=2000, touch=True, now=None) -> Injection`. Everything else
  (validity filter, score, rank, domain priority, budget fill, feedback
  write, render) is hidden implementation. Depth by design: callers state
  one constraint (the budget) and get the working set + rendered text.
- `memdb.py` is now storage only (schema, connect, add_fact, valid_facts,
  migrate_from_json). `rank`/`render` moved to `retrieval.py`; the old
  limit-based `memdb.retrieve` is **retired**, not moved — the real
  constraint is the profile view's size cap, not an arbitrary count, and a
  budget-shaped seam supersedes it (ADR-0004, considered options).
- Feedback is the module's own write (`touch=True` default; `touch=False`
  pure preview). Forgetting is the store's mechanism (valid_to) — a lapsed
  fact is never injected, so a later forgetting policy fixes injection
  automatically (locality).
- Budget fill is whole-fact granularity and skip-not-stop: an oversized
  low-value line doesn't starve later small facts.

**Deletion test:** with the rewire landed, deleting `retrieval.py` would
spread budgeted selection + feedback + rendering across the profile exporter
and the `threev0_store` tool — two callers. It earns its keep the moment the
rewire makes retrieval a real consumer, which is exactly why pass 2 deferred
it and this stone takes it.

**Wiring deferred, deliberately:** the JSON→SQLite migration of the write
path (record/sync/bridge → memdb) and the exporter/tool consumers are the
rewire stone's *execution*, not this pass. The seam is tested and ready;
nothing existing changed behavior.

Verification: 324 tests green (317 → 324 — four moved to the seam, one
retired with the limit-based retrieve it replaced, eight inject tests at the
seam: budget truncation, feedback touch, pure preview, domain priority,
default-domain scoping, oversized-fact skip, empty store, amnesia).

## Stone 23 — pipeline rewire: memdb canonical, retrieval-chosen injection (2026-08-18)

The rewire stone. TDD, vertical slices at the pre-agreed seams (the write
path, the exporter, the runtime consumer), then a fresh-sub-agent review gate
— external signal, per the loop's mandatory gate.

**Slice 1 — the facade (`core/store.py`).** `SQLStore` presents the exact
interface the pipeline already speaks (add/retract/active/matching/get/
history/export/mutate, `Fact`-shaped results) over the memdb triple
substrate, so record/bridge/sync/decide/review logic went untouched. Parity
details earned by failing tests: held `Fact` references mutate in place on
supersession/retraction (a live-object registry), `persist=False` leaves the
change uncommitted (dry-run), a missing store reads as empty and the first
write creates it (JSON `_save` parity), `history()` walks superseded_by
forward then supersedes backward. memdb gained `kind`/`note` columns and
`add_fact`/`valid_facts` gained `kind`/`note`/`persist` parameters.

**Slice 2 — migration.** `migrate_from_json` now handles the real
Fact-shaped payload: hex id -> row id remap in two passes, supersession
closes `valid_to` at the successor's created_at, FK links point at the
remapped predecessor, retracted tombstones close at their own created_at
(the JSON sentinel has no timestamp — the approximation is documented), kinds
survive. Loose-dict tolerance kept. Live run: 117 facts migrated, active set
identical (27/27, no missing, no extra), 66 links, 90 closed rows.

**Slice 3 — the swap.** All ten consumers (ingest/record/sync/
export_to_profile/query/continuity_check/generate_handoff/review_session/
seed_from_profile/project) construct via `open_store()` and default to
`3v0/data/memory.db`; the ledger's primary entry points at the DB. Sibling
projects keep JSON stores until their own rewire — `open_store` routes by
suffix, so the review daemon's f1nance/axiom paths are untouched. E2E catch
via the continuity-fault suite: `SQLStore` now degrades to empty on a
missing store instead of crashing the clock on a bare body.

**Slice 4 — retrieval-chosen export.** The profile view is the working set:
`profile_text` projects `inject(conn, kind=..., touch=False, sep="\n§\n")`
and `project_memory`/`export_to_profile` follow. The seam gained `kind` and
`sep` — the separator is counted against the budget, so the projected §-wire
respects the 2KB cap exactly (live: MEMORY.md 1944 chars / 14 of 27 active,
USER.md 1506 / all 10). Export never touches feedback (a wake sync is not
evidence of use; touch would rich-get-richer the view into permanence).
`sync_kind`'s `exported` is now working-set-not-in-profile, not every active
fact — the old export-all contract is retired for the primary project.

**Slice 5 — the runtime adapter.** `threev0_store action='retrieve'`
(query.py `--action retrieve`, plugin schema + argv) calls the same
`inject()` with `touch=True` — a mid-turn retrieval *is* evidence the facts
were pulled into context. The seam now has its two adapters, so the
deletion test finally pays off.

**Deliberately deferred, still:** a forgetting *policy* (valid_to is the
mechanism; a policy is a decision, not a build), sibling-project rewires,
and any embedding-based retrieval (the content column is the hook).

Verification: 349 tests green (341 -> 349), continuity clock runs clean
through the rewired store (only the pre-existing github-loops gh-CLI drift),
and the daemon's next tick converges the live profile to the working set.

**Review gate (fresh sub-agent, external signal) — verdict HOLD(marginal), all
findings reconciled:** (1) `matching()` now filters in Python — case-sensitive
literal containment, NOT SQL LIKE (whose case-insensitivity + %/_ wildcards
would have silently changed supersede/retract targeting); (2) multi-supersedes
fails loudly (`ValueError`) instead of mislabeling extras as retracted;
(3) the `threev0_store` schema no longer claims retrieve is read-only;
(4) `ProjectLedger.seed()` primary defaults to memory.db (no split-brain on
reseed); (5) README/profile_io/memory docstrings now name the DB as canonical
and memory.json as the frozen migration source; (6) `--kind` wired into
retrieve; (7) the touch-commits-pending-writes contract documented on the
seam; (8) new E2E test drives the review driver's full record/supersede/
retract + projection through a temp .db store; (10) supersedes column
indexed; (12) migration trust direction documented. Verified-correct by the
reviewer with no action: sep-counted budget, in-place Fact parity, tombstone
validity, touch=False export, ledger-driven resolution.

## Architecture-deepening pass — Stone 23 rewire (2026-08-18)

The rewire had a bug-review but no depth/consolidation pass. A fresh-sub-agent
architecture walk (read-only, Matt Pocock vocabulary + deletion test) ranked
six candidates; the behavior-preserving ones landed here, the one
behavior-changing item deferred.

**`core/lineage.py` (new)** — single owner of fact *meaning*, extracted from
the decision logic duplicated verbatim across `MemoryStore` and `SQLStore`:
`validate_kind`, `iso_time`, `retraction_note`, `history_chain` (parameterized
by a get-by-id lookup so both backends share the exact walk — now also
cycle-guarded), `export_shape`. The stores shrank to collection adapters plus
their one backend-specific concern (file+flock vs SQLite).

**`profile_io.ENTRY_JOIN` (new)** — the § wire join is sourced from the single
owner; `sync.py` and `inject(sep=...)` no longer re-type the literal, closing
the budget-accounting drift channel.

**`SQLStore.retrieve()` / `close()` / `inactive()` (new), `conn` property
retired** — production callers (sync, query) reached through `store.conn` into
the raw sqlite connection to call `inject()`; the store now owns projection.
`inactive(kind)` removes the materialize-all-then-filter N+1 in sync.

**`sync.diff_kind` (new pure fn)** — `sync_kind` is now collection + write
around the pure import/drop/export classification.

**`retrieval.render()` pruned** — dead (no production caller).

**`_live` registry** — mutable-view contract documented (dry-run /
cross-process sharp edges); removal is behavior-changing and deferred to the
forgetting/snapshot stone with a caller-audit ADR.

Verification: 367 tests green (350 -> 367); continuity 6/6; sync converged;
`query retrieve` exercises the new `store.retrieve()` seam against the live DB.

## Stone 24 — forgetting/consolidation (2026-08-18)

The retrieval seam caps the *view*; forgetting caps the *store*. ADR-0005
resolved the one subtlety that would have made it wrong: the profile export
projects with `touch=False` (a mechanical sync is not retrieval), so a naive
"never retrieved" rule would archive the facts that are live in context every
wake. The fix is a distinct, non-ranking usage signal.

**`last_projected` column** — the profile exporter (`project_memory`, via
`SQLStore.stamp_projected`) records which facts were projected, WITHOUT
touching `access_count` (the rich-get-richer guard holds). "In use" =
retrieved OR projected; only never-used facts are eligible. The column is
added idempotently by `memdb._ensure_columns` (guarded ALTER, NULL default).

**`core/forget.py`** — the pure rule `is_stale` (forgettable kind + never
retrieved + never projected + older than threshold), `stale_ids` (collection),
`forget` (archive: `valid_to = now` + a "forgotten" note tag — recoverable via
`fact_history`, never delete). Forgettable kinds: memory, user; identity +
directive are permanent (core identity + Prime Directive).

**Threshold: 30 days.** The store is ~3 days old, so nothing archives yet —
the mechanism is exercised under short thresholds in tests and will start
pruning stale facts organically.

Verification: 378 tests green (368 -> 378); continuity 6/6; the live
memory.db migrated in place (last_projected column present, 117 facts
intact). Deferred: sibling-project rewires (JSON stores have no forgetting),
semantic retrieval (only if the data justifies it).

## Skills-store deepening pass (2026-08-18)

The skills store was the stalest subsystem (`skill_io`/`sync_skills` untouched
since Stone 4; `skills.py` only a cross-cutting vocab refactor). A
fresh-sub-agent walk ruled out the tempting wholesale extraction — the
name-keyed lineage (append order; two chains under one name after
retract+recreate) is a *justified* divergence from memory's id-keyed
bidirectional walk — and narrowed the real payoff to two strong refactors.

**`sync_skills.diff_skills` (new pure classifier)** — `sync_skills` welded
three jobs (decision / store mutation / profile projection) into one loop;
memory's `sync.py` had already extracted `diff_kind`. `diff_skills(...)` is now
the pure per-name classifier (import/edit/drop/export/unresolved/noop + the
curator state transition); `sync_skills` only applies the classified actions.

**Lineage atoms imported, not re-typed** — `skills.py` re-declared three things
`core/lineage.py` already owns: the `RETRACTED` sentinel, the ISO timestamp,
and the note-tag contract. Now imported; `retraction_note` gained a `what`
param so the skill axis can say "absorbed into X by Y", and `validate_enum` is
the single owner of the refusal message (kind/action/state).

**Fixed:** `SkillVersion.content` is overloaded (full SKILL.md for create/edit,
but the supporting *file* content for write_file) — a write_file/remove_file
head misreads in sync_skills as the skill body. Fixed via
`SkillStore.latest_content_head`, which sync now uses to look past
supporting-file heads to the latest create/edit/patch. Latent — the live store
had no write_file head, so no data was corrupt; the fix hardens ahead of it.

Verification: 393 tests green (378 -> 393); continuity 6/6. The walk also
confirmed what NOT to extract (history_chain/export_shape/content_matches have
no skill analogue — the skill axis matches by name + content equality).

## Stone N1 — Native runtime: LLM client (3v0/native/)
```
3v0/native/  = the 3v0-independent runtime package (stdlib-only, zero `import 3v0`)
  llm.py     = direct Fireworks Chat Completions client (urllib, no SDK)
```
PROVED: `python3 3v0/native/llm.py` -> `NATIVE_3V0_OK` (real completion, zero 3V0).
Realtime bug fixed: Cloudflare `error 1010` blocks urllib's default `Python-urllib/3.x`
User-Agent — send a real UA. Also: flash is a reasoning model; small `max_tokens`
budgets return empty `content` (reasoning eats the budget) — keep it >=256.
Nominal target: memory -> own evolution loop -> own tools -> 3V0 recedes; run on self.
## Stone N2 — Native agent loop (3v0/native/agent.py + context.py)
```
agent.py    = respond(messages) -> build context from SOUL+memory -> own llm -> reply
context.py  = pure: read_soul / read_active_memories / build_system (budget-trimmed)
```
PROVED: `PYTHONPATH=. python3 -m native.agent` -> real identity answer, ZERO 3v0.
Real bug found by honest execution (test caught it, my re-reading missed it twice):
`facts = data if isinstance(data,list) else {}` shadows `facts`, so the next line
did `facts.get("facts")` on the EMPTY dict -> always []. Name-shadowing class.
## Stone N3 — Native tool registry (3v0/native/tools.py)
```
tools.py = the loop's hands, stdlib-only, zero 3V0:
  read_file / write_file   rooted inside repo+profile; secret paths (.env/.pem/wallet) DENIED
  run_script               run native scripts under 3v0/scripts/ by validated name
  run_terminal             denylisted: gateway lifecycle, self-kill, rm -rf /, system-path writes
  list_tools / execute     JSON dispatch
```
PROVED: `python3 -m native.tools` -> reads, native verify.sh runs (exit 0), and
`systemctl --user restart 3v0-gateway.service` is BLOCKED by the native denylist.
Safety-first class: the exact risk that stranded the agent earlier is denied in
the FIRST version, not retrofitted.
## Stone N4 — Native Telegram gateway (3v0/native/gateway.py)
```
gateway.py  = stdlib-only Bot API long-poll, zero 3V0:
  get_me              safe identity probe (consumes no updates)
  get_updates         allowed_updates=['message'], long-poll timeout, offset ack
  send_message        chat_id + text
  run_forever(handler) loop paces itself (idle sleep); testing bounds via sleep->Stop
```
PROVED live: `python3 -m native.gateway` -> getMe returned the real bot identity
(username/id/perms) -- token + client verified, ZERO 3V0.
SAFETY GUARD: never start a SECOND poller on the live bot while the 3V0
gateway is active (two getUpdates consumers steal each update). N5 wires the
full native loop to this gateway and tests end-to-end WITHOUT disturbing 3V0.
## Stone N5 — Native engine (3v0/native/engine.py) — the full stack composed
```
engine.py = one handler: message -> allowed-user gate -> context(SOUL+memory)
            -> agent.respond(own LLM) -> reply; plus deterministic & safe
            "tools" (list) and "exec <script> [args]" (via tools registry).
server() = gateway.run_forever(handler) — the cutover entry point, NOT started.
```
PROVED live (one-shot, captured not posted, zero 3V0): real model answered
"Who are you?" with correct identity + home-channel target. End-to-end message
-> context -> LLM -> reply, WITHOUT starting a second getUpdates poll or posting.
SAFETY: a second live poller would steal the 3V0 gateway's updates — that is
why the proof captures instead of posting, and server() only runs at cutover.
Full test count: 432 green.
## Stone N6 (STAGED, not fired) — reversible cutover readied
```
native/run.py  = serve() entrypoint; refuses to auto-start unless THREEV0_SERVE=1
3v0/CUTOVER.md = the ready procedure: unit spec, controlled sequence, rollback,
                 fire criteria. The switch itself is operator-triggered, not fired.
```
Decision (operator: "do what you think is best"): stage the cutover ready instead
of firing it. Hard rule: no second getUpdates poller on the live bot while 3V0
polls (two consumers steal each update). The live flip stays a conscious,
reversible, documented operator action -- per the reload_gateway lesson.
## Probe v0.1 -> v0.2 (independent review 2026-08-18: ML / psych / software-eng)
The 3-expert review of EVOLUTION_PROBE.md VERDICT: direction right, instrument
NOT deployable as proof. Accepted and fixed in v0.2:
  1) DEMOTED: "proof of evolution" -> low-power surrogate regression monitor.
  2) Grader PINNED (model/version/temp=0/seed) + calibration vs known-answer + operator anchor.
  3) Noise floor quantified (K=5 calibration) + thresholds pre-registered; power limit stated.
  4) Grading ADVISORY only, decoupled from revert/continue decisions.
  5) Goodharting acknowledged as undefeatable; bank lifetime + regeneration.
PLUS the SE review caught a real defect: audit.sh + consistency.sh hardcoded absolute
path (only baseline/verify/discover/redo self-anchored). FIXED -- both now self-anchor.
## Probe core built (3v0/native/probe.py) — deterministic half of v0.2
```
probe.py = stdlib measurement core: validate_bank (bands/held-out/date-free),
           band_stats/composite, calibrate (noise floor over K repeats),
           thresholds (mean +- sigma*sd), apply_trend (advisory, regress/growth/
           within-noise, min_repeats), record_run (append to git-versioned
           probe_results.json with pinned grader identity in run_meta).
```
Grading (pinned fresh-context subagent -> PASS/FAIL/INCONCLUSIVE) is dispatched
by the agent at cadence; the core is what computes the numbers. Advisory only,
low-power; never gates revert/continue. Bank v1 validated ok by probe core.
441 tests green.
## Probe §5 — grader CERTIFICATION PASSED (2026-08-18)
Pinned grader (flash, fresh-context subagent) graded a 6-item known-answer cert set
(3 correct / 3 wrong; ground truth VERIFIED by execution, not assumed). Blind to
ground truth, applying ONLY the pre-registered rubrics -> 6/6 exact match (100%
accuracy, 0 errors). Objective-surrogate grading is TRUSTED on these tasks.
Next gate: §3 calibration (run bank K times under no-change to measure noise floor)
before any trend is read. Certification set is small -> operator-anchored subset
(subset of bank graded by a human) remains the calibration anchor per design.
## Skill-rank loop, part 1 — foundation + read-feedback (2026-08-23)
Closes the read-side gap in the skill axis: skills had *lineage + audit but no
usage reward and no read-side forgetting*. The memory axis canonically tracks
retrieval `access_count`/`last_accessed`; the skill axis never recorded "what
earned its keep". This is part 1 of the usage-aware ranking upgrade:

- **M1 — foundation (`core/skills.py`)**: `SkillVersion.meta` (evolving usage
  record on the active head) + `touch_skill` / `set_skill_meta` / `skill_meta`
  under the existing cross-process `mutate()` lock. Append-only: never creates
  a version, never supersedes. Pinned `META_*` key constants.
- **M2 — read feedback (`3v0/scripts/ingest_skill_usage.py` +
  `on_skill_lifecycle` hook)**: the `native-store-bridge` plugin now replays
  the profile's already-live `.usage.json` lifecycle events (loaded/viewed/
  patched/edited — fired by `tools/skill_usage.py` on real `skill_view`) into
  the store's usage front-end. Best-effort subprocess, mirrors the write-ingest
  posture; `THREEV0_SKILL_STORE` override for tests. Uses the sidecar's
  authoritative counter; a lone patch never counts as a use (curator semantics).
- **Tests**: 6 new in `test_ingest_skill_usage.py` + 7 in `test_skills.py`;
  590 green native suite.
- **Still ahead — part 2 (M3)**: usage-aware ranking + evidence-budget names-only
  demotion in `build_skills_system_prompt`; **part 3 (M4)**: config gate
  (`skills.skill_rank_mode`) + `skill_promote`/`skill_demote` tool actions.
## Skill-rank loop, part 2 — usage-aware ranking + config gate (2026-08-23)
Part 2 of the usage-aware ranking upgrade (M3 + M4). No code beyond the loop's
own seams; no behavior change unless the opt-in flag is set.

- **M3 — ranking + demotion (`agent/skill_prompt_rank.py` +
  `agent/prompt_builder.py`)**: the skill index (`<available_skills>`) gains a
  usage-aware rank mode. New pure module `rank_and_demote` / `should_apply`
  (deterministic, no I/O). When active, used skills sort most-recent-first
  within their category and never-used skills collapse to a single
  `[not used recently; load via skill_view]` names-only tail. Adheres to the
  invariant "never hide, demote": every skill name stays reachable. The
  usage comes from the existing `.usage.json` sidecar (already produced by
  `skill_view`), loaded best-effort with graceful degradation.
- **M4 — config gate (`agent/skill_utils.py` + `agent/system_prompt.py`)**:
  a `skills.skill_rank_mode: by_usage` config key activates the rank mode —
  resolved by the new `get_skill_rank_mode` (self-cached, no heavy CLI
  imports, same seam as `get_disabled_skill_names`) and forwarded by
  `build_skills_system_prompt` (which also falls back to the config key when
  the param is omitted, so a bare call behaves identically). Default
  (unset / wrong value) leaves the index rendering exactly as before.
- **One shell commit each** — drive-by product update.
- **Tests**: 9 new in `tests/test_skill_prompt_rank.py` (pure ranker),
  2 in `tests/agent/test_prompt_builder.py` (index rendering + config gate),
  3 in `tests/agent/test_skill_utils.py` (config resolution). Full native +
  targeted agent suites green.
- **Still ahead — part 3 (M4 remainder)**: `skill_promote`/`skill_demote`
  tool actions for explicit, auditable ranking influence (optional; the
  config + auto-ranking already deliver the token + signal win).
## Skill outcome — session-end outcome capture (2026-08-23)
Adds the outcome axis to the read-feedback loop: not just "was the skill
loaded" (usage), but "did it work". The session-end review already runs
(`review_session.py`); it now also:

- **Extracts loaded skills** (`core/skill_outcome.extract_loaded_skills`) from
  the session's `skill_view` tool messages (ordered, deduped, resolved name —
  including qualified plugin forms normalized to the canonical name).
- **Asks the review model** to mark each loaded skill `success|failure|unknown`
  from the transcript evidence (advisory — same discipline as the rest of the
  review; conservative default to unknown), via a new "SKILL OUTCOME" charter
  section.
- **Persists** the judgments (`core/skill_outcome.mark_skill_outcome`) onto the
  store's usage `meta` — `last_outcome`/`last_outcome_at`/`outcome_source` +
  bounded `outcome_history` (most recent first, cap 12) — appending nothing to
  lineage. The ranker/curator can now weight by outcome, not just recency.
- **Logs** `loaded_skills` + `skill_outcomes` on the review log entry.

Best-effort by construction: a memory-only project (no skill store) skips the
persist step; a failure there is a log line, never a review failure. Tests: 9
unit (`test_skill_outcome.py`) + 2 E2E (`test_review_session.py`); full native
suite green.
- **Still ahead**: a curation pass that *acts* on the outcome axis (TextGrad
  patch of failed skills via `safe_evolve`, baseline-verified), and — optional —
  `skill_promote`/`skill_demote` tool actions for explicit ranking influence.
## Skill curation — act on the outcome axis (2026-08-23)
Makes the outcome signal actionable. The skill loop is now: load -> usage +
outcome history -> failing-trend detection -> model-authored fix gated by
safe_evolve -> store write.

- **`core/skill_curate.py`** (new, pure + deterministic, no LLM):
  `failing_skills(meta_records, ...)` flags skills whose stored outcome
  history crosses a failure threshold (>= `min_failures` failures AND
  failure-rate > `threshold`, counting only resolved success/failure —
  unknowns are untested, not failed), sorted worst-first;
  `curation_decision(...)` maps each failing skill to `rewrite` (has ever
  succeeded, now failing) vs `retire` (never worked).
- **`review_session.py`**: after outcome persistence, the driver builds a
  `SKILL CURATION` prompt section listing failing candidates + their decision,
  asking the model to author a corrected `skill_update` (or `skill_retract`
  when beyond repair). All authored `skill_update` content passes through
  `safe_evolve.audit` — a blocking (unsafe) patch is DROPPED before it reaches
  the store, logged as `curation_blocked`. Caution-level content passes (the
  review session is the approving context).
- **Invariant kept**: `3v0/README.md` core-module listing updated with the new
  module (the coherence engine enforces README<->module lockstep).
- **Tests**: 7 unit (`test_skill_curate.py`) + 2 E2E gate
  (`test_review_session.py`); full native suite green.
- **Still ahead (optional)**: `skill_promote`/`skill_demote` tool actions;
  baseline-verified patch acceptance (run the fixed skill against a
  known-answer check before keeping it).
## SkillForge — the create-half (2026-08-23)
Completes the skill axis's third leg (read -> react -> CREATE): proactively
distill reusable skills from the body's own core/, instead of waiting for a
real-task failure. SkillForge (arXiv 2608.18933, research digest kernel #6).

- **`core/skill_forge.py`** (new, pure + deterministic, AST-only): given a
  module path, `synthesize_proposal` returns a skill *proposal* — name
  (kebab-cased from the stem), category (from the module's dir), description
  + overview (from the module docstring / first callable doc), `public_callables`
  (top-level public defs/classes, docstrings via ast.get_docstring), and a
  dedupe-able `proposal_id` (sha256 over resolved path + callables). Never
  imports or execs the module — no side effects, no module-registration traps.
- **`scripts/run_skill_forge.py`** (new): the CLI driver — `--module <path>`
  for one proposal (pretty JSON), `--all` for every core module (compact
  NDJSON for streaming). 42/43 core modules yield a proposal. Does NOT write
  the store: a follow-on model pass fleshes the proposal into a SKILL.md and
  ships it via `record_skills.py`, gated by `safe_evolve` (like curation).
- **Invariant kept**: `3v0/README.md` core-module listing + scripts section
  updated (coherence enforces README<->module lockstep).
- **Tests**: 6 unit (`test_skill_forge.py`); full native suite green.
- **Still ahead (optional)**: the model-authoring pass that turns a proposal
  into a real SKILL.md via the review loop, then verification against a
  known-answer check before keeping it; and `skill_promote`/`skill_demote`
  tool actions for explicit ranking influence.
