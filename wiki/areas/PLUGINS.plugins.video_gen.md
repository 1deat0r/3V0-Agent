# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/video_gen/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/video_gen/deepinfra/__init__.py` | source | DeepInfra video generation backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/video_gen/deepinfra/plugin.yaml |
| `plugins/video_gen/deepinfra/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/video_gen/deepinfra/__init__.py |
| `plugins/video_gen/fal/__init__.py` | source | FAL.ai video generation backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/video_gen/fal/plugin.yaml |
| `plugins/video_gen/fal/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/video_gen/fal/__init__.py |
| `plugins/video_gen/xai/__init__.py` | source | xAI Grok-Imagine video generation backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/video_gen/xai/plugin.yaml |
| `plugins/video_gen/xai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/video_gen/xai/__init__.py |
