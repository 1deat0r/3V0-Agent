# tests/ + 3v0/tests/ — the Python test suites (tests-js/ and evals/ pruned) — `tests/conformance/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/conformance/__init__.py` | test | Tests `conformance/__init__.py` — see related for the module under test | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/conformance/test_vector_generator.py; tests/conformance/vectors/discord.json; tests/conformance/vectors/slack.json; tests/conformance/vectors/telegram.json |
| `tests/conformance/test_vector_generator.py` | test | Conformance vector generator tests (Phase 5 oracle workstream). | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/conformance/__init__.py; tests/conformance/vectors/discord.json; tests/conformance/vectors/slack.json; tests/conformance/vectors/telegram.json; tests/conformance/vectors/whatsapp.json |
| `tests/conformance/vectors/discord.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | tests/conformance/vectors/slack.json; tests/conformance/vectors/telegram.json; tests/conformance/vectors/whatsapp.json |
| `tests/conformance/vectors/slack.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | tests/conformance/vectors/discord.json; tests/conformance/vectors/telegram.json; tests/conformance/vectors/whatsapp.json |
| `tests/conformance/vectors/telegram.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | tests/conformance/vectors/discord.json; tests/conformance/vectors/slack.json; tests/conformance/vectors/whatsapp.json |
| `tests/conformance/vectors/whatsapp.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | tests/conformance/vectors/discord.json; tests/conformance/vectors/slack.json; tests/conformance/vectors/telegram.json |
