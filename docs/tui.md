# TUI — theme, boot, and repaint architecture

The Ink-based terminal UI (`ui-tui/`) draws the 3V0 conversation surface. This
doc records the parts that are easy to get wrong: how the theme resolves and
caches, what repaints when, and the startup-flash lineage.

## Theme resolution (flash-free boot)

The theme starts from the **boot cache** so a stable setup renders correctly
from paint one, then the gateway's skin confirms/overrides it:

1. **Boot seed** (`lib/themeBoot.ts`) — `readBootTheme()` reads
   `$EV0_HOME/tui-theme-boot.json` (last session's resolved Theme) at module
   import. `uiStore` seeds `theme: bootTheme ?? DEFAULT_THEME`. `DEFAULT_THEME`
   is gold/3V0 and only appears on a true first launch.
2. **Live skin** (`app/createGatewayEventHandler.ts`) — the gateway sends
   `skin.changed` ~instantly at connect. `themeForSkin()` re-derives the Theme
   LIVE from the skin + ambient signals (OSC-11 background probe, `EV0_TUI_*`,
   polarity): `fromSkin()` (`theme.ts`) builds the palette
   deterministically but environment-dependently.
3. **Commit** — `commitTheme(theme)` patches `$uiState` and (only on a real
   change) issues a deferred full `forceRedraw` to avoid palette tearing.

### The repaint trap

`fromSkin` re-derives secondary tones (muted/label/status) against the live
background, so two commits of the same skin differ in SOME derived byte on
every launch. A byte-for-byte `themesEqual` therefore made the anti-tearing
`forceRedraw` fire every start even with matching branding.

`themesEqual` compares the **identity core** now: background/surface,
text/primary/accent/border, status tones, brand identity, and explicit
light↔dark polarity. A genuine switch (skin change, polarity flip, palette
swap) still trips it; environment-driven drift on an unchanged theme does not.

## Startup flash lineage (resolved + open)

A "flash before my theme" has, in order:

- **Hermes/Ares brand** (resolved): the default `LOGO_ART` was "HERMES AGENT";
  the `ares` skin was Ares-branded. Both are now 3V0 (commit `3fd2d570a6`).
- **Resume repaint** (resolved): `sessionResumeView` force-redrew at scroll
  delay 0, racing the resumed transcript's first render. The 0ms tick now
  scrolls without force-redraw (commit `ece5c8b969`).
- **Theme re-derivation repaint** (resolved): `themesEqual` above
  (commit `82c39553f5`).
- **First-frame status fragment** (`…` + inverted glyph + start of a word,
  e.g. `…T r` captured in a PTY) **— OPEN.** A bare status/verb line still
  paints in the very first Ink frame before the full layout + skin. The exact
  source string is `Tr…` (word truncated at the boot frame's width) and has
  NOT yet been isolated. Candidate: a pre-session status rendered outside the
  chrome; the `◈ ui.status` line was removed but the fragment persists.
  To pinpoint: capture the first frame's full word (`…T r` -> what word?).

## Anti-tearing forceRedraw

The full clear+repaint on a REAL theme swap is load-bearing: the renderer's
diff/blit cache treats layout-unchanged regions as reusable, so incremental
repaints after a palette change tear (stale cells keep the old palette). The
deferred `forceRedraw` (a `setTimeout` after the recolored tree flushes)
guarantees a coherent frame. Skipping it when `themesEqual` is true keeps the
no-op boot path paint-free.

## Upstream `@3v0/shared`

Upstream never shipped `apps/shared` in this body; the TUI imports
`@3v0/shared/{billing,skin,charge-settlement}`. It is vendored under
`apps/shared/` (commit `7a8dfa276e`, completed `930e2877d0`) and must stay in
sync with what `ui-tui/` reads. `npm run check --workspace=ui-tui` enforces
typecheck + tests + lint.