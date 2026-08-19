# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/image_gen/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/image_gen/deepinfra/__init__.py` | source | DeepInfra image generation backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/image_gen/deepinfra/plugin.yaml |
| `plugins/image_gen/deepinfra/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/image_gen/deepinfra/__init__.py |
| `plugins/image_gen/fal/__init__.py` | source | FAL.ai image generation backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/image_gen/fal/plugin.yaml |
| `plugins/image_gen/fal/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/image_gen/fal/__init__.py |
| `plugins/image_gen/krea/__init__.py` | source | Krea image generation backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/image_gen/krea/plugin.yaml |
| `plugins/image_gen/krea/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/image_gen/krea/__init__.py |
| `plugins/image_gen/openai-codex/__init__.py` | source | OpenAI image generation backend — ChatGPT/Codex OAuth variant. | Python module executed or imported by the runtime; check git intent before deleting | plugins/image_gen/openai-codex/plugin.yaml |
| `plugins/image_gen/openai-codex/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/image_gen/openai-codex/__init__.py |
| `plugins/image_gen/openai/__init__.py` | source | OpenAI image generation backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/image_gen/openai/plugin.yaml |
| `plugins/image_gen/openai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/image_gen/openai/__init__.py |
| `plugins/image_gen/openrouter/__init__.py` | source | OpenRouter-compatible image generation backend (OpenRouter + Nous Portal). | Python module executed or imported by the runtime; check git intent before deleting | plugins/image_gen/openrouter/plugin.yaml |
| `plugins/image_gen/openrouter/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/image_gen/openrouter/__init__.py |
| `plugins/image_gen/xai/__init__.py` | source | xAI image generation backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/image_gen/xai/plugin.yaml |
| `plugins/image_gen/xai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/image_gen/xai/__init__.py |
