# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins//`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/__init__.py` | source | Plugin package marker | Discovery root | threev0_cli/plugins.py |
| `plugins/_provider_loader.py` | source | Generic provider-plugin discovery loader (architecture-review pass 3, C1). | Python module executed or imported by the runtime; check git intent before deleting | plugins/3v0-achievements/LICENSE; plugins/3v0-achievements/README.md; plugins/3v0-achievements/dashboard/dist/index.js; plugins/3v0-achievements/dashboard/dist/style.css |
| `plugins/plugin_utils.py` | source | Shared concurrency helpers for plugin authors. | Python module executed or imported by the runtime; check git intent before deleting | plugins/3v0-achievements/LICENSE; plugins/3v0-achievements/README.md; plugins/3v0-achievements/dashboard/dist/index.js; plugins/3v0-achievements/dashboard/dist/style.css |
