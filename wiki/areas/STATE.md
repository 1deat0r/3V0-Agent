# ev0_state* + ev0_constants/logging — session store & profile paths

The session store family. `ev0_state.py` (SessionDB, FTS5) + schema/search/common/portability siblings; `ev0_constants.py` (get_hermes_home — profile-aware), `ev0_logging.py`, `ev0_time.py`. Hardcoding ~/.hermes anywhere else is the known-bug class.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `ev0_bootstrap.py` | source | Early-boot module that applies profile override and seeds environment before other imports | Runs before everything so HERMES_HOME / profile routing is correct at import time | ev0_constants.py;ev0_cli/main.py |
| `ev0_cli/__init__.py` | source | Hermes CLI - Unified command-line interface for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/_early_recovery.py` | source | Dependency-light venv recovery that runs BEFORE ev0_cli.main's imports. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/_install_repair.py` | source | Dependency install execution shared between early recovery and full recovery. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/_parser.py` | source | Top-level argparse construction for the hermes CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/_scan_venv_blockers.py` | source | ``ev0_cli/_scan_venv_blockers.py`` — Standalone venv-process scan for JSON consumption. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/_startup_fast.py` | source | Pre-import startup fast paths — THE canonical lightweight helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/_subprocess_compat.py` | source | Windows subprocess compatibility helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/active_sessions.py` | source | Cross-process active chat session leases. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/agent_import.py` | source | hermes import-agent — import Claude Code / Codex CLI setups into Hermes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/agent_plugins.py` | source | Compatibility helpers for Agent Plugins v1 portable directory packages. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/approval_mode.py` | source | Shared persistent approval-mode command logic. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/approval_transport.py` | source | Host-owned contract for plugin-provided human approval transports. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/approvals_suggest.py` | source | ``hermes approvals suggest`` — mine approval history into allowlist proposals. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/approvals_test.py` | test | ``hermes approvals test`` — dry-run approval verdict for a command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `ev0_cli/auth.py` | source | Auth flows (login/logout, providers) | Account surface | ev0_cli/auth_commands.py |
| `ev0_cli/auth_commands.py` | source | Credential-pool auth subcommands. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/azure_detect.py` | source | Azure Foundry endpoint auto-detection. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/backup.py` | source | hermes backup subcommand | State export | safety: ev0_state_portability.py |
| `ev0_cli/bang_shell.py` | source | ``!<command>`` shell mode for the interactive CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/banner.py` | source | Startup banner rendering | Branding + build info | ev0_cli/skin_engine.py;assets/banner.png |
| `ev0_cli/blueprint_cmd.py` | source | Shared ``/blueprint`` command logic for CLI, TUI, and gateway. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/browser_connect.py` | source | Shared helpers for attaching Hermes to a local Chromium-family CDP port. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/build_info.py` | source | Baked-in build metadata for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/bundles.py` | source | Bundle management (skill/skin bundles) | Install surface | tools/skills_hub.py |
| `ev0_cli/callbacks.py` | source | Interactive prompt callbacks for terminal_tool integration. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/checkpoints.py` | source | CLI-side checkpoint integration | Resume-after-crash in the CLI | tools/checkpoint_manager.py |
| `ev0_cli/claw.py` | source | Claw — capture/alt-input mode | Advanced input modes | cli.py |
| `ev0_cli/cli_agent_setup_mixin.py` | source | Agent-construction and session-resume display methods for ``HermesCLI``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/cli_billing_mixin.py` | source | Billing and subscription handlers for the interactive CLI (god-file decomposition). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/cli_commands_mixin.py` | source | Slash-command handlers for the interactive CLI (god-file decomposition Phase 4). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/cli_output.py` | source | Shared CLI output helpers for Hermes CLI modules. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/clipboard.py` | source | Clipboard integration | Paste UX | cli.py |
| `ev0_cli/codex_models.py` | source | Codex model discovery from API, local cache, and config. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/codex_runtime_plugin_migration.py` | source | Migrate Hermes' MCP server config and Codex's installed curated plugins | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/codex_runtime_switch.py` | source | Shared logic for the /codex-runtime slash command. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/colors.py` | source | Shared ANSI color utilities for Hermes CLI modules. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/commands.py` | source | COMMAND_REGISTRY — canonical slash commands (CommandDef) | Single source: CLI, gateway, Telegram menu, Slack map, autocomplete | cli.py;gateway/run.py;gateway/slash_commands.py |
| `ev0_cli/completion.py` | source | Slash command + path autocomplete | CLI input UX | ev0_cli/commands.py |
| `ev0_cli/config.py` | source | DEFAULT_CONFIG schema + loaders (load_config, migrations, OPTIONAL_ENV_VARS) | The config.yaml contract; non-secret settings live here, not .env | ev0_cli/config_defaults.py;ev0_cli/config_migrations.py |
| `ev0_cli/config_defaults.py` | source | Default config values | Deep-merged under user YAML | ev0_cli/config.py |
| `ev0_cli/config_migrations.py` | source | Config version migrations | Bumps _config_version only when a transform is needed | ev0_cli/config.py |
| `ev0_cli/console_engine.py` | source | Console abstraction layer | Portable output | ev0_cli/cli_output.py |
| `ev0_cli/container_boot.py` | source | Container-boot reconciliation of per-profile gateway s6 services. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/context_switch_guard.py` | source | Warn when an in-session model switch will trigger preflight compression on the next turn. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/copilot_auth.py` | source | GitHub Copilot authentication utilities. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/credential_lifecycle.py` | source | Unified provider-credential lifecycle across every store Hermes reads. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/cron.py` | source | hermes cron subcommand | CLI surface for cron/jobs.py | cron/jobs.py;ev0_cli/commands.py |
| `ev0_cli/curator.py` | source | CLI subcommand: `hermes curator <subcommand>`. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/curses_ui.py` | source | Shared curses menu machinery | Every interactive menu must be built here | ev0_cli/tools_config.py |
| `ev0_cli/dashboard_auth/__init__.py` | source | Dashboard authentication provider framework. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/audit.py` | source | Audit log for dashboard-auth events. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/base.py` | source | Abstract base + dataclasses + exceptions for dashboard auth providers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/cookies.py` | source | Cookie helpers for dashboard auth. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/login_page.py` | source | Server-rendered /login page. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/middleware.py` | source | Auth-gate middleware for the dashboard. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/native_flow.py` | source | Gateway-brokered RFC 8252 (OAuth 2.0 for Native Apps) authorization store. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/prefix.py` | source | Helpers for X-Forwarded-Prefix support. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/public_paths.py` | source | Shared allowlist of ``/api/*`` paths that bypass dashboard auth. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/registry.py` | source | Module-level registry for DashboardAuthProvider instances. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/routes.py` | source | HTTP routes for the dashboard-auth OAuth round trip. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/token_auth.py` | source | Route-agnostic non-interactive (bearer-token) auth seam for the dashboard. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_auth/ws_tickets.py` | source | WS-upgrade auth credentials for gated mode. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_procs.py` | source | Dashboard process-hygiene helpers — extracted from ``ev0_cli/main.py``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dashboard_register.py` | source | ``hermes dashboard register`` — register a self-hosted dashboard OAuth client. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/data/plugin_index.json` | data | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `ev0_cli/debug.py` | source | ``hermes debug`` debug tools for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/default_soul.py` | source | Default SOUL.md template seeded into HERMES_HOME on first run. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dep_ensure.py` | source | Lazy dependency bootstrapper for non-Python runtime deps. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/diagnostics_upload.py` | source | Client for uploading ``hermes debug share`` bundles to Nous-internal S3. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dingtalk_auth.py` | source | DingTalk Device Flow authorization. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/doctor.py` | source | Doctor command for hermes CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/doctor_live.py` | source | ``hermes doctor --live`` — opt-in bounded real-call tool-backend probes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/dump.py` | source | Dump command for hermes CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/env_loader.py` | source | Helpers for loading Hermes .env files consistently across entrypoints. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/fallback_cmd.py` | source | hermes fallback — manage the fallback provider chain. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/fallback_config.py` | source | Helpers for reading the effective fallback provider chain from config. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/focus_view.py` | source | Focus view — a display-only reduced-output mode. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/foreign_sessions.py` | source | Import sessions from foreign coding agents (Claude Code, Codex CLI). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/gateway.py` | source | Gateway subcommand for hermes CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/gateway_enroll.py` | source | ``hermes gateway enroll`` — enroll a self-hosted gateway with a relay connector. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/gateway_windows.py` | source | Windows gateway service backend (Scheduled Task + Startup-folder fallback). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/gitlock.py` | source | Stale git lock-file recovery for update/check paths. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/goals.py` | source | Persistent session goals — the Ralph loop for Hermes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/gui_uninstall.py` | source | Hermes Desktop (Chat GUI) uninstaller. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/heartbeat.py` | source | Session heartbeats — recurring re-entry prompts for the current session. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/hooks.py` | source | hermes hooks — inspect and manage shell-script hooks. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/init_command.py` | source | ``/init`` — build the prompt that generates or updates a project AGENTS.md. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/input_sanitize.py` | source | Sanitize user prompt text leaked from terminal / paste control sequences. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/inventory.py` | source | Provider/model inventory context — shared substrate for the dashboard | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/journey.py` | source | ``hermes journey`` — what Hermes has learned, on a timeline. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/kanban.py` | source | CLI for the Hermes Kanban board — ``hermes kanban …`` subcommand. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/kanban_db.py` | source | SQLite-backed Kanban board for multi-profile, multi-project collaboration. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/kanban_decompose.py` | source | Kanban decomposer — fan a triage task out into a graph of child tasks. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/kanban_diagnostics.py` | source | Kanban diagnostics — structured, actionable distress signals for tasks. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/kanban_specify.py` | source | Kanban triage specifier — flesh out a one-liner into a real spec. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/kanban_swarm.py` | source | Kanban Swarm v1: thin swarm topology helpers on top of Kanban. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/lifecycle.py` | source | Hermes lifecycle dispatch for first-party observers and plugins. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/linux_desktop_entry.py` | source | Install and remove the Linux desktop entry (``hermes.desktop``). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/logs.py` | source | ``hermes logs`` — view and filter Hermes log files. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/loops.py` | source | Recurring in-session wakeups — the /loop command (Claude Code parity). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/main.py` | source | CLI entrypoint — argparse tree, profile override bootstrap, subcommand wiring | The hermes command; _apply_profile_override must run before any import | ev0_bootstrap.py;ev0_cli/config.py |
| `ev0_cli/managed_scope.py` | source | Managed scope — IT-pushed, user-immutable config & env layer. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/managed_uv.py` | source | Hermes-managed uv and Python runtime repair. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/mcp_catalog.py` | source | MCP catalog — curated, Nous-approved MCP servers shipped with the repo. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/mcp_config.py` | source | MCP Server Management CLI — ``hermes mcp`` subcommand. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/mcp_picker.py` | source | MCP picker — interactive `hermes mcp picker` (also the default `hermes mcp`). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/mcp_security.py` | source | Security checks for user-configured MCP server entries. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/mcp_startup.py` | source | Shared CLI/TUI-safe helpers for background MCP discovery. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/mem_trim.py` | source | Rate-limited heap release for long-lived Hermes gateway processes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/memory_oauth.py` | source | HTTP routes for memory-provider OAuth connect, mounted by ``web_server``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/memory_setup.py` | source | hermes memory setup\|status — configure memory provider plugins. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/middleware.py` | source | Hermes middleware contract helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/migrate.py` | source | CLI handlers for ``hermes migrate ...``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/moa_cmd.py` | source | CLI helpers for configuring Mixture of Agents. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/moa_config.py` | source | Mixture-of-Agents configuration and slash-command helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/model_catalog.py` | source | Remote model catalog fetcher. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/model_cost_guard.py` | source | Expensive-model confirmation helpers for model selection surfaces. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/model_data_policy_guard.py` | source | Data-policy confirmation helpers for model selection surfaces. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/model_normalize.py` | source | Per-provider model name normalization. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/model_search.py` | source | Picker-only search aliases for model ids. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/model_selection_guards.py` | source | Unified selection-time guard registry for model switching surfaces. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/model_setup_flows.py` | source | Per-provider model-selection wizard flows for ``hermes setup`` / ``hermes model``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/model_switch.py` | source | Shared model-switching logic for CLI and gateway /model commands. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/models.py` | source | Canonical model catalogs and lightweight validation helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/nous_account.py` | source | Normalized Nous Portal account entitlement helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/nous_auth_keepalive.py` | source | Background keepalive for long-lived Nous Portal sessions. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/nous_billing.py` | source | Nous Portal Remote Spending HTTP client (Phase 2b). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/nous_subscription.py` | source | Helpers for Nous subscription managed-tool capabilities. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/npm_engine.py` | source | Recover from npm ``EBADENGINE`` failures by upgrading a managed npm. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/observability/__init__.py` | source | First-party Hermes observability integrations. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/observability/relay_runtime.py` | source | Compatibility alias for the core Hermes Relay runtime. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/observability/relay_shared_metrics.py` | source | Direct NeMo Relay integration for Hermes shared client metrics. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/observability/schemas/3v0.shared_metrics.v1.schema.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `ev0_cli/observability/schemas/3v0.shared_metrics.v2.schema.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `ev0_cli/observability/shared_metrics.py` | source | Durable aggregation and local export for Hermes shared metrics. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/observability/shared_metrics_contract.py` | source | Bounded product contract for the first Hermes shared-metrics slice. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/observability/shared_metrics_subscriber.py` | source | Relay subscriber for the persisted Hermes shared-metrics slice. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/onepassword_secrets_cli.py` | source | CLI handlers for ``hermes secrets onepassword ...``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/oneshot.py` | source | Oneshot (-z) mode: send a prompt, get the final content block, exit. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/pairing.py` | source | CLI commands for the DM pairing system. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/partial_compress.py` | source | Boundary-aware partial compression — "summarize up to here". | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/personality.py` | source | Single owner for personality overlays. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/pets.py` | source | CLI subcommand: ``hermes pets <subcommand>``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/platform_actions.py` | source | Capability-gated platform action facade for plugins (#64176, action half). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/platforms.py` | source | Shared platform registry for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/plugin_capabilities.py` | source | Plugin capability declarations + consent state (#64228). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/plugin_dev.py` | source | Runtime-backed validation behind ``hermes plugins doctor``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/plugin_index.py` | source | Community plugin index — fetch, cache, search, and name resolution. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/plugin_packs.py` | source | Plugin packs — declarative, shareable plugin sets (#64166). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/plugins.py` | source | PluginManager — discovery of ~/.hermes/plugins, repo plugins, pip entry points | Ships register(ctx) hooks + register_tool + register_cli_command | plugins/;tools/registry.py |
| `ev0_cli/plugins_cmd.py` | source | ``hermes plugins`` CLI subcommand — install, update, remove, and list plugins. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/portal_cli.py` | source | ``hermes portal`` — the human-readable entry point for Nous Portal. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/profile_describer.py` | source | Profile describer — auto-generate ``description`` for a profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/profile_distribution.py` | source | Profile distributions — shareable, packaged Hermes profiles via git. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/profiles.py` | source | Profile management for multiple isolated Hermes instances. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/projects_cmd.py` | source | ``hermes project`` CLI — manage first-class, multi-folder Projects. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/projects_db.py` | source | Per-profile first-class Project store. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/prompt_size.py` | source | Prompt-size diagnostic: ``hermes prompt-size``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/prompt_stash.py` | source | Ctrl+S prompt stash — pure state machine for the classic CLI composer. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/provider_catalog.py` | source | Unified provider catalog — one source of truth for the provider universe. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/providers.py` | source | Single source of truth for provider identity in Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/proxy/__init__.py` | source | Local OpenAI-compatible proxy that forwards to OAuth-authenticated upstreams. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/proxy/adapters/__init__.py` | source | Upstream adapter registry for the local proxy server. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/proxy/adapters/base.py` | source | Abstract base for proxy upstream adapters. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/proxy/adapters/nous_portal.py` | source | Nous Portal upstream adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/proxy/adapters/xai.py` | source | xAI Grok OAuth upstream adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/proxy/cli.py` | source | CLI handlers for the ``hermes proxy`` subcommand. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/proxy/server.py` | source | HTTP server that forwards OpenAI-compatible requests to a configured upstream. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/proxy_cli.py` | source | CLI handlers for ``hermes egress ...``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/psutil_android.py` | source | Helpers for the temporary psutil-on-Android compatibility installer. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/pt_input_extras.py` | source | Augmentations to prompt_toolkit's input-parsing tables. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/pty_bridge.py` | source | PTY bridge — spawns hermes --tui for the dashboard terminal pane | AUTH via ephemeral _SESSION_TOKEN; POSIX PTY only | ev0_cli/web_server.py;ui-tui/ |
| `ev0_cli/pty_session.py` | source | Keep-alive PTY sessions for dashboard terminals. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/relaunch.py` | source | Unified self-relaunch for Hermes CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/resource_limits.py` | source | Best-effort process resource-limit adjustments for long-running services. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/route_identity.py` | source | Fail-closed URL identity normalization for model/provider routes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/runtime_provider.py` | source | Shared runtime provider resolution for CLI, gateway, cron, and helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/secret_prompt.py` | source | Secret input prompts with masked typing feedback. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/secrets_cli.py` | source | CLI handlers for ``hermes secrets bitwarden ...``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/security_advisories.py` | source | Security advisory checker for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/security_audit.py` | source | On-demand supply-chain audit for Hermes Agent installs. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/security_audit_startup.py` | source | Startup security posture audit (warn-on-load, never blocks). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/send_cmd.py` | source | CLI subcommand: ``hermes send`` — pipe text from shell scripts to any | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/service_manager.py` | source | Abstract service manager interface. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/session_export.py` | source | Shared renderers for session export commands. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/session_export_html.py` | source | HTML Export generator for Hermes sessions. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/session_export_md.py` | source | Markdown/QMD export helpers for Hermes sessions. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/session_filters.py` | source | Shared time/filter parsing for `hermes sessions prune` / `archive`. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/session_listing.py` | source | Shared session-listing helpers for CLI and gateway slash surfaces. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/session_lost_and_found.py` | source | Last-resort page-level salvage for an unreadable session database schema. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/session_recap.py` | source | Session recap — summarize what's happened in the current session. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/session_recovery.py` | source | Offline, non-destructive recovery for a damaged Hermes session database. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/sessions_cmd.py` | source | ``hermes sessions`` command — extracted from ``ev0_cli/main.py``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/setup.py` | build | Legacy setup shim | Compatibility entrypoint delegating to pyproject |  |
| `ev0_cli/setup_hidden_env.py` | source | Which platform env vars the setup surfaces hide. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/setup_whatsapp_cloud.py` | source | Interactive setup wizard for the WhatsApp Cloud API adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/sizefmt.py` | source | Small shared size-formatting helpers for CLI/agent output. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/skills_config.py` | source | Skills configuration for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/skills_hub.py` | source | Skills Hub CLI — Unified interface for the Hermes Skills Hub. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/skin_cmd.py` | source | ``hermes skin`` — list, switch, and tweak skins from the CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/skin_engine.py` | source | Skin system — built-in + user YAML skins, data-driven CLI theming | Skins are pure data; no code per skin | ev0_cli/colors.py;agent/display.py |
| `ev0_cli/slack_cli.py` | source | ``hermes slack ...`` CLI subcommands. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/slash_exec.py` | source | Registry-owned slash command execution (thin slice). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/sqlite_runtime.py` | source | Import-safe helpers for inspecting a Python interpreter's linked SQLite. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/sqlite_safe_read.py` | source | Lock-safe inspection of SQLite database files. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/sqlite_util.py` | source | Shared SQLite primitives for the small per-profile / board stores. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/status.py` | source | Status command for hermes CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/stderr_timestamp.py` | source | Run a child process while prefixing each stderr line with a timestamp. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/stdio.py` | source | Windows-safe stdio configuration. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/__init__.py` | source | CLI subcommand parser builders for ``hermes <subcommand>``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/_shared.py` | source | Shared parser helpers used across multiple CLI subcommand builders. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/acp.py` | source | ``hermes acp`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/approvals.py` | source | ``hermes approvals`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/auth.py` | source | ``hermes auth`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/backup.py` | source | ``hermes backup`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/claw.py` | source | ``hermes claw`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/config.py` | source | ``hermes config`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/console.py` | source | ``hermes console`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/cron.py` | source | ``hermes cron`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/dashboard.py` | source | ``hermes dashboard`` / ``hermes serve`` subcommand parsers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/debug.py` | source | ``hermes debug`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/doctor.py` | source | ``hermes doctor`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/dump.py` | source | ``hermes dump`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/gateway.py` | source | ``hermes gateway`` and ``hermes proxy`` subcommand parsers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/gui.py` | source | ``hermes gui`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/hooks.py` | source | ``hermes hooks`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/import_agent.py` | source | ``hermes import-agent`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/import_cmd.py` | source | ``hermes import`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/insights.py` | source | ``hermes insights`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/login.py` | source | ``hermes login`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/logout.py` | source | ``hermes logout`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/logs.py` | source | ``hermes logs`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/mcp.py` | source | ``hermes mcp`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/memory.py` | source | ``hermes memory`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/model.py` | source | ``hermes model`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/monitoring.py` | source | ``hermes monitoring`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/pairing.py` | source | ``hermes pairing`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/pause.py` | source | ``hermes pause`` / ``hermes resume`` — the global emergency stop. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/plugins.py` | source | ``hermes plugins`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/profile.py` | source | ``hermes profile`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/prompt_size.py` | source | ``hermes prompt-size`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/security.py` | source | ``hermes security`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/setup.py` | build | Legacy setup shim | Compatibility entrypoint delegating to pyproject |  |
| `ev0_cli/subcommands/skills.py` | source | ``hermes skills`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/skin.py` | source | ``hermes skin`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/slack.py` | source | ``hermes slack`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/status.py` | source | ``hermes status`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/sync.py` | source | ``hermes sync`` subcommand parser — Skill Sync. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/tools.py` | source | ``hermes tools`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/uninstall.py` | source | ``hermes uninstall`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/update.py` | source | ``hermes update`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/verify.py` | source | ``hermes verify`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/version.py` | source | ``hermes version`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/webhook.py` | source | ``hermes webhook`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/subcommands/whatsapp.py` | source | ``hermes whatsapp`` subcommand parser. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/suggestions_cmd.py` | source | Shared ``/suggestions`` command logic for CLI and gateway. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/telegram_managed_bot.py` | source | Telegram Managed Bot onboarding client. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/terminal_breadcrumbs.py` | source | Per-terminal session breadcrumbs for ``hermes -c`` / ``--continue``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/timefmt.py` | source | Small shared time-formatting helpers for CLI output. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/timeouts.py` | source | Python module `timeouts.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/tips.py` | source | Random tips shown at CLI session start to help users discover features. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/tools_config.py` | source | hermes tools curses UI | The toolset enable/disable picker (curses, per project law) | ev0_cli/curses_ui.py;toolsets.py |
| `ev0_cli/toolset_validation.py` | source | Validation for the ``platform_toolsets`` config section. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/uninstall.py` | source | Hermes Agent Uninstaller. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/update_cmd.py` | source | Hermes update pipeline — extracted from ``ev0_cli/main.py``. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/update_lock.py` | source | Cross-process mutual exclusion for in-flight Hermes updates. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/urllib_security.py` | source | Security policy for credential-bearing stdlib urllib requests. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/vercel_auth.py` | source | Helpers for reporting Vercel Sandbox authentication state. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/verify_cmd.py` | source | ``hermes verify`` — detect a project's run recipe and smoke-test it. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/voice.py` | source | Process-wide voice recording + TTS API for the TUI gateway. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_deps.py` | source | Shared late-binding dependency seam for extracted dashboard routers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_git.py` | source | Backend git operations for the desktop coding rail + Codex-style review pane. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_models.py` | source | Pydantic request/response models for the Hermes dashboard web server. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_routers/__init__.py` | source | Extracted APIRouter modules for the dashboard web server. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_routers/cron.py` | source | Cron dashboard routes (extracted verbatim from web_server.py). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_routers/git.py` | source | Git dashboard routes (extracted verbatim from web_server.py). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_routers/mcp.py` | source | MCP dashboard routes (extracted verbatim from web_server.py). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_routers/profiles.py` | source | Profiles dashboard routes (extracted verbatim from web_server.py). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_routers/sessions.py` | source | Session dashboard routes (extracted verbatim from web_server.py). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_routers/skills.py` | source | Skills dashboard routes (extracted verbatim from web_server.py). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_routers/tools.py` | source | Toolset / terminal-backend dashboard routes (extracted verbatim from | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/web_server.py` | source | Dashboard web server + /api/pty WebSocket endpoint (embedded hermes --tui) | Serves 3v0 dashboard; the PTY tunnel is the chat surface bridge | ev0_cli/pty_bridge.py;web/;ui-tui/ |
| `ev0_cli/webhook.py` | source | hermes webhook — manage dynamic webhook subscriptions from the CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/win_pty_bridge.py` | source | Windows ConPTY bridge for the `hermes dashboard` chat tab. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/windows_ssh_runtime.py` | source | Native Windows trust boundary for Desktop SSH backend lifecycle. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/write_approval_commands.py` | source | Shared handlers for the /memory and /skills write-approval subcommands. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_cli/xai_retirement.py` | source | Detect xAI models retired on May 15, 2026. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `ev0_constants.py` | source | get_hermes_home() / display_hermes_home() — profile-aware path resolution | Every state path in the body resolves through here; hardcoding ~/.hermes elsewhere is a known-bug class | ev0_logging.py;ev0_bootstrap.py;tests/ev0_cli/test_profiles.py |
| `ev0_logging.py` | source | setup_logging() — agent.log / errors.log / gateway.log (profile-aware) | All logs land per-profile via HERMES_HOME; browse with hermes logs | ev0_constants.py;gateway/run.py |
| `ev0_state.py` | source | SessionDB — the SQLite session store (FTS5 search, project/session records) | Canonical session persistence backing resume/search/desktop; god-file, split across ev0_state_* siblings | ev0_state_schema.py;ev0_state_search.py;ev0_state_common.py;ev0_state_portability.py |
| `ev0_state_common.py` | source | Shared helpers for the session store family (types, paths, common queries) | Avoids circular imports between ev0_state and its satellites | ev0_state.py;ev0_state_portability.py |
| `ev0_state_portability.py` | source | Portability/backup layer for session stores (export, import, relocation) | Lets sessions survive profile moves and installs | moves: ev0_state.py;ev0_constants.py |
| `ev0_state_schema.py` | source | SQLite schema definitions + migrations for the session store | Keeps the DB schema versioned and migratable | ev0_state.py |
| `ev0_state_search.py` | source | FTS5 search layer over the session store | Powers /search and session picker; SQLite-side, no external indexer | ev0_state.py |
| `ev0_time.py` | source | Time helpers (UTC stamps, duration parsing) | Consistent time handling across scheduler/cron/session code | cron/scheduler.py;ev0_constants.py |
