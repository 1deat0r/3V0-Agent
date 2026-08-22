# Cron delivery-platform membership comes from the Platform enum

The cron scheduler carried a hand-maintained `_KNOWN_DELIVERY_PLATFORMS`
set beside its home-env-var table. They drifted: `whatsapp_cloud` was in the
env-var map but absent from the known-set, so a connected WhatsApp Cloud
gateway was silently excluded from cron delivery targets.

Membership now validates against the canonical `Platform` enum in
`gateway/config.py`. The hand-maintained `_KNOWN_DELIVERY_PLATFORMS` set was
deleted entirely — keeping it even as a defensive fallback would reinstate
the exact exclusion it caused (code-review pass). On enum-import failure the
honest answer is "unknown"; plugin providers that declare a cron delivery
env var still pass through. The env map remains the *resolution* table (env
var per platform), not the *membership* gate.