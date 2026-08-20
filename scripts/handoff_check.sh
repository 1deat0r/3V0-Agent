#!/usr/bin/env bash
# 3V0 handoff/startup audit — run from repo root.
#
# Audits the body (git), converges the native store onto the 3V0 profile
# (store is canonical, profile is a derived view), re-checks the tracked open
# loops against live GitHub, and regenerates the mechanical handoff draft
# (HANDOFF.generated.md) — instead of the manual multi-command dance.
#
# The tracked-loop list is derived from the claim registry
# (3v0/data/continuity/claims.json) — the single source of truth — NOT a
# hand-synced array. When a loop is added/closed, edit claims.json and
# `python3 3v0/scripts/continuity_check.py --accept` to re-record its state;
# the "Open loops" section and the generated draft both follow automatically.
set -uo pipefail
REPO="NousResearch/3v0-agent"

echo "== BODY =="
git status --short --branch
echo
git log --oneline -10
echo

echo "== CONTINUITY CHECK (invariants, pre-heal) =="
python3 3v0/scripts/continuity_check.py 2>&1
echo

echo "== SYNC (store canonical -> profile) =="
python3 3v0/scripts/sync.py --write 2>&1
echo
python3 3v0/scripts/sync_skills.py --write 2>&1
echo

echo "== OPEN LOOPS (claim registry) =="
LOOP_LINES="$(python3 - <<'PY'
import json, sys
try:
    data = json.load(open("3v0/data/continuity/claims.json", encoding="utf-8"))
except Exception as e:
    print(f"claims.json unreadable: {e}", file=sys.stderr)
    raise SystemExit(0)
loops = data.get("loops", {})
for num in sorted(loops, key=lambda n: int(n) if str(n).isdigit() else 0):
    spec = loops[num] if isinstance(loops[num], dict) else {}
    print(f'{spec.get("kind", "pr")} {num}')
PY
)"
if [[ -z "$LOOP_LINES" ]]; then
  echo "(no loops in the claim registry)"
fi
while read -r kind num; do
  [[ -z "$kind" ]] && continue
  echo "--- $kind #$num ---"
  if [[ "$kind" == "pr" ]]; then
    gh pr view "$num" --repo "$REPO" \
      --json state,title,updatedAt,mergeable \
      --jq '"state=\(.state) updated=\(.updatedAt) mergeable=\(.mergeable) title=\(.title)"' 2>&1
  else
    gh issue view "$num" --repo "$REPO" \
      --json state,title,updatedAt \
      --jq '"state=\(.state) updated=\(.updatedAt) title=\(.title)"' 2>&1
  fi
  echo
done <<< "$LOOP_LINES"

echo "== DRIFT CHECK (project ledger) =="
python3 3v0/scripts/drift_check.py 2>&1
echo

echo "== SELF-ANALYTICS (owned metrics) =="
python3 3v0/scripts/analytics.py 2>&1
echo

echo "== SELF-INSIGHTS (owned findings) =="
python3 3v0/scripts/insights.py 2>&1
echo

echo "== COHERENCE + CONSOLIDATION (standing system) =="
python3 3v0/scripts/coherence_coalesce.py 2>&1 || true
echo

echo "== GENERATED HANDOFF (shadow draft) =="
python3 3v0/scripts/generate_handoff.py 2>&1
echo
