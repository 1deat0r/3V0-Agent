#!/usr/bin/env bash
# consistency.sh — stale-reference linter + source-of-truth propagation guard.
# Run BEFORE committing any change to a canonical text (SOUL.md, a config, a doc)
# so stale copies don't survive (SELF_IMPROVEMENT.md rule 6).
# Usage: ./consistency.sh
# Built 2026-08-18 (accuracy self-improvement lever — targets the propagation
# miss + git-attribution failures the independent review exposed).
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$SCRIPT_DIR/../.."  # repo root (self-anchored; portability fix from probe review)

# Known-stale doctrine phrases. Tune this list as the body evolves.
# Covers the pre-amendment "lock to DeepSeek-v4-pro / one provider" doctrine
# plus looser phrasings that drifted in docs.
PATTERNS=(
  'DeepSeek-v4-pro via the DeepSeek API only'
  'never another provider'
  'locks the model to DeepSeek-v4-pro'
  'locks the reasoning engine to DeepSeek-v4-pro'
  'approval stays on .pro.'
  'the model to DeepSeek-v4-pro'
  'Prime Directive (immutable): DeepSeek-v4-pro'
)

# Scope: tracked markdown/config/shell docs; exclude data, vendored, history.
FILES=$(git -C "$R" ls-files -- '*.md' '*.yaml' '*.yml' '*.sh' 2>/dev/null \
  | grep -vE '3v0/data/|node_modules|\.venv|EVOLUTION_LOOP|docs/adr/|consistency\.sh')

HITS=0
for f in $FILES; do
  for pat in "${PATTERNS[@]}"; do
    line=$(grep -nE "$pat" "$R/$f" 2>/dev/null | head -1)
    if [ -n "$line" ]; then
      echo "STALE [$pat] -> $f:$(printf '%s' "$line" | cut -d: -f1)"
      HITS=$((HITS+1))
    fi
  done
done

FOUND_COUNT=$(printf '%s\n' "$FILES" | grep -c . || true)
if [ "$HITS" -eq 0 ]; then
  echo "OK — no known stale references across $FOUND_COUNT docs."
else
  echo "FOUND $HITS stale reference(s) — fix before committing source-of-truth changes."
  exit 1
fi
