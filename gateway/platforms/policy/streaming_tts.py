"""Streaming-TTS format descriptor and turn-suppression policy.

Extracted verbatim from ``gateway.platforms.base`` (issue #22 expand step).
"""

import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))
from dataclasses import dataclass
from dataclasses import field
from typing import Any

# ---------------------------------------------------------------------------
# Streaming TTS format descriptor and handle (#60671)
# ---------------------------------------------------------------------------

@dataclass
class AudioFormat:
    """Declared PCM format for a streaming-TTS session.

    All chunks delivered via ``write_streaming_tts`` must conform to this
    format: raw little-endian PCM at the declared sample rate, channels,
    and sample width.
    """
    sample_rate: int = 24000
    channels: int = 1
    sample_width: int = 2  # bytes per sample (int16 = 2)


@dataclass
class StreamingTTSHandle:
    """Opaque handle returned by ``begin_streaming_tts``.

    Adapters may subclass or extend this with platform-specific state
    (track IDs, buffers, etc.).  The base fields are used by the consumer
    for bookkeeping and cancellation.
    """
    chat_id: str = ""
    audio_format: AudioFormat = field(default_factory=AudioFormat)
    # Set to True after the first PCM chunk has been written (audible output
    # has started).  The consumer uses this to decide whether a failure
    # should fall back to whole-file TTS (not yet audible) or just end
    # cleanly (already audible — don't replay from the beginning).
    audible: bool = False
    # Set to True by abort_streaming_tts; late chunks are dropped.
    aborted: bool = False


def streaming_tts_turn_key(session_key: str | None, turn_marker: Any = None, *, event: Any = None) -> str | None:
    """Return a per-turn streaming-TTS suppression key.

    The key is intentionally turn-scoped, not chat-scoped, so overlapping
    turns in the same chat cannot suppress each other's fallback paths.
    ``turn_marker`` is usually the gateway run generation; if that is absent
    we fall back to the current event's message/update identifiers.
    """
    if not session_key:
        return None
    if turn_marker is None and event is not None:
        turn_marker = getattr(event, "message_id", None) or getattr(event, "platform_update_id", None)
    if turn_marker is None:
        return None
    return f"{session_key}:{turn_marker}"


def streaming_tts_should_skip_whole_file(
    completed_turns: set[str],
    session_key: str | None,
    turn_marker: Any = None,
    *,
    event: Any = None,
) -> bool:
    """Pure helper used by the auto-TTS suppression path.

    Keeps the suppression decision turn-scoped and testable without
    exercising the whole adapter method stack.
    """
    turn_key = streaming_tts_turn_key(session_key, turn_marker, event=event)
    return bool(turn_key and turn_key in completed_turns)
