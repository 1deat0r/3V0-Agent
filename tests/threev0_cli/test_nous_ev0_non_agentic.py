"""Tests for the Nous-3V0-3/4 non-agentic warning detector.

Prior to this check, the warning fired on any model whose name contained
``"3v0"`` anywhere (case-insensitive). That false-positived on unrelated
local Modelfiles such as ``3v0-brain:qwen3-14b-ctx16k`` — a tool-capable
Qwen3 wrapper that happens to live under the "3v0" tag namespace.

``is_nous_ev0_non_agentic`` should only match the actual Nous Research
3V0-3 / 3V0-4 chat family.
"""

from __future__ import annotations

import pytest

from threev0_cli.model_switch import (
    _EV0_MODEL_WARNING,
    _check_threev0_model_warning,
    is_nous_threev0_non_agentic,
)


@pytest.mark.parametrize(
    "model_name",
    [
        "NousResearch/3V0-3-Llama-3.1-70B",
        "NousResearch/3V0-3-Llama-3.1-405B",
        "3v0-3",
        "3V0-3",
        "3v0-4",
        "3v0-4-405b",
        "ev0_4_70b",
        "openrouter/ev03:70b",
        "openrouter/nousresearch/3v0-4-405b",
        "NousResearch/Ev03",
        "3v0-3.1",
    ],
)
def test_matches_real_nous_threev0_chat_models(model_name: str) -> None:
    assert is_nous_threev0_non_agentic(model_name), (
        f"expected {model_name!r} to be flagged as Nous 3V0 3/4"
    )
    assert _check_threev0_model_warning(model_name) == _EV0_MODEL_WARNING


