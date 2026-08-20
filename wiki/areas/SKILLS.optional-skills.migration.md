# skills/ + optional-skills/ — the skill libraries — `optional-skills/migration/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `optional-skills/migration/DESCRIPTION.md` | doc | Optional migration workflows for importing user state and customizations from | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/migration/openclaw-migration/SKILL.md; optional-skills/migration/openclaw-migration/scripts/openclaw_to_ev0.py |
| `optional-skills/migration/openclaw-migration/SKILL.md` | skill-doc | Skill definition for `openclaw-migration` | The instruction contract a model loads when the skill's trigger matches | optional-skills/migration/openclaw-migration/scripts/openclaw_to_ev0.py |
| `optional-skills/migration/openclaw-migration/scripts/openclaw_to_ev0.py` | source | OpenClaw -> 3V0 migration helper. | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/migration/openclaw-migration/scripts/ |
