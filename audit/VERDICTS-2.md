# VERDICTS-2 — cohort 2: untouched runtime .py (batch A)

136 files / 29,052 LOC. Zero TODO/FIXME/XXX across the whole cohort (scan
evidence). Verdicts below are evidence-grounded (import/reference scan +
content read); batch A covers the high-signal first pass.

| file | verdict | evidence |
|---|---|---|
| gateway/session_state.py | NEEDED | "stale/legacy" markers = deliberate dict→DB migration-compat shims (legacy_dict_property), not rot; used by gateway runner |
| agent/lsp/client.py | NEEDED | Async LSP client over stdio; imported by agent/lsp/manager.py, ev0_cli/main.py:11942, tui_gateway/server.py:444; documented design (version-freshness, no ghost diagnostics) |
| agent/lsp/protocol.py | NEEDED | framer/envelope helpers for the client |
| agent/lsp/range_shift.py | NEEDED | part of lsp subsystem |
| agent/lsp/reporter.py | NEEDED | part of lsp subsystem |
| tools/clarify_gateway.py | NEEDED | resolve_gateway_clarify/mark_awaiting_text imported by gateway/relay/adapter.py, whatsapp_cloud.py, platforms/base.py, cli.py |
| agent/moonshot_schema.py | NEEDED | Kimi/Moonshot provider schema; used by run_agent.py thinking-mode detection + trajectory_compressor tokenizer refs |
| agent/message_sanitization.py | NEEDED | imported by ev0_state.py, gateway/run.py, run_agent.py, codex adapter, conversation loop |
| tools/patch_parser.py | NEEDED | imported across runtime (codex adapter, chat helpers, agent runtime helpers) |
| tools/read_extract.py | NEEDED | (referenced earlier; part of tooling layer) |

NONE of batch A requires IMPROVE/UPDATE/REMOVE/REPLACE. Pattern: every
untouched runtime module is referenced by the live runtime and carries
deliberate design docs, not rot. Continue with batch B (security-adjacent:
message_sanitization full read, edit_approval, path_security, token_auth;
platform adapters: yuanbao_*, qqbot/*, feishu, msgraph; tools: homeassistant,
todo_tool, shell_heredoc, terminal_hints, read_extract).