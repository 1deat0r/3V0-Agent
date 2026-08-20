#!/usr/bin/env python3
"""
3V0 dev-root guard — structural enforcement that 3V0 never develops
in the wrong folder.

Hooks in as a Hermes ``pre_tool_call`` shell hook. Reads the wire payload
from stdin. Exit code 2 blocks the tool call (fail_closed).

Dev rule: file writes (write_file/patch) into a forbidden tree are always
blocked. Terminal commands are blocked only when a forbidden path is a
DIRECT WRITE TARGET: a shell redirect into it, `cd`/`git -C` into it, or a
write verb with it as an operand. Merely referencing a forbidden path (e.g.
running an interpreter that lives there, reading a file there) is allowed —
reads are how cutover diagnostics work.

Canonical dev root (the ONLY place 3V0 writes code):
  /home/mustbearn/Projects/AI Agents/3V0 Agent
"""
import json
import os
import re
import sys

# Trees where 3V0 must NEVER write code (runtime fork, pristine clones,
# stray checkouts of the hermes/3v0 lineage that are not the canonical repo).
CANONICAL = "/home/mustbearn/Projects/AI Agents/3V0 Agent"
FORBIDDEN = [
    "/home/mustbearn/.hermes/hermes-agent",
    "/home/mustbearn/.3V0/hermes-agent",
    "/home/mustbearn/Projects/Research/hermes-agent-repo",
]

# Tool names whose `path` argument we enforce hard (WRITE tools only).
PATH_TOOLS = {"write_file", "patch"}
# Tools whose cwd / command we inspect.
CWD_TOOLS = {"terminal", "execute_code"}

# A write verb / redirection that makes a following forbidden path a WRITE
# TARGET (as opposed to a read or an interpreter path).
_REDIR_INTO = re.compile(r">>?\s*\"?'?")          # `>` or `>>` then optional quotes
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
    """True when `cmd` directs a write at `forbidden` (not just mentions it)."""
    f = norm(forbidden)
    pat = re.escape(f) + r"(?:[/\\\"']|\s|$)"
    # 1. shell redirect into the tree:  `> /path`, `>> /path`
    #    Strip fd-stream redirects (`2>&1`, `2>/dev/null`) first — they
    #    redirect streams, not the forbidden tree — then look for a bare
    #    output redirect whose target starts with the forbidden path.
    cleaned = re.sub(r"\d+>\s*[^\s;&|]+", "", cmd)      # 2>/dev/null, 2>file
    cleaned = re.sub(r"\d+>&\s*\d+", "", cleaned)        # 2>&1
    for m in _REDIR_INTO.finditer(cleaned):
        tail = cleaned[m.end():]
        if re.match(pat, tail):
            return True
    # 2. git operating directly on the tree
    if (_GIT_C.search(cmd) or _GIT_DIR.search(cmd)) and f in cmd:
        return True
    # 3. write verb with the forbidden path as an operand:
    #    `cp x /path/...`, `mv x /path/...`, `touch /path/...`, etc.
    if _WRITE_VERB.search(cmd) and f in cmd:
        # But NOT when the path only appears in an assignment/word like
        # `PY=/path/venv/bin/python` (interpreter reference).
        if re.search(r"=\s*\"?'?" + pat, cmd):
            return False
        return True
    # 4. cd/pushd INTO the tree (everything after runs there)
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
        sys.exit(2)  # fail closed: malformed payload must not silently allow

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
                            f"DEV-ROOT GUARD: refusing to write {path} — "
                            f"{f} is a READ-ONLY reference tree. 3V0 develops "
                            f"ONLY in: {CANONICAL}"
                        )

        if tool in CWD_TOOLS:
            for f in FORBIDDEN:
                if under(cwd, f):
                    blocked(
                        f"DEV-ROOT GUARD: cwd {cwd} is inside forbidden tree "
                        f"{f}. This is a READ-ONLY reference. Run development "
                        f"from the canonical project: {CANONICAL}"
                    )

            if tool == "terminal":
                        cmd = str(ti.get("command") or ti.get("cmd") or "")
                        for f in FORBIDDEN:
                            if f in cmd and _is_write_target(cmd, f):
                                blocked(
                                    f"DEV-ROOT GUARD: command writes into forbidden "
                                    f"tree {f}. Develop ONLY in {CANONICAL}"
                                )

            # ---- Canonical-repo sovereignty guard (2026-08-20 incident) ----
            # A stale process reset the live checkout to upstream via
            # `git reset --hard origin/main`. `origin` was renamed to `upstream`
            # at the git level; these rules stop the footgun from ever being
            # recreated OR the canonical branch from being moved to a
            # remote-tracking ref — from ANY tool that carries a command
            # (terminal OR execute_code — previously execute_code was a bypass).
            cmd_sources = []
            if tool in CWD_TOOLS:
                raw = ti.get("command") or ti.get("cmd") or ""
                if raw:
                    cmd_sources.append(str(raw))
                code = ti.get("code")
                if code:
                    cmd_sources.append(str(code))
            for cmd in cmd_sources:
                # The canonical repo is only meaningful if the command is run
                # there (cwd) or explicitly names it (-C / --git-dir / cd).
                names_canonical = CANONICAL in cmd
                if not (under(cwd, CANONICAL) or names_canonical):
                    continue
                # Normalize code-payload syntax to shell-ish token spacing so
                # the same footgun families catch both `git remote add origin`
                # (terminal) and ["git","remote","add","origin"] (execute_code).
                cmdn = cmd
                if tool == "execute_code":
                    cmdn = re.sub(r'[\[\(\),;"\'=\\]', " ", cmd)
                # 1. Remote-footgun recreation: origin/upstream remotes may not
                #    be added, re-added, set-url'd, or config'd into existence.
                FOOTGUN = [
                    r"git\s+remote\s+(?:add|set-url|rename)\s+\S*(?:origin|upstream)\b",
                    r"git\s+config\s+(?:--\S+\s+)?remote\.(?:origin|upstream)\.\S+",
                    r"git\s+remote\s+(?:add|set-url)\s+\S+\s+(?:https?://github\.com/(?:NousResearch|hermes)|git@github\.com:)",
                    r"remote\s*=\s*[\"']?https?://github\.com/(?:NousResearch|hermes)",
                ]
                for pat in FOOTGUN:
                    if re.search(pat, cmdn):
                        blocked(
                            "DEV-ROOT GUARD: refusing to create/re-point an "
                            "origin/upstream remote — the upstream footgun must "
                            "never exist on the canonical repo. Remotes: `public` "
                            "(push) only; upstream reference is fetched on demand "
                            "into scratch clones."
                        )
                # 2. Update machinery: the exact fetch-and-reset trigger.
                if re.search(
                    r"(?:^|[;&|(])\s*(?:3v0|hermes)\s+update\b|(?:python\w*\s+)?-m\s+\S*\.main\s+update\b",
                    cmdn,
                ):
                    blocked(
                        "DEV-ROOT GUARD: `update` machinery fetches against "
                        "upstream and can reset the canonical branch — the exact "
                        "failure mode of the 2026-08-20 incident. Refusing. "
                        "Update 3V0 by pulling from `public` deliberately."
                    )
                # 3. Canonical branch movement: no reset/checkout to a
                #    remote-tracking ref (upstream/main, origin/main), and no
                #    hard reset / fetch+reset sequences at all on canonical.
                BRANCH_MOVE = [
                    r"git\s+(?:-C\s+\S+(?:\s+\S+)*\s+|--git-dir\S+\s+)?(?:reset|checkout|switch)\s+--?[^\n]*?\b(?:upstream|origin)/\S+",
                    r"git\s+(?:-C\s+\S+(?:\s+\S+)*\s+|--git-dir\S+\s+)?(?:reset|checkout|switch)\s+(?:--hard|--force|-f)\b",
                    r"git\s+fetch\s+(?:upstream|origin)\b.*?\n?\s*(?:git\s+reset|git\s+checkout)",
                ]
                for pat in BRANCH_MOVE:
                    if re.search(pat, cmdn, re.IGNORECASE):
                        blocked(
                            "DEV-ROOT GUARD: refusing movement of the canonical "
                            "branch to a remote-tracking ref or a hard reset — "
                            "the 2026-08-20 incident. Operate on `public/main` "
                            "and never hard-reset a live checkout."
                        )
    except SystemExit:
        raise
    except Exception:
        # Guard bug must not silently allow a write; block closed.
        sys.exit(2)

    # Not blocked: allow.
    sys.exit(0)


if __name__ == "__main__":
    main()