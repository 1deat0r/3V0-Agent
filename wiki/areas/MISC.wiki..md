# locales/ assets/ contributors/ — auxiliary content — `wiki//`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `wiki/README.md` | doc | One-paragraph orientation to the wiki | Fast entry for humans | wiki/index.md |
| `wiki/REVIEW-2026-08-20.md` | doc | Independent Wiki Review — 2026-08-20 | Human/agent-readable documentation; the wiki keeps it pointer-capped | wiki/README.md; wiki/SCHEMA.md; wiki/areas/AGENT.md; wiki/areas/APPS.apps.bootstrap-installer.md; wiki/areas/APPS.apps.desktop.md; wiki/areas/APPS.apps.shared.md; wiki/areas/APPS.md; wiki/areas/CLI.md |
| `wiki/SCHEMA.md` | doc | The wiki maintenance contract — invariant, artifacts, workflow, failure modes | Defines what must stay true for the index to be trusted | scripts/build_wiki.py;.githooks/pre-commit |
| `wiki/curated.tsv` | data | Hand-curated overlay — manual rows merged on --rebuild | Where hand-written entries live (never clobbered); 6 cols/row | scripts/build_wiki.py;wiki/manifest.tsv |
| `wiki/index.md` | doc | Master catalog + reading order for the LLM wiki | The first file an agent reads to map the repo | wiki/SCHEMA.md;wiki/areas/ |
| `wiki/log.md` | doc | Append-only change log for the wiki itself | Audit trail of wiki schema/coverage changes | wiki/SCHEMA.md |
| `wiki/manifest.tsv` | data | Raw 100%-coverage catalog — 6-col TSV rows for every tracked path | The generated artifact --check verifies; commit it | scripts/build_wiki.py;wiki/index.md |
