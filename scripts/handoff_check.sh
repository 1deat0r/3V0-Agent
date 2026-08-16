#!/usr/bin/env bash
# 3V0 handoff/startup audit — run from repo root.
#
# Audits the body (git), converges the native store onto the Hermes profile
# (store is canonical, profile is a derived view), and re-checks the tracked
# open loops against live GitHub in a single command — instead of the manual
# multi-command dance.
#
# The LOOPS array is the single source of truth for what to re-check.
# Keep it in sync with the "Open loops" section of HANDOFF.md.
set -uo pipefail
REPO="NousResearch/hermes-agent"

LOOPS=(
  "pr 86711"
  "pr 72067"
  "pr 73453"
  "issue 84667"
)

echo "== BODY =="
git status --short --branch
echo
git log --oneline -10
echo

echo "== SYNC (store canonical -> profile) =="
python3 3v0/scripts/sync.py --write 2>&1
echo
python3 3v0/scripts/sync_skills.py --write 2>&1
echo

echo "== OPEN LOOPS =="
for entry in "${LOOPS[@]}"; do
  kind=${entry%% *}
  num=${entry##* }
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
done

echo "== DRIFT CHECK (project ledger) =="
python3 3v0/scripts/drift_check.py 2>&1
echo

echo "== CONTINUITY CHECK (invariants) =="
python3 3v0/scripts/continuity_check.py 2>&1
echo
