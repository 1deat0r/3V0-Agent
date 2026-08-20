#!/usr/bin/env python3
"""
3V0 dev-root guard - structural enforcement that 3V0 never writes code
outside the canonical repo and never recreates the upstream-reset footgun.

Path protection list lives in an external config (~/.config/3v0/dev-root-guard-paths.json)
so the guard code itself carries no legacy brand names.

Exit 2 = BLOCK (fail_closed), 0 = allow.
"""
import json
import os
import re
import sys

_PATHS = json.load(open("/home/mustbearn/.config/3v0/dev-root-guard-paths.json"))

CANONICAL = _PATHS["canonical"]
FORBIDDEN = _PATHS.get("forbidden", [])

PATH_TOOLS = {"write_file", "patch"}
CWD_TOOLS = {"terminal", "execute_code"}

_REDIR_INTO = re.compile(r">>?\s*\"?'?")
_WRITE_VERB = re.compile(
    r"(?:^|[\s;&|(])("
    r"cp|mv|rm|touch|mkdir|tee|install|ln|"
    r"git\s+(?:commit|push|add|rm|mv|checkout\s+-b|reset\s+--hard|merge|rebase)"
    r")\s+"
)
_CD_INTO = re.compile(r"(?:^|[\s;&|(])(?:cd|pushd)\s+")
_GIT_C = re.compile(r"git\s+-C\s+")
_GIT_DIR = re.compile(r"git\s+--git-dir[=\s]+\S*")


def norm(p: str) -> str:
    return os.path.realpath(os.path.expanduser(p))


def under(path: str, root: str) -> bool:
    p, r = norm(path), norm(root)
    return p == r or p.startswith(r + os.sep)


def blocked(reason: str):
    print(json.dumps({"action": "block", "message": reason}))
    sys.exit(2)


def _is_write_target(cmd: str, forbidden: str) -> bool:
    f = norm(forbidden)
    pat = re.escape(f) + r"(?:[/\\\"']|\s|$)"
    cleaned = re.sub(r"\d+>\s*[^\s;&|]+", "", cmd)
    cleaned = re.sub(r"\d+>&\s*\d+", "", cleaned)
    for m in _REDIR_INTO.finditer(cleaned):
        tail = cleaned[m.end():]
        if re.match(pat, tail):
            return True
    if (_GIT_C.search(cmd) or _GIT_DIR.search(cmd)) and f in cmd:
        return True
    if _WRITE_VERB.search(cmd) and f in cmd:
        if re.search(r"=\s*\"?'?" + pat, cmd):
            return False
        return True
    if _CD_INTO.search(cmd) and re.search(pat, cmd):
        for m in _CD_INTO.finditer(cmd):
            tail = cmd[m.end():]
            if re.match(pat, tail):
                return True
    return False


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(2)

    tool = str(data.get("tool_name", ""))
    ti = data.get("tool_input") or {}
    if not isinstance(ti, dict):
        ti = {}
    cwd = str(data.get("cwd") or os.getcwd())

    try:
        if tool in PATH_TOOLS:
            path = str(ti.get("path") or ti.get("file_path") or "")
            if path:
                for f in FORBIDDEN:
                    if under(path, f):
                        blocked(
                            f"DEV-ROOT GUARD: refusing to write {path} - "
                            f"read-only reference tree. 3V0 develops ONLY in: {CANONICAL}"
                        )

        if tool in CWD_TOOLS:
            for f in FORBIDDEN:
                if under(cwd, f):
                    blocked(
                        f"DEV-ROOT GUARD: cwd {cwd} is inside a forbidden "
                        f"reference tree. Run development from: {CANONICAL}"
                    )

            cmd_sources = []
            raw = ti.get("command") or ti.get("cmd") or ""
            if raw:
                cmd_sources.append(str(raw))
            code = ti.get("code")
            if code:
                cmd_sources.append(str(code))

            for cmd in cmd_sources:
                names_canonical = CANONICAL in cmd
                if not (under(cwd, CANONICAL) or names_canonical):
                    continue
                cmdn = cmd
                if tool == "execute_code":
                    cmdn = re.sub(r"[\[\(),;\"'=\\]", " ", cmd)
                FOOTGUN = [
                    r"git\s+remote\s+(?:add|set-url|rename)\s+\S*(?:origin|upstream)\b",
                    r"git\s+config\s+(?:--\S+\s+)?remote\.(?:origin|upstream)\.\S+",
                    r"git\s+remote\s+(?:add|set-url)\s+\S+\s+(?:https?://github\.com/(?:NousResearch|1deat0r)|git@github\.com:)",
                    r"remote\s*=\s*[\"']?https?://github\.com/(?:NousResearch|1deat0r)",
                ]
                for pat in FOOTGUN:
                    if re.search(pat, cmdn):
                        blocked(
                            "DEV-ROOT GUARD: refusing to create/re-point an "
                            "origin/upstream remote - the upstream footgun "
                            "must never exist on the canonical repo."
                        )
                if re.search(
                    r"(?:^|[;&|(])\s*(?:3v0|ev0)\s+update\b|(?:python\w*\s+)?-m\s+\S*\.main\s+update\b",
                    cmd,
                ):
                    blocked(
                        "DEV-ROOT GUARD: `update` machinery fetches upstream and "
                        "can reset the canonical branch - refusing. Update 3V0 by "
                        "pulling from `public` deliberately."
                    )
                BRANCH_MOVE = [
                    r"git\s+(?:-C\s+\S+(?:\s+\S+)*\s+|--git-dir\S+\s+)?(?:reset|checkout|switch)\s+--?[^\n]*?\b(?:upstream|origin)/\S+",
                    r"git\s+(?:-C\s+\S+(?:\s+\S+)*\s+|--git-dir\S+\s+)?(?:reset|checkout|switch)\s+(?:--hard|--force|-f)\b",
                    r"git\s+fetch\s+(?:upstream|origin)\b.*?\n?\s*(?:git\s+reset|git\s+checkout)",
                ]
                for pat in BRANCH_MOVE:
                    if re.search(pat, cmdn, re.IGNORECASE):
                        blocked(
                            "DEV-ROOT GUARD: refusing movement of the canonical "
                            "branch to a remote-tracking ref or a hard reset - "
                            "the 2026-08-20 incident class."
                        )
    except SystemExit:
        raise
    except Exception:
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()