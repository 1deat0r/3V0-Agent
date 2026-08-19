# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/hermes-achievements/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/hermes-achievements/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem | plugins/hermes-achievements/README.md; plugins/hermes-achievements/dashboard/dist/index.js; plugins/hermes-achievements/dashboard/dist/style.css; plugins/hermes-achievements/dashboard/manifest.json |
| `plugins/hermes-achievements/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | plugins/hermes-achievements/LICENSE; plugins/hermes-achievements/dashboard/dist/index.js; plugins/hermes-achievements/dashboard/dist/style.css; plugins/hermes-achievements/dashboard/manifest.json |
| `plugins/hermes-achievements/dashboard/dist/index.js` | asset | File `index.js` | Repository content; see related files / area page for the enclosing subsystem | plugins/hermes-achievements/dashboard/dist/style.css |
| `plugins/hermes-achievements/dashboard/dist/style.css` | asset | Stylesheet | Styling for a frontend surface | plugins/hermes-achievements/dashboard/dist/index.js |
| `plugins/hermes-achievements/dashboard/manifest.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | plugins/hermes-achievements/dashboard/dist/index.js; plugins/hermes-achievements/dashboard/dist/style.css; plugins/hermes-achievements/dashboard/plugin_api.py |
| `plugins/hermes-achievements/dashboard/plugin_api.py` | source | Hermes Achievements dashboard plugin backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/hermes-achievements/dashboard/dist/index.js; plugins/hermes-achievements/dashboard/dist/style.css; plugins/hermes-achievements/dashboard/manifest.json |
| `plugins/hermes-achievements/docs/assets/achievements-dashboard-hd.png` | asset | Image asset | Static media referenced by docs or frontend | plugins/hermes-achievements/docs/assets/achievements-tier-showcase-hd.png |
| `plugins/hermes-achievements/docs/assets/achievements-tier-showcase-hd.png` | asset | Image asset | Static media referenced by docs or frontend | plugins/hermes-achievements/docs/assets/achievements-dashboard-hd.png |
| `plugins/hermes-achievements/tests/test_achievement_engine.py` | test | Python module `test_achievement_engine.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh | plugins/hermes-achievements/tests/ |
