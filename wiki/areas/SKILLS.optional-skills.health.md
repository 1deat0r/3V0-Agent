# skills/ + optional-skills/ — the skill libraries — `optional-skills/health/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `optional-skills/health/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer | optional-skills/health/fitness-nutrition/SKILL.md; optional-skills/health/fitness-nutrition/references/FORMULAS.md; optional-skills/health/fitness-nutrition/scripts/body_calc.py |
| `optional-skills/health/fitness-nutrition/SKILL.md` | skill-doc | Skill definition for `fitness-nutrition` | The instruction contract a model loads when the skill's trigger matches | optional-skills/health/fitness-nutrition/references/FORMULAS.md; optional-skills/health/fitness-nutrition/scripts/body_calc.py; optional-skills/health/fitness-nutrition/scripts/nutrition_search.py |
| `optional-skills/health/fitness-nutrition/references/FORMULAS.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer | optional-skills/health/fitness-nutrition/references/ |
| `optional-skills/health/fitness-nutrition/scripts/body_calc.py` | source | body_calc.py — All-in-one fitness calculator. | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/health/fitness-nutrition/scripts/nutrition_search.py |
| `optional-skills/health/fitness-nutrition/scripts/nutrition_search.py` | source | nutrition_search.py — Search USDA FoodData Central for nutrition info. | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/health/fitness-nutrition/scripts/body_calc.py |
| `optional-skills/health/neuroskill-bci/SKILL.md` | skill-doc | Skill definition for `neuroskill-bci` | The instruction contract a model loads when the skill's trigger matches | optional-skills/health/neuroskill-bci/references/api.md; optional-skills/health/neuroskill-bci/references/metrics.md; optional-skills/health/neuroskill-bci/references/protocols.md |
| `optional-skills/health/neuroskill-bci/references/api.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer | optional-skills/health/neuroskill-bci/references/metrics.md; optional-skills/health/neuroskill-bci/references/protocols.md |
| `optional-skills/health/neuroskill-bci/references/metrics.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer | optional-skills/health/neuroskill-bci/references/api.md; optional-skills/health/neuroskill-bci/references/protocols.md |
| `optional-skills/health/neuroskill-bci/references/protocols.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer | optional-skills/health/neuroskill-bci/references/api.md; optional-skills/health/neuroskill-bci/references/metrics.md |
