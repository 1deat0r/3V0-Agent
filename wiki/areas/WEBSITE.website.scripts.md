# website/ — Docusaurus docs site — `website/scripts/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `website/scripts/extract-automation-blueprints.py` | source | Generate the Automation Blueprints catalog JSON for the docs site. | Python module executed or imported by the runtime; check git intent before deleting | website/scripts/extract-skills.py; website/scripts/generate-llms-txt.py; website/scripts/generate-skill-docs.py; website/scripts/prebuild.mjs |
| `website/scripts/extract-skills.py` | source | Extract skill metadata into website/static/api/skills.json for the Skills Hub page. | Python module executed or imported by the runtime; check git intent before deleting | website/scripts/extract-automation-blueprints.py; website/scripts/generate-llms-txt.py; website/scripts/generate-skill-docs.py; website/scripts/prebuild.mjs |
| `website/scripts/generate-llms-txt.py` | source | Generate llms.txt and llms-full.txt for the Hermes docs site. | Python module executed or imported by the runtime; check git intent before deleting | website/scripts/extract-automation-blueprints.py; website/scripts/extract-skills.py; website/scripts/generate-skill-docs.py; website/scripts/prebuild.mjs |
| `website/scripts/generate-skill-docs.py` | source | Generate per-skill Docusaurus pages from skills/ and optional-skills/ SKILL.md files. | Python module executed or imported by the runtime; check git intent before deleting | website/scripts/extract-automation-blueprints.py; website/scripts/extract-skills.py; website/scripts/generate-llms-txt.py; website/scripts/prebuild.mjs |
| `website/scripts/prebuild.mjs` | asset | File `prebuild.mjs` | Repository content; see related files / area page for the enclosing subsystem | website/scripts/extract-automation-blueprints.py; website/scripts/extract-skills.py; website/scripts/generate-llms-txt.py; website/scripts/generate-skill-docs.py |
