#!/usr/bin/env bash
# baseline.sh — deterministic NO-REGRESSION floor. NOT an evolution claim.
#
# The only asymmetry that distinguishes regress from evolve: freeze a reference
# ("what 3V0 could do at commit H") and re-run the SAME checks later. If a later
# state fails the frozen reference, that is a regression signal -- revert-worthy.
#
#   --record : freeze [commit, native modules importable, native scripts, memory
#              facts] into 3v0/data/baseline.json
#   (plain)  : PASS if the current state >= the recorded baseline; else FAIL.
#
# HONEST LIMIT (read this): this proves NON-regression, not evolution. Passing
# the floor only says nothing was lost. Proving positive capability growth
# needs a held-out, ungraduated task probe (the open item in EVOLUTION_LOOP).
set -u
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$S/../.."
D="$R/3v0/data"
BASE="$D/baseline.json"

snapshot() {
  python3 - "$R" <<'PY'
import json, subprocess, os, sys, importlib.util
repo = sys.argv[1]
def sh(*a):
    try: return subprocess.run(a, stdout=subprocess.PIPE, text=True, timeout=180).stdout.strip()
    except Exception: return ""
sys.path.insert(0, os.path.join(repo, "3v0"))
native = sorted(
    m for m in ("native.llm","native.context","native.agent","native.tools",
                "native.gateway","native.engine","native.run")
    if importlib.util.find_spec(m)
)
scripts = sorted(f for f in os.listdir(os.path.join(repo,"3v0","scripts")) if f.endswith(".sh"))
try:
    mem = os.path.join(repo, "3v0", "data", "memory.db")
    facts = subprocess.run(
        ["python3","-c",'import sqlite3,sys;print(sqlite3.connect(sys.argv[1]).execute("select count(*) from facts").fetchone()[0])', mem],
        capture_output=True, text=True).stdout.strip()
except Exception:
    facts = "0"
print(json.dumps({
    "commit": sh("git","-C",repo,"rev-parse","--short","HEAD"),
    "native_modules": native,
    "native_scripts": scripts,
    "memory_facts": facts,
}))
PY
}

record() {
  local cur; cur=$(snapshot)
  printf '%s\n' "$cur" > "$BASE"
  echo "baseline recorded -> $BASE ($(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d["commit"],len(d["native_modules"]),"native mods",d["memory_facts"],"facts")' "$BASE"))"
}

check() {
  [ -f "$BASE" ] || { echo "no baseline yet — run baseline.sh --record"; exit 0; }
  local cur ref; cur=$(snapshot); ref=$(cat "$BASE")
  python3 - "$BASE" "$cur" <<'PY'
import json,sys
ref=json.load(open(sys.argv[1])); cur=json.loads(sys.argv[2])
fails=[]
for k in ("native_modules","native_scripts"):
    missing=[x for x in ref[k] if x not in cur[k]]
    if missing: fails.append(f"{k}: missing {missing}")
if int(cur.get("memory_facts",0) or 0) < int(ref.get("memory_facts",0)):
    fails.append("memory_facts declined")
print("baseline commit:", ref.get("commit"), "-> current:", cur.get("commit"))
if fails:
    print("REGRESSION SUSPECT:"); [print("  -",f) for f in fails]; sys.exit(1)
print("PASS — no regression vs frozen baseline (state >= baseline).")
PY
}

case "${1:-}" in
  --record) record ;;
  -) record ;;
  *) check ;;
esac
