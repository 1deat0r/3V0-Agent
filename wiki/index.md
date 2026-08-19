# 3V0 Codebase Index (LLM Wiki)

The compiled, always-up-to-date knowledge layer over the 3V0 Agent repository.
**Every tracked path in the repo has exactly one index entry** — this file is
the master catalog; `areas/*.md` are the deep pages; `manifest.tsv` is the
raw 100%-coverage artifact.

## Reading order for a new agent

1. `wiki/SCHEMA.md` — the maintenance contract (what must stay true).
2. `wiki/index.md` (this file) — map of the whole tree.
3. `wiki/areas/<AREA>.md` — drill into the subsystem you were asked about.
4. Raw source in the repo — the wiki is a *pointer*, never a replacement.

Entry text is deliberately budget-capped so a small aux model
(`deepseek-v4-flash-0731`-class) can read any area page in one pass.

## Master map (20 areas)

| Area | Where | What lives there | Entry page |
|------|-------|------------------|------------|
| ROOT | `/` | Conversation loop, CLI, tool orchestration, session store, profile paths | `areas/ROOT.md` |
| CORE | `3v0/` | Sovereign memory core + standing systems + canonical data | `areas/CORE.md` |
| AGENT | `agent/` | AIAgent internals: providers, caching, memory, budget, curator | `areas/AGENT.md` |
| STATE | `ev0_state*.py` | Session store family + constants/logging | `areas/STATE.md` |
| TOOLS | `tools/`, `model_tools.py`, `toolsets.py` | Model tool registry + implementations | `areas/TOOLS.md` |
| CLI | `ev0_cli/`, `cli.py` | Interactive CLI, config, skins, dashboard server | `areas/CLI.md` |
| GATEWAY | `gateway/`, `tui_gateway/` | Messaging platforms + TUI backend | `areas/GATEWAY.md` |
| CRON | `cron/` | Scheduled jobs | `areas/CRON.md` |
| PLUGINS | `plugins/` | Plugin ecosystem (memory, providers, platforms, tools) | `areas/PLUGINS.md` |
| SKILLS | `skills/`, `optional-skills/` | The skill libraries | `areas/SKILLS.md` |
| PROVIDERS | `providers/`, `native/` | Provider profiles + native modules | `areas/PROVIDERS.md` |
| APPS | `apps/` | Desktop app + shared TS packages | `areas/APPS.md` |
| UITUI | `ui-tui/`, `tui_gateway/` | Ink terminal UI | `areas/UITUI.md` |
| WEB | `web/` | Dashboard frontend | `areas/WEB.md` |
| WEBSITE | `website/` | Docusaurus docs site | `areas/WEBSITE.md` |
| DOCS | `docs/`, root docs | ADRs, RFCs, guides, policies | `areas/DOCS.md` |
| SCRIPTS | `scripts/` | Dev/test/ops tooling | `areas/SCRIPTS.md` |
| TESTS | `tests/`, `evals/` | Test suites | `areas/TESTS.md` |
| INFRA | `docker/`, `nix/`, `.github/`, packaging | Deployment & CI | `areas/INFRA.md` |
| MISC | `locales/`, `assets/`, … | Auxiliary content | `areas/MISC.md` |

## The load-bearing spine (start here, in order)

Reading these gives you ~90% of the architecture in ~15 files:

1. `AGENTS.md` — governance + contribution law (the constitution).
2. `3v0/SOUL.md` + `3v0/CONTEXT.md` — the agent's identity (only if you will *be* the agent, not just work on the code).
3. `run_agent.py` — the conversation loop.
4. `cli.py` + `ev0_cli/main.py` — CLI entry + command dispatch.
5. `model_tools.py` + `tools/registry.py` + `toolsets.py` — how tools exist.
6. `ev0_state.py` + `ev0_constants.py` — persistence + paths.
7. `gateway/run.py` + `gateway/session.py` — the messaging orchestrator.
8. `agent/prompt_builder.py` + `agent/prompt_caching.py` — the cache-sacred system prompt.
9. `3v0/core/memdb.py` + `3v0/core/store.py` + `3v0/core/consolidate.py` — the memory substrate.
10. `scripts/handoff_check.sh` + `3v0/scripts/verify.sh` — done-ness and the wake ritual.

## Conventions to know before editing

- **Secrets live in `.env`; every behavioral setting in `config.yaml`** (`ev0_cli/config.py`). No new `HERMES_*` env vars for non-secrets.
- **Prompt caching is sacred** — never mutate past context, toolsets, or system prompt mid-conversation (`agent/prompt_cache_boundary.py`).
- **The core is a narrow waist** — new capability prefers CLI command + skill → service-gated tool → plugin → MCP server → new core tool, in that order (footprint ladder).
- **Tests run only via `scripts/run_tests.sh`** (CI-parity env, per-file subprocess isolation). Direct `pytest` diverges from CI.
- **Profile paths** — always `get_hermes_home()` from `ev0_constants`, never hardcoded `~/.hermes`.
- **Git invariant** — 3V0 always commits tracked changes; `memory.db` canonical state is versioned in git.
- **verify.sh is the done-gate** — body changes are "done" when it passes.

## Generated vs maintained

- `manifest.tsv` + `areas/*.md` — **generated** by `scripts/build_wiki.py --rebuild` (auto rows from docstrings + rules + sibling relations).
- `wiki/curated.tsv` + `wiki/areas/_intro_*.md` + `index.md`, `SCHEMA.md`, `README.md`, `log.md` — **hand-maintained**; rebuild preserves them.
- Large areas (TESTS, APPS, SKILLS, WEBSITE, UITUI, MISC) render as a **directory map** with one sub-page per group (`TESTS.tests.agent.md`, `APPS.desktop.md`, …) so any page fits a flash-model pass.
- Check the gate: `python3 scripts/build_wiki.py --check` (also wired into `.githooks/pre-commit`).