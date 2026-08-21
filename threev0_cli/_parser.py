"""
Top-level argparse construction for the 3v0 CLI.

Lives in its own module so other modules (e.g. ``relaunch.py``) can
introspect the parser to discover which flags exist without running the
``main`` fn.

Only the top-level parser and the ``chat`` subparser live here. Every other
subparser (model, gateway, sessions, …) is built inline in ``main.py``
because its dispatch is tightly coupled to module-level ``cmd_*`` functions.
"""

import argparse


# `--profile` / `-p` is consumed by ``main._apply_profile_override`` before
# argparse runs (it sets ``EV0_HOME`` and strips itself from ``sys.argv``),
# so it isn't on the parser. Listed here so all "carry over on relaunch"
# metadata lives in one file.
PRE_ARGPARSE_INHERITED_FLAGS: list[tuple[str, bool]] = [
    ("--profile", True),
    ("-p", True),
]


def _inherited_flag(parser, *args, **kwargs):
    """Register a flag that ``threev0_cli.relaunch`` should carry over when
    the CLI re-execs itself (e.g. after ``sessions browse`` picks a session,
    or after the setup wizard launches chat).

    Equivalent to ``parser.add_argument(...)`` plus tagging the resulting
    Action with ``inherit_on_relaunch = True`` so the relaunch table builder
    can find it via introspection.
    """
    action = parser.add_argument(*args, **kwargs)
    action.inherit_on_relaunch = True
    return action


_EPILOGUE = """
Examples:
    3v0                        Start interactive chat
    3v0 chat -q "Hello"        Single query mode
    3v0 --tui                  Launch the modern TUI (or set display.interface: tui)
    3v0 --cli                  Force the classic REPL (overrides display.interface: tui)
    3v0 -c                     Resume the most recent session
    3v0 -c "my project"        Resume a session by name (latest in lineage)
    3v0 --resume <session_id>  Resume a specific session by ID
    3v0 --resume latest        Resume the most recent session (same as -c)
    3v0 --tui --resume latest --in ./dir   Resume ./dir's latest session in the TUI
    3v0 setup                  Run setup wizard
    3v0 logout                 Clear stored authentication
    3v0 auth add <provider>    Add a pooled credential
    3v0 auth list              List pooled credentials
    3v0 auth remove <p> <t>    Remove pooled credential by index, id, or label
    3v0 auth reset <provider>  Clear exhaustion status for a provider
    3v0 model                  Select default model
    3v0 fallback [list]        Show fallback provider chain
    3v0 fallback add           Add a fallback provider (same picker as `3v0 model`)
    3v0 fallback remove        Remove a fallback provider from the chain
    3v0 config                 View configuration
    3v0 config edit            Edit config in $EDITOR
    3v0 config set model gpt-4 Set a config value
    3v0 gateway                Run messaging gateway
    3v0 -s 3v0-agent-dev,github-auth
    3v0 -w                     Start in isolated git worktree
    3v0 gateway install        Install gateway background service
    3v0 sessions list          List past sessions
    3v0 sessions browse        Interactive session picker
    3v0 sessions rename ID T   Rename/title a session
    3v0 logs                   View agent.log (last 50 lines)
    3v0 logs -f                Follow agent.log in real time
    3v0 logs errors            View errors.log
    3v0 logs --since 1h        Lines from the last hour
    3v0 debug share             Upload debug report for support
    3v0 console                Open the safe 3V0 command console
    3v0 update                 Update to latest version
    3v0 dashboard              Start web UI dashboard (port 9119)
    3v0 dashboard --stop       Stop running dashboard processes
    3v0 dashboard --status     List running dashboard processes

For more help on a command:
    3v0 <command> --help
"""


def build_top_level_parser():
    """Build the top-level parser, the subparsers action, and the ``chat`` subparser.

    Returns ``(parser, subparsers, chat_parser)``. The caller wires
    ``chat_parser.set_defaults(func=cmd_chat)`` and continues registering
    other subparsers via ``subparsers.add_parser(...)``.
    """
    parser = argparse.ArgumentParser(
        prog="3v0",
        description="3V0 Agent - AI assistant with tool-calling capabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_EPILOGUE,
    )

    parser.add_argument(
        "--version", "-V", action="store_true", help="Show version and exit"
    )
    parser.add_argument(
        "-z",
        "--oneshot",
        metavar="PROMPT",
        default=None,
        help=(
            "One-shot mode: send a single prompt and print ONLY the final "
            "response text to stdout. No banner, no spinner, no tool "
            "previews, no session_id line. Tools, memory, rules, and "
            "AGENTS.md in the CWD are loaded as normal; approvals are "
            "auto-bypassed. Intended for scripts / pipes."
        ),
    )
    parser.add_argument(
        "--usage-file",
        metavar="PATH",
        default=None,
        help=(
            "One-shot mode only: after the run, write a JSON usage report "
            "(estimated cost, token counts, model, api_calls) to PATH. "
            "The report is written even when the run fails, so pipelines "
            "can always account for spend. No effect outside -z/--oneshot."
        ),
    )
    # --model / --provider are accepted at the top level so they can pair
    # with -z without needing the `chat` subcommand.  If neither -z nor a
    # subcommand consumes them, they fall through harmlessly as None.
    # Mirrors `3v0 chat --model ... --provider ...` semantics.
    _inherited_flag(
        parser,
        "-m",
        "--model",
        default=None,
        help=(
            "Model override for this invocation (e.g. anthropic/claude-sonnet-4.6). "
            "Applies to -z/--oneshot and --tui. Also settable via EV0_INFERENCE_MODEL env var."
        ),
    )
    _inherited_flag(
        parser,
        "--provider",
        default=None,
        help=(
            "Provider override for this invocation (e.g. openrouter, anthropic). "
            "Applies to -z/--oneshot and --tui. The persistent provider lives in config.yaml "
            "under model.provider — use `3v0 setup` or edit the file to change it."
        ),
    )
    _inherited_flag(
        parser,
        "--reasoning",
        default=None,
        metavar="LEVEL",
        help=(
            "Reasoning effort for this invocation: none, minimal, low, medium, "
            "high, xhigh, max, or ultra. Overrides agent.reasoning_effort in "
            "config.yaml for this run only; the persistent level lives there "
            "(or per-model under agent.reasoning_overrides)."
        ),
    )
    parser.add_argument(
        "-t",
        "--toolsets",
        default=None,
        help="Comma-separated toolsets to enable for this invocation. Applies to -z/--oneshot and --tui.",
    )
    parser.add_argument(
        "--resume",
        "-r",
        metavar="SESSION",
        default=None,
        help=(
            "Resume a previous session by ID or title, or pass 'latest' for "
            "the most recent session (workspace-scoped, like -c with no name)"
        ),
    )
    parser.add_argument(
        "--no-restore-cwd",
        action="store_true",
        default=False,
        help="Don't cd into a resumed session's recorded working directory.",
    )
    parser.add_argument(
        "--in",
        dest="in_dir",
        metavar="DIR",
        default=None,
        help=(
            "Change into DIR before starting or resuming. Combined with "
            "'--resume latest' or -c, the most recent session for DIR's "
            "workspace is picked, and the session stays in DIR (skips the "
            "recorded-cwd restore)."
        ),
    )
    parser.add_argument(
        "--continue",
        "-c",
        dest="continue_last",
        nargs="?",
        const=True,
        default=None,
        metavar="SESSION_NAME",
        help="Resume a session by name, or the most recent if no name given",
    )
    parser.add_argument(
        "--worktree",
        "-w",
        action="store_true",
        default=False,
        help="Run in an isolated git worktree (for parallel agents)",
    )
    _inherited_flag(
        parser,
        "--accept-hooks",
        action="store_true",
        default=False,
        help=(
            "Auto-approve any unseen shell hooks declared in config.yaml "
            "without a TTY prompt.  Equivalent to EV0_ACCEPT_HOOKS=1 or "
            "hooks_auto_accept: true in config.yaml.  Use on CI / headless "
            "runs that can't prompt."
        ),
    )
    _inherited_flag(
        parser,
        "--skills",
        "-s",
        action="append",
        default=None,
        help="Preload one or more skills for the session (repeat flag or comma-separate)",
    )
    _inherited_flag(
        parser,
        "--yolo",
        action="store_true",
        default=False,
        help="Bypass all dangerous command approval prompts (use at your own risk)",
    )
    _inherited_flag(
        parser,
        "--pass-session-id",
        action="store_true",
        default=False,
        help="Include the session ID in the agent's system prompt",
    )
    _inherited_flag(
        parser,
        "--ignore-user-config",
        action="store_true",
        default=False,
        help="Ignore ~/.3V0/config.yaml and fall back to built-in defaults (credentials in .env are still loaded)",
    )
    _inherited_flag(
        parser,
        "--ignore-rules",
        action="store_true",
        default=False,
        help="Skip auto-injection of AGENTS.md, SOUL.md, .cursorrules, memory, and preloaded skills",
    )
    _inherited_flag(
        parser,
        "--safe-mode",
        action="store_true",
        default=False,
        help="Troubleshooting mode: disable ALL customizations — user config, AGENTS.md/memory injection, plugins, and MCP servers (implies --ignore-user-config and --ignore-rules)",
    )
    _inherited_flag(
        parser,
        "--tui",
        action="store_true",
        default=False,
        help="Launch the modern TUI instead of the classic REPL",
    )
    _inherited_flag(
        parser,
        "--cli",
        action="store_true",
        default=False,
        help="Force the classic prompt_toolkit REPL (overrides display.interface=tui)",
    )
    _inherited_flag(
        parser,
        "--dev",
        dest="tui_dev",
        action="store_true",
        default=False,
        help="With --tui: run TypeScript sources via tsx (skip dist build)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # =========================================================================
    # chat command
    # =========================================================================
    chat_parser = subparsers.add_parser(
        "chat",
        help="Interactive chat with the agent",
        description="Start an interactive chat session with 3V0 Agent",
    )
    chat_parser.add_argument(
        "-q", "--query", help="Single query (non-interactive mode)"
    )
    chat_parser.add_argument(
        "--image", help="Optional local image path to attach to a single query"
    )
    # `default=argparse.SUPPRESS` on flags that are ALSO declared on the
    # top-level parser: when the user writes `3v0 -m foo chat`, argparse
    # first sets `args.model = "foo"` from the top-level parser, then
    # dispatches to the chat subparser. Without SUPPRESS the chat subparser's
    # own default (`None`) would silently clobber the top-level value because
    # the subparser shares the same namespace and `dest`. SUPPRESS keeps the
    # subparser action a no-op unless the user actually passes the flag after
    # the subcommand. Matches the pattern already used for `-s/--skills` and
    # the relaunch-inherited flags `-r/--resume`, `-c/--continue`,
    # `-w/--worktree`, `--yolo`, etc. (see tests/threev0_cli/
    # test_argparse_flag_propagation.py).
    _inherited_flag(
        chat_parser,
        "-m", "--model",
        default=argparse.SUPPRESS,
        help="Model to use (e.g., anthropic/claude-sonnet-4)",
    )
    chat_parser.add_argument(
        "-t", "--toolsets",
        default=argparse.SUPPRESS,
        help="Comma-separated toolsets to enable",
    )
    _inherited_flag(
        chat_parser,
        "--reasoning",
        default=argparse.SUPPRESS,
        metavar="LEVEL",
        help=(
            "Reasoning effort for this session: none, minimal, low, medium, "
            "high, xhigh, max, or ultra. Overrides agent.reasoning_effort for "
            "this run only (same levels as the /reasoning slash command)."
        ),
    )
    _inherited_flag(
        chat_parser,
        "-s",
        "--skills",
        action="append",
        default=argparse.SUPPRESS,
        help="Preload one or more skills for the session (repeat flag or comma-separate)",
    )
    _inherited_flag(
        chat_parser,
        "--provider",
        # No `choices=` here: user-defined providers from config.yaml `providers:`
        # are also valid values, and runtime resolution (resolve_runtime_provider)
        # handles validation/error reporting consistently with the top-level
        # `--provider` flag.
        default=argparse.SUPPRESS,
        help="Inference provider (default: auto). Built-in or a user-defined name from `providers:` in config.yaml.",
    )
    chat_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Verbose output",
    )
    chat_parser.add_argument(
        "-Q",
        "--quiet",
        action="store_true",
        help="Quiet mode for programmatic use: suppress banner, spinner, and tool previews. Only output the final response and session info.",
    )
    chat_parser.add_argument(
        "--resume",
        "-r",
        metavar="SESSION_ID",
        default=argparse.SUPPRESS,
        help=(
            "Resume a previous session by ID (shown on exit), or 'latest' "
            "for the most recent session"
        ),
    )
    chat_parser.add_argument(
        "--no-restore-cwd",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Don't cd into a resumed session's recorded working directory.",
    )
    chat_parser.add_argument(
        "--in",
        dest="in_dir",
        metavar="DIR",
        default=argparse.SUPPRESS,
        help=(
            "Change into DIR before starting or resuming (scopes "
            "'--resume latest' / -c lookups to DIR's workspace)."
        ),
    )
    chat_parser.add_argument(
        "--continue",
        "-c",
        dest="continue_last",
        nargs="?",
        const=True,
        default=argparse.SUPPRESS,
        metavar="SESSION_NAME",
        help="Resume a session by name, or the most recent if no name given",
    )
    chat_parser.add_argument(
        "--create-if-missing",
        action="store_true",
        default=argparse.SUPPRESS,
        help=(
            "With -c/--continue <name>: if no session matches the name, "
            "create a new session with that title and proceed (instead of "
            "failing with a not-found error). Programmatic callers that "
            "want 'send to this named thread, making it if needed'."
        ),
    )
    chat_parser.add_argument(
        "--worktree",
        "-w",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Run in an isolated git worktree (for parallel agents on the same repo)",
    )
    _inherited_flag(
        chat_parser,
        "--accept-hooks",
        action="store_true",
        default=argparse.SUPPRESS,
        help=(
            "Auto-approve any unseen shell hooks declared in config.yaml "
            "without a TTY prompt (see also EV0_ACCEPT_HOOKS env var and "
            "hooks_auto_accept: in config.yaml)."
        ),
    )
    chat_parser.add_argument(
        "--checkpoints",
        action="store_true",
        default=False,
        help="Enable filesystem checkpoints before destructive file operations (use /rollback to restore)",
    )
    chat_parser.add_argument(
        "--max-turns",
        type=int,
        default=None,
        metavar="N",
        help="Maximum tool-calling iterations per conversation turn (default: 500, or agent.max_turns in config)",
    )
    _inherited_flag(
        chat_parser,
        "--yolo",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Bypass all dangerous command approval prompts (use at your own risk)",
    )
    _inherited_flag(
        chat_parser,
        "--pass-session-id",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Include the session ID in the agent's system prompt",
    )
    _inherited_flag(
        chat_parser,
        "--ignore-user-config",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Ignore ~/.3V0/config.yaml and fall back to built-in defaults (credentials in .env are still loaded). Useful for isolated CI runs, reproduction, and third-party integrations.",
    )
    _inherited_flag(
        chat_parser,
        "--ignore-rules",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Skip auto-injection of AGENTS.md, SOUL.md, .cursorrules, memory, and preloaded skills. Combine with --ignore-user-config for a fully isolated run.",
    )
    _inherited_flag(
        chat_parser,
        "--safe-mode",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Troubleshooting mode: disable ALL customizations — user config, AGENTS.md/memory injection, plugins, and MCP servers (implies --ignore-user-config and --ignore-rules). Use to isolate whether a problem comes from your setup or from 3V0 itself.",
    )
    chat_parser.add_argument(
        "--source",
        default=None,
        help="Session source tag for filtering (default: cli). Use 'tool' for third-party integrations that should not appear in user session lists.",
    )
    _inherited_flag(
        chat_parser,
        "--tui",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Launch the modern TUI instead of the classic REPL",
    )
    _inherited_flag(
        chat_parser,
        "--cli",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Force the classic prompt_toolkit REPL (overrides display.interface=tui)",
    )
    _inherited_flag(
        chat_parser,
        "--dev",
        dest="tui_dev",
        action="store_true",
        default=argparse.SUPPRESS,
        help="With --tui: run TypeScript sources via tsx (skip dist build)",
    )

    return parser, subparsers, chat_parser
