"""Bounded retry w/ exponential backoff for external provider calls.

Some providers (incl. bitdeer) surface throttling / transient
unavailability as 403 or 5xx. retry_call backs off with increasing waits
(base, base*factor, ... up to cap + jitter) on retryable statuses, so a
transient block self-heals instead of failing the call. Hard auth (401) and
other non-retryable 4xx raise immediately.

Disposition (ticket #17): this stays a NATIVE-substrate module — stdlib
only, no ``agent/`` imports by design (the native runtime is deliberately
independent of the agent tree). It is NOT a duplicate of
``agent/retry_utils.py``; that module owns retry policy for the agent/gateway
surfaces, this owns it for the native engine (consumer:
``3v0/core/semantic.py``).
"""
from __future__ import annotations

import random
import time


class ProviderError(Exception):
    def __init__(self, code: int, message: str, *, retryable: bool):
        super().__init__(message)
        self.code = code
        self.retryable = retryable


def _status_retryable(code: int) -> bool:
    # 408/409/425/429 and 5xx are classic transient; 403 MAY be provider-side
    # throttling (bitdeer), so it is retried too under the cap.
    return code in (403, 408, 409, 425, 429) or 500 <= code <= 599


def retry_call(fn, *, attempts: int = 6, base: float = 1.0, factor: float = 2.0,
               cap: float = 30.0, jitter: float = 0.25, status_retryable=None,
               on_retry=None):
    """Call ``fn`` retrying transient failures with increasing waits.

    ``fn`` must raise ProviderError on HTTP/transport failure. Retries with
    wait = min(cap, base*factor**attempt) + jitter (jitter=0 disables). Returns
    the first success; re-raises the last error when all attempts fail.
    """
    ok = status_retryable or _status_retryable
    delay = base
    last = None
    for attempt in range(attempts):
        try:
            return fn()
        except ProviderError as e:
            last = e
            if not ok(e.code):
                raise
            if attempt == attempts - 1:
                break
            wait = min(cap, delay * (factor ** attempt))
            if jitter:
                wait += random.uniform(0.0, jitter * delay)
            if on_retry:
                on_retry(attempt + 1, e.code, wait)
            time.sleep(wait)
    raise last  # type: ignore[misc]