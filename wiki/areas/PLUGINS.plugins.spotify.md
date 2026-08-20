# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/spotify/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/spotify/__init__.py` | source | Spotify integration plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/spotify/client.py; plugins/spotify/plugin.yaml; plugins/spotify/tools.py |
| `plugins/spotify/client.py` | source | Thin Spotify Web API helper used by 3V0 native tools. | Python module executed or imported by the runtime; check git intent before deleting | plugins/spotify/__init__.py; plugins/spotify/plugin.yaml; plugins/spotify/tools.py |
| `plugins/spotify/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/spotify/__init__.py; plugins/spotify/client.py; plugins/spotify/tools.py |
| `plugins/spotify/tools.py` | source | Native Spotify tools for 3V0 (registered via plugins/spotify). | Python module executed or imported by the runtime; check git intent before deleting | plugins/spotify/__init__.py; plugins/spotify/client.py; plugins/spotify/plugin.yaml |
