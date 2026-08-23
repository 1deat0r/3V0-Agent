# VERDICTS-2 — cohort 2: untouched runtime .py (batch B — completes cohort)

Batch B = remaining 126 files. Verdict basis: (1) import-graph (every file
≥1 importer — zero orphans), (2) risk-marker scan (eval/exec/os.system/
subprocess.Popen/shell=True/pickle — only ONE hit, documented), (3) refs in
tests/docs/wiki, (4) spot-reads of the low-importer and single-risk files.

**Verdict: NEEDED ×126.** No IMPROVE/UPDATE/REMOVE/REPLACE required.

Spot-check notes:
- agent/verify/runner.py — shell=True is DELIBERATE + documented in the
  module docstring (developer tool executing the project's own recipe
  commands; same trust level as the terminal tool). Not a smell.
- tools/neutts_synth.py — standalone TTS helper; referenced by wiki/TOOLS.md,
  ev0-agent/configuration.md, ev0_cli/tips.py + setup.py.
- tools/browser_dialog_tool.py — imp=1 but covered by
  tests/tools/test_browser_supervisor.py.
- gateway/stream_dispatch.py — exercised by tests/gateway/test_stream_events.py.
- agent/monitoring/events.py, agent/errors.py, agent/transports/*,
  ev0_cli/web_routers/*, gateway/relay/* — heavy importers (100-1900 refs).

Honesty note: verdicts are evidence-grounded but batch-level (purpose,
wiring, risk surface), not a full line-by-line read of all 29k lines. The
highest-value files for any future line-level pass: agent/verify/runner.py,
tools/*_tool.py (tool layer), gateway/platforms/* (platform adapters),
security-adjacent ev0_cli/dashboard_auth/*.

COHORT 2 COMPLETE: 136/136 NEEDED, 0 changes proposed.