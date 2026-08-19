# tests/ + tests-js/ + evals/ — the test suites — `tests/monitoring/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/monitoring/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/monitoring/test_cron_health_export.py; tests/monitoring/test_emitter.py; tests/monitoring/test_export_redaction.py; tests/monitoring/test_gateway_health_export.py |
| `tests/monitoring/test_cron_health_export.py` | test | Python module `test_cron_health_export.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/monitoring/__init__.py; tests/monitoring/test_emitter.py; tests/monitoring/test_export_redaction.py; tests/monitoring/test_gateway_health_export.py; tests/monitoring/test_otlp_exporter.py |
| `tests/monitoring/test_emitter.py` | test | Tests for the monitoring emitter: hot-path invariant + subscriber fan-out. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/monitoring/__init__.py; tests/monitoring/test_cron_health_export.py; tests/monitoring/test_export_redaction.py; tests/monitoring/test_gateway_health_export.py |
| `tests/monitoring/test_export_redaction.py` | test | Export redaction tests — the security-critical layer. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/monitoring/__init__.py; tests/monitoring/test_cron_health_export.py; tests/monitoring/test_emitter.py; tests/monitoring/test_gateway_health_export.py; tests/monitoring/test_otlp_exporter.py |
| `tests/monitoring/test_gateway_health_export.py` | test | Python module `test_gateway_health_export.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/monitoring/__init__.py; tests/monitoring/test_cron_health_export.py; tests/monitoring/test_emitter.py; tests/monitoring/test_export_redaction.py; tests/monitoring/test_otlp_exporter.py |
| `tests/monitoring/test_otlp_exporter.py` | test | OTLP exporter tests: config resolution, span mapping, streaming subscriber. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/monitoring/__init__.py; tests/monitoring/test_cron_health_export.py; tests/monitoring/test_emitter.py; tests/monitoring/test_export_redaction.py; tests/monitoring/test_gateway_health_export.py |
