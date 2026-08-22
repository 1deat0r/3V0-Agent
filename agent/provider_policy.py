"""Provider/vendor capability policy (ticket #16).

Policy = decisions that depend on WHO the provider is, not on the agent loop:
  - which models manage temperature server-side (Kimi/Moonshot),
  - which families need a raised context-compaction trigger (Codex OAuth
    route's 272K / 128K caps, Arcee Trinity thinking),
  - which routes must omit ``temperature`` entirely.

These used to live inside ``agent/auxiliary_client.py``; they are pure
predicates over (model, provider, base_url) and have no dependency on the
auxiliary client machinery. Keeping them here means every consumer (aux
client, conversation loop, model picker) reads one source of truth instead
of hand-copying vendor rules.

If a new vendor needs special-casing, add the predicate HERE — not in the
turn loop.
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Sentinel: caller must remove the ``temperature`` key entirely.
OMIT_TEMPERATURE = object()


def is_kimi_model(model: Optional[str]) -> bool:
    """True for any Kimi / Moonshot model that manages temperature server-side."""
    bare = (model or "").strip().lower().rsplit("/", 1)[-1]
    return bare.startswith("kimi-") or bare == "kimi"


def is_arcee_trinity_thinking(model: Optional[str]) -> bool:
    """True for Arcee Trinity Large Thinking (direct or via OpenRouter)."""
    bare = (model or "").strip().lower().rsplit("/", 1)[-1]
    return bare == "trinity-large-thinking"


# Context window enforced by ChatGPT's Codex OAuth backend for the
# gpt-5.4 / gpt-5.5 / gpt-5.6 families. The raw OpenAI API and OpenRouter
# expose 1.05M for the same slugs, but the Codex backend hard-caps at 272K
# (verified live for 5.4/5.5: a ~330K-token request to
# chatgpt.com/backend-api/codex/responses is rejected with
# ``context_length_exceeded`` while ~250K succeeds; gpt-5.6 shares the same
# 272K Codex cap — see _CODEX_OAUTH_CONTEXT_FALLBACK in model_metadata.py).
# With a 272K ceiling the default 50% compaction trigger fires at ~136K —
# wasteful, since the model can hold far more raw context before
# summarization actually buys anything. We raise the trigger to 85% (~231K)
# on this exact route so Codex gpt-5.4 / gpt-5.5 / gpt-5.6 sessions use the
# window they actually have.
CODEX_GPT54_GPT55_COMPACTION_THRESHOLD = 0.85

# gpt-5.3-codex-spark is Codex-OAuth-only (ChatGPT Pro entitlement) with a
# native 128K context window.  The default 50% compaction trigger fires at
# ~64K — wasting half the usable window, often before the session has enough
# turns to summarize meaningfully.  We raise the trigger to 70% (~90K) so
# spark sessions use more of the window before summarization, while still
# leaving ~38K headroom for the summary and continued conversation before
# the 128K hard limit.
CODEX_SPARK_COMPACTION_THRESHOLD = 0.70


def is_codex_gpt54_or_gpt55(model: Optional[str], provider: Optional[str] = None) -> bool:
    """True for gpt-5.4 / gpt-5.5 / gpt-5.6 on the ChatGPT Codex OAuth backend.

    Matches only the Codex OAuth route (provider ``openai-codex``), not the
    direct OpenAI API, OpenRouter, or GitHub Copilot paths — those expose a
    larger context window for the same slug and must keep the user's default
    compaction threshold. ``-pro`` variants and dated snapshots are matched
    via prefix so the override tracks every 272K-capped family (5.4, 5.5,
    5.6 sol/terra/luna incl. their ``-pro`` modes) without re-listing every
    variant. (Name kept for backward compatibility with the
    ``compression.codex_gpt55_autoraise`` config key.)
    """
    prov = (provider or "").strip().lower()
    if prov != "openai-codex":
        return False
    bare = (model or "").strip().lower().rsplit("/", 1)[-1]
    return (
        bare == "gpt-5.4"
        or bare.startswith("gpt-5.4-")
        or bare.startswith("gpt-5.4.")
        or bare == "gpt-5.5"
        or bare.startswith("gpt-5.5-")
        or bare.startswith("gpt-5.5.")
        or bare == "gpt-5.6"
        or bare.startswith("gpt-5.6-")
        or bare.startswith("gpt-5.6.")
    )


def is_codex_spark(model: Optional[str], provider: Optional[str] = None) -> bool:
    """True for ``gpt-5.3-codex-spark`` on the ChatGPT Codex OAuth backend.

    The model is Codex-OAuth-only (ChatGPT Pro entitlement) with a native
    128K context window.  Only the Codex OAuth route (provider
    ``openai-codex``) is matched — the slug is not available on other
    routes.
    """
    prov = (provider or "").strip().lower()
    if prov != "openai-codex":
        return False
    bare = (model or "").strip().lower().rsplit("/", 1)[-1]
    return bare == "gpt-5.3-codex-spark"


def fixed_temperature_for_model(
    model: Optional[str],
    base_url: Optional[str] = None,
) -> "Optional[float] | object":
    """Return a temperature directive for models with strict contracts.

    Returns:
        ``OMIT_TEMPERATURE`` — caller must remove the ``temperature`` key so the
            provider chooses its own default.  Used for all Kimi / Moonshot
            models whose gateway selects temperature server-side.
        ``float`` — a specific value the caller must use (reserved for future
            models with fixed-temperature contracts).
        ``None`` — no override; caller should use its own default.
    """
    if is_kimi_model(model):
        logger.debug("Omitting temperature for Kimi model %r (server-managed)", model)
        return OMIT_TEMPERATURE
    if is_arcee_trinity_thinking(model):
        return 0.5
    return None


def compression_threshold_for_model(
    model: Optional[str],
    provider: Optional[str] = None,
    *,
    allow_codex_gpt55_autoraise: bool = True,
) -> Optional[float]:
    """Return a context-compression threshold override for specific models.

    The threshold is the fraction of the model's context window that must be
    consumed before 3V0 triggers summarization.  Higher values delay
    compression and preserve more raw context.

    Per-model/route overrides:
      - Arcee Trinity Large Thinking → 0.75 (preserve reasoning context).
      - gpt-5.4 / gpt-5.5 / gpt-5.6 on the Codex OAuth route → 0.85, because
        Codex caps all three families at 272K and the default 50% trigger
        would compact at ~136K. Gated by ``allow_codex_gpt55_autoraise``
        (historical config-key name kept for backward compatibility) so the
        user can opt back down to the global default (the caller passes the
        config flag through here).
      - gpt-5.3-codex-spark on the Codex OAuth route → 0.70, because the model
        has a native 128K window and the default 50% trigger would compact at
        ~64K — wasting half the usable context. Not gated by the gpt-5.5
        opt-out flag: 128K is the model's native window, so the raise is
        unambiguously correct.

    Returns a float in (0, 1] to override the global ``compression.threshold``
    config value, or ``None`` to leave the user's config value unchanged.
    """
    if is_arcee_trinity_thinking(model):
        return 0.75
    if allow_codex_gpt55_autoraise and is_codex_gpt54_or_gpt55(model, provider):
        return CODEX_GPT54_GPT55_COMPACTION_THRESHOLD
    if is_codex_spark(model, provider):
        return CODEX_SPARK_COMPACTION_THRESHOLD
    return None