# HTTP Cache-Control response directives

Semantics follow RFC 9111 / MDN.

## no-store
(a) **Meaning:** the response must **not be stored at all** by any cache — neither in shared caches nor in the browser's private cache heuristic. No copy may be kept for reuse.
(b) **Example:** a server returning a one-time payment token or a banking balance would send `Cache-Control: no-store` so the sensitive payload is never persisted by an intermediary or local cache.

## no-cache
(a) **Meaning:** the response **may be stored**, but before serving a stored copy it **must be revalidated with the origin server** (a conditional request like `If-None-Match`/`If-Modified-Since`). It does not forbid storing — it forces a freshness check on each reuse.
(b) **Example:** a server serving a frequently-refreshed API resource (e.g., current stock level) sends `Cache-Control: no-cache` so caches keep it but always confirm with origin before reuse.

## max-age
(a) **Meaning:** the number of seconds a cache may reuse a **fresh** copy of the response without revalidating. It governs the freshness lifetime of a stored response.
(b) **Example:** a server serving a stable image or JSON endpoint sends `Cache-Control: max-age=3600` so caches can serve the response for up to an hour from when it was fetched, with no origin round-trip.

## private
(a) **Meaning:** the response is specific to a **single user and must be stored only in that user's private (non-shared) cache** (e.g., the browser), not in shared/proxy caches shared across users.
(b) **Example:** a personalized dashboard response sends `Cache-Control: private` so a shared CDN must not cache user-specific data, while the user's own browser may.

## public
(a) **Meaning:** the response **may be stored by shared caches** (CDNs, proxies) as well as private ones.
(b) **Example:** a server serving an identical promo page to all visitors sends `Cache-Control: public, max-age=86400` so edge caches can hold and serve it to anyone.

## The two questions
1. **Difference between no-store and no-cache:** `no-store` **forbids storing** the response in any cache at all; `no-cache` **permits storing** but requires **revalidation with the origin before each reuse**. Storage is prohibited vs. storage allowed-but-must-revalidate.
2. **What max-age governs / for whom:** max-age governs how long (in seconds) a cache **may reuse a stored copy without revalidating** — the freshness lifetime. It applies to caches that hold a stored copy (shared or private) reusing it as fresh within that window, after which the copy must be revalidated.
