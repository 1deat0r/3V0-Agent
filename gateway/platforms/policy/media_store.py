"""Per-kind media cache directories and bytes/url caching helpers.

Extracted verbatim from ``gateway.platforms.base`` (issue #22 expand step).
"""

import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))
from dataclasses import dataclass
from pathlib import Path
from threev0_constants import get_threev0_dir
from typing import Optional
import asyncio
import logging
import os
import re
import uuid
from gateway.platforms.policy import inbound_media as _inbound_media
from gateway.platforms.policy import media_types as _media_types
from gateway.platforms.policy import net as _net

# ---------------------------------------------------------------------------
# Image cache utilities
#
# When users send images on messaging platforms, we download them to a local
# cache directory so they can be analyzed by the vision tool (which accepts
# local file paths). This avoids issues with ephemeral platform URLs
# (e.g. Telegram file URLs expire after ~1 hour).
# ---------------------------------------------------------------------------

# Import-time default. Tests monkeypatch this; the get_*_cache_dir() getters
# re-resolve per call so the active profile override is honored.
IMAGE_CACHE_DIR = get_threev0_dir("cache/images", "image_cache")


def _resolve_cache_dir(constant_name: str, new_subpath: str, old_name: str) -> Path:
    """Resolve fresh via get_ev0_dir (active profile), unless a test has
    monkeypatched the constant away from its import-time default."""
    fresh = get_threev0_dir(new_subpath, old_name)
    current = globals().get(constant_name)
    default = _CACHE_DIR_IMPORT_DEFAULTS.get(constant_name)
    if current is not None and default is not None and current != default:
        return Path(current)
    return fresh


def get_image_cache_dir() -> Path:
    """Return the image cache directory, creating it if it doesn't exist."""
    d = _resolve_cache_dir("IMAGE_CACHE_DIR", "cache/images", "image_cache")
    d.mkdir(parents=True, exist_ok=True)
    return d


def _looks_like_image(data: bytes) -> bool:
    """Return True if *data* starts with a known image magic-byte sequence."""
    if len(data) < 4:
        return False
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    if data[:3] == b"\xff\xd8\xff":
        return True
    if data[:6] in {b"GIF87a", b"GIF89a"}:
        return True
    if data[:2] == b"BM":
        return True
    if data[:4] == b"RIFF" and len(data) >= 12 and data[8:12] == b"WEBP":
        return True
    return False


def cache_image_from_bytes(data: bytes, ext: str = ".jpg") -> str:
    """
    Save raw image bytes to the cache and return the absolute file path.

    Args:
        data: Raw image bytes.
        ext:  File extension including the dot (e.g. ".jpg", ".png").

    Returns:
        Absolute path to the cached image file as a string.

    Raises:
        ValueError: If *data* does not look like a valid image (e.g. an HTML
            error page returned by the upstream server).
    """
    _inbound_media.validate_inbound_media_size(len(data), media_type="image")
    if not _looks_like_image(data):
        snippet = data[:80].decode("utf-8", errors="replace")
        raise ValueError(
            f"Refusing to cache non-image data as {ext} "
            f"(starts with: {snippet!r})"
        )
    cache_dir = get_image_cache_dir()
    filename = f"img_{uuid.uuid4().hex[:12]}{ext}"
    filepath = cache_dir / filename
    filepath.write_bytes(data)
    return str(filepath)


async def cache_image_from_url(url: str, ext: str = ".jpg", retries: int = 2) -> str:
    """
    Download an image from a URL and save it to the local cache.

    Retries on transient failures (timeouts, 429, 5xx) with exponential
    backoff so a single slow CDN response doesn't lose the media.

    Args:
        url: The HTTP/HTTPS URL to download from.
        ext: File extension including the dot (e.g. ".jpg", ".png").
        retries: Number of retry attempts on transient failures.

    Returns:
        Absolute path to the cached image file as a string.

    Raises:
        ValueError: If the URL targets a private/internal network (SSRF protection).
    """
    from tools.url_safety import create_ssrf_safe_async_client, is_safe_url
    if not is_safe_url(url):
        raise ValueError(f"Blocked unsafe URL (SSRF protection): {_net.safe_url_for_log(url)}")

    import httpx
    _log = logging.getLogger(__name__)

    async with create_ssrf_safe_async_client(
        timeout=30.0,
        follow_redirects=True,
        event_hooks={"response": [_net._ssrf_redirect_guard]},
    ) as client:
        for attempt in range(retries + 1):
            try:
                async with client.stream(
                    "GET",
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; Ev0Agent/1.0)",
                        "Accept": "image/*,*/*;q=0.8",
                    },
                ) as response:
                    response.raise_for_status()
                    content = await _inbound_media._read_httpx_body_with_limit(
                        response, media_type="image",
                    )
                return cache_image_from_bytes(content, ext)
            except (httpx.TimeoutException, httpx.HTTPStatusError) as exc:
                if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 429:
                    raise
                if attempt < retries:
                    wait = 1.5 * (attempt + 1)
                    _log.debug(
                        "Media cache retry %d/%d for %s (%.1fs): %s",
                        attempt + 1,
                        retries,
                        _net.safe_url_for_log(url),
                        wait,
                        exc,
                    )
                    await asyncio.sleep(wait)
                    continue
                raise


def _cleanup_cache_dir(cache_dir: Path, max_age_hours: int) -> int:
    """
    Delete files in *cache_dir* older than *max_age_hours*.

    Shared implementation behind every ``cleanup_*_cache`` helper — one loop,
    not N copies.  Returns the number of files removed.
    """
    import time

    cutoff = time.time() - (max_age_hours * 3600)
    removed = 0
    for f in cache_dir.iterdir():
        if f.is_file() and f.stat().st_mtime < cutoff:
            try:
                f.unlink()
                removed += 1
            except OSError:
                pass
    return removed


def cleanup_image_cache(max_age_hours: int = 24) -> int:
    """
    Delete cached images older than *max_age_hours*.

    Returns the number of files removed.
    """
    return _cleanup_cache_dir(get_image_cache_dir(), max_age_hours)


# ---------------------------------------------------------------------------
# Audio cache utilities
#
# Same pattern as image cache -- voice messages from platforms are downloaded
# here so the STT tool (OpenAI Whisper) can transcribe them from local files.
# ---------------------------------------------------------------------------

AUDIO_CACHE_DIR = get_threev0_dir("cache/audio", "audio_cache")


def get_audio_cache_dir() -> Path:
    """Return the audio cache directory, creating it if it doesn't exist."""
    d = _resolve_cache_dir("AUDIO_CACHE_DIR", "cache/audio", "audio_cache")
    d.mkdir(parents=True, exist_ok=True)
    return d


def _sniff_audio_ext(data: bytes, fallback_ext: str) -> str:
    """Prefer a container-matching extension when audio magic bytes are obvious.

    Thin wrapper around the shared sniffer in ``tools.audio_container`` —
    ONE module owns container detection for both the outbound TTS repair
    (``tools/tts_tool.py``) and this inbound cache path.
    """
    from tools.audio_container import sniff_audio_ext

    return sniff_audio_ext(data, fallback_ext)


def cache_audio_from_bytes(data: bytes, ext: str = ".ogg") -> str:
    """
    Save raw audio bytes to the cache and return the absolute file path.

    Args:
        data: Raw audio bytes.
        ext:  File extension including the dot (e.g. ".ogg", ".mp3").

    Returns:
        Absolute path to the cached audio file as a string.
    """
    _inbound_media.validate_inbound_media_size(len(data), media_type="audio")
    cache_dir = get_audio_cache_dir()
    sniffed_ext = _sniff_audio_ext(data, ext)
    filename = f"audio_{uuid.uuid4().hex[:12]}{sniffed_ext}"
    filepath = cache_dir / filename
    filepath.write_bytes(data)
    return str(filepath)


async def cache_audio_from_url(url: str, ext: str = ".ogg", retries: int = 2) -> str:
    """
    Download an audio file from a URL and save it to the local cache.

    Retries on transient failures (timeouts, 429, 5xx) with exponential
    backoff so a single slow CDN response doesn't lose the media.

    Args:
        url: The HTTP/HTTPS URL to download from.
        ext: File extension including the dot (e.g. ".ogg", ".mp3").
        retries: Number of retry attempts on transient failures.

    Returns:
        Absolute path to the cached audio file as a string.

    Raises:
        ValueError: If the URL targets a private/internal network (SSRF protection).
    """
    from tools.url_safety import create_ssrf_safe_async_client, is_safe_url
    if not is_safe_url(url):
        raise ValueError(f"Blocked unsafe URL (SSRF protection): {_net.safe_url_for_log(url)}")

    import httpx
    _log = logging.getLogger(__name__)

    async with create_ssrf_safe_async_client(
        timeout=30.0,
        follow_redirects=True,
        event_hooks={"response": [_net._ssrf_redirect_guard]},
    ) as client:
        for attempt in range(retries + 1):
            try:
                async with client.stream(
                    "GET",
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; Ev0Agent/1.0)",
                        "Accept": "audio/*,*/*;q=0.8",
                    },
                ) as response:
                    response.raise_for_status()
                    content = await _inbound_media._read_httpx_body_with_limit(
                        response, media_type="audio",
                    )
                return cache_audio_from_bytes(content, ext)
            except (httpx.TimeoutException, httpx.HTTPStatusError) as exc:
                if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 429:
                    raise
                if attempt < retries:
                    wait = 1.5 * (attempt + 1)
                    _log.debug(
                        "Audio cache retry %d/%d for %s (%.1fs): %s",
                        attempt + 1,
                        retries,
                        _net.safe_url_for_log(url),
                        wait,
                        exc,
                    )
                    await asyncio.sleep(wait)
                    continue
                raise


def cleanup_audio_cache(max_age_hours: int = 24) -> int:
    """
    Delete cached audio files older than *max_age_hours*.

    Returns the number of files removed.
    """
    return _cleanup_cache_dir(get_audio_cache_dir(), max_age_hours)


# ---------------------------------------------------------------------------
# Video cache utilities
#
# Same pattern as image/audio cache -- videos from platforms are downloaded
# here so the agent can reference them by local file path.
# ---------------------------------------------------------------------------

VIDEO_CACHE_DIR = get_threev0_dir("cache/videos", "video_cache")


def get_video_cache_dir() -> Path:
    """Return the video cache directory, creating it if it doesn't exist."""
    d = _resolve_cache_dir("VIDEO_CACHE_DIR", "cache/videos", "video_cache")
    d.mkdir(parents=True, exist_ok=True)
    return d


def cache_video_from_bytes(data: bytes, ext: str = ".mp4") -> str:
    """Save raw video bytes to the cache and return the absolute file path."""
    _inbound_media.validate_inbound_media_size(len(data), media_type="video")
    cache_dir = get_video_cache_dir()
    filename = f"video_{uuid.uuid4().hex[:12]}{ext}"
    filepath = cache_dir / filename
    filepath.write_bytes(data)
    return str(filepath)


def cleanup_video_cache(max_age_hours: int = 24) -> int:
    """
    Delete cached videos older than *max_age_hours*.

    Returns the number of files removed.
    """
    return _cleanup_cache_dir(get_video_cache_dir(), max_age_hours)


# ---------------------------------------------------------------------------
# Document cache utilities
#
# Same pattern as image/audio cache -- documents from platforms are downloaded
# here so the agent can reference them by local file path.
# ---------------------------------------------------------------------------

DOCUMENT_CACHE_DIR = get_threev0_dir("cache/documents", "document_cache")


SCREENSHOT_CACHE_DIR = get_threev0_dir("cache/screenshots", "browser_screenshots")


def get_screenshot_cache_dir() -> Path:
    """Return the browser screenshot cache directory, creating it if needed."""
    d = _resolve_cache_dir("SCREENSHOT_CACHE_DIR", "cache/screenshots", "browser_screenshots")
    d.mkdir(parents=True, exist_ok=True)
    return d


def cleanup_screenshot_cache(max_age_hours: int = 24) -> int:
    """
    Delete cached browser screenshots older than *max_age_hours*.

    Returns the number of files removed.
    """
    return _cleanup_cache_dir(get_screenshot_cache_dir(), max_age_hours)


# Import-time defaults; _resolve_cache_dir compares against these to tell a
# test monkeypatch from an unmodified constant.
_CACHE_DIR_IMPORT_DEFAULTS = {
    "IMAGE_CACHE_DIR": IMAGE_CACHE_DIR,
    "AUDIO_CACHE_DIR": AUDIO_CACHE_DIR,
    "VIDEO_CACHE_DIR": VIDEO_CACHE_DIR,
    "DOCUMENT_CACHE_DIR": DOCUMENT_CACHE_DIR,
    "SCREENSHOT_CACHE_DIR": SCREENSHOT_CACHE_DIR,
}


def get_document_cache_dir() -> Path:
    """Return the document cache directory, creating it if it doesn't exist."""
    d = _resolve_cache_dir("DOCUMENT_CACHE_DIR", "cache/documents", "document_cache")
    d.mkdir(parents=True, exist_ok=True)
    return d


def cache_document_from_bytes(data: bytes, filename: str) -> str:
    """
    Save raw document bytes to the cache and return the absolute file path.

    The cached filename preserves the original human-readable name with a
    unique prefix: ``doc_{uuid12}_{original_filename}``.

    Args:
        data: Raw document bytes.
        filename: Original filename (e.g. "report.pdf").

    Returns:
        Absolute path to the cached document file as a string.

    Raises:
        ValueError: If the sanitized path escapes the cache directory.
    """
    cache_dir = get_document_cache_dir()
    # Sanitize: strip directory components, null bytes, and control characters
    safe_name = Path(filename).name if filename else "document"
    safe_name = safe_name.replace("\x00", "").strip()
    if not safe_name or safe_name in {".", ".."}:
        safe_name = "document"
    cached_name = f"doc_{uuid.uuid4().hex[:12]}_{safe_name}"
    filepath = cache_dir / cached_name
    # Final safety check: ensure path stays inside cache dir
    if not filepath.resolve().is_relative_to(cache_dir.resolve()):
        raise ValueError(f"Path traversal rejected: {filename!r}")
    filepath.write_bytes(data)
    return str(filepath)


def cleanup_document_cache(max_age_hours: int = 24) -> int:
    """
    Delete cached documents older than *max_age_hours*.

    Returns the number of files removed.
    """
    return _cleanup_cache_dir(get_document_cache_dir(), max_age_hours)


# ---------------------------------------------------------------------------
# Unified media caching
#
# One entry point for "I have raw attachment bytes from a platform — cache them
# and tell me what I got." Classifies by extension/MIME against the shared
# registries above, routes to the right cache_*_from_bytes helper, and returns
# a small result the caller can store and/or describe in a transcript. Used by
# both the addressed-message path and the observed-group-context path, on any
# platform — not Telegram-specific.
# ---------------------------------------------------------------------------

@dataclass
class CachedMedia:
    """Result of caching one attachment's bytes."""

    path: str                 # absolute cache path, agent-visible (sandbox-translated)
    media_type: str           # MIME type recorded on the MessageEvent
    kind: str                 # "image" | "video" | "audio" | "document"
    display_name: str         # human-readable name for transcript notes

    def context_note(self) -> str:
        """One-line transcript annotation pointing the agent at the file."""
        return f"[{self.kind} '{self.display_name}' saved at: {self.path}]"


def _resolve_media_ext(filename: str, mime_type: str) -> str:
    """Best-effort file extension from filename, then MIME fallback."""
    if filename:
        ext = os.path.splitext(filename)[1].lower()
        if ext:
            return ext
    mime = (mime_type or "").lower()
    if not mime:
        return ""
    for table in (
        _media_types.SUPPORTED_IMAGE_DOCUMENT_TYPES,
        _media_types.SUPPORTED_VIDEO_TYPES,
        _media_types.SUPPORTED_DOCUMENT_TYPES,
    ):
        for ext, m in table.items():
            if m == mime:
                return ext
    return ""


def cache_media_bytes(
    data: bytes,
    *,
    filename: str = "",
    mime_type: str = "",
    default_kind: Optional[str] = None,
) -> Optional[CachedMedia]:
    """Classify and cache raw attachment bytes; return a CachedMedia or None.

    ``default_kind`` ("image"/"video"/"audio"/"document") biases classification
    when the extension/MIME are ambiguous — e.g. a Telegram native photo whose
    file has no usable name. Any non-image/video/audio file is cached as a
    document and surfaced to the agent (arbitrary types get
    ``application/octet-stream``); only images that fail validation
    (``cache_image_from_bytes`` raises ValueError) return None.
    """
    from tools.credential_files import to_agent_visible_cache_path

    ext = _resolve_media_ext(filename, mime_type)
    mime = (mime_type or "").lower()
    display = re.sub(r"[^\w.\- ]", "_", filename) if filename else (ext.lstrip(".") or "file")

    is_image = (
        mime.startswith("image/")
        or ext in _media_types.SUPPORTED_IMAGE_DOCUMENT_TYPES
        or default_kind == "image"
    )
    is_video = mime.startswith("video/") or ext in _media_types.SUPPORTED_VIDEO_TYPES or default_kind == "video"
    is_audio = mime.startswith("audio/") or ext in _media_types._AUDIO_EXTS or default_kind == "audio"

    if is_image:
        img_ext = ext if ext in _media_types.SUPPORTED_IMAGE_DOCUMENT_TYPES else ".jpg"
        try:
            path = cache_image_from_bytes(data, ext=img_ext)
        except ValueError:
            return None
        out_mime = mime if mime.startswith("image/") else _media_types.SUPPORTED_IMAGE_DOCUMENT_TYPES.get(img_ext, "image/jpeg")
        return CachedMedia(to_agent_visible_cache_path(path), out_mime, "image", display)

    if is_video:
        vid_ext = ext if ext in _media_types.SUPPORTED_VIDEO_TYPES else ".mp4"
        path = cache_video_from_bytes(data, ext=vid_ext)
        return CachedMedia(to_agent_visible_cache_path(path), _media_types.SUPPORTED_VIDEO_TYPES.get(vid_ext, "video/mp4"), "video", display)

    if is_audio:
        aud_ext = ext if ext in _media_types._AUDIO_EXTS else ".ogg"
        path = cache_audio_from_bytes(data, ext=aud_ext)
        out_mime = mime if mime.startswith("audio/") else _media_types._AUDIO_MIME_TYPES[aud_ext]
        return CachedMedia(to_agent_visible_cache_path(path), out_mime, "audio", display)

    # Any other file type is cached and surfaced to the agent as a local path
    # so it can be inspected with terminal / read_file / etc. Authorization to
    # talk to the agent is the gate that matters — once a user is allowed to
    # message it, the file-extension allowlist must not silently drop their
    # uploads. Known extensions keep their precise MIME; everything else is
    # tagged application/octet-stream (or the caller-supplied MIME) so the
    # agent knows it's an arbitrary file and reaches for terminal tools.
    fallback_name = filename or (f"document{ext}" if ext else "document.bin")
    path = cache_document_from_bytes(data, fallback_name)
    if ext in _media_types.SUPPORTED_DOCUMENT_TYPES:
        out_mime = _media_types.SUPPORTED_DOCUMENT_TYPES[ext]
    else:
        out_mime = mime if mime else "application/octet-stream"
    return CachedMedia(to_agent_visible_cache_path(path), out_mime, "document", display or fallback_name)
