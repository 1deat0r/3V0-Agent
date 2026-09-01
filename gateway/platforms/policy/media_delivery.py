"""Outbound media delivery path policy (roots, denylist, docker mounts, tag stripping).

Extracted verbatim from ``gateway.platforms.base`` (issue #22 expand step).
"""

import sys

from env_compat import branded_env
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))
from pathlib import Path
from threev0_constants import get_default_threev0_root
from threev0_constants import get_threev0_home
from typing import List
from typing import Optional
from typing import Tuple
import os
import re
import time
from gateway.platforms.policy import media_store as _media_store
from gateway.platforms.policy import media_types as _media_types

_EV0_HOME = get_threev0_home()


_EV0_ROOT = get_default_threev0_root()


MEDIA_DELIVERY_ALLOW_DIRS_ENV = "EV0_MEDIA_ALLOW_DIRS"


MEDIA_DELIVERY_TRUST_RECENT_ENV = "EV0_MEDIA_TRUST_RECENT_FILES"


MEDIA_DELIVERY_TRUST_RECENT_SECONDS_ENV = "EV0_MEDIA_TRUST_RECENT_SECONDS"


# Strict mode toggles the original allowlist+recency path-validation behavior.
# Off by default — symmetric with inbound (we accept any document type the
# user uploads), and with the denylist still blocking obvious credential /
# system paths. Operators running public-facing gateways where prompt
# injection from one user could exfiltrate the host's secrets to that same
# user should set this to true.
MEDIA_DELIVERY_STRICT_ENV = "EV0_MEDIA_DELIVERY_STRICT"


MEDIA_DELIVERY_SAFE_ROOTS = (
    _media_store.IMAGE_CACHE_DIR,
    _media_store.AUDIO_CACHE_DIR,
    _media_store.VIDEO_CACHE_DIR,
    _media_store.DOCUMENT_CACHE_DIR,
    _media_store.SCREENSHOT_CACHE_DIR,
    _EV0_HOME / "image_cache",
    _EV0_HOME / "audio_cache",
    _EV0_HOME / "video_cache",
    _EV0_HOME / "document_cache",
    _EV0_HOME / "browser_screenshots",
    # Canonical cache layout — listed alongside the legacy *_cache dirs so
    # generated artifacts deliver on installs that have both (#31733).
    _EV0_HOME / "cache" / "images",
    _EV0_HOME / "cache" / "audio",
    _EV0_HOME / "cache" / "videos",
    _EV0_HOME / "cache" / "documents",
    _EV0_HOME / "cache" / "screenshots",
)


# Default recency window for trusting freshly-produced files (seconds).
# The agent's actual work generally completes well inside 10 minutes; legitimate
# build artifacts (PDFs from pandoc, plots from matplotlib, etc.) almost always
# land seconds before delivery. Old system files (/etc/passwd, ~/.ssh/id_rsa,
# stray credentials) have mtimes measured in days or months — well outside this
# window — so prompt-injection paths pointing at pre-existing host files are
# still rejected.
_MEDIA_DELIVERY_TRUST_RECENT_DEFAULT_SECONDS = 600


# Hard denylist applied even when a path would otherwise pass recency trust.
# These prefixes hold credentials, system state, or process introspection that
# should never be uploaded as a gateway attachment, regardless of how new the
# file looks. The cache-dir allowlist still beats this — an operator-configured
# allowed root can intentionally live under one of these prefixes (rare, but
# their choice).
_MEDIA_DELIVERY_DENIED_PREFIXES = (
    "/etc",
    "/proc",
    "/sys",
    "/dev",
    "/root",
    "/boot",
    "/var/log",
    "/var/lib",
    "/var/run",
)


# Within $HOME we additionally deny common credential / config directories.
# Resolved at check time against the live $HOME so containers and alt-home
# setups work correctly.
_MEDIA_DELIVERY_DENIED_HOME_SUBPATHS = (
    ".ssh",
    ".aws",
    ".gnupg",
    ".kube",
    ".docker",
    ".config",
    ".azure",
    ".gcloud",
    "Library/Keychains",  # macOS
)


# Canonical cache subdirectories that hold deliverable artifacts. Used both
# for the top-level safe roots above and to enumerate per-profile cache roots
# at check time (see _media_delivery_allowed_roots).
_MEDIA_DELIVERY_CACHE_SUBDIRS = (
    "images",
    "audio",
    "videos",
    "documents",
    "screenshots",
)


def _profile_cache_roots() -> List[Path]:
    """Return per-profile canonical cache roots under the shared 3V0 root.

    Profile gateways write generated artifacts to
    ``<root>/profiles/<name>/cache/{images,audio,...}``. The static safe-roots
    list only covers the *active* EV0_HOME's cache, so a gateway running at
    the root (e.g. ``EV0_HOME=/opt/data``) while the model emits a
    profile-scoped path silently fails delivery. Enumerated dynamically at
    check time so profiles created after startup are covered, and so the
    resolved profile path is allowlisted *before* the ``/root`` system denylist
    is consulted (which otherwise wins when EV0_HOME is symlinked under a
    denied prefix and $HOME is not that prefix). See issue #31733.
    """
    roots: List[Path] = []
    profiles_dir = _EV0_ROOT / "profiles"
    try:
        profile_dirs = [p for p in profiles_dir.iterdir() if p.is_dir()]
    except OSError:
        return roots
    for profile_dir in profile_dirs:
        for subdir in _MEDIA_DELIVERY_CACHE_SUBDIRS:
            roots.append(profile_dir / "cache" / subdir)
    return roots


def _kanban_attachment_roots() -> List[Path]:
    """Return durable Kanban attachment roots without importing kanban_db."""
    override = (branded_env("KANBAN_ATTACHMENTS_ROOT") or "").strip()
    if override:
        return [Path(override).expanduser()]
    home_override = (branded_env("KANBAN_HOME") or "").strip()
    root = Path(home_override).expanduser() if home_override else _EV0_ROOT
    roots = [root / "kanban" / "attachments"]
    boards_root = root / "kanban" / "boards"
    try:
        board_dirs = [
            path for path in boards_root.iterdir()
            if path.is_dir() and not path.is_symlink()
            and re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", path.name)
            and (path / "kanban.db").is_file()
        ]
    except OSError:
        return roots
    roots.extend(path / "attachments" for path in board_dirs)
    return roots


def _media_delivery_allowed_roots() -> List[Path]:
    """Return roots from which model-emitted local media may be delivered."""
    roots = [Path(root) for root in MEDIA_DELIVERY_SAFE_ROOTS]
    roots.extend(_profile_cache_roots())
    roots.extend(_kanban_attachment_roots())
    extra_roots = os.environ.get(MEDIA_DELIVERY_ALLOW_DIRS_ENV, "")
    for chunk in extra_roots.split(os.pathsep):
        for raw_root in chunk.split(","):
            raw_root = raw_root.strip()
            if not raw_root:
                continue
            root = Path(os.path.expanduser(raw_root))
            if root.is_absolute():
                roots.append(root)
    return roots


def _media_delivery_recency_seconds() -> float:
    """Return the recency window for trusting freshly-produced files.

    0 disables recency-based trust entirely (pure-allowlist mode).
    """
    raw = os.environ.get(MEDIA_DELIVERY_TRUST_RECENT_ENV, "1").strip().lower()
    if raw in ("0", "false", "no", "off", ""):
        return 0.0
    try:
        custom = os.environ.get(MEDIA_DELIVERY_TRUST_RECENT_SECONDS_ENV, "").strip()
        if custom:
            seconds = float(custom)
            return max(0.0, seconds)
    except (TypeError, ValueError):
        pass
    return float(_MEDIA_DELIVERY_TRUST_RECENT_DEFAULT_SECONDS)


def _media_delivery_strict_mode() -> bool:
    """Return True when path validation should require allowlist/recency match.

    Off by default. In non-strict mode, ``validate_media_delivery_path``
    accepts any existing regular file that isn't under the credential /
    system-path denylist — restoring the pre-#29523 behavior for the
    single-user case. Strict mode preserves the original
    allowlist+recency-window logic for operators running public-facing
    gateways where prompt injection from one user shouldn't be able to
    exfiltrate the host's secrets to that same user.
    """
    raw = os.environ.get(MEDIA_DELIVERY_STRICT_ENV, "0").strip().lower()
    return raw in ("1", "true", "yes", "on")


def _media_delivery_denied_paths() -> List[Path]:
    """Return absolute denylist paths under which delivery is never allowed."""
    denied = [Path(p) for p in _MEDIA_DELIVERY_DENIED_PREFIXES]
    home = Path(os.path.expanduser("~"))
    for sub in _MEDIA_DELIVERY_DENIED_HOME_SUBPATHS:
        denied.append(home / sub)
    # The active 3V0 profile and shared 3V0 root both contain control
    # files and credentials. Only cache subdirectories under them are
    # explicitly allowlisted above (matched BEFORE this denylist in
    # validate_media_delivery_path, so generated media still delivers).
    #
    # These are the per-file credential / secret stores that live at the
    # EV0_HOME root. The set mirrors the canonical read guard in
    # agent/file_safety.py (get_read_block_error / build_write_denied_*) so the
    # delivery (read/exfil) side can't trail the write side: a credential the
    # agent is forbidden to write or read must also never be auto-attached to a
    # chat reply. Enumerated explicitly per-file rather than denying the whole
    # tree, so skills/, logs/, and ad-hoc agent-written files under ~/.3V0
    # stay deliverable (see #32090, #34425).
    _ROOT_CREDENTIAL_FILES = (
        ".env",
        "auth.json",
        "auth.lock",
        "credentials",
        "config.yaml",
        # Anthropic PKCE / OAuth refresh credential store.
        ".anthropic_oauth.json",
        # Google Workspace skill: auto-refreshing OAuth token (mtime bumps
        # every turn, which defeated the strict-mode recency window) plus the
        # pending-exchange session/verifier file.
        "google_token.json",
        "google_oauth_pending.json",
        os.path.join("auth", "google_oauth.json"),
        # Webhook subscription HMAC secrets.
        "webhook_subscriptions.json",
        # Bitwarden Secrets Manager plaintext and encrypted disk caches.
        os.path.join("cache", "bws_cache.json"),
        os.path.join("cache", "bws_cache.enc.json"),
    )
    # Directory trees whose every child is credential material.
    #
    # mcp-tokens/ holds live MCP OAuth access tokens (<server>.json) and
    # dynamically-registered client credentials (<server>.client.json); see
    # tools/mcp_oauth.py. Same credential class as auth.json/credentials/.
    # The write side already denies it (file_tools _check_sensitive_path);
    # this pairs the media-delivery (exfil) side so a prompt-injection MEDIA
    # tag can't deliver a live bearer token as a native attachment.
    # (session/kanban SQLite stores are handled by #41071 — kept out here.)
    _ROOT_CREDENTIAL_DIRS = (
        "pairing",
        "mcp-tokens",
    )
    for threev0_root in (_EV0_HOME, _EV0_ROOT):
        for rel in _ROOT_CREDENTIAL_FILES:
            denied.append(threev0_root / rel)
        for rel in _ROOT_CREDENTIAL_DIRS:
            denied.append(threev0_root / rel)
    return denied


def _path_under_denied_prefix(resolved: Path) -> bool:
    """Return True if ``resolved`` lives under a deny-listed system path.

    One narrow exception: when a denied prefix IS the running user's own home,
    the home itself is not treated as denied. ``/root`` is on the system-path
    denylist so that a non-root gateway can't deliver another user's home, but
    on a root-run gateway ``$HOME=/root`` and the operator's own deliverables
    (``/root/work/proposal.docx``) live directly under it. The credential
    sub-directories inside home (``~/.ssh``, ``~/.aws``, ...) and 3V0
    secrets (``~/.3V0/.env``, ``auth.json``) are *separate, more-specific*
    denied paths, so they stay blocked regardless of this exception — it can
    only un-block a plain file sitting in the running user's home tree, never a
    credential location or another user's home.
    """
    try:
        home = Path(os.path.expanduser("~")).resolve(strict=False)
    except (OSError, RuntimeError, ValueError):
        home = None
    for denied in _media_delivery_denied_paths():
        try:
            resolved_denied = denied.expanduser().resolve(strict=False)
        except (OSError, RuntimeError, ValueError):
            continue
        if not (_path_is_within(resolved, resolved_denied) or resolved == resolved_denied):
            continue
        # Allow the running user's own home tree; its credential sub-dirs are
        # caught by their own (more-specific) denylist entries above.
        if home is not None and resolved_denied == home:
            continue
        return True
    return False


def _file_is_recently_produced(resolved: Path, window_seconds: float) -> bool:
    """Return True if the file's mtime is within ``window_seconds`` of now.

    Used as a session-scoped trust signal: agents almost always produce
    delivery artifacts within seconds of asking to send them, while
    prompt-injection paths pointing at pre-existing host files (/etc/passwd,
    ~/.ssh/id_rsa) have mtimes measured in days or months.
    """
    if window_seconds <= 0:
        return False
    try:
        mtime = resolved.stat().st_mtime
    except OSError:
        return False
    return (time.time() - mtime) <= window_seconds


def _path_is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _parse_docker_volume_mounts() -> List[Tuple[Path, Path]]:
    """Parse configured Docker volume mounts into ``(host_path, container_path)``.

    Source of truth is ``TERMINAL_DOCKER_VOLUMES`` (JSON list of
    ``host:container[:mode]`` specs), matching terminal/docker runtime config.
    Named volumes and non-absolute hosts are skipped because they cannot be
    resolved on the gateway host for media delivery.
    """
    raw = os.getenv("TERMINAL_DOCKER_VOLUMES", "").strip()
    if not raw:
        return []
    try:
        import json as _json

        parsed = _json.loads(raw)
    except Exception:
        return []
    if not isinstance(parsed, list):
        return []

    mounts: List[Tuple[Path, Path]] = []
    for entry in parsed:
        if not isinstance(entry, str):
            continue
        spec = entry.strip()
        if not spec:
            continue
        # Prefer the first ':/' so absolute container paths are unambiguous.
        sep = spec.find(":/")
        if sep <= 0:
            continue
        host_raw = spec[:sep]
        container_and_mode = spec[sep + 1 :]  # starts with /
        container_raw = container_and_mode.split(":", 1)[0]
        if not container_raw.startswith("/"):
            continue
        # Skip named volumes (no absolute/drive host path).
        host_expanded = os.path.expanduser(host_raw)
        if not (
            host_expanded.startswith("/")
            or (len(host_expanded) > 1 and host_expanded[1] == ":")
        ):
            continue
        try:
            host_path = Path(host_expanded).resolve(strict=False)
            container_path = Path(container_raw)
        except (OSError, RuntimeError, ValueError):
            continue
        if not container_path.is_absolute():
            continue
        mounts.append((host_path, container_path))
    return mounts


def _default_docker_workspace_host_root() -> Optional[Path]:
    """Host path for Docker's default persistent ``/workspace`` mount."""
    if os.getenv("TERMINAL_ENV", "").strip().lower() != "docker":
        return None
    if os.getenv("TERMINAL_CONTAINER_PERSISTENT", "true").strip().lower() not in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return None
    # Explicit cwd mount takes over /workspace when enabled.
    if os.getenv("TERMINAL_DOCKER_MOUNT_CWD_TO_WORKSPACE", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }:
        cwd = os.getenv("TERMINAL_CWD") or os.getcwd()
        try:
            host = Path(os.path.expanduser(cwd)).resolve(strict=False)
        except (OSError, RuntimeError, ValueError):
            return None
        return host if host.is_dir() else None
    try:
        from tools.environments.base import get_sandbox_dir

        root = (get_sandbox_dir() / "docker" / "default" / "workspace").resolve(strict=False)
    except Exception:
        return None
    return root if root.is_dir() else None


def _docker_persistent_home_host_root() -> Optional[Path]:
    """Host path for Docker's default persistent ``/root`` home mount.

    Persistent containers bind ``<sandbox>/docker/<task>/home`` to ``/root``
    (tools/environments/docker.py), so an agent that writes ``/root/out.png``
    produced a real host file the gateway couldn't find. Same collapse rule as
    the workspace mount: the gateway's container sharing resolves to the
    ``default`` task sandbox.
    """
    if os.getenv("TERMINAL_ENV", "").strip().lower() != "docker":
        return None
    if os.getenv("TERMINAL_CONTAINER_PERSISTENT", "true").strip().lower() not in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return None
    try:
        from tools.environments.base import get_sandbox_dir

        root = (get_sandbox_dir() / "docker" / "default" / "home").resolve(strict=False)
    except Exception:
        return None
    return root if root.is_dir() else None


def _cache_dir_container_mounts() -> List[Tuple[Path, Path]]:
    """(host, container) pairs for the auto-mounted 3V0 cache dirs.

    The agent legitimately sees generated artifacts at ``/root/.3V0/...``
    (``agent_visible_image`` from image_generate, cache-dir reads) and will
    naturally emit those container paths in MEDIA tags. These mounts are
    longer prefixes than the ``/root`` home mount, so longest-prefix matching
    picks the cache translation over the home translation for them.
    """
    if os.getenv("TERMINAL_ENV", "").strip().lower() != "docker":
        return []
    try:
        from tools.credential_files import get_cache_directory_mounts

        return [
            (Path(m["host_path"]), Path(m["container_path"]))
            for m in get_cache_directory_mounts()
        ]
    except Exception:
        return []


def _translate_docker_container_media_path(candidate: Path) -> Optional[Path]:
    """Translate a container-absolute path to its host path when possible.

    Uses longest-prefix match across configured ``docker_volumes``, the
    auto-mounted 3V0 cache dirs (``/root/.3V0/...``), the default
    persistent Docker ``/workspace`` host root, and the persistent ``/root``
    home mount.
    """
    if not candidate.is_absolute():
        return None

    # In-process gateways (Desktop backend, `3v0 serve`) may not have
    # bridged terminal.* config into TERMINAL_* env vars — run the idempotent
    # bridge so the mount parsing below sees the active backend and volumes
    # (same guard _binary_reference_block applies for inbound attachments).
    try:
        from tools.terminal_tool import _ensure_terminal_env_bridged

        _ensure_terminal_env_bridged()
    except Exception:
        pass

    mounts = list(_parse_docker_volume_mounts())
    mounts.extend(_cache_dir_container_mounts())
    # Synthetic /workspace mount for default persistent sandbox / cwd bind.
    default_ws = _default_docker_workspace_host_root()
    if default_ws is not None and not any(c.as_posix() == "/workspace" for _, c in mounts):
        mounts.append((default_ws, Path("/workspace")))
    # Synthetic /root mount for the persistent home bind. Cache mounts above
    # are longer prefixes, so /root/.3V0/... still translates to the host
    # cache — this only catches stray home writes like /root/out.png.
    default_home = _docker_persistent_home_host_root()
    if default_home is not None and not any(c.as_posix() == "/root" for _, c in mounts):
        # /root/.3V0/* that did NOT match a cache mount is the container's
        # credential/secret surface (.env, auth.json, ... are individually
        # bind-mounted from the real host stores). Translating those through
        # the home mount would resolve to sandbox-home copies OUTSIDE the
        # host-side credential denylist prefixes — refuse instead so the
        # normal "container path doesn't exist on host" rejection applies.
        if not candidate.as_posix().startswith("/root/.3V0"):
            mounts.append((default_home, Path("/root")))

    if not mounts:
        return None

    # Longest container-prefix match.
    best: Optional[Tuple[Path, Path, int]] = None
    candidate_posix = candidate.as_posix()
    for host_root, container_root in mounts:
        container_posix = container_root.as_posix().rstrip("/") or "/"
        if candidate_posix == container_posix or candidate_posix.startswith(container_posix + "/"):
            score = len(container_posix)
            if best is None or score > best[2]:
                best = (host_root, container_root, score)
    if best is None:
        return None

    host_root, container_root, _ = best
    try:
        relative = candidate.relative_to(container_root)
        translated = (host_root / relative).resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return None
    if translated != host_root and not _path_is_within(translated, host_root):
        return None
    return translated


def validate_media_delivery_path(path: str) -> Optional[str]:
    """Return a safe absolute file path for native media delivery, else None.

    Default mode (single-user / private gateway): accept any existing regular
    file that isn't under the credential / system-path denylist
    (``_MEDIA_DELIVERY_DENIED_PREFIXES`` + ``~/.ssh``, ``~/.aws``, etc.).
    This matches the symmetry of inbound delivery — Telegram/Discord/Slack
    will hand the agent any file the user uploads, and the agent can hand
    back any file that isn't a credential.

    Strict mode (opt-in via ``gateway.strict`` in ``config.yaml`` or
    ``EV0_MEDIA_DELIVERY_STRICT=1``): the file MUST live under a
    3V0-managed cache, under an operator-allowlisted root
    (``EV0_MEDIA_ALLOW_DIRS``), or be freshly produced inside the
    configured recency window. Suitable for public-facing bots where
    prompt injection from one user shouldn't be able to exfiltrate the
    host's secrets to that same user.

    Symlinks are resolved before any containment / denylist check.
    """
    if not path:
        return None

    candidate = str(path).strip()
    if len(candidate) >= 2 and candidate[0] == candidate[-1] and candidate[0] in "`\"'":
        candidate = candidate[1:-1].strip()
    candidate = candidate.lstrip("`\"'").rstrip("`\"',.;:)}]")
    if not candidate:
        return None

    try:
        expanded = Path(os.path.expanduser(candidate))
    except (OSError, RuntimeError, ValueError):
        # expanduser raises ValueError("embedded null byte") for a ~\x00 path.
        return None
    if not expanded.is_absolute():
        return None

    # Docker agents emit MEDIA:/workspace/... (or other configured container
    # mount paths). Resolve those to host paths before the normal host-side
    # existence / denylist checks.
    translated = _translate_docker_container_media_path(expanded)
    if translated is not None:
        resolved = translated
    else:
        try:
            resolved = expanded.resolve(strict=True)
        except (OSError, RuntimeError, ValueError):
            return None

    if not resolved.is_file():
        return None

    # Cache / operator allowlist is always honored — these are unconditionally
    # trusted regardless of mode.
    for root in _media_delivery_allowed_roots():
        try:
            resolved_root = root.expanduser().resolve(strict=False)
        except (OSError, RuntimeError, ValueError):
            continue
        if _path_is_within(resolved, resolved_root):
            return str(resolved)

    # Non-strict mode (default): accept anything not on the denylist.
    # The denylist still blocks /etc, /proc, ~/.ssh, ~/.aws, and the
    # credential/secret stores under the 3V0 root (~/.3V0/.env,
    # auth.json, .anthropic_oauth.json, google_token.json, pairing/, ...) —
    # so the obvious prompt-injection / credential-exfil sites
    # (``MEDIA:/etc/passwd``, ``MEDIA:~/.ssh/id_rsa``,
    # ``MEDIA:~/.3V0/google_token.json``) remain rejected.
    if not _media_delivery_strict_mode():
        if _path_under_denied_prefix(resolved):
            return None
        return str(resolved)

    # Strict mode: fall back to recency-based trust for freshly-produced
    # files (e.g. ``pandoc -o /tmp/report.pdf`` or
    # ``write_file("/home/user/report.pdf", ...)``). System paths and
    # credential locations remain blocked even when "recent" — see
    # ``_MEDIA_DELIVERY_DENIED_PREFIXES`` for the denylist.
    window = _media_delivery_recency_seconds()
    if window > 0 and not _path_under_denied_prefix(resolved):
        if _file_is_recently_produced(resolved, window):
            return str(resolved)

    return None


def _match_extensionless_path(scan_text: str, match: "re.Match") -> Optional[Tuple[str, int]]:
    """Resolve an extensionless MEDIA tag match to a validated on-disk path.

    Tries the regex-captured path first. When that fails validation, the
    candidate is progressively extended forward across single spaces
    (validation-gated, bounded at 8 tokens, never past a newline or a
    subsequent ``MEDIA:`` keyword) so unknown-extension paths containing
    spaces deliver (#24032). Returns ``(safe_path, end_offset)`` where
    ``end_offset`` is the index in ``scan_text`` just past the matched path,
    or ``None`` when nothing validates.
    """
    raw = match.group("path")
    path = _normalize_media_tag_path(raw)
    if not path:
        return None
    safe = validate_media_delivery_path(path)
    if safe:
        return safe, match.end("path")
    start = match.start("path")
    nl = scan_text.find("\n", start)
    limit = nl if nl != -1 else len(scan_text)
    segment = scan_text[start:limit]
    nxt = segment.find("MEDIA:", 1)
    if nxt != -1:
        segment = segment[:nxt]
    pos = match.end("path") - start
    for _ in range(8):
        while pos < len(segment) and segment[pos] in " \t":
            pos += 1
        if pos >= len(segment):
            break
        tok_end = pos
        while tok_end < len(segment) and segment[tok_end] not in " \t":
            tok_end += 1
        candidate = _normalize_media_tag_path(segment[:tok_end])
        safe = validate_media_delivery_path(candidate)
        if safe:
            return safe, start + tok_end
        pos = tok_end
    return None


def _merge_spans(spans: list) -> list:
    """Merge overlapping/nested (start, end) spans so multi-pattern matches
    over the same tag never double-delete adjacent text."""
    merged: list = []
    for s, e in sorted(spans):
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged


def _normalize_media_tag_path(raw: str) -> str:
    path = str(raw or "").strip()
    if len(path) >= 2 and path[0] == path[-1] and path[0] in "`\"'":
        path = path[1:-1].strip()
    return path.lstrip("`\"'").rstrip("`\"',.;:)}]")


def _path_lacks_deliverable_extension(path: str) -> bool:
    """True when MEDIA_TAG_CLEANUP_RE's extension alternation does not cover
    ``path`` — either the basename has no extension at all (Caddyfile,
    Makefile, …) or the extension is not in _media_types.MEDIA_DELIVERY_EXTS (.py, .log,
    .weirdext, …). Such paths route through the validated delivery pass
    (``validate_media_delivery_path``) instead of the unconditional one, so
    every file type is deliverable (#36060) while nonexistent / denylisted
    paths stay visible in the text.
    """
    suffix = Path(path).suffix.lower()
    return not suffix or suffix not in _media_types.MEDIA_DELIVERY_EXTS


def _resolve_extensionless_candidate(path: str) -> Optional[str]:
    """Validate a bare extensionless-branch path (no forward extension).

    Thin wrapper kept for call sites that only have the normalized path
    (no scan-text context for spaced-path recovery).
    """
    if not path:
        return None
    return validate_media_delivery_path(path)


def _strip_media_tag_directives(text: str) -> str:
    """Remove MEDIA: tags and [[audio_as_voice]] / [[as_document]] markers.

    Protected spans (fenced code blocks, inline code holding non-deliverable
    example tags, blockquotes, JSON string values) are used as a mask-locator
    only — tags inside them are neither stripped nor mangled, matching
    ``extract_media``'s treatment so display text and delivery agree (#16434).
    """
    if (
        "MEDIA:" not in text
        and "[[audio_as_voice]]" not in text
        and "[[as_document]]" not in text
    ):
        return text
    cleaned = text.replace("[[audio_as_voice]]", "").replace("[[as_document]]", "")

    # Locate real tag spans on a masked copy (offset-preserving), then delete
    # exactly those spans from the unmasked text — same pattern as
    # extract_media. Import-cycle-free: BasePlatformAdapter is defined later
    # in this module, so resolve it lazily at call time.
    from gateway.platforms.base import BasePlatformAdapter  # lazy: defined later in base
    masked = BasePlatformAdapter._mask_protected_spans(cleaned)
    masked = BasePlatformAdapter._mask_json_string_media(masked)

    spans: list = [m.span() for m in _media_types.MEDIA_TAG_CLEANUP_RE.finditer(masked)]
    for match in _media_types.MEDIA_EXTENSIONLESS_TAG_RE.finditer(masked):
        path = _normalize_media_tag_path(match.group("path"))
        if not path or not _path_lacks_deliverable_extension(path):
            continue
        resolved = _match_extensionless_path(masked, match)
        if resolved is not None:
            spans.append((match.start(), resolved[1]))

    if spans:
        chars = list(cleaned)
        for start, end in reversed(_merge_spans(spans)):
            del chars[start:end]
        cleaned = "".join(chars)
    return cleaned
