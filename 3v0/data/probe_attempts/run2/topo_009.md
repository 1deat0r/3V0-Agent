# Build ordering (probe009)

**(1) A valid topological order of the buildable modules** (each module appears after all its dependencies):

`m_core → m_util → m_log → m_net → m_store → m_auth → m_api → m_ui`

- `m_core`, `m_util`: no dependencies (any position).
- `m_log` depends only on `m_core` → after it.
- `m_net` depends only on `m_log` → after it.
- `m_store` depends only on `m_net` → after it.
- `m_auth` depends only on `m_core` → after it.
- `m_api` depends only on `m_auth` → after it.
- `m_ui` depends on both `m_core` and `m_api` → after both (it is last in this order).

Every module is present exactly once and all dependencies precede it, so this is a valid compile order.

**(2) Modules that cannot be ordered — circular dependency:**

`m_a` and `m_b`. `m_a` depends on `m_b`, while `m_b` depends on `m_a` — a 2-node cycle. Neither can be compiled first, so neither can be placed in any valid topological order.
