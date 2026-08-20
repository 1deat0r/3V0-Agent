# ev0_cli/ + cli.py — interactive CLI, config, skins, subcommands

The interactive CLI (`cli.py`), its config contract (`ev0_cli/config.py` — non-secrets live in config.yaml, not .env), the central slash-command registry (`ev0_cli/commands.py`), skins, curses pickers, and the dashboard server (`web_server.py` + `pty_bridge.py` embedding 3v0 --tui).
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
