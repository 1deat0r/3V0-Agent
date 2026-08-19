# cron/ — scheduled jobs

Scheduled jobs: store (`jobs.py`), scheduler tick (lock-guarded, hard 3-min interrupt), provider backends, execution ledger, suggestions, blueprint catalog. Agent schedules via the `cronjob` tool; users via `hermes cron` or `/cron`.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `cron/__init__.py` | source | Cron job scheduling system for Hermes Agent. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `cron/blueprint_catalog.py` | source | Blueprint jobs catalog (well-known scheduled tasks) | One-shot canonical jobs | 4: cron/scheduler.py;cron/jobs.py |
| `cron/executions.py` | source | Execution ledger for cron runs | Audit of what fired | run: cron/monitor.py |
| `cron/jobs.py` | source | Job store — SQLite-backed cron jobs (schedules, skills, context_from, workdir) | The agent's own scheduler; 3-minute hard interrupt invariant | ev0_cli/cron.py;tools/cronjob_tools.py |
| `cron/lifecycle_guard.py` | source | Cron job lifecycle guards (pause/resume rules) | Policy enforcement | : cron/jobs.py;ev0_cli/cron.py |
| `cron/monitor.py` | source | Cron monitoring surfaces | Observability for jobs | cron/executions.py |
| `cron/notepad.py` | source | Cron notepad — per-job notes | Context persistence | for jobs: cron/jobs.py |
| `cron/scheduler.py` | source | Scheduler tick loop (lock-guarded) | Runs inside the gateway process; .tick.lock prevents duplicates | cron/jobs.py |
| `cron/scheduler_provider.py` | source | Pluggable scheduler backends (system/provider cron) | Alternative runtimes: system cron, managed providers | cron/scheduler.py;plugins/cron_providers/ |
| `cron/scripts/__init__.py` | source | Scripts shipped with the cron subsystem (runnable via ``python3 -m cron.scripts.<name>``). | Python module executed or imported by the runtime; check git intent before deleting |  |
| `cron/scripts/classify_items.py` | source | Classify candidate items by urgency/importance and emit only the urgent ones. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `cron/suggestion_catalog.py` | source | Curated catalog of starter cron-job suggestions. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `cron/suggestions.py` | source | Cron job suggestions (natural-language->schedule) | UX helper | for: cron/suggestion_catalog.py |
