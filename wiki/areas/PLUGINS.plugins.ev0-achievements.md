# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/ev0-achievements/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/ev0-achievements/LICENSE` | asset | File `LICENSE` | Repository content; see related files / area page for the enclosing subsystem | plugins/ev0-achievements/README.md; plugins/ev0-achievements/dashboard/dist/index.js; plugins/ev0-achievements/dashboard/dist/style.css; plugins/ev0-achievements/dashboard/manifest.json |
| `plugins/ev0-achievements/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | plugins/ev0-achievements/LICENSE; plugins/ev0-achievements/dashboard/dist/index.js; plugins/ev0-achievements/dashboard/dist/style.css; plugins/ev0-achievements/dashboard/manifest.json |
| `plugins/ev0-achievements/dashboard/dist/index.js` | js-module | JS module `index.js` | Node/Electron JS source executed by the build/runtime; check git intent before deleting | plugins/ev0-achievements/dashboard/dist/style.css |
| `plugins/ev0-achievements/dashboard/dist/style.css` | asset | Stylesheet | Styling for a frontend surface | plugins/ev0-achievements/dashboard/dist/index.js |
| `plugins/ev0-achievements/dashboard/manifest.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | plugins/ev0-achievements/dashboard/dist/index.js; plugins/ev0-achievements/dashboard/dist/style.css; plugins/ev0-achievements/dashboard/plugin_api.py |
| `plugins/ev0-achievements/dashboard/plugin_api.py` | source | 3V0 Achievements dashboard plugin backend. | Python module executed or imported by the runtime; check git intent before deleting | plugins/ev0-achievements/dashboard/dist/index.js; plugins/ev0-achievements/dashboard/dist/style.css; plugins/ev0-achievements/dashboard/manifest.json |
| `plugins/ev0-achievements/docs/assets/achievements-dashboard-hd.png` | asset | Image asset | Static media referenced by docs or frontend | plugins/ev0-achievements/docs/assets/achievements-tier-showcase-hd.png |
| `plugins/ev0-achievements/docs/assets/achievements-tier-showcase-hd.png` | asset | Image asset | Static media referenced by docs or frontend | plugins/ev0-achievements/docs/assets/achievements-dashboard-hd.png |
| `plugins/ev0-achievements/tests/test_achievement_engine.py` | test | Tests `plugins/ev0-achievements/tests/test_achievement_engine.py` — see related for the module under test | Test module — asserts the repo contract; run via scripts/run_tests.sh | plugins/ev0-achievements/tests/ |
