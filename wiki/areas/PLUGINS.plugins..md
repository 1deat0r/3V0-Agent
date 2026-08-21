# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins//`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/__init__.py` | source | Plugin package marker | Discovery root | threev0_cli/plugins.py |
| `plugins/plugin_utils.py` | source | Shared concurrency helpers for plugin authors. | Python module executed or imported by the runtime; check git intent before deleting | plugins/__init__.py; plugins/browser/browser_use/__init__.py; plugins/browser/browser_use/plugin.yaml; plugins/browser/browser_use/provider.py; plugins/browser/browserbase/__init__.py |
