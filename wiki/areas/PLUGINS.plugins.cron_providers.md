# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/cron_providers/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/cron_providers/__init__.py` | source | Cron scheduler provider plugin discovery. | Python module executed or imported by the runtime; check git intent before deleting | plugins/cron_providers/chronos/__init__.py; plugins/cron_providers/chronos/_nas_client.py; plugins/cron_providers/chronos/plugin.yaml; plugins/cron_providers/chronos/verify.py |
| `plugins/cron_providers/chronos/__init__.py` | source | Chronos — NAS-mediated managed cron provider (scale-to-zero). | Python module executed or imported by the runtime; check git intent before deleting | plugins/cron_providers/chronos/_nas_client.py; plugins/cron_providers/chronos/plugin.yaml; plugins/cron_providers/chronos/verify.py |
| `plugins/cron_providers/chronos/_nas_client.py` | source | Thin HTTP client for the agent → NAS ``agent-cron`` endpoints (Chronos). | Python module executed or imported by the runtime; check git intent before deleting | plugins/cron_providers/chronos/__init__.py; plugins/cron_providers/chronos/plugin.yaml; plugins/cron_providers/chronos/verify.py |
| `plugins/cron_providers/chronos/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/cron_providers/chronos/__init__.py; plugins/cron_providers/chronos/_nas_client.py; plugins/cron_providers/chronos/verify.py |
| `plugins/cron_providers/chronos/verify.py` | source | Inbound cron-fire token verification for Chronos (Phase 4E.1). | Python module executed or imported by the runtime; check git intent before deleting | plugins/cron_providers/chronos/__init__.py; plugins/cron_providers/chronos/_nas_client.py; plugins/cron_providers/chronos/plugin.yaml |
