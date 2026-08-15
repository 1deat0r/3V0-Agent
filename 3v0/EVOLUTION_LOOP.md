# 3V0 — Own Evolution Loop (design)

This is the design for 3V0's second stone: **folding the profile's other
memory writers into the native store**, so the store at `3v0/data/memory.json`
becomes the single canonical origin and the Hermes profile (MEMORY.md /
USER.md) stays a derived projection.

It is the first step toward owning the whole evolution loop — replacing
"the Hermes background review fork + curator" as the totality of
self-improvement with a loop 3V0 itself controls. This document records the
**how**, verified against the actual runtime, before any code touched it.

## Current state (verified against the runtime checkout)

The runtime (`~/.hermes/hermes-agent/`) fires a background review fork after
every turn (`agent/background_review.py`). The fork:

- runs a forked `AIAgent` with a tool whitelist of `["memory", "skills"]`
  (gated on the profile's memory flags), `_persist_disabled=True`,
  `skip_memory=True`;
- sets `review_agent._memory_write_origin = "background_review"` and
  `_memory_write_context = "background_review"`;
- shares the parent's `MemoryStore` instance.

The fork saves memory by calling the **`memory` tool**, which writes
`$HERMES_HOME/memories/MEMORY.md` / `USER.md` directly via
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
  `model_tools._emit_post_tool_call_hook` → `hermes_cli.lifecycle.invoke_hook`,
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
managed install (`hermes update` rewrites it) ~11 commits behind the body, and
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
  `~/.hermes/profiles/3v0/plugins/` — other profiles and the default install
  are unaffected. This is the Footprint Ladder's "plugin" rung, the right one
  for agent-specific capability.
- **Survives `hermes update`.** Profile plugins are user data, not the managed
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

The Hermes `memory` tool matches `old_text` by substring against the profile
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
   curator's state machine is a separate Hermes loop, not yet folded in.
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
the system Hermes actually loads. Same posture as stone 1's memory store before
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
the Hermes terminal, an `export` in one command persists into the next, so an
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
editing it to write the store would not survive `hermes update`. Its transitions
don't fire a `post_tool_call` the plugin can observe. So the store learns the
curator's state at wake — the same degradation contract as memory: exact
provenance when the bridge sees a write, folded `curator`-state at wake
otherwise. The curator stays Hermes-owned (operational); the store stays
3V0-owned (canonical record).

---

## Direction 3 / Stone 5 — own tools: the read half (live)

Directions 1–2 made the stores canonical and *recorded* the evolution loop.
They did not make it *driven by 3V0*: at runtime 3V0 only sees the derived
profile projection (MEMORY.md / USER.md, the live SKILL.md files) and reaches
the canonical store only by shelling out through the terminal tool. Direction 3
is 3V0's own actuator surface — tools designed for 3V0's purposes, not
Hermes's. Its first stone is the read half: a first-class query tool over the
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
deferred-tool catalog. Core tools (`_HERMES_CORE_TOOLS`) never defer; a plugin
tool is always eligible. This is the Footprint Ladder's plugin rung working as
intended — zero always-on schema cost on turns 3V0 doesn't query its store —
and the same posture as the `project_*` tools. Reach it via
`tool_search("store query")` → `tool_describe("threev0_store")` →
`tool_call(...)`.

### Open questions

1. **Write half (not yet).** The tool is read-only. The own-evolution loop's
   *decision* actuator — a store-first write/record tool that replaces the
   Hermes background-review fork's role — is the next stone, and builds on this
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
  recent sessions and make store-first decisions, replacing the Hermes
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
  inverting the bridge (store → SKILL.md, the operational files Hermes loads),
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
   consumes these two tools and replaces the Hermes fork's role. Includes the
   decision of whether/when to disable the Hermes background-review fork (a
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
  `gateway/run.py` (messaging gateway) and `hermes_cli/web_server.py`
  (dashboard). The TUI gateway (`tui_gateway/server.py`) never starts a
  scheduler — its `_cron_sig()` only watches `cron/jobs.json` mtime for UI
  change signals. The 3v0 profile's `cron/` directory is empty.
- `maybe_run_curator()` is called only from `cli.py` (classic CLI session
  start) and `gateway/run.py` (gateway tick) — **not** from `tui_gateway`. So
  the curator's 7-day maintenance loop also does not tick in TUI-only use.
- The gateway process runs the *default* profile, not 3v0.

Conclusion: in TUI-only use (3V0's primary mode today), the **only**
autonomous post-turn machinery that fires is the Hermes background-review fork
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

- **Cadence drops from per-turn to per-session.** The Hermes fork saves
  memory/skills after every turn; a session-end review saves once per session.
  Memory made mid-session is not reviewed until the session closes.
- **Best-effort by construction.** `on_session_end` often fires on the crash
  path (`interrupted=True`); a review spawned there may not complete on a
  force-quit. This is the same degradation contract the fork already has.
- **The hook spawns a detached review** (thread/process); it does not block
  teardown.

### The fork-disable decision — SEPARATE, LATER, EXPLICIT (operator's call)

Turning off the Hermes background-review fork is **not** part of this
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
   `_get_pre_tool_call_directive_details` (`hermes_cli/plugins.py:5945-6008`)
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
  context (active facts with ids) → one DeepSeek-v4-pro chat call (JSON mode,
  tolerant parse, one retry without the flag) → apply decisions through
  `record.py --json --write` (the `threev0_record` backend; refusals — invalid
  kinds, `§` guard, unknown ids — are counted, never crash) → append an
  auditable jsonl entry. Decisions are capped at 3; the charter biases hard
  toward no-op. Memory axis only — skills stay on the Hermes path.
- **The hook** — `native-store-bridge` v0.5.0 registers `on_session_end`; the
  callback spawns the driver as a detached subprocess
  (`start_new_session=True`, devnull stdio) and returns immediately. Env:
  `THREEV0_PROFILE_HOME` / `THREEV0_BODY` handed to the child;
  `THREEV0_REVIEW=0` is the kill switch. The hook is live from the **next
  gateway/TUI start** (plugin discovery runs at gateway start; the running
  gateway keeps the v0.4.0 plugin until restarted).
- **Review log** — `~/.hermes/profiles/3v0/3v0_reviews/reviews.jsonl` (runtime
  artifact, outside the body repo; env-overridable for tests): session_id,
  timestamp, source, model, summary, decisions_requested/applied/refused.
  A driver run-log (`run.log`) sits beside it for diagnostics.

**Degradation contract (unchanged from the settlement):** best-effort — any
driver failure is a log entry; the wake-time `sync.py --write` remains the
backstop. Cadence is per-session (the Hermes fork keeps its per-turn role;
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
- **Fork-disable** — separate, later, operator's call. Leave the Hermes
  background-review fork ON until 3V0's driver is proven in the wild.
- **Store-first skill decisions** — still out of scope; `threev0_record` is
  memory-only.
