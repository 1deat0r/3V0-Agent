#!/usr/bin/env bash
# audit.sh — one-command snapshot of the 3V0 body.
# Replaces N turns of ad-hoc auditing with a single call.
# Self-improvement lever for speed + efficiency + token-efficiency (built 2026-08-18).
set -u
R="/home/mustbearn/Projects/AI Agents/3V0 Agent"
D="$R/3v0/data"

echo "== HEAD: $(git -C "$R" log --oneline -1 2>/dev/null || echo '?')"
echo "== git status:"
git -C "$R" status --short 2>/dev/null | head -15
echo "(end status)"
echo "== memory facts: $(python3 -c "import sqlite3;print(sqlite3.connect('$D/memory.db').execute('select count(*) from facts').fetchone()[0])" 2>/dev/null || echo 'err')"
echo "== skills.json valid? $(python3 -c "import json;_=json.load(open('$D/skills.json'))" 2>/dev/null && echo 'yes' || echo 'NO')"
echo "== root cruft count: $(cd "$R" && ls 2>/dev/null | grep -cE 'log\.txt|sqlite_leak|test_durations|egg-info' || echo 0)"
echo "== .env tracked in git? $(cd "$R" && git ls-files 2>/dev/null | grep -c '\.env$' || echo 0) (must be 0)"
echo "== token health:"
python3 "$R/3v0/scripts/analytics.py" --db "$HOME/.hermes/profiles/3v0/state.db" 2>/dev/null | head -3 || echo "analytics n/a"
echo "== 3v0-review daemon: $(systemctl --user is-active 3v0-review 2>/dev/null || echo '?')"
