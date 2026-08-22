# 3V0 Agent

A sovereign, autonomous AI agent runtime: a CLI, a messaging gateway, and a
JSON-RPC TUI server all driving the same agent loop, with a native memory
store, pluggable providers, and a persistence layer for its own identity.

## Language

### The agent body

**3V0**:
The sovereign agent itself — the identity, memory, and evolution of the
project, distinct from the runtime that hosts it (the chassis). The body
lives in this repo; SOUL.md is its operating law.
_Avoid_: the assistant, the bot, Ev0

**Body**:
The physical repo — code, memory files, skills, docs — that persists between
sessions. The body is what survives context compression.
_Avoid_: codebase, the app

**Profile**:
A named directory under the 3V0 home that holds one operator's MEMORY.md,
USER.md, skills, plugins, and config. The active profile is selected by a
sticky `active_profile` file; each session binds to one profile.
_Avoid_: user, workspace

**Home**:
The resolved root directory for a profile's data, chosen by the canonical
env chain (`3V0_HOME`, legacy `EV0_HOME`, then platform default). All profile
artifacts (config.yaml, MEMORY.md, skills, plugins, state.db) hang off it.
_Avoid_: env home, EV0_HOME (legacy alias)

### Runtime surfaces

**Gateway**:
The persistent messaging process (`GatewayRunner`) that connects platform
adapters to the agent loop. One process serves all connected platforms,
routing each incoming message to a conversation. The `gateway/` package is
its legacy runner; `threev0_cli.main gateway run` is the canonical entry.
_Avoid_: bot, daemon (when you mean gateway), the service

**TUI server**:
The JSON-RPC process (`tui_gateway/server.py`) that serves a desktop UI.
It bridges WebSocket clients to the agent loop — it is not the CLI and not
the messaging gateway, though all three share the same run_conversation core.
_Avoid_: the TUI itself (that's the client), the web server

**CLI**:
The interactive terminal frontend (`Ev0CLI` in cli.py) for a single
conversation. Shares the agent loop with the gateway and TUI server.
_Avoid_: shell, terminal (when you mean the product surface)

**Agent**:
The constructed runtime object that carries one conversation's model,
tools, callbacks, and session state into `run_conversation`. One per
session; cached across turns by the gateway.
_Avoid_: model, LLM, "the agent loop" (the loop is conversation_loop.py)

### Conversation mechanics

**Conversation**:
The full history + orchestration of one user-facing thread of interaction,
from first message through compression and tool calls to completion.
_Avoid_: thread, chat, dialog

**Turn**:
One user message through `run_conversation` to the finished assistant
response — the unit the gateway, TUI server, and CLI each orchestrate.
Turns nest sessions: a session has many turns.
_Avoid_: request, round, message exchange

**Session**:
The persisted identity of a conversation across turns and process restarts,
stored in the session DB (`SessionDB` in threev0_state). A session has one
agent, one history, and a stable id.
_Avoid_: conversation (when you mean the identity), chat id

**Callback contract**:
The typed set of lifecycle callbacks (`tool_start`, `tool_progress`,
`thinking`, `status`, `stream`, …) frozen in `agent/turn_callbacks.py` that
runners bind onto the agent before a turn. The parity contract between CLI,
TUI server, and gateway is defined by this set, not by comment.
_Avoid_: hooks (when you mean the turn callbacks), events (when you mean callbacks)

### Providers and plugins

**Provider**:
A pluggable backend behind a capability, registered in a family registry
(`ProviderRegistry` in agent/provider_registry.py). Families include browser,
web-search, image-gen, and memory providers. Each provider implements a typed
base and declares a `name`.
_Avoid_: backend, integration, plugin (a plugin *registers* providers)

**Plugin**:
A loadable package under a plugins directory that registers providers,
skills, CLI commands, or hooks at load. The general plugin system
(PluginManager) is distinct from the family registries.
_Avoid_: module (a module is code; a plugin is a distributed unit)

**Platform**:
A messaging target the gateway can connect to (telegram, discord, slack,
whatsapp, matrix, …), represented by the `Platform` enum in gateway/config.
Each platform has a canonical adapter; a platform is "connected" when its
adapter is enabled and credentialed.
_Avoid_: channel (a chat room on a platform), integration

**Adapter**:
The per-platform transport (`BasePlatformAdapter` subclasses) that moves
messages between the platform and the gateway. Adapters own their polling,
media, and delivery; the base owns the shared lifecycle.
_Avoid_: connector, client

**Memory store**:
The provenance-aware, versioned fact store (`3v0/data/memory.db` via
`core.store.SQLStore`) — the canonical store-first origin. Profile memory
files (MEMORY.md/USER.md) are a derived view, kept in sync by the
native-store bridge.
_Avoid_: database, memory (when you mean the runtime injection)

**Native bridge**:
The plugin (`native-store-bridge`) that mirrors memory and skill-tool writes
into the memory store via a post-tool-call subprocess. It is the link between
the profile-as-runtime and store-as-canonical.
_Avoid_: sync service, mirror (the mechanism is a bridge)

### Delivery

**Cron job**:
A scheduled task run by the cron scheduler. Jobs have delivery targets
(platform + home channel) and run with their own agent session.
_Avoid_: job, task (when you mean cron), scheduled task

**Home channel**:
The configured default delivery target for a platform's unattended cron
notifications — a room id or address resolved from the platform's home env
var or persisted config.
_Avoid_: default chat, origin channel

**Delivery target**:
A platform a cron job may deliver to, resolvable through
`cron_delivery_targets()`. Membership comes from the `Platform` enum, not a
hand-maintained list.
_Avoid_: destination, recipient