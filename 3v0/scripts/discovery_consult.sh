#!/usr/bin/env bash
# discovery_consult.sh — consult or update the discovery feedback store.
# Advisory correction cache with heuristic recall — NOT guaranteed-improving ML.
# A PRIOR MISS hit is a HYPOTHESIS: revalidate the 'corrected' target against the
# current active set / catalog / task intent before acting; never honor blindly.
# A stale or wrong entry must be demoted, not followed and not re-recorded.
# Usage:
#   discovery_consult.sh "<query terms>"                       # advisory recall
#   discovery_consult.sh add "<query>" "<chosen>" "<corrected>" "<reason>"
#   discovery_consult.sh dump                                   # count + entries
# Self-anchored (portable). add() dedups on (query,chosen,corrected), flocks,
# uses monotonic max(id)+1, atomic temp+rename write.
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORE="${DISCOVERY_STORE:-$SCRIPT_DIR/../data/discovery_feedback.json}"

add() {
  python3 - "$STORE" "$1" "$2" "$3" "$4" <<'PY'
import json, sys, datetime, os, fcntl, tempfile
store, q, chosen, corrected, reason = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
with open(store + ".lock", "a") as lf:
    fcntl.flock(lf, fcntl.LOCK_EX)
    try:
        with open(store) as f: d = json.load(f)
    except Exception: d = []
    for e in d:
        if e.get("query")==q and e.get("chosen")==chosen and e.get("corrected")==corrected:
            e["count"] = e.get("count",1) + 1
            e["last_seen"] = datetime.date.today().isoformat()
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(store))
            os.write(fd, json.dumps(d, indent=2).encode()); os.close(fd); os.replace(tmp, store)
            print(f"duplicate correction #{e['id']}: count={e['count']}")
            sys.exit(0)
    n = max((e.get("id",0) for e in d), default=0) + 1
    d.append({"id": n, "date": datetime.date.today().isoformat(), "query": q,
              "chosen": chosen, "corrected": corrected, "reason": reason,
              "count": 1, "hits": 0, "errors": 0})
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(store))
    os.write(fd, json.dumps(d, indent=2).encode()); os.close(fd); os.replace(tmp, store)
    print(f"recorded correction #{n}")
PY
}

if [ "${1:-}" = "add" ]; then
  if [ $# -ge 5 ]; then add "$2" "$3" "$4" "$5"; exit 0
  else echo 'usage: discovery_consult.sh add "<query>" "<chosen>" "<corrected>" "<reason>"'; exit 1; fi
fi

if [ "${1:-}" = "dump" ]; then
  python3 - "$STORE" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("(store empty/unreadable)"); sys.exit(0)
print(f"store entries: {len(d)}")
for e in d:
    print(f"  #{e.get('id')} [{e.get('date')}] count={e.get('count',1)} hits={e.get('hits',0)} errors={e.get('errors',0)} query='{e.get('query')}' -> corrected='{e.get('corrected')}'")
PY
  exit 0
fi

q="${1:-}"
if [ -z "$q" ]; then
  echo "usage: discovery_consult.sh \"<query terms>\" | add | dump"
  exit 1
fi
python3 - "$STORE" "$q" <<'PY'
import json, sys
store, q = sys.argv[1], sys.argv[2].lower()
try: d = json.load(open(store))
except Exception: print("(store empty/unreadable)"); sys.exit(0)
hits = [e for e in d if
        q in e.get("query", "").lower() or
        q in e.get("corrected", "").lower() or
        q in e.get("reason", "").lower()]
if not hits:
    print("(no prior correction for this query)")
else:
    for e in hits:
        print(f"ADVISORY PRIOR MISS: query='{e.get('query')}' -> chose '{e.get('chosen')}', "
              f"hint corrected='{e.get('corrected')}' ({e.get('reason')}). "
              f"REVALIDATE against current active set/catalog/intent before acting; do not honor blindly.")
PY
