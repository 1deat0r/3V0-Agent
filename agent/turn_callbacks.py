"""Turn-frame callback contract (architecture-review pass 2, C1).

The three agent-turn runners — ``cli.py`` (Ev0CLI), ``tui_gateway/server.py``
(worker-thread bridge) and ``gateway/run.py`` (TurnRunner) — each wire a set
of lifecycle callbacks onto the agent object before calling
``agent.conversation_loop.run_conversation``. Historically each runner named
those callbacks differently (``function_name`` vs ``name``, ``function_args``
vs ``args``) and the contract lived only in a "parity with gateway/run.py"
comment. That drift is exactly what this module eliminates: the callback
names and signatures are declared ONCE here; every runner imports
:data:`CALLBACK_KEYS` / the :class:`TurnCallbacks` TypedDict and binds
through it.

Design intent (deep module): the contract is small — one TypedDict, one
invariant, one builder — while the per-runner implementations (rendering,
spooling, IPC) stay behind each runner's own interface. Callers get
*leverage* (one contract, N runners), maintainers get *locality* (a new
callback is added here, not re-invented three times).

Vocabulary: the callbacks are the seam between the turn-loop implementation
(agent.conversation_loop) and the adapters (CLI / TUI / gateway) that render
loop events for their surface.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional, TypedDict

# ── The contract ─────────────────────────────────────────────────────────
# Each runner binds these names onto the agent instance (or passes them in an
# agent-init kwargs dict). The signature of each callback is frozen here;
# runners MUST NOT rename parameters (e.g. `function_name` -> `name`) — the
# codebase-style deviation is exactly the bug this module exists to prevent.

#: tool_start_callback(tool_call_id: str, name: str, args: dict)
ToolStartCallback = Callable[[str, str, Dict[str, Any]], Any]
#: tool_complete_callback(tool_call_id, name, args, result)
ToolCompleteCallback = Callable[
    [str, str, Dict[str, Any], Any], Any
]
#: tool_progress_callback(event_type, name, preview, args, **kwargs)
#: event_type values: tool.started, tool.completed, reasoning.available, ...
ToolProgressCallback = Callable[
    [str, Optional[str], Optional[str], Optional[Dict[str, Any]]], Any
]
#: tool_gen_callback(name) — fired when a tool starts generating output.
ToolGenCallback = Callable[[str], Any]
#: thinking_callback(text) — assistant scratch/thinking deltas.
ThinkingCallback = Callable[[str], Any]
#: status_callback(event_type, message) — lifecycle status changes.
StatusCallback = Callable[[str, str], Any]
#: stream_callback(text) — text delta during streaming (TTS pre-start).
StreamCallback = Callable[[str], Any]
#: voice_ack_callback(call_id, tool_name, args) — one-shot voice ack.
VoiceAckCallback = Callable[[str, str, Dict[str, Any]], Any]


class TurnCallbacks(TypedDict, total=False):
    """The full set of callbacks a turn runner may bind.

    ``total=False`` because no runner binds every callback; the contract is
    the *names and signatures*, not a minimum set. Every key here is consumed
    by agent/agent_init.py or agent/conversation_loop.py under this exact
    spelling.
    """

    tool_start_callback: ToolStartCallback
    tool_complete_callback: ToolCompleteCallback
    tool_progress_callback: ToolProgressCallback
    tool_gen_callback: ToolGenCallback
    thinking_callback: ThinkingCallback
    status_callback: StatusCallback
    stream_callback: StreamCallback
    voice_ack_callback: VoiceAckCallback


#: Canonical key names, in bind order. Consumers (agent_init, run_conversation)
#: read exactly these keys; runners constructing a kwargs dict MUST use them.
CALLBACK_KEYS: tuple[str, ...] = (
    "tool_start_callback",
    "tool_complete_callback",
    "tool_progress_callback",
    "tool_gen_callback",
    "thinking_callback",
    "status_callback",
    "stream_callback",
    "voice_ack_callback",
)


def bind_callbacks(
    agent: Any,
    callbacks: TurnCallbacks,
) -> None:
    """Bind the given callbacks onto an agent instance (in place).

    Each runner previously assigned ``agent.tool_progress_callback = ...``
    etc. in its own spelling; this is the single binding site for the
    canonical keys. Missing keys are left untouched so a partially-bound
    agent keeps its existing wiring (e.g. cached-agent reuse).
    """
    for key in CALLBACK_KEYS:
        value = callbacks.get(key)
        if value is not None:
            setattr(agent, key, value)


def build_agent_init_callback_kwargs(
    callbacks: TurnCallbacks,
) -> Dict[str, Any]:
    """Return the callback kwargs accepted by agent-init agent construction.

    Mirrors :func:`bind_callbacks` for the path that constructs a fresh agent
    through agent_init's kwargs dict (the tui_gateway path). Only present
    keys are included.
    """
    return {key: callbacks[key] for key in CALLBACK_KEYS if key in callbacks}