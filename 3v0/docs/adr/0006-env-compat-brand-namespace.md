# ADR-0006 — Brand-compatible env namespace (corrected: migrate to 3V0_*)

Status: accepted + amended (2026-08-21, second revision)
Scope: ev0-brand env vars, import package, and the eradication boundary

## Context — operator directive (authoritative)

> "It should all be 3V0 unless it cannot because of a hard barrier."

Verified barrier map (tested, not assumed):

| Surface | Can it be `3V0_*`? | Evidence |
|---|---|---|
| Python `os.environ` keys | **YES** | `os.environ['3V0_HOME']=...` valid key; no grammar rule on keys |
| `env VAR=x cmd` (wrappers, systemd) | **YES** | `env '3V0_TEST=1' python -c ...` works |
| `.env` / `.env.example` | **YES** | no barrier — dotenv-style files accept any name |
| File names, package.json names, git paths | **YES** | no grammar rule outside Python identifiers |
| POSIX shell `export 3V0_X=x` | **NO** | `export: not a valid identifier` — use `env VAR=x cmd` instead |
| Python import statement `import 3v0_cli` | **NO** | `SyntaxError: invalid decimal literal` — identifiers can't start with a digit. Rename to a valid identifier (`threev0_cli`) instead |

Conclusion: the old-name residue (`EV0_*` env vars, `threev0_cli` package,
`threev0_logging.py`, `3v0-ink`, etc.) is **not** a permanent exception — it is
under active migration. Only two constraints survive:

1. Python identifiers must not start with a digit → package/module names use
   the `threev0*` spelling (same family as the `THREEV0_*` units).
2. Shell wrappers assign digit-leading vars via `env '3V0_X=...' cmd`, never
   `export 3V0_X=...`.

## Migration phases

- **Phase E (env contract):** `EV0_*` → `3V0_*` in Python reads/writes,
  `.env.example`, `setup-3v0.sh`, workflows, AGENTS.md doctrine, comments.
  Python resolves `3V0_*` first, `EV0_*` second (legacy read-compat, dropped
  once no production path reads EV0_*). `THREEV0_*` is NOT a production
  writer — systemd `Environment="3V0_X=..."` accepts digit-leading keys
  (grammar only bites POSIX `export`, which we avoid via `env VAR=x cmd`).
  The env namespace is exactly two spellings: `3v0` (everywhere grammar
  allows) and `threev0` (Python identifiers only — `import 3v0_cli` is a
  `SyntaxError`).
- **Phase P (import package):** `threev0_cli/` (and
  `threev0_bootstrap.py`, `threev0_logging.py`, `threev0_state*.py`,
  `ui-tui/packages/3v0-ink/` similarly), mechanical import rewrites across
  ~749 files / 6,514 import sites, gated by the canonical test suite.
- **Phase R (remainder):** residual `ev0` in comments/history/allowlists —
  scrubbed or declared with a written justification.

Each phase is behavior-preserving (rename-only; no semantics change), except
the final removal of the EV0_* read fallback, which is a deliberate breaking
change scheduled after the runtime's next restart.

## Consequences

- New code: use `3V0_*` env vars; import from `threev0_cli` after Phase P.
- The previous "declared exceptions" section of this ADR is **retired** —
  it overstated the barrier and treated inertia as a constraint.
- `3v0/data/memory.db` old-name bytes remain classified as history (session
  text, never scrubbed) — the one standing boundary.