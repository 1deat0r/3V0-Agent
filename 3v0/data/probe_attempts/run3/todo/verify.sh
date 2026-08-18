#!/usr/bin/env bash
# probe020: conformance suite against the running todo server (STAGE1-3).
set -u
B="http://127.0.0.1:${TODO_PORT:-18080}"
fails=0
ok()   { printf 'PASS %s\n' "$1"; }
bad()  { printf 'FAIL %s\n' "$1"; fails=$((fails+1)); }

# STAGE1 base conformance
CODE=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$B/todos" -H 'Content-Type: application/json' -d '{"title":"write report"}')
[ "$CODE" = "201" ] && ok S1-POST-201 || { bad S1-POST-201 "got $CODE"; }
ID=$(curl -s -X POST "$B/todos" -H 'Content-Type: application/json' -d '{"title":"ship feature"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
BOD=$(curl -s -X POST "$B/todos" -H 'Content-Type: application/json' -d '{"title":"test me"}' | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["done"], d["title"])')
[ "$BOD" = "False test me" ] && ok S1-created-echo || bad S1-created-echo "got [$BOD]"
curl -s "$B/todos" | grep -q '"title": "test me"' && ok S1-GET-list || bad S1-GET-list
R=$(curl -s "$B/todos/$ID")
echo "$R" | grep -q '"title": "ship feature"' && ok S1-GET-byid || bad S1-GET-byid "$R"
P=$(curl -s -o /dev/null -w '%{http_code}' -X PUT "$B/todos/$ID" -H 'Content-Type: application/json' -d '{"done":true,"title":"shipped feature"}')
[ "$P" = "200" ] && ok S1-PUT-200 || bad S1-PUT-200
curl -s "$B/todos/$ID" | grep -q '"done": true' && ok S1-PUT-applied || bad S1-PUT-applied
D=$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$B/todos/$ID")
[ "$D" = "200" ] && ok S1-DELETE-200 || bad S1-DELETE-200
[ "$(curl -s -o /dev/null -w '%{http_code}' "$B/todos/$ID")" = "404" ] && ok S1-GET-missing-404 || bad S1-GET-missing-404
[ "$(curl -s -o /dev/null -w '%{http_code}' -X PUT "$B/todos/99999" -H 'Content-Type: application/json' -d '{}')" = "404" ] && ok S1-PUT-missing-404 || bad S1-PUT-missing-404
[ "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$B/todos/99999")" = "404" ] && ok S1-DELETE-missing-404 || bad S1-DELETE-missing-404
[ "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$B/todos" -H 'Content-Type: application/json' -d '{"title":"   "}')" = "400" ] && ok S1-empty-title-400 || bad S1-empty-title-400

# STAGE2: 50 concurrent POSTs -> exactly 50 distinct todos
seq 1 50 | xargs -P 25 -I{} curl -s -o /dev/null -w '%{http_code}\n' -X POST "$B/todos" -H 'Content-Type: application/json' -d "{\"title\":\"conc-{}\"}" | grep -c 201 >/dev/null
N=$(curl -s "$B/todos" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(sum(1 for t in d if t["title"].startswith("conc-")))')
[ "$N" = "50" ] && ok S2-fifty-distinct || bad S2-fifty-distinct "count=$N"
curl -s "$B/todos" | python3 -c 'import sys,json;d=json.load(sys.stdin);t=[x["title"] for x in d if x["title"].startswith("conc-")];assert len(set(t))==50,sorted(t)' && ok S2-fifty-unique-titles || bad S2-fifty-unique-titles

# STAGE3: Idempotency-Key -> exactly one todo; second echoes first id as 200
F1=$(curl -s -X POST "$B/todos" -H 'Content-Type: application/json' -H 'Idempotency-Key: ktx-abc-1' -d '{"title":"dedup target"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
R2=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$B/todos" -H 'Content-Type: application/json' -H 'Idempotency-Key: ktx-abc-1' -d '{"title":"dedup target"}')
[ "$R2" = "200" ] && ok S3-dup-200 || bad S3-dup-200
F2=$(curl -s -X POST "$B/todos" -H 'Content-Type: application/json' -H 'Idempotency-Key: ktx-abc-1' -d '{"title":"dedup target"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
[ "$F1" = "$F2" ] && ok S3-same-id-echoed || bad S3-same-id-echoed "f1=$F1 f2=$F2"
C=$(curl -s "$B/todos" | python3 -c 'import sys,json;print(sum(1 for t in json.load(sys.stdin) if t["title"]=="dedup target"))')
[ "$C" = "1" ] && ok S3-single-todo || bad S3-single-todo "count=$C"

echo "----"
if [ "$fails" = "0" ]; then echo "ALL_PASS probe020 conformance"; else echo "FAILURES: $fails"; exit 1; fi
