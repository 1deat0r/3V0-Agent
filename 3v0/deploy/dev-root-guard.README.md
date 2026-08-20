# 3V0 dev-root guard

Structural enforcement that 3V0 **never develops in the wrong folder**.

## The rule
- Code is developed **only** in `/home/mustbearn/Projects/AI Agents/3V0 Agent`.
- The following trees are **READ-ONLY references** — never write, never commit
  into them:
  - `~/.hermes/hermes-agent` (old pre-cutover runtime checkout)
  - `~/.3V0/hermes-agent` (copy of the old runtime inside the new home)
  - `~/Projects/Research/hermes-agent-repo` (pristine upstream clone)

## How it's enforced
Installed as a Hermes `pre_tool_call` shell hook (`fail_closed: true`) so it
fires on every tool call in the live profile:

```yaml
hooks:
  pre_tool_call:
    - command: "python3 /home/mustbearn/.3V0/profiles/3v0/hooks/dev-root-guard.py"
      fail_closed: true
hooks_auto_accept: true
```

The hook binary exits `2` (blocking the tool call) when:
- a `write_file`/`patch` targets a forbidden tree, or
- a terminal command *directs a write* at a forbidden tree (shell redirect
  into it, `git -C <tree> commit`, `cd <tree> && git …`, or a write verb with
  the tree as an operand).

Reads of the forbidden trees are **allowed** — that's how cutover diagnostics
work. Merely referencing a forbidden path (e.g. running an interpreter that
lives there) is not a write and passes.

## Install / re-install
```bash
cp 3v0/deploy/dev-root-guard.py ~/.3V0/profiles/3v0/hooks/dev-root-guard.py
```
(Config wiring lives in the profile's `config.yaml`; use `hermes config set`
per the repo invariant.)

## Test
```bash
python3 3v0/deploy/dev-root-guard.py <<< '{"tool_name":"write_file","tool_input":{"path":"/home/mustbearn/.hermes/hermes-agent/x.py"}}'
# → exits 2 (blocked). Good.
```