# cron/ — scheduled jobs

Scheduled jobs: store (`jobs.py`), scheduler tick (lock-guarded, hard 3-min interrupt), provider backends, execution ledger, suggestions, blueprint catalog. Agent schedules via the `cronjob` tool; users via `3v0 cron` or `/cron`.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `cron/__init__.py` | source | Cron job scheduling system for 3V0 Agent. | Python module executed or imported by the runtime; check git intent before deleting | cron/blueprint_catalog.py; cron/executions.py; cron/jobs.py; cron/lifecycle_guard.py; cron/monitor.py; cron/notepad.py; cron/scheduler.py; cron/scheduler_provider.py; cron/scripts/__init__.py |
| `cron/blueprint_catalog.py` | source | Blueprint jobs catalog (well-known scheduled tasks) | One-shot canonical jobs | cron/jobs.py |
| `cron/executions.py` | source | Audit of what fired | Records cron executions for the scheduler's audit trail | cron/scheduler.py; cron/jobs.py; gateway/run.py |
| `cron/jobs.py` | source | Job store — SQLite-backed cron jobs (schedules, skills, context_from, workdir) | The agent's own scheduler; 3-minute hard interrupt invariant | threev0_cli/cron.py; tools/cronjob_tools.py |
| `cron/lifecycle_guard.py` | source | Cron job lifecycle guards (pause/resume rules) | Policy enforcement | threev0_cli/cron.py |
| `cron/monitor.py` | source | Cron monitoring surfaces | Observability for jobs | cron/executions.py |
| `cron/notepad.py` | source | Context persistence | Persists scratch context for cron jobs across runs | cron/scheduler.py; agent/memory_manager.py |
| `cron/scheduler.py` | source | Scheduler tick loop (lock-guarded) | Runs inside the gateway process; .tick.lock prevents duplicates | cron/jobs.py |
| `cron/scheduler_provider.py` | source | Pluggable scheduler backends (system/provider cron) | Alternative runtimes: system cron, managed providers | cron/scheduler.py; plugins/cron_providers/ |
| `cron/scripts/__init__.py` | source | Scripts shipped with the cron subsystem (runnable via ``python3 -m cron.scripts.<name>``). | Python module executed or imported by the runtime; check git intent before deleting | cron/scripts/classify_items.py |
| `cron/scripts/classify_items.py` | source | Classify candidate items by urgency/importance and emit only the urgent ones. | Python module executed or imported by the runtime; check git intent before deleting | cron/scripts/__init__.py |
| `cron/suggestion_catalog.py` | source | Curated catalog of starter cron-job suggestions. | Python module executed or imported by the runtime; check git intent before deleting | cron/__init__.py; cron/blueprint_catalog.py; cron/executions.py; cron/jobs.py; cron/lifecycle_guard.py; cron/monitor.py; cron/notepad.py; cron/scheduler.py; cron/scheduler_provider.py |
| `cron/suggestions.py` | source | UX helper | Builds suggested cron-job prompts for interactive setup | cron/scheduler.py; gateway/slash_commands.py |
