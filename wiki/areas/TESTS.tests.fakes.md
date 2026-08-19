# tests/ + tests-js/ + evals/ — the test suites — `tests/fakes/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/fakes/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/fakes/fake_ha_server.py |
| `tests/fakes/fake_ha_server.py` | test | Fake Home Assistant server for integration testing. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/fakes/__init__.py |
