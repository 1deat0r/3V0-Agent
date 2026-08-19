# tests/ + tests-js/ + evals/ — the test suites — `tests/fixtures/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/fixtures/cua_driver_0_9_tools_list.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | tests/fixtures/plugins/example-dashboard/dashboard/manifest.json; tests/fixtures/plugins/example-dashboard/dashboard/plugin_api.py; tests/fixtures/session-resume-active-turn.json |
| `tests/fixtures/plugins/example-dashboard/dashboard/manifest.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | tests/fixtures/plugins/example-dashboard/dashboard/plugin_api.py |
| `tests/fixtures/plugins/example-dashboard/dashboard/plugin_api.py` | test | Example dashboard plugin — backend API routes (test fixture). | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/fixtures/plugins/example-dashboard/dashboard/manifest.json |
| `tests/fixtures/session-resume-active-turn.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | tests/fixtures/cua_driver_0_9_tools_list.json; tests/fixtures/plugins/example-dashboard/dashboard/manifest.json; tests/fixtures/plugins/example-dashboard/dashboard/plugin_api.py |
