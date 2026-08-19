# Repository root — load-bearing core entrypoints

The waist of the system. `run_agent.py` is the conversation loop, `cli.py` the interactive shell, `model_tools.py`+`toolsets.py` the tool orchestration, `ev0_state*.py` the session store, `ev0_constants.py`/`ev0_logging.py` the profile-aware paths. Start here to trace any feature end-to-end.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `batch_runner.py` | source | Parallel batch task runner driving many AIAgent sessions | Runs offline jobs/campaigns against the same core loop without a live TTY | run_agent.py;tests/run_agent |
| `cli.py` | source | HermesCLI — interactive CLI orchestrator (prompt_toolkit + Rich), slash commands, session management | The primary human-facing surface; hosts command dispatch and config loading | for shell_commands: ev0_cli/commands.py;ev0_cli/config.py;ev0_cli/main.py;run_agent.py |
| `run_agent.py` | source | AIAgent class — the core synchronous conversation loop (model calls, tool dispatch, budget, interrupts) | Everything talks to a model through this loop; the narrow waist of the whole system | model_tools.py;cli.py;agent/conversation_loop.py;agent/prompt_builder.py |
| `trajectory_compressor.py` | source | Context compression / trajectory compaction service for long conversations | Prevents prompt-cache breakage and context overflow on long sessions; the one allowed mid-conversation context mutation | agent/context_compressor.py;agent/native_compaction.py;agent/conversation_compression.py |
| `utils.py` | source | Shared utilities (paths, JSON, file atomics, misc helpers) | Common helpers used repo-wide; keep dependency-free | ev0_constants.py;ev0_logging.py |
