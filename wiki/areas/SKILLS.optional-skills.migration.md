# skills/ + optional-skills/ — the skill libraries — `optional-skills/migration/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `optional-skills/migration/DESCRIPTION.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer | optional-skills/migration/openclaw-migration/SKILL.md; optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py |
| `optional-skills/migration/openclaw-migration/SKILL.md` | skill-doc | Skill definition for `openclaw-migration` | The instruction contract a model loads when the skill's trigger matches | optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py |
| `optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py` | source | OpenClaw -> Hermes migration helper. | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/migration/openclaw-migration/scripts/ |
