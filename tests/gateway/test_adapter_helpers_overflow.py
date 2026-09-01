"""Unit tests for the shared overflow_split_and_deliver core (issue #22/#23).

The adapter-level regression tests (test_telegram_overflow_partial,
test_discord_overflow_partial) pin each surface's contract through its
adapter; this file pins the shared core's own contract — including the
per-surface policy knobs (partial_success, delivered_prefix_fn) the
adapters pass.
"""

from __future__ import annotations

import asyncio

import pytest

from gateway.platforms.adapter_helpers import overflow_split_and_deliver
from gateway.platforms.base import SendResult


def _run(coro):
    return asyncio.run(coro)


class TestDefaultContract:
    def test_all_chunks_delivered(self):
        async def main():
            return await overflow_split_and_deliver(
                ["a", "b", "c"],
                original_message_id="1",
                edit_first=_ok(None),
                send_continuation=_ids("2", "3"),
                adapter_name="t",
            )

        r = _run(main())
        assert isinstance(r, SendResult)
        assert r.success is True
        assert r.message_id == "3"
        assert r.continuation_message_ids == ("2", "3")
        assert r.raw_response is None

    def test_first_chunk_edit_failure_is_success_false(self):
        async def main():
            async def boom(chunk):
                raise RuntimeError("edit dead")

            return await overflow_split_and_deliver(
                ["a", "b"],
                original_message_id="1",
                edit_first=boom,
                send_continuation=_ids("2"),
                adapter_name="t",
            )

        r = _run(main())
        assert r.success is False
        assert "edit dead" in r.error
        assert r.raw_response is None

    def test_empty_chunks_is_noop_success(self):
        async def main():
            return await overflow_split_and_deliver(
                [],
                original_message_id="1",
                edit_first=_ok(None),
                send_continuation=_ids("2"),
            )

        r = _run(main())
        assert r.success is True
        assert r.message_id == "1"

    def test_partial_defaults_to_success_true(self):
        async def main():
            async def send(chunk, prev):
                if chunk == "b":
                    return "2"
                raise RuntimeError("send dead")

            return await overflow_split_and_deliver(
                ["a", "b", "c"],
                original_message_id="1",
                edit_first=_ok(None),
                send_continuation=send,
                adapter_name="t",
            )

        r = _run(main())
        assert r.success is True
        assert r.message_id == "2"
        assert r.raw_response["partial_overflow"] is True
        assert r.raw_response["delivered_chunks"] == 2
        assert r.raw_response["total_chunks"] == 3
        assert r.raw_response["last_message_id"] == "2"
        assert r.continuation_message_ids == ("2",)


class TestPartialFailureContract:
    def test_partial_success_false_is_strict_failure(self):
        async def main():
            async def send(chunk, prev):
                if chunk == "b":
                    return "2"
                raise RuntimeError("send dead")

            return await overflow_split_and_deliver(
                ["a", "b", "c"],
                original_message_id="1",
                edit_first=_ok(None),
                send_continuation=send,
                adapter_name="t",
                partial_success=False,
            )

        r = _run(main())
        assert r.success is False
        assert r.error == "overflow_continuation_failed"
        assert r.retryable is True
        assert r.message_id == "2"
        assert r.raw_response["partial_overflow"] is True
        assert r.raw_response["last_message_id"] == "2"
        assert r.continuation_message_ids == ("2",)

    def test_delivered_prefix_fn_rides_the_partial_payload(self):
        seen = {}

        async def main():
            async def send(chunk, prev):
                if chunk == "b":
                    return "2"
                raise RuntimeError("send dead")

            def prefix(delivered):
                seen["chunks"] = list(delivered)
                return "ab"

            return await overflow_split_and_deliver(
                ["a", "b", "c"],
                original_message_id="1",
                edit_first=_ok(None),
                send_continuation=send,
                delivered_prefix_fn=prefix,
            )

        r = _run(main())
        # The renderer sees only what the user actually has: chunk 1 + the
        # continuations that landed.
        assert seen["chunks"] == ["a", "b"]
        assert r.raw_response["delivered_prefix"] == "ab"


class TestContinuationThreading:
    def test_continuation_receives_previous_id(self):
        got = []

        async def main():
            async def send(chunk, prev):
                got.append((chunk, prev))
                return f"next-{chunk}"

            return await overflow_split_and_deliver(
                ["a", "b", "c"],
                original_message_id="1",
                edit_first=_ok(None),
                send_continuation=send,
            )

        _run(main())
        assert got == [("b", "1"), ("c", "next-b")]

    def test_none_continuation_id_keeps_original_threading(self):
        async def main():
            return await overflow_split_and_deliver(
                ["a", "b"],
                original_message_id="1",
                edit_first=_ok(None),
                send_continuation=_ok(None),
            )

        r = _run(main())
        assert r.success is True
        assert r.message_id == "1"
        assert r.continuation_message_ids == ()


def _ok(value):
    async def call(*args, **kwargs):
        return value
    return call


def _ids(*ids):
    iterator = iter(ids)

    async def send(chunk, prev):
        return next(iterator)
    return send
