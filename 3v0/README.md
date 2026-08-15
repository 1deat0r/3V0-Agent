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
- `data/memory.json` — the store's source of truth (seeded from the profile).
- `scripts/seed_from_profile.py` — import profile MEMORY.md / USER.md → store.
- `scripts/export_to_profile.py` — emit store → MEMORY.md / USER.md (derived
  view of the store; the profile becomes a projection, not the origin).
- `scripts/sync.py` — reconcile store ↔ profile (report by default, `--write`
  to converge).
- `scripts/record.py` — record/correct a fact in the store, then re-export the
  derived view to the profile.
- `scripts/ingest.py` — replay a memory-tool write into the store under lock
  (JSON on stdin). Called by the `native-store-bridge` plugin.
- `plugin/native-store-bridge/` — profile plugin (canonical source) that
  mirrors every successful `memory`-tool write into the store via a
  `post_tool_call` hook. Installed in the profile's `plugins/` and enabled in
  `config.yaml`; see `EVOLUTION_LOOP.md`.
- `tests/` — tests for the native core.

## Direction (v0.01 in progress)

1. **Own memory/identity substrate** (this directory) — done: the store is
   canonical, the profile a derived view.
2. **Own evolution loop** — in progress. Stone 1 (store-first memory) is live:
   the `native-store-bridge` plugin mirrors all memory writes (foreground +
   background review fork) into the store. Next: the curator/skill-store axis,
   or making the memory tool itself store-first.
3. **Own capabilities/tools** — designed for 3V0's purposes, not Hermes's.
4. **Own roadmap of versions** — Hermes recedes from "what 3V0 is" to "a
   runtime 3V0 currently runs on."

The goal is not to abandon the fork — it is to make the fork a detail.
