# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`AGENTS.md`** — the normative development guide. Its "How to use this
  file" map tells you which rules are always-on vs which reference to fetch
  on demand from **`docs/dev-guide/`** (the disclosed subsystem guides).
- **`CONTEXT.md`** at the repo root — the canonical domain glossary
  (runtime/chassis); `3v0/CONTEXT.md` is the scoped sub-glossary for the
  native substrate (recurses the root glossary — read both as one).
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **ADRs live in two places** — the runtime/chassis ledger is `docs/ADR.md`
  (dated, unnumbered); the `3v0/` native substrate uses the numbered series
  `3v0/docs/adr/`. See the banner at the top of `docs/ADR.md` for which to use.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo (this repo — the 3V0 agent body):

```
/
├── AGENTS.md                   ← normative spine + "how to use" map
├── CONTEXT.md                  ← canonical glossary (runtime/chassis)
├── docs/dev-guide/             ← disclosed subsystem reference (AGENTS.md → these)
├── docs/ADR.md                 ← runtime/chassis ADR ledger
├── 3v0/CONTEXT.md              ← scoped sub-glossary (native substrate)
├── 3v0/docs/adr/               ← native-substrate numbered ADRs
│   ├── 0001-store-first-memory.md
│   ├── 0002-check-before-heal.md
│   └── ...
└── src/ (threev0_cli/, agent/, tools/, ...)
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0006 (env-compat brand namespace) — but worth reopening because…_