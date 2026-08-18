#!/usr/bin/env bash
# reload_gateway.sh — 3V0's sanctioned, safe self-reload of 3v0-gateway (native runtime).
#
# WHY A SCRIPT (and why this is the ONLY self-restart path 3V0 is permitted):
# a DIRECT `systemctl --user restart 3v0-gateway` from inside the gateway
# kills this very subprocess before it completes (systemd's KillMode=mixed sweeps
# the service cgroup, SIGTERM→SIGKILL on children), so the gateway may never come
# back. The safe pattern is to hand the restart to a DETACHED transient systemd
# unit (its OWN cgroup, created via `systemd-run --user`) scheduled a few seconds
# out: that unit survives the gateway's cgroup sweep and performs a clean restart.
# That is exactly the "separate shell outside the running gateway" the guard
# recommends — now self-served instead of operator-handed.
#
# The guard exemption lives in tools/terminal_tool.py (see the _sanctioned_reload
# branch) and was added on the operator's explicit direction (2026-08-18) so 3V0
# can deploy its own runtime (Flash model switch, native-store plugin, own venv)
# without parking the action on a human shell. Ad-hoc lifecycle commands remain
# blocked.
#
# Usage:  reload_gateway.sh [delay_seconds]   (default 6; >=2 so the message sends)
set -euo pipefail

SVC="3v0-gateway.service"
DELAY="${1:-6}"
case "$DELAY" in
  *[!0-9]*|'') DELAY=6 ;;
esac
[ "$DELAY" -ge 2 ] || DELAY=6
UNIT="gw-3v0-reload"

systemd-run --user --on-active="${DELAY}s" --unit="$UNIT" \
  /usr/bin/systemctl --user restart "$SVC" \
  >/dev/null 2>&1

echo "gateway self-reload scheduled in ${DELAY}s via detached transient unit ${UNIT} (survives the gateway cgroup sweep)."
