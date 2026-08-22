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


class TestBindCallbacks:
    def test_binds_present_keys_onto_agent(self):
        calls: list[str] = []

        class _Agent:
            pass

        agent = _Agent()
        tc.bind_callbacks(
            agent,
            {
                "tool_progress_callback": lambda *a, **k: calls.append("progress"),
                "thinking_callback": lambda text: calls.append("think"),
            },
        )
        assert agent.tool_progress_callback is not None
        assert agent.thinking_callback is not None
        agent.tool_progress_callback("tool.started", "x", None, None)
        agent.thinking_callback("...")
        assert calls == ["progress", "think"]

    def test_missing_keys_are_left_untouched(self):
        class _Agent:
            tool_progress_callback = "existing"

        agent = _Agent()
        tc.bind_callbacks(agent, {"thinking_callback": lambda text: None})
        assert agent.tool_progress_callback == "existing"
        assert agent.thinking_callback is not None

    def test_builder_filters_absent_keys(self):
        kwargs = tc.build_agent_init_callback_kwargs(
            {"tool_progress_callback": lambda *a, **k: None}
        )
        assert set(kwargs) == {"tool_progress_callback"}


class TestCliCallbackSignature:
    """The CLI's tool_progress callback uses canonical parameter names.

    Regression: cli._on_tool_progress used function_name/function_args while
    agent_init and the tui gateway use name/args — identical positions,
    divergent spellings, invisible drift (C1)."""