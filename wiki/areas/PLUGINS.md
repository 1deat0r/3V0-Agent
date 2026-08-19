# plugins/ — plugin ecosystem (memory, providers, tools)

The plugin ecosystem. `plugins/memory/` (closed in-tree provider set), `plugins/model-providers/` (lazy discovery, user overrides), `plugins/platforms/` (fewer adapters via plugins), context_engine, kanban, observability, achievements, disk-cleanup, spotify. In-tree third-party-product plugins are closed by policy.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/__init__.py` | source | Plugin package marker | Discovery root | ev0_cli/plugins.py |
| `plugins/browser/browser_use/__init__.py` | source | Browser Use cloud browser plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/browser/browser_use/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/browser/browser_use/provider.py` | source | Browser Use cloud browser provider — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/browser/browserbase/__init__.py` | source | Browserbase cloud browser plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/browser/browserbase/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/browser/browserbase/provider.py` | source | Browserbase cloud browser provider — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/browser/firecrawl/__init__.py` | source | Firecrawl cloud browser plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/browser/firecrawl/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/browser/firecrawl/provider.py` | source | Firecrawl cloud browser provider — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/context_engine/__init__.py` | source | Context engine plugin discovery. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/cron_providers/__init__.py` | source | Cron scheduler provider plugin discovery. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/cron_providers/chronos/__init__.py` | source | Chronos — NAS-mediated managed cron provider (scale-to-zero). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/cron_providers/chronos/_nas_client.py` | source | Thin HTTP client for the agent → NAS ``agent-cron`` endpoints (Chronos). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/cron_providers/chronos/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/cron_providers/chronos/verify.py` | source | Inbound cron-fire token verification for Chronos (Phase 4E.1). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/dashboard_auth/basic/__init__.py` | source | BasicAuthProvider — username/password dashboard auth (no OAuth IDP). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/dashboard_auth/basic/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/dashboard_auth/drain/__init__.py` | source | DrainSecretProvider — shared-bearer-secret auth for the drain-control endpoint. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/dashboard_auth/drain/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/dashboard_auth/nous/__init__.py` | source | NousDashboardAuthProvider — Nous Portal OAuth (authorization-code + PKCE). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/dashboard_auth/nous/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/dashboard_auth/self_hosted/__init__.py` | source | SelfHostedOIDCProvider — generic self-hosted OpenID Connect dashboard auth. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/dashboard_auth/self_hosted/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/disk-cleanup/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/disk-cleanup/__init__.py` | source | disk-cleanup plugin — auto-cleanup of ephemeral Hermes session files. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/disk-cleanup/disk_cleanup.py` | source | disk_cleanup — ephemeral file cleanup for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/disk-cleanup/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/google_meet/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/google_meet/SKILL.md` | skill-doc | Skill definition for `google_meet` | The instruction contract a model loads when the skill's trigger matches |  |
| `plugins/google_meet/__init__.py` | source | google_meet plugin — let the agent join a Meet call, transcribe it, follow up. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/audio_bridge.py` | source | Virtual audio bridge for feeding generated speech into Chrome's mic. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/cli.py` | source | CLI commands for the google_meet plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/meet_bot.py` | source | Headless Google Meet bot — Playwright + live-caption scraping. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/node/__init__.py` | source | Remote 'node host' primitive for the google_meet plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/node/cli.py` | source | `hermes meet node ...` subcommand tree. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/node/client.py` | source | Gateway-side RPC client for a remote meet node. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/node/protocol.py` | source | Wire protocol for gateway ↔ node RPC. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/node/registry.py` | source | Local JSON registry of approved remote meet nodes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/node/server.py` | source | Remote node server. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/google_meet/process_manager.py` | source | Subprocess lifecycle manager for the google_meet bot. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/realtime/__init__.py` | source | Realtime speech subpackage for the google_meet plugin (v2). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/realtime/openai_client.py` | source | OpenAI Realtime API WebSocket client + file-queue speaker. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/google_meet/tools.py` | source | Agent-facing tools for the google_meet plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/hermes-achievements/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/hermes-achievements/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/hermes-achievements/dashboard/dist/index.js` | asset | File `index.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/hermes-achievements/dashboard/dist/style.css` | asset | Stylesheet | Styling for a frontend surface |  |
| `plugins/hermes-achievements/dashboard/manifest.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `plugins/hermes-achievements/dashboard/plugin_api.py` | source | Hermes Achievements dashboard plugin backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/hermes-achievements/docs/assets/achievements-dashboard-hd.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `plugins/hermes-achievements/docs/assets/achievements-tier-showcase-hd.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `plugins/hermes-achievements/tests/test_achievement_engine.py` | test | Python module `test_achievement_engine.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `plugins/image_gen/deepinfra/__init__.py` | source | DeepInfra image generation backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/image_gen/deepinfra/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/image_gen/fal/__init__.py` | source | FAL.ai image generation backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/image_gen/fal/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/image_gen/krea/__init__.py` | source | Krea image generation backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/image_gen/krea/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/image_gen/openai-codex/__init__.py` | source | OpenAI image generation backend — ChatGPT/Codex OAuth variant. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/image_gen/openai-codex/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/image_gen/openai/__init__.py` | source | OpenAI image generation backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/image_gen/openai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/image_gen/openrouter/__init__.py` | source | OpenRouter-compatible image generation backend (OpenRouter + Nous Portal). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/image_gen/openrouter/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/image_gen/xai/__init__.py` | source | xAI image generation backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/image_gen/xai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/kanban/dashboard/dist/index.js` | asset | File `index.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/kanban/dashboard/dist/style.css` | asset | Stylesheet | Styling for a frontend surface |  |
| `plugins/kanban/dashboard/manifest.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `plugins/kanban/dashboard/plugin_api.py` | source | Kanban dashboard plugin — backend API routes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/kanban/systemd/3v0-kanban-dispatcher.service` | asset | File `3v0-kanban-dispatcher.service` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/memory/__init__.py` | source | Memory provider plugin discovery. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/byterover/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/memory/byterover/__init__.py` | source | ByteRover memory plugin — MemoryProvider interface. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/byterover/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/memory/config_schema.py` | source | Declarative configuration schema for memory provider plugins. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/hindsight/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/memory/hindsight/__init__.py` | source | Hindsight memory plugin — MemoryProvider interface. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/hindsight/config_schema.py` | source | Hindsight's declared config surface — rendered by the generic desktop panel. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/hindsight/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/memory/hindsight/templates.py` | source | Starter bank templates for the Hindsight memory-provider setup wizard. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/holographic/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/memory/holographic/__init__.py` | source | hermes-memory-store — holographic memory plugin using MemoryProvider interface. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/holographic/holographic.py` | source | Holographic Reduced Representations (HRR) with phase encoding. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/holographic/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/memory/holographic/retrieval.py` | source | Hybrid keyword/BM25 retrieval for the memory store. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/holographic/store.py` | source | SQLite-backed fact store with entity resolution and trust scoring. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/honcho/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/memory/honcho/__init__.py` | source | Honcho memory plugin — MemoryProvider for Honcho AI-native memory. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/honcho/cli.py` | source | CLI commands for Honcho integration management. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/honcho/client.py` | source | Honcho client initialization and configuration. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/honcho/config_schema.py` | source | Honcho's declared config surface — rendered by the generic desktop panel. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/honcho/oauth.py` | source | OAuth credential storage and refresh for the Honcho memory provider. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/honcho/oauth_flow.py` | source | Browser sign-in flow for the Honcho memory provider — no CLI step. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/honcho/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/memory/honcho/session.py` | source | Honcho-based session management for conversation history. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/mem0/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/memory/mem0/__init__.py` | source | Mem0 memory plugin — MemoryProvider interface. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/mem0/_backend.py` | source | Backend abstraction for Mem0 Platform and OSS modes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/mem0/_oss_providers.py` | source | OSS provider definitions for LLM, embedder, and vector store. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/mem0/_setup.py` | source | Setup wizard for Mem0 plugin — interactive and flag-based modes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/mem0/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/memory/openviking/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/memory/openviking/__init__.py` | source | OpenViking memory plugin — full bidirectional MemoryProvider interface. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/openviking/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/memory/query_rewrite.py` | source | Rewrite the latest user message into a clean memory-retrieval query. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/retaindb/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/memory/retaindb/__init__.py` | source | RetainDB memory plugin — MemoryProvider interface. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/retaindb/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/memory/supermemory/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/memory/supermemory/__init__.py` | source | Supermemory memory plugin using the MemoryProvider interface. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/memory/supermemory/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/model-providers/actual/__init__.py` | source | Actual Computer provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/actual/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/ai-gateway/__init__.py` | source | Vercel AI Gateway provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/ai-gateway/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/alibaba-coding-plan/__init__.py` | source | Alibaba Cloud Coding Plan provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/alibaba-coding-plan/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/alibaba/__init__.py` | source | Alibaba Cloud DashScope provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/alibaba/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/anthropic/__init__.py` | source | Native Anthropic provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/anthropic/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/arcee/__init__.py` | source | Arcee AI provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/arcee/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/azure-foundry/__init__.py` | source | Microsoft Foundry provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/azure-foundry/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/bedrock/__init__.py` | source | AWS Bedrock provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/bedrock/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/copilot-acp/__init__.py` | source | GitHub Copilot ACP provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/copilot-acp/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/copilot/__init__.py` | source | Copilot / GitHub Models provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/copilot/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/custom/__init__.py` | source | Custom / Ollama (local) provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/custom/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/deepinfra/__init__.py` | source | DeepInfra provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/deepinfra/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/deepseek/__init__.py` | source | DeepSeek provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/deepseek/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/fireworks/__init__.py` | source | Fireworks AI provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/fireworks/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/gemini/__init__.py` | source | Google Gemini provider profiles. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/gemini/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/gmi/__init__.py` | source | GMI Cloud provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/gmi/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/huggingface/__init__.py` | source | Hugging Face provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/huggingface/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/kilocode/__init__.py` | source | Kilo Code provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/kilocode/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/kimi-coding/__init__.py` | source | Kimi / Moonshot provider profiles. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/kimi-coding/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/minimax/__init__.py` | source | MiniMax provider profiles (international + China). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/minimax/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/nous/__init__.py` | source | Nous Portal provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/nous/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/novita/__init__.py` | source | NovitaAI provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/novita/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/nvidia/__init__.py` | source | NVIDIA NIM provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/nvidia/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/ollama-cloud/__init__.py` | source | Ollama Cloud provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/ollama-cloud/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/openai-codex/__init__.py` | source | OpenAI Codex (Responses API) provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/openai-codex/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/opencode-zen/__init__.py` | source | OpenCode provider profiles (Zen + Go). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/opencode-zen/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/openrouter/__init__.py` | source | OpenRouter provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/openrouter/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/qwen-oauth/__init__.py` | source | Qwen Portal provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/qwen-oauth/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/stepfun/__init__.py` | source | StepFun provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/stepfun/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/upstage/__init__.py` | source | Upstage Solar provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/upstage/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/vertex/__init__.py` | source | Google Vertex AI provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/vertex/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/xai/__init__.py` | source | xAI (Grok) provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/xai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/xiaomi/__init__.py` | source | Xiaomi MiMo provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/xiaomi/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/model-providers/zai/__init__.py` | source | ZAI / GLM provider profile. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/model-providers/zai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/observability/langfuse/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/observability/langfuse/__init__.py` | source | langfuse — Hermes plugin for Langfuse observability. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/observability/langfuse/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/observability/nemo_relay/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/observability/nemo_relay/__init__.py` | source | nemo_relay — optional Hermes plugin for NeMo Relay observability. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/observability/nemo_relay/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/a2a/DESIGN.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `plugins/platforms/a2a/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/platforms/a2a/__init__.py` | source | A2A (Agent-to-Agent) plugin for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/a2a/adapter.py` | source | A2A inbound platform adapter — exposes Hermes as an A2A-discoverable agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/a2a/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/a2a/protocol.py` | source | A2A protocol helpers — Agent Card construction, JSON-RPC framing, task store, | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/a2a/security.py` | source | A2A security primitives — shared by the inbound adapter and the client tools. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/a2a/tools.py` | source | A2A client tools — let the Hermes agent talk to *other* agents as a peer. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/buzz/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/buzz/adapter.py` | source | Buzz Platform Adapter for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/buzz/nostr_auth.py` | source | Dependency-free Nostr signing for Buzz WebSocket authentication. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/buzz/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/dingtalk/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/dingtalk/adapter.py` | source | DingTalk platform adapter using Stream Mode. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/dingtalk/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/discord/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/discord/adapter.py` | source | Discord platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/discord/ffmpeg_utils.py` | source | Shared ffmpeg executable discovery for Discord voice paths. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/discord/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/discord/recovery.py` | source | Durable state for Discord reconnect message recovery. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/discord/voice_mixer.py` | source | Continuous PCM audio mixer for Discord voice channels. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/email/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/email/adapter.py` | source | Email platform adapter for the Hermes gateway. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/email/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/feishu/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/feishu/adapter.py` | source | Feishu/Lark platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/feishu/feishu_comment.py` | source | Feishu/Lark drive document comment handling. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/feishu/feishu_comment_rules.py` | source | Feishu document comment access-control rules. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/feishu/feishu_meeting_invite.py` | source | Feishu/Lark meeting-invitation event handling. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/feishu/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/google_chat/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/google_chat/adapter.py` | source | Google Chat platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/google_chat/oauth.py` | source | User OAuth helper for the Google Chat gateway adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/google_chat/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/homeassistant/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/homeassistant/adapter.py` | source | Home Assistant platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/homeassistant/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/irc/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/irc/adapter.py` | source | IRC Platform Adapter for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/irc/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/line/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/line/adapter.py` | source | LINE Messaging API platform adapter for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/line/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/matrix/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/matrix/adapter.py` | source | Matrix gateway adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/matrix/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/mattermost/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/mattermost/adapter.py` | source | Mattermost gateway adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/mattermost/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/ntfy/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/ntfy/adapter.py` | source | ntfy platform adapter (Hermes plugin). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/ntfy/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/photon/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/platforms/photon/__init__.py` | source | Photon Spectrum (iMessage) platform plugin entry point. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/photon/adapter.py` | source | Photon Spectrum (iMessage) platform adapter for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/photon/auth.py` | source | Photon Dashboard API client + device-code login flow. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/photon/cli.py` | source | ``hermes photon ...`` CLI subcommands — registered by the plugin via | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/photon/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/photon/sidecar/.gitignore` | asset | File `.gitignore` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/platforms/photon/sidecar/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/platforms/photon/sidecar/index.mjs` | asset | File `index.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/platforms/photon/sidecar/package-lock.json` | lockfile | Generated dependency lockfile | Pins every transitive dep with hashes (supply-chain invariant); regenerated by uv/npm |  |
| `plugins/platforms/photon/sidecar/package.json` | build | Node package manifest | Declares JS workspace deps + scripts |  |
| `plugins/platforms/photon/sidecar/patch-spectrum-mixed-attachments.mjs` | asset | File `patch-spectrum-mixed-attachments.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/platforms/photon/sidecar/send-format.mjs` | asset | File `send-format.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/platforms/photon/sidecar/stream-staleness.mjs` | asset | File `stream-staleness.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/platforms/photon/sidecar_paths.py` | source | Resolve where the Photon sidecar runs from and where its Node deps live. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/raft/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/raft/adapter.py` | source | Raft channel platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/raft/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/simplex/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/simplex/adapter.py` | source | SimpleX Chat platform adapter (Hermes plugin). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/simplex/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/slack/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/slack/adapter.py` | source | Slack platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/slack/block_kit.py` | source | Render agent markdown into Slack Block Kit blocks. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/slack/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/sms/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/sms/adapter.py` | source | SMS (Twilio) platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/sms/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/teams/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/teams/adapter.py` | source | Microsoft Teams platform adapter for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/teams/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/telegram/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/telegram/adapter.py` | source | Telegram platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/telegram/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/telegram/telegram_ids.py` | source | Helpers for Telegram Bot API chat identifiers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/telegram/telegram_network.py` | source | Telegram-specific network helpers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/wecom/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/wecom/adapter.py` | source | WeCom (Enterprise WeChat) platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/wecom/callback_adapter.py` | source | WeCom callback-mode adapter for self-built enterprise applications. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/wecom/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/platforms/wecom/wecom_crypto.py` | source | WeCom BizMsgCrypt-compatible AES-CBC encryption for callback mode. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/whatsapp/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/whatsapp/adapter.py` | source | WhatsApp platform adapter. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/platforms/whatsapp/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/plugin_utils.py` | source | Shared concurrency helpers for plugin authors. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/security-guidance/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/security-guidance/NOTICE` | asset | File `NOTICE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `plugins/security-guidance/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `plugins/security-guidance/__init__.py` | source | security-guidance plugin — fast pattern-matched security warnings on file writes. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/security-guidance/patterns.py` | source | Regex-based security pattern definitions for the security-guidance plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/security-guidance/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/spotify/__init__.py` | source | Spotify integration plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/spotify/client.py` | source | Thin Spotify Web API helper used by Hermes native tools. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/spotify/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/spotify/tools.py` | source | Native Spotify tools for Hermes (registered via plugins/spotify). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/teams_pipeline/__init__.py` | source | Teams meeting pipeline plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/teams_pipeline/cli.py` | source | CLI commands for the Teams meeting pipeline plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/teams_pipeline/meetings.py` | source | Graph-backed Teams meeting helpers for the plugin runtime. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/teams_pipeline/models.py` | source | Normalized models for the Teams meeting pipeline plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/teams_pipeline/pipeline.py` | source | Pipeline orchestration for Microsoft Teams meeting summaries. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/teams_pipeline/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/teams_pipeline/runtime.py` | source | Gateway runtime wiring for the Teams meeting pipeline plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/teams_pipeline/store.py` | source | Durable local state for the Teams pipeline plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/teams_pipeline/subscriptions.py` | source | Microsoft Graph subscription helpers for the Teams pipeline plugin. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/video_gen/deepinfra/__init__.py` | source | DeepInfra video generation backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/video_gen/deepinfra/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/video_gen/fal/__init__.py` | source | FAL.ai video generation backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/video_gen/fal/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/video_gen/xai/__init__.py` | source | xAI Grok-Imagine video generation backend. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/video_gen/xai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/brave_free/__init__.py` | source | Brave Search (free tier) plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/brave_free/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/brave_free/provider.py` | source | Brave Search (free tier) — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/ddgs/__init__.py` | source | DuckDuckGo search plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/ddgs/_search_worker.py` | source | DDGS search child-process entrypoint (#68096). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/ddgs/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/ddgs/provider.py` | source | DuckDuckGo search — plugin form (via the ``ddgs`` package). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/exa/__init__.py` | source | Exa web search + extract plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/exa/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/exa/provider.py` | source | Exa web search + content extraction — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/firecrawl/__init__.py` | source | Firecrawl web search + extract plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/firecrawl/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/firecrawl/provider.py` | source | Firecrawl web search + extract — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/parallel/__init__.py` | source | Parallel.ai web search + extract plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/parallel/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/parallel/provider.py` | source | Parallel.ai web search + content extraction — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/searxng/__init__.py` | source | SearXNG search plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/searxng/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/searxng/provider.py` | source | SearXNG search — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/tavily/__init__.py` | source | Tavily web search + extract plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/tavily/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/tavily/provider.py` | source | Tavily web search + content extraction — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/xai/__init__.py` | source | xAI web search plugin — bundled, auto-loaded. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `plugins/web/xai/plugin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `plugins/web/xai/provider.py` | source | xAI Web Search — plugin form. | Python module executed or imported by the runtime; check git intent before deleting |  |
