# tests/ + tests-js/ + evals/ — the test suites

The test suites — `tests/` (Python, ~17k tests; per-file subprocess isolation via run_tests_parallel), `evals/`, conformance/integration/stress. `3v0/tests/` covers the sovereign core. Run only via `scripts/run_tests.sh`.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `evals/compaction/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `evals/compaction/fixtures.py` | source | Transcript fixtures for the compaction eval harness. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/compaction/policies.py` | source | Compaction policy matrix. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/compaction/report.py` | source | Render a compaction-eval scorecard as a terminal table + markdown. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/compaction/results/SCORECARD-2026-08-15.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `evals/compaction/results/codex-arm-2026-08-15/acp.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `evals/compaction/results/codex-arm-2026-08-15/gui.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `evals/compaction/results/codex-arm-2026-08-15/prmerge.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `evals/compaction/results/codex-arm-2026-08-15/sweep.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `evals/compaction/runner.py` | source | Compaction eval runner. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/compaction/scripts/build_html_report.py` | source | Build a self-contained HTML report comparing compaction runs. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/compaction/scripts/codex_arm.py` | source | Run the codex CLI as an eval arm on the same transcripts + question banks. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/compaction/scripts/reconstruct_lineage.py` | source | Reconstruct the full uncompacted transcript of a session LINEAGE. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/compaction/scripts/replay_lineage.py` | source | Replay a ~500K-token prefix of a reconstructed lineage through compaction. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/compaction/test_region_scoping.py` | test | Region-scoping tripwire: the summarizer must only see the compacted region. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `evals/readtool/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `evals/readtool/fixtures.py` | source | Hostile-workspace fixture generator for the read-tool eval. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/readtool/report.py` | source | Compare read-tool eval result sets (baseline vs feature labels). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/readtool/results/.gitignore` | asset | File `.gitignore` | Repository content; see related files / area page for the enclosing subsystem |  |
| `evals/readtool/results/SUMMARY.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `evals/readtool/runner.py` | source | Run the read-tool eval through the REAL Hermes AIAgent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `evals/readtool/tasks.py` | source | Task battery for the read-tool eval. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `tests-js/allow-scripts-sync.test.ts` | frontend-ts | TypeScript module `allow-scripts-sync.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `tests-js/assistant-ui-tap-compat.test.ts` | frontend-ts | TypeScript module `assistant-ui-tap-compat.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `tests-js/bootstrap-installer-stage-timer.test.ts` | frontend-ts | TypeScript module `bootstrap-installer-stage-timer.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `tests-js/desktop-mac-entitlements.test.ts` | frontend-ts | TypeScript module `desktop-mac-entitlements.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `tests-js/eslint.config.mjs` | asset | File `eslint.config.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `tests-js/package-json-lazy-deps.test.ts` | frontend-ts | TypeScript module `package-json-lazy-deps.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `tests-js/package.json` | build | Node package manifest | Declares JS workspace deps + scripts |  |
| `tests-js/react-dom-pair-compat.test.ts` | frontend-ts | TypeScript module `react-dom-pair-compat.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `tests-js/tsconfig.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `tests-js/vitest.config.ts` | frontend-ts | TypeScript module `vitest.config.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `tests/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/conftest.py` | test | Shared fixtures for tests/acp. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_approval_isolation.py` | test | Tests for GHSA-96vc-wcxf-jjff and GHSA-qg5c-hvr5-hjgr. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_auth.py` | test | Tests for acp_adapter.auth — provider detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_edit_approval.py` | test | Tests for ACP pre-edit approval gating. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_entry.py` | test | Tests for acp_adapter.entry startup wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_events.py` | test | Tests for acp_adapter.events — callback factories for ACP notifications. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_mcp_e2e.py` | test | End-to-end tests for ACP MCP server registration and tool-result reporting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_named_provider_catalogs.py` | test | Tests for named user-defined provider entries in the ACP model selector. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_permissions.py` | test | Tests for acp_adapter.permissions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_ping_suppression.py` | test | Tests for acp_adapter.entry._BenignProbeMethodFilter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_server.py` | test | Tests for acp_adapter.server — HermesACPAgent ACP server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_session.py` | test | Tests for acp_adapter.session — SessionManager and SessionState. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_session_db_private_access.py` | test | Tests for the update_session_meta fix. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_session_provenance.py` | test | Tests for ACP session-provenance derivation (issue #33617). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp/test_tools.py` | test | Tests for acp_adapter.tools — tool kind mapping and ACP content building. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp_adapter/test_acp_commands.py` | test | Python module `test_acp_commands.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp_adapter/test_acp_images.py` | test | Python module `test_acp_images.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp_adapter/test_acp_logging_redaction.py` | test | ACP adapter stderr logging must go through RedactingFormatter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp_adapter/test_acp_mcp_discovery.py` | test | Behavioral regression tests for ACP background MCP discovery + late-refresh. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/acp_adapter/test_detect_provider_entra.py` | test | Regression tests for ACP adapter detection under Azure Foundry Entra ID. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/__init__.py` | test | Pytest helpers for LSP-related tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/_mock_lsp_server.py` | test | A minimal in-process LSP server used by tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_backend_gate.py` | test | Integration test: LSP layer is skipped on non-local backends. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_broken_set.py` | test | Tests for the broken-set short-circuit added to handle outer-timeout failures. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_client_e2e.py` | test | End-to-end client tests against the in-process mock LSP server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_delta_key.py` | test | Tests for cross-edit LSP delta filtering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_diagnostics_field.py` | test | Tests for the ``lsp_diagnostics`` field on WriteResult / PatchResult. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_eventlog.py` | test | Tests for the structured logging dedup model. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_install_and_lint_fixes.py` | test | Tests for follow-up fixes to the LSP integration (PR after #24168). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_lifecycle.py` | test | Tests for service-singleton lifecycle: atexit handler, idempotent shutdown. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_powershell_server.py` | test | Tests for the PowerShellEditorServices (PSES) server registration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_protocol.py` | test | Tests for the LSP protocol framing layer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_reporter.py` | test | Tests for the diagnostic reporter (formatting layer). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_service.py` | test | Tests for the synchronous LSPService wrapper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_shell_linter_lsp_skip.py` | test | Skip the per-file shell linter when LSP will handle the same file. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_stale_diagnostics.py` | test | Regression tests for the "ghost diagnostics" staleness bug. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/lsp/test_workspace.py` | test | Tests for workspace + project-root resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_account_usage.py` | test | Python module `test_account_usage.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_adapter.py` | test | Tests for agent/anthropic_adapter.py — Anthropic Messages API adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_billing_guidance.py` | test | Tests for the Anthropic-subscription branch of | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_keychain.py` | test | Tests for Bug #12905 fixes in agent/anthropic_adapter.py — macOS Keychain support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_kimi_signed_thinking_replay.py` | test | Kimi-family endpoints don't need thinking blocks stripped on replay; DeepSeek does. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_kwargs_sanitize.py` | test | Tests for sanitize_anthropic_kwargs (#31673). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_mcp_prefix_strip.py` | test | Tests for GH-25255: Anthropic OAuth ``mcp__`` tool-name round-trip. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_oauth_pkce.py` | test | Regression tests for the Anthropic OAuth PKCE flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_oauth_ua_prefix.py` | test | Regression tests for the OAuth User-Agent header in anthropic_adapter.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_output_field_leak.py` | test | Regression: output-only SDK fields must not leak into Anthropic request input. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_request_blank_block_guard.py` | test | Regression: the final Anthropic request must carry no blank text block. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_request_client_reuse.py` | test | Per-request Anthropic wire client reuse across sequential LLM calls. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_thinking_block_order.py` | test | Regression test for the Anthropic interleaved thinking-block 400. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_token_scope_isolation.py` | test | Regression tests: resolve_anthropic_token() must honour the profile secret scope. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_anthropic_whitespace_text_blocks.py` | test | Regression: whitespace-only text blocks must be coerced, not sent verbatim. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_api_content_sidecar.py` | test | Tests for the ``api_content`` sidecar ("persist what you send"). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_arcee_trinity_overrides.py` | test | Tests for Arcee Trinity Large Thinking per-model overrides. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_async_token_accounting.py` | test | Async token accounting — SessionDB background writer queue. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_async_utils.py` | test | Tests for agent.async_utils.safe_schedule_threadsafe. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_aux_progress_streaming.py` | test | Tests for the auxiliary forward-progress streaming layer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_anthropic_pool_fallback_regression.py` | test | Regression: _try_anthropic() must fall back to the legacy token resolver | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client.py` | test | Tests for agent.auxiliary_client resolution chain, provider overrides, and model overrides. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client_anthropic_custom.py` | test | Tests for agent.auxiliary_client._try_custom_endpoint's anthropic_messages branch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client_azure_foundry.py` | test | Tests for auxiliary client routing of the ``azure-foundry`` provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client_base_url_host_validation_52608.py` | test | Regression tests for issue #52608. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client_bootstrap_skew.py` | test | Regression for #64333 — auxiliary client must survive a version-skewed | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client_proxy_env.py` | test | Regression guard: auxiliary OpenAI clients must use env-only proxy policy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client_resolve_dedup.py` | test | Tests for resolve_provider_client fall-through log dedup (salvage #56283). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client_ssl_verify.py` | test | Regression: auxiliary-client keepalive httpx client must honor custom CA bundles. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_client_xai_oauth_recovery.py` | test | Tests for xAI OAuth 403 error recovery in auxiliary_client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_compression_timeout_floor.py` | test | Regression tests for the compression-scoped auxiliary timeout floor (#54915). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_concurrency.py` | test | Tests for per-task concurrency limiting on auxiliary LLM calls (#23324). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_config_bridge.py` | test | Tests for auxiliary model config bridging — verifies that config.yaml values | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_explicit_base_anthropic.py` | test | Tests for resolve_provider_client's ``custom`` + ``explicit_base_url`` branch | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_explicit_cancellation.py` | test | Deterministic cross-thread cancellation tests for compression aux transports. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_main_first.py` | test | Regression tests for the ``auto`` → main-model-first policy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_named_custom_providers.py` | test | Tests for named custom provider and 'main' alias resolution in auxiliary_client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_relay.py` | test | Python module `test_auxiliary_relay.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_runtime_cache_key.py` | test | Regression coverage for implicit live-runtime auxiliary cache keys. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_transient_retry.py` | test | Transient-transport retry count + per-model client-cache isolation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_transport_autodetect.py` | test | Tests for transport auto-detection in agent.auxiliary_client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_auxiliary_user_default_headers.py` | test | Tests for user-configured ``model.default_headers`` in the auxiliary client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_azure_identity_adapter.py` | test | Tests for the Microsoft Entra ID adapter (agent/azure_identity_adapter.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_backend_identity.py` | test | Owner-level tests for agent.backend_identity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_background_review_usage.py` | test | Background-review usage attribution (issue #87250). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_battery.py` | test | Behavior tests for the status-bar battery helper (agent/battery.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_bedrock_1m_context.py` | test | Tests for the 1M-context beta header on AWS Bedrock Claude models. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_bedrock_adapter.py` | test | Tests for the AWS Bedrock Converse API adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_bedrock_empty_text_blocks.py` | test | Regression tests for Bedrock Converse empty/whitespace text block rejection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_bedrock_integration.py` | test | Integration tests for the AWS Bedrock provider wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_bedrock_interrupt_post_worker.py` | test | Regression: /stop must not be swallowed on the Bedrock streaming path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_billing_links.py` | test | Tests for provider-agnostic billing recovery links (agent/billing_links.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_billing_unverified_carrythrough.py` | test | #82154: an unverified billing verdict must carry its ambiguity through | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_billing_usage.py` | test | Tests for the shared dollar usage model (agent/billing_usage.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_billing_view.py` | test | Unit tests for the Phase 2b Remote Spending core + HTTP client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_bot_profile_prompt_isolation.py` | test | Regression: a bot profile's system prompt must reflect ITS OWN skills/home, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_bounded_response.py` | test | Tests for bounded reads of streaming HTTP error response bodies. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_budget_reasoning_details_exclusion.py` | test | Regression tests for #73298 (second site): the tail-budget walk must not | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_cache_disabled_on_stubs.py` | test | Regression for #76085: prompt_caching.cache_ttl off on stub policy paths. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_canon_args_memo_parity.py` | test | Byte-parity + complexity proof for the memoized send-path tool-call | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_cascading_interrupt_6600.py` | test | Regression guard for the cascading-interrupt hang (PR #6600). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_chat_completion_helpers_provider_sort.py` | test | Python module `test_chat_completion_helpers_provider_sort.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_cjk_token_estimation.py` | test | Python module `test_cjk_token_estimation.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_close_interrupted_tool_sequence.py` | test | Regression tests for ``close_interrupted_tool_sequence`` (#48879 follow-up). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_codex_app_server_event_bridge.py` | test | Regression tests for the codex_app_server → Hermes UI event bridge. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_codex_app_server_persist.py` | test | Regression for #49225 — codex app-server turns must reach the session DB | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_codex_cloudflare_headers.py` | test | Regression guard: Codex Cloudflare 403 mitigation headers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_codex_gpt55_autoraise_notice.py` | test | Regression tests for the Codex gpt-5.x autoraise notice gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_codex_request_transport_diagnostics.py` | test | Diagnostics for Codex Responses transport failures. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_codex_responses_adapter.py` | test | Python module `test_codex_responses_adapter.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_codex_runtime_live_events.py` | test | Regression tests for live Codex app-server events. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_codex_ttfb_watchdog.py` | test | Regression tests for the Codex time-to-first-byte (TTFB) watchdog. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_coding_context.py` | test | Tests for agent.coding_context — RuntimeMode seam, resolver, toolset, git probe. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_command_token_source.py` | test | ``key_cmd``: derive a provider API key by running a command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compaction_anti_thrash.py` | test | The anti-thrashing guard must actually fire. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compaction_redaction_boundaries.py` | test | Strict redaction at every compaction text boundary (issue #43666 item 2). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compress_context_progress_timeout.py` | test | Progress-aware timeout around in-agent compress_context (#72016). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compress_focus.py` | test | Tests for focus_topic flowing through the compressor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compress_signal_leak.py` | test | Invariant: stale signal leak between consecutive compress_context calls. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressed_summary_metadata.py` | test | Regression tests for the compressed-summary metadata flag (#38389). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_adoption_preserves_live_tail.py` | test | Regression: preflight durable-snapshot adoption must not drop the live | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_anti_thrash_persistence.py` | test | Anti-thrash state must survive process restarts (#54923). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_anti_thrash_recovery.py` | test | Anti-thrash recovery: the tripped guard must not be permanent (#14694). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_attempt_telemetry.py` | test | Python module `test_compression_attempt_telemetry.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_concurrent_fork.py` | test | Regression: prevent transcript fork when two paths compress the same session_id. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_count_warning_36908.py` | test | Regression for #36908: the repeated-compression warning must reach the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_fallback_budget.py` | test | Tests for #62452 — compression fallback timeout independence + escalating | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_interrupt_protection.py` | test | Regression for #23975: context compression must survive a mid-flight | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_logging_session_context.py` | test | Regression: compaction must move the LOGGING session context with the id. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_max_attempts_config.py` | test | compression.max_attempts — config-driven compression retry cap. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_orphan_recovery.py` | test | Recovery for legacy compression parents with no continuation child. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_progress.py` | test | Regression: detect compression progress by tokens, not just rows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_review_76354.py` | test | Regressions for the #76354 review of the compression timeout architecture. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_rotation_state.py` | test | Compression rotation hardening — state-loss fixes at the compaction boundary. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_small_ctx_threshold_floor.py` | test | Compression hygiene: small-context threshold floor, reasoning-trace | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compression_worker_isolation_76354.py` | test | Regressions for #76354 review F3/F4/F5 — worker isolation, durable lease | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_actionable_tail_anchor.py` | test | Regression tests for blank user echoes displacing actionable compaction state. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_assistant_tail_anchor.py` | test | Regression coverage for #29824 — the WebUI session viewer (and TUI | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_historical_media.py` | test | Tests for post-compression historical-media stripping. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_image_tokens.py` | test | Tests for image-token accounting in the context compressor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_media_stripping.py` | test | Tests for MEDIA directive stripping in context compaction (#14665). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_tail_cut_oob_fix.py` | test | Regression test for #75588 — short tool-only suffix can make context | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_tail_cut_tool_pair_floor.py` | test | Regression coverage: the minimum-progress floor must not split a tool group. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_tool_call_budget.py` | test | Regression tests for tool_call envelope accounting in the compression | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_compressor_zero_user_guard.py` | test | Regression coverage for #58753 — compression could drop the only | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_breakdown.py` | test | Tests for live session context breakdown. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_compressor.py` | test | Tests for agent/context_compressor.py — compression logic, thresholds, truncation fallback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_compressor_cross_session_guard.py` | test | Tests for cross-session _previous_summary contamination bug (#38788). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_compressor_session_end_clears_state.py` | test | Tests for on_session_end() clearing all per-session compressor state. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_compressor_summary_continuity.py` | test | Regression tests for iterative context-summary continuity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_compressor_temporal_anchoring.py` | test | Tests for temporal anchoring in context-compaction summaries. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_compressor_zero_user_provenance.py` | test | Regression coverage for zero-user compaction integrity (#64539). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_engine.py` | test | Tests for the ContextEngine ABC and plugin slot. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_engine_host_contract.py` | test | Regressions for the context-engine host contract. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_engine_on_turn_complete_usage.py` | test | Integration test: ``finalize_turn`` forwards the turn's real usage to the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_engine_select_context.py` | test | Tests for the per-turn ``ContextEngine.select_context()`` hook. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_references.py` | test | Python module `test_context_references.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_refs_concurrent.py` | test | Tests for concurrent @-reference expansion in context_references. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_context_route_mismatch.py` | test | Tests for agent_init._context_route_mismatch context-pin scoping. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_copilot_acp_client.py` | test | Focused regressions for the Copilot ACP shim safety layer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_copilot_acp_deprecation.py` | test | Tests for gh-copilot CLI deprecation detection and GitHub Models Azure URL mapping. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool.py` | test | Tests for multi-credential runtime pooling and rotation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_deferred_refresh.py` | test | Thread-safety of the deferred single-use-token refresh path (#71775). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_key_rotation.py` | test | Tests for credential pool upsert — key rotation clears exhaustion state. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_lease_refresh_reselect.py` | test | acquire_lease must re-select after a deferred single-use-token refresh. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_no_entries_log_throttle.py` | test | Regression: the credential-pool "no available entries" INFO line must be | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_oat_authtype.py` | test | Regression tests for #63737: sk-ant-oat pool entries are OAuth. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_oauth_writethrough.py` | test | Regression tests for credential-pool OAuth refresh write-through to root. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_provider_boundary.py` | test | Credential pools must never cross provider or custom-endpoint boundaries. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_quarantine_locking.py` | test | Codex/nous quarantine paths must mutate self._entries under the lock. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_routing.py` | test | Tests for credential pool preservation through turn config and 429 recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_sole_cooldown.py` | test | Sole-credential cooldown: a pool with nothing to rotate to should not bench | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credential_pool_unmatched_rotation_bound.py` | test | #70401: the unmatched-identity rotation branch in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credits_cold_start.py` | test | Tests for cold-start credits hydration at session open. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credits_fixture_snapshot.py` | test | Tests for _snapshot_from_credits_state — the dev-fixture /usage renderer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credits_policy.py` | test | Tests for evaluate_credits_notices — pure threshold reconciliation policy (L4.1). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credits_tracker.py` | test | Tests for agent.credits_tracker — CreditsState + parse_credits_headers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_credits_view.py` | test | Tests for the /credits command — shared view core + gateway handler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_cron_inline_api_call_62151.py` | test | Regression guard for #62151 — gateway cron must not wedge on the 2nd+ call. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_crossloop_client_cache.py` | test | Tests for cross-loop client cache isolation fix (#2681). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_curator.py` | test | Tests for agent/curator.py — orchestrator, idle gating, state transitions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_curator_activity.py` | test | Regression tests for curator skill activity timestamps. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_curator_backup.py` | test | Tests for agent/curator_backup.py — snapshot + rollback of the skills tree. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_curator_classification.py` | test | Tests for the curator consolidated-vs-pruned classifier. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_curator_reports.py` | test | Tests for the curator per-run report writer (run.json + REPORT.md). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_cursor_optimizations_parity.py` | test | Byte-parity + benchmark harness for the per-iteration cursor optimizations. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_custom_pool_mismatch_guard.py` | test | Regression tests for the credential-pool provider-mismatch guard with | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_custom_provider_ca_probes.py` | test | Custom-provider TLS settings must reach the /models and pricing probes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_custom_provider_extra_body.py` | test | Python module `test_custom_provider_extra_body.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_custom_provider_extra_body_matching.py` | test | Tests for custom-provider model matching (extra_body / service_tier drop bug). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_custom_providers_vision.py` | test | Tests for custom_providers[].models[].supports_vision override (#41036). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_deadline.py` | test | Tests for agent/deadline.py — the unified deadline layer (#85125). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_deepseek_anthropic_thinking.py` | test | Regression guard: preserve thinking blocks on DeepSeek's /anthropic endpoint. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_direct_provider_url_detection.py` | test | Python module `test_direct_provider_url_detection.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_display.py` | test | Tests for agent/display.py — build_tool_preview() and inline diff previews. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_display_emoji.py` | test | Tests for get_tool_emoji in agent/display.py — skin + registry integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_display_todo_progress.py` | test | Tests for get_cute_tool_message todo progress display. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_display_tool_failure.py` | test | Tests for _detect_tool_failure + _trim_error + get_cute_tool_message | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_empty_tool_name_loop_dampening.py` | test | Regression for #47967 — empty-name phantom tool calls. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_endpoint_blackhole.py` | test | Tests for short-circuiting probes to endpoints that blackhole TCP connects. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_engine_preflight_wire.py` | test | Engine-driven sub-threshold preflight maintenance (#20316, salvaged from #20424). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_error_classifier.py` | test | Tests for agent.error_classifier — structured API error classification. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_external_skills.py` | test | Tests for external skill directories (skills.external_dirs config). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_external_skills_dirs_cache.py` | test | Guards for ``get_external_skills_dirs`` mtime-based memo. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_failover_identity.py` | test | Tests for system-prompt model-identity sync across provider failover. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_file_safety.py` | test | Tests for agent/file_safety.py read guards — env file blocking. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_file_safety_container_mirror.py` | test | Tests for the container-context sandbox-mirror guard (#32049 follow-up). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_file_safety_credentials.py` | test | Tests for HERMES_HOME credential-file read blocking in file_safety. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_file_safety_cross_profile.py` | test | Tests for the cross-Hermes-profile write guard in agent/file_safety. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_file_safety_sandbox_mirror.py` | test | Tests for the sandbox-mirror write guard in agent/file_safety. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_file_safety_session_state.py` | test | Session transcript stores are read-only to agent file tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_gateway_turn_sidecar.py` | test | Gateway must-deliver notes on the current user message. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_gemini_fast_fallback.py` | test | Regression tests for #11314 — credential-pool rotation vs. fallback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_gemini_free_tier_gate.py` | test | Tests for Gemini free-tier detection and blocking. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_gemini_native_adapter.py` | test | Tests for the native Google AI Studio Gemini adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_gemini_schema.py` | test | Tests for agent.gemini_schema — OpenAI→Gemini tool parameter translation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_gemini_standard_key_guidance.py` | test | Tests for Gemini legacy Standard-key 401 guidance. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_ghost_skill_pruning.py` | test | Ghost-skill defense tests (#32106, salvage of PR #44166). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_hygiene_timeout_cooldown_isolation.py` | test | Hygiene idle-timeout cooldowns must not block the in-agent compressor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_i18n.py` | test | Tests for agent.i18n -- catalog parity, fallback, language resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_idle_compaction.py` | test | Tests for the opt-in idle-triggered compaction policy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_idle_compaction_lock_and_guards.py` | test | Idle-triggered compaction: interaction with the compression guards. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_image_gen_registry.py` | test | Tests for agent/image_gen_registry.py — provider registration & active lookup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_image_routing.py` | test | Tests for agent/image_routing.py — the per-turn image input mode decision. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_insights.py` | test | Tests for agent/insights.py — InsightsEngine analytics and reporting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_intent_ack_continuation.py` | test | Intent-ack continuation gate + detector behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_interrupt_compat.py` | test | Compatibility contract for explicit hard-stop producers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_jiter_preload.py` | test | Python module `test_jiter_preload.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_kanban_stop.py` | test | Tests for the kanban worker turn-end stop guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_kimi_coding_anthropic_thinking.py` | test | Kimi / Moonshot thinking behavior on the Anthropic-Messages wire. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_last_total_tokens.py` | test | Test that last_total_tokens is correctly set by ContextCompressor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_learn_prompt.py` | test | Tests for /learn — open-ended skill distillation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_learning_graph.py` | test | Behavior contracts for the learning-graph assembler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_learning_graph_render.py` | test | Behavior contracts for the terminal Star Map renderer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_learning_mutations.py` | test | Behavior contracts for journey node edit/delete (agent.learning_mutations). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_lmstudio_reasoning.py` | test | Reasoning-effort resolution for LM Studio. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_local_probe_disk_cache.py` | test | Tests for the local-endpoint probe disk L2 cache in agent/model_metadata. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_local_stream_timeout.py` | test | Tests for local provider stream read timeout auto-detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_manual_compression_feedback.py` | test | Behavioral coverage for manual compression status messages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_markdown_tables.py` | test | Tests for `agent.markdown_tables.realign_markdown_tables`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_async_sync.py` | test | Regression guard: end-of-turn memory sync must not block the turn. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_boundary_commit.py` | test | Tests for MemoryManager.commit_session_boundary_async. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_provider.py` | test | Tests for the memory provider interface, manager, and builtin provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_provider_unavailable_warning.py` | test | Regression tests for NousResearch/hermes-agent#2765. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_recall_indicator.py` | test | MemoryManager.describe_recall — the deterministic recall indicator. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_session_switch.py` | test | Tests for the on_session_switch hook and session_id propagation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_skill_scaffolding.py` | test | MemoryManager strips slash-skill scaffolding for every provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_user_id.py` | test | Tests for per-user memory scoping via user_id threading. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_memory_write_bridge.py` | test | Behavior tests for the built-in memory → external provider bridge. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_message_content.py` | test | Python module `test_message_content.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_message_metadata.py` | test | Python module `test_message_metadata.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_message_sanitization_policy.py` | test | Tests for the single-owner call_id + reasoning_content policies. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_micro_compaction.py` | test | Tests for per-turn micro-compaction in ``ContextCompressor``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_minimax_auxiliary_url.py` | test | Tests for Anthropic-to-OpenAI auxiliary URL normalization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_minimax_provider.py` | test | Tests for MiniMax provider hardening — context lengths, thinking, catalog, beta headers, transport. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_aggregator_cache_control.py` | test | Regression test: the MoA aggregator's one-shot synthesis call | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_aggregator_cost_slot.py` | test | Tests for MoA aggregator-slot exposure used by session cost accounting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_cold_start_cache_66793.py` | test | Regression tests for MoA cold-start caching (#66793). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_context_max_tokens.py` | test | Regression test for aggregate_moa_context's reference/aggregator max_tokens split. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_observability_bridge.py` | test | Per-advisor MoA metrics crossing the plugin-hook boundary. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_prepared_request_client_swap.py` | test | `_moa_prepared_request` must never reach a client that cannot consume it. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_progress.py` | test | Tests for the MOA progress indicator added in issue #59546. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_quiet_reference_output.py` | test | Regression coverage for machine-readable MoA quiet output. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_reasoning_effort.py` | test | Python module `test_moa_reasoning_effort.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_reference_system_prompt.py` | test | Test that the MoA reference system prompt contains explicit warnings | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_slot_api_mode.py` | test | Tests for MoA slot_runtime api_mode propagation (issue #54379). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_slot_max_tokens.py` | test | Tests for per-slot max_tokens in MoA reference calls. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_switch_api_mode.py` | test | Regression test for MoA primary-call routing on persisted preset switches. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moa_trace_streamed_capture.py` | test | Tests for MoA trace aggregator-output capture across streaming modes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_model_extra_type_guard.py` | test | Regression test for PR #15157: non-dict ``model_extra`` must not crash | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_model_metadata.py` | test | Tests for agent/model_metadata.py — token estimation, context lengths, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_model_metadata_local_ctx.py` | test | Tests for _query_local_context_length and the local server fallback in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_model_metadata_ssl.py` | test | Tests for _resolve_requests_verify() env var precedence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_models_dev.py` | test | Tests for agent.models_dev — models.dev registry integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_models_dev_meta_mapping.py` | test | Meta Model API maps to the models.dev 'meta' provider id (context/pricing). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_moonshot_schema.py` | test | Tests for Moonshot/Kimi flavored-JSON-Schema sanitizer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_non_stream_stale_timeout.py` | test | Tests for the non-stream stale-call detector context estimator. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_none_deref_guards.py` | test | Regression tests for None-dereference guards on ``.get(key, "").method()`` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_nous_credits_gauge.py` | test | Tests for the Nous-credits subscription % gauge in build_nous_credits_snapshot. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_nous_credits_snapshot.py` | test | Tests for build_nous_credits_snapshot (L6-A, magnitudes-only). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_nous_oauth_401_guidance.py` | test | Tests for the Nous OAuth 401 actionable-guidance branch in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_nous_portal_anthropic_wire.py` | test | Nous Portal ``anthropic/*`` models route on the native Messages wire. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_nous_rate_guard.py` | test | Tests for agent/nous_rate_guard.py — cross-session Nous Portal rate limit guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_onboarding.py` | test | Tests for agent/onboarding.py — contextual first-touch hint helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_oneshot.py` | test | Tests for agent.oneshot — shared one-off (stateless) LLM requests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_openrouter_response_cache.py` | test | Tests for OpenRouter response caching header injection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_org_skill_namespace.py` | test | M2 org-skill namespace: token-gated resolution, provenance, collisions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_outbound_webhooks.py` | test | Tests for the outbound webhook dispatcher (agent.outbound_webhooks). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_pet_engine.py` | test | Tests for the petdex pet engine (agent/pet/*). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_pet_generate.py` | test | Tests for pet generation: deterministic atlas ops, store register, orchestration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_platform_hint_desktop.py` | test | System-prompt assembly for the desktop chat surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_platform_hint_overrides.py` | test | Tests for per-platform prompt-hint overrides (config.yaml → platform_hints). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_plugin_context_references.py` | test | Tests for plugin context reference provider API (Issue #26193). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_plugin_llm.py` | test | Unit tests for the plugin LLM facade (``agent.plugin_llm``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_plugin_llm_task_routing.py` | test | Tests for plugin auxiliary-task routing via ``ctx.llm.complete(task=...)``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_plugin_prompt_sections.py` | test | Python module `test_plugin_prompt_sections.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_portal_tags.py` | test | Tests for agent.portal_tags — Nous Portal request tag contract. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_post_compression_trim.py` | test | A successful compaction hands allocator pages back to the OS. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_pre_compress_memory_context.py` | test | Behavior contracts for memory-provider context in compression prompts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_preflight_compression_gate.py` | test | Regression tests for issue #27405. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_preflight_lock_defer.py` | test | Preflight lock-defer must not arm the insufficient-progress blocker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_proactive_prune_config.py` | test | compression.proactive_prune_* — config parse seam for the proactive prune. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_proactive_prune_restart_safety.py` | test | Restart-safety regressions for proactive tool-result pruning. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_proactive_tool_result_pruning.py` | test | Tests for proactive tool-result pruning. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_probe_cache_followups.py` | test | Tests for probe-cache follow-ups on the #29988/#37595/#50572 salvage. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_profile_home_override_precedence.py` | test | Regression: multiplex gateway profile scoping + full-prompt wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_prompt_builder.py` | test | Tests for agent/prompt_builder.py — context scanning, truncation, skills index. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_prompt_cache_boundary.py` | test | Builder-declared stable-prefix cache boundaries (#81867). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_prompt_cache_scope.py` | test | Tests for the rotation-stable prompt-cache scope (issue #79017). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_prompt_cache_ttl_propagation.py` | test | #84733: prompt-cache TTL/prefix propagation into MoA/aux paths + failover re-preflight. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_prompt_caching.py` | test | Tests for agent/prompt_caching.py — Anthropic cache control injection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_protected_tail_pressure_61932.py` | test | Algorithmic reproduction and regression for issue #61932. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_proxy_and_url_validation.py` | test | Tests for malformed proxy env var and base URL validation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_pydantic_dump_warning_leak.py` | test | Serializer-warning leak regression tests (#82xxx). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_rate_limit_tracker.py` | test | Tests for agent.rate_limit_tracker — header parsing and formatting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_reactions.py` | test | Behavior tests for the token-free reaction detector. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_reasoning_stale_timeout_floor.py` | test | Regression tests for the reasoning-model stale-timeout floor (issue #52217). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_reasoning_summaries.py` | test | Reasoning summary-part boundary repair (agent/reasoning_summaries.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_redact.py` | test | Tests for agent.redact -- secret masking in logs and output. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_reference_handoff_active_turn.py` | test | Regression coverage for #80622: a reference-only compaction handoff must | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_refine_focus.py` | test | Tests for the /refine focus parameter on spawn_background_review_thread. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_relay_llm.py` | test | Tests for the core Relay-managed physical LLM attempt adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_relay_nested_execution.py` | test | Regression tests for nested managed Relay execution (#77244). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_relay_runtime_bounded_scope_ops.py` | test | Bounded native scope operations in the Relay session coordinator. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_relay_scope_pop_metadata.py` | test | Regression for #78993: scope.pop metadata kwarg on older NeMo Relay. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_relay_session_segments.py` | test | Session-span segmentation for continuous sessions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_relay_tools.py` | test | Tests for the core Relay-managed Hermes tool adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_repetition_guard.py` | test | Unit tests for the truncated-response repetition guard (issue #86581). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_replay_budget_accounting.py` | test | Tests for provider-aware replay-field accounting in tail-budget walks (#73624). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_replay_cleanup.py` | test | Tests for agent.replay_cleanup — shared replay-tail sanitizers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_request_client_reuse.py` | test | Per-request OpenAI wire client reuse across sequential LLM calls. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_restore_primary_pool_reselect.py` | test | Test that _restore_primary_runtime re-selects from the credential pool | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_resume_stale_active_task.py` | test | Regression coverage for #35344: a resumed session must not let a stale | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_rotation_flush_persisted_boundary_68196.py` | test | Regression (#68196): rotating preflight compression must not re-append the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_runtime_cwd.py` | test | Tests for agent/runtime_cwd.py — the single source of truth for the agent working directory. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_save_url_image.py` | test | Direct tests for ``agent.image_gen_provider.save_url_image`` (#26942). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_secret_scope.py` | test | Tests for the profile-scoped credential primitive (Workstream A / Phase 2). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_secret_scope_tier1_migration.py` | test | Regression tests for the Tier-1 core-gateway secret-scope migration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_send_path_history_isolation.py` | test | Send-path transforms must never write through into persisted history. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_sequential_tool_interrupt.py` | test | Sequential tool execution must abandon the wait when the user interrupts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_session_activity.py` | test | Unit tests for the shared session activity observation contract. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_session_rotation_flush_cold_resume_68454.py` | test | Regression (#68454): /new, /resume, /branch must not re-append cold-resumed | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_set_runtime_main_custom_provider.py` | test | Regression test: set_runtime_main() must pass base_url/api_key/api_mode | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_shell_hooks.py` | test | Tests for the shell-hooks subprocess bridge (agent.shell_hooks). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_shell_hooks_consent.py` | test | Consent-flow tests for the shell-hook allowlist. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_shell_hooks_tree_kill.py` | test | Process-tree cleanup for timed-out shell hooks (port of openai/codex#37527). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skill_bundles.py` | test | Tests for agent/skill_bundles.py — YAML-defined skill bundles. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skill_commands.py` | test | Tests for agent/skill_commands.py — skill slash command scanning and platform filtering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skill_commands_reload.py` | test | Tests for ``agent.skill_commands.reload_skills``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skill_invocation_description.py` | test | describe_skill_invocation() — recovering what the user typed from a /skill turn. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skill_todo_retention_parity.py` | test | Retention parity at the compaction boundary (#84718). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skill_utils.py` | test | Tests for agent/skill_utils.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skills_guidance_content_filter.py` | test | SKILLS_GUIDANCE must not carry the phrasing Anthropic's content filter rejects. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skip_background_review.py` | test | Tests for the skip_background_review constructor flag. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_skip_memory_store_65429.py` | test | Regression test for issue #65429. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_soul_md_profile_isolation.py` | test | Regression (#50233, SOUL.md half): a profile agent's SOUL.md must load from | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_ssl_ca_guard.py` | test | Tests for the preventive SSL CA bundle guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_ssl_verify.py` | test | Tests for agent.ssl_verify.resolve_httpx_verify. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_stale_replay_prune.py` | test | Tests for stale codex_reasoning_items pruning during compaction (#71058). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_stream_chunk_byte_estimate.py` | test | Tests for _estimate_chunk_bytes — the cheap per-chunk stream size proxy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_stream_read_timeout_floor.py` | test | Stream read timeout must never preempt the stale-stream detector. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_stream_single_writer_guard.py` | test | Regression tests for the best-effort single-writer fence accessors. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_streaming_context_scrubber.py` | test | Unit tests for StreamingContextScrubber (agent/memory_manager.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_subagent_lifecycle.py` | test | Contract tests for the public plugin subagent lifecycle API. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_subagent_progress.py` | test | Tests for subagent progress relay (issue #169). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_subagent_stop_hook.py` | test | Tests for the subagent_stop hook event. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_subdirectory_hints.py` | test | Tests for progressive subdirectory hint discovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_subdirectory_hints_tilde.py` | test | Regression tests for the home-directory RuntimeError bug. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_subprocess_env_guard.py` | test | Lint guard: no new raw ``os.environ.copy()`` spawn-env sites. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_subscription_view.py` | test | Tests for agent.subscription_view — the surface-agnostic /subscription core. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_summarize_tool_result_type_safety.py` | test | Type safety tests for _summarize_tool_result. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_summary_prefix_semantics.py` | test | Pin the semantics of SUMMARY_PREFIX so the compaction handoff doesn't | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_summary_prefix_tool_use.py` | test | Regression tests for the SUMMARY_PREFIX tool-use clause (#65848 class). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_summary_role_template_alternation.py` | test | Regression coverage: the compaction summary role must alternate against | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_surrogate_chokepoints.py` | test | Lone-surrogate chokepoint regression tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_synthetic_turn_display_kind.py` | test | A synthesized turn's row is typed when it is WRITTEN, not when it ends. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_system_prompt.py` | test | Tests for agent/system_prompt.py — context-file cwd wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_system_prompt_restore.py` | test | Tests for ``agent.conversation_loop._restore_or_build_system_prompt``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_think_scrubber.py` | test | Tests for StreamingThinkScrubber. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_thinking_timeout_guidance.py` | test | Tests for the reasoning-model thinking-timeout detection + guidance. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_thread_scoped_output.py` | test | Tests for agent.thread_scoped_output.thread_scoped_silence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_title_generator.py` | test | Tests for agent.title_generator — auto-generated session titles. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_tool_call_arg_no_redaction.py` | test | Regression test for #43083. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_tool_dispatch_helpers.py` | test | Tests for the tool-result message builder — focuses on the untrusted-content | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_tool_executor_checkpoint_paths.py` | test | Behavioral coverage for file-tool checkpoint path resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_tool_guardrails.py` | test | Pure tool-call guardrail primitive tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_tool_result_classification.py` | test | Tests for shared tool result classification helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_trace_upload.py` | test | Tests for agent.trace_upload — Hugging Face session-trace upload. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_transcription_registry.py` | test | Tests for agent/transcription_registry.py and agent/transcription_provider.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_tts_registry.py` | test | Tests for agent/tts_registry.py and agent/tts_provider.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_context.py` | test | Unit tests for the extracted turn prologue (``agent/turn_context.py``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_context_overflow_warning.py` | test | Tests for the silent-context-overflow warning (the fix for the bug where a | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_finalizer_cleanup_guard.py` | test | Regression test for #8049. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_finalizer_final_response_persistence.py` | test | Python module `test_turn_finalizer_final_response_persistence.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_finalizer_interrupt_alternation.py` | test | Regression test for #48879. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_finalizer_iteration_limit_exit.py` | test | Regression tests for iteration-limit exit normalization (#61631). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_overlap_tripwire.py` | test | note_turn_start / note_turn_persisted — the concurrent-turn tripwire. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_retry_state.py` | test | Unit tests for TurnRetryState (god-file Phase 1b). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_turn_summary.py` | test | Tests for per-turn accounting: summary formatter, collector, spinner flow, gating. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_unsupported_parameter_retry.py` | test | Regression tests for the generic unsupported-parameter detector in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_unsupported_temperature_retry.py` | test | Regression tests for the universal "unsupported temperature" retry in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_usage_pricing.py` | test | Python module `test_usage_pricing.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_verification_evidence.py` | test | Python module `test_verification_evidence.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_verification_evidence_fd_leak.py` | test | Regression: the verification-evidence ledger must close every connection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_verification_stop.py` | test | Python module `test_verification_stop.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_verification_stop_caching.py` | test | Verification-loop synthetic scaffolding must never reach durable session state. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_verify_hooks.py` | test | Unit tests for the verification-loop policy (agent/verify_hooks.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_vertex_adapter.py` | test | Tests for the Vertex AI adapter (agent/vertex_adapter.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_video_gen_registry.py` | test | Tests for agent/video_gen_registry.py — provider registration & active lookup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_vision_resolved_args.py` | test | Test that call_llm vision path passes resolved provider args, not raw ones. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/test_vision_routing_31179.py` | test | Regression tests for issue #31179. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_bedrock_transport.py` | test | Tests for the BedrockTransport. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_chat_completions.py` | test | Tests for the ChatCompletionsTransport. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_chat_completions_empty_tool_calls.py` | test | Tests for empty / null ``tool_calls`` stripping in ChatCompletionsTransport. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_codex_app_server_runtime.py` | test | Tests for the optional codex app-server runtime gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_codex_app_server_session.py` | test | Tests for CodexAppServerSession — drive turns through a mock client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_codex_event_projector.py` | test | Tests for CodexEventProjector — codex item/* events → Hermes messages list. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_codex_transport.py` | test | Tests for the ResponsesApiTransport (Codex). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_ev0_tools_mcp_server.py` | test | Tests for the hermes-tools-as-MCP server module surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_transport.py` | test | Tests for the transport ABC, registry, and AnthropicTransport. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/agent/transports/test_types.py` | test | Tests for agent/transports/types.py — dataclass construction + helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_assemble_review_comment.py` | test | Tests for scripts/ci/assemble_review_comment.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_classify_changes.py` | test | Tests for scripts/ci/classify_changes.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_e2e_screenshot_status.py` | test | Tests for scripts/ci/e2e_screenshot_status.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_emit_review_status.py` | test | Tests for scripts/ci/emit_review_status.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_list_os_marked_tests.py` | test | Tests for ``scripts/ci/list_os_marked_tests.py``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_live_comment.py` | test | Tests for scripts/ci/live_comment.py run selection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_lockfile_diff.py` | test | Tests for scripts/ci/lockfile_diff.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_publish_e2e_evidence.py` | test | Tests for scripts/ci/publish_e2e_evidence.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ci/test_timings_report.py` | test | Tests for scripts/ci/timings_report.py — generate_review_status(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/conftest.py` | test | Shared fixtures for CLI tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_bang_shell_mode.py` | test | Tests for `!<command>` shell mode in the interactive CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_bracketed_paste_timeout.py` | test | Tests for bracketed-paste timeout safety valve (#16263). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_branch_command.py` | test | Tests for the /branch (/fork) command — session branching. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_busy_input_mode_command.py` | test | Tests for the /busy CLI command and busy-input-mode config handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_chat_q_exit_clear.py` | test | Regression tests for #53009: chat -q final response erased by exit-summary clear. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_active_agent_ref_wiring.py` | test | Regression test for #49287 — the CLI memory-provider ``on_session_end`` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_approval_ui.py` | test | Python module `test_cli_approval_ui.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_async_delegation_delivery.py` | test | Regression coverage for CLI async-delegation completion ownership. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_background_busy_path.py` | test | Regression tests for classic-CLI mid-run /background dispatch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_background_status_indicator.py` | test | Tests for the /background indicator in the CLI status bar. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_background_tui_refresh.py` | test | Tests for CLI background command TUI refresh behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_bracketed_paste_sanitizer.py` | test | Tests for defensive bracketed-paste wrapper stripping in the CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_browser_connect.py` | test | Tests for CLI browser CDP auto-launch helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_cmd_backspace.py` | test | Verify Cmd+Backspace / Cmd+ForwardDelete byte sequences from CSI-u | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_codex_context_reference.py` | test | Regression coverage for provider-aware @-context sizing in the CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_context_warning.py` | test | Tests for the low context length warning in the CLI banner. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_copy_command.py` | test | Tests for CLI /copy command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_delegate_background_notice.py` | test | The CLI spells out auto-resume when a delegate_task goes to the background. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_extension_hooks.py` | test | Tests for protected HermesCLI TUI extension hooks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_external_editor.py` | test | Tests for CLI external-editor support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_file_drop.py` | test | Tests for _detect_file_drop — file path detection that prevents | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_first_run_setup.py` | test | First-run onboarding routing for a completely unconfigured install. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_force_redraw.py` | test | Tests for CLI redraw helpers used to recover from terminal buffer drift. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_goal_interrupt.py` | test | Tests for CLI goal-continuation interrupt handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_image_command.py` | test | Python module `test_cli_image_command.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_init.py` | test | Tests for HermesCLI initialization -- catches configuration bugs | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_insights_command.py` | test | Python module `test_cli_insights_command.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_interrupt_ack_race.py` | test | Regression tests for the CLI interrupt-acknowledgement race. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_interrupt_drain_regression.py` | test | Regression test for #20271: classic-CLI hangs when messages typed during | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_interrupt_subagent.py` | test | End-to-end test simulating CLI interrupt during subagent execution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_light_mode.py` | test | Tests for the light-mode terminal detection + color remap in cli.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_loading_indicator.py` | test | Regression tests for loading feedback on slow slash commands. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_markdown_rendering.py` | test | Python module `test_cli_markdown_rendering.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_mcp_config_watch.py` | test | Tests for automatic MCP reload when config.yaml mcp_servers section changes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_new_session.py` | test | Regression tests for CLI fresh-session commands. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_pet_pane.py` | test | The base-CLI petdex pane: reactive half-block sprite above the prompt. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_prefix_matching.py` | test | Tests for slash command prefix matching in HermesCLI.process_command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_preloaded_skills.py` | test | Python module `test_cli_preloaded_skills.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_provider_resolution.py` | test | Python module `test_cli_provider_resolution.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_queue_paste.py` | test | Regression tests for collapsed paste references passed to /queue. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_reload_skills.py` | test | Tests for the ``/reload-skills`` CLI slash command (``HermesCLI._reload_skills``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_resume_command.py` | test | Python module `test_cli_resume_command.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_retry.py` | test | Regression tests for CLI /retry history replacement semantics. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_save_config_value.py` | test | Tests for save_config_value() in cli.py — atomic write behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_secret_capture.py` | test | Python module `test_cli_secret_capture.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_shift_enter_newline.py` | test | Verify Shift+Enter byte sequences parse to the same key tuple Alt+Enter | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_shutdown_memory_messages.py` | test | Regression tests for #15165 (CLI sibling site) — CLI exit cleanup must | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_skin_integration.py` | test | Python module `test_cli_skin_integration.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_status_bar.py` | test | Python module `test_cli_status_bar.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_status_bar_goal.py` | test | Status-bar goal segment (⊙ goal N/M) — active-goal-only rendering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_status_command.py` | test | Tests for CLI /status command behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_steer_busy_path.py` | test | Regression tests for classic-CLI mid-run /steer dispatch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_terminal_response_sanitizer.py` | test | Tests for defensive terminal control-response stripping in the CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_terminal_shortcuts.py` | test | Regression tests for terminal navigation/focus escape sequences. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_tools_command.py` | test | Tests for /tools slash command handler in the interactive CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_user_message_preview.py` | test | Python module `test_cli_user_message_preview.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_yolo_resume_persistence.py` | test | Regression tests: YOLO mode persists across ``hermes --resume``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cli_yolo_toggle.py` | test | Regression tests for the CLI ``/yolo`` in-chat toggle. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_compress_flags.py` | test | Tests for /compress --preview/--dry-run/--aggressive flags and the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_compress_focus.py` | test | Tests for /compress <focus> — guided compression with focus topic. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_compress_here.py` | test | Tests for /compress here [N] — boundary-aware partial compression. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_compress_type_ahead.py` | test | Type-ahead queue-drain proof for /compress (issue #61042, PR #68284). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cpr_local_leak.py` | test | Local CPR leak reproduction + classic-CLI Application output selection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cprint_bg_thread.py` | test | Tests for cli._cprint's bg-thread cooperation with prompt_toolkit. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_ctrl_enter_newline.py` | test | Regression tests for issue #22379 — Ctrl+Enter newline over SSH/WSL. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_cwd_env_respect.py` | test | Tests for CLI/TUI CWD resolution in load_cli_config(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_destructive_slash_confirm.py` | test | Tests for cli.HermesCLI._confirm_destructive_slash. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_destructive_slash_inline_skip_e2e.py` | test | End-to-end integration test for the destructive-slash inline-skip path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_exit_delete_session.py` | test | Tests for `/exit --delete` and `/quit --delete` session deletion. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_exit_summary_resume_hint.py` | test | Tests for the CLI exit summary's resume hint, including profile-flag support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_exit_watchdog_signal_arm.py` | test | Exit watchdog: arm on shutdown *intent* (signal), never at chat startup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_fast_command.py` | test | Tests for the /fast CLI command and service-tier config handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_focus_view.py` | test | Tests for ``/focus`` — the display-only reduced-output view. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_indicator_command.py` | test | Tests for the /indicator CLI command and busy-indicator style config. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_interrupt_output_history_regression.py` | test | Regression tests for #60920/#60941: interrupt marker duplication on redraw. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_manual_compress.py` | test | Tests for CLI manual compression messaging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_moa_command.py` | test | Python module `test_moa_command.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_modify_other_keys_aliases.py` | test | Regression tests for issue #87711 — Ctrl+key / Alt+key combos broken | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_partial_compress.py` | test | Tests for ev0_cli.partial_compress — the pure split/parse helpers | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_personality_none.py` | test | Tests for /personality none — clearing personality overlay. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_prefill_config.py` | test | Regression tests for CLI prefill config key compatibility. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_prepend_note_to_message.py` | test | Tests for cli._prepend_note_to_message. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_prompt_stash.py` | test | Tests for the Ctrl+S prompt stash state machine (ev0_cli.prompt_stash). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_prompt_stash_cli.py` | test | Tests for the Ctrl+S prompt stash wiring inside HermesCLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_prompt_text_input_thread_safety.py` | test | Tests for ``HermesCLI._prompt_text_input`` thread-safe input dispatch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_quick_commands.py` | test | Tests for user-defined quick commands that bypass the agent loop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_reasoning_command.py` | test | Tests for the combined /reasoning command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_resume_display.py` | test | Tests for session resume history display — _display_resumed_history() and | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_resume_model_restore.py` | test | Tests for CLI resume model restoration and /model session persistence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_resume_quiet_stderr.py` | test | Tests for /resume status lines going to stderr in quiet mode (#11793). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_save_conversation_location.py` | test | Tests for /save — the conversation snapshot slash command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_session_boundary_hooks.py` | test | Python module `test_session_boundary_hooks.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_single_query_session_finalize.py` | test | Python module `test_single_query_session_finalize.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_slash_command_interrupt.py` | test | Tests for the KeyboardInterrupt guard around slash command dispatch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_slash_confirm_windows.py` | test | Regression tests for #30768, #32383, and #33961. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_steer_inline_repaint_34569.py` | test | Regression guard for issue #34569 — inline /steer (and /model) submit | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_stream_delta_think_tag.py` | test | Tests for _stream_delta's handling of <think> tags in prose vs real reasoning blocks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_stream_flush_left.py` | test | Streamed response lines must be flush-left (no leading indent). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_stream_partial_line_flush.py` | test | Streaming display: logical lines are emitted ONLY at real newlines. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_surrogate_sanitization.py` | test | Tests for surrogate character sanitization in user input. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_terminal_interrupt_recovery.py` | test | Regression tests for #33271: terminal recovery after interrupt. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_termios_drift_heal.py` | test | Regression tests for cooked-mode termios drift healing (cli._heal_cooked_mode_drift). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_tool_progress_scrollback.py` | test | Tests for stacked tool progress scrollback lines in the CLI TUI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_transformed_stream_output.py` | test | Regression coverage for CLI delivery after transform_llm_output streaming. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_tui_terminal_reset_on_exit.py` | test | Regression tests for GitHub #36823 — the TUI must reset terminal input | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_update_command.py` | test | Tests for the /update slash command in the classic CLI and TUI launcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_version_command.py` | test | Tests for the /version slash command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_worktree.py` | test | Tests for git worktree isolation (CLI --worktree / -w flag). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_worktree_security.py` | test | Security-focused integration tests for CLI worktree setup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cli/test_worktree_sync_base.py` | test | Tests for worktree base-ref resolution — branch from the fresh remote tip. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/live_cua_0_9_smoke.py` | test | Opt-in macOS smoke test for the installed cua-driver live MCP contract. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_cua_atexit_teardown.py` | test | Tests for cua-driver subprocess teardown on interpreter exit. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_cua_cli_fallback_env.py` | test | Regression test: the cua-driver CLI-fallback transport must sanitize the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_cua_no_overlay.py` | test | Tests for the cua-driver --no-overlay policy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_cua_perf_knobs.py` | test | Behavior contracts for computer_use latency knobs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_cua_spawn_env_sanitization.py` | test | Regression tests: every remaining cua-driver spawn site must sanitize the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_cua_telemetry.py` | test | Tests for the cua-driver telemetry opt-in policy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_cua_wsl_manifest_path.py` | test | Python module `test_cua_wsl_manifest_path.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_doctor.py` | test | Tests for ``tools.computer_use.doctor``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/computer_use/test_permissions_resolution.py` | test | Regression tests for Computer Use readiness under a thin GUI PATH. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/conformance/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/conformance/test_vector_generator.py` | test | Conformance vector generator tests (Phase 5 oracle workstream). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/conformance/vectors/discord.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `tests/conformance/vectors/slack.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `tests/conformance/vectors/telegram.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `tests/conformance/vectors/whatsapp.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `tests/conftest.py` | test | Shared fixtures for the hermes-agent test suite. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/conftest.py` | test | Cron-test fixtures. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_agent_scheduling_gate.py` | test | Behavior contract for the cron.allow_agent_scheduling config gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_blueprint_catalog.py` | test | Tests for Automation Blueprints — the parameterized automation blueprint system. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_claim_job_for_fire.py` | test | Tests for the store-level CAS fire claim (Phase 4C). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cleanup_timeout.py` | test | Regression tests for bounded cron post-run cleanup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_codex_execution_paths.py` | test | Python module `test_codex_execution_paths.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_compute_next_run_last_run_at.py` | test | Test that compute_next_run uses last_run_at for cron jobs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_context_from.py` | test | Tests for cron job context_from feature (issue #5439 Option C). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_created_delivery.py` | test | Create-time delivery resolution for cron-context job creation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_direct_api_call_62151.py` | test | Regression guard for #62151 — gateway cron must not wedge on 2nd+ API call. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_direct_api_call_watchdog.py` | test | Regression guard for #80759 — the inline non-streaming call must be bounded. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_drift_alert_once.py` | test | Drift-guard skips must alert once per job, not once per tick (#44585 + #73506). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_failure_alert_remediation_hint.py` | test | The empty-chain failure alert must tell the operator how to fix it. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_failure_summarizer_inactivity.py` | test | _summarize_cron_failure_for_delivery must not mislabel the scheduler's own | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_inactivity_timeout.py` | test | Tests for cron job inactivity-based timeout. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_kanban_env_isolation.py` | test | Cron sessions must not inherit a kanban worker's dispatcher identity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_no_agent.py` | test | Tests for cronjob no_agent mode — script-driven jobs that skip the LLM. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_origin_synthetic_thread.py` | test | Cron origin capture: Slack per-message session-key threads are not routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_profile_isolation.py` | test | Regression tests for #4707 — cron must be per-profile. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_prompt_injection_skill.py` | test | Regression guard: skill content loaded at cron runtime must be scanned. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_provider_pin.py` | test | Provider-drift fail-closed guard for cron jobs (#44585). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_relay_delivery_guards.py` | test | Fire-time guards: stale Slack creation-thread routing + relay-fronted preflight. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_run_stale_claim_reap_86721.py` | test | Regression for #86721 — a one-shot `hermes cron run` invocation's | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_script.py` | test | Tests for cron job script injection feature. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cron_workdir.py` | test | Tests for per-job workdir support in cron jobs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_cronjob_schema.py` | test | Tests for the cronjob tool schema shape. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_dead_owner_claim_reclaim.py` | test | Dead-owner cron claim reclaim + one-shot CLI `cron run` sync gate (#86721). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_execution_ledger.py` | test | Durable cron execution-ledger behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_file_permissions.py` | test | Tests for file permissions hardening on sensitive files. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_idle_tick_config_skip.py` | test | Idle cron ticks must not load config (#33612 salvage). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_inflight_stale_guard.py` | test | RED-first regression test for the cron in-flight claim leak (t_27b59583). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_jobs.py` | test | Tests for cron/jobs.py — schedule parsing, job CRUD, and due-job detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_jobs_changed_notify.py` | test | Tests for on_jobs_changed wiring (Phase 4F.1). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_jobs_crossprocess_lock.py` | test | Regression test for the jobs.json cross-process lock. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_jobs_file_ownership.py` | test | Regression tests for issue #68483. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_jobs_shrink_merge_80624.py` | test | Regression for #80624 — concurrent creates must not be clobbered on save. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_monitor_kind.py` | test | Tests for monitor-mode cron jobs — cheap source each tick, hash-suppressed agent runs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_notepad.py` | test | Per-job durable cron notepad: KV scratchpad surviving scheduled wake-ups. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_parallel_pool.py` | test | Tests for the persistent parallel pool and running-job guard in cron/scheduler.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_preflight_config.py` | test | Cron pre-dispatch configuration validation (T1-26). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_reasoning_config_per_model.py` | test | Tests for per-model reasoning_effort override in cron scheduler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_recurring_eagain_redispatch.py` | test | Deterministic reproduction of the recurring-cron EAGAIN wedge (t_8b5480b3). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_recurring_wedge_selfheal.py` | test | Deterministic reproduction of the recurring-cron wedge (t_8b5480b3) — RED/GREEN. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_relay_fronted_delivery.py` | test | Cron delivery for relay-fronted logical platforms. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_rewrite_skill_refs.py` | test | Tests for cron.jobs.rewrite_skill_refs — the curator integration that | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_run_one_job.py` | test | Characterization + unit tests for the `run_one_job` shared helper (Phase 4A). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_scheduler.py` | test | Tests for cron/scheduler.py — origin resolution, delivery routing, and error logging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_scheduler_cron_session_isolation.py` | test | Regression test for cron-session approval isolation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_scheduler_mcp_init.py` | test | Regression tests for MCP server availability in cron jobs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_scheduler_provider.py` | test | Characterization tests for the cron trigger before/after the provider refactor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_scheduler_shutdown_guard.py` | test | Regression coverage for #58720 / #55924 — cron scheduling races | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_script_claim_heartbeat.py` | test | Regression coverage for one-shot claims during blocking cron scripts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_sessiondb_init_hang.py` | test | Regression test for a hung SessionDB() init permanently wedging a cron job. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_shutdown_interrupt.py` | test | Tests for #60432: cron jobs must not be silently invisible to gateway | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_suggestions.py` | test | Tests for the Suggested Cron Jobs feature. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_terminal_cwd_lock.py` | test | Tests for the TERMINAL_CWD readers-writer lock in cron/scheduler.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_ticker_stall_60703.py` | test | Regression tests for #60703 — cron ticker silently stalls after gateway restart. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/cron/test_usage_audit_logger.py` | test | Tests for the cron usage_audit.jsonl logger. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/dashboard/test_ws_client_host.py` | test | Regression tests for the in-container WebSocket client host resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/conftest.py` | test | Shared fixtures for docker-image integration tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_config_migration.py` | test | Runtime smoke test for Docker config-schema migration on boot. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_container_restart.py` | test | Container-restart survives per-profile gateway registrations. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_dashboard.py` | test | Harness: dashboard opt-in via HERMES_DASHBOARD. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_docker_exec_privilege_drop.py` | test | Regression tests for the docker-exec privilege-drop shim. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_dump_build_sha.py` | test | Regression test: ``hermes dump`` reports a real git SHA inside the container. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_gateway_bootstrap_state.py` | test | Runtime smoke tests for Docker gateway_state.json bootstrap seeding. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_gateway_run_supervised.py` | test | Harness: `docker run <image> gateway run` redirects to supervised mode. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_home_override_scripts.py` | test | Runtime smoke tests for Docker HOME overrides and script behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_immutable_install.py` | test | Runtime smoke tests for Docker immutable install tree and install-method stamp. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_immutable_install_permissions.py` | test | Docker smoke tests for immutable install permissions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_license_file_present.py` | test | Runtime smoke test for Docker image license-file presence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_log_dir_seed.py` | test | Runtime smoke test for Docker $HERMES_HOME/logs/gateways seeding. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_main_invocation.py` | test | Harness: docker run <image> [cmd...] invocation patterns. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_profile_gateway.py` | test | Harness: per-profile gateway start/stop inside the container. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_puid_pgid_remap.py` | test | Runtime smoke tests for Docker PUID/PGID and UID/GID remap. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_s6_profile_gateway_integration.py` | test | Harness: in-container integration tests for S6ServiceManager. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_smoke.py` | test | Runtime smoke tests for the Docker image entrypoint and subcommands. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_sqlite_runtime.py` | test | Runtime qualification for SQLite in the published Docker image. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_stage2_browser_discovery.py` | test | Runtime smoke tests for Docker stage2 browser executable discovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_tini_compat_shim.py` | test | Runtime smoke test for the Docker tini compatibility shim (#34192, #66679). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_toplevel_chown.py` | test | Runtime smoke tests for Docker top-level state-file ownership repair. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_tui_passthrough.py` | test | Harness: interactive TUI TTY passthrough. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_tui_prebuilt_bundle.py` | test | Harness: the image ships a prebuilt TUI bundle, not a runtime npm install. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_user_flag_guard.py` | test | Runtime smoke tests for Docker --user flag guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/docker/test_zombie_reaping.py` | test | Harness: PID 1 must reap orphaned zombie processes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/e2e/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/e2e/conftest.py` | test | Shared fixtures for gateway e2e tests (Telegram, Discord). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/e2e/matrix_xsign_bootstrap/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `tests/e2e/matrix_xsign_bootstrap/docker-compose.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py` | test | End-to-end test for Matrix cross-signing auto-bootstrap. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/e2e/test_discord_adapter.py` | test | Minimal e2e tests for Discord mention stripping + /command detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/e2e/test_platform_commands.py` | test | E2E tests for gateway slash commands (Telegram, Discord). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/e2e/test_relay_native_anthropic_stream.py` | test | Native Anthropic SDK streaming through Relay's managed execution path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/conftest.py` | test | Fixtures shared across ev0_cli kanban tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/conftest_dashboard_auth.py` | test | Stub auth provider + shared fixtures for dashboard-auth tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/fixtures/plugin_compat_legacy/__init__.py` | test | Frozen legacy plugin used by the behavior compatibility suite. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/fixtures/plugin_compat_legacy/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `tests/ev0_cli/test_25106_global_switch_persists_base_url_api_mode.py` | test | Regression tests for #25106: CLI `/model <name> --global` never persisted | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_active_sessions.py` | test | Python module `test_active_sessions.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_actual_provider.py` | test | Regression tests for the Actual Computer provider wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_agent_env_advertisement.py` | test | Tests for the AI_AGENT / HERMES_AGENT harness-attribution env vars. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_agent_import.py` | test | Tests for ev0_cli.agent_import — ``hermes import-agent``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_agent_plugins.py` | test | Agent Plugins v1 portable package validation tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ai_gateway_models.py` | test | AI Gateway model list and pricing translation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_anthropic_model_flow_stale_oauth.py` | test | Tests for Bug #12905 fix — stale OAuth token detection in hermes model flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_anthropic_oauth_flow.py` | test | Tests for Anthropic OAuth setup flow behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_anthropic_oauth_routes_to_messages_api.py` | test | Regression coverage for issue #32243. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_anthropic_picker_curated.py` | test | Regression tests for the Anthropic model-picker dropping curated aliases. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_anthropic_provider_persistence.py` | test | Tests for Anthropic credential persistence helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_api_key_providers.py` | test | Tests for API-key provider support (z.ai/GLM, Kimi, MiniMax, AI Gateway). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_api_mode_aliases.py` | test | Legacy ``api_mode`` spellings must keep selecting the transport they named. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_apply_model_switch_result_context.py` | test | Regression test for the `/model` picker confirmation display. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_apply_profile_override.py` | test | Regression tests for _apply_profile_override HERMES_HOME guard (issue #22502). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_approval_transport.py` | test | Approval transport plugin contract and fail-closed host routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_approvals_command.py` | test | Cross-surface contract for the persistent /approvals mode command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_approvals_suggest.py` | test | Tests for ``hermes approvals suggest`` (ev0_cli/approvals_suggest.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_approvals_test.py` | test | Tests for ``hermes approvals test`` — dry-run approval verdict CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_arcee_provider.py` | test | Tests for Arcee AI provider support — standard direct API provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_argparse_flag_propagation.py` | test | Tests for parent→subparser flag propagation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_at_context_completion_filter.py` | test | Regression test: `@folder:` completion must only surface directories and | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_atomic_json_write.py` | test | Tests for utils.atomic_json_write — crash-safe JSON file writes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_atomic_yaml_write.py` | test | Tests for utils.atomic_yaml_write — crash-safe YAML file writes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_codex_provider.py` | test | Tests for Codex auth — tokens stored in Hermes auth store (~/.hermes/auth.json). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_codex_quota_probe.py` | test | Tests for the Codex upstream-quota-restored probe and cooldown clearing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_codex_self_heal.py` | test | Regression tests for Codex refresh_token self-heal (cross-store rotation). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_commands.py` | test | Tests for auth subcommands backed by the credential pool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_loopback_ssh_hint.py` | test | Unit tests for _print_loopback_ssh_hint() in ev0_cli/auth.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_nous_provider.py` | test | Regression tests for Nous OAuth refresh and inference JWT interactions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_profile_fallback.py` | test | Tests for cross-profile auth fallback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_provider_gate.py` | test | Tests for is_provider_explicitly_configured(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_provider_scope.py` | test | resolve_provider auto-detection must read provider keys through the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_qwen_provider.py` | test | Tests for Qwen OAuth provider authentication (ev0_cli/auth.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_ssl_macos.py` | test | Tests for ev0_cli.auth._default_verify platform-aware fallback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_store_read_failure.py` | test | A transient read failure on auth.json must not degrade to an empty store. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_store_windows_encoding.py` | test | Regression tests for auth store encoding on Windows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_toctou_file_modes.py` | test | Regression tests for TOCTOU-safe credential file writers in ``ev0_cli.auth``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_usable_secret.py` | test | Tests for placeholder API key detection in ev0_cli.auth. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_auth_xai_oauth_provider.py` | test | Tests for xAI Grok OAuth — tokens stored in Hermes auth store (~/.hermes/auth.json). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_authenticated_providers_exhausted_pool.py` | test | Regression test for #45759. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_aux_config.py` | test | Tests for the auxiliary-model configuration UI in ``hermes model``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_aux_picker_inventory.py` | test | Auxiliary-task pickers share one provider-inventory substrate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_azure_detect.py` | test | Tests for ev0_cli.azure_detect — transport & model auto-detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_azure_foundry_entra.py` | test | Tests for Azure Foundry Entra ID runtime resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_backup.py` | test | Tests for hermes backup and import commands. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_backup_stability.py` | test | Python module `test_backup_stability.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_banner.py` | test | Tests for banner toolset name normalization and skin color usage. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_banner_git_state.py` | test | Python module `test_banner_git_state.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_banner_skills.py` | test | Tests for banner get_available_skills() — disabled and platform filtering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_banner_skills_width.py` | test | Tests for banner skills display — terminal-width-aware truncation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_base_url_host_identity.py` | test | Regression tests: provider-identity checks must compare URL *hostnames*, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_bedrock_mantle_key_env.py` | test | Bedrock API-key setup must produce a config that actually authenticates. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_bedrock_model_picker.py` | test | Tests for AWS Bedrock integration in the model picker and provider catalog. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_bedrock_region_scoped_picker.py` | test | Regression tests for #28156 — Bedrock picker must be region-scoped. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_billing_cli.py` | test | Tests for the /billing CLI handler (cli.py::_show_billing). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_billing_portal_url.py` | test | Portal-URL resolution for Phase 2b billing errors (nous_billing). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_billing_scope_stepup.py` | test | Tests for the Phase 2b billing:manage scope step-up (auth.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_bitwarden_status.py` | test | Python module `test_bitwarden_status.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_bounded_probe_run.py` | test | ``bounded_probe_run`` — deadlock-safe capture for fail-open probes (#87134). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_browser_connect_dual_stack.py` | test | Dual-stack loopback discovery + port-squatter handling for /browser connect. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_build_info.py` | test | Tests for ev0_cli.build_info — baked-in build SHA resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_bundles.py` | test | Tests for ev0_cli/bundles.py — the `hermes bundles` CLI subcommand. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_busy_policy_invariants.py` | test | Invariant tests for the declarative busy_policy on CommandDef. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_bytecode_sweep.py` | test | Tests for the launch-time stale-bytecode sweep (checkout fingerprint guard). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cached_fetch_api_models.py` | test | Cache-contract tests for ``cached_fetch_api_models()``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_canonical_custom_identity.py` | test | ``canonical_custom_identity`` must return the durable config-key identity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_certifi_repair.py` | test | Regression tests for issue #29866. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_chat_c_fail_loudly.py` | test | Tests for `chat -c <title>` failing loudly (stderr) and `--create-if-missing`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_chat_skills_flag.py` | test | Python module `test_chat_skills_flag.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_checkout_mutation_guards.py` | test | The test suite must never mutate the LIVE checkout or its venv. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_checkpoints_prune.py` | test | Tests for `hermes checkpoints prune`'s orphan confirmation flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_claw.py` | test | Tests for hermes claw commands. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_clear_stale_base_url.py` | test | Tests for _clear_stale_openai_base_url() cleanup after provider switch (#5161). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cli_active_session_limit.py` | test | Python module `test_cli_active_session_limit.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cli_custom_provider_vision.py` | test | End-to-end CLI coverage for named custom-provider vision routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cli_model_once.py` | test | Python module `test_cli_model_once.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cli_output.py` | test | Python module `test_cli_output.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cli_startup_model_cost_guard.py` | test | Python module `test_cli_startup_model_cost_guard.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_clipboard_text_write.py` | test | Tests for native clipboard text write (ev0_cli/clipboard.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cmd_update.py` | test | Tests for cmd_update — branch fallback when remote branch doesn't exist. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cmd_update_docker.py` | test | Tests for ``hermes update`` / ``--check`` inside the Docker container. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_coalesce_session_args.py` | test | Tests for _coalesce_session_name_args — multi-word session name merging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_codex_cli_model_picker.py` | test | Regression tests for the /model picker's credential-discovery paths. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_codex_models.py` | test | Python module `test_codex_models.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_codex_runtime_plugin_migration.py` | test | Tests for the codex MCP plugin migration helper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_codex_runtime_switch.py` | test | Tests for the /codex-runtime slash-command shared logic. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_commands.py` | test | Tests for the central command registry and autocomplete. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_commands_execute.py` | test | Invariant tests for registry-owned slash execution (CommandDef.execute). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_completer_config_reads.py` | test | Measured-work pins for the slash-completer config reads. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_completion.py` | test | Tests for ev0_cli/completion.py — shell completion script generation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_computer_use_cli.py` | test | CLI coverage for the public Computer Use command surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_config.py` | test | Tests for ev0_cli configuration management. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_config_env_expansion.py` | test | Tests for ${ENV_VAR} substitution in config.yaml values. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_config_env_ref_parity.py` | test | Config `${env:VAR}` SecretRef parity (salvaged from PR #59516). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_config_env_refs.py` | test | Python module `test_config_env_refs.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_config_loader_e2e.py` | test | E2E for the canonical-loader migration (managed-scope/env-expansion drift fix). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_config_read_guard.py` | test | Lint guard: no new raw yaml.safe_load(config.yaml) reads outside owner modules. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_config_validation.py` | test | Tests for config.yaml structure validation (validate_config_structure). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_configured_builtin_models.py` | test | Configured models extend built-in picker rows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_console_engine.py` | test | Python module `test_console_engine.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_container_aware_cli.py` | test | Tests for container-aware CLI routing (NixOS container mode). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_container_boot.py` | test | Tests for ev0_cli.container_boot — the cont-init.d-time | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_context_switch_guard.py` | test | Tests for ev0_cli.context_switch_guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_copilot_auth.py` | test | Tests for ev0_cli.copilot_auth — Copilot token validation and resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_copilot_catalog_oauth_fallback.py` | test | Catalog-API-key fallback for the Copilot ``/model`` picker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_copilot_context.py` | test | Tests for Copilot live /models context-window resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_copilot_in_model_list.py` | test | Tests for GitHub Copilot entries shown in the /model picker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_copilot_model_api_mode.py` | test | Tests for Copilot model API-mode routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_copilot_runtime_api_mode.py` | test | Tests for Copilot runtime api_mode resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_copilot_token_exchange.py` | test | Tests for Copilot token exchange (raw GitHub token → Copilot API token). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_credential_lifecycle.py` | test | E2E tests for the unified provider-credential lifecycle (#51071 #59761 #62269). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cron.py` | test | Tests for ev0_cli.cron command handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cron_dashboard_off_loop.py` | test | Regression tests: cron dashboard handlers must not run profile I/O on the event loop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cron_fire_dashboard.py` | test | Tests for the Chronos cron-fire webhook ON THE DASHBOARD APP (web_server). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cron_model_impact.py` | test | Python module `test_cron_model_impact.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cron_parser_builder.py` | test | Unit tests for the extracted ``hermes cron`` parser builder. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_cron_profile_enumeration_lightweight.py` | test | Cron aggregation must not perform full profile metadata scans. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ctrlg_editor_submit.py` | test | Tests for Ctrl+G external-editor submit in the classic CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curator_archive_prune.py` | test | Tests for `hermes curator archive` and `hermes curator prune`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curator_recent_run_notice.py` | test | Tests for `_print_curator_recent_run_notice`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curator_run.py` | test | Tests for `hermes curator run` CLI behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curator_status.py` | test | Tests for `hermes curator status` output. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curator_usage.py` | test | Tests for `hermes curator usage` — the all-skills usage view. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curses_arrow_keys.py` | test | Regression tests for arrow-key decoding in the curses menus. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curses_color_compat.py` | test | Tests for curses color compatibility on low-color terminals (Docker). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curses_ui_fuzzy_rank.py` | test | Tests for the ranked fuzzy scorer used by the searchable curses pickers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_curses_ui_search.py` | test | Python module `test_curses_ui_search.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_custom_provider_context_length.py` | test | Regression tests for custom_providers per-model context_length resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_custom_provider_extra_headers.py` | test | Tests for per-provider ``extra_headers`` in providers / custom_providers config. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_custom_provider_identity.py` | test | Unit tests for find_custom_provider_identity (base_url → custom:<name>). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_custom_provider_model_switch.py` | test | Tests that `hermes model` always shows the model selection menu for custom | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_custom_provider_normalize_no_mutate.py` | test | Regression: _normalize_custom_provider_entry must never mutate its input. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_custom_provider_tls.py` | test | Tests for per-provider TLS settings in custom_providers config. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_admin_endpoints.py` | test | Tests for the dashboard admin API endpoints (MCP, pairing, webhooks, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_401_reauth.py` | test | Phase 6 — 401 re-auth + ``next=`` propagation tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_audit.py` | test | Audit log for dashboard-auth events. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_cookies.py` | test | Tests for the dashboard-auth cookie helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_gate.py` | test | Regression harness for the dashboard auth gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_middleware.py` | test | End-to-end behavioural tests for the dashboard auth gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_native_flow.py` | test | E2E + unit tests for the RFC 8252 native-app (system-browser + loopback + | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_password_login.py` | test | Tests for the password (non-redirect) dashboard-auth login flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_plugin_hook.py` | test | The plugin context exposes register_dashboard_auth_provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_prefix.py` | test | Path-prefix (X-Forwarded-Prefix) awareness for the dashboard-auth gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_provider_base.py` | test | Contract test for DashboardAuthProvider implementations. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_status_endpoint.py` | test | Phase 7 — /api/status exposes auth-gate state + AuthWidget integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_stub_provider.py` | test | Contract test for the StubAuthProvider used in dashboard-auth E2E tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_ws_auth.py` | test | Tests for the WS-upgrade auth helper (Phase 5 task 5.2). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_auth_ws_tickets.py` | test | Tests for the WS-upgrade ticket store (Phase 5 task 5.1). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_basic_auth_plugin_enable.py` | test | Regression tests for dashboard basic-auth plugin enablement (#54489). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_browser_safe_imports.py` | test | Static dashboard tests for browser-safe @nous-research/ui imports. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_lifecycle_flags.py` | test | Tests for ``hermes dashboard --stop`` / ``--status`` flags. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_oauth_endpoints_server_gate.py` | test | Regression guard for PR #61281 (mobile/hosted dashboard OAuth). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_param_clamps.py` | test | Dashboard query-param clamps (#39200 + #74778 salvage). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_profiles_nav_label.py` | test | Static dashboard tests for the Profiles navigation copy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_register.py` | test | Tests for ``hermes dashboard register``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_token_auth.py` | test | Contract tests for the generic non-interactive (bearer-token) auth seam. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_tui_backcompat.py` | test | Regression test: `hermes dashboard --tui` must not hard-crash. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_unified_launch.py` | test | Tests for the unified profile→machine dashboard launch routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dashboard_web_dist_validation.py` | test | Regression tests: `hermes dashboard` validates HERMES_WEB_DIST before serving. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_debug.py` | test | Tests for ``hermes debug`` CLI command and debug utilities. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_default_interface_resolution.py` | test | Tests for the configurable default interface (cli vs tui). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_deferred_platform_client_tools.py` | test | Deferred platform plugins must still register their *client* tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dep_ensure.py` | test | Python module `test_dep_ensure.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_deprecated_cwd_warning.py` | test | Tests for warn_deprecated_cwd_env_vars() migration warning. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_desktop_exe_integrity.py` | test | Behavior tests for the Windows desktop-exe integrity gate (#69179). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_desktop_repo_discovery_config.py` | test | Python module `test_desktop_repo_discovery_config.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_destructive_slash_confirm_gate.py` | test | Tests for the approvals.destructive_slash_confirm config gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_detect_api_mode_for_url.py` | test | Tests for ev0_cli.runtime_provider._detect_api_mode_for_url. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_determine_api_mode_hostname.py` | test | Regression tests for ``determine_api_mode`` hostname handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_diagnostics_upload.py` | test | Tests for ``ev0_cli.diagnostics_upload`` — the Nous-S3 upload client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_diff_command.py` | test | Tests for the CLI ``/diff`` command handler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dingtalk_auth.py` | test | Unit tests for ev0_cli/dingtalk_auth.py (QR device-flow registration). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_discord_skill_clamp_warning.py` | test | Tests for Discord /skill 32-char clamp collision warnings. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_doctor.py` | test | Tests for ev0_cli.doctor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_doctor_command_install.py` | test | Tests for the Command Installation check in hermes doctor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_doctor_dedicated_provider_skip.py` | test | Regression: hermes doctor must not run a generic Bearer-auth health | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_doctor_journal_modes.py` | test | Tests for doctor's per-database journal-mode report. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_doctor_live.py` | test | Tests for ``hermes doctor --live`` — opt-in bounded real-call tool-backend probes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dump_env_visibility.py` | test | `hermes debug` must not report a shell-only API key as plainly "set". | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dump_git_commit.py` | test | Tests for ev0_cli.dump._get_git_commit — git SHA resolution for ``hermes dump``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_dump_terminal_backend.py` | test | `hermes debug` must report the EFFECTIVE terminal backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_early_recovery.py` | test | Tests for ev0_cli._early_recovery — the dependency-light bootstrap | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ensure_acp_launcher.py` | test | `hermes update` must self-heal the ``hermes-acp`` launcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ensure_ev0_home_memo.py` | test | ensure_hermes_home is memoized per home path (perf: it runs on every | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ensure_ev0_home_uid_34107.py` | test | Regression tests for #34107 — Docker UID/GID handling in ensure_hermes_home. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ensure_gateway_service.py` | test | Tests for ev0_cli.gateway.ensure_gateway_service — the zero-prompt | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ensure_utf8_locale.py` | test | Regression tests for ev0_cli._ensure_utf8(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_env_custom_keys.py` | test | GET /api/env surfaces arbitrary/custom .env keys (not just catalogued ones). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_env_export_line_lifecycle.py` | test | Regression tests for the Tools & Keys GitHub PAT save/remove path (#40041). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_env_export_prefix.py` | test | Tests for ``export `` prefix handling in the hand-rolled .env parsers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_env_load_cache.py` | test | Tests for the load_env() process-level cache. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_env_loader.py` | test | Python module `test_env_loader.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_env_sanitize_on_load.py` | test | Tests for .env sanitization during load to prevent token duplication (#8908). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_fallback_cmd.py` | test | Tests for `hermes fallback` — chain reading, add/remove/clear, legacy migration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_fallback_config.py` | test | Tests for ev0_cli/fallback_config.py — fallback entry API-key resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_fireworks_provider.py` | test | Focused tests for Fireworks AI first-class provider wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_foreign_sessions.py` | test | Tests for ev0_cli.foreign_sessions — Claude Code / Codex CLI import. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway.py` | test | Tests for ev0_cli.gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_external_supervisor.py` | test | Tests for explicit ownership by a wrapped external gateway supervisor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_foreign_xdg_runtime.py` | test | Regression tests for a foreign/leaked ``XDG_RUNTIME_DIR`` in the user-systemd | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_linger.py` | test | Tests for gateway linger auto-enable behavior on headless Linux installs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_platform_gating.py` | test | Host-specific gating in ``ev0_cli.gateway._all_platforms()``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_proc_fallback.py` | test | Tests for /proc-based gateway PID detection in Docker environments. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_restart_loop.py` | test | Tests for gateway restart-loop defenses (#30719). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_run_hard_exit.py` | test | Regression tests for CLI gateway run exit behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_runtime_health.py` | test | Python module `test_gateway_runtime_health.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_s6_dispatch.py` | test | Tests for the Phase 4 s6 dispatch helper in ev0_cli.gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_service.py` | test | Tests for gateway service management helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_service_paths.py` | test | Python module `test_gateway_service_paths.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_windows.py` | test | Tests for ev0_cli.gateway_windows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gateway_wsl.py` | test | Tests for WSL detection and WSL-aware gateway behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gemini_free_tier_setup_block.py` | test | Tests for the Gemini free-tier block in the setup wizard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gemini_provider.py` | test | Tests for Google AI Studio (Gemini) provider integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_get_env_value_scope.py` | test | get_env_value must be scope-aware — the last scope-blind reader (#67027). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_git_probe_tree_kill.py` | test | POSIX process-tree cleanup for ``bounded_git_probe`` (port of openai/codex#36793). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_global_auth_store_memo.py` | test | Measured-work pins for the _load_global_auth_store() memo. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gmi_provider.py` | test | Focused tests for GMI Cloud first-class provider wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_goal_gates.py` | test | Tests for /goal quality gates (GoalGate, run_gate, GoalManager gate flow). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_goals.py` | test | Tests for ev0_cli/goals.py — persistent cross-turn goals. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gpt56_registration.py` | test | Behavior contracts for the GPT-5.6 (Sol/Terra/Luna) registration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_graphical_browser_detection.py` | test | Tests for `_can_open_graphical_browser()` in ev0_cli.auth. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gui_command.py` | test | Tests for ``hermes gui`` desktop launcher wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_gui_uninstall.py` | test | Tests for ev0_cli.gui_uninstall — GUI-only uninstall + install discovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_heartbeat.py` | test | Tests for /heartbeat (ev0_cli/heartbeat.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_hooks_cli.py` | test | Tests for the ``hermes hooks`` CLI subcommand. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ignore_user_config_flags.py` | test | Tests for --ignore-user-config and --ignore-rules flags on `hermes chat`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_image_gen_picker.py` | test | Tests for plugin image_gen providers injecting themselves into the picker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_imagegen_managed_gateway.py` | test | Regression tests for image_gen use_gateway persistence (managed FAL clobber). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_in_dir_msys_paths.py` | test | ``--in`` accepts Git Bash / MSYS-style paths on Windows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_init_command.py` | test | Tests for /init — generate or update AGENTS.md from a project scan. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_input_sanitize.py` | test | Tests for shared user prompt input sanitization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_install_cua_driver.py` | test | Tests for ``install_cua_driver`` upgrade semantics. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_inventory.py` | test | Behavior tests for ev0_cli.inventory. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_inventory_pricing.py` | test | Tests for inventory._apply_pricing — the pricing/tier enrichment that | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_jobs_json_utf8_bom.py` | test | UTF-8 BOM tolerance for independent jobs.json readers (dump/status). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_journey_render.py` | test | Behavior contracts for /journey output routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_block_kinds.py` | test | Tests for typed block reasons + the unblock-loop breaker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_blocked_sticky.py` | test | Regression tests for #28712 — kanban dispatcher must not auto-promote | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_board_project.py` | test | Board→project scoping in kanban_db. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_boards.py` | test | Tests for the multi-board kanban layer (``hermes kanban boards …``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_cli.py` | test | Tests for the kanban CLI surface (ev0_cli.kanban). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_cli_dispatch_passthrough.py` | test | Regression tests for #33488 (CLI max_in_progress / max_spawn / per-profile | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_comment_queries.py` | test | Comment-watermark queries in kanban_db. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_core_functionality.py` | test | Core-functionality tests for the kanban kernel + CLI additions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_count_notify_subs.py` | test | Tests for ``kanban_db.count_notify_subs`` — the read-only subscription probe. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_db.py` | test | Tests for the Kanban DB layer (ev0_cli.kanban_db). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_db_init.py` | test | Python module `test_kanban_db_init.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_db_repair.py` | test | Tests for kanban DB corruption repair, backup retention, WAL checkpointing, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_decompose.py` | test | Tests for the decomposer module + `hermes kanban decompose` CLI surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_decompose_db.py` | test | Tests for kb.decompose_triage_task — the DB-layer atomic fan-out | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_default_assignee.py` | test | Regression tests for #27145 — kanban.default_assignee for unassigned ready tasks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_diagnostics.py` | test | Tests for ev0_cli.kanban_diagnostics — rule-engine that produces | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_dispatch_lock.py` | test | Tests for the kanban dispatcher single-writer lock (issue #35240). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_dispatch_tick_hook.py` | test | Tests for the ``on_kanban_dispatch_tick`` observer hook. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_goal_mode.py` | test | Tests for kanban goal_mode — per-card Ralph-style goal loop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_init_lock_bounded.py` | test | Tests for the bounded kanban init lock (issue #36644). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_lifecycle_hooks.py` | test | Tests for kanban lifecycle plugin hooks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_notify.py` | test | Python module `test_kanban_notify.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_parent_reopen_invalidation.py` | test | Regressions for domain-layer descendant invalidation on ancestor reopen. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_per_profile_cap.py` | test | Regression tests for #21582 — per-profile concurrency cap in dispatcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_project_link.py` | test | Kanban <-> Projects integration: project-linked tasks get a deterministic | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_promote.py` | test | Tests for the kanban `promote` verb (issue #28822). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_reclaim_claim_lock_guard.py` | test | Tests: reclaim paths are claim-lock-aware so they can't desync a re-claimed | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_review_lifecycle.py` | test | Review-lifecycle tests: the first-class ``running -> review`` transition. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_review_lifecycle_complete.py` | test | End-to-end regressions for the Kanban review lifecycle. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_review_surfaces.py` | test | Cross-surface regressions for the complete Kanban review lifecycle. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_specify.py` | test | Tests for the specifier module + `hermes kanban specify` CLI surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_specify_db.py` | test | Tests for kb.specify_triage_task — the DB-layer atomic promotion | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_swarm.py` | test | Python module `test_kanban_swarm.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_task_updated_hook.py` | test | Tests for the ``on_kanban_task_updated`` mutation observer (RFC #58548). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_worker_image_extraction.py` | test | Worker-side image enrichment for kanban tasks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_worker_lifecycle_hooks.py` | test | Tests for the ``on_kanban_worker_*`` observer hooks (RFC #58548). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_worker_session_source.py` | test | Kanban worker runs must not surface as user conversations. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_worker_spawn_toolsets.py` | test | Python module `test_kanban_worker_spawn_toolsets.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_worker_terminal_cwd.py` | test | Tests: kanban worker spawn pins TERMINAL_CWD to the task workspace. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_worktree_isolation.py` | test | Per-task worktree isolation for decompose siblings. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_write_guard.py` | test | #69283: kanban write guard prevents tests from writing to real ~/.hermes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kanban_write_txn_busy_retry.py` | test | write_txn BUSY-retry behaviour. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_kimi_cn_provider_listing.py` | test | Test that kimi-coding and kimi-coding-cn both appear in the /model picker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_launcher.py` | test | Tests for the top-level `./hermes` launcher script. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_lazy_command_exports.py` | test | The decomposed command modules stay lazy after `import ev0_cli.main`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_lazy_refresh_venv_repair.py` | test | Tests for lazy-backend refresh venv repair (#57828 / #58004). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_lifecycle.py` | test | Python module `test_lifecycle.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_linux_desktop_entry.py` | test | Tests for the Linux XDG desktop entry installed by ``hermes desktop``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_list_picker_providers.py` | test | Tests for ``list_picker_providers`` — the /model picker filter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_lmstudio_context_policy.py` | test | Python module `test_lmstudio_context_policy.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_logs.py` | test | Tests for ev0_cli.logs — log viewing and filtering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_loops.py` | test | Tests for ev0_cli/loops.py — /loop recurring in-session wakeups. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_main_model_custom_provider_normalization.py` | test | Dashboard main-model writes preserve declared provider identities. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_installs.py` | test | Python module `test_managed_installs.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope.py` | test | Unit tests for ev0_cli.managed_scope (resolver + loaders + key helpers). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope_cli_config.py` | test | Managed scope must reach cli.py's independent config loader (CLI_CONFIG). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope_config.py` | test | Config integration tests — managed scope wins over user config at the leaf. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope_env.py` | test | Env integration tests — managed .env applied last with override. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope_loaders.py` | test | Each standalone config loader (gateway, TUI/desktop, cron) must honor managed scope. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope_overlay.py` | test | apply_managed_overlay() — the shared helper used by every standalone loader. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope_regression.py` | test | Regression harness — pins config/env load behavior BEFORE managed scope exists. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope_surfacing.py` | test | Surfacing tests — managed scope shown in `config show` and `hermes doctor`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_scope_writeguard.py` | test | Write-guard tests — managed keys can't be set/removed by the user. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_managed_uv.py` | test | Tests for ev0_cli.managed_uv — one path, no guessing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_add_command_dest.py` | test | Regression test: ``hermes mcp add --command`` must not clobber the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_catalog.py` | test | Tests for ev0_cli.mcp_catalog and ev0_cli.mcp_picker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_config.py` | test | Tests for ev0_cli.mcp_config — ``hermes mcp`` subcommands. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_dashboard_oauth.py` | test | Dashboard HTTP contract for hosted MCP OAuth. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_discovery_timing.py` | test | Regression tests for MCP discovery timing in non-interactive sessions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_reload_confirm_gate.py` | test | Tests for the approvals.mcp_reload_confirm config gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_security.py` | test | Tests for MCP server exfiltration hardening. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_startup.py` | test | Regression tests for bounded/lazy CLI MCP startup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mcp_tools_config.py` | test | Tests for MCP tools interactive configuration in ev0_cli.tools_config. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_mem_trim.py` | test | Tests for the long-lived gateway heap-trim helper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_memory_reset.py` | test | Tests for the `hermes memory reset` CLI command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_memory_setup.py` | test | Python module `test_memory_setup.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_memory_setup_provider_arg.py` | test | Tests for `hermes memory setup [provider]` routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_memory_status.py` | test | Tests for `hermes memory status` CLI command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_memory_status_env_hint.py` | test | `hermes memory status` should explain *why* a provider is unavailable. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_migrate_xai.py` | test | Tests for ``hermes migrate xai`` — apply path with ruamel round-trip. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_moa_config.py` | test | Python module `test_moa_config.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_moa_set_models_preserves_extra_keys.py` | test | Regression tests for ``set_moa_models`` preserving undeclared config keys. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_cache_parallel_prefetch.py` | test | Tests for parallel model-catalog prefetch and thread-safe cache writes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_cache_swr.py` | test | Stale-while-revalidate behavior for the model-id disk cache and the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_catalog.py` | test | Tests for ev0_cli.model_catalog — remote manifest fetch + cache + fallback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_cost_guard.py` | test | Python module `test_model_cost_guard.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_data_policy_guard.py` | test | Tests for the data-training-tier selection guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_flow_pooled_credentials.py` | test | Pool-only credentials must be visible to interactive model setup flows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_normalize.py` | test | Tests for ev0_cli.model_normalize — provider-aware model name normalization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_picker_excluded_providers.py` | test | Tests that ``model_catalog.excluded_providers`` hides providers from the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_picker_expensive_confirm.py` | test | Python module `test_model_picker_expensive_confirm.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_picker_secret_scope.py` | test | The /model picker must read provider keys through the per-profile scope. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_picker_viewport.py` | test | Tests for the prompt_toolkit /model picker scroll viewport. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_provider_persistence.py` | test | Tests that provider selection via `hermes model` always persists correctly. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_search.py` | test | Picker search aliases for brand-less wire model ids. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_search_alias_dedup.py` | test | Picker dedup must fold live bare wire-ids into their curated public slug. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_selection_guards.py` | test | Tests for the unified model-selection guard registry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_configured_provider_routing.py` | test | Regression tests for #45006: typed `/model <name>` resolution must route a | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_confirm_thread.py` | test | The /model <name> --provider <p> path must run the expensive-model | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_context_display.py` | test | Regression test for /model context-length display on provider-capped models. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_context_offload.py` | test | ``/model`` context-length resolution must not run on the gateway event loop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_copilot_api_mode.py` | test | Regression tests for Copilot api_mode recomputation during /model switch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_custom_providers.py` | test | Regression tests for /model support of config.yaml custom_providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_filter_unresolved.py` | test | Picker rows must resolve to a runtime provider (#57503). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_once_flags.py` | test | Python module `test_model_switch_once_flags.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_openai_api_mode.py` | test | Regression tests for OpenAI-direct api_mode recomputation during /model switch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_opencode_anthropic.py` | test | Regression tests for OpenCode /v1 stripping during /model switch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_parsing.py` | test | Single-owner /model parsing + effective-model resolution tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_persist_default.py` | test | Tests for session-scoped-by-default model switching. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_switch_variant_tags.py` | test | Tests for OpenRouter variant tag preservation in model switching. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_model_validation.py` | test | Tests for provider-aware `/model` validation in ev0_cli.models. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_models.py` | test | Tests for the ev0_cli models module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_models_dev_preferred_merge.py` | test | Tests for the models.dev-preferred merge behavior in provider_model_ids | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_non_ascii_credential.py` | test | Tests for non-ASCII credential detection and sanitization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_noninteractive_git.py` | test | Non-interactive internal git invocations (port of openai/codex#34540/#34612). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_normalize_main_model_assignment.py` | test | Regression tests for ``_normalize_main_model_assignment`` (POST /api/model/set). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_account.py` | test | Tests for normalized Nous Portal account entitlement helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_auth_keepalive.py` | test | Python module `test_nous_auth_keepalive.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_auth_status_cache.py` | test | Tests for the get_nous_auth_status() process-level cache. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_billing_request.py` | test | Tests for the ev0_cli.nous_billing HTTP client's response handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_ev0_non_agentic.py` | test | Tests for the Nous-Hermes-3/4 non-agentic warning detector. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_inference_url_validation.py` | test | Regression tests for Nous Portal inference_base_url host-allowlist validation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_portal_staging_allowlist.py` | test | Regression tests for the Nous Portal env-override bypassing the host | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_session_validity.py` | test | Tests for the local-only Nous session classifier exposed on /api/status. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_nous_subscription.py` | test | Tests for Nous subscription feature detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_npm_engine.py` | test | Tests for npm ``EBADENGINE`` recovery (``ev0_cli/npm_engine.py``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_official_openai_host.py` | test | Security + parity contract for ``is_official_openai_host``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ollama_cloud_auth.py` | test | Tests for Ollama Cloud authentication and /model switch fixes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ollama_cloud_provider.py` | test | Tests for Ollama Cloud provider integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_oneshot_surrogate.py` | test | Oneshot stdout must survive lone UTF-16 surrogates in model text (#80366). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_oneshot_usage_file.py` | test | Tests for hermes -z --usage-file (per-run JSON usage report). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_openai_codex_model_validation_fallback.py` | test | Regression tests for OpenAI Codex model validation when the listing lags behind | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_openai_discovery_endpoint.py` | test | Discovery honors ``model.base_url`` and cache identity tracks the endpoint. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_openai_listing_authority.py` | test | Live-listing authority on official OpenAI hosts (model switching). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_openai_picker_curated.py` | test | Regression tests for two OpenAI/OpenRouter model-picker bugs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_opencode_go_flat_namespace.py` | test | Tests for opencode-go / opencode-zen flat-namespace model handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_opencode_go_in_model_list.py` | test | Test that opencode-go appears in /model list when credentials are set. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_opencode_go_validation_fallback.py` | test | Tests for the static-catalog fallback in validate_requested_model. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_opencode_zen_model_limit.py` | test | Regression tests for OpenCode Zen model picker limits. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_openrouter_reasoning_metadata.py` | test | Tests for OpenRouter reasoning-capability metadata (prime-agent#1258 port). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_orphan_desktop_serve_reap.py` | test | Orphan Desktop-local ``hermes serve`` reap at backend start. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_overlay_slug_resolution.py` | test | Test that overlay providers with mismatched models.dev keys resolve correctly. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_pairing.py` | test | Python module `test_pairing.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_path_completion.py` | test | Tests for file path autocomplete in the CLI completer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_personality_single_owner.py` | test | Tests for ev0_cli.personality — the single owner of personality state — | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_pet_toggle.py` | test | Tests for pet slash-command config helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_picker_prewarm.py` | test | Tests for the /model picker background cache prewarm. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_pin_kanban_board_env.py` | test | Tests for `_pin_kanban_board_env` helper invoked by `cmd_chat`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_pip_install_detection.py` | test | Python module `test_pip_install_detection.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_placeholder_usage.py` | test | Tests for CLI placeholder text in config/setup output. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_platform_actions.py` | test | Tests for the capability-gated platform action facade (#64176, action half). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_api_compat.py` | test | Behavior-contract compatibility tests for native Hermes plugins. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_auxiliary_tasks.py` | test | Tests for the plugin auxiliary-task registration API. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_call_mcp.py` | test | Tests for the capability-gated ``ctx.call_mcp`` plugin surface (#64204). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_capabilities.py` | test | Tests for the plugin capability model + consent flow (#64228). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_cli_registration.py` | test | Tests for plugin CLI registration system. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_config_state_bridge.py` | test | End-to-end coverage for the profile-scoped plugin config/state bridge (#64227). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_dev.py` | test | Python module `test_plugin_dev.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_event_bus.py` | test | Tests for the inter-plugin event bus (PluginContext.emit / subscribe). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_index_search.py` | test | Tests for the community plugin index (#64181). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_install_ref.py` | test | Exact-commit plugin installation and source metadata. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_manifest_v2.py` | test | Tests for plugin manifest v2 (#64165). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_message_injection.py` | test | Tests for plugin message injection across CLI and gateway hosts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_ownership_ledger.py` | test | End-to-end coverage for plugin registration ownership and reload cleanup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_packs.py` | test | Plugin packs (#64166): parse/validate, SHA enforcement, install fan-out, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_prompt_sections.py` | test | Python module `test_plugin_prompt_sections.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_runtime_disable_gate.py` | test | Regression tests for runtime plugin disable gating. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugin_scanner_recursion.py` | test | Tests for PR1 pluggable image gen: scanner recursion, kinds, path keys. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugins.py` | test | Tests for the Hermes plugin system (ev0_cli.plugins). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugins_cmd.py` | test | Tests for ev0_cli.plugins_cmd — the ``hermes plugins`` CLI subcommand. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugins_cmd_category_discovery.py` | test | Tests for the nested category plugin discovery fix (issue #41066). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugins_cmd_enable_disable_nested.py` | test | Tests for nested/alias-normalized enable & disable flows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugins_cmd_list.py` | test | Python module `test_plugins_cmd_list.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugins_hub_perf_guard.py` | test | Python module `test_plugins_hub_perf_guard.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugins_transcription_registration.py` | test | Tests for PluginContext.register_transcription_provider(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_plugins_tts_registration.py` | test | Tests for PluginContext.register_tts_provider() (issue #30398). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_post_setup_gating.py` | test | Tests for the post_setup install-state gate in `_toolset_needs_configuration_prompt`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_pre_command_hook.py` | test | Tests for the ``pre_command`` observer hook (#64204). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_profile_describer.py` | test | Tests for the profile.yaml metadata layer (description + description_auto) | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_profile_distribution.py` | test | Tests for ev0_cli.profile_distribution — git-based profile installs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_profile_export_credentials.py` | test | Tests for credential exclusion + secret scrubbing during profile export. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_profile_install_env_encoding.py` | test | Regression: the distribution-install preview must read .env as UTF-8. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_profiles.py` | test | Comprehensive tests for ev0_cli.profiles module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_profiles_s6_hooks.py` | test | Tests for the Phase 4 s6 hooks in ev0_cli.profiles. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_profiles_sidebar_cache.py` | test | Regression tests for dashboard sidebar scan coalescing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_profiles_sidebar_scope.py` | test | The sidebar's profile scope, across both endpoints that serve it. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_project_plugin_rce_bypass.py` | test | Regression coverage for GHSA-5qr3-c538-wm9j (#29156) — Remote Code | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_projects_cli.py` | test | Tests for the `hermes project` CLI dispatch (ev0_cli/projects_cmd). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_projects_db.py` | test | Tests for the per-profile Projects store (ev0_cli/projects_db). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_prompt_api_key.py` | test | Tests for ``_prompt_api_key`` — the shared Keep/Replace/Clear menu used by | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_prompt_compose_command.py` | test | Tests for the CLI `/prompt` editor-compose command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_prompt_size.py` | test | Tests for the ``hermes prompt-size`` diagnostic (issue #34667). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_provider_catalog.py` | test | Tests for the unified provider catalog (ev0_cli.provider_catalog). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_provider_config_validation.py` | test | Tests for providers config entry validation and normalization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_provider_groups.py` | test | Tests for provider-group folding (display-only picker grouping). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_provider_live_curated_merge.py` | test | Tests for live+curated merge in the generic profile-based provider path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_provider_parity.py` | test | End-to-end provider parity contract: the desktop Providers tabs must show | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_provider_precedence.py` | test | Regression tests for #29285 — provider precedence in resolve_provider("auto"). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_provider_section3_grouping.py` | test | Regression tests for section-3 (``providers:``) same-endpoint grouping in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_proxy.py` | test | Tests for the `hermes proxy` subcommand and its upstream adapters. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_psutil_android_extract.py` | test | Regression tests for the Android psutil compatibility installer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_pty_bridge.py` | test | Unit tests for ev0_cli.pty_bridge — PTY spawning + byte forwarding. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_quarantine_forensic_logging.py` | test | Redaction-safe forensic logging at the Nous OAuth quarantine path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_quarantine_noop_restore.py` | test | Regression tests for the quarantine no-op restore gap (#75584). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_read_raw_config_readonly.py` | test | Tests for read_raw_config_readonly() — the no-deepcopy raw config read. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_reasoning_effort_menu.py` | test | Python module `test_reasoning_effort_menu.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_reasoning_full_command.py` | test | Tests for the CLI `/reasoning full` / `/reasoning clamp` recap toggle. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_redact_config_bridge.py` | test | Regression test for config.yaml `security.redact_secrets: false` toggle. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_regression_16767.py` | test | Python module `test_regression_16767.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_relaunch.py` | test | Tests for ev0_cli.relaunch — unified self-relaunch utility. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_relay_shared_metrics.py` | test | Focused tests for the Hermes shared-metrics durable store. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_relay_shared_metrics_runtime.py` | test | Tests for the direct Hermes-to-Relay shared-metrics runtime. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_remote_spending_gate_contract.py` | test | Tests for the Remote-Spending gate denial contract (NAS PR #481). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_resolve_ephemeral_system_prompt.py` | test | Unit tests for resolve_ephemeral_system_prompt_from_config. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_resolve_last_session.py` | test | Verify `hermes -c` picks the session the user most recently used. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_resolve_provider_openrouter_pool.py` | test | Regression tests for issue #42130. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_resolve_token_memo.py` | test | Tests for the resolve_nous_access_token startup-burst memo (PR #66016). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_resume_latest_and_in_dir.py` | test | Tests for `--resume latest` and `--in DIR` launch sugar. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_run_with_idle_timeout.py` | test | Coverage for _run_with_idle_timeout — the streaming subprocess helper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_runtime_provider_resolution.py` | test | Python module `test_runtime_provider_resolution.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_runtime_transport_precedence.py` | test | Runtime transport precedence: declared provider transport is the fallback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_safe_mode.py` | test | Tests for `hermes chat --safe-mode` isolation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_sale_pricing.py` | test | Sale UI pricing helpers: gateway pricing.original → discount chrome. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_scan_venv_blockers.py` | test | Tests for ev0_cli/_scan_venv_blockers.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_secret_prompt.py` | test | Python module `test_secret_prompt.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_secret_source_bootstrap.py` | test | Tests for plugin secret-source first-process re-pull (#64177). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_secrets_bitwarden_non_tty.py` | test | Regression tests for hermes secrets bitwarden setup non-TTY guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_secrets_token_rotation.py` | test | Tests for `hermes secrets bitwarden token` / `hermes secrets onepassword token`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_security_advisories.py` | test | Tests for ev0_cli.security_advisories. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_security_audit.py` | test | Unit tests for ev0_cli.security_audit — parsers + OSV plumbing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_security_audit_startup.py` | test | Tests for the startup security posture audit (ev0_cli.security_audit_startup). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_send_cmd.py` | test | Tests for the ``hermes send`` CLI subcommand. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_serve_command.py` | test | Contract for the headless ``hermes serve`` backend command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_serve_parent_watchdog.py` | test | Regression tests for Desktop-owned ``hermes serve`` lifecycle tracking. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_service_manager.py` | test | Tests for ev0_cli.service_manager — the abstract ServiceManager | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_browse.py` | test | Tests for the interactive session browser (`hermes sessions browse`). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_export.py` | test | Python module `test_session_export.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_export_html.py` | test | Tests for the HTML session export renderer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_export_html_escape.py` | test | Python module `test_session_export_html_escape.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_export_md.py` | test | Python module `test_session_export_md.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_filters.py` | test | Tests for ev0_cli.session_filters — CLI time/filter parsing for | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_handoff.py` | test | Tests for session handoff (CLI to gateway platform). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_listing.py` | test | Tests for the shared session-listing helpers (ev0_cli/session_listing.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_recap.py` | test | Unit tests for ev0_cli.session_recap. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_recovery.py` | test | Python module `test_session_recovery.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_recovery_lost_and_found.py` | test | Tests for recovery-tooling gaps: issue #80205 (range-query budget can | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_session_save.py` | test | Tests for the /save current-session export helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_sessions_delete.py` | test | Python module `test_sessions_delete.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_sessions_export_md_cli.py` | test | Python module `test_sessions_export_md_cli.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_sessions_size_delta_label.py` | test | Tests for the session-store size-delta label (`hermes sessions optimize*`). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_set_config_value.py` | test | Tests for set_config_value — verifying secrets route to .env and config to config.yaml. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup.py` | test | Tests for setup.py configuration flows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_3v0_script.py` | test | Python module `test_setup_3v0_script.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_agent_settings.py` | test | Tests for agent-settings copy in the interactive setup wizard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_blank_slate.py` | test | Tests for Blank Slate setup mode (ev0_cli/setup.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_hidden_env.py` | test | Setup surfaces ask only for what a platform can't start without. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_irc.py` | test | Tests for IRC gateway configuration via `hermes setup gateway` UI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_matrix_e2ee.py` | test | Test that setup.py has shutil available for Matrix E2EE auto-install. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_model_provider.py` | test | Regression tests for interactive setup provider/model persistence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_noninteractive.py` | test | Tests for non-interactive setup and first-run headless behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_openclaw_migration.py` | test | Tests for OpenClaw migration integration in the setup wizard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_prompt_menus.py` | test | Python module `test_setup_prompt_menus.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_reconfigure.py` | test | Tests for the setup wizard's returning-user behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_summary_provider_warning.py` | test | Setup summary must warn loudly when no provider got configured. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_telemetry.py` | test | Tests for shared-metrics configuration discovery and setup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_setup_tts_xai_oauth.py` | test | Regression: TTS/setup xAI OAuth must not hijack the active chat provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_signal_handler_kanban_worker.py` | test | Regression test for #28181 — kanban worker SIGTERM must terminate the process. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_sizefmt.py` | test | Tests for the shared byte formatter (ev0_cli.sizefmt). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_skills_config.py` | test | Tests for ev0_cli/skills_config.py and skills_tool disabled filtering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_skills_hub.py` | test | Python module `test_skills_hub.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_skills_install_flags.py` | test | Tests for --yes / --force flag separation in `hermes skills install`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_skills_skip_confirm.py` | test | Tests for skip_confirm and invalidate_cache behavior in /skills install | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_skills_subparser.py` | test | Test that skills subparser doesn't conflict (regression test for #898). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_skin_cmd.py` | test | `hermes skin set` — deterministic single-color tweak of the active skin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_skin_engine.py` | test | Tests for ev0_cli.skin_engine — the data-driven skin/theme system. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_skin_palettes.py` | test | Built-in skin palette audit: completeness + WCAG contrast, per polarity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_slack_cli.py` | test | Tests for Slack CLI helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_spawn_gateway_restart_reap.py` | test | Tests for _spawn_gateway_restart orphan-reap guard (#77276). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_spotify_auth.py` | test | Python module `test_spotify_auth.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_sqlite_runtime.py` | test | Behavioral tests for exact-interpreter SQLite runtime inspection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ssh_ownership_endpoint.py` | test | Python module `test_ssh_ownership_endpoint.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_ssh_session_token_parser.py` | test | Python module `test_ssh_session_token_parser.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_startup_fast_guards.py` | test | Guards for ev0_cli._startup_fast — the pre-import version fast path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_startup_plugin_gating.py` | test | Guards for CLI startup performance regression. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_state_db_guard.py` | test | Tests for the state.db integrity guard used by the update flow (#68474). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_status.py` | test | Python module `test_status.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_status_model_provider.py` | test | Tests for ev0_cli.status model/provider display. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_status_provider_label.py` | test | `hermes status` provider label honors config.yaml model.base_url (#3296). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_stderr_timestamp.py` | test | Tests for ev0_cli.stderr_timestamp. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_stt_picker.py` | test | Tests for the Speech-to-Text category in `hermes tools` (tools_config). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_subcommands_batch.py` | test | Smoke tests for the batch-extracted subcommand parser builders. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_subcommands_followup.py` | test | Smoke tests for the Phase 2 follow-up subcommand builders (promoted handlers). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_subcommands_profile_gateway.py` | test | Unit tests for extracted subcommand parser builders (profile, gateway). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_subparser_routing_fallback.py` | test | Tests for the defensive subparser routing workaround (bpo-9338). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_subprocess_timeouts.py` | test | Tests for subprocess.run() timeout coverage in CLI utilities. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_subscription_cli.py` | test | Tests for the /subscription CLI change flow (cli.py::_show_subscription). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_suppress_eio_on_interrupt.py` | test | Tests for OSError EIO suppression during interrupt shutdown (#13710). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_system_stats_platform.py` | test | Python module `test_system_stats_platform.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_systemd_optional_directives.py` | test | Tests for systemd optional-directive normalization (issue #41119). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_systemd_watchdog_unit.py` | test | Generated service behavior for the opt-in systemd watchdog. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_teams_pipeline_plugin_cli.py` | test | Tests for the teams_pipeline plugin CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_telegram_managed_bot.py` | test | Tests for ev0_cli.telegram_managed_bot — QR codes, deep links, pairing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tencent_tokenhub_provider.py` | test | Tests for Tencent TokenHub provider support (Hy3 Preview). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_terminal_breadcrumbs.py` | test | Tests for ev0_cli/terminal_breadcrumbs.py — per-terminal ``hermes -c``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_terminal_io_broken_81521.py` | test | CLI freezes UI paints after stdout/PTY EIO (#81521). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_terminal_menu_fallbacks.py` | test | Regression tests for numbered fallbacks when the interactive curses menu | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_timeouts.py` | test | Python module `test_timeouts.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_timestamps_command.py` | test | Tests for the CLI `/timestamps` toggle and timestamps in `/history`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tips.py` | test | Tests for ev0_cli/tips.py — random tip display at session start. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tool_token_estimation.py` | test | Tests for tool token estimation and curses_ui status_fn support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tools_config.py` | test | Tests for ev0_cli.tools_config platform tool persistence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tools_disable_enable.py` | test | Tests for hermes tools disable/enable/list command (backend). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_toolset_validation.py` | test | Unit tests for ev0_cli.toolset_validation (see #38798). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tts_picker.py` | test | Tests for the TTS plugin picker surface in ev0_cli/tools_config.py (issue #30398). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tui_bundled.py` | test | Python module `test_tui_bundled.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tui_heap_sizing.py` | test | Tests for cgroup-aware TUI V8 heap sizing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tui_launcher_skips_plugin_discovery.py` | test | Regression test: the TUI launcher must not spend time on plugin discovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tui_mouse_residue_suppression.py` | test | Tests for the TUI-hot-path mouse-residue suppression. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tui_npm_install.py` | test | _tui_need_npm_install: auto npm when node_modules is behind the lockfile. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_tui_resume_flow.py` | test | Python module `test_tui_resume_flow.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_uninstall_dry_run.py` | test | Python module `test_uninstall_dry_run.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_uninstall_node_symlinks.py` | test | Tests for ev0_cli.uninstall.remove_node_symlinks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_uninstall_shell_configs.py` | test | Tests for ``remove_path_from_shell_configs`` — the uninstaller's shell-rc rewrite. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_apply_shallow_count.py` | test | Shallow-checkout guard on the `hermes update` apply path (#53479). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_autostash.py` | test | Python module `test_update_autostash.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_behind_count_recovery.py` | test | Behind-count recovery via the GitHub compare API (banner.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_bootstrap_cache_refresh.py` | test | Tests for _refresh_bootstrap_cache_scripts (the stale-installer-cache fix). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_check.py` | test | Tests for the update check mechanism in ev0_cli.banner. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_cold_start_gateway_liveness.py` | test | #84185: a Windows gateway cold-started after update that dies immediately | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_concurrent_quarantine.py` | test | Tests for issue #26670 — concurrent hermes.exe detection and improved | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_config_clears_custom_fields.py` | test | Tests for ev0_cli.auth._update_config_for_provider clearing stale fields. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_current_node_repair.py` | test | The commit_count == 0 path must repair Node deps, not just Python (#77211). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_eol_churn.py` | test | Regression: ``hermes update`` should take a managed checkout off autocrlf=true. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_fleet_restart_timeout.py` | test | Regression for #68523 — one systemctl timeout must not abort fleet restarts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_gateway_launcher_refresh.py` | test | Legacy pythonw launcher normalization + post-update launcher refresh. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_gateway_restart_aborted.py` | test | Regression for #78574 — a crashed gateway-restart phase must not stay silent. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_hangup_protection.py` | test | Tests for SIGHUP protection and stdout mirroring in ``hermes update``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_head_moved_gate.py` | test | Tests for the post-pull HEAD-movement gate in ``hermes update``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_import_guard.py` | test | Tests for the post-update *import* guard in ``hermes update``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_interrupted_recovery.py` | test | Tests for interrupted-install self-heal (the ``.update-incomplete`` marker). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_lock.py` | test | Cross-process update mutual exclusion (``ev0_cli.update_lock``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_modified_notice.py` | test | Guard: every `hermes update` path that reports user-modified skills must | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_orphan_backend_reap.py` | test | Tests for the orphaned-Desktop-backend reap in the venv-holder guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_post_pull_syntax_guard.py` | test | Tests for the post-pull syntax guard in ``hermes update``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_secret_import_lock.py` | test | Regression coverage for Windows updater self-locking native dependencies. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_self_lock.py` | test | Regression coverage for the updater self-lock deferral (#83569, #86735). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_stale_dashboard.py` | test | Tests for the stale-dashboard handling run at the end of ``hermes update``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_venv_health.py` | test | Tests for the Windows half-updated-venv hardening (July 2026 incident). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_wedged_gateway.py` | test | Tests for the wedged-gateway health probe + bounded escalation (#81642). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_yes_flag.py` | test | Tests for `hermes update --yes / -y` — assume yes for interactive prompts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_zip_atomic_replace.py` | test | Regression: the ZIP-update directory replace must never leave a half-deleted tree. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_zip_symlink_reject.py` | test | Regression: _update_via_zip must reject ZIP members with symlink mode. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_update_zip_two_phase.py` | test | Tests for the two-phase ZIP replace and the shared venv-layout helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_upstage_provider.py` | test | Focused tests for Upstage Solar first-class provider wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_urllib_security.py` | test | Wire-level tests for credential-safe stdlib urllib redirects. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_user_providers_model_switch.py` | test | Tests for user-defined providers (providers: dict) in /model. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_verify_console_scripts.py` | test | Tests for _verify_console_scripts_installed (issue #52931). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_verify_core_dependencies.py` | test | Tests for _verify_core_dependencies_installed. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_vertex_model_picker.py` | test | Vertex visibility in the /model picker (follow-up to PR #56688). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_vertex_provider.py` | test | Tests for Vertex AI runtime-provider resolution and profile registration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_video_gen_picker.py` | test | Tests for plugin video_gen providers in the tools picker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_voice_wrapper.py` | test | Tests for ``ev0_cli.voice`` — the TUI gateway's voice wrapper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_oauth_dispatch.py` | test | Regression tests for the OAuth dispatcher in ev0_cli.web_server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_profile_soul_writes.py` | test | ``PUT /api/profiles/{name}/soul`` must not destroy an existing SOUL.md. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_routers_tools_install_on_enable.py` | test | Install-on-enable for toolset toggles (dashboard/desktop PUT endpoint). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_3v0.py` | test | Tests for ev0_cli.web_server and related config utilities. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_boot_handshake.py` | test | Integration tests for the desktop boot handshake fix (PR #50231 / issue #50209). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_config_offloop.py` | test | GET /api/config must not block the event loop on _SKILLS_PROFILE_LOCK. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_console_ws.py` | test | Dashboard Hermes Console websocket tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_cron_profiles.py` | test | Regression tests for dashboard cron job profile routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_files.py` | test | Tests for the dashboard-managed file browser API. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_fs.py` | test | Python module `test_web_server_fs.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_gateway_topology.py` | test | Tests for the /api/status profile + gateway topology readout. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_git.py` | test | Python module `test_web_server_git.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_host_header.py` | test | Tests for GHSA-ppp5-vxwm-4cf7 — Host-header validation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_messaging_profiles.py` | test | Regression tests for profile-scoped dashboard Channels endpoints. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_oauth_write.py` | test | Python module `test_web_server_oauth_write.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_profile_unification.py` | test | Regression tests for the machine-dashboard multi-profile unification. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_pty_idle_backoff.py` | test | Regression: dashboard PTY pump must back off when the terminal is idle. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_pty_import.py` | test | Test the platform-branched PTY bridge import in ev0_cli.web_server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_pty_reconnect.py` | test | Focused tests for dashboard PTY reconnect breadcrumbs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_session_search.py` | test | Python module `test_web_server_session_search.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_skill_editor.py` | test | Tests for the dashboard skill editor endpoints and cron skill attachment. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_skills_profiles.py` | test | Regression tests for dashboard profile-scoped skills/toolsets management. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_server_speak_stream.py` | test | /api/audio/speak-stream — desktop streaming TTS over WebSocket. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_web_ui_build.py` | test | Tests for _web_ui_build_needed — staleness check for the web UI dist. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_webhook_cli.py` | test | Tests for ev0_cli/webhook.py — webhook subscription CLI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_whatsapp_cloud_setup.py` | test | Tests for the WhatsApp Cloud API setup wizard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_whatsapp_onboarding.py` | test | Python module `test_whatsapp_onboarding.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_whatsapp_setup_ordering.py` | test | Regression tests for ``cmd_whatsapp`` env-var write ordering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_win_pty_bridge.py` | test | Unit tests for ev0_cli.win_pty_bridge — ConPTY spawning + byte forwarding. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_windows_native_docs.py` | test | Python module `test_windows_native_docs.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_xai_curated_models.py` | test | Regression tests for xAI curated + models.dev picker-time merge. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_xai_model_flow.py` | test | Python module `test_xai_model_flow.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_xai_oauth_profile_auth.py` | test | Regression tests for xAI OAuth auth resolution in profile/cron contexts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_xai_oauth_refresh.py` | test | Python module `test_xai_oauth_refresh.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_xai_oauth_writethrough.py` | test | Regression tests for xAI OAuth refresh write-through to the global root. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_xai_provider_labels.py` | test | Regression tests for xAI provider label disambiguation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_xai_retirement.py` | test | Unit tests for ev0_cli.xai_retirement (May 15, 2026 model retirement). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_xiaomi_provider.py` | test | Tests for Xiaomi MiMo provider support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_cli/test_yolo_startup_order.py` | test | Regression tests for #60328: --yolo must set HERMES_YOLO_MODE in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_append_messages_batch.py` | test | Tests for SessionDB.append_messages_batch (#23254 salvage). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_aux_usage_accounting.py` | test | Tests for auxiliary usage accounting (issue #23270). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_conversation_root.py` | test | Tests for SessionDB.get_conversation_root — stable conversation id resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_get_anchored_view.py` | test | Tests for SessionDB.get_anchored_view — anchored window + session bookends. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_get_messages_around.py` | test | Tests for SessionDB.get_messages_around (anchored-window primitive). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_get_messages_include_compacted.py` | test | Tests for SessionDB.get_messages(include_compacted=...). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_isolation_marker_env.py` | test | Subprocess-surviving isolation marker (#82770). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_live_db_guard_ancestry.py` | test | The live-DB guard must survive a scrubbed child environment (#82770). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_live_db_isolation_guard.py` | test | Behavioral tests for the live-DB test-isolation guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_never_active_keyed_prune.py` | test | Sweeping never-active keyed gateway rows (#82770). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_orphan_gateway_session_repair.py` | test | Repair of gateway sessions that lost their routing identity (#82616). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_reasoning_roundtrip.py` | test | Round-trip tests for the structured reasoning columns. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_replace_messages_archive_siblings.py` | test | Sibling-site regression tests for the #80216 bug class. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_resolve_resume_session_id.py` | test | Regression guard for #15000: --resume <id> after compression loses messages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_restore_alternation_repair.py` | test | get_messages_as_conversation(repair_alternation=True) — heal durable | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_session_archiving.py` | test | Python module `test_session_archiving.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_session_hidden.py` | test | Python module `test_session_hidden.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_session_lifecycle_status.py` | test | Lifecycle status classification for session pickers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_session_md_export.py` | test | Python module `test_session_md_export.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/ev0_state/test_session_read_state.py` | test | Python module `test_session_read_state.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/fakes/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/fakes/fake_ha_server.py` | test | Fake Home Assistant server for integration testing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/fixtures/cua_driver_0_9_tools_list.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `tests/fixtures/plugins/example-dashboard/dashboard/manifest.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `tests/fixtures/plugins/example-dashboard/dashboard/plugin_api.py` | test | Example dashboard plugin — backend API routes (test fixture). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/fixtures/session-resume-active-turn.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `tests/gateway/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/_plugin_adapter_loader.py` | test | Shared helper for loading platform-plugin ``adapter.py`` modules in tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/conftest.py` | test | Shared fixtures for gateway tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/feishu_helpers.py` | test | Shared fixtures for Feishu adapter tests (admission, group policy, dispatch). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/platforms/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/platforms/test_yuanbao_recall_db_only.py` | test | Yuanbao recall: branch A1 (exact id) and A2 (content-match) against DB-only transcripts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/platforms/test_yuanbao_state_cleanup.py` | test | Yuanbao per-turn state cleanup: RecallGuard tracking dicts + member cache TTL. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/stub_connector.py` | test | Test-only in-memory stub connector implementing RelayTransport. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_auth.py` | test | Unit tests for gateway/relay/auth.py — the gateway-side relay auth primitives. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_channel_context_consume.py` | test | Unit tests for relay channel-context consumption (design relay-channel-context). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_contract_doc_conformance.py` | test | Cross-repo contract conformance: docs/relay-connector-contract.md ⟷ Python. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_descriptor.py` | test | Tests for the experimental CapabilityDescriptor (relay Phase 0, Task 0.2). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_descriptor_from_entry.py` | test | Descriptor <- PlatformEntry projection (relay Phase 0, Task 0.3). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_handoff_relay_aliasing.py` | test | Unit tests for /handoff platform aliasing over relay (Phase 1 parity). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_identity_token_resolver.py` | test | Unit tests for the generic-OIDC / Nous-Portal caller-identity token resolver. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_no_stub_leak.py` | test | CI guard: the test-only StubConnector must never leak into production paths. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_adapter.py` | test | RelayAdapter capability-advertisement tests (relay Phase 1, Task 1.1). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_follow_up.py` | test | A2 outbound capability action: the token-less ``follow_up`` op. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_going_idle.py` | test | Phase 5 §5.3 — going-idle / buffered-flip primitive (gateway side). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_interactive.py` | test | Relay Phase 3 interactive tests — prompt op egress, prompt_response | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_interrupt.py` | test | Relay /stop interrupt routing (relay Phase 1, Task 1.4). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_media.py` | test | Relay Phase 2 media tests — send_media egress lanes + inbound media localization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_multiplatform.py` | test | Unit tests for Phase 1.5 multi-platform-per-agent (relay). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_passthrough.py` | test | Relay passthrough-over-WS forwarding (Phase 5 §5.1). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_per_platform_caps.py` | test | Per-platform capability descriptors on the relay (multi-platform Phase 1.5). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_policy_send.py` | test | Unit tests for the gateway-side relay relevance-policy declaration (Phase 6 ζ). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_registration.py` | test | RelayAdapter registration via the platform registry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_roundtrip.py` | test | End-to-end relay round-trip against the in-memory stub connector. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_roundtrip_telegram.py` | test | End-to-end relay round-trip for Telegram against the in-memory stub. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_sheds_crypto.py` | test | Invariant: the relay path sheds platform crypto — it re-validates nothing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_slack_dm_streaming.py` | test | Slack relay: edit-based streaming of the reply must fire in a DM. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_slack_prompt_dm_root.py` | test | Slack relay: interactive prompts follow the turn's thread stamp. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_relay_threads.py` | test | Relay Phase 4 tests — thread lifecycle ops, reply_to enrichment parse, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_self_provision.py` | test | Unit tests for boot-time relay self-provisioning. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_wire_user_identity.py` | test | Unit tests for relay wire-field hygiene (Phase 1 parity). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/relay/test_ws_transport.py` | test | WebSocketRelayTransport against a real in-process WebSocket server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/restart_test_helpers.py` | test | Python module `restart_test_helpers.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_10710_auto_reset_evicts_cached_agent.py` | test | Regression test for #10710 — stale context summary leak after auto-reset. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_13121_shutdown_inflight_transcript_flush.py` | test | Regression tests for #13121 — gateway restart/shutdown must persist an | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_25107_stale_base_url_api_mode.py` | test | Regression tests for #25107: gateway /model switch left a stale | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_35809_auto_reset_clean_context.py` | test | Regression tests for #35809 — compression-exhaustion auto-reset loop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_35994_reset_button_deadlock.py` | test | Regression test for #35994: Telegram /new confirm-button deadlock. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_42039_duplicate_user_message.py` | test | Tests for #42039 — user messages stored twice in state.db. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_48031_model_switch_after_auto_reset.py` | test | Regression test for #48031 — /model switch lost after session auto-reset. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_53175_cleanup_off_loop.py` | test | Regression test for #53175: gateway event loop wedged by synchronous | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_64674_multiplex_primary_token_scope.py` | test | #64674 — multiplex primary gateway must not fail forever without bot tokens. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_7100_transient_failure_transcript.py` | test | Tests for #7100 — transient failures (429/timeout) must not drop the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_71671_faulthandler_no_stderr.py` | test | Regression: #71671 — gateway must survive faulthandler.enable() with sys.stderr=None. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_73297_memory_flush_on_reset.py` | test | Regression tests for #73297: memory rollback after /reset. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_73771_media_resend_dedup.py` | test | Regression tests for #73771 — session-wide MEDIA dedup swallowing | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_75349_whatsapp_multiplex_secret_scope.py` | test | Regression test for #75349 — WhatsApp bridge loses WHATSAPP_* vars under multiplex. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_abandoned_turn_process_cleanup.py` | test | Regression coverage for abandoned gateway-turn subprocess cleanup (#76115). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_active_session_text_merge.py` | test | Regression tests for active-session TEXT follow-up queueing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_active_turn_recovery.py` | test | Regression tests for exact durable active-turn restart recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_adapter_connect_classification.py` | test | Connect-failure classification + reconnect-queue escalation (OOF-156). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_adapter_connect_is_reconnect_contract.py` | test | Regression: every platform adapter's ``connect()`` must accept the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_adapter_startup_secret_scope.py` | test | Regression tests — Slack-pattern scoped credential reads at adapter startup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_agent_cache.py` | test | Integration tests for gateway AIAgent caching. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_agent_cache_pressure.py` | test | Memory-pressure eviction for the gateway agent cache (#80764). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_agents_command_delegations.py` | test | Gateway /agents surfaces background delegations with live activity (#51690). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_aiohttp_body_caps.py` | test | Regression tests: aiohttp servers must set an explicit ``client_max_size``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_allowed_channels_widening.py` | test | Tests for the allowed_{channels,chats,rooms} whitelist extension | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_allowlist_startup_check.py` | test | Tests for the startup allowlist warning check in gateway/run.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server.py` | test | Tests for the OpenAI-compatible API server gateway adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_active_work_drain.py` | test | Regression coverage for #63529 API-server shutdown draining. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_bind_guard.py` | test | Tests for the API server bind-address startup guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_jobs.py` | test | Tests for the Cron Jobs API endpoints on the API server adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_media_data_urls.py` | test | MEDIA: tag → base64 data-URL resolution for the API server (salvage of #2696). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_multimodal.py` | test | End-to-end tests for inline image inputs on /v1/chat/completions and /v1/responses. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_multiplex_secret_scope.py` | test | Regression for #61276: api_server agent entry under multiplex isolation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_normalize.py` | test | Tests for _normalize_chat_content in the API server adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_runs.py` | test | Tests for /v1/runs endpoints: start, status, events, steer, and stop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_api_server_toolset.py` | test | Tests for hermes-api-server toolset and API server tool availability. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_approval_prompt_redaction.py` | test | Regression test for approval prompt credential redaction (issue #48456). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_approvals_command.py` | test | Gateway contract and live dispatch for /approvals. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_approve_deny_commands.py` | test | Tests for /approve and /deny gateway commands. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_async_delegation_session_binding.py` | test | Gateway-side session binding for async delegations (#57498, #55578). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_async_delivery_capability.py` | test | Tests for the async-delivery capability gate (issue #10760). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_async_session_db.py` | test | AsyncSessionDB offload facade + gateway raw-call guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_async_session_store.py` | test | Async SessionStore boundary for gateway event-loop safety. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_audio_cache.py` | test | Tests for audio cache utilities in gateway/platforms/base.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_auth_fallback.py` | test | Test that AuthError triggers fallback provider resolution (#7230). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_auto_continue.py` | test | Tests for the auto-continue feature (#4493 / #45232). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_auto_voice_reply_format.py` | test | Tests for gateway auto-TTS voice reply audio format selection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_background_command.py` | test | Tests for /background gateway slash command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_background_process_notifications.py` | test | Tests for configurable background process notification modes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_base_auto_tts_output_format.py` | test | Base-adapter auto-TTS must pass a platform-aware explicit output path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_base_topic_sessions.py` | test | Tests for BasePlatformAdapter topic-aware session handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_baseexception_turn_notify.py` | test | Regression: _process_message_background must notify the user when a turn | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_bluebubbles.py` | test | Tests for the BlueBubbles iMessage gateway adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_bounded_adapter_teardown.py` | test | Regression tests: the shutdown teardown loop must not hang on a wedged adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_branch_routing_columns.py` | test | Regression test for /branch losing gateway routing columns (#NNNNN). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_bundles_command.py` | test | Tests for the ``/bundles`` gateway slash command handler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_busy_session_ack.py` | test | Tests for busy-session acknowledgment when user sends messages during active agent runs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_busy_session_auth_bypass.py` | test | Tests for #17775: unauthorized users must be blocked in the busy-session path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_buzz_adapter.py` | test | Tests for the Buzz platform adapter plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_buzz_websocket.py` | test | Tests for the Buzz WebSocket transport (NIP-42) and Nostr signing module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cached_agent_history_guard.py` | test | Regression tests for cached gateway transcript selection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cached_agent_max_iterations.py` | test | Regression tests for PR #48127: cached agent max_iterations refresh. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cancel_background_drain.py` | test | Regression test: cancel_background_tasks must drain late-arrival tasks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cgroup_cleanup.py` | test | Tests for the systemd ExecStopPost cgroup reaper (issue #37454). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_channel_continuity_hint.py` | test | Tests for the lightweight Slack/Discord channel session-continuity hint. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_channel_directory.py` | test | Tests for gateway/channel_directory.py — channel resolution and display. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_channel_directory_connected_only.py` | test | Session-based channel discovery must not resurrect disconnected platforms. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_channel_overrides.py` | test | Tests for per-channel model and system prompt overrides (Fixes #1955). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_checkpoint_config.py` | test | Runtime coverage for gateway filesystem-checkpoint configuration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_choice_picker.py` | test | Tests for the gateway interactive choice picker (/reasoning, /fast). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cjk_fts_config_bridge.py` | test | config.yaml sessions.* bridges for the search-index knobs (config-authoritative). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_clarify_active_session_bypass.py` | test | Regression tests for clarify replies while a gateway session is busy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_clarify_progress_leak.py` | test | Regression tests for #52374 — raw clarify tool-call JSON must never leak | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_clarify_thread_followup_not_swallowed.py` | test | Regression tests for #62034 — pending multi-choice clarify prompts must not | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_clean_shutdown_marker.py` | test | Tests for the clean shutdown marker that prevents unwanted session auto-resets. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_code_fence_tracking.py` | test | Tests for code fence tracking across message split / truncation / streaming paths. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_command_bypass_active_session.py` | test | Regression tests: slash commands must bypass the base adapter's active-session guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_complete_path_at_filter.py` | test | Regression tests for the TUI gateway's `complete.path` handler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_completion_delivery.py` | test | Lifecycle-scoped gateway delivery regressions for terminal completions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_completion_session_boundary.py` | test | Session-boundary gating for background-process completion delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compress_command.py` | test | Tests for gateway /compress user-facing messaging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compress_focus.py` | test | Tests for gateway /compress <focus> — focus topic on the gateway side. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compress_plugin_engine.py` | test | Regression test: /compress works with context engine plugins. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compress_preview.py` | test | Tests for gateway /compress --preview/--dry-run/--aggressive flags | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compression_concurrent_sessions.py` | test | Behavioral tests for concurrent compression across distinct and shared sessions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compression_deferred_soft_result.py` | test | Gateway must treat ``compression_deferred`` as a soft result (#49874). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compression_failure_session_sync.py` | test | Python module `test_compression_failure_session_sync.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compression_in_flight_check.py` | test | #5 regression: _session_has_compression_in_flight must offload both blocking sources to thread pool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compression_interrupt_demotion_56391.py` | test | Regression tests for #56391. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compression_progress_notices.py` | test | Opt-in compression progress notices on chat gateways (#52995). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_compression_session_id_persistence.py` | test | Regression tests for #29335 — gateway must persist ``session_entry.session_id`` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_config.py` | test | Tests for gateway configuration management. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_config_cwd_bridge.py` | test | Tests for the config.yaml → env var bridge logic in gateway/run.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_config_driven_access_policy.py` | test | Tests for config-driven platform access policies at the gateway layer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_config_env_bridge_authority.py` | test | Regression tests for the config.yaml → env var bridge in gateway/run.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_context_ref_expansion_runtime.py` | test | Regression test for the "@" context-reference-expansion block in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_conversation_scope_funnel.py` | test | Behavior tests for _clear_conversation_scope — the single conversation- | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cron_active_work_drain.py` | test | Tests for #60432: the gateway shutdown drain was structurally blind to | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cron_drain_floor.py` | test | Regression tests for #82161. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cron_fire_webhook.py` | test | Tests for the Chronos cron-fire webhook (POST /api/cron/fire) — Phase 4E.2. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cron_interrupt_notification.py` | test | Regression tests for #82232. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cron_shutdown_drain.py` | test | Regression tests for #58818. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_cwd_placeholder.py` | test | Unit tests for gateway.cwd_placeholder.resolve_placeholder_terminal_cwd. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_dead_targets.py` | test | Tests for confirmed-dead delivery-target short-circuiting (deleted Telegram | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_debug_command.py` | test | Tests for the gateway /debug command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_dedupe_user_turns.py` | test | Regression tests for issue #47237. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_delegation_session_id_leak.py` | test | Delegated children must not replace their parent's session identity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_delivery.py` | test | Tests for the delivery routing module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_delivery_ledger.py` | test | Tests for the gateway delivery-obligation ledger (gateway/delivery_ledger.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_delivery_ledger_fd_leak.py` | test | Regression: the gateway delivery ledger must close every SQLite connection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_delivery_ledger_producer.py` | test | Producer-hook tests: _process_message_background records delivery | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_delivery_silence_filter.py` | test | Tests for the outbound silence-narration filter (anti-loop control). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_destructive_slash_always_persist_report.py` | test | Answering "Always Approve" must not claim an opt-out that was not saved. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_destructive_slash_confirm.py` | test | Tests for the gateway's destructive-slash-confirm wrapper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_diff_command.py` | test | End-to-end tests for the gateway ``/diff`` command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_dingtalk.py` | test | Tests for DingTalk platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_allowed_channels.py` | test | Regression guard for #14920: wildcard "*" in Discord channel config lists. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_allowed_mentions.py` | test | Tests for the Discord ``allowed_mentions`` safe-default helper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_approval_mentions.py` | test | Discord approval prompts can opt into owner mentions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_attachment_download.py` | test | Tests for Discord attachment downloads via the authenticated bot session. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_bot_auth_bypass.py` | test | Regression guard for #4466: DISCORD_ALLOW_BOTS works without DISCORD_ALLOWED_USERS. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_bot_filter.py` | test | Tests for Discord bot message filtering (DISCORD_ALLOW_BOTS). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_channel_controls.py` | test | Tests for Discord ignored_channels and no_thread_channels config. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_channel_prompts.py` | test | Tests for Discord channel_prompts resolution and injection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_channel_skills.py` | test | Tests for Discord channel_skill_bindings auto-skill resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_clarify_buttons.py` | test | Tests for Discord clarify button rendering and resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_component_auth.py` | test | Security regression tests: Discord component views honor allowlists. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_connect.py` | test | Python module `test_discord_connect.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_document_handling.py` | test | Tests for Discord incoming document/file attachment handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_double_dispatch.py` | test | Tests for Discord double-dispatch prevention (#51057). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_edit_message_overflow.py` | test | Regression tests for Discord oversized edit_message split-and-deliver. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_exec_approval_content.py` | test | Python module `test_discord_exec_approval_content.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_fail_closed_feedback.py` | test | Python module `test_discord_fail_closed_feedback.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_format.py` | test | Discord format_message: tables converted to bullet groups. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_free_response.py` | test | Tests for Discord free-response defaults and mention gating. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_imports.py` | test | Import-safety tests for the Discord gateway adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_lazy_install_views.py` | test | Regression: Discord UI view classes must be defined after lazy-install. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_liveness.py` | test | Regression tests for Discord Gateway WebSocket liveness. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_media_metadata.py` | test | Python module `test_discord_media_metadata.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_missed_message_backfill.py` | test | Tests for Discord missed-message startup backfill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_model_picker.py` | test | Regression tests for the Discord /model picker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_opus.py` | test | Tests for Discord Opus codec loading — must use ctypes.util.find_library. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_pending_text_batch_shutdown.py` | test | Regression guard for Discord text-batch flush during gateway shutdown. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_platform_events.py` | test | Discord ``gateway_platform_event`` fire-sites (#64176 remaining scope). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_plugin_setup.py` | test | Tests for the Discord plugin's interactive_setup wizard home-channel flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_prompt_content_siblings.py` | test | Sibling coverage for the embed-invisibility fix (send_exec_approval got it | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_prompt_timeout_config.py` | test | Tests for the configurable Discord interactive-view timeout. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_race_polish.py` | test | Discord adapter race polish: concurrent join_voice_channel must not | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_reactions.py` | test | Tests for Discord message reactions tied to processing lifecycle hooks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_reply_mode.py` | test | Tests for Discord reply_to_mode functionality. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_roles_dm_scope.py` | test | Regression guard: DISCORD_ALLOWED_ROLES must be guild-scoped, not global. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_send.py` | test | Python module `test_discord_send.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_slash_auth.py` | test | Security regression tests: slash commands honor on_message authorization gates. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_slash_commands.py` | test | Tests for native Discord slash command fast-paths (thread creation & auto-thread). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_split_cap.py` | test | Regression tests for the Discord split-delivery cap (issue #86581). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_sync_limit.py` | test | Test Discord slash command sync respects the 100-command hard limit. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_system_messages.py` | test | Tests for Discord system message filtering (thread renames, pins, etc.). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_thread_persistence.py` | test | Tests for Discord thread participation persistence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_thread_slash_expired_defer.py` | test | Sibling coverage for expired slash defer handling: /thread creation must | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_discord_voice_mixer.py` | test | Tests for the Discord continuous voice mixer (ambient + ducked speech) | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_disk_status.py` | test | Tests for gateway.disk_status — the /api/status disk rollup (NS-656). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_display_config.py` | test | Tests for gateway.display_config — per-platform display/verbosity resolver. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_dm_topics.py` | test | Tests for Telegram DM Private Chat Topics (Bot API 9.4). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_document_cache.py` | test | Tests for document cache utilities in gateway/platforms/base.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_document_context_note.py` | test | Tests for the document context note prepended to user turns with attachments. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_duplicate_reply_suppression.py` | test | Tests for duplicate reply suppression across the gateway stack. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_email.py` | test | Tests for the Email gateway platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_email_charset_fallback.py` | test | Email charset robustness: unknown/malformed charsets must never drop mail. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_email_robustness.py` | test | Email adapter robustness against malformed IMAP responses (salvage of #2794). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_email_secret_scope.py` | test | Tests for email adapter credential isolation under multiplexing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_empty_model_recovery.py` | test | Regression tests for #35314 — empty model on the post-interrupt recovery turn. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_env_flag_truthy.py` | test | Env flags accept 'on' as truthy consistently (salvage of #2863). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_ephemeral_reply.py` | test | Tests for EphemeralReply — system-notice auto-delete in gateway adapters. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_escape_reasoning_fences.py` | test | Tests for escape_code_fences_for_display. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_external_drain_control.py` | test | Tests for the external drain-control marker contract + gateway state machine. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_extract_local_files.py` | test | Tests for extract_local_files() — auto-detection of bare local file paths | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_fallback_chain_reload.py` | test | Regression tests for #60955: gateway must not freeze fallback_providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_fallback_eviction.py` | test | Tests for fallback-eviction gating on failed runs (#7130). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_fast_command.py` | test | Tests for gateway /fast support and Priority Processing routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu.py` | test | Tests for the Feishu gateway integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_approval_buttons.py` | test | Tests for Feishu interactive card approval buttons. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_bot_admission.py` | test | Adapter-layer tests for Feishu bot-sender admission (``FeishuAdapter._admit``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_bot_auth_bypass.py` | test | Regression guard for Feishu bot-sender authorization bypass. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_channel_prompts.py` | test | Tests for Feishu per-channel prompt resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_comment.py` | test | Tests for feishu_comment — event filtering, access control integration, wiki reverse lookup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_comment_rules.py` | test | Tests for feishu_comment_rules — 3-tier access control rule engine. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_lazy_import.py` | test | Regression coverage for deferred Feishu SDK loading. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_meeting_invite.py` | test | Tests for Feishu vc.bot.meeting_invited_v1 event handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_onboard.py` | test | Tests for plugins.platforms.feishu.adapter — Feishu scan-to-create registration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_sdk_executor.py` | test | Regression tests for the Feishu adapter's owned SDK executor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_table_markdown.py` | test | Tests for Feishu adapter outbound markdown payload construction. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_feishu_voice_message_type.py` | test | Regression tests for Feishu native voice-note classification. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_fence_chunker.py` | test | Invariant tests for the shared fence-aware markdown chunker core. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_finalize_session_off_loop.py` | test | Session-finalize plugin hooks must not block the gateway event loop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_first_turn_session_meta_rebaseline.py` | test | Regression: first-turn ``session_meta`` row must be re-baselined into the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_footer_command_mid_run.py` | test | Regression: /footer must dispatch to its handler while an agent is running. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_fresh_reset_skill_injection.py` | test | Regression tests for topic/channel skill auto-injection after /new or /reset. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_command_dispatch_minimal.py` | test | Python module `test_gateway_command_dispatch_minimal.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_command_help.py` | test | Gateway command help rendering tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_command_line_matcher.py` | test | Tests for the strict gateway command-line matcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_inactivity_timeout.py` | test | Tests for staged inactivity timeout in gateway agent runs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_platform_event_hook.py` | test | Tests for the ``gateway_platform_event`` observer hook (#64176's observer half). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_process_exit.py` | test | Python module `test_gateway_process_exit.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_shutdown.py` | test | Python module `test_gateway_shutdown.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_silence_tokens.py` | test | Gateway intentional-silence token behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_gateway_utf8_encoding.py` | test | Static guard: every ``read_text`` / ``write_text`` call in the gateway and | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_goal_continuation_drain.py` | test | Regression: /goal continuations enqueued via the adapter FIFO are drained | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_goal_max_turns_config.py` | test | Python module `test_goal_max_turns_config.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_goal_status_notice.py` | test | Python module `test_goal_status_notice.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_goal_verdict_send.py` | test | Tests for gateway /goal verdict-message delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_google_chat.py` | test | Tests for Google Chat platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_google_chat_oauth_dependencies.py` | test | Security-floor tests for the Google Chat runtime installer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_handoff_thread_session_key.py` | test | Regression: CLI→Discord handoff must key a thread destination on the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_handoff_watcher_async_db.py` | test | Regression test for #40695 (salvage of keystone PR #40782). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_history_media_current_turn.py` | test | Regression: current-turn TTS media must not be dedup-stripped (#B, staging 2026-07-29). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_home_target_env_var.py` | test | Regression tests for /sethome env-var resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_homeassistant.py` | test | Tests for the Home Assistant gateway adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_hooks.py` | test | Tests for gateway/hooks.py — event hook system. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_hygiene_failure_cooldown_ladder.py` | test | Session-hygiene compression must escalate its cooldown for repeat failures. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_image_input_routing_runtime.py` | test | Python module `test_image_input_routing_runtime.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_incomplete_gateway_turns.py` | test | Regression tests for hidden-reasoning-only incomplete gateway turns. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_insights_unicode_flags.py` | test | Tests for Unicode dash normalization in /insights command flag parsing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_interactive_prompt_base.py` | test | Tests for the shared interactive-prompt formatting cores in BasePlatformAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_internal_event_bypass_pairing.py` | test | Tests that internal synthetic events (e.g. background process completion) | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_internal_event_never_interrupts_busy_session.py` | test | Regression test: internal synthetic events must never interrupt a busy session. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_internal_notification_marker_82888.py` | test | Regression tests for #82888 — internal synthetic turns are persisted typed. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_interrupt_key_match.py` | test | Tests verifying interrupt key consistency between adapter and gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_irc_adapter.py` | test | Tests for the IRC platform adapter plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_auto_decompose_live.py` | test | Tests for live auto-decompose settings resolution (issue #49638). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_notifier.py` | test | Python module `test_kanban_notifier.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_notifier_apiserver_wake.py` | test | Kanban notifier behavior on stateless (api_server) subscriptions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_notifier_wake_only_ordering.py` | test | Wake-only (delivery_mode='wake') push-adapter delivery ordering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_notifier_watcher_dispatch_gate.py` | test | Notifier polling stays active when another gateway owns dispatching. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_notifier_zero_sub_gate.py` | test | Tests for the kanban notifier zero-subscription early exit. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_reconcile_orphans.py` | test | Tests: orphaned-card reconciliation for the kanban dispatcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_wake_scope.py` | test | Kanban wake events must key to the same session as inbound messages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_kanban_watchers_mixin.py` | test | Tests for the extracted GatewayKanbanWatchersMixin (god-file Phase 3). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_keep_typing_timeout.py` | test | Tests for BasePlatformAdapter._keep_typing timeout-per-tick behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_lifecycle_ledger.py` | test | Tests for gateway.lifecycle_ledger — unclean-shutdown detection (NS-608). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_line_plugin.py` | test | Tests for the LINE platform adapter plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_load_transcript_db_only.py` | test | Verify load_transcript returns SQLite messages without any JSONL file. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_local_model_connection_reply.py` | test | Regression tests for #86570: gateway provider error connection messaging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_loop_command.py` | test | Gateway /loop command tests — dispatch, routing capture, mid-run guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_loop_exception_handler.py` | test | Tests for the gateway loop-level transient-network-error safety net. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_loop_liveness_watchdog.py` | test | Gateway event-loop freeze backstops for issue #69089. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix.py` | test | Tests for Matrix platform adapter (mautrix-python backend). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_approval_reaction_fail_closed.py` | test | Tests for Matrix adapter fail-closed approval reaction auth. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_dm_invite_recording.py` | test | Tests for Matrix DM room recording on invite (issue #44679). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_exec_approval.py` | test | Python module `test_matrix_exec_approval.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_mention.py` | test | Tests for Matrix require-mention gating and auto-thread features. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_message_event_metadata.py` | test | Tests for Matrix MessageEvent metadata (sender, reply context). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_message_length.py` | test | Tests for Matrix outbound message length configuration (#53026). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_plugin_setup.py` | test | Tests for the Matrix plugin's interactive_setup wizard home-channel flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_project_context_isolation.py` | test | Matrix Project A / Project B context-isolation regressions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_recovery_key_scope.py` | test | Regression test for #69090: MATRIX_RECOVERY_KEY must honor the active | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_matrix_voice.py` | test | Tests for Matrix voice message support (MSC3245). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_mattermost.py` | test | Tests for Mattermost platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_mattermost_plugin_setup.py` | test | Tests for the Mattermost plugin's interactive_setup wizard home-channel flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_max_concurrent_sessions.py` | test | Tests for the gateway max_concurrent_sessions active-session cap. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_max_tokens_propagation.py` | test | Regression tests for max_tokens propagation from config.yaml to AIAgent. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_mcp_reload_refreshes_cached_agents.py` | test | Regression test for /reload-mcp refreshing cached agent tool lists. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_media_cache.py` | test | Contract tests for gateway.platforms.media_cache — the shared mime↔ext | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_media_download_retry.py` | test | Tests for media download retry logic added in PR #2982. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_media_extraction.py` | test | Tests for MEDIA tag extraction from tool results. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_media_metadata_contract.py` | test | Contract: media-send overrides must accept the ``metadata`` kwarg. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_media_spaced_paths_and_history_dedupe.py` | test | Regression tests: spaced paths, GIS extensions, cross-turn dedupe plumbing, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_media_tag_cleanup.py` | test | Tests for MEDIA_TAG_CLEANUP_RE regex matching behavior (#63632). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_media_tag_formatting_variants.py` | test | Regression tests: MEDIA tag formatting variants that previously broke delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_media_tag_separator.py` | test | Regression tests for #68773 — MEDIA tags without a separator merge paths. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_memory_monitor.py` | test | Tests for gateway.memory_monitor — periodic process memory logging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_memory_status.py` | test | Tests for gateway.memory_status — the /api/status memory rollup (NS-656). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_memory_trim_housekeeping.py` | test | Memory-trim coverage for the long-lived messaging gateway housekeeper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_message_deduplicator.py` | test | Tests for MessageDeduplicator TTL enforcement (#10306). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_message_timestamps.py` | test | Python module `test_message_timestamps.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_mirror.py` | test | Tests for gateway/mirror.py — session mirroring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_mixed_attachment_routing.py` | test | Regression tests for mixed-attachment routing in gateway/run.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_moa_one_shot_restore.py` | test | MoA one-shot model override must be restored on both success and failure. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_model_command_async_offload.py` | test | Regression tests for #41289: the Discord/Telegram ``/model`` slash command | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_model_command_context_offload.py` | test | ``/model`` context-length resolution must not block the gateway event loop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_model_command_custom_providers.py` | test | Regression tests for gateway /model support of config.yaml custom_providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_model_command_expensive_confirm.py` | test | Gateway typed ``/model <name>`` must route through the expensive-model | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_model_command_flat_string_config.py` | test | Regression tests for gateway /model --global persistence when config.yaml | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_model_command_profile_config.py` | test | Regression coverage for profile-scoped gateway ``/model`` reads. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_model_picker_persist.py` | test | Regression tests for gateway inline-keyboard model-picker persistence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_model_switch_persistence.py` | test | Tests that gateway /model switch persists across messages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_msgraph_webhook.py` | test | Tests for the Microsoft Graph webhook adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_adapter_registry.py` | test | Phase 3: secondary-profile adapter registry + same-token conflict detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_api_server_routing.py` | test | Multiplex /p/<profile>/ routing for the api_server adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_background_task_scope.py` | test | Regression: background tasks respect profile secret scope when multiplexing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_busy_input_mode.py` | test | Profile-specific busy-input behavior for multiplexed gateways. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_credential_isolation.py` | test | End-to-end credential isolation proof for multiplex mode (Workstream A). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_http_routing.py` | test | Phase 1: HTTP-inbound /p/<profile>/ routing for the webhook adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_lifecycle.py` | test | Phase 4: lifecycle guard + per-profile observability. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_pairing_stores.py` | test | Regression: per-profile PairingStore creation in _start_secondary_profile_adapters. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_phase0.py` | test | Phase 0 foundations for multi-profile gateway multiplexing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_multiplex_profile_authz.py` | test | Regression tests for multiplex profile-aware own-policy authorization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_native_image_buffer_isolation.py` | test | Python module `test_native_image_buffer_isolation.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_new_clears_last_resolved_model.py` | test | Regression tests for #58403 — /new must clear _last_resolved_model cache. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_normalize_empty_agent_response.py` | test | Unit tests for persistence-failure-aware messaging in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_notice_delivery.py` | test | Python module `test_notice_delivery.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_notice_rendering.py` | test | Unit tests for messaging-gateway credit-notice rendering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_notify_fatal_error_shield.py` | test | Regression test for #81335 — fatal-error handler must survive cancellation | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_ntfy_plugin.py` | test | Tests for the ntfy platform-plugin adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_own_policy_startup_gate.py` | test | Regression tests for own-policy open startup gate in gateway/run.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_pairing.py` | test | Tests for gateway/pairing.py — DM pairing security system. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_pairing_allowlist_bypass.py` | test | Pairing store <-> allowlist consolidation (#23778). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_pending_drain_no_recursion.py` | test | Regression test for #17758 — chained pending-message drains must not | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_pending_drain_race.py` | test | Regression tests: pending-drain + finally-cleanup races must not spawn | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_pending_event_none.py` | test | Tests for pending follow-up extraction in recursive _run_agent calls. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_pending_queue_spool.py` | test | Regression tests for runtime spool-on-drop of the pending transcript queue. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_per_platform_streaming_defaults.py` | test | Per-platform streaming defaults + dashboard exposure. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_pii_redaction.py` | test | Tests for PII redaction in gateway session context prompts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_plaintext_approval_routing.py` | test | Tests for #46866: plain-text approval responses must resolve a blocking | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_planned_stop_watcher.py` | test | Tests for the planned-stop marker watcher thread (gateway/run.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_platform_base.py` | test | Tests for gateway/platforms/base.py — MessageEvent, media extraction, message truncation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_platform_connected_checkers.py` | test | Verify that every gateway platform — built-in and plugin — has a connection | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_platform_http_client_limits.py` | test | Tests for the shared httpx.Limits helper that all long-lived platform | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_platform_reconnect.py` | test | Tests for the gateway platform reconnection watcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_platform_reconnect_fd_leak.py` | test | Regression tests for the gateway platform fd-leak fix (#37011). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_platform_registry.py` | test | Tests for the platform adapter registry and dynamic Platform enum. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_plugin_message_injection.py` | test | Tests for plugin-triggered turns in existing gateway sessions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_plugin_platform_interface.py` | test | Interface compliance tests for all plugin-based gateway platforms. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_poller_fd_lifecycle.py` | test | Poller socket lifecycle — proxied fd-leak regressions (#79889). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_post_delivery_callback_chaining.py` | test | Tests for ``BasePlatformAdapter.register_post_delivery_callback`` chaining. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_post_stream_media_delivery.py` | test | Post-stream media delivery is explicit-only (#20834). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_pre_gateway_dispatch.py` | test | Tests for the pre_gateway_dispatch plugin hook. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_priority_path_compression_demotion_56391.py` | test | Regression test: the ``_handle_message`` PRIORITY busy-path must also | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_profile_resolution.py` | test | Tests for GatewayRunner._resolve_profile_home_for_source — profile resolution logic. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_profile_routing.py` | test | Tests for gateway/profile_routing.py — profile-based routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_prompt_tail_freeze.py` | test | Byte-stable gateway system prompts (the ephemeral session-context pin). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_proxy_mode.py` | test | Tests for gateway proxy mode — forwarding messages to a remote API server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_qqbot.py` | test | Tests for the QQ Bot platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_qqbot_credential_isolation.py` | test | Credential isolation for the QQ (qqbot) gateway adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_qqbot_scope_paths.py` | test | End-to-end profile-scope coverage for the QQ (qqbot) authorization, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_queue_command.py` | test | Tests for the gateway /queue command handler (running-agent path). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_queue_consumption.py` | test | Tests for /queue message consumption after normal agent completion. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_queued_native_image_session_key.py` | test | Python module `test_queued_native_image_session_key.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_raft_adapter.py` | test | Tests for the Raft channel adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_readiness.py` | test | Python module `test_readiness.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_reasoning_command.py` | test | Tests for gateway /reasoning command and hot reload behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_reasoning_config_per_model.py` | test | Tests for per-model reasoning_effort override in gateway _load_reasoning_config. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_relay_capability_surface.py` | test | Phase 0 regression harness for the relay/connector work. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_relay_completion_injection_routing.py` | test | Regression: completion injection must resolve the RELAY adapter for | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_relay_delivery_followups.py` | test | Follow-up regressions for the 2026-08-09 relay delivery fixes (#82592). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_relay_final_delivery_incident.py` | test | Regression: relay-plane delivery defects (staging incident 2026-08-09). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_relay_injection_egress_priming.py` | test | Regression: synthetic injections must prime relay egress routing metadata. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_relay_teardown_drain.py` | test | Regression: relay transport teardown must drain in-flight outbound frames. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_relay_upstream_authz.py` | test | Tests for relay upstream-enforced authorization at the gateway layer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_reload_skills_command.py` | test | Tests for the ``/reload-skills`` gateway slash command handler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_reload_skills_discord_resync.py` | test | Tests for `/reload-skills` resyncing the Discord ``/skill`` autocomplete. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_replace_child_reap.py` | test | Tests for --replace child-process reaping (POSIX taskkill /T parity). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_replay_entry_fields.py` | test | Tests for ``gateway.run._build_replay_entry``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_reply_to_injection.py` | test | Tests for reply-to pointer injection in _prepare_inbound_message_text. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_response_filters.py` | test | Python module `test_response_filters.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_restart_after_turn.py` | test | Unit tests for in-band restart after-turn deferral helpers (#77184). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_restart_drain.py` | test | Python module `test_restart_drain.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_restart_notification.py` | test | Tests for /restart notification — the gateway notifies the requester on comeback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_restart_redelivery_dedup.py` | test | Tests for /restart idempotency guard against Telegram update re-delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_restart_resume_pending.py` | test | Tests for the resume_pending session continuity path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_restart_service_detection.py` | test | Tests for /restart service-manager detection (launchd vs interactive). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_resume_command.py` | test | Tests for /resume gateway slash command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_retry_replacement.py` | test | Regression tests for /retry replacement semantics. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_retry_response.py` | test | Regression test: /retry must return the agent response, not None. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_routing_save_fast_path.py` | test | Single-row routing save fast path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_run_cleanup_progress.py` | test | Tests for opt-in cleanup of temporary progress bubbles. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_run_progress_interrupt.py` | test | Tests for interrupt-aware tool-progress suppression in gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_run_progress_topics.py` | test | Tests for topic-aware gateway progress updates. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_run_tool_media_re.py` | test | Tests for _TOOL_MEDIA_RE regex patterns in gateway/run.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_runner_fatal_adapter.py` | test | Python module `test_runner_fatal_adapter.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_runner_startup_failures.py` | test | Python module `test_runner_startup_failures.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_running_agent_session_toggles.py` | test | Regression tests: /yolo and /verbose dispatch mid-agent-run. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_runtime_config_env_expansion.py` | test | Regression tests for gateway runtime config env-var expansion. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_runtime_env_reload_config_authority.py` | test | Regression tests for gateway per-turn env reload preserving config authority. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_runtime_footer.py` | test | Unit tests for gateway.runtime_footer — the opt-in runtime-metadata footer | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_safe_adapter_disconnect.py` | test | Regression tests: failed-connect path must call adapter.disconnect(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_scale_to_zero.py` | test | Unit tests for the scale-to-zero idle-detection pure logic (Phase 0). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_scale_to_zero_watcher.py` | test | Watcher-level tests for scale-to-zero: the idle watcher's dormant sequence and | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_send_error_classification.py` | test | Tests for structured send-error classification (SendResult.error_kind). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_send_image_file.py` | test | Tests for send_image_file() on Telegram, Discord, and Slack platforms, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_send_multiple_images.py` | test | Tests for ``send_multiple_images`` native batching across platforms. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_send_retry.py` | test | Tests for BasePlatformAdapter._send_with_retry and _is_retryable_error. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_send_voice_reply_notify.py` | test | Regression test for issue #27970 Bug 2. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session.py` | test | Tests for gateway session management. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_api.py` | test | Focused tests for API server session-control endpoints. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_boundary_hooks.py` | test | Tests that on_session_finalize and on_session_reset plugin hooks fire in the gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_boundary_security_state.py` | test | Regression tests for approval-state cleanup on session boundaries. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_context_inheritance.py` | test | Cross-session ContextVar *inheritance* leak guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_continuity_82616.py` | test | Regression tests for gateway session continuity (#82616). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_dm_thread_seeding.py` | test | Tests for DM thread session isolation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_env.py` | test | Python module `test_session_env.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_hygiene.py` | test | Tests for gateway session hygiene — auto-compression of large sessions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_id_cache_coherence.py` | test | Regression tests for #54947 — cross-process guard must not invalidate the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_info.py` | test | Tests for GatewayRunner._format_session_info — session config surfacing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_list_allowed_sources.py` | test | Regression tests for the TUI gateway's ``session.list`` handler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_load_bool.py` | test | Regression tests for issue #46994. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_messages_shutdown_preserve.py` | test | Regression tests for #72680 (retargeted). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_model_override_credential_pool.py` | test | Session /model overrides must attach credential_pool for 402 rotation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_model_override_persistence.py` | test | Per-session /model overrides must survive gateway restarts (#3659 salvage). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_model_override_routing.py` | test | Regression tests for session-scoped model/provider overrides in gateway agents. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_model_reset.py` | test | Tests that /new (and its /reset alias) clears session-scoped overrides. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_override_thread_recovery.py` | test | Regression tests for #30479 — session-scoped /model and /reasoning overrides | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_race_guard.py` | test | Tests for the session race guard that prevents concurrent agent runs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_reset_notify.py` | test | Tests for session auto-reset notifications. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_split_brain_11016.py` | test | Regression tests for issue #11016 — Telegram sessions trapped in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_stall_watchdog.py` | test | Tests for gateway session stall watchdog (#72016 item 2). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_state_cleanup.py` | test | Regression tests for _release_running_agent_state and SessionDB shutdown. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_store_expiry_finalized.py` | test | Session expiry finalization closes sessions as session_reset. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_store_lock_io.py` | test | Regression: blocking I/O must not run while session_store._lock is held. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_store_prune.py` | test | Tests for SessionStore.prune_old_entries and the gateway watcher that calls it. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_store_runtime_stale_guard.py` | test | Runtime self-heal for stale sessions.json routing entries (#54878). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_store_stale_prune.py` | test | Tests for SessionStore._prune_stale_sessions_locked — crash self-healing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_session_title_rename_lane.py` | test | Which title stage is allowed to spend a platform rename. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_sethome_synthetic_thread.py` | test | /sethome must not persist Slack's synthetic per-message session thread. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_setup_feishu.py` | test | Tests for _setup_feishu() in ev0_cli/gateway.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_shared_group_sender_prefix.py` | test | Python module `test_shared_group_sender_prefix.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_shutdown_cache_cleanup.py` | test | Regression tests for gateway shutdown cleaning up cached agent memory providers (issue #11205). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_shutdown_flush.py` | test | Tests for gateway/shutdown_flush.py — pending message durability (#72680). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_shutdown_forensics.py` | test | Tests for gateway.shutdown_forensics — fast snapshot + async diag spawn. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_shutdown_memory_provider_messages.py` | test | Regression tests for #15165 — gateway session shutdown must pass the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_shutdown_watchdog.py` | test | Shutdown watchdog + loop heartbeat coverage for #66892. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_signal.py` | test | Tests for Signal messenger platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_signal_format.py` | test | Tests for Signal _markdown_to_signal() formatting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_signal_rate_limit.py` | test | Tests for the SignalAttachmentScheduler token-bucket simulator. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_simplex_plugin.py` | test | Tests for the SimpleX Chat platform-plugin adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_skip_context_files_wiring.py` | test | Per-platform ``skip_context_files`` gateway wiring (#26860). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack.py` | test | Tests for Slack platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_approval_buttons.py` | test | Tests for Slack Block Kit approval buttons and thread context fetching. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_block_kit.py` | test | Unit tests for the Slack Block Kit renderer (pure function, no adapter). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_block_kit_adapter.py` | test | Integration tests: SlackAdapter wiring of Block Kit into send paths. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_bot_auth_bypass.py` | test | Regression guard for Slack bot/workflow-sender authorization bypass. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_channel_session_scope.py` | test | Regression guard for #15421 bug 1 — Slack channel session scoping. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_channel_skills.py` | test | Tests for Slack channel_skill_bindings auto-skill resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_clarify_buttons.py` | test | Tests for Slack Block Kit interactive clarify buttons. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_cron_continuable_surface.py` | test | Tests for the Slack ``cron_continuable_surface`` extra key and its pairing warning. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_dedup_ttl.py` | test | Tests for Slack Socket Mode dedup TTL (#4777). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_download_ssrf.py` | test | SSRF regression tests for inbound Slack file downloads. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_group_dm_scope_warning.py` | test | Tests for the connect-time group-DM scope nudge. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_ignore_other_user_mentions.py` | test | Tests for the Slack ``ignore_other_user_mentions`` option. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_log_noise.py` | test | C13 — Slack log noise & log privacy invariants. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_mention.py` | test | Tests for Slack mention gating (require_mention / free_response_channels). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_mention_humanization.py` | test | Tests for Slack inbound mention humanization + bot identity grounding. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_native_streaming.py` | test | Tests: SlackAdapter native streaming (chat.startStream/appendStream/stopStream). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_peer_agent_smoke.py` | test | Repeatable smoke tests for Slack peer-agent routing invariants. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_plugin_action_handlers.py` | test | Tests for plugin-registered Slack Block Kit action handlers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_plugin_setup.py` | test | Tests for the Slack plugin's interactive_setup wizard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_relay_parent_command.py` | test | Python module `test_slack_relay_parent_command.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_require_mention_channels.py` | test | Tests for the Slack ``require_mention_channels`` per-channel override. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_runner_ignored_channels.py` | test | Python module `test_slack_runner_ignored_channels.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_sdk_response.py` | test | Slack Web API responses must be read as real SDK responses, not dicts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_send_retry.py` | test | Regression: Slack send() must surface retryable + retry_after on 429. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_socket_reconnect_heal.py` | test | Tests for Slack Socket Mode teardown (issue #46990). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_status_update.py` | test | Tests for SlackAdapter.send_or_update_status (issue #30045, Slack). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_user_token_warning.py` | test | Tests for the connect-time user-token (vs bot-token) nudge. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slack_wake_external_bot_messages.py` | test | Regression tests for #63530 — Slack adapter drops human replies in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slash_access.py` | test | Unit tests for gateway.slash_access — per-platform slash command access control. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_slash_access_dispatch.py` | test | Integration tests for slash command access control gating in gateway/run.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_sms.py` | test | Tests for SMS (Twilio) platform integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_sse_agent_cancel.py` | test | Tests for SSE client disconnect → agent task cancellation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_sse_frame.py` | test | Byte-contract tests for the shared ``_sse_frame`` SSE encoder. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_ssl_cert_detection.py` | test | Regression tests for gateway SSL certificate environment repair. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_ssl_certs.py` | test | Tests for SSL certificate auto-detection in gateway/run.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stacked_skill_platform_disabled.py` | test | Regression test for stacked slash-skill invocations bypassing the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stale_confirmation_expiry.py` | test | Tests for stale confirmation text expiry in gateway history. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stale_finalize_suppression.py` | test | Regression coverage for #71643 — stale streamed finalize suppression. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stale_platform_lock_retryable.py` | test | Regression tests for platform-lock acquire behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stale_self_heal_agent_cache_eviction.py` | test | Regression test for the #54878 x #54947 interaction. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_startup_connect_parallel.py` | test | Regression tests for parallel platform connect at gateway startup (#83791). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_startup_no_eager_platform_install.py` | test | Regression tests: ``_apply_env_overrides`` must not lazy-install platform | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_startup_restart_race.py` | test | Python module `test_startup_restart_race.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_status.py` | test | Tests for gateway runtime status tracking. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_status_command.py` | test | Tests for gateway /status behavior and token persistence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_status_phrases.py` | test | Python module `test_status_phrases.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stderr_formatting.py` | test | Regression tests for operator-visible gateway stderr formatting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_steer_command.py` | test | Tests for the gateway /steer command handler. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_steer_fifo_overwrite.py` | test | Regression tests for #75164 — /steer fallback must not overwrite FIFO head. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_step_callback_compat.py` | test | Tests for step_callback backward compatibility. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_sticker_cache.py` | test | Tests for gateway/sticker_cache.py — sticker description cache. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stop_thread_sibling.py` | test | Regression tests: /stop can interrupt a sibling participant's run in a | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stream_consumer.py` | test | Tests for GatewayStreamConsumer — media directive stripping in streaming. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stream_consumer_draft.py` | test | Tests for native draft streaming in GatewayStreamConsumer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stream_consumer_fresh_final.py` | test | Regression tests for the fresh-final-for-long-lived-previews path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stream_consumer_silence.py` | test | Streaming intentional-silence suppression. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stream_consumer_thread_routing.py` | test | Regression tests for stream consumer thread/topic routing fix. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stream_events.py` | test | Structured stream-event protocol + dispatcher behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_streaming_tts_consumer.py` | test | Tests for the gateway streaming-TTS consumer and adapter contract (#60671). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_streaming_tts_gateway_regression.py` | test | Gateway regression: the outer finalisation path must not NameError on | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stt_config.py` | test | Gateway STT config tests — honor stt.enabled: false from config.yaml. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stt_transcript_echo_config.py` | test | Python module `test_stt_transcript_echo_config.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_stuck_loop.py` | test | Tests for stuck-session loop detection (#7536). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_subagent_protection_30170.py` | test | Regression tests for #30170. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_suppression_contract_matrix.py` | test | Contract matrix for the gateway's final-send suppression (#82656). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_systemd_notify.py` | test | Tests for the optional systemd event-loop watchdog protocol. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_systemd_watchdog_lifecycle.py` | test | Gateway lifecycle contract for the opt-in systemd watchdog. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_table_helpers.py` | test | Shared GFM table → bullet conversion helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_teams.py` | test | Tests for the Microsoft Teams platform adapter plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_teams_dotenv_isolation.py` | test | Canaries for Teams SDK import-time dotenv isolation (#62935 / #62947). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_teams_pipeline_runtime_wiring.py` | test | Tests for Teams pipeline runtime wiring into the gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_approval_buttons.py` | test | Tests for Telegram inline keyboard approval buttons. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_audio_vs_voice.py` | test | Tests for #24870 — Telegram: audio file attachments must NOT be routed to STT. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_auth_check.py` | test | Tests for Telegram adapter early authorization check. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_bot_auth_bypass.py` | test | Regression guard for Telegram bot-origin authorization (#32188). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_callback_auth_fail_closed.py` | test | Tests for Telegram adapter fail-closed auth fallback (#24457). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_caption_merge.py` | test | Tests for TelegramPlatform._merge_caption caption deduplication logic. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_channel_posts.py` | test | Regression tests for Telegram channel_post updates. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_clarify_buttons.py` | test | Tests for Telegram inline keyboard clarify buttons. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_closewait_limits_31599.py` | test | Regression test for #31599 — Telegram general-pool CLOSE_WAIT fd leak. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_conflict.py` | test | Python module `test_telegram_conflict.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_connect.py` | test | Tests for Telegram connect() non-retryable fatal error on missing credentials. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_documents.py` | test | Tests for Telegram document handling in gateway/platforms/telegram.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_error_redaction.py` | test | Regression tests for remaining unredacted Telegram transport-error sites. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_fallback_pool_release_71593.py` | test | Regression test for #71593 / #63311 — Telegram fallback-pool FD leak. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_final_delivery.py` | test | Regression coverage for Telegram final delivery after streamed edit failure. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_format.py` | test | Tests for Telegram MarkdownV2 formatting in gateway/platforms/telegram.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_forum_commands.py` | test | Tests for lazy forum command registration in TelegramAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_group_gating.py` | test | Python module `test_telegram_group_gating.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_init_deadline.py` | test | Python module `test_telegram_init_deadline.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_long_command_batching.py` | test | Regression tests for long slash-command pastes split by Telegram clients. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_max_doc_bytes.py` | test | Tests for Telegram document-size cap. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_media_read_timeout.py` | test | Every Telegram media upload passes the long media read timeout. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_mention_boundaries.py` | test | Tests for Telegram bot mention detection (bug #12545). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_model_picker.py` | test | Tests for Telegram model picker thread fallback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_network.py` | test | Tests for plugins.platforms.telegram.telegram_network – fallback transport layer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_network_reconnect.py` | test | Tests for Telegram polling network error recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_noise_filter.py` | test | Gateway noise/secret filtering across chat surfaces (Telegram + siblings). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_overflow_partial.py` | test | Regression coverage for partial Telegram overflow delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_pending_update_probe.py` | test | TelegramAdapter wedged-getUpdates detection via pending_update_count. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_photo_interrupts.py` | test | Python module `test_telegram_photo_interrupts.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_polling_progress.py` | test | Behavior contract for generation-safe Telegram polling progress. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_progress_edit_transient.py` | test | Tests for transient-error handling in Telegram progress-message editing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_prune_stale_topic_binding_31501.py` | test | Regression tests for #31501 — prune stale Telegram DM topic bindings. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_reactions.py` | test | Tests for Telegram message reactions tied to processing lifecycle hooks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_reply_mode.py` | test | Tests for Telegram reply_to_mode functionality. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_reply_quote.py` | test | Tests for Telegram native partial-quote handling in _build_message_event. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_rich_messages.py` | test | Tests for Bot API 10.1 Rich Messages (sendRichMessage) on Telegram. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_rich_newlines.py` | test | Tests for rich-message newline normalization (issue #46070). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_send_draft_format.py` | test | TelegramAdapter.send_draft MarkdownV2 formatting parity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_send_path_health.py` | test | TelegramAdapter send-path health gating after reconnect storms. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_slash_confirm.py` | test | Regression guard: send_slash_confirm must use format_message + MARKDOWN_V2. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_start_polling_timeout.py` | test | Regression tests for #59614: start_polling() must be time-bounded. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_status_indicator.py` | test | Tests for the Telegram bot status indicator. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_status_update.py` | test | Tests for TelegramAdapter.send_or_update_status (issue #30045). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_text_batch_perf.py` | test | Regression tests for the Telegram text-batch adaptive-delay fast-path | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_text_batching.py` | test | Tests for Telegram text message aggregation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_thread_fallback.py` | test | Tests for Telegram topic/thread routing fallbacks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_topic_mode.py` | test | Tests for Telegram private-chat topic-mode routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_typing_backoff.py` | test | Telegram typing indicator transient backoff tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_username_chat_id.py` | test | Tests for Telegram username (non-numeric) chat_id handling (#13206). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_voice_caption_markdown.py` | test | Telegram voice-message captions must render markdown (#32029). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_voice_duration.py` | test | Telegram voice/audio messages must carry an explicit duration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_voice_v0_regressions.py` | test | Python module `test_telegram_voice_v0_regressions.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_telegram_webhook_secret.py` | test | Tests for GHSA-3vpc-7q5r-276h — Telegram webhook secret required. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_text_batching.py` | test | Tests for text message batching across all gateway adapters. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_title_command.py` | test | Tests for /title gateway slash command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_tool_log_mode.py` | test | Tests for the `log` tool_progress mode (salvage of #3459 / #3458). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_tool_response_drop_recovery.py` | test | Regression tests for tool-using response silent drop (issue #29346). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_transcript_offset.py` | test | Tests for transcript history offset fix. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_tts_media_routing.py` | test | Tests for cross-platform audio/voice media routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_tui_approval_redaction.py` | test | Regression test for TUI approval-prompt credential redaction (#48456). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_tui_slash_worker_path.py` | test | Regression test for slash_worker PATH construction (#83845). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_turn_context.py` | test | Unit tests for the TurnContext/TurnRunner seam extracted from | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_turn_lease.py` | test | Behavior tests for the per-session turn lease (#64934). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_typing_indicator_toggle.py` | test | Per-platform typing-indicator toggle (PlatformConfig.typing_indicator). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_unauthorized_dm_behavior.py` | test | Python module `test_unauthorized_dm_behavior.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_unavailable_skill_hint.py` | test | Tests for gateway.run._check_unavailable_skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_undo_rewind_session.py` | test | Tests for SessionStore.rewind_session — the gateway /undo [N] primitive. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_unknown_command.py` | test | Tests for gateway warning when an unrecognized /command is dispatched. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_update_command.py` | test | Tests for /update gateway slash command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_update_cron_drain.py` | test | Regression tests for #60432. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_update_streaming.py` | test | Tests for /update live streaming, prompt forwarding, and gateway IPC. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_usage_command.py` | test | Tests for gateway /usage command — agent cache lookup and output fields. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_verbose_command.py` | test | Tests for gateway /verbose command (config-gated tool progress cycling). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_version_command.py` | test | Tests for gateway /version command. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_video_context_note.py` | test | Tests for video attachment context notes in gateway turns. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_vision_memory_leak.py` | test | Tests for _enrich_message_with_vision — regression for #5719. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_vision_preprocess.py` | test | Gateway vision pre-process prompt should stay concise. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_voice_command.py` | test | Tests for the /voice command and auto voice reply in the gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_voice_mode_platform_isolation.py` | test | Tests for voice mode platform isolation (bug #12542). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_wake_delivery.py` | test | Tests for gateway/wake.py — background wake delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_watchdog_review_76354.py` | test | Regressions for #76354 review S1/S2/S4 — activity write budget, watchdog | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_weak_credential_guard.py` | test | Tests for gateway weak credential rejection at startup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_webhook_adapter.py` | test | Unit tests for the generic webhook platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_webhook_deliver_only.py` | test | Tests for the webhook adapter's ``deliver_only`` route mode. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_webhook_dynamic_routes.py` | test | Tests for webhook adapter dynamic route loading. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_webhook_integration.py` | test | Integration tests for the generic webhook platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_webhook_route_toolsets.py` | test | Per-route webhook toolset overrides (adapter.toolsets_for_source). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_webhook_session_close.py` | test | Invariant test: a completed webhook delivery closes its session. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_webhook_signature_rate_limit.py` | test | Test that HMAC signature validation happens BEFORE rate limiting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_wecom.py` | test | Tests for the WeCom platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_wecom_callback.py` | test | Tests for the WeCom callback-mode adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_wecom_plugin_setup.py` | test | Tests for the WeCom plugin's interactive_setup wizard home-channel flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_weixin.py` | test | Tests for the Weixin platform adapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_weixin_secret_scope.py` | test | Weixin adapter secret-scope regression tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_weixin_typing.py` | test | Tests for WeChat iLink typing ticket refresh logic (issue #38085). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_allowlist_lid_resolution.py` | test | WhatsApp DM/group allowlist must resolve phone↔LID aliases at intake. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_bridge_dir_resolution.py` | test | Tests for resolve_whatsapp_bridge_dir() — read-only install tree handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_bridge_pidfile.py` | test | Regression tests: the WhatsApp stale-bridge cleanup must never kill a stranger. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_cloud.py` | test | Tests for the WhatsApp Cloud API adapter (Phase 2). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_cloud_allowed_users.py` | test | Regression tests for PR #58448 salvage: the documented | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_connect.py` | test | Tests for WhatsApp connect() error handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_formatting.py` | test | Tests for WhatsApp message formatting and chunking. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_from_owner.py` | test | Tests for WhatsApp owner-message metadata and source-level text tagging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_group_gating.py` | test | Python module `test_whatsapp_group_gating.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_identity.py` | test | Tests for gateway.whatsapp_identity alias resolution path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_media_path_profile.py` | test | Regression: the WhatsApp inbound-media path validator follows the active | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_native_delivery.py` | test | Python module `test_whatsapp_native_delivery.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_plugin_setup.py` | test | Tests for the WhatsApp plugin's interactive_setup wizard home-channel flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_reply_prefix.py` | test | Tests for WhatsApp reply_prefix config.yaml support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_stale_bridge.py` | test | Tests for the WhatsApp stale-bridge staleness handshake. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_text_batching.py` | test | Text-debounce batching for the WhatsApp adapter (issue #35301). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_whatsapp_to_jid.py` | test | Unit tests for gateway.whatsapp_identity.to_whatsapp_jid. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_ws_auth_retry.py` | test | Tests for auth-aware retry in Mattermost WS and Matrix sync loops. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_ws_auth_retry_verifier_probe.py` | test | Adversarial verifier probes for the mattermost-ws-401-classify fix | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_yolo_command.py` | test | Tests for gateway /yolo session scoping. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_yuanbao_forwarded_heartbeat.py` | test | ForwardedRecordsParseMiddleware must actually send its loading heartbeat. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/gateway/test_yuanbao_media_ssrf.py` | test | SSRF protection tests for yuanbao_media.download_url(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/conftest.py` | test | Package-level isolation for Honcho unit tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_async_memory.py` | test | Tests for the async-memory Honcho improvements. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_auth_recovery.py` | test | Tests for OAuth 401 recovery: prompt exchange retry, invalid_grant handling, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_cli.py` | test | Tests for plugins/memory/honcho/cli.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_client.py` | test | Tests for plugins/memory/honcho/client.py — Honcho client configuration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_client_identity_isolation.py` | test | Multi-profile client isolation tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_empty_profile_hint.py` | test | Tests for honcho_profile's empty-card hint (#5137 follow-up). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_network_isolation.py` | test | B8 regressions: honcho unit tests must never touch the network. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_oauth.py` | test | Tests for plugins/memory/honcho/oauth.py — OAuth grant storage + refresh. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_oauth_flow.py` | test | End-to-end test for the zero-CLI Honcho OAuth flow against a fake AS. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_pin_peer_name.py` | test | Tests for the ``pinPeerName`` / ``pinUserPeer`` config flag. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_query_rewrite.py` | test | Behavior contract for Honcho's latest-message query rewrite. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_save_messages.py` | test | Tests for the saveMessages knob: when false, the provider never writes to Honcho. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/honcho_plugin/test_session.py` | test | Tests for plugins/memory/honcho/session.py — HonchoSession and helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/install/install-update-e2e.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `tests/integration/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/integration/test_batch_runner.py` | test | Test script for batch runner | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/integration/test_checkpoint_resumption.py` | test | Test script to verify checkpoint behavior in batch_runner.py | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/integration/test_daytona_terminal.py` | test | Integration tests for the Daytona terminal backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/integration/test_ha_integration.py` | test | Integration tests for Home Assistant (tool + gateway). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/integration/test_modal_terminal.py` | test | Test Modal Terminal Tool | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/integration/test_vision_docker_resolve.py` | test | Docker integration tests for the vision image-source resolver. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/integration/test_voice_channel_flow.py` | test | Integration tests for Discord voice channel audio flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/integration/test_web_tools.py` | test | Comprehensive Test Suite for Web Tools Module | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/manual/cron_inchannel_dm_e2e.py` | test | DM-path verification for in_channel continuable cron (Option A scoping). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/manual/cron_inchannel_e2e.py` | test | Offline E2E for continuable in-channel cron (specs/cron-inchannel-continuable). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/monitoring/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/monitoring/test_cron_health_export.py` | test | Python module `test_cron_health_export.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/monitoring/test_emitter.py` | test | Tests for the monitoring emitter: hot-path invariant + subscriber fan-out. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/monitoring/test_export_redaction.py` | test | Export redaction tests — the security-critical layer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/monitoring/test_gateway_health_export.py` | test | Python module `test_gateway_health_export.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/monitoring/test_otlp_exporter.py` | test | OTLP exporter tests: config resolution, span mapping, streaming subscriber. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/openviking_plugin/test_openviking.py` | test | Tests for plugins/memory/openviking/__init__.py — URI normalization and payload handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/browser/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/browser/check_parity_vs_main.py` | test | Behavior-parity check for the browser-provider plugin migration (#25214). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/browser/test_browser_provider_plugins.py` | test | Plugin-side tests for the browser provider migration (PR #25214). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/dashboard_auth/test_basic_provider.py` | test | Tests for the BasicAuthProvider plugin (username/password, scrypt, signed | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/dashboard_auth/test_drain_provider.py` | test | Tests for the DrainSecretProvider plugin (non-interactive bearer secret). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/dashboard_auth/test_nous_provider.py` | test | Tests for the bundled Nous dashboard-auth plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/dashboard_auth/test_self_hosted_provider.py` | test | Tests for the bundled self-hosted OIDC dashboard-auth plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/check_parity_vs_main.py` | test | Behavior-parity check for the image-gen FAL plugin migration (#26241). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/test_deepinfra_provider.py` | test | Tests for the bundled DeepInfra image_gen plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/test_fal_provider.py` | test | Tests for the FAL.ai image generation plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/test_krea_provider.py` | test | Tests for Krea image generation provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/test_openai_codex_provider.py` | test | Tests for the bundled ``openai-codex`` image_gen plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/test_openai_provider.py` | test | Tests for the bundled OpenAI image_gen plugin (gpt-image-2, three tiers). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/test_openrouter_compat_provider.py` | test | Tests for the OpenRouter-compatible image gen provider (OpenRouter + Nous). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/image_gen/test_xai_provider.py` | test | Tests for xAI image generation provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_byterover_provider.py` | test | Tests for the ByteRover memory provider config gates. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_config_schema.py` | test | Tests for config-schema loading from memory provider plugin dirs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_discovery_sources.py` | test | Discovery parity for out-of-tree memory providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_hindsight_config_schema.py` | test | Tests for Hindsight's declared config surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_hindsight_env_perms.py` | test | Regression tests: the embedded Hindsight profile env file carries the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_hindsight_local_runtime_hint.py` | test | NousResearch/hermes-agent#7718 — actionable message when local_embedded | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_hindsight_provider.py` | test | Tests for the Hindsight memory provider plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_hindsight_templates.py` | test | Tests for the Hindsight setup-wizard starter-template step. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_holographic_auto_extract.py` | test | Regression tests for #57682 — holographic auto_extract harvested | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_holographic_retrieval.py` | test | Tests for FactRetriever FTS5 query sanitization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_holographic_shutdown_closes_db.py` | test | Regression test for #44037 — holographic provider leaked its SQLite | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_holographic_store.py` | test | Tests for the holographic MemoryStore shared-connection registry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_honcho_cli_peers.py` | test | Regression tests for #76414: `hermes honcho peers` showed "(not set)" | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_honcho_config_schema.py` | test | Tests for Honcho's declared config surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_mem0_backend.py` | test | Tests for Mem0Backend abstraction — PlatformBackend, OSSBackend, SelfHostedBackend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_mem0_providers.py` | test | Tests for OSS provider definitions and validation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_mem0_setup.py` | test | Tests for Mem0 setup wizard — flag parsing, config building, validation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_mem0_v3.py` | test | Tests for Mem0 v3 API — new tool names, paginated responses, update/delete tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_memory_lazy_install.py` | test | Regression tests: supermemory + mem0 memory providers must lazy-install | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_openviking_endpoint_always_blocked.py` | test | OpenViking endpoint always-blocked floor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_openviking_provider.py` | test | Python module `test_openviking_provider.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_openviking_shutdown.py` | test | Tests for OpenViking memory-provider shutdown teardown. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_retaindb_provider.py` | test | Python module `test_retaindb_provider.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/memory/test_supermemory_provider.py` | test | Python module `test_supermemory_provider.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_copilot_profile.py` | test | Unit tests for the Copilot provider profile's reasoning-effort wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_custom_profile.py` | test | Unit tests for the custom provider profile's reasoning wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_deepseek_profile.py` | test | Unit tests for the DeepSeek provider profile's thinking-mode wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_fireworks_profile.py` | test | Unit tests for the Fireworks AI provider profile. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_gemini_profile.py` | test | Contract tests for the native Google Gemini provider profile. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_kimi_profile.py` | test | Unit tests for the Kimi/Moonshot provider profile's reasoning wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_minimax_profile.py` | test | Unit tests for the MiniMax provider profile. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_ollama_cloud_profile.py` | test | Unit tests for the Ollama Cloud provider profile's reasoning-effort wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_opencode_go_profile.py` | test | Unit tests for OpenCode Go reasoning-control wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_upstage_profile.py` | test | Unit tests for the Upstage Solar provider profile. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/model_providers/test_zai_profile.py` | test | Unit tests for the Z.AI / GLM provider profile's reasoning wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_auth.py` | test | Tests for the Photon auth module (device login + dashboard API). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_check_requirements_risks.py` | test | Tests for check_requirements() diagnostic logging (fix) and remaining risks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_fatal_notify_self_cancel.py` | test | Photon's fatal-error notification must not be cancelled by its own teardown. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_inbound.py` | test | Inbound dispatch + dedup tests for PhotonAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_markdown.py` | test | Markdown handling tests for PhotonAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_mention_gating.py` | test | Group-chat mention-gating tests for PhotonAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_npm_error_log_regression.py` | test | Regression tests for the npm stderr capture + error log persistence fix. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_outbound_media.py` | test | Outbound-media tests for PhotonAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_overflow_recovery.py` | test | Photon adapter resilience to transient Spectrum/Envoy upstream overflow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_poll_clarify.py` | test | Native-poll clarify tests for PhotonAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_presence_watchdog.py` | test | Presence-watchdog tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_reactions.py` | test | Reaction (tapback) tests for PhotonAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_rich_links.py` | test | Rich-link handling tests for PhotonAdapter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_runtime_record.py` | test | Sidecar runtime-record persistence tests (issue #69960). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_setup_access.py` | test | Tests for `hermes photon setup`'s access auto-configuration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_sidecar_deps_stale.py` | test | Regression tests for the Photon sidecar stale-dependency self-heal. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_sidecar_lifecycle.py` | test | Sidecar lifecycle tests: orphan reaping and parent-death wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_sidecar_paths.py` | test | Tests for the Photon sidecar directory resolver (NS-606). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_spectrum_patch.py` | test | Regression tests for Hermes' Spectrum mixed text+attachment workaround. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_streaming.py` | test | Regression tests for Photon adapter streaming behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_url_send_path.py` | test | Behavior tests for Photon raw-URL outbound routing (issue: markdown 500s). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/photon/test_zombie_stream_watchdog.py` | test | Zombie-stream watchdog tests (half-open gRPC stream, issue #54036). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/platforms/test_discord_gate_isolation.py` | test | Per-profile isolation of Discord/Telegram allow/deny gates (issue #72348). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_a2a_phase23.py` | test | Streaming / push / anti-loop / task-store tests for the A2A plugin (v1.0). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_a2a_plugin.py` | test | Tests for the A2A (Agent-to-Agent) platform plugin — protocol v1.0. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_achievements_plugin.py` | test | Tests for the bundled hermes-achievements dashboard plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_chronos_cron.py` | test | Unit tests for the Chronos NAS-mediated cron provider (Phase 4D). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_chronos_verify.py` | test | Tests for the Chronos inbound cron-fire JWT verifier (Phase 4E.1). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_discord_runtime_failure.py` | test | Python module `test_discord_runtime_failure.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_disk_cleanup_plugin.py` | test | Tests for the disk-cleanup plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_google_meet_audio.py` | test | Tests for plugins.google_meet.audio_bridge (v2). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_google_meet_node.py` | test | Tests for the google_meet node primitive. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_google_meet_plugin.py` | test | Tests for the google_meet plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_google_meet_realtime.py` | test | Tests for plugins.google_meet.realtime.openai_client (v2). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_hindsight_health_grace_timeout.py` | test | Embedded-daemon health grace timeout export (issue #13125 comment thread). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_hindsight_root_guard.py` | test | Root-user guard for Hindsight local_embedded mode (issue #13125). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_holographic_vector_storage.py` | test | Storage-size regression tests for holographic HRR vectors. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_kanban_attachments.py` | test | Tests for Kanban task file attachments (#35338). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_kanban_board_project_api.py` | test | Kanban dashboard plugin: project listing + project-scoped boards. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_kanban_dashboard_plugin.py` | test | Tests for the Kanban dashboard plugin backend (plugins/kanban/dashboard/plugin_api.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_kanban_dashboard_task_updated_hook.py` | test | Dashboard mutation-boundary coverage for ``on_kanban_task_updated``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_kanban_estimate.py` | test | Kanban dashboard plugin: task effort estimate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_kanban_model_override.py` | test | Per-task model/provider override — DB layer, worker spawn, dashboard API. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_kanban_worker_runs.py` | test | Tests for kanban worker/runs read endpoints. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_kanban_ws_idle_disconnect.py` | test | Regression: kanban events WS must notice client disconnect on an idle board. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_langfuse_plugin.py` | test | Tests for the bundled observability/langfuse plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_nemo_relay_bounded_marks.py` | test | Plugin Relay marks must be bounded — never an unbounded native call. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_nemo_relay_mark_turn_parenting.py` | test | Marks must parent to the live turn scope, not the session scope. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_nemo_relay_plugin.py` | test | Tests for the bundled observability/nemo_relay plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_plugin_dashboard_auth_contract.py` | test | Guardrail: dashboard plugins must NOT read the session token directly. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_raft_check_fn_silent.py` | test | Regression tests for the raft platform plugin's check_fn. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_retaindb_plugin.py` | test | Tests for the RetainDB memory plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_security_guidance_plugin.py` | test | Tests for the security-guidance plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/test_teams_pipeline_plugin.py` | test | Tests for the Teams pipeline plugin package. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/transcription/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/transcription/check_parity_vs_main.py` | test | Behavior-parity check for the STT plugin hook + command-provider registry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/tts/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/tts/check_parity_vs_main.py` | test | Behavior-parity check for the TTS plugin hook (issue #30398). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/video_gen/__init__.py` | test | Make tests/plugins/video_gen a package. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/video_gen/test_deepinfra_provider.py` | test | Tests for the bundled DeepInfra video_gen plugin. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/video_gen/test_fal_plugin.py` | test | Tests for the FAL video gen plugin — family routing, payload shape. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/video_gen/test_xai_plugin.py` | test | Smoke tests for the xAI video gen plugin — load & register surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/video_gen/test_xai_plugin_integration.py` | test | Integration tests for the xAI video gen plugin's simplified surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/web/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/plugins/web/test_web_search_provider_plugins.py` | test | Plugin-side tests for the web search provider migration (PR #25182). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/test_e2e_wiring.py` | test | E2E tests: verify _build_kwargs_from_profile produces correct output. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/test_entry_point_discovery.py` | test | Tests for pip entry-point provider discovery (hermes_agent.plugins group). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/test_fetch_models_base_url.py` | test | Tests for ProviderProfile.fetch_models base_url override (issue #47009). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/test_plugin_discovery.py` | test | Tests for the model-providers plugin discovery system. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/test_profile_wiring.py` | test | Profile-path parity tests: verify profile path produces identical output to legacy flags. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/test_provider_profiles.py` | test | Tests for the provider module registry and profiles. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/test_provider_registry.py` | test | Python module `test_provider_registry.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/providers/test_transport_parity.py` | test | Parity tests: pin the exact current transport behavior per provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/conftest.py` | test | Fast-path fixtures shared across tests/run_agent/. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/repro_48013_image_shrink_brick.py` | test | Runnable proof for issue #48013 — image-dimension 400 session brick. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_1630_context_overflow_loop.py` | test | Tests for #1630 — gateway infinite 400 failure loop prevention. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_18028_content_policy_blocked.py` | test | Regression guard for #18028: provider content-policy / safety-filter | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_24996_fallback_exhaustion_cooldown.py` | test | Regression tests for #24996 — fallback-switch storm on host memory. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_28161_anthropic_stream_pool_cleanup.py` | test | Anthropic stream cleanup must not call _replace_primary_openai_client() and | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_31273_402_not_retried.py` | test | Regression guard for #31273: HTTP 402 (billing exhaustion) must abort | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_32646_fallback_429_after_timeout.py` | test | Regression test for #32646: fallback_providers not activated when | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_413_compression.py` | test | Tests for payload/context-length → compression retry logic in AIAgent. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_63425_credential_pool_auto_detect.py` | test | Reproduction test for issue #63425: Provider auto-detection discards credential pools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_66267_multimodal_interim.py` | test | Tests for issue #66267 — multimodal (list) tool-result content must not | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_70773_shared_client_fd_corruption.py` | test | #70773: the shared OpenAI-wire client must never be pool-closed from a | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_81641_text_turn_incremental_persistence.py` | test | Behavior contract: a completed pure-text assistant turn is durable before | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_860_dedup.py` | test | Tests for issue #860 — SQLite session transcript deduplication. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_agent_guardrails.py` | test | Unit tests for AIAgent pre/post-LLM-call guardrails. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_anthropic_mid_tool_call_drop.py` | test | The Anthropic streaming path must not accept a tool_use block whose stream | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_anthropic_prompt_cache_policy.py` | test | Tests for AIAgent._anthropic_prompt_cache_policy(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_anthropic_response_header_capture.py` | test | Anthropic Messages path must capture rate-limit + credits headers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_anthropic_third_party_oauth_guard.py` | test | Tests for ``_is_anthropic_oauth`` guard against third-party Anthropic-compatible providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_anthropic_truncation_continuation.py` | test | Regression test for anthropic_messages truncation continuation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_api_max_retries_config.py` | test | Tests for agent.api_max_retries config surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_async_httpx_del_neuter.py` | test | Tests for the AsyncHttpxClientWrapper.__del__ neuter fix. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_auth_provider_failover.py` | test | Auth-failure provider failover (conversation loop). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_authorization_gate.py` | test | Tests for the concurrent authorization gate and human-wait accounting (#79719). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_background_review.py` | test | Regression tests for background review agent cleanup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_background_review_cache_parity.py` | test | Tests that the background review fork inherits the parent's cached system prompt. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_background_review_cost_controls.py` | test | Unit coverage for the background-review aux-model selector + routed digest. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_background_review_summary.py` | test | Tests for AIAgent._summarize_background_review_actions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_background_review_toolset_restriction.py` | test | Tests that the background review agent restricts tools at runtime, not at schema time. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_callable_api_key.py` | test | Tests that callable api_key (Entra ID bearer provider) flows through | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_codex_app_server_compaction.py` | test | Python module `test_codex_app_server_compaction.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_codex_app_server_integration.py` | test | Integration test for the codex_app_server runtime path through AIAgent. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_codex_app_server_lifecycle.py` | test | Codex app-server session lifecycle on hard agent teardown (#65260). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_codex_multimodal_tool_result.py` | test | Tests for codex_responses_adapter multimodal tool-result handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_codex_no_tools_nonetype.py` | test | Regression coverage for #32892. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_codex_silent_hang_hint.py` | test | Tests for the ``_codex_silent_hang_hint`` heuristic. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_codex_xai_oauth_recovery.py` | test | Regression tests for the May 2026 xAI OAuth (SuperGrok / X Premium) bugs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_commit_memory_session_context_engine.py` | test | Regression tests for AIAgent.commit_memory_session. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compress_focus_plugin_fallback.py` | test | Regression test: _compress_context tolerates plugin engines with strict signatures. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_abort_state_reset.py` | test | Regression tests for #58630: every compression abort path must reset | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_boundary.py` | test | Tests for context compression boundary alignment. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_boundary_hook.py` | test | Test: the context engine is notified of a compression-boundary rollover. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_budget_rearm.py` | test | Regression test for re-arming the compression budget after tool progress. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_budget_refund.py` | test | Behavioral tests for provider-confirmed compression-budget rearming. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_closed_adoption.py` | test | Compression race at the flush chokepoint: a turn writing against a session | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_feasibility.py` | test | Tests for _check_compression_model_feasibility() — warns when the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_lock_defer.py` | test | Lock-contended compression no-ops must soft-DEFER, never exhaust (#49874). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_persistence.py` | test | Tests for context compression persistence in the gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compression_trigger_excludes_reasoning.py` | test | Verify compression trigger excludes reasoning/completion tokens (#12026). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_compressor_fallback_update.py` | test | Tests that _try_activate_fallback updates the context compressor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_concurrent_interrupt.py` | test | Tests for interrupt handling in concurrent tool execution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_context_token_tracking.py` | test | Tests for context token tracking in run_agent.py's usage extraction. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_continuation_ceiling_wedge.py` | test | Regression tests for the post-ceiling session wedge. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_continuation_repetition_guard.py` | test | Regression tests for the truncated-response repetition guard (#86581). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_conversation_fallback_state.py` | test | Regression tests for conversation loop fallback state management. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_copilot_native_vision_headers.py` | test | Python module `test_copilot_native_vision_headers.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_create_openai_client_disables_sdk_retries.py` | test | Regression guard: _create_openai_client must disable SDK-level retries. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_create_openai_client_kwargs_isolation.py` | test | Guardrail: _create_openai_client must not mutate its input kwargs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_create_openai_client_proxy_env.py` | test | Regression guard: _create_openai_client must honor HTTP(S)_PROXY env vars. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_create_openai_client_reuse.py` | test | Regression guardrail: sequential _create_openai_client calls must not | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_create_openai_client_ssl_verify.py` | test | Regression: keepalive httpx client must honor custom CA bundles for HTTPS providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_credential_pool_interrupt.py` | test | Regression test for #26145: credential pool rotation after interrupt-resume. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_credential_rotation_route_settings.py` | test | Credential rotation must not carry route-scoped TLS policy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_credits_notices_toggle.py` | test | Tests for the display.credits_notices config gate on _emit_credits_notices. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_cross_process_turn_lease.py` | test | AIAgent enters turns only after acquiring and reloading durable state. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_custom_provider_extra_headers_client.py` | test | Per-provider ``extra_headers`` applied to the OpenAI client (#3526 salvage). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_deepseek_reasoning_content_echo.py` | test | Regression test: DeepSeek V4 thinking mode reasoning_content echo. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_deepseek_v4_thinking_live.py` | test | Live DeepSeek V4 thinking-mode tool-call replay smoke test. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_dict_tool_call_args.py` | test | Python module `test_dict_tool_call_args.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_dropped_tool_call_recovery.py` | test | Regression tests for dropped tool-call recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_empty_response_recovery_persistence.py` | test | Regression tests for empty-response recovery transcript persistence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_empty_terminal_reasoning_surface.py` | test | Tests for the empty-terminal reasoning surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_env_credential_turn_refresh.py` | test | Per-turn adoption of ~/.hermes/.env credential edits (#67821). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_exit_cleanup_interrupt.py` | test | Tests for KeyboardInterrupt handling in exit cleanup paths. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_fallback_api_mode_preservation.py` | test | Fallback activation must preserve the Anthropic wire signal (PR #79787). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_fallback_credential_isolation.py` | test | Tests for fallback credential pool isolation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_fallback_reasoning_override.py` | test | Tests for per-model reasoning_effort override during fallback activation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_file_mutation_verifier.py` | test | Tests for the per-turn file-mutation verifier footer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_fireworks_live.py` | test | Live Fireworks smoke test — exercises the Hermes runtime, not a raw SDK client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_identity_flush.py` | test | Regression tests for identity-based SessionDB flushing (#46053). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_image_generate_parallel.py` | test | Regression tests for parallel image-generation tool batches. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_image_rejection_fallback.py` | test | Tests for the image-rejection fallback in run_agent. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_image_shrink_recovery.py` | test | Tests for reactive image-shrink recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_in_place_compaction.py` | test | Tests for in-place context compaction (config: compression.in_place, #38763). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_infinite_compaction_loop.py` | test | Tests for the infinite compaction loop fix (issue #40803). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_init_fallback_on_exhausted_pool.py` | test | Regression test for #17929: AIAgent.__init__ should try fallback_model | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_interactive_interrupt.py` | test | Interactive interrupt test that mimics the exact CLI flow. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_interrupt_propagation.py` | test | Test interrupt propagation from parent to child agents. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_invalid_context_length_warning.py` | test | Tests that invalid context_length values in config produce visible warnings. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_iteration_budget_race.py` | test | Tests for IterationBudget thread safety. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_jsondecodeerror_retryable.py` | test | Regression guard for #14782: json.JSONDecodeError must not be classified | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_last_reasoning_per_turn.py` | test | Tests for per-turn reasoning extraction in AIAgent.run_conversation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_lmstudio_load_mode.py` | test | Python module `test_lmstudio_load_mode.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_long_context_tier_429.py` | test | Tests for Anthropic Sonnet long-context tier 429 handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_malformed_tool_arguments.py` | test | Malformed model tool arguments are rejected at the dispatch boundary. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_materialize_data_url_cleanup.py` | test | Regression test: temp file cleanup when materializing data URLs for vision. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_memory_nudge_counter_hydration.py` | test | Regression test for issue #22357 — gateway memory-nudge counter hydration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_memory_provider_init.py` | test | Regression tests for memory provider selection during AIAgent init. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_memory_sync_interrupted.py` | test | Regression guard for #15218 — external memory sync must skip interrupted turns. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_message_sequence_repair.py` | test | Tests for pre-API-call message-sequence repair. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_moa_fanout_cadence.py` | test | every_n fanout cadence: advisors refresh every Nth tool iteration and | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_moa_loop_mode.py` | test | Python module `test_moa_loop_mode.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_moa_privacy_filter.py` | test | MoA privacy redaction filter (config: moa.privacy_filter — display \| full). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_moa_streaming.py` | test | Tests for MoA aggregator streaming. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_multimodal_tool_content_recovery.py` | test | Tests for reactive multimodal-tool-content recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_native_compaction.py` | test | Tests for native OpenAI Responses server-side compaction (gpt-5.6 only). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_nonretryable_error_html_summary.py` | test | Regression: non-retryable API failures must not leak raw HTML pages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_notice_spine.py` | test | Regression tests for the notice-spine (AgentNotice + emitter callbacks). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_nous_429_fallback_reentry.py` | test | Regression guard: a genuine Nous 429 must re-enter the retry loop so the | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_nous_fallback_unavailable.py` | test | Tests for Nous fallback local-availability suppression. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_openai_client_lifecycle.py` | test | Python module `test_openai_client_lifecycle.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_overflow_overhead_aware_tokens.py` | test | Regression tests: overflow recovery handlers must pass overhead-aware token estimates. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_partial_stream_finish_reason.py` | test | Regression tests for issue #30963 — partial-stream stub finish_reason. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_per_model_compression_threshold.py` | test | Tests for per-model compression threshold overrides. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_per_model_threshold_init_ordering.py` | test | Follow-up regression tests for per-model compression threshold overrides. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_percentage_clamp.py` | test | Tests for percentage clamping at 100% across display paths. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_plugin_context_engine_init.py` | test | Tests that plugin context engines get update_model() called during init. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_plugin_stream_hooks.py` | test | Python module `test_plugin_stream_hooks.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_post_tool_compression_attempt_cap.py` | test | Behavioral regression tests for the post-tool compression attempt cap. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_pre_compress_memory_context.py` | test | Behavior contracts for the pre-compression memory-context handoff. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_preflight_compression_cap_e2e.py` | test | E2E: compression.max_attempts=6 drives a 4th+ preflight compaction pass. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_primary_runtime_restore.py` | test | Tests for per-turn primary runtime restoration and transport recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_proactive_prune_loop_wiring.py` | test | Behavioral tests for the post-tool proactive tool-result prune wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_provider_attribution_headers.py` | test | Attribution default_headers applied per provider via base-URL detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_provider_fallback.py` | test | Tests for ordered provider fallback chain (salvage of PR #1761). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_provider_parity.py` | test | Provider parity tests: verify that AIAgent builds correct API kwargs | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_repair_tool_call_arguments.py` | test | Tests for _repair_tool_call_arguments — malformed JSON repair pipeline. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_repair_tool_call_name.py` | test | Tests for AIAgent._repair_tool_call — tool-name normalization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_request_client_reuse_abort_races.py` | test | Races between the request-client reuse cache and the abort machinery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_reset_aware_primary_restore.py` | test | Reset-aware primary restore — stay on fallback until the primary's | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_retry_status_buffer.py` | test | Tests for the retry/fallback status buffer helpers on AIAgent. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_review_prompt_class_first.py` | test | Behavior tests for the skill review / combined review prompts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_run_agent.py` | test | Unit tests for run_agent.py (AIAgent). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_run_agent_codex_responses.py` | test | Python module `test_run_agent_codex_responses.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_run_agent_multimodal_prologue.py` | test | Regression tests for run_conversation's prologue handling of multimodal content. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_sequential_chats_live.py` | test | Live regression guardrail for the keepalive/transport bug class (#10933). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_sequential_tool_timeout.py` | test | Sequential tool calls recover when one dispatch never returns. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_session_activity_persist.py` | test | Durable session activity projection from AIAgent._touch_activity (#72016). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_session_id_env.py` | test | Test that HERMES_SESSION_ID is exposed as an env var and ContextVar. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_session_meta_filtering.py` | test | Tests for session_meta filtering — issue #4715. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_session_reset_fix.py` | test | Tests for session reset completeness (fixes #2635). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_session_source.py` | test | Python module `test_session_source.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_start_order_gate.py` | test | Tests for the concurrent start-order gate (PR #79571 / issue #79569). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_steer.py` | test | Tests for AIAgent.steer() — mid-run user message injection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_stream_drop_logging.py` | test | Tests for richer stream-drop diagnostics in agent.log. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_stream_interrupt_retry.py` | test | Tests that /stop interrupts streaming retry loops immediately. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_stream_single_writer_65991.py` | test | Regression tests for the streaming single-writer invariant (#65991). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_stream_stale_breaker_reset.py` | test | Follow-up for the cross-turn stream-stale circuit breaker (#58962). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_stream_stale_circuit_breaker.py` | test | Cross-turn stream-stale circuit breaker (issue #58962). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_streaming.py` | test | Tests for streaming token delivery infrastructure. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_streaming_tool_call_repair.py` | test | Tests for tool call argument repair in the streaming assembly path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_strict_api_validation.py` | test | Test validation error prevention for strict APIs (Fireworks, etc.) | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_strip_reasoning_tags_cli.py` | test | Tests for cli.py::_strip_reasoning_tags — specifically the tool-call | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_summarize_api_error.py` | test | Regression: empty-body HTTP 4xx errors must still surface a real provider message. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_switch_model_context.py` | test | Tests that switch_model does not inherit stale context_length overrides. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_switch_model_fallback_prune.py` | test | Regression test for TUI v2 blitz bug: explicit /model --provider switch | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_switch_model_pool_reload_52727.py` | test | Regression tests for #52727: switch_model() must reload the credential pool | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_switch_model_reapplies_headers.py` | test | Regression tests for #61099: switch_model must reapply provider-specific | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_switch_model_reasoning_override.py` | test | Tests for per-model reasoning_effort override during /model switch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_switch_model_rollback.py` | test | Regression test for #33175: switch_model() must roll back to the pre-swap | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_switch_model_stale_base_url.py` | test | Regression tests for #47828: switch_model must not pair a new provider | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_thinking_only_sanitizer.py` | test | Tests for the thinking-only assistant message sanitizer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_thinking_prefill_trailing_turn.py` | test | Regression test for the thinking-only prefill reaching the wire. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_thinking_sig_recovery_persistence.py` | test | Regression tests for the thinking-block signature recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tls_fd_recycle_corruption.py` | test | Regressions for issue #29507 — cross-thread close of the per-request OpenAI | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_token_persistence_non_cli.py` | test | Python module `test_token_persistence_non_cli.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tool_activity_heartbeat.py` | test | Tests for the in-flight tool activity heartbeat (#84491). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tool_arg_coercion.py` | test | Tests for tool argument type coercion. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tool_batch_segmentation.py` | test | Segment-aware mixed tool-batch dispatch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tool_call_args_sanitizer.py` | test | Tests for AIAgent._sanitize_tool_call_arguments. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tool_call_guardrail_runtime.py` | test | Runtime tests for tool-call loop guardrails. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tool_call_incremental_persistence.py` | test | Behavior contracts for incremental tool-call persistence (#49045). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tool_executor_contextvar_propagation.py` | test | Regression guard for PR #16660 (salvaged as PR #18027): ContextVar | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_tool_name_db_persistence.py` | test | Test that tool_name is correctly persisted to the session DB for tool-result messages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_turn_completion_explainer.py` | test | Tests for the end-of-turn completion explainer (#34452). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_unicode_ascii_codec.py` | test | Tests for UnicodeEncodeError recovery with ASCII codec. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_verification_continuation_budget.py` | test | End-to-end regression coverage for verification budget exhaustion (#61631, #65919 §7). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_vision_aware_preprocessing.py` | test | Tests for the vision-aware image preprocessing in run_agent.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_vision_tool_messages.py` | test | Tests for proactive vision-tool-message downgrade (issue #41072). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_agent/test_wait_state_visibility.py` | test | Tests for wait-state visibility — the live "what are we waiting on" notices. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/run_interrupt_test.py` | test | Run a real interrupt test with actual AIAgent + delegate child. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/scripts/test_build_skills_index_health.py` | test | Invariants for scripts/build_skills_index.py's health-check guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/scripts/test_contributor_map.py` | test | Tests for the conflict-free contributor mapping system. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/scripts/test_footgun_subprocess_encoding.py` | test | Tests for the ``subprocess text=True without explicit encoding=`` footgun | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/scripts/test_smoke_nemo_relay_shared_metrics.py` | test | Tests for the shared-metrics smoke artifact. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/scripts/test_windows_footguns_full_repo_scan.py` | test | Full-repo self-scan wrapper for scripts/check-windows-footguns.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/secret_sources/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/secret_sources/conformance.py` | test | Conformance kit for :class:`agent.secret_sources.base.SecretSource`. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/secret_sources/test_error_remediation.py` | test | Error remediation for secret sources. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/secret_sources/test_profile_secrets.py` | test | Orchestrator-level profile secret handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/secret_sources/test_secret_source_registry.py` | test | Tests for the secret-source contract + orchestrator. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_actual_setup_skill.py` | test | Smoke tests for the actual-setup optional skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_authoring_standards.py` | test | CI enforcement of the skill authoring standards (AGENTS.md hardline). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_box_skill.py` | test | Durable integration contracts for the bundled Box productivity skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_cloudflare_temporary_deploy_skill.py` | test | Tests for optional-skills/web-development/cloudflare-temporary-deploy/scripts/parse_deploy_output.py | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_comfyui_skill.py` | test | Invariant tests for the bundled comfyui skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_competitor_news_monitor_skill.py` | test | Tests for the competitor-news-monitor skill and competitor-watch blueprint. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_darwinian_evolver_skill.py` | test | Smoke tests for the darwinian-evolver optional skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_document_to_action_items_skill.py` | test | Tests for the document-to-action-items optional skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_email_inbox_triage_skill.py` | test | Tests for the email-inbox-triage bundled skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_fetch_transcript.py` | test | Tests for skills/media/youtube-content/scripts/fetch_transcript.py (issue #22243). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_github_credential_token.py` | test | Regression tests for Tirith-safe GitHub credential extraction (#22722). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_github_issue_to_pr_skill.py` | test | Tests for the github-issue-to-pr bundled skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_google_workspace_api.py` | test | Tests for Google Workspace gws bridge and CLI wrapper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_google_workspace_credential_files.py` | test | Regression test: google-workspace SKILL.md must declare required_credential_files. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_google_workspace_daily_brief_reference.py` | test | Tests for the google-workspace daily-brief reference. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_google_workspace_setup.py` | test | Security-floor tests for the Google Workspace runtime installer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_google_workspace_setup_deps.py` | test | Regression test: google-workspace setup.py REQUIRED_PACKAGES must pin httplib2. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_grounded_citations_skill.py` | test | Tests for the grounded-citations bundled skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_har_derived_api_client_skill.py` | test | Tests for the har-derived-api-client optional skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_hyperliquid_skill.py` | test | Python module `test_hyperliquid_skill.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_mcp_oauth_remote_gateway_skill.py` | test | Tests for the mcp-oauth-remote-gateway optional skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_meeting_action_items_skill.py` | test | Tests for the meeting-action-items bundled skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_memento_cards.py` | test | Tests for optional-skills/productivity/memento-flashcards/scripts/memento_cards.py | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_merge_reconciler_skill.py` | test | Contract checks for the bundled merge-reconciler skill asset. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_office_document_skills.py` | test | Invariant tests for the bundled office/document skills. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_openclaw_migration.py` | test | Python module `test_openclaw_migration.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_openclaw_migration_hardening.py` | test | Tests for the OpenClaw→Hermes migration hardening features. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_pinecone_research_skill.py` | test | Smoke tests for the pinecone-research optional skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_product_price_monitor_skill.py` | test | Tests for the product-price-monitor skill and its price-watch blueprint. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_sdlc_review_skill.py` | test | Contract tests for the bundled SDLC review skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_social_media_content_calendar_skill.py` | test | Tests for the social-media-content-calendar optional skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_telephony_skill.py` | test | Python module `test_telephony_skill.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_tldraw_offline_skill.py` | test | Tests for the tldraw-offline optional skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_unbroker_skill.py` | test | Hermetic tests for the unbroker skill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_weekly_review_planning_skill.py` | test | Tests for the weekly-review-planning skill and blueprint->skill wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_xurl_article_ingestion_docs.py` | test | Python module `test_xurl_article_ingestion_docs.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_xurl_x_search_routing.py` | test | Behavioral contract for xurl / x_search routing guidance. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/skills/test_youtube_quiz.py` | test | Tests for optional-skills/productivity/memento-flashcards/scripts/youtube_quiz.py | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/state/test_compression_lineage_guard.py` | test | Regression tests for stale writes after a compression session split. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/state/test_disk_full_error.py` | test | is_disk_full_error classifies ENOSPC / SQLITE_FULL failures. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/state/test_fts_runtime_rebuild.py` | test | Runtime FTS-corruption self-heal on the SessionDB write path (#65637 class). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/state/test_no_more_rows_retry.py` | test | Retry of transient 'no more rows available' engine errors (#74934 port). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/state/test_session_git_metadata_generation.py` | test | Cross-process ordering for asynchronous session Git metadata probes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/state/test_session_model_usage_pk_heal.py` | test | Unconditional session_model_usage PK heal (#73823, salvage of #73838). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/state/test_session_turn_lease.py` | test | Cross-process session turn lease behavior (#84234). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/state/test_write_lock_patience.py` | test | Write-lock patience for the shared state.db (#74478). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `tests/stress/_fake_worker.py` | test | Fake worker process that exercises the real subprocess contract. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/conftest.py` | test | pytest config for the stress/ subdirectory. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/test_atypical_scenarios.py` | test | Atypical user scenarios and configurations. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/test_benchmarks.py` | test | Scale benchmarks for the Kanban kernel. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/test_concurrency.py` | test | Multi-process concurrency stress test for the Kanban kernel. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/test_concurrency_mixed.py` | test | Harder concurrency stress: mixed operations + larger scale. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/test_concurrency_parent_gate.py` | test | Stress test for parent-completion invariant at the claim gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/test_concurrency_reclaim_race.py` | test | Target the reclaim race specifically. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/test_property_fuzzing.py` | test | Randomized property testing for the Kanban kernel. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/stress/test_subprocess_e2e.py` | test | E2E: dispatcher spawns real Python subprocess workers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_account_usage.py` | test | Python module `test_account_usage.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_atomic_replace_symlinks.py` | test | Regression tests for GitHub #16743 — atomic writes must preserve symlinks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_atomic_write_text_metadata.py` | test | ``atomic_write_text``'s opt-in metadata preservation (mode + owner). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_audio_playback_guard.py` | test | Regression tests for the test-suite audio-playback guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_background_review_list_shapes.py` | test | Regression tests for the list-shape AttributeError guards in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_background_review_session_isolation.py` | test | Tests for background-review session-store isolation (ev0_state). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_base_url_hostname.py` | test | Targeted tests for ``utils.base_url_hostname`` and ``base_url_host_matches``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_batch_runner_checkpoint.py` | test | Tests for batch_runner checkpoint behavior — incremental writes, resume, atomicity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_batch_runner_durability.py` | test | Tests for batch_runner trajectory durability and pool cleanup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_batch_runner_exit_code.py` | test | Regression tests for batch_runner process exit codes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_bitwarden_secrets.py` | test | Hermetic tests for the Bitwarden Secrets Manager integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_cli_manual_compress.py` | test | Python module `test_cli_manual_compress.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_cli_skin_integration.py` | test | Python module `test_cli_skin_integration.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_code_skew.py` | test | Tests for gateway code-skew detection (stale-checkout guard). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_command_secret_source.py` | test | E2E tests for the ``command`` secret source. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_compression_watermark_commit.py` | test | Watermark commit: concurrent appends survive in-place compaction (#75316). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_conftest_wal_gate.py` | test | The conftest WAL gate must agree with ev0_state, and must not import it. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_copilot_initiator.py` | test | Tests for per-turn Copilot x-initiator header injection (issue #3040). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_credential_file_permissions.py` | test | Read-time permission warnings for on-disk credential/token files. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_cron_manage_profile_scope.py` | test | cron.manage optional ``profile`` param — per-profile store scoping. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ctx_halving_fix.py` | test | Tests for the context-halving bugfix. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_delegate_cascade_49148.py` | test | Regression tests for delegate-child cascade collection (#49148). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_desktop_update_windows_python_handoff.py` | test | Regression: the Windows Desktop update hand-off must run through python.exe. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_desktop_update_windows_timestamp.py` | test | Regression tests for Windows desktop-update Unix timestamps. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_dispatch_session_id.py` | test | Tests that handle_function_call forwards session_id into registry.dispatch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_empty_model_fallback.py` | test | Tests for empty model fallback — when provider is configured but model is missing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_empty_session_hygiene.py` | test | Tests for empty-session hygiene — gemini-cli#27770 port. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_engines_satisfiable.py` | test | The manifest's ``engines`` must be satisfiable by a toolchain we can actually ship. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_env_loader_applied_homes.py` | test | Regression tests for #40597: _APPLIED_HOMES must be marked AFTER a real | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_env_loader_op_bootstrap.py` | test | Tests for the 1Password bootstrap-token reliability patches. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_env_loader_secret_sources.py` | test | Tests for the secret-source tracking in ``ev0_cli.env_loader``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_estop.py` | test | Global emergency stop (`hermes pause` / `hermes resume`) — agent/estop.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_bootstrap.py` | test | Tests for ev0_bootstrap — Windows UTF-8 stdio shim. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_constants.py` | test | Tests for ev0_constants module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_home_profile_warning.py` | test | Tests for get_hermes_home() profile-mode fallback warning. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_logging.py` | test | Tests for ev0_logging — centralized logging setup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_state.py` | test | Tests for ev0_state.py — SessionDB SQLite CRUD, FTS5 search, export. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_state_compression_busy_retry.py` | test | Appends flow freely during compression; the commit preserves them (#75316). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_state_compression_locks.py` | test | Tests for ``SessionDB`` compression-lock primitives. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_state_readonly_preflight.py` | test | Tests for the read-only DB preflight (port of Kilo-Org/kilocode#12508). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ev0_state_wal_fallback.py` | test | Tests for the WAL→DELETE journal-mode fallback on NFS / SMB / FUSE. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_evidence_store.py` | test | Python module `test_evidence_store.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_fast_safe_load.py` | test | Invariants for utils.fast_safe_load. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_fts_cjk_bigram.py` | test | Tests for the messages_fts_cjk CJK-bigram index (salvaged from PR #65544). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_fts_update_of_narrowing.py` | test | FTS UPDATE OF narrowing + migration (#73639 retargeted onto split SessionDB). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_gateway_streaming_nested_config.py` | test | Regression test for #25676 — nested gateway.streaming config must be loaded. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_get_tool_definitions_cache_isolation.py` | test | Regression tests for issue #17335. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_gitlock.py` | test | Tests for ev0_cli.gitlock — stale git lock recovery + ancestry probe. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_hermetic_side_effect_guards.py` | test | Regression tests for hermetic guards around local desktop side effects. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_honcho_client_concurrency.py` | test | Concurrency test for get_honcho_client() — the TOCTOU race fix (#24759). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_honcho_client_config.py` | test | Tests for Honcho client configuration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_honcho_session_context.py` | test | Tests for Honcho session context peer resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_honcho_startup_fail_open.py` | test | Regression tests for Honcho startup fail-open behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_autostash_conflict_recovery.py` | test | Regression: installer autostash restore conflicts must not abort the run. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_commit_pin_rollback.py` | test | Regression: a stale ``--commit`` pin must not roll an install backwards. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_diverged_update.py` | test | Regression: installer/bootstrap must recover from diverged managed clones. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_lockfile_churn.py` | test | Regression: installer update should discard pure npm lockfile churn. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_macos_launcher.py` | test | Regression coverage for the user-facing macOS Hermes launcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_no_initial_commit.py` | test | Regression for #40998: installer fails on an interrupted prior clone. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_ascii_only.py` | test | Regression: install.ps1 must stay pure ASCII. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_browser_install.py` | test | Regression test for install.ps1 browser setup (PR #44772 review). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_managed_node_swap.py` | test | Regression: the Test-Node managed-Node stage-and-swap must stay same-directory. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_native_stderr_eap.py` | test | Regression tests for #48352: Windows PowerShell 5.1 native stderr. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_node_path_for_npm.py` | test | Regression tests for #48130: Windows npm lifecycle scripts need node on PATH. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_python_fallback_venv.py` | test | Regression: the Windows installer must honor its Python fallback at venv time. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_uv_install_fallback.py` | test | Regression: Install-Uv must surface installer errors and have fallbacks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_uv_powershell_host.py` | test | Regression: the Windows installer must not spawn a bare ``powershell``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_venv_process_tree.py` | test | Windows installer regression for Hermes children outside the venv. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_venv_recreate_safety.py` | test | Regression tests for transactional Windows venv recreation (#83149). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_venv_rename_abort.py` | test | Regression: Windows installer must not gut the venv on rename failure (#83149). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_venv_transaction_boundary.py` | test | Transaction-boundary regression for Windows venv recreation (#83149). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_ps1_web_server_syntax_probe.py` | test | Regression: install.ps1 must syntax-check the dashboard backend source. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_scripts_computer_use.py` | test | Regression tests: installers provision cua-driver (Computer Use). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_acp_launcher.py` | test | `setup_path()` must also install a `hermes-acp` launcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_bootstrap_marker.py` | test | install.sh must stamp the desktop bootstrap-complete marker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_browser_install.py` | test | Regression tests for install.sh browser setup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_install_method_stamp.py` | test | Contract test: install.sh stamps the install method next to the code tree | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_node_deps_failure.py` | test | Behavioral coverage for required Node dependency installation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_node_global_prefix.py` | test | Regression tests for the Hermes-managed Node's npm global prefix. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_node_npm_check.py` | test | Regression tests for install.sh Node/npm checks (#77003). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_pythonpath_sanitization.py` | test | Regression tests for install.sh Python environment sanitization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_root_fhs_uv_python_path.py` | test | Regression test for install.sh root-mode uv Python install path. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_setup_wizard_tty_probe.py` | test | Regression for #16746: install.sh /dev/tty gates must actually open /dev/tty. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_symlink_stomp.py` | test | Regression for #21454: re-running install.sh on a symlinked prior install. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_sh_termux_network_prereqs.py` | test | Regression tests for Termux network prerequisite handling in install.sh. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_install_unmerged_index.py` | test | Regression: installer fails when the existing checkout has an unmerged index. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ipv4_preference.py` | test | Tests for network.force_ipv4 — the socket.getaddrinfo monkey-patch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_iron_proxy.py` | test | Hermetic tests for the iron-proxy egress integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_iron_proxy_cli.py` | test | Unit tests for ``ev0_cli.proxy_cli`` command handlers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_iron_proxy_e2e.py` | test | End-to-end smoke test for the iron-proxy egress integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_journal_mode_config.py` | test | Behavioral coverage for #68545's centralized journal-mode setting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_lazy_secrets_dispatch.py` | test | End-to-end tests for lazy cryptography loading. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_lazy_secrets_import.py` | test | Regression test: hermes update must not load cryptography eagerly. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_lazy_session_regressions.py` | test | Reproduction tests for #18370 fallout: lazy session creation regressions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_list_recent_user_messages_handoffs.py` | test | list_recent_user_messages must skip legacy compaction handoffs (#80622). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_live_system_guard.py` | test | Regression tests for the conftest live-system guard's argv handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_live_system_guard_self_test.py` | test | Self-test for the live-system guard fixture in tests/conftest.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_log_isolation.py` | test | The test suite must never write into the operator's real Hermes logs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_managed_runtime_resolution.py` | test | Guard: Hermes-owned subprocesses must not resolve managed runtimes by bare PATH. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_mcp_serve.py` | test | Tests for mcp_serve — Hermes MCP server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_message_reactions.py` | test | Message reactions: persistence, tapback semantics, and cache safety. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_mini_swe_runner.py` | test | Python module `test_mini_swe_runner.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_minimax_model_validation.py` | test | Tests for MiniMax model validation via static catalog (issues #12611, #12460, #12399, #12547). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_minimax_oauth.py` | test | Tests for MiniMax OAuth provider (ev0_cli/auth.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_minisweagent_path.py` | test | Python module `test_minisweagent_path.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_moa_prepared_request_leak_78382.py` | test | Test: _moa_prepared_request does not leak to native OpenAI clients (#78382). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_model_forces_max_completion_tokens.py` | test | Targeted tests for ``utils.model_forces_max_completion_tokens``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_model_picker_scroll.py` | test | Tests for the scrolling viewport logic in _curses_prompt_choice (issue #5755). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_model_tools.py` | test | Tests for model_tools.py — function call dispatch, agent-loop interception, legacy toolsets. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_model_tools_async_bridge.py` | test | Regression tests for the _run_async() event-loop lifecycle. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_no_shadowed_test_definitions.py` | test | No test module may define the same name twice in one scope. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_ollama_num_ctx.py` | test | Tests for Ollama num_ctx context length detection and injection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_onepassword_secrets.py` | test | Hermetic tests for the 1Password (`op` CLI) secret source. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_os_marker_gating.py` | test | The collection guard against a test carrying two host-OS markers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_output_cap_parsing.py` | test | Python module `test_output_cap_parsing.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_packaging_build_guard.py` | test | Behavioral regression coverage for the wheel/sdist distribution guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_packaging_metadata.py` | test | Python module `test_packaging_metadata.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_plugin_skills.py` | test | Tests for namespaced plugin skill registration and resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_plugin_utils.py` | test | Tests for plugins/plugin_utils.py — thread-safe lazy singleton helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_process_loop_event_loop_warning.py` | test | Tests for the process_loop RuntimeWarning fix -- issue #19285. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_profile_isolation_runtime.py` | test | Profile-isolation regression tests for single-process multi-profile runtimes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_project_metadata.py` | test | Regression tests for packaging metadata in pyproject.toml. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_pty_keepalive_ws.py` | test | Python module `test_pty_keepalive_ws.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_pty_session.py` | test | Python module `test_pty_session.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_redaction_registry.py` | test | Tests for the plugin redaction-pattern registry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_resource_limits.py` | test | Tests for configurable RLIMIT_NOFILE startup handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_retry_utils.py` | test | Tests for agent.retry_utils jittered backoff. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_run_tests_parallel.py` | test | Verify scripts/run_tests_parallel.py kills test-spawned grandchildren. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_run_tests_parallel_stdio.py` | test | The runner's status glyphs must not crash narrow console encodings. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_sanitize_tool_error.py` | test | Tests for `_sanitize_tool_error` in model_tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_schema_read_probe.py` | test | Contract tests for schema_read_probe_statements(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_search_slow_query_log.py` | test | Tests for the session-search slow-query log (salvaged from PR #65544). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_secret_scope_plugin_families.py` | test | Regression tests: plugin-family credential reads honor the profile secret scope. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_session_db_context_manager.py` | test | ``SessionDB`` must support ``with``, so an owning scope releases its fds. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_session_db_read_conn_pool.py` | test | The SessionDB read path must not leak one connection per (SessionDB x thread). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_session_db_read_path_split.py` | test | Tests for the SessionDB read-path split (pooled read-only connections). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_session_skill_previews.py` | test | Session previews must never surface a /skill's own body. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_session_system_prompt_dedup.py` | test | Behavior coverage for content-addressed session system prompts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_session_vacuum_config.py` | test | Python module `test_session_vacuum_config.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_session_workspace_binding.py` | test | Session <-> workspace grouping key (ev0_state.workspace_key). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_slack_thread_require_mention.py` | test | Python module `test_slack_thread_require_mention.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_slash_worker_watchdog.py` | test | Python module `test_slash_worker_watchdog.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_sql_injection.py` | test | Tests that verify SQL injection mitigations in insights and state modules. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_sqlite_lock_safe_inspection.py` | test | POSIX advisory locks must survive Hermes' own database inspection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_sqlite_wal_reset_gate.py` | test | SQLite WAL-reset vulnerability gate (issue #69784). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_stale_tool_call_marker_session_repair.py` | test | Tests for stale tool-call marker session repair (ev0_state, #78148). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_stale_utils_module_import.py` | test | Regression for the stale-``utils``-module ImportError after a hot ``git pull``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_state_db_malformed_repair.py` | test | Recovery from a malformed state.db schema (duplicate sqlite_master rows). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_state_db_notadb_selfheal.py` | test | Tests for the state.db runtime connection self-heal (PR #82280 remainder). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_state_db_repair_loop_cap.py` | test | #86747 regression: the state.db repair loop must be bounded across restarts | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_state_db_stats.py` | test | Tests for state.db health/stats collection (hermes doctor section). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_subprocess_home_isolation.py` | test | Tests for subprocess HOME handling in profile mode. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_telegram_polling_progress_ptb.py` | test | Integration coverage for polling progress against the installed PTB runtime. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_termux_all_extra_compat.py` | test | Regression coverage for the Termux broad install profile. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_timezone.py` | test | Tests for timezone support (ev0_time module + integration points). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_tini_shim.py` | test | Unit tests for docker/tini-shim.sh argument stripping (#66679). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_toolset_distributions.py` | test | Tests for toolset_distributions.py — distribution CRUD, sampling, validation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_toolsets.py` | test | Tests for toolsets.py — toolset resolution, validation, and composition. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_trajectory_compressor.py` | test | Tests for trajectory_compressor.py — config, metrics, and compression logic. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_trajectory_compressor_async.py` | test | Tests for trajectory_compressor AsyncOpenAI event loop binding. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_transform_api_error_classification_hook.py` | test | Tests for the ``transform_api_error_classification`` plugin hook. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_transform_llm_output_hook.py` | test | Tests for the ``transform_llm_output`` plugin hook. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_transform_tool_result_hook.py` | test | Tests for the ``transform_tool_result`` plugin hook wired into | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_tui_entry_mcp_owner.py` | test | Regression tests: the stdio TUI consults the shared MCP discovery owner. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_tui_gateway_loop_noise.py` | test | Tests for tui_gateway.loop_noise — the WS peer-hangup teardown filter (#50005). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_tui_gateway_queue_on_busy.py` | test | A prompt that lands mid-turn is redirected or queued, never dropped. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_tui_gateway_server.py` | test | Python module `test_tui_gateway_server.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_tui_gateway_server_crash_history.py` | test | Regression coverage for crashed TUI gateway turns. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_tui_gateway_ws.py` | test | Python module `test_tui_gateway_ws.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_tui_mcp_late_refresh.py` | test | Tests for the TUI gateway's late MCP tool-snapshot refresh. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_utils_atomic_roundtrip_yaml_save.py` | test | Tests for atomic_roundtrip_yaml_save() — comment-preserving full-state writes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_utils_truthy_values.py` | test | Tests for shared truthy-value helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_voice_max_recording_seconds.py` | test | Regression test: voice.max_recording_seconds is actually enforced. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_wal_checkpoint_strategy.py` | test | Tests for SessionDB WAL checkpoint strategy (issue #45383). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_web_server.py` | test | Test that start_server configures ws-ping keepalive. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_web_server_sessiondb_eventloop.py` | test | Python module `test_web_server_sessiondb_eventloop.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_web_server_status_topology_cache.py` | test | Regression tests for the /api/status profile-topology cache. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_windows_subprocess_no_window_flags.py` | test | Python module `test_windows_subprocess_no_window_flags.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_yaml_indent_consistency_31999.py` | test | Regression tests for issue #31999. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_yuanbao_integration.py` | test | test_yuanbao_integration.py - Yuanbao 模块集成测试 | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_yuanbao_markdown.py` | test | test_yuanbao_markdown.py - Unit tests for yuanbao_markdown.py | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_yuanbao_pipeline.py` | test | test_yuanbao_pipeline.py - Unit tests for the inbound middleware pipeline. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_yuanbao_proto.py` | test | test_yuanbao_proto.py - yuanbao_proto 单元测试 | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_yuanbao_reconnect_set_active.py` | test | test_yuanbao_reconnect_set_active.py - Verify _do_reconnect restores the active singleton. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_yuanbao_shutdown.py` | test | test_yuanbao_shutdown.py - Yuanbao adapter shutdown teardown timing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/test_zeroed_state_db.py` | test | #68474 hardening: zeroed state.db detection + quarantine. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/conftest.py` | test | Shared fixtures for tests/tools/ web-provider tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_accretion_caps.py` | test | Accretion caps for _read_tracker (file_tools) and _completion_consumed | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_ansi_strip.py` | test | Comprehensive tests for ANSI escape sequence stripping (ECMA-48). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approval.py` | test | Tests for the dangerous command approval module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approval_config_readonly.py` | test | Regression tests: the approval guard path reads config via | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approval_deny_rules.py` | test | Tests for user-defined deny rules (approvals.deny in config.yaml). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approval_hook_session_id.py` | test | Approval hooks must carry the Hermes session id to observer plugins. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approval_interrupt.py` | test | Regression: a blocking gateway approval wait must honor an interrupt (#8697). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approval_mode_parity.py` | test | Cross-surface approval mode/timeout parity invariant. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approval_plugin_hooks.py` | test | Tests for pre_approval_request / post_approval_response plugin hooks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approval_windows.py` | test | Windows destructive-command approval coverage (#69472). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_approved_command_clean_slate.py` | test | Regression tests: a user-approved command runs from a clean interrupt slate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_async_delegation.py` | test | Tests for async (background) delegation — tools/async_delegation.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_async_delegation_fd_leak.py` | test | Regression: the async-delegation ledger must close every SQLite connection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_audio_container.py` | test | Tests for the shared magic-byte audio container sniffer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_base_environment.py` | test | Tests for BaseEnvironment unified execution model. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_binary_document_write_guard.py` | test | Tests for the binary-document write guard (port of nearai/ironclaw#7109). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_blocked_command_guidance.py` | test | Tests for blocked-command recovery guidance (parser-limit + backgrounding). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_blueprints.py` | test | Tests for the blueprints layer (skill frontmatter <-> cron automation bridge). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_bot_mode_probe.py` | test | Tests for tools/bot_mode_probe.py — the Bot Mode teammate-protocol section. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_camofox.py` | test | Tests for the Camofox browser backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_camofox_auth.py` | test | Tests that Camofox browser sends Authorization header when CAMOFOX_API_KEY is set. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_camofox_ensure_tab.py` | test | Regression test: _ensure_tab must send ``listItemId`` (not ``sessionKey``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_camofox_persistence.py` | test | Persistence tests for the Camofox browser backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_camofox_private_page_guard.py` | test | Regression tests for the Camofox private-page read guards. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_camofox_state.py` | test | Tests for Hermes-managed Camofox state helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_camofox_timeout.py` | test | Tests for browser_camofox._get_command_timeout — config-driven timeout. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_cdp_override.py` | test | Python module `test_browser_cdp_override.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_cdp_tool.py` | test | Unit tests for browser_cdp tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_chromium_autoinstall.py` | test | Tests for gated Chromium-binary auto-install on local cold start. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_chromium_check.py` | test | Tests for Chromium-presence detection in browser_tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_cleanup.py` | test | Regression tests for browser session cleanup and screenshot recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_cloud_fallback.py` | test | Tests for cloud browser provider runtime fallback to local Chromium. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_cloud_provider_cache.py` | test | Tests for ``_get_cloud_provider()`` caching policy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_command_timeout_race.py` | test | Regression tests for the _get_command_timeout cache race (#14331). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_console.py` | test | Tests for browser_console tool and browser_vision annotate param. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_console_ssrf.py` | test | Tests that browser_console blocks console messages and errors from eval-navigated private pages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_content_none_guard.py` | test | Tests for None guard on browser_tool LLM response content. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_eval_ssrf.py` | test | Tests that browser_console(expression=...) cannot bypass the SSRF guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_eval_supervisor_path.py` | test | Unit tests for the supervisor-WS fast path in browser_console / _browser_eval. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_get_images_ssrf.py` | test | Tests that browser_get_images blocks image data from eval-navigated private pages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_hardening.py` | test | Tests for browser_tool.py hardening: caching, security, thread safety, truncation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_headed_mode.py` | test | Tests for headed browser mode: config/env resolution, --headed injection, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_homebrew_paths.py` | test | Tests for macOS Homebrew PATH discovery in browser_tool.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_hybrid_routing.py` | test | Tests for hybrid browser-backend routing (LAN/localhost auto-local). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_lightpanda.py` | test | Tests for Lightpanda engine support in browser_tool.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_npx_warmup.py` | test | Tests for tools.browser_tool.warm_agent_browser_npx_cache (#43564, security | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_open_timeout.py` | test | Tests for browser first-open timeout and timeout diagnostics. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_orphan_reaper.py` | test | Tests for _reap_orphaned_browser_sessions() — kills orphaned agent-browser | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_private_page_action_guard.py` | test | Regression tests for private-page browser interaction guards. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_secret_exfil.py` | test | Tests for secret exfiltration prevention in browser and web tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_snapshot_ssrf.py` | test | Tests that browser_snapshot blocks content from eval-navigated private pages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_ssrf_local.py` | test | Tests that browser_navigate SSRF checks respect local-backend mode and | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_supervisor.py` | test | Integration tests for tools.browser_supervisor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_supervisor_healthcheck.py` | test | Unit tests for _SupervisorRegistry cache-hit healthcheck. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_type_redaction.py` | test | Regression tests for browser_type display redaction. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_use_cli.py` | test | Tests for the Browser Use CLI 3.0 backend (tools/browser_use_cli.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_browser_use_session_expiry.py` | test | Regression coverage for provider-authoritative cloud browser expiry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_budget_config.py` | test | Unit tests for tools/budget_config.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_build_subprocess_env.py` | test | Tests for tools.environments.local.build_subprocess_env — the single | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_checkpoint_manager.py` | test | Tests for tools/checkpoint_manager.py — CheckpointManager (v2 single-store). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_clarify_gateway.py` | test | Tests for the gateway-side clarify primitive (tools/clarify_gateway.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_clarify_tool.py` | test | Tests for tools/clarify_tool.py - Interactive clarifying questions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_cli_approval_exec_ask_leak.py` | test | Regression: interactive CLI must not lose the Dangerous Command panel. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_clipboard.py` | test | Tests for clipboard image paste — clipboard extraction, multimodal conversion, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_code_execution.py` | test | Tests for the code execution sandbox (programmatic tool calling). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_code_execution_modes.py` | test | Tests for execute_code's strict / project execution modes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_code_execution_windows_env.py` | test | Tests for execute_code env scrubbing on Windows. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_command_guards.py` | test | Tests for check_all_command_guards() — combined tirith + dangerous command guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use.py` | test | Tests for the computer_use toolset (cua-driver backend, universal schema). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_approval_isolation.py` | test | Regression: leaked approval callbacks must not poison later tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_browser_authorization.py` | test | Authorization plumbing for the cua-driver typed browser route. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_browser_contract_020.py` | test | Behavior coverage for the cua-driver 0.20 public browser contract. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_capture_routing.py` | test | End-to-end regression for #24015 — capture routing via auxiliary.vision. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_cua_0_10_permissions.py` | test | Behavior contracts for cua-driver 0.10 permission-mode integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_cua_0_9.py` | test | Behavior contracts for cua-driver's verify/escalate and typed-browser ladder. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_cua_backend_linux.py` | test | Regression tests for Linux/X11 capture target selection (#58026, #54173). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_delivery_ladder.py` | test | Regression tests for the cua-driver verify → escalate ladder. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_display_count_guard.py` | test | macOS ScreenCaptureKit display_count=0 diagnosability. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_empty_discovery_diagnosis.py` | test | Diagnosability of empty window discovery + CLI-fallback fail-fast. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_input_target_guard.py` | test | Input actions must not silently deliver to a different app than requested. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_null_pid_windows.py` | test | Regression for the X11 null-PID `list_windows` crash. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_placeholder_ids.py` | test | A zero-filled ``pid``/``window_id`` must not be read as exact targeting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_vision_routing.py` | test | Unit tests for tools.computer_use.vision_routing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_computer_use_zero_bounds.py` | test | Zero-rect AX bounds must read as 'unknown', never as a clickable position. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_config_null_guard.py` | test | Tests for config.get() null-coalescing in tool configuration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_container_cwd_sanitize.py` | test | Regression tests for host-path cwd sanitization on container backends. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_credential_files.py` | test | Tests for credential file passthrough and skills directory mounting. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_credential_pool_env_fallback.py` | test | Tests for credential_pool .env fallback and auth credential_pool lookup. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_cron_approval_mode.py` | test | Tests for approvals.cron_mode — configurable approval behavior for cron jobs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_cron_prompt_injection.py` | test | Regression tests for cron prompt injection scanner bypass. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_cronjob_run_background.py` | test | Tests for cronjob action='run' background dispatch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_cronjob_run_immediate.py` | test | Tests for cronjob action='run' immediate execution (#41037). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_cronjob_tools.py` | test | Tests for tools/cronjob_tools.py — prompt scanning, schedule/list/remove dispatchers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_cross_profile_guard.py` | test | Tests for the cross-profile soft guard wired into write_file / patch / | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_daemon_pool.py` | test | Tests for tools.daemon_pool.DaemonThreadPoolExecutor. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_daytona_environment.py` | test | Unit tests for the Daytona cloud sandbox environment backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_debug_helpers.py` | test | Tests for tools/debug_helpers.py — DebugSession class. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate.py` | test | Tests for the subagent delegation tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_apiserver_background.py` | test | delegate_task(background=true) on stateless API-server sessions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_batch_validation.py` | test | Batch input validation for delegate_task(tasks=[...]). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_composite_toolsets.py` | test | Tests for composite toolset expansion in delegate_task intersection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_control_actions.py` | test | delegate_task(action=...) — model-facing live orchestration of subagents. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_cost_footer.py` | test | Per-delegation cost in the serialized result entry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_cron_sync_fallback.py` | test | Regression test for #86632: cron's synchronous delegate_task fallback must | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_kanban_isolation.py` | test | Regression tests for delegate_task isolation from parent Kanban workers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_output_schema.py` | test | T1-24: structured-output schema on delegate_task. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_subagent_timeout_diagnostic.py` | test | Regression tests for subagent timeout diagnostic dump (issue #14726). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_summary_budget.py` | test | Tests for subagent summary budgeting (PR #9126). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegate_toolset_scope.py` | test | Tests for delegate_tool toolset scoping. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_delegation_live_log.py` | test | Tests for tools/delegation_live_log.py — live subagent transcripts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_denial_circuit_breaker.py` | test | Tests for the consecutive-denial circuit breaker in smart approvals. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_desktop_ui.py` | test | Tests for the desktop-only renderer-event bridge. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_discord_send_message_caption.py` | test | Discord standalone MEDIA:<path> caption delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_discord_tool.py` | test | Tests for the Discord server introspection and management tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_cgroup_limits.py` | test | Tests for cgroup resource-limit gating in the docker backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_config_migrate.py` | test | Python module `test_docker_config_migrate.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_daemon_redirect.py` | test | Docker/Podman daemon-redirect and lifecycle flag-insertion detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_environment.py` | test | Python module `test_docker_environment.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_find.py` | test | Tests for tools.environments.docker.find_docker — Docker CLI discovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_network_config.py` | test | Regression tests for the Docker terminal network toggle. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_orphan_reaper_integration.py` | test | Integration tests for the docker orphan-reaper wiring in terminal_tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_rebootstrap_nous_session.py` | test | Unit tests for scripts/docker_rebootstrap_nous_session.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_docker_session_isolation.py` | test | Per-session docker container isolation (docker + container_persistent: false). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_dockerfile_immutable_install.py` | test | Contract tests for the Docker image's immutable /opt/hermes install tree. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_dockerfile_node_modules_perms.py` | test | Contract test: Docker TUI must not require writable node_modules. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_dockerfile_pid1_reaping.py` | test | Contract tests for the container Dockerfile. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_ensure_task_env.py` | test | Unit tests for terminal_tool.ensure_task_env — the lazy sandbox bring-up | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_env_passthrough.py` | test | Tests for tools.env_passthrough — skill and config env var passthrough. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_env_probe.py` | test | Tests for tools/env_probe.py — local Python toolchain probe. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_ev0_subprocess_env.py` | test | Tests for ev0_subprocess_env() — the centralized credential-safe env | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_execute_code_approval_cluster.py` | test | Regression tests for the execute_code approval-bypass cluster. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_execution_flag_detection.py` | test | Execution-bearing option detection across interpreters and read-only tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_fal_common.py` | test | Tests for tools/fal_common.py — shared FAL.ai SDK plumbing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_feishu_tools.py` | test | Tests for feishu_doc_tool and feishu_drive_tool — registration and schema validation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_operations.py` | test | Tests for tools/file_operations.py — deny list, result dataclasses, helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_operations_edge_cases.py` | test | Tests for edge cases in tools/file_operations.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_ops_cwd_tracking.py` | test | Regression tests for cwd-staleness in ShellFileOperations. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_read_guards.py` | test | Tests for read_file_tool safety guards: device-path blocking, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_staleness.py` | test | Tests for file staleness detection in write_file and patch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_state_registry.py` | test | Tests for the cross-agent FileStateRegistry (tools/file_state.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_sync.py` | test | Tests for FileSyncManager — mtime tracking, deletion detection, transactional rollback. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_sync_back.py` | test | Tests for FileSyncManager.sync_back() — pull remote changes to host. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_sync_perf.py` | test | Reproducible perf benchmark for file sync overhead. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_sync_sigint.py` | test | Cross-platform regression for the deferred-SIGINT re-delivery in sync-back. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_tools.py` | test | Tests for the file tools module (schema, handler wiring, error paths). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_tools_container_config.py` | test | Tests for docker container_config key propagation in file_tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_tools_cwd_resolution.py` | test | Regression tests for file-tool path resolution base correctness. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_tools_live.py` | test | Live integration tests for file operations and terminal tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_tools_tilde_profile.py` | test | Regression tests for profile-aware tilde expansion in file tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_write_safety.py` | test | Tests for file write safety and HERMES_WRITE_SAFE_ROOT sandboxing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_file_write_surrogate_roundtrip.py` | test | Surrogate-safe stdin piping for the local execution environment (#79178). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_find_shell.py` | test | Tests for _find_shell — user-login-shell preference on POSIX. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_flux3_video_tool.py` | test | Native BFL FLUX 3 tools: gating, transport, media delivery, redaction. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_focus_pane_tool.py` | test | Tests for the GUI-surface ``focus_pane`` tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_force_dangerous_override.py` | test | Regression tests for skills guard policy precedence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_fuzzy_match.py` | test | Tests for the fuzzy matching module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_gateway_cwd_contract.py` | test | Tool-surface cwd contract tests for gateway workspaces. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_generation_source_confinement.py` | test | Tests for the generation-tool source-image confinement chokepoint. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_gnu_long_option_abbreviation_bypass.py` | test | Tests for GNU long-option abbreviation bypass in DANGEROUS_PATTERNS. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_hardline_blocklist.py` | test | Tests for the unconditional hardline command blocklist. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_heartbeat_stale_thresholds.py` | test | Tests for delegate heartbeat stale threshold configuration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_hidden_dir_filter.py` | test | Tests for the hidden directory filter in skills listing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_homeassistant_tool.py` | test | Tests for the Home Assistant tool module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_hook_output_spill.py` | test | Tests for tools.hook_output_spill. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_hub_lock_non_utf8_68053.py` | test | Regression test for #68053 — hub lock.json with Windows-1252 bytes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_image_generation.py` | test | Tests for tools/image_generation_tool.py — FAL multi-model support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_image_generation_artifacts.py` | test | Python module `test_image_generation_artifacts.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_image_generation_env.py` | test | FAL_KEY env var normalization (whitespace-only treated as unset). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_image_generation_image_to_image.py` | test | Tests for the image-to-image / editing surface of ``image_generate``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_image_generation_interrupt.py` | test | _wait_fal_result must notice a user interrupt while the FAL job runs. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_image_generation_plugin_dispatch.py` | test | Python module `test_image_generation_plugin_dispatch.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_image_source.py` | test | Tests for tools/image_source.py — the unified vision image-source resolver. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_init_session_cwd_respect.py` | test | Tests that init_session() respects the configured cwd. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_interrupt.py` | test | Tests for the interrupt system. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_interrupted_command_cwd.py` | test | An interrupted command must not adopt the shared environment's cwd. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_kanban_comment_injection.py` | test | Live operator-note injection into a running kanban worker. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_kanban_redaction.py` | test | Tests: redact_sensitive_text is applied in kanban tool handlers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_kanban_tools.py` | test | Tests for the Kanban tool surface (tools/kanban_tools.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_lazy_deps.py` | test | Tests for tools.lazy_deps — the supply-chain-resilient on-demand installer. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_lazy_deps_durable_target.py` | test | Tests for the durable lazy-install target (immutable Docker images). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_lazy_deps_managed.py` | test | Managed-install guard in :func:`tools.lazy_deps.ensure` (#48628). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_line_ending_preservation.py` | test | Tests for CRLF line-ending preservation in write_file and patch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_llm_content_none_guard.py` | test | Tests for None guard on response.choices[0].message.content.strip(). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_background_child_hang.py` | test | Regression tests for issue #8340. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_cwd_permission_fallback.py` | test | Regression tests for inaccessible-cwd fallback (#65583). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_env_blocklist.py` | test | Tests for subprocess env sanitization in LocalEnvironment. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_env_cwd_recovery.py` | test | Tests for LocalEnvironment recovery when ``self.cwd`` is deleted. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_env_relative_cwd.py` | test | Regression tests for local terminal initial cwd normalization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_env_session_leak.py` | test | Cross-session HERMES_SESSION_* leak guard for the local terminal backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_env_windows_msys.py` | test | Tests for the Windows / Git Bash MSYS-path normalization in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_interrupt_cleanup.py` | test | Regression tests for _wait_for_process subprocess cleanup on exception exit. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_shell_init.py` | test | Tests for terminal.shell_init_files / terminal.auto_source_bashrc. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_local_tempdir.py` | test | Python module `test_local_tempdir.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_managed_browserbase_and_modal.py` | test | Python module `test_managed_browserbase_and_modal.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_managed_media_gateways.py` | test | Python module `test_managed_media_gateways.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_managed_modal_environment.py` | test | Python module `test_managed_modal_environment.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_managed_tool_gateway.py` | test | Python module `test_managed_tool_gateway.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_bridge_single_failure.py` | test | Regression test for #50394. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_cancelled_error_propagation.py` | test | Regression tests for ``MCPServerTask.run`` + ``asyncio.CancelledError``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_capability_gating.py` | test | Tests for capability-gated MCP tool discovery and keepalive. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_circuit_breaker.py` | test | Tests for MCP tool-handler circuit-breaker recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_client_cert.py` | test | Tests for mTLS client certificate config on MCP HTTP/SSE transports. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_config_whitespace_warning.py` | test | Tests for MCP config hidden-whitespace warnings. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_dashboard_oauth.py` | test | Hosted-dashboard bridge for MCP OAuth browser callbacks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_discovery_cross_process.py` | test | Cross-process regression coverage for MCP discovery serialization. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_dynamic_discovery.py` | test | Tests for MCP dynamic tool discovery (notifications/tools/list_changed). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_elicitation.py` | test | Tests for the MCP elicitation handler in tools.mcp_tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_empty_error_message.py` | test | Regression tests for MCP error messages when str(exc) is empty. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_failure_classification.py` | test | Tests for exception-group unwrapping and failure classification in | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_identity_header.py` | test | Tests for the per-server MCP identity header (``identity_header``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_image_content.py` | test | Regression tests for MCP ImageContent block handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_initial_connect_shutdown.py` | test | Regression tests for initial MCP failure ownership and teardown. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_invalid_url.py` | test | Tests for the MCP remote-URL validator. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_lazy_start.py` | test | Behavior-contract tests for lazy MCP server startup (#56832). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_list_pagination.py` | test | Tests for MCP list_* pagination (nextCursor draining). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_loop_profile_override.py` | test | Regression tests for HERMES_HOME override propagation onto the MCP loop. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_oauth.py` | test | Tests for tools/mcp_oauth.py — OAuth 2.1 PKCE support for MCP servers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_oauth_bidirectional.py` | test | Regression test for the ``HermesMCPOAuthProvider.async_auth_flow`` bidirectional | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_oauth_cold_load_expiry.py` | test | Tests for cold-load token expiry tracking in MCP OAuth. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_oauth_integration.py` | test | End-to-end integration tests for the MCP OAuth consolidation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_oauth_manager.py` | test | Tests for the MCP OAuth manager (tools/mcp_oauth_manager.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_oauth_metadata.py` | test | Tests for OAuth server metadata persistence across process restarts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_parked_self_probe.py` | test | Tests for the parked-server self-probe revival path (#57129). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_poll_loop_oom_integration.py` | test | End-to-end coverage for the MCP poll-loop OOM spin (#63892). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_preflight_content_type.py` | test | Tests for MCPServerTask._preflight_content_type fast-fail behaviour. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_probe.py` | test | Tests for probe_mcp_server_tools() in tools.mcp_tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_rapid_drop_budget.py` | test | Tests for the MCP rapid-drop reconnect budget (#62212). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_reconnect_log_hygiene.py` | test | Tests for MCP reconnect log hygiene and backoff jitter (#65673, #66092). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_reconnect_retry_reset.py` | test | Tests for MCP reconnect retry counter reset (#57604). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_reconnect_signal.py` | test | Tests for the MCPServerTask reconnect signal. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_register_wakes_stale.py` | test | New sessions must wake parked/stale cached MCP servers immediately. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_resource_content.py` | test | Tests for MCP ResourceLink / EmbeddedResource / AudioContent handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_schema_cache.py` | test | Unit tests for the on-disk MCP schema cache (tools/mcp_schema_cache.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_server_log_notifications.py` | test | Tests for MCP server log notification handling (port of anomalyco/opencode#34529). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_sse_transport.py` | test | Regression tests for SSE transport in ``MCPServerTask._run_http``. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_stability.py` | test | Tests for MCP stability fixes — event loop handler, PID tracking, shutdown robustness. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_stdio_encoding_handler.py` | test | Tests for MCP stdio encoding error handler fix (issue #46099). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_stdio_init_timeout.py` | test | Regression test for the stdio-MCP subprocess/FD leak (#59349). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_stdio_watchdog.py` | test | Contract tests for the direct POSIX stdio MCP child watchdog. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_structured_content.py` | test | Tests for MCP tool structuredContent preservation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_tool.py` | test | Tests for the MCP (Model Context Protocol) client support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_tool_401_handling.py` | test | Tests for MCP tool-handler auth-failure detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_tool_issue_948.py` | test | Python module `test_mcp_tool_issue_948.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_tool_session_expired.py` | test | Tests for MCP tool-handler transport-session auto-reconnect. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_transport_group_reconnect.py` | test | Regression tests for issue #66092. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_trust_gating.py` | test | Tests for MCP tool trust-tier gating via readOnlyHint annotations. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_mcp_utility_capability_gating.py` | test | Regression tests for capability-gated MCP utility schema registration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_media_caption_split.py` | test | Guard test for the MEDIA:<path> caption chokepoint (_media_caption_split). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_memory_tool.py` | test | Tests for tools/memory_tool.py — MemoryStore, security scanning, and tool dispatcher. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_memory_tool_import_fallback.py` | test | Regression tests for memory-tool import fallbacks. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_memory_tool_schema.py` | test | Schema-shape tests for the built-in memory tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_microsoft_graph_auth.py` | test | Tests for tools/microsoft_graph_auth.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_microsoft_graph_client.py` | test | Tests for tools/microsoft_graph_client.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_modal_bulk_upload.py` | test | Tests for Modal bulk upload via tar/base64 archive. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_modal_sandbox_fixes.py` | test | Tests for Modal sandbox infrastructure fixes (TBLite baseline). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_modal_snapshot_isolation.py` | test | Python module `test_modal_snapshot_isolation.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_notify_on_complete.py` | test | Tests for notify_on_complete background process feature. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_open_preview_tool.py` | test | Tests for the GUI-surface ``open_preview`` tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_osv_check.py` | test | Tests for OSV malware check on MCP extension packages. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_parse_env_var.py` | test | Tests for _parse_env_var and _get_env_config env-var validation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_patch_already_applied.py` | test | Tests for already-applied patch detection (success-shaped no-op). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_patch_failure_tracking.py` | test | Tests for per-file consecutive patch-failure tracking. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_patch_multimatch_locations.py` | test | Tests for multi-match location listing in patch ambiguity errors. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_patch_parser.py` | test | Tests for the V4A patch format parser. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_patch_ws_diagnosis.py` | test | Tests for whitespace-visualized mismatch diagnosis in patch no-match hints. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_pr_6656_regressions.py` | test | Regression tests for PR #6656 — skill uninstall + bundle hash + pairing lock. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_pre_transcription_hook.py` | test | Tests for the ``pre_transcription`` plugin hook and STT prompt threading | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_process_registry.py` | test | Tests for tools/process_registry.py — ProcessRegistry query methods, pruning, checkpoint. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_process_registry_write_stdin_surrogates.py` | test | Sibling regression test for #79178: background-PTY stdin must round-trip | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_process_wait_clarity.py` | test | Tests for process wait timeout-result clarity (not-an-error semantics). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_react_to_message_tool.py` | test | Ownership tests for desktop message reactions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_binary_type_disclosure.py` | test | Tests for magic-byte type disclosure in the binary-file refusal. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_extract.py` | test | Tests for structured-document extraction in the read_file tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_file_utf8_binary_regression.py` | test | End-to-end regression tests for the UTF-8 'flagged as binary' class. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_loop_detection.py` | test | Tests for the read-loop detection mechanism in file_tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_past_eof_note.py` | test | Tests for the past-EOF and empty-file notes in read_file. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_preview_tool.py` | test | Tests for the GUI-surface ``read_preview`` tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_shell_line_clamp.py` | test | Shell-pipeline per-line clamp in ShellFileOperations.read_file. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_special_file_guard.py` | test | Tests for the stat-based special-file guard in read_file_tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_unicode_filename_retry.py` | test | Tests for unicode-equivalent filename retry + near-miss suggestions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_read_window_tool.py` | test | Tests for the GUI-surface ``read_window_below`` tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_refresh_agent_mcp_tools.py` | test | Tests for the shared MCP agent-tool refresh helper and discovery-wait bound. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_registry.py` | test | Tests for the central tool registry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_request_tool_approval.py` | test | Tests for tools.approval.request_tool_approval — the plugin pre_tool_call | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_resolve_path.py` | test | Tests for _resolve_path() — TERMINAL_CWD-aware path resolution in file_tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_restored_delegation_ownership.py` | test | Regression coverage for #64484 — durable-restored delegation completions | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_sandbox_failure_hints.py` | test | Tests for execute_code sandbox failure hints. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_schema_sanitizer.py` | test | Tests for tools/schema_sanitizer.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_search_auto_multiline.py` | test | Tests for search_files auto-multiline routing on \n patterns. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_search_budget_truncation.py` | test | Python module `test_search_budget_truncation.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_search_error_guard.py` | test | Regression tests for the rg/grep error guard in content search. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_search_hidden_dirs.py` | test | Tests that search_files excludes hidden directories by default. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_search_zero_match_and_multipath.py` | test | Tests for search_files zero-match probes and multi-path recovery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_self_repo_guard.py` | test | Tests for tools/self_repo_guard.py — the running-source-checkout git guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_send_message_missing_platforms.py` | test | Tests for _send_mattermost, _send_matrix, _send_homeassistant, _send_dingtalk. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_send_message_plugin_extensibility.py` | test | Cross-surface regressions for standalone platform send extensibility (#64900). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_send_message_react.py` | test | Tests for send_message action='react'/'unreact' dispatch. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_send_message_slack.py` | test | Slack-specific send_message delivery regressions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_send_message_target_parse.py` | test | Parser-only and lightweight routing tests for send_message targets. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_send_message_telegram_proxy.py` | test | Regression tests for the standalone Telegram send path's proxy support. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_send_message_tool.py` | test | Tests for tools/send_message_tool.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_session_cwd_store.py` | test | Session-cwd record store (cwd rearchitecture, step 1: dual-write). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_session_search.py` | test | Tests for the single-shape session_search tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_setup_mcp_tool.py` | test | setup_mcp tool — the desktop inline MCP consent card's tool half. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_shared_container_task_id.py` | test | Regression tests for the shared-container task_id mapping. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_shell_bypass_denylist.py` | test | Shell-obfuscation bypass coverage for the dangerous-command denylist. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_signal_media.py` | test | Tests for Signal media delivery in send_message_tool.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_single_query_approval_mode.py` | test | Tests for approvals.single_query_mode — configurable approval behavior for | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_singularity_preflight.py` | test | Tests for Singularity/Apptainer preflight availability check. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_bundle_provenance.py` | test | Multi-file third-party skill bundles and scanner provenance (#60598). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_env_passthrough.py` | test | Test that skill_view registers required env vars in the passthrough registry. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_improvements.py` | test | Tests for skill fuzzy patching via tools.fuzzy_match. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_linter.py` | test | Tests for tools/skill_linter.py — the advisory SKILL.md convention linter. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_manager_tool.py` | test | Tests for tools/skill_manager_tool.py — skill creation, editing, and deletion. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_provenance.py` | test | Tests for tools/skill_provenance.py — write-origin ContextVar. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_size_limits.py` | test | Tests for skill content size limits. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_usage.py` | test | Tests for tools/skill_usage.py — sidecar telemetry + provenance filtering. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_view_dedup.py` | test | Tests for skill_view repeat-view dedup (unchanged-skill stub). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_view_path_check.py` | test | Tests for the skill_view path boundary check. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skill_view_traversal.py` | test | Tests for path traversal prevention in skill_view. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_ast_audit.py` | test | Tests for tools.skills_ast_audit — opt-in AST diagnostic scanner. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_guard.py` | test | Tests for tools/skills_guard.py - security scanner for skills. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_hub.py` | test | Tests for tools/skills_hub.py — source adapters, lock file, taps, dedup logic. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_hub_browse_sh.py` | test | Python module `test_skills_hub_browse_sh.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_hub_clawhub.py` | test | Python module `test_skills_hub_clawhub.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_list_modified_diff.py` | test | Tests for discovering and diffing user-modified bundled skills. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_sync.py` | test | Tests for tools/skills_sync.py — manifest-based skill seeding and updating. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_sync_client.py` | test | Tests for tools/skills_sync_client.py — the Skill Sync client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_tool.py` | test | Tests for tools/skills_tool.py — skill discovery and viewing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_tool_discovery_cache.py` | test | Regression tests for the _find_all_skills discovery cache (#58985 salvage). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_skills_tool_profile_scope.py` | test | Regression tests for profile-scoped skills_tool path resolution. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_slack_send_message_media.py` | test | Slack media delivery for send_message. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_slash_confirm.py` | test | Tests for tools/slash_confirm.py — the generic slash-command confirmation primitive. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_smart_approval_injection.py` | test | Regression tests for prompt injection hardening in smart approvals. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_smart_approval_policy.py` | test | Tests for the operator-customizable smart-approval policy. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_snapshot_multiline_session_env_injection.py` | test | Newline in bridged session env must not become shell code via the snapshot. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_snapshot_session_id_leak.py` | test | Cross-session HERMES_SESSION_ID leak via the shared bash snapshot. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_spill_safety.py` | test | Symlink-refusal and permission tests for tools.spill_safety. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_spotify_client.py` | test | Python module `test_spotify_client.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_ssh_bulk_upload.py` | test | Tests for SSH bulk upload via tar pipe. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_ssh_environment.py` | test | Tests for the SSH remote execution environment backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_stage2_hook_seed_one_symlinks.py` | test | Regression tests for symlink-safe Docker stage2 first-boot seeds. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_stage2_hook_symlink_chown.py` | test | Regression tests for symlink-safe Docker stage2 ownership repair. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_startup_latency_regressions.py` | test | Startup-latency regressions: probe-mode aux clients, lazy MCP SDK, | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_stt_cloud_trim.py` | test | Tests for the cloud STT pre-upload silence trim. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_stt_default_language.py` | test | Default STT language contract. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_stt_idle_unload.py` | test | Tests for the local whisper model idle-unload mechanism. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_stt_language_resolution.py` | test | Tests for the unified STT language resolution (_resolve_stt_language). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_stt_silence_hallucinations.py` | test | Tests for the local faster-whisper silence-hallucination hardening. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_subagent_steer.py` | test | steer_subagent — redirecting a live delegated child without stopping it. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_subagent_worktree.py` | test | Tests for opt-in subagent worktree isolation (tools/subagent_worktree.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_subprocess_stdin_guard.py` | test | Verify that TUI-context subprocess calls specify stdin=. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_subprocess_utf8_encoding.py` | test | Regression test for issue #53428 — subprocess.run(text=True) without | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_symlink_prefix_confusion.py` | test | Tests for the symlink boundary check prefix confusion fix in skills_guard.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_sync_back_backends.py` | test | Tests for backend-specific bulk download implementations and cleanup() wiring. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_telegram_send_message_caption.py` | test | Standalone Telegram MEDIA:<path> caption delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_compound_background.py` | test | Regression tests for _rewrite_compound_background. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_config_env_sync.py` | test | Regression tests for terminal config -> env-var bridging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_cwd_echo.py` | test | Tests for the terminal result cwd echo (feat/terminal-cwd-echo). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_degraded_mode.py` | test | Remote terminal backend graceful degradation (terminal.degraded_mode). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_env_bridge.py` | test | Behavioral regressions for the terminal config → env bridge. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_error_redaction.py` | test | Terminal tool result errors must not leak credential-shaped strings. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_exit_semantics.py` | test | Tests for terminal command exit code semantic interpretation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_foreground_timeout_cap.py` | test | Tests for foreground timeout cap in terminal_tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_heredoc_background_guard.py` | test | Regression tests for conservative heredoc-aware background-'&' detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_hints.py` | test | Tests for tools/terminal_hints.py — output-pattern failure hints. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_none_command_guard.py` | test | Regression tests for invalid/None terminal command handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_output_transform_hook.py` | test | Python module `test_terminal_output_transform_hook.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_requirements.py` | test | Python module `test_terminal_requirements.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_self_repo_guard.py` | test | terminal_tool wiring tests for the self-repo git mutation guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_task_cwd.py` | test | Regression tests for task/session cwd propagation in terminal_tool. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_timeout_output.py` | test | Verify that terminal command timeouts preserve partial output. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_tool.py` | test | Regression tests for sudo detection and sudo password handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_tool_exception_redaction.py` | test | Terminal-tool exception paths must redact secrets before returning to the model. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_tool_pty_fallback.py` | test | Python module `test_terminal_tool_pty_fallback.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_tool_requirements.py` | test | Tests for terminal/file tool availability in local dev environments. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_terminal_truncation_spill.py` | test | Tests for terminal truncation spill + metadata (deferred retrieval). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_termux_api_detection.py` | test | Regression tests for issue #31015 — Termux:API app detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_threaded_process_handle.py` | test | Tests for _ThreadedProcessHandle — the adapter for SDK backends. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_threat_patterns.py` | test | Tests for tools/threat_patterns.py — shared threat-pattern library. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tirith_security.py` | test | Tests for the tirith security scanning subprocess wrapper. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_todo_tool.py` | test | Tests for the todo tool module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_todo_tool_type_coercion.py` | test | Tests for defensive type coercion in todo_tool (issue #14185). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tool_backend_helpers.py` | test | Unit tests for tools/tool_backend_helpers.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tool_output_limits.py` | test | Tests for tools.tool_output_limits. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tool_result_storage.py` | test | Tests for tools/tool_result_storage.py -- 3-layer tool result persistence. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tool_search.py` | test | Tests for tools/tool_search.py — progressive tool disclosure. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tool_search_context_provider.py` | test | Regression coverage for provider-aware context sizing in the tool-search gate. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_transcription.py` | test | Tests for transcription_tools.py — local (faster-whisper) and OpenAI providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_transcription_command_providers.py` | test | Tests for the STT command-provider registry (``stt.providers.<name>``). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_transcription_deepinfra.py` | test | Tests for the DeepInfra STT provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_transcription_dotenv_fallback.py` | test | Regression tests for the transcription_tools variant of #17140. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_transcription_plugin_dispatch.py` | test | Tests for STT plugin dispatch in tools/transcription_tools.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_transcription_tools.py` | test | Tests for tools.transcription_tools — three-provider STT pipeline. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_command_providers.py` | test | Tests for custom command-type TTS providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_container_repair.py` | test | Tests for the class-level TTS .ogg container repair. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_deepinfra.py` | test | Tests for the DeepInfra TTS provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_dotenv_fallback.py` | test | Regression tests for #17140. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_gemini.py` | test | Tests for the Google Gemini TTS provider in tools/tts_tool.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_instructions.py` | test | Tests for the OpenAI TTS `instructions` field passthrough. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_kittentts.py` | test | Tests for the KittenTTS local provider in tools/tts_tool.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_long_form_chunking.py` | test | Tests for the long-form TTS chunking and delivery packing pipeline. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_macos_output.py` | test | macOS output policy for streaming TTS. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_max_text_length.py` | test | Tests for per-provider TTS input-character limits. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_minimax_region.py` | test | MiniMax TTS region, endpoint, and credential selection tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_mistral.py` | test | Tests for the Mistral (Voxtral) TTS provider in tools/tts_tool.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_model_cache_lru.py` | test | LRU bound on the Piper/KittenTTS model caches. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_openai_config.py` | test | tts.openai.api_key / base_url from config.yaml drive the OpenAI audio client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_opus_routing.py` | test | Python module `test_tts_opus_routing.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_output_timestamp.py` | test | Regression test for salvaged PR #43911 — microsecond TTS output timestamps. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_path_traversal.py` | test | Regression: text_to_speech_tool output_path must reject '..' traversal. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_piper.py` | test | Tests for the native Piper TTS provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_plugin_dispatch.py` | test | Tests for TTS plugin dispatch in tools/tts_tool.py (issue #30398). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_prepare_spoken.py` | test | Unit tests for the shared TTS text cleaner (tools/tts_text_normalize). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_provider_base_urls.py` | test | Class-level base_url parity: every cloud TTS provider honors config base_url. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_pythonpath_fallback.py` | test | Regression tests for #53259. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_response_body_cap.py` | test | Regression tests for bounded upstream TTS response reads. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_speed.py` | test | Tests for TTS speed configuration across providers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_streaming.py` | test | Tests for the provider-agnostic streaming TTS backend (tools.tts_streaming) | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_streaming_e2e.py` | test | End-to-end tests for streaming TTS providers. Gated on real API keys. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_text_normalize.py` | test | Python module `test_tts_text_normalize.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_tts_xai_speech_tags.py` | test | Tests for xAI TTS speech-tag handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_url_safety.py` | test | Tests for SSRF protection in url_safety module. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_vercel_sandbox_environment.py` | test | Unit tests for the Vercel Sandbox terminal backend. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_video_analyze.py` | test | Tests for video_analyze tool in tools/vision_tools.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_video_generation_dispatch.py` | test | Tests for the unified ``video_generate`` tool dispatch surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_video_generation_dynamic_schema.py` | test | Tests for the dynamic schema builder. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_video_generation_tool_surface_matrix.py` | test | Tool-surface routing matrix: every (provider, model, modality) combo. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_vision_native_fast_path.py` | test | Tests for the native-vision fast path inside vision_analyze. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_vision_region.py` | test | Tests for the optional region crop parameter on vision_analyze. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_vision_scale_disclosure.py` | test | Downscale coordinate-scale disclosure tests. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_vision_tools.py` | test | Tests for tools/vision_tools.py — URL validation, type hints, error logging. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_voice_cli_integration.py` | test | Tests for CLI voice mode integration -- markdown stripping, voice state | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_voice_credential_pool_resolution.py` | test | Tests for ``resolve_provider_secret`` — the single owner of STT/TTS | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_voice_mode.py` | test | Tests for tools.voice_mode -- all mocked, no real microphone or API calls. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_voice_mode_playback_env_scrub.py` | test | Voice-mode system playback must scrub credential env (sibling of #70342). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_voice_stop_phrase.py` | test | Tests for the voice-chat stop phrase (say "stop" and nothing else to end). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_voice_thinking_sound.py` | test | Tests for the ambient voice-chat "thinking" sound (tools/voice_mode.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_voice_tts_echo_guard.py` | test | Tests for the playback-phase TTS-echo guard (#75780). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_voice_wsl_pipewire.py` | test | Regression: WSL voice detection must honor PIPEWIRE_REMOTE, not only PULSE_SERVER. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_wake_word.py` | test | Tests for tools.wake_word — the "Hey Hermes" hotword detector. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_watch_patterns.py` | test | Tests for watch_patterns background process monitoring feature. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_extract_robustness.py` | test | Tests for web_extract truncate-store robustness (findings from #54843 review). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_providers.py` | test | Tests for the web tools provider architecture. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_providers_brave_free.py` | test | Tests for the Brave Search (free tier) web search provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_providers_ddgs.py` | test | Tests for the DuckDuckGo (ddgs) web search provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_providers_searxng.py` | test | Tests for the SearXNG web search provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_providers_xai.py` | test | Tests for the xAI Web Search provider (plugins/web/xai/). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_tools_config.py` | test | Tests for web backend client configuration and singleton behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_tools_dict_urls.py` | test | Regression tests for model-forwarded web-search result objects. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_tools_tavily.py` | test | Tests for Tavily web backend integration. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_web_tools_truncate.py` | test | Unit tests for the truncate-and-store web_extract path (no LLM). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_website_policy.py` | test | Python module `test_website_policy.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_whatsapp_send_message_media.py` | test | WhatsApp media delivery for send_message (#19105). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_windows_agent_loop_papercuts.py` | test | Windows agent-loop correctness regressions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_windows_compat.py` | test | Tests for Windows compatibility of process management code. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_windows_native_support.py` | test | Behavioral tests for Windows-specific compatibility fixes. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_working_diff.py` | test | Tests for tools.working_diff.collect_working_diff — the git collection | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_write_approval.py` | test | Tests for the memory/skill write-approval gate (tools/write_approval.py) | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_write_deny.py` | test | Tests for _is_write_denied() — verifies deny list blocks sensitive paths on all platforms. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_write_file_syntax_gate.py` | test | Tests for the fail-closed pre-write syntax gate on write_file. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_write_verification.py` | test | Tests for write_file post-write content verification (verified flag). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_x_search_tool.py` | test | Tests for the X (Twitter) Search tool backed by xAI Responses API. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_xai_http_credentials.py` | test | Python module `test_xai_http_credentials.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_xai_http_storage.py` | test | Tests for xAI Imagine storage helper behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_yolo_mode.py` | test | Tests for --yolo (HERMES_YOLO_MODE) approval bypass. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tools/test_zombie_process_cleanup.py` | test | Tests for zombie process cleanup — verifies processes spawned by tools | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_attach_does_not_wait_for_agent.py` | test | Attach RPCs must not block on the deferred agent build. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_auto_continue.py` | test | Crash-interrupted turns auto-continue on the next session.resume. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_billing_rpc.py` | test | Tests for the Phase 2b billing JSON-RPC methods (tui_gateway/server.py). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_change_watcher.py` | test | The generalized change watcher (#73618): cheap on-disk signatures → | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_codex_app_server_live_events.py` | test | Cross-layer regression for Codex app-server tool cards in the TUI. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_cold_start_gil_stall.py` | test | Tests for cold-start GIL stall mitigations (#60800). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_compaction_status.py` | test | Auto-compaction status re-tagging for the desktop "Summarizing…" indicator. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_compress_lock_skip.py` | test | Tests for TUI gateway /compress lock-hold signalling. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_compute_host.py` | test | Python module `test_compute_host.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_compute_host_phase1.py` | test | Python module `test_compute_host_phase1.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_custom_provider_session_persistence.py` | test | Session persistence must not strip a custom provider's identity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_delegation_session_lifecycle.py` | test | Fail-closed ownership + session-scoped delegation lifecycle (#55578). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_entry_import_off_main_thread.py` | test | Regression test: importing tui_gateway.entry off the main thread must not crash. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_entry_picker_prewarm.py` | test | Regression test: the stdio TUI entry point prewarms the /model picker cache. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_entry_sys_path.py` | test | Tests for tui_gateway/entry.py sys.path hardening (issues #15989, #51286). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_ephemeral_profile_override.py` | test | Regression tests: profile HERMES_HOME override in ephemeral agent threads (#50233). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_failed_turn_retention.py` | test | Failed turns must retain a replayable ``inflight`` snapshot. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_fast_session_scope.py` | test | Fast-mode (service tier) session scoping in the TUI gateway (desktop backend). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_finalize_session_persist.py` | test | Integration test: verify _finalize_session persists messages on force-quit. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_gateway_owned_session_reap.py` | test | Tests for #60609: the TUI backend must not end gateway-owned sessions. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_goal_command.py` | test | Tests for /goal handling in tui_gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_gui_surface_toolsets.py` | test | GUI capability follows the SESSION's client, not the backend's process env. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_hud_surface_note.py` | test | HUD mode reaches the model as a per-turn note, not as a platform hint. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_image_ref_message.py` | test | Desktop image submit path must never block on vision calls (#83291). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_image_routing_stale_model.py` | test | Regression coverage for live TUI image-routing identity. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_inline_rpc_gil_starvation.py` | test | Tests for tui_gateway inline-RPC pool routing under GIL pressure (#50005). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_interim_assistant_callback.py` | test | Tests for the interim_assistant_callback config gating in tui_gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_iso_certify_seam.py` | test | Tests for the AC-4 isolation certify seam + harness helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_kanban_notify_poller.py` | test | Tests for the TUI-side kanban notification poller (issue #59890). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_loop_command.py` | test | Tests for /loop handling in tui_gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_make_agent_personality_prompt.py` | test | _make_agent resolves ephemeral prompt from display.personality. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_make_agent_provider.py` | test | Regression test for #11884: _make_agent must resolve runtime provider. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_mcp_late_refresh_thread_owner.py` | test | Regression test for issue #51587. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_mcp_profile_rpcs.py` | test | E2E tests for the per-profile MCP lifecycle RPCs (mcp.servers.*). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_mcp_reload_rev.py` | test | reload.mcp revision-aware coalescing (review on #20379, finding 1). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_moa_reference_emit.py` | test | Tests for the TUI gateway relaying MoA reference events to the client. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_model_switch_marker_role.py` | test | Tests for _append_model_switch_marker role fix (issue #48338). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_personality_clobbers_system_prompt.py` | test | Reproduction: /personality (desktop config.set) clobbers agent.system_prompt. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_pet_generate_rpc.py` | test | Gateway RPC tests for pet generation (pet.generate / pet.hatch). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_project_tree.py` | test | Invariants for the authoritative project-tree builder (tui_gateway.project_tree). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_projects_rpc.py` | test | Tests for the projects.* JSON-RPC methods on the tui_gateway server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_prompt_accept_logging.py` | test | Desktop/TUI turn-dispatch observability (#86647). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_protocol.py` | test | Tests for tui_gateway JSON-RPC protocol plumbing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_reasoning_config_per_model.py` | test | Tests for per-model reasoning_effort override in TUI gateway _load_reasoning_config. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_reasoning_session_scope.py` | test | Reasoning-effort session scoping in the TUI gateway (desktop backend). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_render.py` | test | Tests for tui_gateway.render — rendering bridge fallback behavior. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_review_summary_callback.py` | test | Tests for tui_gateway background-review summary delivery. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_session_cwd_follow.py` | test | A session that settles into another git worktree re-anchors onto it. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_session_db_ownership_teardown.py` | test | Dedicated profile ``SessionDB`` handles must be closed by whoever ends up owning them. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_session_git_metadata_generation.py` | test | Gateway wiring for generation-scoped Git metadata publication. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_session_id_injection.py` | test | Contract test: tui_gateway._set_session_context must inject the live | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_session_images_dir.py` | test | Write-side scoping for desktop/clipboard image uploads (#69575). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_session_platform_resolution.py` | test | Platform/source tagging for the desktop chat surface. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_session_reclaim_notify.py` | test | A backend-reclaimed session must tell the clients still holding it. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_session_resume_db_ownership.py` | test | ``session.resume`` must not abandon the profile-scoped SessionDB it opens. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_slash_fuzzy.py` | test | Tests for the description-aware slash fuzzy scorer (grok-cli port). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_slash_worker_ansi.py` | test | The slash worker feeds desktop chat bubbles, which render plain text — so | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_slash_worker_mcp_discovery.py` | test | Integration coverage for profile-local MCP discovery in slash workers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_slash_worker_profile_home.py` | test | Tests for TUI gateway slash_worker profile_home propagation (#40677). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_slash_worker_sys_path.py` | test | Regression tests for tui_gateway/slash_worker.py sys.path hardening (issue #51286). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_subagent_child_mirror.py` | test | Tests for the gateway's child-session live mirror. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_subprocess_encoding.py` | test | Regression tests for UTF-8 encoding hardening in tui_gateway/server.py (#53137). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_undo_command.py` | test | Tests for /undo handling in tui_gateway. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/tui_gateway/test_wait_for_mcp_discovery.py` | test | Tests for tui_gateway.entry.wait_for_mcp_discovery (PR #35245). | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/verify/test_environment_and_runner.py` | test | Tests for the verify environment manifest and the smoke runner. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/verify/test_ledger_and_nudge_integration.py` | test | Integration of the verify subsystem with the existing verification stack. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/verify/test_recipes.py` | test | Tests for agent/verify/recipes.py — static run-recipe detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/verify/test_verify_cmd.py` | test | Tests for the ``hermes verify`` CLI command implementation. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/website/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/website/test_extract_skills.py` | test | Tests for website/scripts/extract-skills.py helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `tests/website/test_generate_skill_docs.py` | test | Tests for website/scripts/generate-skill-docs.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
