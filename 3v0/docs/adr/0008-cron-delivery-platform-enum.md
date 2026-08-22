# Cron delivery-platform membership comes from the Platform enum

The cron scheduler carried a hand-maintained `_KNOWN_DELIVERY_PLATFORMS`
set beside its home-env-var table. They drifted: `whatsapp_cloud` was in the
env-var map but absent from the known-set, so a connected WhatsApp Cloud
gateway was silently excluded from cron delivery targets.

Membership now validates against the canonical `Platform` enum in
`gateway/config.py` (with the static set retained only as a defensive
fallback if the enum import fails). This kills the drift class: a platform
cannot be declared deliverable in one place and omitted in another. The env
map remains the *resolution* table (env var per platform), not the
*membership* gate.