# Provider registries share one generic primitive; secret_sources is excluded

The browser, web-search, and image-gen provider registries hand-copied the
same registration/locking/snapshot machinery and drifted (web-search grew a
capability concept the others lacked). We extracted the mechanical core into
`agent/provider_registry.ProviderRegistry` — a generic, typed-per-family,
thread-safe registry — and the three now delegate to it, keeping only their
resolution policy. Scope semantics are preserved exactly: lookups default to
the canonical home key, snapshots/restores use the literal scope, and the
generation counter bumps monotonically (including on reset).

The `secret_sources/registry.py` module was deliberately NOT migrated: it is
an apply orchestrator whose insertion order *is* its apply precedence, with
origin tracking, a builtins gate, and provenance records — a different animal
that happens to share the "registry" name. Forcing it onto the generic would
erase those semantics for the sake of symmetry.