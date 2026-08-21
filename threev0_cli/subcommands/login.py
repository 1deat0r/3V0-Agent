"""``3v0 login`` subcommand parser.

Extracted verbatim from ``threev0_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_login_parser(subparsers, *, cmd_login: Callable) -> None:
    """Attach the deprecated ``login`` subcommand to ``subparsers``.

    ``3v0 login`` was removed in favor of ``3v0 auth`` / ``3v0 model``
    (the runtime handler in ``threev0_cli/auth.py::login_command`` just prints a
    deprecation message and exits).  The subparser is kept registered so that
    old scripts/aliases invoking ``3v0 login [--flags]`` still receive the
    actionable deprecation message rather than an argparse ``invalid choice:
    'login'`` error — but:

    - The subparser is registered WITHOUT a ``help=`` kwarg so the row is
      omitted from ``3v0 --help`` (argparse only lists subcommands that
      have a help string).  This hides a command that no longer works (#24756)
      without the ``help=argparse.SUPPRESS`` ``==SUPPRESS==`` leak that
      argparse emits for a top-level subparser on Python 3.12+.
    - ``--provider`` accepts ANY value (no ``choices=``) so that, e.g.,
      ``3v0 login --provider anthropic`` reaches the deprecation handler and
      gets pointed at ``3v0 model`` instead of crashing in argparse with
      ``invalid choice: 'anthropic'`` before the handler can run.
    """
    login_parser = subparsers.add_parser(
        "login",
        description=(
            "Deprecated. Use `3v0 auth` to manage credentials, "
            "`3v0 model` to select a provider, or `3v0 setup` for full setup."
        ),
    )
    # No ``choices=`` on purpose — the handler is a deprecation notice that
    # ignores the value, and a restrictive list would reject providers the user
    # legitimately wants (e.g. ``anthropic``) with an argparse error before the
    # friendly redirect message is ever printed.
    login_parser.add_argument(
        "--provider",
        default=None,
        help="(deprecated) Provider name; ignored — see `3v0 model`",
    )
    login_parser.add_argument(
        "--portal-url", help="Portal base URL (default: production portal)"
    )
    login_parser.add_argument(
        "--inference-url",
        help="Inference API base URL (default: production inference API)",
    )
    login_parser.add_argument(
        "--client-id", default=None, help="OAuth client id to use (default: 3v0-cli)"
    )
    login_parser.add_argument("--scope", default=None, help="OAuth scope to request")
    login_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not attempt to open the browser automatically",
    )
    login_parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="HTTP request timeout in seconds (default: 15)",
    )
    login_parser.add_argument(
        "--ca-bundle", help="Path to CA bundle PEM file for TLS verification"
    )
    login_parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS verification (testing only)",
    )
    login_parser.set_defaults(func=cmd_login)
