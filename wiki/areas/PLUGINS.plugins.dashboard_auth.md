# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/dashboard_auth/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/dashboard_auth/basic/__init__.py` | source | BasicAuthProvider — username/password dashboard auth (no OAuth IDP). | Python module executed or imported by the runtime; check git intent before deleting | plugins/dashboard_auth/basic/plugin.yaml |
| `plugins/dashboard_auth/basic/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/dashboard_auth/basic/__init__.py |
| `plugins/dashboard_auth/drain/__init__.py` | source | DrainSecretProvider — shared-bearer-secret auth for the drain-control endpoint. | Python module executed or imported by the runtime; check git intent before deleting | plugins/dashboard_auth/drain/plugin.yaml |
| `plugins/dashboard_auth/drain/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/dashboard_auth/drain/__init__.py |
| `plugins/dashboard_auth/nous/__init__.py` | source | NousDashboardAuthProvider — Nous Portal OAuth (authorization-code + PKCE). | Python module executed or imported by the runtime; check git intent before deleting | plugins/dashboard_auth/nous/plugin.yaml |
| `plugins/dashboard_auth/nous/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/dashboard_auth/nous/__init__.py |
| `plugins/dashboard_auth/self_hosted/__init__.py` | source | SelfHostedOIDCProvider — generic self-hosted OpenID Connect dashboard auth. | Python module executed or imported by the runtime; check git intent before deleting | plugins/dashboard_auth/self_hosted/plugin.yaml |
| `plugins/dashboard_auth/self_hosted/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/dashboard_auth/self_hosted/__init__.py |
