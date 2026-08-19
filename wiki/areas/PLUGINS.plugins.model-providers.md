# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/model-providers/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/model-providers/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | plugins/model-providers/actual/__init__.py; plugins/model-providers/actual/plugin.yaml; plugins/model-providers/ai-gateway/__init__.py; plugins/model-providers/ai-gateway/plugin.yaml |
| `plugins/model-providers/actual/__init__.py` | source | Actual Computer provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/actual/plugin.yaml |
| `plugins/model-providers/actual/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/actual/__init__.py |
| `plugins/model-providers/ai-gateway/__init__.py` | source | Vercel AI Gateway provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/ai-gateway/plugin.yaml |
| `plugins/model-providers/ai-gateway/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/ai-gateway/__init__.py |
| `plugins/model-providers/alibaba-coding-plan/__init__.py` | source | Alibaba Cloud Coding Plan provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/alibaba-coding-plan/plugin.yaml |
| `plugins/model-providers/alibaba-coding-plan/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/alibaba-coding-plan/__init__.py |
| `plugins/model-providers/alibaba/__init__.py` | source | Alibaba Cloud DashScope provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/alibaba/plugin.yaml |
| `plugins/model-providers/alibaba/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/alibaba/__init__.py |
| `plugins/model-providers/anthropic/__init__.py` | source | Native Anthropic provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/anthropic/plugin.yaml |
| `plugins/model-providers/anthropic/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/anthropic/__init__.py |
| `plugins/model-providers/arcee/__init__.py` | source | Arcee AI provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/arcee/plugin.yaml |
| `plugins/model-providers/arcee/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/arcee/__init__.py |
| `plugins/model-providers/azure-foundry/__init__.py` | source | Microsoft Foundry provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/azure-foundry/plugin.yaml |
| `plugins/model-providers/azure-foundry/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/azure-foundry/__init__.py |
| `plugins/model-providers/bedrock/__init__.py` | source | AWS Bedrock provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/bedrock/plugin.yaml |
| `plugins/model-providers/bedrock/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/bedrock/__init__.py |
| `plugins/model-providers/copilot-acp/__init__.py` | source | GitHub Copilot ACP provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/copilot-acp/plugin.yaml |
| `plugins/model-providers/copilot-acp/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/copilot-acp/__init__.py |
| `plugins/model-providers/copilot/__init__.py` | source | Copilot / GitHub Models provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/copilot/plugin.yaml |
| `plugins/model-providers/copilot/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/copilot/__init__.py |
| `plugins/model-providers/custom/__init__.py` | source | Custom / Ollama (local) provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/custom/plugin.yaml |
| `plugins/model-providers/custom/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/custom/__init__.py |
| `plugins/model-providers/deepinfra/__init__.py` | source | DeepInfra provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/deepinfra/plugin.yaml |
| `plugins/model-providers/deepinfra/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/deepinfra/__init__.py |
| `plugins/model-providers/deepseek/__init__.py` | source | DeepSeek provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/deepseek/plugin.yaml |
| `plugins/model-providers/deepseek/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/deepseek/__init__.py |
| `plugins/model-providers/fireworks/__init__.py` | source | Fireworks AI provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/fireworks/plugin.yaml |
| `plugins/model-providers/fireworks/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/fireworks/__init__.py |
| `plugins/model-providers/gemini/__init__.py` | source | Google Gemini provider profiles. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/gemini/plugin.yaml |
| `plugins/model-providers/gemini/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/gemini/__init__.py |
| `plugins/model-providers/gmi/__init__.py` | source | GMI Cloud provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/gmi/plugin.yaml |
| `plugins/model-providers/gmi/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/gmi/__init__.py |
| `plugins/model-providers/huggingface/__init__.py` | source | Hugging Face provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/huggingface/plugin.yaml |
| `plugins/model-providers/huggingface/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/huggingface/__init__.py |
| `plugins/model-providers/kilocode/__init__.py` | source | Kilo Code provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/kilocode/plugin.yaml |
| `plugins/model-providers/kilocode/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/kilocode/__init__.py |
| `plugins/model-providers/kimi-coding/__init__.py` | source | Kimi / Moonshot provider profiles. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/kimi-coding/plugin.yaml |
| `plugins/model-providers/kimi-coding/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/kimi-coding/__init__.py |
| `plugins/model-providers/minimax/__init__.py` | source | MiniMax provider profiles (international + China). | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/minimax/plugin.yaml |
| `plugins/model-providers/minimax/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/minimax/__init__.py |
| `plugins/model-providers/nous/__init__.py` | source | Nous Portal provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/nous/plugin.yaml |
| `plugins/model-providers/nous/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/nous/__init__.py |
| `plugins/model-providers/novita/__init__.py` | source | NovitaAI provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/novita/plugin.yaml |
| `plugins/model-providers/novita/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/novita/__init__.py |
| `plugins/model-providers/nvidia/__init__.py` | source | NVIDIA NIM provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/nvidia/plugin.yaml |
| `plugins/model-providers/nvidia/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/nvidia/__init__.py |
| `plugins/model-providers/ollama-cloud/__init__.py` | source | Ollama Cloud provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/ollama-cloud/plugin.yaml |
| `plugins/model-providers/ollama-cloud/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/ollama-cloud/__init__.py |
| `plugins/model-providers/openai-codex/__init__.py` | source | OpenAI Codex (Responses API) provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/openai-codex/plugin.yaml |
| `plugins/model-providers/openai-codex/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/openai-codex/__init__.py |
| `plugins/model-providers/opencode-zen/__init__.py` | source | OpenCode provider profiles (Zen + Go). | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/opencode-zen/plugin.yaml |
| `plugins/model-providers/opencode-zen/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/opencode-zen/__init__.py |
| `plugins/model-providers/openrouter/__init__.py` | source | OpenRouter provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/openrouter/plugin.yaml |
| `plugins/model-providers/openrouter/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/openrouter/__init__.py |
| `plugins/model-providers/qwen-oauth/__init__.py` | source | Qwen Portal provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/qwen-oauth/plugin.yaml |
| `plugins/model-providers/qwen-oauth/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/qwen-oauth/__init__.py |
| `plugins/model-providers/stepfun/__init__.py` | source | StepFun provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/stepfun/plugin.yaml |
| `plugins/model-providers/stepfun/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/stepfun/__init__.py |
| `plugins/model-providers/upstage/__init__.py` | source | Upstage Solar provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/upstage/plugin.yaml |
| `plugins/model-providers/upstage/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/upstage/__init__.py |
| `plugins/model-providers/vertex/__init__.py` | source | Google Vertex AI provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/vertex/plugin.yaml |
| `plugins/model-providers/vertex/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/vertex/__init__.py |
| `plugins/model-providers/xai/__init__.py` | source | xAI (Grok) provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/xai/plugin.yaml |
| `plugins/model-providers/xai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/xai/__init__.py |
| `plugins/model-providers/xiaomi/__init__.py` | source | Xiaomi MiMo provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/xiaomi/plugin.yaml |
| `plugins/model-providers/xiaomi/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/xiaomi/__init__.py |
| `plugins/model-providers/zai/__init__.py` | source | ZAI / GLM provider profile. | Python module executed or imported by the runtime; check git intent before deleting | plugins/model-providers/zai/plugin.yaml |
| `plugins/model-providers/zai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling | plugins/model-providers/zai/__init__.py |
