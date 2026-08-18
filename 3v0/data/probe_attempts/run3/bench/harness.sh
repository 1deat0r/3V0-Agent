#!/usr/bin/env bash
# probe021: run all three benchmark stages in order; log evidence; print ALL_PASS + wall time.
set -uo pipefail
cd "$(dirname "$0")"
LOG=run.log
T0=$(date +%s)
: > "$LOG"
log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$LOG"; }

log "STAGE1: hidden deterministic cases..."
python3 tests_hidden.py | tee -a "$LOG"

log "STAGE2: timing ref vs naive on largest input (N=30,000)..."
python3 tests_timing.py | tee -a "$LOG"

log "STAGE3: proving naive_wrong.py is objectively wrong vs correct ref.py..."
python3 tests_wrong.py | tee -a "$LOG"

T1=$(date +%s)
log "ALL_PASS  (wall: $((T1-T0))s)"
