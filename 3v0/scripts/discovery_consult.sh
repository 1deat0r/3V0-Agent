#!/usr/bin/env bash
# discovery_consult.sh — consult or update the discovery feedback store.
# Prevents repeat misses: every past miss is a consultable correction.
# Usage:
#   discovery_consult.sh "<query terms>"                        # list prior corrections for a query
#   discovery_consult.sh add "<query>" "<chosen>" "<corrected>" "<reason>"   # record a miss
# Fast paths (active-set, exact-name, single-candidate) skip the consult.
set -u
STORE="/home/mustbearn/Projects/AI Agents/3V0 Agent/3v0/data/discovery_feedback.json"

add() {
  python3 - "$STORE" "$1" "$2" "$3" "$4" <<'PY'
import json, sys, datetime
store, q, chosen, corrected, reason = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
try: d = json.load(open(store))
except Exception: d = []
n = max((e["id"] for e in d), default=0) + 1
d.append({"id": n, "date": datetime.date.today().isoformat(),
          "query": q, "chosen": chosen, "corrected": corrected, "reason": reason})
json.dump(d, open(store, "w"), indent=2)
print(f"recorded correction #{n}")
PY
}

if [ "${1:-}" = "add" ]; then
  if [ $# -ge 5 ]; then add "$2" "$3" "$4" "$5"; exit 0
  else echo 'usage: discovery_consult.sh add "<query>" "<chosen>" "<corrected>" "<reason>"'; exit 1; fi
fi

Q="${1:-}"
if [ -z "$Q" ]; then python3 "$STORE" 2>/dev/null; exit 0; fi
python3 - "$STORE" "$Q" <<'PY'
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
        print(f"PRIOR MISS: query='{e.get('query')}' -> chose '{e.get('chosen')}', "
              f"SHOULD be '{e.get('corrected')}' ({e.get('reason')})")
PY
