# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/browser/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/browser/browser_use/__init__.py` | source | Browser Use cloud browser plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/browser/browser_use/plugin.yaml; plugins/browser/browser_use/provider.py |
| `plugins/browser/browser_use/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/browser/browser_use/__init__.py; plugins/browser/browser_use/provider.py |
| `plugins/browser/browser_use/provider.py` | source | Browser Use cloud browser provider — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/browser/browser_use/__init__.py; plugins/browser/browser_use/plugin.yaml |
| `plugins/browser/browserbase/__init__.py` | source | Browserbase cloud browser plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/browser/browserbase/plugin.yaml; plugins/browser/browserbase/provider.py |
| `plugins/browser/browserbase/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/browser/browserbase/__init__.py; plugins/browser/browserbase/provider.py |
| `plugins/browser/browserbase/provider.py` | source | Browserbase cloud browser provider — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/browser/browserbase/__init__.py; plugins/browser/browserbase/plugin.yaml |
| `plugins/browser/firecrawl/__init__.py` | source | Firecrawl cloud browser plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/browser/firecrawl/plugin.yaml; plugins/browser/firecrawl/provider.py |
| `plugins/browser/firecrawl/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/browser/firecrawl/__init__.py; plugins/browser/firecrawl/provider.py |
| `plugins/browser/firecrawl/provider.py` | source | Firecrawl cloud browser provider — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/browser/firecrawl/__init__.py; plugins/browser/firecrawl/plugin.yaml |
