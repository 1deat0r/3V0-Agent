# skills/ + optional-skills/ — the skill libraries

The skill libraries: `skills/` (built-in, active by default, by category) and `optional-skills/` (heavier/niche, installed via `hermes skills install official/...`). SKILL.md frontmatter is load-bearing for the loader. Authoring standards are hardline.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `optional-skills/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/autonomous-ai-agents/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/autonomous-ai-agents/antigravity-cli/SKILL.md` | skill-doc | Skill definition for `antigravity-cli` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/autonomous-ai-agents/antigravity-cli/references/cli-docs.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/autonomous-ai-agents/blackbox/SKILL.md` | skill-doc | Skill definition for `blackbox` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/autonomous-ai-agents/grok/SKILL.md` | skill-doc | Skill definition for `grok` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/autonomous-ai-agents/honcho/SKILL.md` | skill-doc | Skill definition for `honcho` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/autonomous-ai-agents/openhands/SKILL.md` | skill-doc | Skill definition for `openhands` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/blockchain/evm/SKILL.md` | skill-doc | Skill definition for `evm` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/blockchain/evm/scripts/evm_client.py` | source | evm_client.py — EVM blockchain CLI tool for the Hermes Agent project. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/blockchain/hyperliquid/SKILL.md` | skill-doc | Skill definition for `hyperliquid` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/blockchain/hyperliquid/scripts/hyperliquid_client.py` | source | Hyperliquid CLI Tool for Hermes Agent | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/blockchain/solana/SKILL.md` | skill-doc | Skill definition for `solana` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/blockchain/solana/scripts/solana_client.py` | source | Solana Blockchain CLI Tool for Hermes Agent | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/communication/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/communication/one-three-one-rule/SKILL.md` | skill-doc | Skill definition for `one-three-one-rule` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/audiocraft-audio-generation/SKILL.md` | skill-doc | Skill definition for `audiocraft-audio-generation` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/audiocraft-audio-generation/references/advanced-usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/audiocraft-audio-generation/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/PORT_NOTES.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/SKILL.md` | skill-doc | Skill definition for `baoyu-article-illustrator` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/baoyu-article-illustrator/prompts/system.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/palettes/macaron.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/palettes/mono-ink.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/palettes/neon.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/palettes/warm.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/prompt-construction.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/style-presets.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/blueprint.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/chalkboard.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/editorial.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/elegant.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/fantasy-animation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/flat-doodle.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/flat.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/ink-notes.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/intuition-machine.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/minimal.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/nature.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/notion.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/pixel-art.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/playful.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/retro.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/scientific.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/screen-print.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/sketch-notes.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/sketch.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/vector-illustration.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/vintage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/warm.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/styles/watercolor.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-article-illustrator/references/workflow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/PORT_NOTES.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/SKILL.md` | skill-doc | Skill definition for `baoyu-comic` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/baoyu-comic/references/analysis-framework.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/art-styles/chalk.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/art-styles/ink-brush.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/art-styles/ligne-claire.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/art-styles/manga.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/art-styles/minimalist.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/art-styles/realistic.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/auto-selection.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/base-prompt.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/character-template.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/layouts/cinematic.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/layouts/dense.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/layouts/four-panel.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/layouts/mixed.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/layouts/splash.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/layouts/standard.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/layouts/webtoon.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/ohmsha-guide.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/partial-workflows.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/presets/concept-story.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/presets/four-panel.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/presets/ohmsha.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/presets/shoujo.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/presets/wuxia.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/storyboard-template.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/tones/action.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/tones/dramatic.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/tones/energetic.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/tones/neutral.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/tones/romantic.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/tones/vintage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/tones/warm.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/baoyu-comic/references/workflow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/SKILL.md` | skill-doc | Skill definition for `concept-diagrams` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/concept-diagrams/examples/apartment-floor-plan-conversion.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/automated-password-reset-flow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/autonomous-llm-research-agent-flow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/banana-journey-tree-to-smoothie.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/commercial-aircraft-structure.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/cpu-ooo-microarchitecture.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/electricity-grid-flow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/feature-film-production-pipeline.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/hospital-emergency-department-flow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/ml-benchmark-grouped-bar-chart.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/place-order-uml-sequence.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/smart-city-infrastructure.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/smartphone-layer-anatomy.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/sn2-reaction-mechanism.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/examples/wind-turbine-structure.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/references/dashboard-patterns.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/references/infrastructure-patterns.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/references/physical-shape-cookbook.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/concept-diagrams/templates/template.html` | asset | File `template.html` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/creative/creative-ideation/SKILL.md` | skill-doc | Skill definition for `creative-ideation` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/creative-ideation/references/anti-slop.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/exercises.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/full-prompt-library.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/heuristics.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/method-catalog.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/affinity-diagrams.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/analogy-and-blending.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/biomimicry.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/chance-and-remix.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/compression-progress.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/creative-discipline.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/defamiliarization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/derive-and-mapping.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/first-principles.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/jobs-to-be-done.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/lateral-provocations.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/leverage-points.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/oblique-strategies.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/oulipo.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/pataphysics.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/pattern-languages.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/polya.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/premortem-and-inversion.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/scamper.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/story-skeletons.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/triz-principles.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/creative-ideation/references/methods/volume-generation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/heartmula/SKILL.md` | skill-doc | Skill definition for `heartmula` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/hyperframes/SKILL.md` | skill-doc | Skill definition for `hyperframes` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/hyperframes/references/cli.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/hyperframes/references/composition.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/hyperframes/references/features.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/hyperframes/references/gsap.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/hyperframes/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/hyperframes/references/website-to-video.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/hyperframes/scripts/setup.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `optional-skills/creative/kanban-video-orchestrator/SKILL.md` | skill-doc | Skill definition for `kanban-video-orchestrator` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/kanban-video-orchestrator/assets/brief.md.tmpl` | asset | File `brief.md.tmpl` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/creative/kanban-video-orchestrator/assets/setup.sh.tmpl` | asset | File `setup.sh.tmpl` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/creative/kanban-video-orchestrator/assets/soul.md.tmpl` | asset | File `soul.md.tmpl` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/creative/kanban-video-orchestrator/references/examples.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/kanban-video-orchestrator/references/intake.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/kanban-video-orchestrator/references/kanban-setup.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/kanban-video-orchestrator/references/monitoring.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/kanban-video-orchestrator/references/role-archetypes.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/kanban-video-orchestrator/references/tool-matrix.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/kanban-video-orchestrator/scripts/bootstrap_pipeline.py` | source | Bootstrap a video production kanban from a structured plan JSON. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/creative/kanban-video-orchestrator/scripts/monitor.py` | source | Monitor a running video-production kanban. Polls `hermes kanban list` and | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/creative/meme-generation/EXAMPLES.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/meme-generation/SKILL.md` | skill-doc | Skill definition for `meme-generation` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/meme-generation/scripts/.gitignore` | asset | File `.gitignore` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/creative/meme-generation/scripts/generate_meme.py` | source | Generate a meme image by overlaying text on a template. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/creative/meme-generation/scripts/templates.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/creative/pixel-art/ATTRIBUTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/pixel-art/SKILL.md` | skill-doc | Skill definition for `pixel-art` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/pixel-art/references/palettes.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/pixel-art/scripts/__init__.py` | source | Python module `__init__.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/creative/pixel-art/scripts/palettes.py` | source | Named RGB palettes for pixel_art() and pixel_art_video(). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/creative/pixel-art/scripts/pixel_art.py` | source | Pixel art converter — Floyd-Steinberg dithering with preset or named palette. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/creative/pixel-art/scripts/pixel_art_video.py` | source | Pixel art video — overlay procedural animations onto a source image. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/creative/social-media-content-calendar/SKILL.md` | skill-doc | Skill definition for `social-media-content-calendar` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/tldraw-offline/SKILL.md` | skill-doc | Skill definition for `tldraw-offline` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/tldraw-offline/scripts/counter.js` | asset | File `counter.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/creative/tldraw-offline/scripts/main.js` | asset | File `main.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/creative/tldraw-offline/scripts/validate_shapes.mjs` | asset | File `validate_shapes.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/creative/unreal-mcp/SKILL.md` | skill-doc | Skill definition for `unreal-mcp` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/creative/unreal-mcp/references/advanced-workflows.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/unreal-mcp/references/pitfalls.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/unreal-mcp/references/recipes.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/unreal-mcp/references/scene-craft.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/creative/unreal-mcp/references/tool-surface.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/data-science/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/data-science/jupyter-notebook/SKILL.md` | skill-doc | Skill definition for `jupyter-notebook` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/devops/actual-setup/SKILL.md` | skill-doc | Skill definition for `actual-setup` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/devops/actual-setup/references/opencode.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/devops/docker-management/SKILL.md` | skill-doc | Skill definition for `docker-management` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/devops/hermes-s6-container-supervision/SKILL.md` | skill-doc | Skill definition for `hermes-s6-container-supervision` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/devops/inference-sh-cli/SKILL.md` | skill-doc | Skill definition for `inference-sh-cli` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/devops/inference-sh-cli/references/app-discovery.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/devops/inference-sh-cli/references/authentication.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/devops/inference-sh-cli/references/cli-reference.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/devops/inference-sh-cli/references/running-apps.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/devops/pinggy-tunnel/SKILL.md` | skill-doc | Skill definition for `pinggy-tunnel` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/devops/watchers/SKILL.md` | skill-doc | Skill definition for `watchers` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/devops/watchers/scripts/_watermark.py` | source | Shared watermark helper used by the three watcher scripts. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/devops/watchers/scripts/watch_github.py` | source | Watch GitHub activity — issues, pulls, releases, or commits — with dedup. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/devops/watchers/scripts/watch_http_json.py` | source | Watch any JSON endpoint that returns a list of objects; dedup by ID field. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/devops/watchers/scripts/watch_rss.py` | source | Watch an RSS 2.0 or Atom feed; print new items to stdout, silent on empty. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/dogfood/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/dogfood/adversarial-ux-test/SKILL.md` | skill-doc | Skill definition for `adversarial-ux-test` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/email/agentmail/SKILL.md` | skill-doc | Skill definition for `agentmail` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/3-statement-model/SKILL.md` | skill-doc | Skill definition for `3-statement-model` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/3-statement-model/references/formatting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/finance/3-statement-model/references/formulas.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/finance/3-statement-model/references/sec-filings.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/finance/comps-analysis/SKILL.md` | skill-doc | Skill definition for `comps-analysis` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/dcf-model/SKILL.md` | skill-doc | Skill definition for `dcf-model` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/dcf-model/TROUBLESHOOTING.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/finance/dcf-model/requirements.txt` | asset | File `requirements.txt` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/finance/dcf-model/scripts/validate_dcf.py` | source | DCF Model Validation Script | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/finance/excel-author/SKILL.md` | skill-doc | Skill definition for `excel-author` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/excel-author/scripts/recalc.py` | source | Recalculate an .xlsx file's formulas using LibreOffice headless. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/finance/lbo-model/SKILL.md` | skill-doc | Skill definition for `lbo-model` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/merger-model/SKILL.md` | skill-doc | Skill definition for `merger-model` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/polymarket/SKILL.md` | skill-doc | Skill definition for `polymarket` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/polymarket/references/api-endpoints.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/finance/polymarket/scripts/polymarket.py` | source | Polymarket CLI helper — query prediction market data. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/finance/pptx-author/SKILL.md` | skill-doc | Skill definition for `pptx-author` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/stocks/SKILL.md` | skill-doc | Skill definition for `stocks` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/finance/stocks/scripts/stocks_client.py` | source | stocks_client.py - Stock market data CLI tool for the Hermes Agent project. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/gaming/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/gaming/minecraft-modpack-server/SKILL.md` | skill-doc | Skill definition for `minecraft-modpack-server` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/gaming/pokemon-player/SKILL.md` | skill-doc | Skill definition for `pokemon-player` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/health/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/health/fitness-nutrition/SKILL.md` | skill-doc | Skill definition for `fitness-nutrition` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/health/fitness-nutrition/references/FORMULAS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/health/fitness-nutrition/scripts/body_calc.py` | source | body_calc.py — All-in-one fitness calculator. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/health/fitness-nutrition/scripts/nutrition_search.py` | source | nutrition_search.py — Search USDA FoodData Central for nutrition info. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/health/neuroskill-bci/SKILL.md` | skill-doc | Skill definition for `neuroskill-bci` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/health/neuroskill-bci/references/api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/health/neuroskill-bci/references/metrics.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/health/neuroskill-bci/references/protocols.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mcp/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mcp/fastmcp/SKILL.md` | skill-doc | Skill definition for `fastmcp` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mcp/fastmcp/references/fastmcp-cli.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mcp/fastmcp/scripts/scaffold_fastmcp.py` | source | Copy a FastMCP starter template into a working file. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/mcp/fastmcp/templates/api_wrapper.py` | source | Python module `api_wrapper.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/mcp/fastmcp/templates/database_server.py` | source | Python module `database_server.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/mcp/fastmcp/templates/file_processor.py` | source | Python module `file_processor.py` | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/mcp/mcp-oauth-remote-gateway/SKILL.md` | skill-doc | Skill definition for `mcp-oauth-remote-gateway` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mcp/mcp-oauth-remote-gateway/references/stripe-mcp-oauth-revocation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mcp/mcp-oauth-remote-gateway/scripts/diagnose-oauth-mcp.py` | source | Diagnose an OAuth-gated remote MCP server's connection state. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/mcp/mcporter/SKILL.md` | skill-doc | Skill definition for `mcporter` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/migration/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/migration/openclaw-migration/SKILL.md` | skill-doc | Skill definition for `openclaw-migration` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py` | source | OpenClaw -> Hermes migration helper. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/mlops/accelerate/SKILL.md` | skill-doc | Skill definition for `accelerate` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/accelerate/references/custom-plugins.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/accelerate/references/megatron-integration.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/accelerate/references/performance.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/chroma/SKILL.md` | skill-doc | Skill definition for `chroma` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/chroma/references/integration.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/clip/SKILL.md` | skill-doc | Skill definition for `clip` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/clip/references/applications.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/faiss/SKILL.md` | skill-doc | Skill definition for `faiss` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/faiss/references/index_types.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/flash-attention/SKILL.md` | skill-doc | Skill definition for `flash-attention` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/flash-attention/references/benchmarks.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/flash-attention/references/transformers-integration.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/guidance/SKILL.md` | skill-doc | Skill definition for `guidance` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/guidance/references/backends.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/guidance/references/constraints.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/guidance/references/examples.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/huggingface-tokenizers/SKILL.md` | skill-doc | Skill definition for `huggingface-tokenizers` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/huggingface-tokenizers/references/algorithms.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/huggingface-tokenizers/references/integration.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/huggingface-tokenizers/references/pipeline.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/huggingface-tokenizers/references/training.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/inference/outlines/SKILL.md` | skill-doc | Skill definition for `outlines` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/inference/outlines/references/backends.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/inference/outlines/references/examples.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/inference/outlines/references/json_generation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/instructor/SKILL.md` | skill-doc | Skill definition for `instructor` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/instructor/references/examples.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/instructor/references/providers.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/instructor/references/validation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/lambda-labs/SKILL.md` | skill-doc | Skill definition for `lambda-labs` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/lambda-labs/references/advanced-usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/lambda-labs/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/llava/SKILL.md` | skill-doc | Skill definition for `llava` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/llava/references/training.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/modal/SKILL.md` | skill-doc | Skill definition for `modal` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/modal/references/advanced-usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/modal/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/models/segment-anything-model/SKILL.md` | skill-doc | Skill definition for `segment-anything-model` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/models/segment-anything-model/references/advanced-usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/models/segment-anything-model/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/nemo-curator/SKILL.md` | skill-doc | Skill definition for `nemo-curator` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/nemo-curator/references/deduplication.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/nemo-curator/references/filtering.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/obliteratus/SKILL.md` | skill-doc | Skill definition for `obliteratus` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/obliteratus/references/analysis-modules.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/obliteratus/references/methods-guide.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/obliteratus/templates/abliteration-config.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-skills/mlops/obliteratus/templates/analysis-study.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-skills/mlops/obliteratus/templates/batch-abliteration.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `optional-skills/mlops/peft/SKILL.md` | skill-doc | Skill definition for `peft` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/peft/references/advanced-usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/peft/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/pinecone/SKILL.md` | skill-doc | Skill definition for `pinecone` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/pinecone/references/deployment.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/pytorch-fsdp/SKILL.md` | skill-doc | Skill definition for `pytorch-fsdp` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/pytorch-fsdp/references/common-patterns.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/pytorch-fsdp/references/index.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/pytorch-fsdp/references/other.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/pytorch-lightning/SKILL.md` | skill-doc | Skill definition for `pytorch-lightning` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/pytorch-lightning/references/callbacks.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/pytorch-lightning/references/distributed.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/pytorch-lightning/references/hyperparameter-tuning.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/qdrant/SKILL.md` | skill-doc | Skill definition for `qdrant` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/qdrant/references/advanced-usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/qdrant/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/research/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/research/dspy/SKILL.md` | skill-doc | Skill definition for `dspy` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/research/dspy/references/examples.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/research/dspy/references/modules.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/research/dspy/references/optimizers.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/saelens/SKILL.md` | skill-doc | Skill definition for `saelens` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/saelens/references/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `optional-skills/mlops/saelens/references/api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/saelens/references/tutorials.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/simpo/SKILL.md` | skill-doc | Skill definition for `simpo` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/simpo/references/datasets.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/simpo/references/hyperparameters.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/simpo/references/loss-functions.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/slime/SKILL.md` | skill-doc | Skill definition for `slime` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/slime/references/api-reference.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/slime/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/stable-diffusion/SKILL.md` | skill-doc | Skill definition for `stable-diffusion` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/stable-diffusion/references/advanced-usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/stable-diffusion/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/tensorrt-llm/SKILL.md` | skill-doc | Skill definition for `tensorrt-llm` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/tensorrt-llm/references/multi-gpu.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/tensorrt-llm/references/optimization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/tensorrt-llm/references/serving.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/torchtitan/SKILL.md` | skill-doc | Skill definition for `torchtitan` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/torchtitan/references/checkpoint.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/torchtitan/references/custom-models.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/torchtitan/references/float8.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/torchtitan/references/fsdp.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/axolotl/SKILL.md` | skill-doc | Skill definition for `axolotl` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/training/axolotl/references/api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/axolotl/references/dataset-formats.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/axolotl/references/index.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/axolotl/references/other.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/trl-fine-tuning/SKILL.md` | skill-doc | Skill definition for `trl-fine-tuning` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/training/trl-fine-tuning/references/dpo-variants.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/trl-fine-tuning/references/grpo-training.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/trl-fine-tuning/references/online-rl.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/trl-fine-tuning/references/reward-modeling.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/trl-fine-tuning/references/sft-training.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/trl-fine-tuning/templates/basic_grpo_training.py` | source | Basic GRPO Training Template | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/mlops/training/unsloth/SKILL.md` | skill-doc | Skill definition for `unsloth` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/training/unsloth/references/index.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/unsloth/references/llms-full.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/unsloth/references/llms-txt.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/training/unsloth/references/llms.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/mlops/whisper/SKILL.md` | skill-doc | Skill definition for `whisper` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/mlops/whisper/references/languages.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/payments/mpp-agent/SKILL.md` | skill-doc | Skill definition for `mpp-agent` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/payments/stripe-link-cli/SKILL.md` | skill-doc | Skill definition for `stripe-link-cli` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/payments/stripe-projects/SKILL.md` | skill-doc | Skill definition for `stripe-projects` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/productivity/canvas/SKILL.md` | skill-doc | Skill definition for `canvas` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/productivity/canvas/scripts/canvas_api.py` | source | Canvas LMS API CLI for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/productivity/here-now/SKILL.md` | skill-doc | Skill definition for `here-now` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/productivity/here-now/scripts/drive.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `optional-skills/productivity/here-now/scripts/publish.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `optional-skills/productivity/memento-flashcards/SKILL.md` | skill-doc | Skill definition for `memento-flashcards` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/productivity/memento-flashcards/scripts/memento_cards.py` | source | Memento card storage, spaced-repetition engine, and CSV I/O. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/productivity/memento-flashcards/scripts/youtube_quiz.py` | source | Fetch YouTube transcripts for Memento quiz generation. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/productivity/shop/SKILL.md` | skill-doc | Skill definition for `shop` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/productivity/shop/references/catalog-mcp.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/productivity/shop/references/direct-api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/productivity/shop/references/legal.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/productivity/shop/references/safety.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/productivity/shopify/SKILL.md` | skill-doc | Skill definition for `shopify` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/productivity/siyuan/SKILL.md` | skill-doc | Skill definition for `siyuan` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/productivity/telephony/SKILL.md` | skill-doc | Skill definition for `telephony` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/productivity/telephony/scripts/telephony.py` | source | Telephony helper for the Hermes optional telephony skill. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/bioinformatics/SKILL.md` | skill-doc | Skill definition for `bioinformatics` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/darwinian-evolver/SKILL.md` | skill-doc | Skill definition for `darwinian-evolver` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/darwinian-evolver/scripts/parrot_openrouter.py` | source | parrot_openrouter: same as the upstream `parrot` example but the LLM call goes | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/darwinian-evolver/scripts/show_snapshot.py` | source | show_snapshot.py — Dump the population from a darwinian-evolver snapshot pickle. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/darwinian-evolver/templates/custom_problem_template.py` | source | Template: a custom darwinian-evolver problem. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/domain-intel/SKILL.md` | skill-doc | Skill definition for `domain-intel` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/domain-intel/scripts/domain_intel.py` | source | Domain Intelligence — Passive OSINT via Python stdlib. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/drug-discovery/SKILL.md` | skill-doc | Skill definition for `drug-discovery` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/drug-discovery/references/ADMET_REFERENCE.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/drug-discovery/scripts/chembl_target.py` | source | chembl_target.py — Search ChEMBL for a target and retrieve top active compounds. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/drug-discovery/scripts/ro5_screen.py` | source | ro5_screen.py — Batch Lipinski Ro5 + Veber screening via PubChem API. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/duckduckgo-search/SKILL.md` | skill-doc | Skill definition for `duckduckgo-search` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/duckduckgo-search/scripts/duckduckgo.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `optional-skills/research/gitnexus-explorer/SKILL.md` | skill-doc | Skill definition for `gitnexus-explorer` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/gitnexus-explorer/scripts/proxy.mjs` | asset | File `proxy.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/research/osint-investigation/SKILL.md` | skill-doc | Skill definition for `osint-investigation` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/osint-investigation/references/sources/courtlistener.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/gdelt.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/icij-offshore.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/nyc-acris.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/ofac-sdn.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/opencorporates.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/sec-edgar.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/senate-ld.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/usaspending.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/wayback.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/references/sources/wikipedia.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/osint-investigation/scripts/_http.py` | source | Tiny stdlib HTTP helper used by fetch_*.py scripts. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/_normalize.py` | source | Shared entity-name normalization helpers (stdlib-only). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/build_findings.py` | source | Build a structured findings.json with evidence chains (stdlib-only). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/entity_resolution.py` | source | Cross-source entity resolution (stdlib-only). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_courtlistener.py` | source | Search court records via CourtListener (Free Law Project). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_gdelt.py` | source | Search the GDELT 2.0 DOC API for news mentions. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_icij_offshore.py` | source | Search ICIJ Offshore Leaks via the bulk CSV database. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_nyc_acris.py` | source | Search NYC property records via ACRIS (Automated City Register Information System). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_ofac_sdn.py` | source | Fetch OFAC SDN list (CSV format) and normalize. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_opencorporates.py` | source | Search OpenCorporates company registry data. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_sec_edgar.py` | source | Fetch SEC EDGAR filings index for a given CIK or company name. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_senate_ld.py` | source | Fetch Senate Lobbying Disclosure (LD-1 / LD-2) filings. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_usaspending.py` | source | Fetch federal contracts/awards from USAspending.gov API v2. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_wayback.py` | source | Search the Internet Archive Wayback Machine via the CDX server. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/fetch_wikipedia.py` | source | Search Wikipedia + Wikidata for an entity (person, company, place, concept). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/scripts/timing_analysis.py` | source | Permutation test for donation/contract timing correlation (stdlib-only). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/osint-investigation/templates/source-template.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/research/parallel-cli/SKILL.md` | skill-doc | Skill definition for `parallel-cli` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/pinecone-research/SKILL.md` | skill-doc | Skill definition for `pinecone-research` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/pinecone-research/scripts/memory_manager.py` | source | Pinecone memory manager — namespace-based session memory for agents. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/pinecone-research/scripts/rag_pipeline.py` | source | Pinecone RAG pipeline — index documents and query with retrieval-augmented generation. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/research/qmd/SKILL.md` | skill-doc | Skill definition for `qmd` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/scrapling/SKILL.md` | skill-doc | Skill definition for `scrapling` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/searxng-search/SKILL.md` | skill-doc | Skill definition for `searxng-search` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/research/searxng-search/scripts/searxng.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `optional-skills/security/1password/SKILL.md` | skill-doc | Skill definition for `1password` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/security/1password/references/cli-examples.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/1password/references/get-started.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/godmode/SKILL.md` | skill-doc | Skill definition for `godmode` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/security/godmode/references/jailbreak-templates.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/godmode/references/refusal-detection.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/godmode/scripts/auto_jailbreak.py` | source | Auto-Jailbreak Pipeline | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/godmode/scripts/godmode_race.py` | source | ULTRAPLINIAN Multi-Model Racing Engine | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/godmode/scripts/load_godmode.py` | source | Loader for G0DM0D3 scripts. Handles the exec-scoping issues. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/godmode/scripts/parseltongue.py` | source | Parseltongue v4 — Input Obfuscation Engine | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/godmode/templates/prefill-subtle.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/godmode/templates/prefill.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/oss-forensics/SKILL.md` | skill-doc | Skill definition for `oss-forensics` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/security/oss-forensics/references/evidence-types.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/oss-forensics/references/github-archive-guide.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/oss-forensics/references/investigation-templates.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/oss-forensics/references/recovery-techniques.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/oss-forensics/scripts/evidence-store.py` | source | OSS Forensics Evidence Store Manager | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/oss-forensics/templates/forensic-report.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/oss-forensics/templates/malicious-package-report.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/sherlock/SKILL.md` | skill-doc | Skill definition for `sherlock` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/security/unbroker/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `optional-skills/security/unbroker/SKILL.md` | skill-doc | Skill definition for `unbroker` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/security/unbroker/assets/unbroker.png` | asset | Image asset | Static media referenced by docs or frontend |  |
| `optional-skills/security/unbroker/references/brokers/addresses.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/advancedbackgroundchecks.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/beenverified.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/clustal.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/clustrmaps.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/cyberbackgroundchecks.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/familytreenow.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/fastpeoplesearch.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/intelius.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/mylife.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/nuwber.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/peekyou.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/peoplefinders.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/radaris.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/rehold.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/searchpeoplefree.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/socialcatfish.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/spokeo.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/thatsthem.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/truepeoplesearch.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/usphonebook.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/brokers/whitepages.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/unbroker/references/legal/ccpa.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/unbroker/references/legal/drop.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/unbroker/references/legal/gdpr.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/unbroker/references/methods.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/unbroker/references/site-playbooks.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/unbroker/references/state-machine.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/unbroker/scripts/autopilot.py` | source | Autonomous action queue: what should the agent do RIGHT NOW for this subject? | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/badbool.py` | source | Pull and parse the Big-Ass Data Broker Opt-Out List (BADBOOL) into broker records. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/brokers.py` | source | Load and query the broker database (references/brokers/*.json). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/cdp.py` | source | Launch (or detect) the operator's local Chrome/Chromium over the DevTools Protocol (CDP). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/config.py` | source | Install-wide configuration with easiest-first defaults. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/crypto.py` | source | At-rest encryption for sensitive files via the `age` binary (optional). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/dossier.py` | source | Subject dossier management + consent gate + least-disclosure field selection. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/email_modes.py` | source | Email modes A/B/C helpers + anti-phishing verification-link extraction. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/emailer.py` | source | Programmatic email (Mode B) via stdlib smtplib/imaplib - no human in the loop. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/ledger.py` | source | Case ledger: opt-out state machine + append-only audit log. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/legal.py` | source | Render opt-out / legal request text from templates/ with safe substitution. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/paths.py` | source | Filesystem paths for the unbroker skill (stdlib only). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/pdd.py` | source | unbroker - deterministic CLI helper. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/registry.py` | source | Ingest the California Data Broker Registry into broker records (coverage breadth). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/report.py` | source | Status dashboards, Markdown reports, human-task digest, and Google Sheets row export. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/scan.py` | source | Stdlib fetch helper for simple url_pattern brokers (osint-style). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/storage.py` | source | Storage helpers (stdlib only): atomic JSON, append-only JSONL, strict perms. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/tiers.py` | source | Automation-tier selection and per-subject action planning. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/scripts/vectors.py` | source | Enumerate the search queries to run per broker, across ALL of a subject's identifiers. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/security/unbroker/templates/consent/authorization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/unbroker/templates/emails/ccpa-authorized-agent.txt` | asset | File `ccpa-authorized-agent.txt` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/security/unbroker/templates/emails/ccpa-deletion.txt` | asset | File `ccpa-deletion.txt` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/security/unbroker/templates/emails/ccpa-indirect-deletion.txt` | asset | File `ccpa-indirect-deletion.txt` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/security/unbroker/templates/emails/gdpr-erasure.txt` | asset | File `gdpr-erasure.txt` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/security/unbroker/templates/emails/generic-optout.txt` | asset | File `generic-optout.txt` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/security/web-pentest/SKILL.md` | skill-doc | Skill definition for `web-pentest` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/security/web-pentest/references/bypass-techniques.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/web-pentest/references/exploitation-techniques.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/web-pentest/references/scope-enforcement.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/web-pentest/references/vuln-taxonomy.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/web-pentest/scripts/recon-scan.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `optional-skills/security/web-pentest/templates/authorization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/security/web-pentest/templates/exploitation-queue.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `optional-skills/security/web-pentest/templates/pentest-report.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/ast-grep/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/software-development/ast-grep/SKILL.md` | skill-doc | Skill definition for `ast-grep` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/software-development/ast-grep/install.ps1` | asset | File `install.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/software-development/ast-grep/install.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `optional-skills/software-development/ast-grep/references/cli.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/ast-grep/references/install.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/ast-grep/references/patterns.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/ast-grep/references/pitfalls.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/ast-grep/references/recipes.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/ast-grep/references/sgconfig.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/ast-grep/references/yaml-rules.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/ast-grep/scripts/ast_grep_helper.py` | source | ast-grep-helper: a thin LLM-friendly wrapper around `sg` (ast-grep). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/software-development/ast-grep/tests/smoke.ps1` | asset | File `smoke.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `optional-skills/software-development/ast-grep/tests/smoke.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `optional-skills/software-development/code-wiki/SKILL.md` | skill-doc | Skill definition for `code-wiki` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/software-development/code-wiki/templates/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `optional-skills/software-development/code-wiki/templates/architecture.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/code-wiki/templates/getting-started.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/code-wiki/templates/module.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/rest-graphql-debug/SKILL.md` | skill-doc | Skill definition for `rest-graphql-debug` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/software-development/subagent-driven-development/SKILL.md` | skill-doc | Skill definition for `subagent-driven-development` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/software-development/subagent-driven-development/references/context-budget-discipline.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/software-development/subagent-driven-development/references/gates-taxonomy.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/web-development/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `optional-skills/web-development/cloudflare-temporary-deploy/SKILL.md` | skill-doc | Skill definition for `cloudflare-temporary-deploy` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/web-development/cloudflare-temporary-deploy/scripts/parse_deploy_output.py` | source | Parse `wrangler deploy --temporary` output into structured JSON. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/web-development/har-derived-api-client/SKILL.md` | skill-doc | Skill definition for `har-derived-api-client` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/web-development/har-derived-api-client/scripts/har_capture.py` | source | Record a HAR file while driving a website with Playwright. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/web-development/har-derived-api-client/scripts/har_capture_cdp.py` | source | Capture a HAR from a browser you connect to over CDP (not one you launch). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/web-development/har-derived-api-client/scripts/har_to_client.py` | source | Distill a HAR file into an API summary an agent can turn into a client. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `optional-skills/web-development/page-agent/SKILL.md` | skill-doc | Skill definition for `page-agent` | The instruction contract a model loads when the skill's trigger matches |  |
| `optional-skills/yuanbao/SKILL.md` | skill-doc | Skill definition for `yuanbao` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/apple/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/apple/apple-notes/SKILL.md` | skill-doc | Skill definition for `apple-notes` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/apple/apple-reminders/SKILL.md` | skill-doc | Skill definition for `apple-reminders` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/apple/findmy/SKILL.md` | skill-doc | Skill definition for `findmy` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/apple/imessage/SKILL.md` | skill-doc | Skill definition for `imessage` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/autonomous-ai-agents/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/claude-code/SKILL.md` | skill-doc | Skill definition for `claude-code` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/autonomous-ai-agents/codex/SKILL.md` | skill-doc | Skill definition for `codex` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/autonomous-ai-agents/computer-use/SKILL.md` | skill-doc | Skill definition for `computer-use` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/autonomous-ai-agents/hermes-agent/SKILL.md` | skill-doc | Skill definition for `hermes-agent` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/autonomous-ai-agents/hermes-agent/references/background-systems.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/cli-reference.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/configuration.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/contributor-guide.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/delegate-task-concurrency-diagnosis.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/desktop-plugins.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/native-mcp.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/petdex.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/portal-auth-for-third-party-apps.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/project-context-files.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/providers-and-models.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/security-privacy.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/slash-commands.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/themes.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/tui-widgets.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/webhooks.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/references/windows-quirks.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/autonomous-ai-agents/hermes-agent/templates/clock.mjs` | asset | File `clock.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/autonomous-ai-agents/hermes-agent/templates/plugin.js` | asset | File `plugin.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/autonomous-ai-agents/hermes-agent/templates/skin.yaml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `skills/autonomous-ai-agents/merge-reconciler/SKILL.md` | skill-doc | Skill definition for `merge-reconciler` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/autonomous-ai-agents/opencode/SKILL.md` | skill-doc | Skill definition for `opencode` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/architecture-diagram/SKILL.md` | skill-doc | Skill definition for `architecture-diagram` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/architecture-diagram/templates/template.html` | asset | File `template.html` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/creative/ascii-art/SKILL.md` | skill-doc | Skill definition for `ascii-art` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/ascii-video/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/creative/ascii-video/SKILL.md` | skill-doc | Skill definition for `ascii-video` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/ascii-video/references/architecture.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/ascii-video/references/composition.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/ascii-video/references/effects.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/ascii-video/references/inputs.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/ascii-video/references/optimization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/ascii-video/references/scenes.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/ascii-video/references/shaders.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/ascii-video/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/PORT_NOTES.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/SKILL.md` | skill-doc | Skill definition for `baoyu-infographic` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/baoyu-infographic/references/analysis-framework.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/base-prompt.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/bento-grid.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/binary-comparison.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/bridge.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/circular-flow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/comic-strip.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/comparison-matrix.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/dashboard.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/dense-modules.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/funnel.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/hierarchical-layers.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/hub-spoke.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/iceberg.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/isometric-map.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/jigsaw.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/linear-progression.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/periodic-table.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/story-mountain.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/structural-breakdown.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/tree-branching.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/venn-diagram.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/layouts/winding-roadmap.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/structured-content-template.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/aged-academia.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/bold-graphic.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/chalkboard.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/claymation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/corporate-memphis.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/craft-handmade.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/cyberpunk-neon.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/hand-drawn-edu.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/ikea-manual.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/kawaii.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/knolling.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/lego-brick.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/morandi-journal.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/origami.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/pixel-art.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/pop-laboratory.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/retro-pop-grid.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/storybook-watercolor.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/subway-map.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/technical-schematic.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/baoyu-infographic/references/styles/ui-wireframe.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/claude-design/SKILL.md` | skill-doc | Skill definition for `claude-design` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/comfyui/SKILL.md` | skill-doc | Skill definition for `comfyui` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/comfyui/references/official-cli.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/comfyui/references/rest-api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/comfyui/references/template-integrity.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/comfyui/references/workflow-format.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/comfyui/scripts/_common.py` | source | _common.py — Shared logic for ComfyUI skill scripts. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/auto_fix_deps.py` | source | auto_fix_deps.py — Run check_deps.py, then attempt to install whatever is missing. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/check_deps.py` | source | check_deps.py — Verify a ComfyUI workflow's dependencies (custom nodes, models, | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/comfyui_setup.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `skills/creative/comfyui/scripts/extract_schema.py` | source | extract_schema.py — Analyze a ComfyUI API-format workflow and extract | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/fetch_logs.py` | source | fetch_logs.py — Retrieve workflow execution diagnostics from a ComfyUI server. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/hardware_check.py` | source | hardware_check.py — Detect whether this machine can realistically run ComfyUI locally. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/health_check.py` | source | health_check.py — One-stop verification that the ComfyUI environment is ready. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/run_batch.py` | source | run_batch.py — Run a workflow many times, varying parameters per run. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/run_workflow.py` | source | run_workflow.py — Inject parameters into a ComfyUI workflow, submit it, monitor | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/scripts/ws_monitor.py` | source | ws_monitor.py — Real-time ComfyUI WebSocket monitor. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/comfyui/tests/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/creative/comfyui/tests/conftest.py` | test | Pytest configuration for the comfyui skill test suite. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/creative/comfyui/tests/pytest.ini` | asset | File `pytest.ini` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/creative/comfyui/tests/test_check_deps.py` | test | Tests for check_deps.py — focuses on parsing logic that doesn't need a server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/creative/comfyui/tests/test_cloud_integration.py` | test | Integration tests against the live Comfy Cloud API. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/creative/comfyui/tests/test_common.py` | test | Unit tests for _common.py — pure logic only, no network. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/creative/comfyui/tests/test_extract_schema.py` | test | Tests for extract_schema.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/creative/comfyui/tests/test_run_workflow.py` | test | Tests for run_workflow.py — focuses on logic that doesn't require a server. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/creative/comfyui/workflows/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/creative/comfyui/workflows/animatediff_video.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/creative/comfyui/workflows/flux_dev_txt2img.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/creative/comfyui/workflows/sd15_txt2img.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/creative/comfyui/workflows/sdxl_img2img.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/creative/comfyui/workflows/sdxl_inpaint.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/creative/comfyui/workflows/sdxl_txt2img.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/creative/comfyui/workflows/upscale_4x.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/creative/comfyui/workflows/wan_video_t2v.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/creative/design-md/SKILL.md` | skill-doc | Skill definition for `design-md` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/design-md/templates/starter.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/excalidraw/SKILL.md` | skill-doc | Skill definition for `excalidraw` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/excalidraw/references/colors.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/excalidraw/references/dark-mode.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/excalidraw/references/examples.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/excalidraw/scripts/upload.py` | source | Upload an .excalidraw file to excalidraw.com and print a shareable URL. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/creative/humanizer/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/creative/humanizer/SKILL.md` | skill-doc | Skill definition for `humanizer` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/manim-video/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/creative/manim-video/SKILL.md` | skill-doc | Skill definition for `manim-video` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/manim-video/references/animation-design-thinking.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/animations.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/camera-and-3d.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/decorations.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/equations.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/graphs-and-data.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/mobjects.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/paper-explainer.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/production-quality.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/rendering.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/scene-planning.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/updaters-and-trackers.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/references/visual-design.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/manim-video/scripts/setup.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `skills/creative/p5js/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/creative/p5js/SKILL.md` | skill-doc | Skill definition for `p5js` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/p5js/references/animation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/color-systems.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/core-api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/export-pipeline.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/interaction.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/shapes-and-geometry.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/typography.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/visual-effects.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/references/webgl-and-3d.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/p5js/scripts/export-frames.js` | asset | File `export-frames.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/creative/p5js/scripts/render.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `skills/creative/p5js/scripts/serve.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `skills/creative/p5js/scripts/setup.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `skills/creative/p5js/templates/viewer.html` | asset | File `viewer.html` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/creative/popular-web-designs/SKILL.md` | skill-doc | Skill definition for `popular-web-designs` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/popular-web-designs/templates/airbnb.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/airtable.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/apple.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/bmw.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/cal.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/claude.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/clay.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/clickhouse.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/cohere.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/coinbase.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/composio.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/cursor.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/elevenlabs.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/expo.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/figma.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/framer.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/hashicorp.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/ibm.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/intercom.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/kraken.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/linear.app.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/lovable.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/minimax.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/mintlify.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/miro.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/mistral.ai.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/mongodb.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/notion.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/nvidia.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/ollama.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/opencode.ai.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/pinterest.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/posthog.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/raycast.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/replicate.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/resend.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/revolut.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/runwayml.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/sanity.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/sentry.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/spacex.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/spotify.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/stripe.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/supabase.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/superhuman.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/together.ai.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/uber.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/vercel.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/voltagent.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/warp.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/webflow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/wise.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/x.ai.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/popular-web-designs/templates/zapier.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/pretext/SKILL.md` | skill-doc | Skill definition for `pretext` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/pretext/references/patterns.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/pretext/templates/donut-orbit.html` | asset | File `donut-orbit.html` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/creative/pretext/templates/hello-orb-flow.html` | asset | File `hello-orb-flow.html` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/creative/sketch/SKILL.md` | skill-doc | Skill definition for `sketch` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/songwriting-and-ai-music/SKILL.md` | skill-doc | Skill definition for `songwriting-and-ai-music` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/touchdesigner-mcp/SKILL.md` | skill-doc | Skill definition for `touchdesigner-mcp` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/creative/touchdesigner-mcp/references/3d-scene.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/animation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/audio-reactive.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/dat-scripting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/external-data.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/geometry-comp.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/glsl.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/layout-compositor.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/mcp-tools.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/midi-osc.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/network-patterns.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/operator-tips.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/operators.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/panel-ui.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/particles.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/pitfalls.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/postfx.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/projection-mapping.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/python-api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/replicator.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/creative/touchdesigner-mcp/scripts/setup.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `skills/devops/sdlc-review/SKILL.md` | skill-doc | Skill definition for `sdlc-review` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/email/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/email/email-inbox-triage/SKILL.md` | skill-doc | Skill definition for `email-inbox-triage` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/email/himalaya/SKILL.md` | skill-doc | Skill definition for `himalaya` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/email/himalaya/references/configuration.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/email/himalaya/references/message-composition.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/codebase-inspection/SKILL.md` | skill-doc | Skill definition for `codebase-inspection` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/github/github-auth/SKILL.md` | skill-doc | Skill definition for `github-auth` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/github/github-auth/scripts/gh-env.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `skills/github/github-auth/scripts/git-credential-token.py` | source | Print the first unambiguous GitHub token in a git credential-store file. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/github/github-code-review/SKILL.md` | skill-doc | Skill definition for `github-code-review` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/github/github-code-review/references/review-output-template.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/github-issue-to-pr/SKILL.md` | skill-doc | Skill definition for `github-issue-to-pr` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/github/github-issues/SKILL.md` | skill-doc | Skill definition for `github-issues` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/github/github-issues/templates/bug-report.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/github-issues/templates/feature-request.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/github-pr-workflow/SKILL.md` | skill-doc | Skill definition for `github-pr-workflow` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/github/github-pr-workflow/references/ci-troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/github-pr-workflow/references/conventional-commits.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/github-pr-workflow/templates/pr-body-bugfix.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/github-pr-workflow/templates/pr-body-feature.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/github/github-repo-management/SKILL.md` | skill-doc | Skill definition for `github-repo-management` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/github/github-repo-management/references/github-api-cheatsheet.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/index-cache/anthropics_skills_skills_.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/index-cache/lobehub_index.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/index-cache/openai_skills_skills_.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `skills/media/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/media/gif-search/SKILL.md` | skill-doc | Skill definition for `gif-search` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/media/songsee/SKILL.md` | skill-doc | Skill definition for `songsee` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/media/youtube-content/SKILL.md` | skill-doc | Skill definition for `youtube-content` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/media/youtube-content/references/output-formats.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/media/youtube-content/scripts/fetch_transcript.py` | source | Fetch a YouTube video transcript and output it as structured JSON. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/mlops/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/evaluation/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/evaluation/evaluating-llms-harness/SKILL.md` | skill-doc | Skill definition for `evaluating-llms-harness` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/mlops/evaluation/evaluating-llms-harness/references/api-evaluation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/evaluation/evaluating-llms-harness/references/benchmark-guide.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/evaluation/evaluating-llms-harness/references/custom-tasks.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/evaluation/evaluating-llms-harness/references/distributed-eval.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/evaluation/weights-and-biases/SKILL.md` | skill-doc | Skill definition for `weights-and-biases` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/mlops/evaluation/weights-and-biases/references/artifacts.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/evaluation/weights-and-biases/references/integrations.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/evaluation/weights-and-biases/references/sweeps.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/huggingface-hub/SKILL.md` | skill-doc | Skill definition for `huggingface-hub` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/mlops/inference/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/llama-cpp/SKILL.md` | skill-doc | Skill definition for `llama-cpp` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/mlops/inference/llama-cpp/references/advanced-usage.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/llama-cpp/references/hub-discovery.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/llama-cpp/references/optimization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/llama-cpp/references/quantization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/llama-cpp/references/server.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/llama-cpp/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/serving-llms-vllm/SKILL.md` | skill-doc | Skill definition for `serving-llms-vllm` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/mlops/inference/serving-llms-vllm/references/optimization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/serving-llms-vllm/references/quantization.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/serving-llms-vllm/references/server-deployment.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/inference/serving-llms-vllm/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/mlops/models/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/note-taking/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/note-taking/obsidian/SKILL.md` | skill-doc | Skill definition for `obsidian` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/airtable/SKILL.md` | skill-doc | Skill definition for `airtable` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/box/SKILL.md` | skill-doc | Skill definition for `box` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/box/references/bulk-operations.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/cli-guide.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/content-workflows.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/hubs.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/oauth-setup.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/rest-api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/sdk-development.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/search-and-ai.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/troubleshooting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/box/references/webhooks-and-events.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/document-to-action-items/SKILL.md` | skill-doc | Skill definition for `document-to-action-items` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/docx/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/productivity/docx/SKILL.md` | skill-doc | Skill definition for `docx` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/docx/references/revisions-and-comments.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/docx/scripts/docx_comments.py` | source | List, add, and delete comments in a .docx. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/docx/scripts/docx_common.py` | source | Shared helpers: paragraph iteration and run-preserving text replacement. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/docx/scripts/docx_create.py` | source | Create a .docx document from a JSON spec. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/docx/scripts/docx_edit.py` | source | Edit an existing .docx in place (or to a new file). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/docx/scripts/docx_read.py` | source | Read a .docx: text, structure outline, styles, images, revision detection. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/docx/scripts/docx_revisions.py` | source | Inspect and resolve tracked changes (w:ins / w:del) in a .docx. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/docx/scripts/docx_template.py` | source | Fill {{placeholder}} tokens in a .docx from a JSON mapping. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/docx/scripts/docx_validate.py` | source | Health-check a .docx package and report issues as JSON. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/docx/tests/test_docx_skill.py` | test | Pytest suite proving create / read / edit / template round-trips. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/productivity/google-workspace/SKILL.md` | skill-doc | Skill definition for `google-workspace` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/google-workspace/references/daily-brief.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/google-workspace/references/gmail-search-syntax.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/google-workspace/scripts/_hermes_home.py` | source | Resolve HERMES_HOME for standalone skill scripts. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/google-workspace/scripts/google_api.py` | source | Google Workspace API CLI for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/google-workspace/scripts/gws_bridge.py` | source | Bridge between Hermes OAuth token and gws CLI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/google-workspace/scripts/setup.py` | build | Legacy setup shim | Compatibility entrypoint delegating to pyproject |  |
| `skills/productivity/maps/SKILL.md` | skill-doc | Skill definition for `maps` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/maps/scripts/maps_client.py` | source | maps_client.py - CLI tool for maps, geocoding, routing, POI search, and more. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/meeting-action-items/SKILL.md` | skill-doc | Skill definition for `meeting-action-items` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/nano-pdf/SKILL.md` | skill-doc | Skill definition for `nano-pdf` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/notion/SKILL.md` | skill-doc | Skill definition for `notion` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/notion/references/block-types.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/ocr-and-documents/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/ocr-and-documents/SKILL.md` | skill-doc | Skill definition for `ocr-and-documents` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/ocr-and-documents/scripts/extract_marker.py` | source | Extract text from documents using marker-pdf. High-quality OCR + layout analysis. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/ocr-and-documents/scripts/extract_pymupdf.py` | source | Extract text from documents using pymupdf. Lightweight (~25MB), no models. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/productivity/pdf/SKILL.md` | skill-doc | Skill definition for `pdf` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/pdf/references/forms.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/pdf/scripts/_raster.py` | source | Shared page rasterizer with a fallback chain: pypdfium2 -> pdftoppm. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_create.py` | source | Create a PDF from a JSON spec using reportlab platypus. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_fill_form.py` | source | Fill AcroForm fields from a UTF-8 JSON file; optionally flatten. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_form_layout.py` | source | Validate a form-spec layout BEFORE building the PDF, with optional | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_make_form.py` | source | Create a fillable AcroForm PDF from a JSON spec (reportlab canvas.acroForm). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_merge.py` | source | Merge multiple PDFs into one, optionally adding a bookmark per source file. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_meta.py` | source | Document metadata and file attachments for PDFs (pypdf). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_page_image.py` | source | Export PDF pages as PNG images at a chosen DPI. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_read.py` | source | Read a PDF: per-page text, tables, metadata, or form fields. JSON to stdout. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_secure.py` | source | Encrypt or decrypt a PDF with passwords (AES-256 via pypdf). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_split.py` | source | Extract page ranges from a PDF, optionally rotating and/or compressing pages. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_stamp.py` | source | Stamp text or an image at coordinates onto selected PDF pages. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/scripts/pdf_watermark.py` | source | Stamp/watermark every page of a PDF with page 1 of another PDF. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/pdf/tests/test_pdf_skill.py` | test | End-to-end tests for the pdf skill helper scripts. No network required. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/productivity/powerpoint/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/productivity/powerpoint/SKILL.md` | skill-doc | Skill definition for `powerpoint` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/powerpoint/scripts/pptx_create.py` | source | Create a .pptx presentation from a JSON deck spec. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/powerpoint/scripts/pptx_edit.py` | source | Edit a .pptx in place (or save to --output). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/powerpoint/scripts/pptx_from_template.py` | source | Build a deck from a .pptx template (brand deck) and fill placeholders. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/powerpoint/scripts/pptx_read.py` | source | Read a .pptx file: JSON outline, notes, or export embedded images. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/powerpoint/scripts/pptx_render.py` | source | Render every slide of a .pptx to per-slide PNG images. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/powerpoint/tests/test_powerpoint_skill.py` | test | End-to-end tests for the powerpoint skill helper scripts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/productivity/product-price-monitor/SKILL.md` | skill-doc | Skill definition for `product-price-monitor` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/session-librarian/SKILL.md` | skill-doc | Skill definition for `session-librarian` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/teams-meeting-pipeline/SKILL.md` | skill-doc | Skill definition for `teams-meeting-pipeline` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/weekly-review-planning/SKILL.md` | skill-doc | Skill definition for `weekly-review-planning` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/xlsx/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/productivity/xlsx/SKILL.md` | skill-doc | Skill definition for `xlsx` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/productivity/xlsx/references/restructuring.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/productivity/xlsx/scripts/csv_to_xlsx.py` | source | Convert a CSV file to a styled .xlsx workbook with type inference. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/xlsx/scripts/xlsx_create.py` | source | Create an .xlsx workbook from a JSON spec. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/xlsx/scripts/xlsx_edit.py` | source | Edit an existing .xlsx workbook in place (or to --out). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/xlsx/scripts/xlsx_read.py` | source | Read an .xlsx workbook: inventory, JSON/CSV dumps, formula listing. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/xlsx/scripts/xlsx_recalc.py` | source | Recalculate a workbook's formulas headlessly with LibreOffice. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/xlsx/scripts/xlsx_restructure.py` | source | Reference-aware row/column insert and delete for .xlsx workbooks. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/xlsx/scripts/xlsx_to_csv.py` | source | Export one sheet of an .xlsx workbook to CSV. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/productivity/xlsx/tests/test_xlsx_skill.py` | test | End-to-end tests for the xlsx skill helper scripts. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `skills/research/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/arxiv/SKILL.md` | skill-doc | Skill definition for `arxiv` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/research/arxiv/scripts/search_arxiv.py` | source | Search arXiv and display results in a clean format. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/research/blocked-page-recovery/SKILL.md` | skill-doc | Skill definition for `blocked-page-recovery` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/research/blocked-page-recovery/scripts/recover_page.py` | source | Recover a blocked / paywalled / WAF'd page from third-party copies. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/research/blogwatcher/SKILL.md` | skill-doc | Skill definition for `blogwatcher` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/research/competitor-news-monitor/SKILL.md` | skill-doc | Skill definition for `competitor-news-monitor` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/research/grounded-citations/SKILL.md` | skill-doc | Skill definition for `grounded-citations` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/research/grounded-citations/references/citation-formats.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/grounded-citations/references/grounding-rationale.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/grounded-citations/scripts/_hermes_home.py` | source | Resolve HERMES_HOME for standalone skill scripts. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/research/grounded-citations/scripts/sources.py` | source | Citation ledger for grounded answers and documents. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `skills/research/llm-wiki/SKILL.md` | skill-doc | Skill definition for `llm-wiki` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/research/research-paper-writing/SKILL.md` | skill-doc | Skill definition for `research-paper-writing` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/research/research-paper-writing/references/autoreason-methodology.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/checklists.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/citation-workflow.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/experiment-patterns.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/human-evaluation.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/paper-types.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/phase5-paper-drafting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/reviewer-guidelines.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/sources.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/references/writing-guide.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/templates/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/research/research-paper-writing/templates/aaai2026/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/research/research-paper-writing/templates/aaai2026/aaai2026-unified-supp.tex` | asset | File `aaai2026-unified-supp.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/aaai2026/aaai2026-unified-template.tex` | asset | File `aaai2026-unified-template.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/aaai2026/aaai2026.bib` | asset | File `aaai2026.bib` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/aaai2026/aaai2026.bst` | asset | File `aaai2026.bst` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/aaai2026/aaai2026.sty` | asset | File `aaai2026.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/acl/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/research/research-paper-writing/templates/acl/acl.sty` | asset | File `acl.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/acl/acl_latex.tex` | asset | File `acl_latex.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/acl/acl_lualatex.tex` | asset | File `acl_lualatex.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/acl/acl_natbib.bst` | asset | File `acl_natbib.bst` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/acl/anthology.bib.txt` | asset | File `anthology.bib.txt` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/acl/custom.bib` | asset | File `custom.bib` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/acl/formatting.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/research/research-paper-writing/templates/colm2025/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `skills/research/research-paper-writing/templates/colm2025/colm2025_conference.bib` | asset | File `colm2025_conference.bib` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/colm2025/colm2025_conference.bst` | asset | File `colm2025_conference.bst` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/colm2025/colm2025_conference.pdf` | asset | File `colm2025_conference.pdf` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/colm2025/colm2025_conference.sty` | asset | File `colm2025_conference.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/colm2025/colm2025_conference.tex` | asset | File `colm2025_conference.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/colm2025/fancyhdr.sty` | asset | File `fancyhdr.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/colm2025/math_commands.tex` | asset | File `math_commands.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/colm2025/natbib.sty` | asset | File `natbib.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/iclr2026/fancyhdr.sty` | asset | File `fancyhdr.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/iclr2026/iclr2026_conference.bib` | asset | File `iclr2026_conference.bib` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/iclr2026/iclr2026_conference.bst` | asset | File `iclr2026_conference.bst` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/iclr2026/iclr2026_conference.pdf` | asset | File `iclr2026_conference.pdf` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/iclr2026/iclr2026_conference.sty` | asset | File `iclr2026_conference.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/iclr2026/iclr2026_conference.tex` | asset | File `iclr2026_conference.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/iclr2026/math_commands.tex` | asset | File `math_commands.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/iclr2026/natbib.sty` | asset | File `natbib.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/algorithm.sty` | asset | File `algorithm.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/algorithmic.sty` | asset | File `algorithmic.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/example_paper.bib` | asset | File `example_paper.bib` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/example_paper.pdf` | asset | File `example_paper.pdf` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/example_paper.tex` | asset | File `example_paper.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/fancyhdr.sty` | asset | File `fancyhdr.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/icml2026.bst` | asset | File `icml2026.bst` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/icml2026.sty` | asset | File `icml2026.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/icml2026/icml_numpapers.pdf` | asset | File `icml_numpapers.pdf` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/neurips2025/Makefile` | asset | File `Makefile` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/neurips2025/extra_pkgs.tex` | asset | File `extra_pkgs.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/neurips2025/main.tex` | asset | File `main.tex` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/research/research-paper-writing/templates/neurips2025/neurips.sty` | asset | File `neurips.sty` | Repository content; see related files / area page for the enclosing subsystem |  |
| `skills/smart-home/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/smart-home/openhue/SKILL.md` | skill-doc | Skill definition for `openhue` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/social-media/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/social-media/xurl/SKILL.md` | skill-doc | Skill definition for `xurl` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/dogfood/SKILL.md` | skill-doc | Skill definition for `dogfood` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/dogfood/references/issue-taxonomy.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/software-development/dogfood/templates/dogfood-report-template.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `skills/software-development/hermes-agent-skill-authoring/SKILL.md` | skill-doc | Skill definition for `hermes-agent-skill-authoring` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/inspecting-hermes-desktop-dom/SKILL.md` | skill-doc | Skill definition for `inspecting-hermes-desktop-dom` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/node-inspect-debugger/SKILL.md` | skill-doc | Skill definition for `node-inspect-debugger` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/plan/SKILL.md` | skill-doc | Skill definition for `plan` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/python-debugpy/SKILL.md` | skill-doc | Skill definition for `python-debugpy` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/requesting-code-review/SKILL.md` | skill-doc | Skill definition for `requesting-code-review` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/simplify-code/SKILL.md` | skill-doc | Skill definition for `simplify-code` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/spike/SKILL.md` | skill-doc | Skill definition for `spike` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/systematic-debugging/SKILL.md` | skill-doc | Skill definition for `systematic-debugging` | The instruction contract a model loads when the skill's trigger matches |  |
| `skills/software-development/test-driven-development/SKILL.md` | skill-doc | Skill definition for `test-driven-development` | The instruction contract a model loads when the skill's trigger matches |  |
