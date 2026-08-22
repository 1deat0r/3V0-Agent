"""Ticket #16: provider/vendor policy lives in one seam, not agent core."""

from agent import provider_policy as pp


class TestPolicySeamOwnership:
    def test_predicates_live_in_provider_policy(self):
        assert callable(pp.is_kimi_model)
        assert callable(pp.is_arcee_trinity_thinking)
        assert callable(pp.is_codex_gpt54_or_gpt55)
        assert callable(pp.is_codex_spark)
        assert callable(pp.fixed_temperature_for_model)
        assert callable(pp.compression_threshold_for_model)

    def test_auxiliary_client_reexports_for_backwards_compat(self):
        from agent import auxiliary_client as aux

        assert aux._is_kimi_model is pp.is_kimi_model
        assert aux._is_codex_spark is pp.is_codex_spark
        assert aux._fixed_temperature_for_model is pp.fixed_temperature_for_model
        assert aux._compression_threshold_for_model is pp.compression_threshold_for_model
        assert aux.OMIT_TEMPERATURE is pp.OMIT_TEMPERATURE

    def test_kimi(self):
        assert pp.is_kimi_model("moonshotai/kimi-k2.5") is True
        assert pp.is_kimi_model("kimi-k2-thinking") is True
        assert pp.is_kimi_model("claude-sonnet-4") is False

    def test_arcee_trinity(self):
        assert pp.is_arcee_trinity_thinking("arcee/trinity-large-thinking") is True
        assert pp.is_arcee_trinity_thinking("trinity-large-thinking") is True
        assert pp.is_arcee_trinity_thinking("gpt-5.4") is False

    def test_codex_gpt55_only_on_codex_route(self):
        assert pp.is_codex_gpt54_or_gpt55("gpt-5.6-sol", provider="openai-codex") is True
        assert pp.is_codex_gpt54_or_gpt55("gpt-5.6-sol", provider="openai") is False
        assert pp.is_codex_gpt54_or_gpt55("claude-sonnet-4", provider="openai-codex") is False

    def test_spark_only_on_codex_route(self):
        assert pp.is_codex_spark("gpt-5.3-codex-spark", provider="openai-codex") is True
        assert pp.is_codex_spark("gpt-5.3-codex-spark", provider="openai") is False

    def test_temperature_policy(self):
        assert pp.fixed_temperature_for_model("kimi-k2.5") is pp.OMIT_TEMPERATURE
        assert pp.fixed_temperature_for_model("arcee/trinity-large-thinking") == 0.5
        assert pp.fixed_temperature_for_model("gpt-5.4") is None

    def test_compression_policy(self):
        assert pp.compression_threshold_for_model("arcee/trinity-large-thinking") == 0.75
        assert (
            pp.compression_threshold_for_model(
                "gpt-5.6-sol", provider="openai-codex"
            )
            == pp.CODEX_GPT54_GPT55_COMPACTION_THRESHOLD
        )
        assert (
            pp.compression_threshold_for_model(
                "gpt-5.6-sol", provider="openai-codex", allow_codex_gpt55_autoraise=False
            )
            is None
        )
        assert (
            pp.compression_threshold_for_model("gpt-5.3-codex-spark", provider="openai-codex")
            == pp.CODEX_SPARK_COMPACTION_THRESHOLD
        )