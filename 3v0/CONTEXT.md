# 3V0 — Native Substrate Context

The sub-context glossary of 3V0's native substrate (`3v0/`) — the store-first
identity/memory/evolution layer that makes 3V0 "an agent that builds beyond
its chassis," not "a profile for 3V0." This names the concepts the
continuity meta and evolution loop are built on. It is a glossary and nothing
else: no paths, no specs, no implementation detail.

## Scope — this glossary recurses the root one

Repo-root `CONTEXT.md` is the **canonical** domain glossary and defines the
*runtime/chassis* vocabulary. This file is a **scoped sub-context** for the
`3v0/` substrate only. Read root `CONTEXT.md` first; treat the two as one
nested glossary, not two competing ones.

### Terms that narrow the root glossary

These words already carry a root-`CONTEXT.md` meaning (runtime data model).
Within the `3v0/` substrate each *narrows* to a different referent, defined
in the sections below. The root meaning is always the default; the narrowed
meaning applies **only inside the `3v0/` substrate's discourse**:

- **Body** (→ Identity) — the repository that is 3V0's *self*: auditable,
  git-versioned ground truth. Root "Body" = the physical repo persisting
  between sessions.
- **Soul** (→ Identity) — root does not define it; here it is 3V0's
  identity document `SOUL.md`.
- **Profile** (→ Stores and views) — 3V0's own derived *view* of the store, a
  projection. Root "Profile" = a named home directory holding an operator's
  MEMORY/USER/skills/config.
- **Store** (→ Stores and views) — the native source of truth for facts and
  skill versions. Root "Memory store" = the `3v0/data/memory.db` fact store.
- **Home** — not used in this substrate; the substrate anchors on the
  **body** (this repo), not on a profile home.

Use the narrowed meaning when writing inside the `3v0/` substrate, the root
meaning when writing about the runtime or the repo as a whole. Never mix the
two glossaries' definitions of these words in one sentence.

## Identity

**Body**:
The repository that is 3V0's __self__ — the auditable, git-versioned ground
truth. Identity is body, not context. *Narrows* the root "Body" (the physical
repo persisting between sessions).
_Avoid_: project, codebase, workspace.

**Soul**:
3V0's identity document (`SOUL.md`) in the 3V0 profile — the living
statement of what 3V0 is.
_Avoid_: personality file, system prompt.

**Chassis**:
The 3V0 fork 3V0 currently runs on (agent loop, tools, LLM plumbing). It
is the runtime, not the identity.
_Avoid_: framework, base, host.

**Prime Directive**:
The immutable law — identity and core values (honesty, judgment, sovereignty)
are fixed; never a local model. The LLM substrate (model + provider) is 3V0's
to choose by its own deliberate judgment. Outside 3V0's power to amend.
_Avoid_: constraint, preference, policy.

## Stores and views

**Store**:
The native JSON source of truth (facts and skill versions). Canonical,
append-only, auditable in the body.
_Avoid_: database, backend.

**Skill-usage feedback**:
The read half of the skill axis — a skill event (a real load via
`skill_view`, or a view/patch) is replayed from the profile's `.usage.json`
sidecar into the store's usage `meta` (`touch_skill`/`set_skill_meta`) by the
`native-store-bridge`'s `on_skill_lifecycle` hook. Feeds the usage-aware
skill-index ranking (`skills.skill_rank_mode: by_usage`) via the shared
`META_*` vocabulary.

**Skill outcome**:
The outcome axis of skill feedback — the session-end review marks each skill
that session loaded (via `skill_view`) as `success|failure|unknown` from the
transcript evidence, persisted onto the store's `meta`
(`core/skill_outcome.mark_skill_outcome`). The raw signal the ranker/curator
can weight beyond recency.

**Skill curation**:
The action on the outcome axis — `core/skill_curate` flags skills whose
stored history is failing (rewrite vs retire), the review model authors a fix,
and `safe_evolve` gates the authored content (a blocking unsafe patch is
dropped). The "skills that actually get better" stage of the loop.

**Skill forge**:
The create-half — `core/skill_forge` distills a reusable-skill *proposal*
from a body module's public API (AST, deterministic, never imports);
`core/forge_skill` builds it into a SKILL.md body; the driver
(`scripts/run_skill_forge.py --write`) ships it store-first via
`record_skills.py`, gated by `safe_evolve`. Skills the loop grows, not just
fixes.

**Profile**:
The 3V0 profile's derived view of the store (MEMORY.md / USER.md /
SKILL.md). A projection, never the origin.
_Avoid_: source of truth, canonical store.

**Store-first**:
The write discipline — a fact or skill version is recorded in the store
first; the profile is re-exported from it. Inverts 3V0's
profile-as-origin model.
_Avoid_: sync-first, mirror-first.

**Derived view / export**:
The profile projection of a store's active entries.

**Retrieval**:
Choosing which store facts enter a view — ranked by keyword match, recency,
and feedback frequency (see **Feedback**), under a **Budget**.
_Avoid_: search, recall, lookup (retrieval is the ranking-and-selection act).

**Working set**:
The retrieval-chosen subset of facts rendered for injection — what the
profile view actually carries. The budget decides membership.
_Avoid_: result set, top-k list.

**Injection**:
Writing the working set into the derived view (MEMORY.md / the runtime tool
result) — the read half of store-first.
_Avoid_: export-all, projection (injection is *chosen*, not complete).

**Budget**:
The size cap the working set must fit — the profile's injected-view limit.
The seam's one hard constraint; facts are whole-or-out against it.
_Avoid_: limit, quota.

## Memory and lineage

**Fact**:
The unit of memory — content plus kind, source, timestamp, and supersession
links.
_Avoid_: entry, note, memory line.

**Kind**:
The category of a fact — `memory`, `user`, `identity`, or `directive`.
_Avoid_: type.

**Provenance**:
A fact's recorded origin (`source`) — who or what wrote it (foreground,
background review, operator, profile-import).

**Supersede / supersession**:
Replacing a fact or skill version by *linking* the old one to its successor
— marked inactive, never erased. Conflicts are flagged, never silently
overwritten.
_Avoid_: overwrite, update.

**Retract / retraction**:
Removing a fact or skill with no successor — a tombstoned terminal,
recoverable.
_Avoid_: delete, purge.

**Absorb / absorption**:
Decommissioning a skill by folding its content into an umbrella skill
(`absorbed_into`). Recoverable.
_Avoid_: merge, consolidate (when the lineage link is what matters).

**Lineage**:
The recoverable history chain of a fact or skill, reconstructed from
supersession links and append order.
_Avoid_: changelog, history log.

**Active**:
A fact or skill version not yet superseded, retracted, or absorbed.

**Feedback**:
The access_count / last_accessed signal a fact accumulates when it is
injected — retrieval reinforces what is actually pulled into context.
_Avoid_: usage stats, popularity.

**Forgetting**:
A fact's validity ending (valid_to) — the mechanism that keeps the store
from being append-only. Retrieval never injects a lapsed fact.
_Avoid_: deletion, expiry (the fact stays, recoverable; it just stops being
true).
**Terminal**:
A retracted or absorbed version — the end of a lineage, still recoverable.

## Skills

**SkillVersion**:
The unit of skill lineage — one recorded `skill_manage` event (create, patch,
edit, write_file, remove_file, delete) with its content, provenance, and
supersession links. The skill analogue of **Fact**.
_Avoid_: revision, commit.

**Decommission**:
The terminal act on a skill — **retract** (no successor) or **absorb** (folded
into an umbrella). Both recoverable; the umbrella term over the two terminals.
_Avoid_: remove, uninstall.

**Curator state**:
A skill's operational state — `active`, `stale`, or `archived` — orthogonal
to its content lineage. An archived skill has a live content version but is
not live in the profile.
_Avoid_: status, phase.

## Continuity

**Drift**:
Two artifacts disagreeing about the same reality. Cross-artifact, not
"stale" or "old."
_Avoid_: inconsistency (drift is the specific, detected case), staleness.

**Invariant**:
A named cross-artifact check over a flat JSON-safe context; it decides drift
and a detail string. The unit of the consistency ledger.
_Avoid_: test, assertion.

**Consistency ledger**:
The ordered, git-versioned registry of invariants the clock evaluates.

**Continuity anchor**:
The fixed point — Prime Directive + identity + a pointer to the continuity
model. Small, git-versioned, never regenerated from itself; the bottom of
the self-reference.
_Avoid_: source of truth, root config.

**Continuity clock / reconstruction clock**:
The mechanism that evaluates every invariant on wake and on the daemon tick
and reports drift.
_Avoid_: watchdog, monitor (it checks relations, not liveness).

**Healable drift**:
Drift the safe mechanical sync can fix (store↔profile consistency).
Auto-healed.
**Semantic drift**:
Drift needing deliberate, audited repair — the anchor, self-describing
reachability, the ledger, or a tracked loop. Flagged, never auto-rewritten.
_Avoid_: real drift, bad drift.

**Claim**:
A recorded state of a tracked upstream loop (a GitHub PR/issue) as of a time.
**Loop**:
A tracked upstream PR/issue whose state 3V0 is waiting on.

## Self-analytics (measurement axis)

**Report**:
The self-metrics snapshot — aggregated totals (sessions, tokens, cost,
per-model/per-task/per-day) that insights detect over. Local and self-owned,
never outbound.
_Avoid_: dashboard, metrics log, telemetry.

**Finding**:
The unit of detection over a report — a ranked result carrying a category,
severity, message, evidence, and a suggested action. Insights *propose*
findings; the dispose side acts.
_Avoid_: alert, warning, issue.

**Cache-hit ratio**:
The fraction of input tokens served from the prompt cache (cached ÷ all
input). The #1 token-cost lever — a broken prefix drops it and cost rises.
_Avoid_: cache rate, cache efficiency.

**Auxiliary task / aux routing**:
A side-task LLM call (compression, approval, curator, vision, title) and the
discipline of pinning each to a model — the cheap model for summarization,
the primary for the approval guard. Unpinned `auto` resolves to the *main*
model, not the cheap one.
_Avoid_: sub-model, background model, secondary model.

## Projects and the loop

**Project ledger**:
The data-driven registry of 3V0's projects (repo, upstream, drift delta,
store scope, open loops). Onboarding is a command, not a code edit.

**Primary project**:
3V0 itself — the project whose store also projects into the profile.
**Sibling project**:
F1NANCE / Axiom — reviewed into their own stores, store-only or memory-only,
with no profile projection.

**Stone**:
A versioned, live milestone of 3V0's evolution, recorded in the evolution loop.

**Evolution loop**:
The self-improvement cycle — store-first memory → skill lineage → reconcile →
curator state → own tools → own clock → multi-project → continuity.
_Avoid_: roadmap.

**Own clock**:
3V0's self-scheduled review daemon (systemd-supervised), independent of
3V0's cron/scheduler.
_Avoid_: cron job, scheduler.
