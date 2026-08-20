# tests/ + 3v0/tests/ — the Python test suites (tests-js/ and evals/ pruned) — `tests/e2e/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/e2e/__init__.py` | test | Tests `e2e/__init__.py` — see related for the module under test | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/e2e/conftest.py; tests/e2e/matrix_xsign_bootstrap/README.md; tests/e2e/matrix_xsign_bootstrap/docker-compose.yml; tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py |
| `tests/e2e/conftest.py` | test | Shared fixtures for gateway e2e tests (Telegram, Discord). | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/e2e/__init__.py; tests/e2e/matrix_xsign_bootstrap/README.md; tests/e2e/matrix_xsign_bootstrap/docker-compose.yml; tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py |
| `tests/e2e/matrix_xsign_bootstrap/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | tests/e2e/matrix_xsign_bootstrap/docker-compose.yml; tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py |
| `tests/e2e/matrix_xsign_bootstrap/docker-compose.yml` | build | Docker Compose definition | Local multi-container orchestration (dev/CI matrix) | tests/e2e/matrix_xsign_bootstrap/README.md; tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py |
| `tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py` | test | End-to-end test for Matrix cross-signing auto-bootstrap. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/e2e/matrix_xsign_bootstrap/README.md; tests/e2e/matrix_xsign_bootstrap/docker-compose.yml |
| `tests/e2e/test_discord_adapter.py` | test | Minimal e2e tests for Discord mention stripping + /command detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/e2e/__init__.py; tests/e2e/conftest.py; tests/e2e/matrix_xsign_bootstrap/README.md; tests/e2e/matrix_xsign_bootstrap/docker-compose.yml; tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py |
| `tests/e2e/test_platform_commands.py` | test | E2E tests for gateway slash commands (Telegram, Discord). | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/e2e/__init__.py; tests/e2e/conftest.py; tests/e2e/matrix_xsign_bootstrap/README.md; tests/e2e/matrix_xsign_bootstrap/docker-compose.yml; tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py |
| `tests/e2e/test_relay_native_anthropic_stream.py` | test | Native Anthropic SDK streaming through Relay's managed execution path. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/e2e/__init__.py; tests/e2e/conftest.py; tests/e2e/matrix_xsign_bootstrap/README.md; tests/e2e/matrix_xsign_bootstrap/docker-compose.yml; tests/e2e/matrix_xsign_bootstrap/test_bootstrap.py |
