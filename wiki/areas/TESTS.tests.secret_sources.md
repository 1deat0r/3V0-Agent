# tests/ + tests-js/ + evals/ — the test suites — `tests/secret_sources/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/secret_sources/__init__.py` | test | Tests `secret_sources/__init__.py` — see related for the module under test | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/secret_sources/conformance.py; tests/secret_sources/test_error_remediation.py; tests/secret_sources/test_profile_secrets.py; tests/secret_sources/test_secret_source_registry.py |
| `tests/secret_sources/conformance.py` | test | Conformance kit for :class:`agent.secret_sources.base.SecretSource`. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/secret_sources/__init__.py; tests/secret_sources/test_error_remediation.py; tests/secret_sources/test_profile_secrets.py; tests/secret_sources/test_secret_source_registry.py |
| `tests/secret_sources/test_error_remediation.py` | test | Error remediation for secret sources. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/secret_sources/__init__.py; tests/secret_sources/conformance.py; tests/secret_sources/test_profile_secrets.py; tests/secret_sources/test_secret_source_registry.py |
| `tests/secret_sources/test_profile_secrets.py` | test | Orchestrator-level profile secret handling. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/secret_sources/__init__.py; tests/secret_sources/conformance.py; tests/secret_sources/test_error_remediation.py; tests/secret_sources/test_secret_source_registry.py |
| `tests/secret_sources/test_secret_source_registry.py` | test | Tests for the secret-source contract + orchestrator. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/secret_sources/__init__.py; tests/secret_sources/conformance.py; tests/secret_sources/test_error_remediation.py; tests/secret_sources/test_profile_secrets.py |
