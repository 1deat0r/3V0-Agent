"""Native gateway serve entrypoint — the (future, deliberate) cutover.

NEVER auto-starts: serve() only runs under THREEV0_SERVE=1. An accidental
`python -m native.run` must not start a second getUpdates poller on the live
bot while the 3V0 gateway polls it — two pollers steal each update.
See 3v0/CUTOVER.md for the sequencing and rollback.
"""
from __future__ import annotations

import os

from . import engine


def serve(long_poll: int = 25, idle: float = 1.0) -> None:
    engine.server(long_poll=long_poll, idle=idle)


if __name__ == "__main__":
    if os.environ.get("THREEV0_SERVE") == "1":
        serve()
    else:
        print(
            "native gateway: set THREEV0_SERVE=1 to serve (cutover only; "
            "see 3v0/CUTOVER.md). Refusing to auto-start a second poller."
        )
