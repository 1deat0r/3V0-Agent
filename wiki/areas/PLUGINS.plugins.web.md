# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/web/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/web/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/brave_free/__init__.py; plugins/web/brave_free/plugin.yaml; plugins/web/brave_free/provider.py; plugins/web/ddgs/__init__.py; plugins/web/ddgs/_search_worker.py |
| `plugins/web/brave_free/__init__.py` | source | Brave Search (free tier) plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/brave_free/plugin.yaml; plugins/web/brave_free/provider.py |
| `plugins/web/brave_free/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/web/brave_free/__init__.py; plugins/web/brave_free/provider.py |
| `plugins/web/brave_free/provider.py` | source | Brave Search (free tier) — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/brave_free/__init__.py; plugins/web/brave_free/plugin.yaml |
| `plugins/web/ddgs/__init__.py` | source | DuckDuckGo search plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/ddgs/_search_worker.py; plugins/web/ddgs/plugin.yaml; plugins/web/ddgs/provider.py |
| `plugins/web/ddgs/_search_worker.py` | source | DDGS search child-process entrypoint (#68096). | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/ddgs/__init__.py; plugins/web/ddgs/plugin.yaml; plugins/web/ddgs/provider.py |
| `plugins/web/ddgs/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/web/ddgs/__init__.py; plugins/web/ddgs/_search_worker.py; plugins/web/ddgs/provider.py |
| `plugins/web/ddgs/provider.py` | source | DuckDuckGo search — plugin form (via the ``ddgs`` package). | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/ddgs/__init__.py; plugins/web/ddgs/_search_worker.py; plugins/web/ddgs/plugin.yaml |
| `plugins/web/exa/__init__.py` | source | Exa web search + extract plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/exa/plugin.yaml; plugins/web/exa/provider.py |
| `plugins/web/exa/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/web/exa/__init__.py; plugins/web/exa/provider.py |
| `plugins/web/exa/provider.py` | source | Exa web search + content extraction — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/exa/__init__.py; plugins/web/exa/plugin.yaml |
| `plugins/web/firecrawl/__init__.py` | source | Firecrawl web search + extract plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/firecrawl/plugin.yaml; plugins/web/firecrawl/provider.py |
| `plugins/web/firecrawl/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/web/firecrawl/__init__.py; plugins/web/firecrawl/provider.py |
| `plugins/web/firecrawl/provider.py` | source | Firecrawl web search + extract — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/firecrawl/__init__.py; plugins/web/firecrawl/plugin.yaml |
| `plugins/web/parallel/__init__.py` | source | Parallel.ai web search + extract plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/parallel/plugin.yaml; plugins/web/parallel/provider.py |
| `plugins/web/parallel/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/web/parallel/__init__.py; plugins/web/parallel/provider.py |
| `plugins/web/parallel/provider.py` | source | Parallel.ai web search + content extraction — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/parallel/__init__.py; plugins/web/parallel/plugin.yaml |
| `plugins/web/searxng/__init__.py` | source | SearXNG search plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/searxng/plugin.yaml; plugins/web/searxng/provider.py |
| `plugins/web/searxng/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/web/searxng/__init__.py; plugins/web/searxng/provider.py |
| `plugins/web/searxng/provider.py` | source | SearXNG search — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/searxng/__init__.py; plugins/web/searxng/plugin.yaml |
| `plugins/web/tavily/__init__.py` | source | Tavily web search + extract plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/tavily/plugin.yaml; plugins/web/tavily/provider.py |
| `plugins/web/tavily/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/web/tavily/__init__.py; plugins/web/tavily/provider.py |
| `plugins/web/tavily/provider.py` | source | Tavily web search + content extraction — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/tavily/__init__.py; plugins/web/tavily/plugin.yaml |
| `plugins/web/xai/__init__.py` | source | xAI web search plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/xai/plugin.yaml; plugins/web/xai/provider.py |
| `plugins/web/xai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/web/xai/__init__.py; plugins/web/xai/provider.py |
| `plugins/web/xai/provider.py` | source | xAI Web Search — plugin form. | Python module executed or imported by the runtime; check git intent before deleting | plugins/web/xai/__init__.py; plugins/web/xai/plugin.yaml |
