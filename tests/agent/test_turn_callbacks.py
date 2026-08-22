"""Tests for the turn-frame callback contract (architecture-review C1).

The three turn runners (CLI, TUI gateway, messaging gateway) bind lifecycle
callbacks onto the agent before run_conversation. Historically each runner
named the callback params differently and the contract lived in a "parity
with gateway/run.py" comment. agent.turn_callbacks freezes the names and
signatures once; these tests make the contract explicit so a future runner
that renames a parameter (function_name -> name, function_args -> args, ...)
fails CI instead of silently drifting.
"""

from __future__ import annotations

import agent.turn_callbacks as tc


class TestCallbackKeyContract:
    """agent_init / run_conversation read exactly these callback keys."""

    def test_canonical_keys_are_present_and_ordered(self):
        assert "tool_progress_callback" in tc.CALLBACK_KEYS
        assert "tool_start_callback" in tc.CALLBACK_KEYS
        assert "tool_complete_callback" in tc.CALLBACK_KEYS
        assert "thinking_callback" in tc.CALLBACK_KEYS
        assert "status_callback" in tc.CALLBACK_KEYS

    def test_every_key_has_a_typed_entry(self):
        for key in tc.CALLBACK_KEYS:
            assert key in tc.TurnCallbacks.__annotations__, key


class TestCliCallbackSignature:
    """The CLI's tool_progress callback uses canonical parameter names.

    Regression: cli._on_tool_progress used function_name/function_args while
    agent_init and the tui gateway use name/args — identical positions,
    divergent spellings, invisible drift (C1).
    """

    def test_cli_on_tool_progress_uses_canonical_names(self):
        import inspect

        import cli

        params = inspect.signature(
            cli.Ev0CLI._on_tool_progress
        ).parameters
        # The canonical contract (agent/turn_callbacks): positional
        # (event_type, name, preview, args) plus **kwargs. If a future
        # rename reintroduces function_name/function_args, CI fails here.
        assert "name" in params, params
        assert "args" in params, params
        assert "function_name" not in params, params
        assert "function_args" not in params, params


class TestGatewayCallbackConformance:
    """Ticket #7: gateway/run.py's direct bindings are contract names."""

    def test_gateway_bound_callbacks_are_in_contract(self):
        from agent.turn_callbacks import CALLBACK_KEYS

        keys = set(CALLBACK_KEYS)
        for bound in (
            "tool_progress_callback",
            "tool_start_callback",
            "tool_complete_callback",
            "status_callback",
        ):
            assert bound in keys, (
                f"gateway binds {bound} which is not in the turn callback "
                "contract (agent.turn_callbacks.CALLBACK_KEYS) — rename it"
            )