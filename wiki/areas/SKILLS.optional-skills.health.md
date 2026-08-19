# skills/ + optional-skills/ — the skill libraries — `optional-skills/health/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `optional-skills/health/DESCRIPTION.md` | doc | Health, wellness, and biometric integration skills — BCI wearables, neurofeedback, sleep tracking, and cognitive state monitoring. | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/health/fitness-nutrition/SKILL.md; optional-skills/health/fitness-nutrition/references/FORMULAS.md; optional-skills/health/fitness-nutrition/scripts/body_calc.py |
| `optional-skills/health/fitness-nutrition/SKILL.md` | skill-doc | Skill definition for `fitness-nutrition` | The instruction contract a model loads when the skill's trigger matches | optional-skills/health/fitness-nutrition/references/FORMULAS.md; optional-skills/health/fitness-nutrition/scripts/body_calc.py; optional-skills/health/fitness-nutrition/scripts/nutrition_search.py |
| `optional-skills/health/fitness-nutrition/references/FORMULAS.md` | doc | Formulas Reference | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/health/fitness-nutrition/references/ |
| `optional-skills/health/fitness-nutrition/scripts/body_calc.py` | source | body_calc.py — All-in-one fitness calculator. | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/health/fitness-nutrition/scripts/nutrition_search.py |
| `optional-skills/health/fitness-nutrition/scripts/nutrition_search.py` | source | nutrition_search.py — Search USDA FoodData Central for nutrition info. | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/health/fitness-nutrition/scripts/body_calc.py |
| `optional-skills/health/neuroskill-bci/SKILL.md` | skill-doc | Skill definition for `neuroskill-bci` | The instruction contract a model loads when the skill's trigger matches | optional-skills/health/neuroskill-bci/references/api.md; optional-skills/health/neuroskill-bci/references/metrics.md; optional-skills/health/neuroskill-bci/references/protocols.md |
| `optional-skills/health/neuroskill-bci/references/api.md` | doc | NeuroSkill WebSocket & HTTP API Reference | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/health/neuroskill-bci/references/metrics.md; optional-skills/health/neuroskill-bci/references/protocols.md |
| `optional-skills/health/neuroskill-bci/references/metrics.md` | doc | NeuroSkill Metric Definitions & Interpretation Guide | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/health/neuroskill-bci/references/api.md; optional-skills/health/neuroskill-bci/references/protocols.md |
| `optional-skills/health/neuroskill-bci/references/protocols.md` | doc | NeuroSkill Guided Protocols | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/health/neuroskill-bci/references/api.md; optional-skills/health/neuroskill-bci/references/metrics.md |
