#!/usr/bin/env bash
# 3V0 handoff/startup audit — run from repo root.
#
# Audits the body (git) and re-checks the tracked open loops against live
# GitHub in a single command, instead of the manual multi-command dance.
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

echo "== OPEN LOOPS =="
for entry in "${LOOPS[@]}"; do
  kind=${entry%% *}
  num=${entry##* }
  echo "--- $kind #$num ---"
  gh "$kind" view "$num" --repo "$REPO" \
    --json state,title,updatedAt,mergeable \
    --jq '"state=\(.state) updated=\(.updatedAt) mergeable=\(.mergeable) title=\(.title)"' 2>&1
  echo
done
