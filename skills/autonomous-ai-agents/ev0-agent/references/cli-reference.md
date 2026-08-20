# 3V0 CLI Reference

Live sources when anything looks stale: `3v0 --help`, `3v0 <command> --help`,
https://github.com/1deat0r/3V0-Agent/docs/reference/cli-commands

### Global Flags

```
3v0 [flags] [command]        (no subcommand = interactive chat)

  --version, -V             Show version
  -z, --oneshot PROMPT      One-shot: print ONLY the final response (for scripts/pipes)
  -m MODEL  --provider P    Model/provider override for this invocation
  -t, --toolsets LIST       Comma-separated toolsets for this invocation
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --tui / --cli             Force the Ink TUI / classic REPL
  --ignore-rules            Skip AGENTS.md/SOUL.md/memory/skill injection
  --safe-mode               Disable ALL customizations (troubleshooting)
  --pass-session-id         Include session ID in system prompt
```

### Chat

```
3v0 chat [flags]
  -q, --query TEXT          Single query, non-interactive
  --image PATH              Attach a local image to a single query
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --max-turns N             Cap tool-calling iterations
  --source TAG              Session source tag (default: cli)
```
(plus the global flags above)

### Configuration

```
3v0 setup [section]      Wizard (model|tts|terminal|gateway|tools|agent)
3v0 model                Interactive model/provider picker
3v0 fallback [add|remove|list]  Fallback provider chain
3v0 config [show|edit|get|set|unset|path|env-path|check|migrate]
3v0 login / logout       OAuth sign-in / clear stored auth
3v0 doctor [--fix]       Check dependencies and config
3v0 status [--all]       Component status
```

### Tools & Skills

```
3v0 tools [list|enable NAME|disable NAME]   Per-platform toolsets (curses UI with no args)

3v0 skills list|browse|search QUERY|inspect ID
3v0 skills install ID    Hub identifier OR a direct https://…/SKILL.md URL
3v0 skills config        Enable/disable skills per platform
3v0 skills check|update|uninstall|publish PATH
3v0 skills tap add REPO  Add a GitHub repo as a skill source
3v0 bundles              Skill bundles (one /<name> alias loads several skills)
```

### MCP Servers

```
3v0 mcp add NAME (--url or --command) | remove | list | test NAME
3v0 mcp catalog | install NAME     Curated catalog install
3v0 mcp configure NAME             Toggle tool selection
3v0 mcp serve                      Run 3V0 as an MCP server
```
Details (transport, tool discovery, catalog): `references/native-mcp.md`.

### Gateway (Messaging Platforms)

```
3v0 gateway run|install|start|stop|restart|status|setup
```

20+ platforms: Telegram, Discord, Slack, WhatsApp (Baileys + Business Cloud API), iMessage (Photon — `3v0 photon setup`), Signal, Email, SMS, Matrix, Mattermost, Teams, LINE, SimpleX, ntfy, Google Chat, Home Assistant, DingTalk, Feishu, WeCom, Weixin, API Server, Webhooks. Open WebUI connects via the API Server adapter. Most adapters ship under `plugins/platforms/`.
Docs: https://github.com/1deat0r/3V0-Agent/docs/user-guide/messaging/

### Sessions

```
3v0 sessions list|browse|rename ID TITLE|delete ID|export OUT|prune|stats
```

### Cron / Webhooks

```
3v0 cron list|create SCHED|edit ID|pause|resume|run ID|remove|status
    Schedules: '30m', 'every 2h', '0 9 * * *', ISO timestamp
3v0 webhook subscribe NAME|list|remove NAME|test NAME
```
Webhook payloads/routes: `references/webhooks.md`.

### Profiles

```
3v0 profile list|create NAME (--clone|--clone-all|--clone-from)|use|show|delete
3v0 profile rename A B | alias NAME | export NAME | import FILE
```

### Credentials & Pools

```
3v0 auth                 Interactive credential manager
3v0 auth add [PROVIDER]  Add OAuth or API-key credential (nous, openai-codex, qwen-oauth, …)
3v0 auth list|remove P IDX|reset PROVIDER|status
```
Multiple credentials per provider form a pool that rotates automatically and skips exhausted keys.

### Other

```
3v0 desktop / gui        Native desktop app
3v0 dashboard            Web admin panel + embedded chat (--stop / --status)
3v0 proxy                OpenAI-compatible local proxy backed by an OAuth provider
3v0 portal               Quick setup / sign in via Nous Portal
3v0 kanban <verb>        Multi-agent work-queue board
3v0 project              Named multi-folder workspaces
3v0 skin list|use|set    Switch/tweak skins (see references/themes.md)
3v0 pets <verb>          Pet mascots (see references/petdex.md)
3v0 memory setup|status|off|reset   Memory provider
3v0 secrets bitwarden|onepassword   External secret stores
3v0 moa                  Mixture-of-Agents slots
3v0 hooks / security / backup / import / checkpoints / console
3v0 logs [-f] [errors]   View agent/error logs
3v0 send                 One-off message through a gateway platform
3v0 pairing / plugins / insights / journey / computer-use
3v0 acp                  ACP server (IDE integration)
3v0 completion bash|zsh|fish
3v0 update / uninstall / claw migrate
```

Plugin- and provider-supplied subcommands (e.g. `3v0 photon setup`) only appear once their plugin is installed/active.

### Where to Find Things

| Looking for... | Location |
|---|---|
| Config options | `3v0 config edit` · [Configuration docs](https://github.com/1deat0r/3V0-Agent/docs/user-guide/configuration) |
| Tools / toolsets | `3v0 tools list` · [Tools reference](https://github.com/1deat0r/3V0-Agent/docs/reference/tools-reference) |
| Skills catalog | `3v0 skills browse` · [Skills catalog](https://github.com/1deat0r/3V0-Agent/docs/reference/skills-catalog) |
| Provider setup | `3v0 model` · [Providers guide](https://github.com/1deat0r/3V0-Agent/docs/integrations/providers) |
| Env variables | `3v0 config env-path` · [Env vars reference](https://github.com/1deat0r/3V0-Agent/docs/reference/environment-variables) |
| Gateway logs | `~/.3V0/logs/gateway.log` (or `3v0 logs`) |
| Sessions | `3v0 sessions browse` (reads state.db) |
