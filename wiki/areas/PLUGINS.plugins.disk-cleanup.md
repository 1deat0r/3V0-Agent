# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/disk-cleanup/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/disk-cleanup/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | plugins/disk-cleanup/__init__.py; plugins/disk-cleanup/disk_cleanup.py; plugins/disk-cleanup/plugin.yaml |
| `plugins/disk-cleanup/__init__.py` | source | disk-cleanup plugin — auto-cleanup of ephemeral Hermes session files. | Python module executed or imported by the runtime; check git intent before deleting | plugins/disk-cleanup/README.md; plugins/disk-cleanup/disk_cleanup.py; plugins/disk-cleanup/plugin.yaml |
| `plugins/disk-cleanup/disk_cleanup.py` | source | disk_cleanup — ephemeral file cleanup for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting | plugins/disk-cleanup/README.md; plugins/disk-cleanup/__init__.py; plugins/disk-cleanup/plugin.yaml |
| `plugins/disk-cleanup/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/disk-cleanup/README.md; plugins/disk-cleanup/__init__.py; plugins/disk-cleanup/disk_cleanup.py |
