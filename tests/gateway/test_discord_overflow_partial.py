"""Regression coverage for partial Discord overflow delivery.

Mirrors ``test_telegram_overflow_partial.py``: pins the adapter-level
contract of ``_edit_overflow_split`` (now delegated to the shared
``overflow_split_and_deliver`` core) when a continuation lands and a later
one fails — the stream consumer keys its fallback-tail delivery off this
payload.
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from gateway.config import PlatformConfig


def _ensure_discord_mock():
    if "discord" in sys.modules and hasattr(sys.modules["discord"], "__file__"):
        return
    discord_mod = MagicMock()
    discord_mod.Intents.default.return_value = MagicMock()
    discord_mod.Client = MagicMock
    discord_mod.File = MagicMock
    discord_mod.DMChannel = type("DMChannel", (), {})
    discord_mod.Thread = type("Thread", (), {})
    discord_mod.ForumChannel = type("ForumChannel", (), {})
    ext_mod = MagicMock()
    commands_mod = MagicMock()
    commands_mod.Bot = MagicMock
    ext_mod.commands = commands_mod
    sys.modules.setdefault("discord", discord_mod)
    sys.modules.setdefault("discord.ext", ext_mod)
    sys.modules.setdefault("discord.ext.commands", commands_mod)


_ensure_discord_mock()
from plugins.platforms.discord.adapter import DiscordAdapter  # noqa: E402


@pytest.fixture
def discord_adapter() -> DiscordAdapter:
    adapter = DiscordAdapter(PlatformConfig(enabled=True, token="***"))
    object.__setattr__(adapter, "MAX_MESSAGE_LENGTH", 160)
    return adapter


@pytest.mark.asyncio
async def test_edit_overflow_split_partial_success_after_some_continuations_land(
    discord_adapter,
):
    """Discord's contract: a mid-split continuation failure still reports
    success=True with the partial_overflow payload pointing at the last
    delivered continuation."""
    content = "word " * 120  # forces several 160-char chunks
    channel = SimpleNamespace(id=555, send=AsyncMock())
    msg = SimpleNamespace(id=201, edit=AsyncMock())
    channel.send = AsyncMock(
        side_effect=[
            SimpleNamespace(id=202),
            RuntimeError("discord send failed"),
            RuntimeError("discord send failed"),
        ]
    )

    result = await discord_adapter._edit_overflow_split(channel, msg, "201", content)

    assert result.success is True
    assert result.message_id == "202"
    assert result.raw_response["partial_overflow"] is True
    assert result.raw_response["delivered_chunks"] == 2
    assert result.raw_response["total_chunks"] > 2
    assert result.raw_response["last_message_id"] == "202"
    assert result.continuation_message_ids == ("202",)
    # First chunk went to the edit; the failing chunk tries threaded, then
    # the drop-anchor retry (3 sends total across 2 chunks).
    msg.edit.assert_awaited_once()
    assert channel.send.await_count == 3
