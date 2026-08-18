#!/usr/bin/env bash
# redo_tracker.sh — counts + logs preventable re-do's, each driving a guard.
# Redo rate is the efficiency lever; the COUNT/TREND is the measured metric.
# NOT a monotonic-accuracy claim — each logged redo is a measured event.
# Usage: redo_tracker.sh            # list + count
#        redo_tracker.sh add "cause" "guard"
# Self-anchored (portable); REDO_LOG env overrides path. max(id)+1 ids, flocked,
# atomic temp+rename write.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="${REDO_LOG:-$SCRIPT_DIR/../data/redo_log.json}"

list() {
  if [ ! -f "$LOG" ]; then echo "no redo log"; return; fi
  python3 - "$LOG" <<'PY'
import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception: print("redo log unreadable/empty"); sys.exit(0)
print(f"redo count: {len(d)}")
for i,e in enumerate(d,1):
    print(f"  #{e.get('id',i)} [{e.get('date','?')}] cause: {e.get('cause','?')} -> guard: {e.get('guard','?')}")
PY
}

add() {
  python3 - "$LOG" "$1" "$2" <<'PY'
import json,sys,datetime,os,fcntl,tempfile
log,cause,guard=sys.argv[1],sys.argv[2],sys.argv[3]
with open(log+".lock","a") as lf:
    fcntl.flock(lf,fcntl.LOCK_EX)
    try:
        with open(log) as f: d=json.load(f)
    except Exception: d=[]
    n=max((e.get("id",0) for e in d),default=0)+1
    d.append({"id":n,"date":datetime.date.today().isoformat(),"cause":cause,"guard":guard})
    fd,tmp=tempfile.mkstemp(dir=os.path.dirname(log))
    os.write(fd,json.dumps(d,indent=2).encode()); os.close(fd); os.replace(tmp,log)
    print(f"logged redo #{n}")
PY
}

case "${1:-list}" in
  list) list;;
  add) [ $# -ge 3 ] && add "$2" "$3" || echo 'usage: redo_tracker.sh add "cause" "guard"';;
esac
