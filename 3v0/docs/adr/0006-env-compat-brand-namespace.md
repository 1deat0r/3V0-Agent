# ADR-0006 — Brand-compatible env namespace (declared exceptions to eradication)

Status: accepted (2026-08-21)
Scope: ev0-brand env vars, import package, and the eradication boundary

## Context

The operator's total-eradication directive demands zero mentions of the old
brand name (`ev0`, all case variants) with brand-consistent replacements and
functional equivalence. A mass rename of the **env namespace** to the brand
would break every existing install, wrapper, systemd/docker unit, shell export,
and the running gateway for zero functional gain. The import package
`ev0_cli` also cannot be renamed to `3v0_cli` (`3v0_cli` is not a valid Python
identifier; `import 3v0_cli` is a SyntaxError).

## Decision

Three-layer env contract — documented, deterministic, migration-ready:

1. **Canonical (new code):** `3V0_*` — all *new* env vars and new reads use
   `3V0_<NAME>`. `3V0_HOME` is the canonical home var; `EV0_HOME` remains a
   read-compat fallback (see resolver below).
2. **Daemon units:** existing `THREEV0_*` family (THREEV0_PROJECT,
   THREEV0_REVIEW_COOLDOWN_S, THREEV0_SKILLS_DIR, ...) is retained as an
   accepted alias family for service units that predate the brand rename —
   functionally equivalent, documented here so new work does not add to it.
3. **Legacy compat:** `EV0_*` remains a *readable* namespace for the live
   runtime (gateway, launcher, profiles all set/consume EV0_HOME today) and is
   a **declared exception** to eradication — not to be written by new code,
   not to be scrubbed from working runtime behavior.

Resolver rule (in `3v0/core/env_compat.py`): for a logical setting
`<NAME>`, read in order `3V0_<NAME>` → `THREEV0_<NAME>` → `EV0_<NAME>`
(first truthy wins). New code SHOULD use the resolver; direct `os.environ`
reads of `EV0_*` in the native core SHOULD be migrated to it.

## Declared exceptions to "zero mentions"

- Import package `ev0_cli` (6,514 import sites) + `tests/ev0_cli/` path —
  Python identifier constraint; allowlisted.
- `EV0_*` env namespace — runtime compat contract, see above.
- `3v0/data/memory.db` binary old-name tokens — session-history text, scope
  boundary (see plan + commit 07170f598d).
- `.env.example`, workflows, AGENTS.md doctrine — being migrated to the
  canonical `3V0_*` guide; historical comments retained by intent.

## Consequences

- Behavior unchanged today (no process sets `3V0_HOME` yet; resolver falls
  through to `EV0_HOME`).
- New code has an obvious, reviewable pattern; deny-regex/CI can flag new
  `EV0_*` writes without breaking the runtime.
- Eradication claims should be stated as "brand eradication at UI/docs/prose +
  declared compat exceptions", not "zero bytes of ev0".