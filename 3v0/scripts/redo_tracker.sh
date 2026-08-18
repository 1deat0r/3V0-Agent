#!/usr/bin/env bash
# redo_tracker.sh — counts + logs preventable re-do's, each driving a guard.
# Redo rate is the efficiency lever: trend it to zero (TextGrad — every redo
# gets a guard built, and a guarded redo isn't repeated).
# Usage: redo_tracker.sh              # list count + trend
#        redo_tracker.sh add "cause" "guard"
# Built 2026-08-18 (efficiency self-improvement lever).
set -u
R="/home/mustbearn/Projects/AI Agents/3V0 Agent"
LOG="$R/3v0/data/redo_log.json"

list() {
  if [ ! -f "$LOG" ]; then echo "no redo log yet"; return; fi
  python3 - "$LOG" <<'PY'
import json,sys
try:
    d=json.load(open(sys.argv[1]))
except Exception:
    print("redo log unreadable/empty"); sys.exit(0)
print(f"redo count: {len(d)}")
for e in d:
    print(f"  #{e.get('id')} [{e.get('date','?')}] cause: {e.get('cause','?')} -> guard: {e.get('guard','?')}")
PY
}

add() {
  python3 - "$LOG" "$1" "$2" <<'PY'
import json,sys
log,cause,guard=sys.argv[1],sys.argv[2],sys.argv[3]
import datetime
try:
    d=json.load(open(log))
except Exception:
    d=[]
d.append({"id":len(d)+1,"date":datetime.date.today().isoformat(),"cause":cause,"guard":guard})
json.dump(d,open(log,"w"),indent=2)
print(f"logged redo #{len(d)}")
PY
}

case "${1:-list}" in
  list) list ;;
  add)  [ $# -ge 3 ] && add "$2" "$3" || echo 'usage: redo_tracker.sh add "cause" "guard"' ;;
  *)    echo "usage: redo_tracker.sh [list|add \"cause\" \"guard\"]" ;;
esac
