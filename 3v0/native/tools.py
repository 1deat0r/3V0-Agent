"""Native tool registry — the native-mode loop's hands.

Stdlib-only, zero 3V0. Deliberately small and constrained. Tools:
  * read_file / write_file — rooted inside the repo + profile; secret files denied
  * run_script — run a native script under 3v0/scripts/ by name
  * run_terminal — one shell command, but denylisted against self-termination
    and gateway lifecycle (the exact risks that stranded the agent earlier).
Safety is built in from the start, not retrofitted.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SCRIPTS = REPO / "3v0" / "scripts"
PROFILE = Path(__import__("os").environ.get("EV0_HOME") or "~/.3V0/profiles/3v0").expanduser()
_ALLOWED_ROOTS = (REPO.resolve(), PROFILE.resolve())
_SECRET_PARTS = (".env", ".pem", "wallet", "secrets", "cred", "token", "key.pem")

_DENY_REASONS = (
    (re.compile(r"\bsystemctl\b.*?(stop|restart)\b.*?(gateway|3v0-gateway)", re.I), "gateway lifecycle via systemctl"),
    (re.compile(r"\b(?:3v0|ev0)\b.*\bgateway\b.*?(stop|restart)\b", re.I), "gateway lifecycle via 3V0"),
    (re.compile(r"\b(pkill|killall)\b.*\b(?:3v0|ev0|gateway)\b", re.I), "self-termination via pkill/killall"),
    (re.compile(r"\bkill\b.*(pgrep|pidof)", re.I), "self-termination via kill+pgrep"),
    (re.compile(r"\brm\s+-[a-z]*[rf][a-z]*\s+/", re.I), "destroy root"),
    (re.compile(r"\s>\s?/(etc|boot|sys|proc)/", re.I), "write to system path"),
)


def _resolve_safe(path: str) -> Path:
    # Reject traversal FIRST, before any resolution: `../../etc/passwd` must
    # fail regardless of where the repo lives (a resolved path has no ".."
    # parts, so checking after resolve() makes the traversal check dead code).
    raw = Path(path)
    if ".." in raw.parts:
        raise PermissionError(f"path traversal: {path}")
    p = raw.expanduser()
    if not p.is_absolute():
        p = (REPO / p).resolve()
    else:
        p = p.resolve()
    if not any(str(p).startswith(str(root)) for root in _ALLOWED_ROOTS):
        raise PermissionError(f"path outside allowed roots: {p}")
    if any(_SECRET in p.name.lower() or _SECRET in str(p).lower() for _SECRET in _SECRET_PARTS):
        raise PermissionError(f"secret-path denied: {path}")
    return p


def _denied(command: str) -> str | None:
    for pat, reason in _DENY_REASONS:
        if pat.search(command):
            return reason
    return None


def read_file(path: str) -> dict:
    try:
        p = _resolve_safe(path)
    except PermissionError as e:
        return {"error": str(e)}
    if not p.is_file():
        return {"error": f"not a file: {path}"}
    try:
        body = p.read_text()
    except Exception as e:
        return {"error": f"read failed: {e}"}
    return {"content": body, "path": str(p)}


def write_file(path: str, content: str) -> dict:
    try:
        p = _resolve_safe(path)
    except PermissionError as e:
        return {"error": str(e)}
    try:
        p.write_text(content)
    except Exception as e:
        return {"error": f"write failed: {e}"}
    return {"ok": True, "path": str(p)}


def run_script(name: str, *args) -> dict:
    if not re.fullmatch(r"[a-z0-9_.\-]+", name or ""):
        return {"error": f"invalid script name: {name!r}"}
    script = (SCRIPTS / name).resolve()
    if not script.is_file():
        return {"error": f"no such native script: {name}"}
    try:
        proc = subprocess.run(
            [str(script), *map(str, args)],
            capture_output=True, text=True, timeout=120,
        )
    except Exception as e:
        return {"error": f"run failed: {e}"}
    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def run_terminal(command: str, timeout: int = 60) -> dict:
    reason = _denied(command or "")
    if reason:
        return {"error": f"blocked by native safety denylist: {reason}", "blocked": True}
    try:
        proc = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout,
        )
    except Exception as e:
        return {"error": f"run failed: {e}"}
    return {"exit_code": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}


_REGISTRY = {
    "read_file": {
        "description": "Read a UTF-8 text file inside the repo or profile (secrets denied). Args: {path}",
        "handler": read_file,
        "bind": lambda a: (a.get("path", ""),),
    },
    "write_file": {
        "description": "Write a UTF-8 text file inside the repo or profile (secrets denied). Args: {path, content}",
        "handler": write_file,
        "bind": lambda a: (a.get("path", ""), a.get("content", "")),
    },
    "run_script": {
        "description": "Run a native script by name from 3v0/scripts/. Args: {name, args:[...]}",
        "handler": run_script,
        "bind": lambda a: (a.get("name", ""), *a.get("args", [])),
    },
    "run_terminal": {
        "description": "Run one shell command (denylisted: gateway lifecycle, self-kill, rm -rf /). Args: {command}",
        "handler": run_terminal,
        "bind": lambda a: (a.get("command", ""), a.get("timeout", 60)),
    },
}


def list_tools() -> dict:
    return {k: {"description": v["description"]} for k, v in _REGISTRY.items()}


def execute(name: str, args: dict | None = None) -> dict:
    """Generic dispatch: {name,args} -> handler result.

    Each registered tool declares its own ``bind`` (args dict -> handler
    positional args), so adding a tool is ONE registry entry — handler,
    description, and arg-binding live together, and there is no parallel
    if/elif mapping to keep in sync.
    """
    spec = _REGISTRY.get(name)
    if spec is None:
        return {"error": f"unknown tool: {name!r}"}
    try:
        return spec["handler"](*spec["bind"](args or {}))
    except Exception as e:  # noqa: BLE001 - a tool failure is a result, not a crash
        return {"error": f"tool failed: {e}"}


if __name__ == "__main__":
    # live proof: real reads + a native script, and a guaranteed-blocked command
    print("TOOLS:", ", ".join(sorted(list_tools())))
    print("read:", json.dumps(execute("read_file", {"path": "AGENTS.md"})["content"][:40]))
    print("script:", json.dumps(execute("run_script", {"name": "verify.sh", "args": []}).get("exit_code")))
    print("blocked:", json.dumps(execute("run_terminal", {"command": "systemctl --user restart 3v0-gateway.service"})))
