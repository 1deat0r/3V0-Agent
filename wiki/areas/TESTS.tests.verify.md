# tests/ + 3v0/tests/ — the Python test suites (tests-js/ and evals/ pruned) — `tests/verify/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/verify/test_environment_and_runner.py` | test | Tests for the verify environment manifest and the smoke runner. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/verify/test_ledger_and_nudge_integration.py; tests/verify/test_recipes.py; tests/verify/test_verify_cmd.py |
| `tests/verify/test_ledger_and_nudge_integration.py` | test | Integration of the verify subsystem with the existing verification stack. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/verify/test_environment_and_runner.py; tests/verify/test_recipes.py; tests/verify/test_verify_cmd.py |
| `tests/verify/test_recipes.py` | test | Tests for agent/verify/recipes.py — static run-recipe detection. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/verify/test_environment_and_runner.py; tests/verify/test_ledger_and_nudge_integration.py; tests/verify/test_verify_cmd.py |
| `tests/verify/test_verify_cmd.py` | test | Tests for the ``3v0 verify`` CLI command implementation. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/verify/test_environment_and_runner.py; tests/verify/test_ledger_and_nudge_integration.py; tests/verify/test_recipes.py |
