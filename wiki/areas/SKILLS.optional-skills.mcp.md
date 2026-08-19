# skills/ + optional-skills/ — the skill libraries — `optional-skills/mcp/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `optional-skills/mcp/DESCRIPTION.md` | doc | MCP | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/mcp/fastmcp/SKILL.md; optional-skills/mcp/fastmcp/references/fastmcp-cli.md; optional-skills/mcp/fastmcp/scripts/scaffold_fastmcp.py |
| `optional-skills/mcp/fastmcp/SKILL.md` | skill-doc | Skill definition for `fastmcp` | The instruction contract a model loads when the skill's trigger matches | optional-skills/mcp/fastmcp/references/fastmcp-cli.md; optional-skills/mcp/fastmcp/scripts/scaffold_fastmcp.py; optional-skills/mcp/fastmcp/templates/api_wrapper.py |
| `optional-skills/mcp/fastmcp/references/fastmcp-cli.md` | doc | FastMCP CLI Reference | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/mcp/fastmcp/references/ |
| `optional-skills/mcp/fastmcp/scripts/scaffold_fastmcp.py` | source | Copy a FastMCP starter template into a working file. | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/mcp/fastmcp/scripts/ |
| `optional-skills/mcp/fastmcp/templates/api_wrapper.py` | source | Python module `api_wrapper.py` | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/mcp/fastmcp/templates/database_server.py; optional-skills/mcp/fastmcp/templates/file_processor.py |
| `optional-skills/mcp/fastmcp/templates/database_server.py` | source | Python module `database_server.py` | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/mcp/fastmcp/templates/api_wrapper.py; optional-skills/mcp/fastmcp/templates/file_processor.py |
| `optional-skills/mcp/fastmcp/templates/file_processor.py` | source | Python module `file_processor.py` | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/mcp/fastmcp/templates/api_wrapper.py; optional-skills/mcp/fastmcp/templates/database_server.py |
| `optional-skills/mcp/mcp-oauth-remote-gateway/SKILL.md` | skill-doc | Skill definition for `mcp-oauth-remote-gateway` | The instruction contract a model loads when the skill's trigger matches | optional-skills/mcp/mcp-oauth-remote-gateway/references/stripe-mcp-oauth-revocation.md; optional-skills/mcp/mcp-oauth-remote-gateway/scripts/diagnose-oauth-mcp.py |
| `optional-skills/mcp/mcp-oauth-remote-gateway/references/stripe-mcp-oauth-revocation.md` | doc | Stripe MCP (`mcp.stripe.com`) — recurring OAuth session revocation, fix with a restricted key | Human/agent-readable documentation; the wiki keeps it pointer-capped | optional-skills/mcp/mcp-oauth-remote-gateway/references/ |
| `optional-skills/mcp/mcp-oauth-remote-gateway/scripts/diagnose-oauth-mcp.py` | source | Diagnose an OAuth-gated remote MCP server's connection state. | Python module executed or imported by the runtime; check git intent before deleting | optional-skills/mcp/mcp-oauth-remote-gateway/scripts/ |
| `optional-skills/mcp/mcporter/SKILL.md` | skill-doc | Skill definition for `mcporter` | The instruction contract a model loads when the skill's trigger matches | optional-skills/mcp/mcporter/ |
