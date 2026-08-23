# Repository Layout — Why the root looks the way it does

Read this before you "tidy" the repo root. Most things you'd want to move are
there **on purpose**. This map is the single source of truth for every
top-level entry; `wiki/` is the generated file-by-file index.

## The flat core is a deliberate design

The repo root carries 21 top-level `.py` single-file modules (`run_agent.py`,
`cli.py`, `threev0_state.py`, `threev0_constants.py`, `model_tools.py`,
`toolsets.py`, `utils.py`, `mcp_serve.py`, …). This is **not** an accident
and **not** safe to consolidate into packages:

- They are declared as `[tool.setuptools] py-modules` in `pyproject.toml`.
  The comment there is load-bearing: *"Without this, uv2nix's sealed venv is
  missing threev0_constants, run_agent, etc."* Nix/Docker/installer builds
  depend on them being importable as top-level modules.
- They are imported as top-level modules across the whole codebase
  (`import run_agent`, `from threev0_constants import get_ev0_home`,
  `import cli`, `from toolsets import …`) — thousands of import sites. Moving
  them means re-pointing every one of those and rewriting the packaging
  contract. For an agent or a person, a flat root is easier to introspect
  than a hidden package tree.
- The architecture is a "narrow waist": `tools/registry.py` → `model_tools.py`
  → `run_agent.py` / `cli.py`. See AGENTS.md "File Dependency Chain".

**Do not relocate these modules.** If the flat root reads as mess, that's a
documentation failure, not a structural one — this file is the fix.

## Standard root docs (leave at root)

- `README.md`, `README.es/ur-pk/zh-CN.md` — product + localized READMEs.
- `CONTRIBUTING.md` / `CONTRIBUTING.es.md`, `SECURITY.md` / `SECURITY.es.md`,
  `LICENSE` — conventional root locations; tooling/site rules expect them here.
- `AGENTS.md` — the auto-injected development guide (root CWD lookup).
- `CONTEXT.md` — the canonical domain glossary.
- `HANDOFF.md` / `HANDOFF.generated.md` — session handoff; **script-pinned**
  at the repo root by `3v0/scripts/generate_handoff.py`. Do not move.
- `SELF_IMPROVEMENT.md` (theory), `SUSTAINABILITY.md` (funding) — root-level
  body docs, cross-linked to their `3v0/` counterparts.

## Puppet / build files

| File | Purpose | Notes |
|------|---------|-------|
| `pyproject.toml`, `uv.lock`, `setup.py` | Python packaging | `setup.py` is a Nix/sdist build guard |
| `package.json`, `package-lock.json`, `.npmrc`, `.nvmrc` | JS build (eslint, ui-tui) | |
| `setup-3v0.sh`, `3v0-cli` | Installer + launcher | |
| `eslint.config.shared.mjs`, `.prettierrc`, `.prettierignore`, `.coderabbit.yaml` | Lint/CI config | |
| `.env.example`, `cli-config.yaml.example`, `constraints-termux.txt` | Config samples / termux pins | referenced by `scripts/install.sh` |

## Top-level directories (the real layout)

- `threev0_cli/` — CLI subcommands, setup wizard, plugins loader, config.
- `agent/` — agent internals (providers, memory, compression, model adapters).
- `tools/` — tool implementations (`tools/registry.py`), `tools/environments/`.
- `gateway/` — messaging gateway (`run.py` + `platforms/`).
- `tui_gateway/`, `ui-tui/` — TUI backend + Ink renderer.
- `plugins/` — plugin system (memory, model-providers, platforms, …).
- `providers/` — legacy provider profiles (see `plugins/model-providers/`).
- `cron/`, `batch_runner.py`-alike — scheduler + batch execution.
- `acp_adapter/` — ACP (editor protocol) server.
- `skills/`, `optional-skills/`, `optional-mcps/` — bundled skills / MCPs.
- `tests/`, `scripts/` — pytest suite + tooling.
- `docs/` — engineering docs: `dev-guide/` (subsystem reference), `agents/`
  (discovery: domain/issue-tracker/triage), `audit/` (completed audits),
  `ADR.md` (runtime/chassis ADRs), plus per-topic reference.
- `3v0/` — the **native substrate**: store-first memory/evolution layer
  (its own sub-glossary `3v0/CONTEXT.md`, ADRs `3v0/docs/adr/`, continuity
  `3v0/CONTINUITY.md`).
- `web/` — web dashboard frontend.
- `wiki/` — generated file-by-file index (`wiki/index.md`, `wiki/manifest.tsv`).
- `native/` — native code (e.g. `fts5_cjk` sqlite extension).
- `locales/` — i18n bundles.

## What is deliberately NOT here (only in the working dir)

`node_modules/`, `.venv/`, `__pycache__/`, `.pytest_cache/`,
`3v0_agent.egg-info/`, `test_durations.json`, `.bytecode-fingerprint` are all
gitignored build/session debris. They are safe to delete locally and reappear
on build; they are not part of the repo and not "clutter."