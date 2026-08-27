"""Shared adapter helper implementations (issue #22 expand step).

Patterns that were hand-copied per-adapter (typing-flood cooldown, edit
overflow split-and-deliver) get one canonical home here so the migrate
step (#23) can adopt them adapter-by-adapter with zero behavior change.

Importable from both ``gateway.platforms.*`` and ``plugins/platforms/*``
adapters.  This module MUST NOT import ``gateway.platforms.base`` at
module level (base re-exports from here — that would be circular); any
base dependency is resolved lazily inside the function body.
"""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Any, Awaitable, Callable, Optional, Sequence

logger = logging.getLogger(__name__)

__all__ = ["TypingCooldownMixin", "get_scoped_secret", "overflow_split_and_deliver"]


def get_scoped_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """Scope-aware credential read with the default-profile startup fallback.

    Canonical copy of the wrapper hand-pasted across ~15 platform adapters
    (AGENTS.md Profiles rule 7).  Under ``gateway.multiplex_profiles``,
    secondary profiles construct adapters inside a profile secret scope —
    the scope is authoritative and a scoped miss returns ``default`` (NO
    cross-profile borrow from ``os.environ``, which may hold another
    profile's value).  The DEFAULT profile's adapter constructs and sends
    *unscoped*, where a bare ``get_secret`` raises ``UnscopedSecretError``;
    there ``os.environ`` IS that profile's own value, so fall back to it.
    Fail-closed on the scoped path, fail-to-own-env on the unscoped path.
    """
    from agent.secret_scope import UnscopedSecretError, get_secret

    try:
        val = get_secret(name, default)
    except UnscopedSecretError:
        val = os.getenv(name)
    return val if val is not None else default


class TypingCooldownMixin:
    """Per-chat typing-indicator cooldown after transient send failures.

    The canonical shape previously duplicated in the Telegram adapter:
    after a flood-wait / rate-limit style failure, suppress further typing
    refreshes for that chat until the cooldown expires (honoring a
    server-supplied ``retry_after`` when present, clamped to [1, 300]s).

    Mix into an adapter class; call :meth:`_typing_in_cooldown` before
    sending, :meth:`_record_typing_cooldown` on failure, and
    :meth:`_clear_typing_cooldown` after a successful send.  The state dict
    is created lazily, so hosts that never send typing pay nothing.
    """

    #: Default suppression window when the server gives no retry_after.
    _typing_cooldown_seconds: float = 30.0

    def _typing_cooldown_map(self) -> "dict[str, float]":
        m = getattr(self, "_typing_cooldown_until", None)
        if m is None:
            m = {}
            self._typing_cooldown_until = m
        return m

    def _typing_in_cooldown(self, chat_id: Any) -> bool:
        """True while *chat_id* is suppressed; prunes expired entries."""
        until = self._typing_cooldown_map().get(str(chat_id))
        if until is None:
            return False
        if asyncio.get_running_loop().time() < until:
            return True
        self._typing_cooldown_map().pop(str(chat_id), None)
        return False

    def _record_typing_cooldown(
        self, chat_id: Any, retry_after: Any = None
    ) -> None:
        """Suppress typing for *chat_id*; *retry_after* (seconds, any
        numeric-ish value) overrides the default window when parseable."""
        delay = self._typing_cooldown_seconds
        if retry_after is not None:
            try:
                delay = float(retry_after)
            except (TypeError, ValueError):
                pass
        delay = max(1.0, min(delay, 300.0))
        self._typing_cooldown_map()[str(chat_id)] = (
            asyncio.get_running_loop().time() + delay
        )

    def _clear_typing_cooldown(self, chat_id: Any) -> None:
        """End suppression early (call after a confirmed successful send)."""
        self._typing_cooldown_map().pop(str(chat_id), None)


async def overflow_split_and_deliver(
    chunks: Sequence[str],
    *,
    original_message_id: Optional[str],
    edit_first: Callable[[str], Awaitable[None]],
    send_continuation: Callable[[str, Optional[str]], Awaitable[Optional[str]]],
    adapter_name: str = "",
    error_fn: Callable[[Exception], str] = str,
):
    """Deliver pre-chunked overflow across an edit + threaded continuations.

    The platform-neutral core of the ``_edit_overflow_split`` pattern
    (Telegram edit overflow, Discord final-edit overflow): chunk assembly,
    first-chunk edit, continuation threading, and the ``partial_overflow``
    SendResult contract are shared; the platform-specific API calls stay in
    the two callbacks.

    Args:
        chunks: Already-correctly-sized message parts (>=1).  The caller
            chunks with ``truncate_message`` / fence-aware splitting.
        original_message_id: id of the message being edited.
        edit_first: awaited with chunks[0]; raises on failure.  Platform
            quirks that are *not* errors (e.g. Telegram "message is not
            modified") must be swallowed inside this callback.
        send_continuation: awaited with ``(chunk, prev_message_id)`` for
            each remaining chunk; returns the new message id (or None when
            the platform tracks ids elsewhere).  Raises on failure.
        adapter_name: for log prefixes.
        error_fn: renders an exception for ``SendResult.error`` (e.g.
            Telegram's redacting formatter).

    Returns:
        ``SendResult`` with ``message_id`` = LAST visible message id and
        ``continuation_message_ids`` = every extra id in send order.  On a
        mid-stream continuation failure, success is still True with a
        ``raw_response["partial_overflow"]`` payload so the stream consumer
        can deliver the missing tail (dropping chunks the user already saw
        is the worse outcome).  Only a first-chunk edit failure returns
        success=False — a real adapter problem, not overflow.
    """
    from gateway.platforms.base import SendResult  # lazy: avoid cycle

    if not chunks:
        return SendResult(success=True, message_id=original_message_id)

    # Step 1 — edit the existing message with the first chunk.
    try:
        await edit_first(chunks[0])
    except Exception as e:
        logger.error(
            "[%s] Overflow split: first-chunk edit failed: %s",
            adapter_name, e, exc_info=True,
        )
        return SendResult(success=False, error=error_fn(e))

    # Step 2 — send each remaining chunk threaded to the previous one.
    continuation_ids: list[str] = []
    delivered = 1
    prev_id = original_message_id
    for chunk in chunks[1:]:
        try:
            new_id = await send_continuation(chunk, prev_id)
        except Exception as send_err:
            logger.warning(
                "[%s] Overflow split: stopped at %d/%d chunks delivered: %s",
                adapter_name, delivered, len(chunks), send_err,
            )
            last_id = continuation_ids[-1] if continuation_ids else original_message_id
            return SendResult(
                success=True,
                message_id=last_id,
                continuation_message_ids=tuple(continuation_ids),
                raw_response={
                    "partial_overflow": True,
                    "delivered_chunks": delivered,
                    "total_chunks": len(chunks),
                    "last_message_id": last_id,
                    "continuation_message_ids": tuple(continuation_ids),
                },
            )
        delivered += 1
        if new_id is not None:
            prev_id = new_id
            continuation_ids.append(str(new_id))

    last_id = continuation_ids[-1] if continuation_ids else original_message_id
    logger.debug(
        "[%s] Overflow split delivered %d chunks; last_id=%s",
        adapter_name, delivered, last_id,
    )
    return SendResult(
        success=True,
        message_id=last_id,
        continuation_message_ids=tuple(continuation_ids),
    )
