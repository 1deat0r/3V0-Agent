"""Inbound media size limits and bounded httpx body reads.

Extracted verbatim from ``gateway.platforms.base`` (issue #22 expand step).
"""

import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))
from typing import Optional
import logging
logger = logging.getLogger("gateway.platforms.base")

# ---------------------------------------------------------------------------
# Inbound media size cap (#13145)
#
# Inbound image / audio / video payloads are buffered fully into process
# memory before being written to the cache directory. With no cap, a single
# large upload (Discord Nitro allows 500 MB) — or a remote URL in an inbound
# message payload pointing at an arbitrarily large file — can spike RAM and
# OOM-kill the gateway. The ``cache_*_from_bytes`` helpers (the shared funnel
# every platform reaches eventually) and the ``cache_*_from_url`` downloaders
# enforce this cap, so the protection holds regardless of which platform
# adapter or code path produced the bytes.
#
# Configurable via ``gateway.max_inbound_media_bytes`` in config.yaml.
# ``0`` disables the cap. Default 128 MiB — generous enough for ordinary
# photos/voice notes/short clips while still bounding a hostile upload.
# ---------------------------------------------------------------------------
DEFAULT_INBOUND_MEDIA_MAX_BYTES = 128 * 1024 * 1024


def get_inbound_media_max_bytes() -> int:
    """Return the max inbound image/audio/video bytes allowed in memory.

    Reads ``gateway.max_inbound_media_bytes`` from config.yaml. ``0`` (or a
    negative / unparseable value) disables the cap. Non-fatal if config is
    unreadable — falls back to the default.
    """
    try:
        from threev0_cli.config import load_config_readonly as _load_config
        cfg = _load_config()  # read-only: .get() only, never mutated
    except Exception:
        return DEFAULT_INBOUND_MEDIA_MAX_BYTES
    gw = cfg.get("gateway", {}) if isinstance(cfg, dict) else {}
    if not isinstance(gw, dict) or "max_inbound_media_bytes" not in gw:
        return DEFAULT_INBOUND_MEDIA_MAX_BYTES
    try:
        return int(gw["max_inbound_media_bytes"])
    except (TypeError, ValueError):
        return DEFAULT_INBOUND_MEDIA_MAX_BYTES


def validate_inbound_media_size(
    size: int,
    *,
    media_type: str = "media",
    max_bytes: Optional[int] = None,
) -> None:
    """Raise ``ValueError`` if an inbound media payload exceeds the cap.

    A ``max_bytes`` of ``0`` (or the configured cap resolving to ``0``)
    disables the check entirely. Passing ``max_bytes`` lets callers resolve
    the limit once and reuse it across an incremental read.
    """
    limit = get_inbound_media_max_bytes() if max_bytes is None else max_bytes
    if limit and size > limit:
        raise ValueError(
            f"Inbound {media_type} payload is too large "
            f"({size} bytes > {limit} bytes)"
        )


async def _read_httpx_body_with_limit(response, *, media_type: str) -> bytes:
    """Read an httpx streaming response body without exceeding the media cap.

    Rejects early on an oversized ``Content-Length`` header, then re-checks
    the running total as chunks arrive so a lying/absent header can't smuggle
    an unbounded body past the cap.
    """
    max_bytes = get_inbound_media_max_bytes()
    content_length = response.headers.get("content-length")
    if content_length:
        try:
            declared_size = int(content_length)
        except ValueError:
            logger.debug(
                "Ignoring invalid Content-Length for inbound %s: %r",
                media_type, content_length,
            )
        else:
            validate_inbound_media_size(
                declared_size, media_type=media_type, max_bytes=max_bytes,
            )

    chunks: list[bytes] = []
    total = 0
    async for chunk in response.aiter_bytes():
        total += len(chunk)
        validate_inbound_media_size(total, media_type=media_type, max_bytes=max_bytes)
        chunks.append(chunk)
    return b"".join(chunks)
