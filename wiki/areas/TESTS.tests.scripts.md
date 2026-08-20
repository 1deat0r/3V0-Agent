# tests/ + 3v0/tests/ — the Python test suites (tests-js/ and evals/ pruned) — `tests/scripts/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/scripts/test_build_skills_index_health.py` | test | Invariants for scripts/build_skills_index.py's health-check guard. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/scripts/test_contributor_map.py; tests/scripts/test_footgun_subprocess_encoding.py; tests/scripts/test_smoke_nemo_relay_shared_metrics.py; tests/scripts/test_windows_footguns_full_repo_scan.py |
| `tests/scripts/test_contributor_map.py` | test | Tests for the conflict-free contributor mapping system. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/scripts/test_build_skills_index_health.py; tests/scripts/test_footgun_subprocess_encoding.py; tests/scripts/test_smoke_nemo_relay_shared_metrics.py |
| `tests/scripts/test_footgun_subprocess_encoding.py` | test | Tests for the ``subprocess text=True without explicit encoding=`` footgun | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/scripts/test_build_skills_index_health.py; tests/scripts/test_contributor_map.py; tests/scripts/test_smoke_nemo_relay_shared_metrics.py; tests/scripts/test_windows_footguns_full_repo_scan.py |
| `tests/scripts/test_smoke_nemo_relay_shared_metrics.py` | test | Tests for the shared-metrics smoke artifact. | Test module — asserts the repo contract; run via scripts/run_tests.sh | scripts/smoke_nemo_relay_shared_metrics.py; tests/scripts/test_build_skills_index_health.py; tests/scripts/test_contributor_map.py; tests/scripts/test_footgun_subprocess_encoding.py |
| `tests/scripts/test_windows_footguns_full_repo_scan.py` | test | Full-repo self-scan wrapper for scripts/check-windows-footguns.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/scripts/test_build_skills_index_health.py; tests/scripts/test_contributor_map.py; tests/scripts/test_footgun_subprocess_encoding.py; tests/scripts/test_smoke_nemo_relay_shared_metrics.py |
