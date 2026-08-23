"""Contract tests for the ``_EV0_CORE_TOOLS`` narrow-waist footprint.

These assert the *behavioral intent* of the core toolset against a live
registry — not exact counts or literals, so they are not change-detectors
(AGENTS.md: "behavior contracts over snapshots"):

- **G1 — every capability-gated core tool must carry a ``check_fn``.** A tool
  in ``_EV0_CORE_TOOLS`` ships its schema on every API call of every platform
  bundle. Capability-gated tools (home assistant, kanban) that remain in core
  must be behind a non-None ``check_fn`` so they never ship unconditionally.
- **G1b — the niche opt-in tools must NOT be re-added to core.** ``bfl_flux3_*``,
  ``image_generate``, ``text_to_speech``, and ``computer_use`` were deliberately
  moved out of ``_EV0_CORE_TOOLS`` into their opt-in toolsets. A regression that
  re-adds any of them silently grows the waist (``computer_use`` alone is
  ~10 KB of schema). They must instead resolve from their opt-in toolset.
- **G2 — a loose upper-bound on the resolved ``3v0-cli`` schema set.** Guards
  against a single tool ballooning and being paid on every call. The bound is
  deliberately generous so routine description edits don't trip it.
"""

import json

import pytest

from tools.registry import registry
from toolsets import (
    _EV0_CORE_TOOLS,
    get_toolset,
    resolve_toolset,
)

# Capability-gated tools that REMAIN in core, so they MUST ship behind a
# non-None check_fn (never unconditionally). If one is moved to an opt-in
# toolset, remove it here and add it to _OPT_IN_NICHE_TOOLS instead.
_GATED_CORE_TOOLS = {
    # Home Assistant — gated on HASS_TOKEN.
    "ha_list_entities",
    "ha_get_state",
    "ha_list_services",
    "ha_call_service",
    # Kanban — gated on dispatcher context / opt-in kanban toolset.
    "kanban_show",
    "kanban_list",
    "kanban_complete",
    "kanban_block",
    "kanban_request_review",
    "kanban_request_changes",
    "kanban_heartbeat",
    "kanban_comment",
    "kanban_create",
    "kanban_link",
    "kanban_unblock",
    "kanban_attach",
    "kanban_attach_url",
    "kanban_attachments",
}

# Niche tools deliberately kept OUT of _EV0_CORE_TOOLS, mapped to the opt-in
# toolset that carries them. A regression that re-adds one to core defeats the
# narrow-waist goal; a new tool added to core that ought to be opt-in should be
# added here (and kept out of _EV0_CORE_TOOLS).
_OPT_IN_NICHE_TOOLS = {
    "image_generate": "image_gen",
    "text_to_speech": "tts",
    "computer_use": "computer_use",
    "bfl_flux3_text_to_video": "bfl",
    "bfl_flux3_image_to_video": "bfl",
    "bfl_flux3_keyframes_to_video": "bfl",
    "bfl_flux3_video_continuation": "bfl",
    "bfl_flux3_get_result": "bfl",
    "bfl_flux3_prompting_guide": "bfl",
}


@pytest.fixture(scope="module")
def _registry_entries():
    """Discover tools once and index the registry by name."""
    # Importing model_tools triggers built-in tool discovery.
    import model_tools  # noqa: F401

    return {e.name: e for e in registry.get_all_entries()}


class TestCoreToolsNarrowWaist:
    """Behavioral contracts protecting the _EV0_CORE_TOOLS footprint."""

    def test_gated_core_tools_all_carry_a_check_fn(self, _registry_entries):
        """Every capability-gated tool still in core must have a check_fn.

        The guard against a gated niche tool remaining in core yet shipping on
        every session (a dropped ``check_fn`` would expose its schema globally).
        """
        offenders = []
        for name in sorted(_GATED_CORE_TOOLS):
            entry = _registry_entries.get(name)
            assert entry is not None, (
                f"{name} is listed in _EV0_CORE_TOOLS but not registered in the "
                f"tool registry — the name is stale."
            )
            if entry.check_fn is None:
                offenders.append(name)
        assert not offenders, (
            f"Gated core tools with NO check_fn (would ship unconditionally on "
            f"every call): {offenders}. Give each a check_fn, or move it out of "
            f"_EV0_CORE_TOOLS into its opt-in toolset and into "
            f"_OPT_IN_NICHE_TOOLS."
        )

    def test_opt_in_niche_tools_not_in_core_and_resolvable(self, _registry_entries):
        """The moved niche tools stay out of core and resolve from toolsets.

        This locks the narrow-waist move: ``bfl_flux3_*``, ``image_generate``,
        ``text_to_speech``, and ``computer_use`` must NOT be back in
        ``_EV0_CORE_TOOLS``, must still be registered (so they can be enabled),
        and must resolve from their opt-in toolset via ``3v0 tools``.
        """
        core = set(_EV0_CORE_TOOLS)
        leaked = [t for t in _OPT_IN_NICHE_TOOLS if t in core]
        assert not leaked, (
            f"Niche opt-in tools were re-added to _EV0_CORE_TOOLS, growing the "
            f"waist on every call: {leaked}. Keep them in their opt-in toolsets "
            f"({sorted(set(_OPT_IN_NICHE_TOOLS.values()))})."
        )
        missing_resolution = []
        for tool, toolset in _OPT_IN_NICHE_TOOLS.items():
            entry = _registry_entries.get(tool)
            assert entry is not None, (
                f"{tool} has no registry entry — it must be registered to be "
                f"enableable via 3v0 tools."
            )
            assert get_toolset(toolset) is not None, (
                f"{tool} maps to toolset {toolset!r} which is not defined."
            )
            if tool not in resolve_toolset(toolset):
                missing_resolution.append((tool, toolset))
        assert not missing_resolution, (
            f"Tools not resolvable from their opt-in toolset: {missing_resolution}"
        )

    def test_all_core_tool_names_resolve_in_registry(self, _registry_entries):
        """No stale name in _EV0_CORE_TOOLS: every name must register a tool."""
        missing = [n for n in _EV0_CORE_TOOLS if n not in _registry_entries]
        assert not missing, f"_EV0_CORE_TOOLS names with no registry entry: {missing}"

    def test_resolved_cli_schema_set_under_loose_byte_budget(self, _registry_entries):
        """The full resolved ``3v0-cli`` schema set stays under a loose ceiling.

        A relational/behavioral guard, NOT a change-detector: the bound is set
        above the current footprint plus generous headroom so ordinary
        description edits pass, but a single ballooning schema trips it. Every
        byte here is input on every model call, at ~30x on cache-miss.
        """
        resolved = [n for n in resolve_toolset("3v0-cli") if n in _registry_entries]
        total = sum(
            len(json.dumps(_registry_entries[n].schema).encode())
            for n in resolved
        )
        # Generous headroom over the current footprint.
        assert total < 256 * 1024, (
            f"Resolved 3v0-cli schema set is {total // 1024} KB — over the 256 KB "
            f"narrow-waist guard. One or more core tools have ballooned; trim "
            f"schema/descriptions before this grows further."
        )