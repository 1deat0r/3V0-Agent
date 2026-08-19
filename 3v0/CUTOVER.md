# 3V0 CUTOVER — running the native gateway on the live bot

Status: **FIRED 2026-08-14, ROLLED BACK 2026-08-20 (operator decision).** The
native runtime (N1–N5) was cut over and ran on the live bot, then reverted:
the operator judged the native gateway a quality regression vs the renamed
Hermes gateway and restored `3v0-gateway.service` (ev0 CLI) as the serving
baseline going forward. The native runtime remains in the tree as a
hermes-independent alternative, but it is **disabled** and must not be
re-enabled without operator sign-off. This document is kept for the
procedure's historical record.

## Hard constraint
You CANNOT run two `getUpdates` pollers on one bot — they steal each update.
The cutover therefore means stopping the Hermes gateway and starting the native
one. Done wrongly, the bot goes silent. Do not attempt it on momentum.

## The unit (stage at cutover time, do not enable now)
Create `~/.config/systemd/user/3v0-native-gateway.service` at the cutover
moment (not before — an untested live unit is a liability):

```ini
[Unit]
Description=3V0 Agent Gateway — native runtime (hermes-independent)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=/home/mustbearn/Projects/AI Agents/3V0 Agent/3v0
Environment="HERMES_HOME=/home/mustbearn/.hermes/profiles/3v0"
Environment="PYTHONPATH=/home/mustbearn/Projects/AI Agents/3V0 Agent/3v0"
Environment="THREEV0_SERVE=1"
ExecStart=/home/mustbearn/Projects/AI Agents/3V0 Agent/.venv/bin/python -m native.run
Restart=always
RestartSec=5
KillMode=mixed
TimeoutStopSec=60
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

## Cutover sequence (controlled)
1. Preflight: `python3 3v0/native/engine.py` re-verifies the one-shot E2E (must
   print `NATIVE_ENGINE_OK`). MS=(home channel) reachable.
2. Create + (this is deliberate) enable the native unit, `daemon-reload`.
3. Stop the Hermes gateway: `systemctl --user stop 3v0-gateway.service`.
4. Start the native unit: `systemctl --user start 3v0-native-gateway.service`.
5. Verify: send a test message to the bot; it should reply via the native loop
   (watch `journalctl --user -u 3v0-native-gateway` for the getUpdates poll).

## Rollback (reversible, always available)
```bash
systemctl --user stop 3v0-native-gateway.service
systemctl --user start 3v0-gateway.service   # Hermes picks polling back up
```

## Fire criteria (all must hold)
- One-shot E2E re-verified immediately before.
- An operator is watching the channel to catch a silent-bot fast.
- Rollback commands are at hand.
- The operator has explicitly chosen a downtime window.

## Falling back on today's lesson
The `reload_gateway.sh` stop-not-restart failure happened when a mechanism was
turned into a live action before it was proven AND reversible. The native cutover
inverts that: it is documented, reversible, staged, and not fired until the
operator consciously pulls the trigger. Treat the first firewall test of the
previous stage as the gate, not the momentum.
