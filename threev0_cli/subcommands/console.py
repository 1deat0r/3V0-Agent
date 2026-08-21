"""``3v0 console`` subcommand parser."""

from __future__ import annotations

from typing import Callable


def build_console_parser(subparsers, *, cmd_console: Callable) -> None:
    """Attach the safe 3V0 Console REPL subcommand."""
    console_parser = subparsers.add_parser(
        "console",
        help="Open the safe 3V0 command console",
        description=(
            "Open a curated 3V0 command REPL. This is not a raw shell and "
            "does not expose the full 3V0 CLI."
        ),
    )
    console_parser.set_defaults(func=cmd_console)
