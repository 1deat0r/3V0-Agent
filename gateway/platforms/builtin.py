"""Built-in platform adapter registration (ticket #24 — one loading path).

The nine ``gateway/platforms/*`` adapters used to be hand-rolled into an
``if/elif`` chain inside ``GatewayRunner``'s adapter creation — a second
adapter loading path parallel to the platform registry, with its own
dependency probes, warning strings, and ``gateway_runner`` injection
rules. They now register here as :class:`PlatformEntry` records so the
platform registry is the single adapter loading path: plugins, relay,
and built-ins all resolve through ``platform_registry.create_adapter()``.

Everything registered here is deferred and side-effect free until a
factory actually runs:

- ``check_fn`` is a PASSIVE import probe (no pip installs — the active
  installer contract lives on ``ensure_deps_fn``, see #79812).
- factories lazy-import the adapter module, so gateway startup does not
  pull aiohttp/httpx/websockets for platforms the user never enabled.

``ensure_builtin_platforms_registered()`` is idempotent and safe to call
from any entry point that resolves adapters (or enumerates platforms for
status displays).
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_REGISTERED = False


def _import_probe(*module_names: str):
    """Passive dependency probe: True when every named module imports."""

    def _check() -> bool:
        for name in module_names:
            try:
                __import__(name)
            except Exception:
                return False
        return True

    return _check


def ensure_builtin_platforms_registered() -> None:
    """Register the nine built-in platform adapters (idempotent).

    ``PlatformRegistry.register`` replaces same-name entries, so calling
    this repeatedly — or after a plugin deliberately overrode a built-in —
    is safe and keeps last-writer-wins semantics.
    """
    global _REGISTERED
    if _REGISTERED:
        return
    _REGISTERED = True

    from gateway.platform_registry import PlatformEntry, platform_registry

    def _register(
        name: str,
        label: str,
        factory,
        check,
        *,
        validate=None,
        hint: str = "",
    ) -> None:
        platform_registry.register(
            PlatformEntry(
                name=name,
                label=label,
                adapter_factory=factory,
                check_fn=check,
                validate_config=validate,
                install_hint=hint,
                source="builtin",
            )
        )

    def _whatsapp_cloud_factory(config):
        from gateway.platforms.whatsapp_cloud import WhatsAppCloudAdapter

        return WhatsAppCloudAdapter(config)

    _register(
        "whatsapp_cloud",
        "WhatsApp Cloud",
        _whatsapp_cloud_factory,
        _import_probe("aiohttp", "httpx"),
        hint="aiohttp/httpx missing — reinstall 3v0-agent",
    )

    def _signal_check() -> bool:
        from gateway.platforms.signal import check_signal_requirements

        return check_signal_requirements()

    def _signal_validate(config) -> bool:
        from gateway.platforms.signal import validate_signal_config

        ok = validate_signal_config(config)
        if not ok:
            # Preserve the chain's specific reason (the registry only logs
            # a generic validation failure).
            logger.warning(
                "Signal: SIGNAL_HTTP_URL or SIGNAL_ACCOUNT not configured"
            )
        return ok

    def _signal_factory(config):
        from gateway.platforms.signal import SignalAdapter

        return SignalAdapter(config)

    _register(
        "signal",
        "Signal",
        _signal_factory,
        _signal_check,
        validate=_signal_validate,
        hint="runtime requirements not met",
    )

    def _weixin_factory(config):
        from gateway.platforms.weixin import WeixinAdapter

        return WeixinAdapter(config)

    _register(
        "weixin",
        "Weixin",
        _weixin_factory,
        _import_probe("aiohttp", "cryptography"),
        hint="aiohttp/cryptography not installed",
    )

    def _api_server_factory(config):
        from gateway.platforms.api_server import APIServerAdapter

        return APIServerAdapter(config)

    _register(
        "api_server",
        "API Server",
        _api_server_factory,
        _import_probe("aiohttp"),
    )

    def _webhook_factory(config):
        from gateway.platforms.webhook import WebhookAdapter

        return WebhookAdapter(config)

    _register(
        "webhook",
        "Webhook",
        _webhook_factory,
        _import_probe("aiohttp"),
    )

    def _msgraph_factory(config):
        from gateway.platforms.msgraph_webhook import MSGraphWebhookAdapter

        return MSGraphWebhookAdapter(config)

    _register(
        "msgraph_webhook",
        "MSGraph Webhook",
        _msgraph_factory,
        _import_probe("aiohttp"),
    )

    def _bluebubbles_factory(config):
        from gateway.platforms.bluebubbles import BlueBubblesAdapter

        return BlueBubblesAdapter(config)

    _register(
        "bluebubbles",
        "BlueBubbles",
        _bluebubbles_factory,
        _import_probe("aiohttp", "httpx"),
        hint="aiohttp/httpx missing or BLUEBUBBLES_SERVER_URL/BLUEBUBBLES_PASSWORD not configured",
    )

    def _qqbot_factory(config):
        from gateway.platforms.qqbot import QQAdapter

        return QQAdapter(config)

    _register(
        "qqbot",
        "QQBot",
        _qqbot_factory,
        _import_probe("aiohttp", "httpx"),
        hint="aiohttp/httpx missing or QQ_APP_ID/QQ_CLIENT_SECRET not configured",
    )

    def _yuanbao_check() -> bool:
        try:
            from gateway.platforms.yuanbao import WEBSOCKETS_AVAILABLE
        except Exception:
            return False
        return bool(WEBSOCKETS_AVAILABLE)

    def _yuanbao_factory(config):
        from gateway.platforms.yuanbao import YuanbaoAdapter

        return YuanbaoAdapter(config)

    _register(
        "yuanbao",
        "Yuanbao",
        _yuanbao_factory,
        _yuanbao_check,
        hint="websockets not installed. Run: pip install websockets",
    )
