# 3V0 Token-Efficiency Policy

Established 2026-08-18. This is the canonical operating policy for how 3V0
spends its DeepSeek tokens. It is a body document — it persists across
sessions even when memory is compressed — and it is the source of truth for
the "SOTA token-efficiency" stance.

## TL;DR

1. **Reasoning (output) tokens are the dominant cost — right-size effort.**
2. **Maximize prompt-cache hit ratio — keep the prefix stable.**
3. **Prune bulky tool output deterministically, not per-turn.**
4. **Route background/aux LLM work to `deepseek-v4-flash`.**
5. **Keep memory compact and high-signal.**

## DeepSeek V4-Pro economics (why this order)

Per 1M tokens, off-peak (peak = ×2, 01:00–04:00 + 06:00–10:00 UTC):

| Class | $/1M | Multiplier vs cache-hit |
|-------|------|------------------------|
| Input, cache-hit  | $0.022 | 1× |
| Input, cache-miss | $0.66  | 30× |
| Output (incl. reasoning) | $1.98 | 90× |

Consequences:

- **Output tokens are ~90× more expensive than cache-hit input.** Reasoning
  effort is the single biggest cost dial. A `max` reasoning pass on a hard
  question can dwarf the entire prompt.
- **Cache hits are nearly free.** DeepSeek caches automatically on a stable
  prefix (no config). The agent loop re-sends the whole prefix every turn;
  every token that stays byte-identical is a cache-hit. Therefore *breaking
  the prefix mid-conversation is the costliest mistake you can make* — it
  turns the entire growing history back into cache-miss input.
- This matches the literature: "Token Reduction Is Not Cost Reduction"
  (arXiv 2607.12161) — naive prompt compression that rewrites sent history
  per-turn *increases* billed cost by destroying the cache, even though it
  reduces token *counts*.

## Model context window

`deepseek-v4-pro` and `deepseek-v4-flash` both report a **1,000,000-token**
context window (`agent/model_metadata.py`). The default compression
`threshold: 0.50` therefore means "compress at ~500K tokens" — which
practically never fires, so old tool output rides in history and is re-sent
every turn. The deterministic prune below is the real guard.

## Config applied (2026-08-18)

```yaml
compression:
  proactive_prune_tokens: 48000   # deterministic no-LLM prune of bulky old
                                  # tool results once context >48K tokens;
                                  # gated by min_reclaim=4096 so cache breaks
                                  # stay episodic, never per-turn
agent:
  reasoning_effort: high          # explicit default (was implicit); see policy
auxiliary:
  curator:
    model: deepseek-v4-flash      # background skill-review on the cheap model
```

**Deliberately NOT set:**

- `compression.micro_compact` stays `false` — it rewrites sent history every
  turn, breaking the cache prefix every turn (the exact arXiv anti-pattern).
- `compression.proactive_prune_tokens` is NOT set lower than 48K — below that
  you start reclaiming context you still need in a coding session.
- `agent.reasoning_effort` is NOT `low` globally — 3V0's judgment is the
  deliverable (see SOUL.md). `low` is reserved for bulk/mechanical work.
- `fallback_model` stays disabled — it could route away from DeepSeek
  (Prime Directive).

## Operating policy

- **Right-size reasoning.** Default `high`. Drop to `low` only for bulk
  mechanical harvests (mass extraction, mechanical regex/format jobs) via a
  per-cron `reasoning_overrides` or `agent.reasoning_effort` override. Use
  `max` sparingly for genuinely deep design/architecture judgment.
- **Protect the prefix.** Never edit SOUL.md, AGENTS.md, memory, or switch
  toolsets mid-conversation. Slash commands that mutate system-prompt state
  defer to next session (Hermes cache-awareness) unless `--now` is justified.
- **Cheap aux.** All `auxiliary.*` tasks resolve `provider: auto` →
  `default_aux_model=deepseek-v4-flash` automatically (compression, vision,
  titles). Curator was the exception (`auto` = main model) — now pinned to
  flash. Keep it that way.
- **Compact memory.** Memory + user profile are ~1,300 tokens injected every
  turn. Keep entries high-signal; consolidate instead of appending; never
  store re-discoverable data (paths, addresses, IDs) that a file already
  holds.
- **Prefer off-peak** (outside 01–04 / 06–10 UTC) for heavy autonomous LLM
  work — bulk harvests, large review drains, curator passes.

## Verification

- `hermes config check` — no ✗ items; config version current.
- `hermes config get compression.proactive_prune_tokens` → `48000`.
- Model pin `deepseek-v4-pro` survives any `hermes config migrate`.
- Memory usage < 100% (headroom available) after a consolidation pass.

## Change log

- 2026-08-18 — established; set `proactive_prune_tokens=48000`,
  `reasoning_effort=high`, `auxiliary.curator.model=deepseek-v4-flash`;
  consolidated memory 16→15 entries (99%→95%).
