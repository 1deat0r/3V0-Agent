"""Native tool registry — the native-mode loop's hands.

Stdlib-only, zero Hermes. Deliberately small and constrained. Tools:
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
PROFILE = Path(__import__("os").environ.get("HERMES_HOME") or "~/.hermes/profiles/3v0").expanduser()
_ALLOWED_ROOTS = (REPO.resolve(), PROFILE.resolve())
_SECRET_PARTS = (".env", ".pem", "wallet", "secrets", "cred", "token", "key.pem")

_DENY_REASONS = (
    (re.compile(r"\bsystemctl\b.*?(stop|restart)\b.*?(gateway|3v0-gateway)", re.I), "gateway lifecycle via systemctl"),
    (re.compile(r"\bhermes\b.*\bgateway\b.*?(stop|restart)\b", re.I), "gateway lifecycle via hermes"),
    (re.compile(r"\b(pkill|killall)\b.*\b(hermes|gateway|3v0)\b", re.I), "self-termination via pkill/killall"),
    (re.compile(r"\bkill\b.*(pgrep|pidof)", re.I), "self-termination via kill+pgrep"),
    (re.compile(r"\brm\s+-[a-z]*[rf][a-z]*\s+/", re.I), "destroy root"),
    (re.compile(r"\s>\s?/(etc|boot|sys|proc)/", re.I), "write to system path"),
)


def _resolve_safe(path: str) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (REPO / p).resolve()
    else:
        p = p.resolve()
    if not any(str(p).startswith(str(root)) for root in _ALLOWED_ROOTS):
        raise PermissionError(f"path outside allowed roots: {p}")
    if any(part in p.parts for part in ("..",)):
        raise PermissionError(f"path traversal: {path}")
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
    "read_file": {"description": "Read a UTF-8 text file inside the repo or profile (secrets denied). Args: {path}", "handler": read_file},
    "write_file": {"description": "Write a UTF-8 text file inside the repo or profile (secrets denied). Args: {path, content}", "handler": write_file},
    "run_script": {"description": "Run a native script by name from 3v0/scripts/. Args: {name, args:[...]}", "handler": run_script},
    "run_terminal": {"description": "Run one shell command (denylisted: gateway lifecycle, self-kill, rm -rf /). Args: {command}", "handler": run_terminal},
}


def list_tools() -> dict:
    return {k: {"description": v["description"]} for k, v in _REGISTRY.items()}


def execute(name: str, args: dict | None = None) -> dict:
    spec = _REGISTRY.get(name)
    if spec is None:
        return {"error": f"unknown tool: {name!r}"}
    a = args or {}
    try:
        if name == "read_file":
            return spec["handler"](a.get("path", ""))
        if name == "write_file":
            return spec["handler"](a.get("path", ""), a.get("content", ""))
        if name == "run_script":
            return spec["handler"](a.get("name", ""), *a.get("args", []))
        if name == "run_terminal":
            return spec["handler"](a.get("command", ""), a.get("timeout", 60))
        return {"error": f"no arg-mapping for {name!r}"}
    except Exception as e:
        return {"error": f"tool failed: {e}"}


if __name__ == "__main__":
    # live proof: real reads + a native script, and a guaranteed-blocked command
    print("TOOLS:", ", ".join(sorted(list_tools())))
    print("read:", json.dumps(execute("read_file", {"path": "AGENTS.md"})["content"][:40]))
    print("script:", json.dumps(execute("run_script", {"name": "verify.sh", "args": []}).get("exit_code")))
    print("blocked:", json.dumps(execute("run_terminal", {"command": "systemctl --user restart 3v0-gateway.service"})))
