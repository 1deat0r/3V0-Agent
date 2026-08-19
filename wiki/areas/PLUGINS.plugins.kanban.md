# plugins/ — plugin ecosystem (memory, providers, tools) — `plugins/kanban/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `plugins/kanban/dashboard/dist/index.js` | js-module | JS module `index.js` | Node/Electron JS source executed by the build/runtime; check git intent before deleting | plugins/kanban/dashboard/dist/style.css |
| `plugins/kanban/dashboard/dist/style.css` | asset | Stylesheet | Styling for a frontend surface | plugins/kanban/dashboard/dist/index.js |
| `plugins/kanban/dashboard/manifest.json` | config | Structured data/config file | Persistent state or declarative config read by tooling | plugins/kanban/dashboard/dist/index.js; plugins/kanban/dashboard/dist/style.css; plugins/kanban/dashboard/plugin_api.py |
| `plugins/kanban/dashboard/plugin_api.py` | source | Kanban dashboard plugin — backend API routes. | Python module executed or imported by the runtime; check git intent before deleting | plugins/kanban/dashboard/dist/index.js; plugins/kanban/dashboard/dist/style.css; plugins/kanban/dashboard/manifest.json |
| `plugins/kanban/systemd/3v0-kanban-dispatcher.service` | asset | File `3v0-kanban-dispatcher.service` | Repository content; see related files / area page for the enclosing subsystem | plugins/kanban/systemd/ |
