# tests/ + 3v0/tests/ — the Python test suites (tests-js/ and evals/ pruned) — `tests/manual/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/manual/cron_inchannel_dm_e2e.py` | test | DM-path verification for in_channel continuable cron (Option A scoping). | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/manual/cron_inchannel_e2e.py |
| `tests/manual/cron_inchannel_e2e.py` | test | Offline E2E for continuable in-channel cron (specs/cron-inchannel-continuable). | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/manual/cron_inchannel_dm_e2e.py |
