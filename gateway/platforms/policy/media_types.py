"""Media type/extension registries (pure data).

Extracted verbatim from ``gateway.platforms.base`` (issue #22 expand step).
"""

import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))
from typing import Tuple
import re

# Audio file extensions 3V0 recognizes for native audio delivery.
# Keep Telegram's narrower attachment/voice sets below separate: formats such
# as MPEG-2 Layer II are audio to 3V0 but unsupported by sendAudio/sendVoice.
_AUDIO_MIME_TYPES = {
    ".ogg": "audio/ogg",
    ".opus": "audio/opus",
    ".mp3": "audio/mpeg",
    ".m2a": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/m4a",
    ".flac": "audio/flac",
}


_AUDIO_EXTS = frozenset(_AUDIO_MIME_TYPES)


# Telegram's Bot API sendAudio only accepts MP3 / M4A. Other audio
# formats either need to go through sendVoice (Opus/OGG) or must be
# delivered as a regular document.
_TELEGRAM_AUDIO_ATTACHMENT_EXTS = frozenset({'.mp3', '.m4a'})


_TELEGRAM_VOICE_EXTS = frozenset({'.ogg', '.opus'})


SUPPORTED_VIDEO_TYPES = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
    ".mkv": "video/x-matroska",
    ".avi": "video/x-msvideo",
}


SUPPORTED_DOCUMENT_TYPES = {
    ".pdf": "application/pdf",
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".csv": "text/csv",
    ".log": "text/plain",
    ".json": "application/json",
    ".xml": "application/xml",
    ".yaml": "application/yaml",
    ".yml": "application/yaml",
    ".toml": "application/toml",
    ".ini": "text/plain",
    ".cfg": "text/plain",
    ".zip": "application/zip",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".ts": "text/plain",
    ".py": "text/plain",
    ".sh": "text/plain",
}


# ---------------------------------------------------------------------------
# Text-injection extension allowlist
#
# Files whose contents are safe to inline into the prompt (UTF-8 text) when
# small enough. This is intentionally an extension/MIME gate, NOT a blind
# UTF-8 decode: binary formats like PDF/zip/docx can begin with decodable
# ASCII headers and must never be inlined. Any uploaded file is still cached
# and surfaced to the agent regardless of whether it lands in this set —
# this only controls inline-vs-path-pointer for the prompt.
# ---------------------------------------------------------------------------

_TEXT_INJECT_EXTENSIONS = {
    ".txt", ".md", ".markdown", ".csv", ".tsv", ".log",
    ".json", ".jsonl", ".ndjson", ".xml", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".conf", ".env", ".properties",
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".py", ".pyi", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat",
    ".c", ".h", ".cpp", ".cc", ".hpp", ".cs", ".java", ".kt",
    ".go", ".rs", ".rb", ".php", ".pl", ".lua", ".r", ".jl",
    ".swift", ".m", ".scala", ".clj", ".ex", ".exs", ".erl",
    ".sql", ".graphql", ".proto", ".tf", ".hcl",
    ".dockerfile", ".makefile", ".cmake", ".gradle",
    ".rst", ".tex", ".srt", ".vtt", ".diff", ".patch",
}


# ---------------------------------------------------------------------------
# Image document types
#
# Image extensions that platforms may deliver as "documents" rather than
# native photo attachments (Telegram users uploading via the file picker,
# clients that wrap stickers/screenshots as files, etc.). When we see one
# of these, we route the bytes through the image cache and the normal
# vision/photo handling path instead of rejecting them as unsupported
# documents.
# ---------------------------------------------------------------------------

SUPPORTED_IMAGE_DOCUMENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


# ---------------------------------------------------------------------------
# Media-delivery extension allowlist — SINGLE SOURCE OF TRUTH
#
# Both extractors that turn response text into native attachments derive their
# extension set from this tuple:
#   * ``extract_media()``       — explicit ``MEDIA:<path>`` tags
#   * ``extract_local_files()`` — bare absolute/home paths the agent mentions
#
# Historically these two carried independently-maintained extension lists.
# ``extract_media`` had a narrow list (no .md/.json/.yaml/.xml/.html/...) while
# ``extract_local_files`` had a broad one. Combined with the unconditional
# ``MEDIA:\\s*\\S+`` cleanup at the dispatch sites, that mismatch created a
# silent black hole: a ``MEDIA:/report.md`` tag failed the narrow extract_media
# match, got stripped from the body by the loose cleanup regex, and was then
# invisible to extract_local_files — the file was never delivered (issue
# #34517). Keeping one list eliminates the drift; building the cleanup regexes
# from the same set means a tag is only stripped when its extension is one we
# can actually deliver, so an unknown-extension path survives in the body
# instead of vanishing.
#
# Covers images (inline), video (inline where supported), audio (voice/audio),
# documents/spreadsheets/presentations (send_document), archives, and rendered
# web output. The dispatch partition (image vs video vs document) lives in
# ``gateway/run.py``.
# ---------------------------------------------------------------------------

MEDIA_DELIVERY_EXTS: Tuple[str, ...] = (
    # Images (embed inline)
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".svg",
    # Video (embed inline where supported)
    ".mp4", ".mov", ".avi", ".mkv", ".webm", ".3gp",
    # Audio (delivered as voice/audio where supported)
    ".mp3", ".m2a", ".wav", ".ogg", ".opus", ".m4a", ".flac",
    # Documents (uploaded as file attachments)
    ".pdf", ".docx", ".doc", ".odt", ".rtf", ".txt", ".md", ".epub",
    # Spreadsheets / data
    ".xlsx", ".xls", ".ods", ".csv", ".tsv", ".json", ".xml", ".yaml", ".yml",
    # Geospatial / GIS (#24032)
    ".kmz", ".kml", ".geojson", ".gpx",
    # Presentations
    ".pptx", ".ppt", ".odp", ".key",
    # Archives
    ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".apk", ".ipa",
    # Web / rendered output
    ".html", ".htm",
)


# Regex alternation fragment of bare extensions (no leading dot), e.g.
# ``png|jpe?g|...``. ``jpe?g`` collapses jpg/jpeg into one branch. Sorted
# longest-first so the alternation never matches a shorter ext as a prefix of
# a longer one (e.g. ``.tar`` before ``.tar.gz`` components).
_MEDIA_EXT_ALTERNATION = "|".join(
    sorted((e.lstrip(".") for e in MEDIA_DELIVERY_EXTS), key=len, reverse=True)
)


# Anchored ``MEDIA:<path>`` cleanup pattern. Unlike the old loose
# ``MEDIA:\\s*\\S+``, this only strips a tag whose path ends in a known
# deliverable extension (optionally quoted/backticked). A ``MEDIA:`` tag with
# an unknown extension is left in the text so it can still be picked up by the
# bare-path detector (extract_local_files) downstream rather than silently
# deleted. Shared by the non-streaming dispatch path and the streaming
# consumer so both behave identically.
# Path anchors: ``~/`` (Unix home-relative), ``/`` (Unix absolute),
# ``X:\\`` or ``X:/`` (Windows drive-letter absolute — #34632).
# Emphasis tolerance: models routinely wrap the tag in Markdown emphasis
# (``**MEDIA:/x.pdf**``, ``*MEDIA:/x.pdf*``, ``_MEDIA:/x.pdf_``) when they
# present a file to the user. The old single-quote anchor (``[`"']?``) and the
# closing lookahead (which lacked ``*``/``_``) failed to match such tags, so the
# file was silently never delivered and the literal ``MEDIA:`` text leaked into
# the chat. Allow a short run of emphasis/quote markers on both sides so the tag
# is recognised regardless of cosmetic Markdown. Code-block / inline-code /
# blockquote contexts are still neutralised earlier by ``_mask_protected_spans``
# (#35695), so example tags remain non-deliverable.
#
# Both the bare and quoted path forms use non-greedy quantifiers so two
# ``MEDIA:`` tags glued together (``MEDIA:/a.pngMEDIA:/b.png``) or a tag
# followed by stray text don't merge into one invalid path. The trailing
# lookahead also accepts ``MEDIA:`` as a boundary, so the next tag stops
# the current match cleanly (#68773).
#
# Sentence-final punctuation: a ``.`` is accepted as a boundary only when
# followed by whitespace / EOL (``\.(?=\s|$)``) so ``MEDIA:/x/data.csv.``
# at the end of a sentence still extracts ``data.csv``. The whitespace
# guard keeps multi-part extensions intact — for ``archive.tar.gz`` the
# ``.`` after ``tar`` is followed by ``g``, so the match must extend to
# ``.gz`` instead of stopping early at ``.tar``.
# CJK full-width punctuation accepted as MEDIA path terminators, mirroring the
# ASCII set in the looka below. Chinese-language agent output naturally writes
# ``MEDIA:D:\path\早报.pdf（782.6 KB）`` or ``MEDIA:...pdf：内容`` — without
# these, the lookahead fails and the attachment is silently dropped (#88038).
_MEDIA_CJK_TERMINATORS = "（）〈〉《》：，。；！？、\u201c\u201d\u2018\u2019【】"


MEDIA_TAG_CLEANUP_RE = re.compile(
    r'''[`"'*_]{0,3}MEDIA:\s*'''
    r'''(?P<path>`[^`\n]+?`|"[^"\n]+?"|'[^'\n]+?'|'''
    r'''(?:~/|/|[A-Za-z]:[/\\])\S+?(?:[^\S\n]+\S+?)*?\.(?:''' + _MEDIA_EXT_ALTERNATION + r'''))'''
    r'''(?=[\s`"'*_,;:)\]}\[''' + _MEDIA_CJK_TERMINATORS + r''']|MEDIA:|\.(?:\s|$)|$)[`"'*_]{0,3}\.?''',
    re.IGNORECASE,
)


# Paths NOT covered by MEDIA_TAG_CLEANUP_RE's extension alternation — both
# extension-less files (Caddyfile, Dockerfile, Makefile) and files with an
# unknown extension (.py, .log, .weirdext, ...) — are validated and delivered
# via MEDIA_EXTENSIONLESS_TAG_RE. Every ``MEDIA:`` path is therefore
# deliverable regardless of file type (#36060): known extensions extract
# unconditionally via the anchored pattern above, everything else extracts
# only after ``validate_media_delivery_path`` accepts it (exists on disk, not
# under the credential/system denylist, strict-mode rules honored), so
# prompt-injection paths that do not validate are left visible instead of
# silently dropped.
#
# The path class uses a tempered-greedy token (``[^\s\n`"']+?`` followed by
# a ``(?=...)`` lookahead) instead of the prior ``[^\s\n`"']+`` so a
# tag glued to the next ``MEDIA:`` keyword (``MEDIA:/a.pngMEDIA:/b.png``)
# or to arbitrary following text (``MEDIA:/a.pngSome text``) cannot
# silently absorb the next path — that earlier behavior merged the two
# paths into one invalid string and dropped the file (#68773).
#
# The bare form stays non-greedy and whitespace-bounded — spaced paths are
# NOT absorbed at the regex level, because greedy space-tolerance would
# reintroduce the #68773 bug class (gluing the next MEDIA: tag or trailing
# prose into one invalid path). Instead, unknown-extension paths containing
# spaces (``MEDIA:/data/map data.kmz``, ``C:\...\My Documents\x.log``) are
# recovered by ``_match_extensionless_path`` (#24032): when the bare match
# fails validation, the candidate is progressively extended forward across
# single spaces — bounded, stopping at newline / the next ``MEDIA:`` keyword
# — and the first extension that validates on disk wins. Validation is the
# oracle, so prose never rides along and non-existent paths stay visible.
MEDIA_EXTENSIONLESS_TAG_RE = re.compile(
    r'''[`"'*_]{0,3}MEDIA:\s*'''
    r'''(?P<path>`[^`\n]+`|"[^"\n]+"|'[^'\n]+'|'''
    r'''(?:~/|/|[A-Za-z]:[/\\])[^\s\n`"']+?)'''
    r'''(?=[`"'\s,;:)\]}''' + _MEDIA_CJK_TERMINATORS + r''']|MEDIA:|$)'''
    r'''[`"'*_]{0,3}\s*''',
    re.IGNORECASE,
)
