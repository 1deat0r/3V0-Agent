# tests/ + tests-js/ + evals/ — the test suites — `tests/acp_adapter/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/acp_adapter/test_acp_commands.py` | test | Tests `acp_adapter/test_acp_commands.py` — see related for the module under test | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/acp_adapter/test_acp_images.py; tests/acp_adapter/test_acp_logging_redaction.py; tests/acp_adapter/test_acp_mcp_discovery.py; tests/acp_adapter/test_detect_provider_entra.py |
| `tests/acp_adapter/test_acp_images.py` | test | Tests `acp_adapter/test_acp_images.py` — see related for the module under test | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/acp_adapter/test_acp_commands.py; tests/acp_adapter/test_acp_logging_redaction.py; tests/acp_adapter/test_acp_mcp_discovery.py; tests/acp_adapter/test_detect_provider_entra.py |
| `tests/acp_adapter/test_acp_logging_redaction.py` | test | ACP adapter stderr logging must go through RedactingFormatter. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/acp_adapter/test_acp_commands.py; tests/acp_adapter/test_acp_images.py; tests/acp_adapter/test_acp_mcp_discovery.py; tests/acp_adapter/test_detect_provider_entra.py |
| `tests/acp_adapter/test_acp_mcp_discovery.py` | test | Behavioral regression tests for ACP background MCP discovery + late-refresh. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/acp_adapter/test_acp_commands.py; tests/acp_adapter/test_acp_images.py; tests/acp_adapter/test_acp_logging_redaction.py; tests/acp_adapter/test_detect_provider_entra.py |
| `tests/acp_adapter/test_detect_provider_entra.py` | test | Regression tests for ACP adapter detection under Azure Foundry Entra ID. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/acp_adapter/test_acp_commands.py; tests/acp_adapter/test_acp_images.py; tests/acp_adapter/test_acp_logging_redaction.py; tests/acp_adapter/test_acp_mcp_discovery.py |
