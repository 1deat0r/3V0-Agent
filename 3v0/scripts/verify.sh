#!/usr/bin/env bash
# verify.sh — mechanical state gate that defines "done".
# Fails loud (exit non-zero) if any body invariant is violated. Run before
# declaring any body change done / ready to ship.
# Built 2026-08-18 (quality self-improvement lever). Self-anchored (portable).
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$SCRIPT_DIR/../.."             # repo root
D="$SCRIPT_DIR/../data"           # 3v0/data

fail() { echo "FAIL: $1"; FAIL=1; }
FAIL=0

# 1. memory.db readable with facts present
MEM=$(python3 -c "import sqlite3,sys;print(sqlite3.connect(sys.argv[1]).execute('select count(*) from facts').fetchone()[0])" "$D/memory.db" 2>/dev/null) || { fail "memory.db unreadable"; MEM=0; }
[ "$MEM" -gt 0 ] || fail "memory.db empty (facts=$MEM)"
echo "ok: memory facts=$MEM"

# 2. skills.json valid JSON (derived/regenerable; validate the local copy parses)
python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$D/skills.json" 2>/dev/null || { python3 -c "import json,sys; json.load(open(sys.argv[1]))"; fail "skills.json invalid"; }
echo "ok: skills.json valid"

# 3. root cruft absent
CRUFT=$(cd "$R" && ls 2>/dev/null | grep -cE 'log\.txt|sqlite_leak|test_durations|egg-info' || true)
[ "$CRUFT" -eq 0 ] || fail "root cruft present ($CRUFT)"
echo "ok: root cruft=$CRUFT"

# 4. secrets (.env) not tracked in git
ENVTRACKED=$(cd "$R" && git ls-files 2>/dev/null | grep -c '\.env$' || true)
[ "$ENVTRACKED" -eq 0 ] || fail ".env tracked in git ($ENVTRACKED)"
echo "ok: .env tracked=$ENVTRACKED"

# 5. tree clean beyond memory.db (daemon live write). Live data stores
#    (redo_log, discovery_feedback, skills.json) are untracked/gitignored —
#    legitimate local state and expected to change, so not gate failures.
DIRTY=$(cd "$R" && git status --porcelain 2>/dev/null | grep -v '^??' | grep -v '3v0/data/memory.db' | wc -l | tr -d ' ')
[ "$DIRTY" -eq 0 ] || fail "uncommitted changes beyond memory.db: $(cd "$R" && git status --porcelain | grep -v '^??' | grep -v 'memory.db' | head -3 | tr '\n' ' ')"
echo "ok: tree clean (beyond memory.db)"

if [ "$FAIL" -eq 0 ]; then
  echo "PASS — body is in a done/healthy state."
else
  echo "GATE FAILED — do not ship."
  exit 1
fi
