# ui-tui/ — Ink terminal UI

Ink (React) terminal UI — `hermes --tui`. TypeScript owns the screen; `tui_gateway` (Python) owns sessions/tools. The dashboard embeds the real TUI through a PTY — never re-implement it in React.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `ui-tui/.gitignore` | asset | File `.gitignore` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `ui-tui/eslint.config.mjs` | asset | File `eslint.config.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/package.json` | build | Node package manifest | Declares JS workspace deps + scripts |  |
| `ui-tui/packages/hermes-ink/ambient.d.ts` | frontend-ts | TypeScript module `ambient.d.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/index.d.ts` | frontend-ts | TypeScript module `index.d.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/index.js` | asset | File `index.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/packages/hermes-ink/package.json` | build | Node package manifest | Declares JS workspace deps + scripts |  |
| `ui-tui/packages/hermes-ink/src/bootstrap/state.ts` | frontend-ts | TypeScript module `state.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/entry-exports.ts` | frontend-ts | TypeScript module `entry-exports.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/hooks/use-stderr.ts` | frontend-ts | TypeScript module `use-stderr.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/hooks/use-stdout.ts` | frontend-ts | TypeScript module `use-stdout.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/Ansi.tsx` | frontend-tsx | React component `Ansi.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/absolute-in-zero-height-box.test.tsx` | frontend-tsx | React component `absolute-in-zero-height-box.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/app-mouse-watchdog.test.ts` | frontend-ts | TypeScript module `app-mouse-watchdog.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/app-mouse.test.ts` | frontend-ts | TypeScript module `app-mouse.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/app-rawmode-mouse.test.ts` | frontend-ts | TypeScript module `app-rawmode-mouse.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/app-stdin-recovery.test.ts` | frontend-ts | TypeScript module `app-stdin-recovery.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/bidi.ts` | frontend-ts | TypeScript module `bidi.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/cache-eviction.ts` | frontend-ts | TypeScript module `cache-eviction.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/clearTerminal.ts` | frontend-ts | TypeScript module `clearTerminal.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/colorize.test.ts` | frontend-ts | TypeScript module `colorize.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/colorize.ts` | frontend-ts | TypeScript module `colorize.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/AlternateScreen.tsx` | frontend-tsx | React component `AlternateScreen.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/App.focus.test.tsx` | frontend-tsx | React component `App.focus.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/App.tsx` | frontend-tsx | React component `App.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/AppContext.ts` | frontend-ts | TypeScript module `AppContext.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/Box.tsx` | frontend-tsx | React component `Box.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/Button.tsx` | frontend-tsx | React component `Button.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/ClockContext.tsx` | frontend-tsx | React component `ClockContext.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/CursorAdvanceContext.ts` | frontend-ts | TypeScript module `CursorAdvanceContext.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/CursorDeclarationContext.ts` | frontend-ts | TypeScript module `CursorDeclarationContext.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/ErrorOverview.tsx` | frontend-tsx | React component `ErrorOverview.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/Link.tsx` | frontend-tsx | React component `Link.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/Newline.tsx` | frontend-tsx | React component `Newline.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/NoSelect.tsx` | frontend-tsx | React component `NoSelect.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/RawAnsi.tsx` | frontend-tsx | React component `RawAnsi.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/ScrollBox.tsx` | frontend-tsx | React component `ScrollBox.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/Spacer.tsx` | frontend-tsx | React component `Spacer.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/StdinContext.ts` | frontend-ts | TypeScript module `StdinContext.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/TerminalFocusContext.tsx` | frontend-tsx | React component `TerminalFocusContext.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/TerminalSizeContext.tsx` | frontend-tsx | React component `TerminalSizeContext.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/Text.test.ts` | frontend-ts | TypeScript module `Text.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/components/Text.tsx` | frontend-tsx | React component `Text.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/constants.ts` | frontend-ts | TypeScript module `constants.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/cursor.ts` | frontend-ts | TypeScript module `cursor.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/devtools.ts` | frontend-ts | TypeScript module `devtools.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/dom.ts` | frontend-ts | TypeScript module `dom.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/click-event.ts` | frontend-ts | TypeScript module `click-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/cmd-shortcuts.test.ts` | frontend-ts | TypeScript module `cmd-shortcuts.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/dispatcher.ts` | frontend-ts | TypeScript module `dispatcher.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/emitter.ts` | frontend-ts | TypeScript module `emitter.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/event-handlers.ts` | frontend-ts | TypeScript module `event-handlers.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/event.ts` | frontend-ts | TypeScript module `event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/focus-event.ts` | frontend-ts | TypeScript module `focus-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/input-event.ts` | frontend-ts | TypeScript module `input-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/keyboard-event.ts` | frontend-ts | TypeScript module `keyboard-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/mouse-event.ts` | frontend-ts | TypeScript module `mouse-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/paste-event.ts` | frontend-ts | TypeScript module `paste-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/resize-event.ts` | frontend-ts | TypeScript module `resize-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/terminal-event.ts` | frontend-ts | TypeScript module `terminal-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/events/terminal-focus-event.ts` | frontend-ts | TypeScript module `terminal-focus-event.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/focus.ts` | frontend-ts | TypeScript module `focus.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/frame.ts` | frontend-ts | TypeScript module `frame.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/get-max-width.ts` | frontend-ts | TypeScript module `get-max-width.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/global.d.ts` | frontend-ts | TypeScript module `global.d.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hit-test.test.ts` | frontend-ts | TypeScript module `hit-test.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hit-test.ts` | frontend-ts | TypeScript module `hit-test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-animation-frame.ts` | frontend-ts | TypeScript module `use-animation-frame.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-app.ts` | frontend-ts | TypeScript module `use-app.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-cursor-advance.ts` | frontend-ts | TypeScript module `use-cursor-advance.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-declared-cursor.ts` | frontend-ts | TypeScript module `use-declared-cursor.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-external-process.ts` | frontend-ts | TypeScript module `use-external-process.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-input.ts` | frontend-ts | TypeScript module `use-input.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-interval.ts` | frontend-ts | TypeScript module `use-interval.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-search-highlight.ts` | frontend-ts | TypeScript module `use-search-highlight.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-selection.ts` | frontend-ts | TypeScript module `use-selection.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-stdin.ts` | frontend-ts | TypeScript module `use-stdin.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-tab-status.ts` | frontend-ts | TypeScript module `use-tab-status.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-terminal-focus.ts` | frontend-ts | TypeScript module `use-terminal-focus.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-terminal-title.ts` | frontend-ts | TypeScript module `use-terminal-title.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hooks/use-terminal-viewport.ts` | frontend-ts | TypeScript module `use-terminal-viewport.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/hyperlinkHover.ts` | frontend-ts | TypeScript module `hyperlinkHover.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/ink-backpressure.test.ts` | frontend-ts | TypeScript module `ink-backpressure.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/ink-cursor-advance.test.ts` | frontend-ts | TypeScript module `ink-cursor-advance.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/ink-resize.test.ts` | frontend-ts | TypeScript module `ink-resize.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/ink.tsx` | frontend-tsx | React component `ink.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/packages/hermes-ink/src/ink/instances.ts` | frontend-ts | TypeScript module `instances.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/layout/engine.ts` | frontend-ts | TypeScript module `engine.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/layout/geometry.ts` | frontend-ts | TypeScript module `geometry.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/layout/node.ts` | frontend-ts | TypeScript module `node.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/layout/yoga.ts` | frontend-ts | TypeScript module `yoga.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/line-width-cache.ts` | frontend-ts | TypeScript module `line-width-cache.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/log-update.test.ts` | frontend-ts | TypeScript module `log-update.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/log-update.ts` | frontend-ts | TypeScript module `log-update.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/lru.ts` | frontend-ts | TypeScript module `lru.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/measure-element.ts` | frontend-ts | TypeScript module `measure-element.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/measure-text.ts` | frontend-ts | TypeScript module `measure-text.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/node-cache.ts` | frontend-ts | TypeScript module `node-cache.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/optimizer.ts` | frontend-ts | TypeScript module `optimizer.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/osc-response-chain.test.ts` | frontend-ts | TypeScript module `osc-response-chain.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/output.ts` | frontend-ts | TypeScript module `output.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/parse-keypress-drop-probe.test.ts` | frontend-ts | TypeScript module `parse-keypress-drop-probe.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/parse-keypress-noregress.test.ts` | frontend-ts | TypeScript module `parse-keypress-noregress.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/parse-keypress.test.ts` | frontend-ts | TypeScript module `parse-keypress.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/parse-keypress.ts` | frontend-ts | TypeScript module `parse-keypress.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/reconciler.ts` | frontend-ts | TypeScript module `reconciler.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/render-border.test.ts` | frontend-ts | TypeScript module `render-border.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/render-border.ts` | frontend-ts | TypeScript module `render-border.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/render-node-to-output.ts` | frontend-ts | TypeScript module `render-node-to-output.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/render-to-screen.ts` | frontend-ts | TypeScript module `render-to-screen.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/renderer.ts` | frontend-ts | TypeScript module `renderer.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/root.ts` | frontend-ts | TypeScript module `root.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/screen.ts` | frontend-ts | TypeScript module `screen.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/searchHighlight.ts` | frontend-ts | TypeScript module `searchHighlight.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/selection.test.ts` | frontend-ts | TypeScript module `selection.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/selection.ts` | frontend-ts | TypeScript module `selection.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/squash-text-nodes.ts` | frontend-ts | TypeScript module `squash-text-nodes.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/stringWidth.ts` | frontend-ts | TypeScript module `stringWidth.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/styles.ts` | frontend-ts | TypeScript module `styles.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/supports-hyperlinks.ts` | frontend-ts | TypeScript module `supports-hyperlinks.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/tabstops.ts` | frontend-ts | TypeScript module `tabstops.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/terminal-background.test.ts` | frontend-ts | TypeScript module `terminal-background.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/terminal-focus-state.ts` | frontend-ts | TypeScript module `terminal-focus-state.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/terminal-querier.ts` | frontend-ts | TypeScript module `terminal-querier.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/terminal.test.ts` | frontend-ts | TypeScript module `terminal.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/terminal.ts` | frontend-ts | TypeScript module `terminal.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio.ts` | frontend-ts | TypeScript module `termio.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/ansi.ts` | frontend-ts | TypeScript module `ansi.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/csi.ts` | frontend-ts | TypeScript module `csi.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/dec.ts` | frontend-ts | TypeScript module `dec.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/esc.ts` | frontend-ts | TypeScript module `esc.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/osc.test.ts` | frontend-ts | TypeScript module `osc.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/osc.ts` | frontend-ts | TypeScript module `osc.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/parser.test.ts` | frontend-ts | TypeScript module `parser.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/parser.ts` | frontend-ts | TypeScript module `parser.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/sgr.ts` | frontend-ts | TypeScript module `sgr.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/tokenize.test.ts` | frontend-ts | TypeScript module `tokenize.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/tokenize.ts` | frontend-ts | TypeScript module `tokenize.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/termio/types.ts` | frontend-ts | TypeScript module `types.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/useTerminalNotification.ts` | frontend-ts | TypeScript module `useTerminalNotification.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/warn.ts` | frontend-ts | TypeScript module `warn.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/widest-line.ts` | frontend-ts | TypeScript module `widest-line.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/wrap-text.test.ts` | frontend-ts | TypeScript module `wrap-text.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/wrap-text.ts` | frontend-ts | TypeScript module `wrap-text.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/ink/wrapAnsi.ts` | frontend-ts | TypeScript module `wrapAnsi.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/native-ts/yoga-layout/enums.ts` | frontend-ts | TypeScript module `enums.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/native-ts/yoga-layout/index.ts` | frontend-ts | TypeScript module `index.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/debug.ts` | frontend-ts | TypeScript module `debug.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/earlyInput.ts` | frontend-ts | TypeScript module `earlyInput.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/env.ts` | frontend-ts | TypeScript module `env.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/envUtils.ts` | frontend-ts | TypeScript module `envUtils.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/execFileNoThrow.test.ts` | frontend-ts | TypeScript module `execFileNoThrow.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/execFileNoThrow.ts` | frontend-ts | TypeScript module `execFileNoThrow.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/fullscreen.ts` | frontend-ts | TypeScript module `fullscreen.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/intl.ts` | frontend-ts | TypeScript module `intl.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/log.ts` | frontend-ts | TypeScript module `log.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/semver.ts` | frontend-ts | TypeScript module `semver.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/src/utils/sliceAnsi.ts` | frontend-ts | TypeScript module `sliceAnsi.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/text-input.d.ts` | frontend-ts | TypeScript module `text-input.d.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/packages/hermes-ink/text-input.js` | asset | File `text-input.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/packages/hermes-ink/tsconfig.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `ui-tui/scripts/bench-history-scroll.tsx` | frontend-tsx | React component `bench-history-scroll.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/scripts/bench-streaming-md.tsx` | frontend-tsx | React component `bench-streaming-md.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/scripts/billing-fixtures.tsx` | frontend-tsx | React component `billing-fixtures.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/scripts/build.mjs` | asset | File `build.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/scripts/profile-tui.mjs` | asset | File `profile-tui.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/scripts/visual/paths.mjs` | asset | File `paths.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/scripts/visual/render.tsx` | frontend-tsx | React component `render.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/scripts/visual/run.mjs` | asset | File `run.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/scripts/visual/shot.mjs` | asset | File `shot.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `ui-tui/src/__tests__/activeSessionSwitcher.test.ts` | frontend-ts | TypeScript module `activeSessionSwitcher.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/appChromeBlockedTimers.test.tsx` | frontend-tsx | React component `appChromeBlockedTimers.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/appChromeStatusRule.test.tsx` | frontend-tsx | React component `appChromeStatusRule.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/appChromeStatusRuleDevCredits.test.tsx` | frontend-tsx | React component `appChromeStatusRuleDevCredits.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/approvalAction.test.ts` | frontend-ts | TypeScript module `approvalAction.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/asCommandDispatch.test.ts` | frontend-ts | TypeScript module `asCommandDispatch.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/attachments.test.ts` | frontend-ts | TypeScript module `attachments.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/billingStepUp.test.tsx` | frontend-tsx | React component `billingStepUp.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/blockLayout.test.ts` | frontend-ts | TypeScript module `blockLayout.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/brandingMcpCount.test.ts` | frontend-ts | TypeScript module `brandingMcpCount.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/bundleNoAsyncEsmDeadlock.test.ts` | frontend-ts | TypeScript module `bundleNoAsyncEsmDeadlock.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/charts.test.ts` | frontend-ts | TypeScript module `charts.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/clipboard.test.ts` | frontend-ts | TypeScript module `clipboard.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/completionApply.test.ts` | frontend-ts | TypeScript module `completionApply.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/constants.test.ts` | frontend-ts | TypeScript module `constants.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/createGatewayEventHandler.test.ts` | frontend-ts | TypeScript module `createGatewayEventHandler.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/createSlashHandler.test.ts` | frontend-ts | TypeScript module `createSlashHandler.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/cursorDriftRegression.test.ts` | frontend-ts | TypeScript module `cursorDriftRegression.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/details.test.ts` | frontend-ts | TypeScript module `details.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/emoji.test.ts` | frontend-ts | TypeScript module `emoji.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/externalLink.test.ts` | frontend-ts | TypeScript module `externalLink.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/forceTruecolor.test.ts` | frontend-ts | TypeScript module `forceTruecolor.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/gatewayClient.test.ts` | frontend-ts | TypeScript module `gatewayClient.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/gatewayRecovery.test.ts` | frontend-ts | TypeScript module `gatewayRecovery.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/gracefulExit.test.ts` | frontend-ts | TypeScript module `gracefulExit.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/imeVietnameseTelex.test.tsx` | frontend-tsx | React component `imeVietnameseTelex.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/inlineSlashSkill.test.ts` | frontend-ts | TypeScript module `inlineSlashSkill.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/inputSelectionClipboard.test.ts` | frontend-ts | TypeScript module `inputSelectionClipboard.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/journeyCommand.test.ts` | frontend-ts | TypeScript module `journeyCommand.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/loaders.test.ts` | frontend-ts | TypeScript module `loaders.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/markdown.test.ts` | frontend-ts | TypeScript module `markdown.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/mathUnicode.test.ts` | frontend-ts | TypeScript module `mathUnicode.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/memoryMonitor.test.ts` | frontend-ts | TypeScript module `memoryMonitor.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/mergeUsageStable.test.ts` | frontend-ts | TypeScript module `mergeUsageStable.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/messageLine.test.ts` | frontend-ts | TypeScript module `messageLine.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/messages.test.ts` | frontend-ts | TypeScript module `messages.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/moaProgressActivity.test.ts` | frontend-ts | TypeScript module `moaProgressActivity.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/modelPicker.test.ts` | frontend-ts | TypeScript module `modelPicker.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/orchestratorPromptSession.test.ts` | frontend-ts | TypeScript module `orchestratorPromptSession.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/osc52.test.ts` | frontend-ts | TypeScript module `osc52.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/overlayPrimitives.test.ts` | frontend-ts | TypeScript module `overlayPrimitives.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/parentLog.test.ts` | frontend-ts | TypeScript module `parentLog.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/paths.test.ts` | frontend-ts | TypeScript module `paths.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/petPane.test.tsx` | frontend-tsx | React component `petPane.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/petPolling.test.ts` | frontend-ts | TypeScript module `petPolling.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/platform.test.ts` | frontend-ts | TypeScript module `platform.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/precisionWheel.test.ts` | frontend-ts | TypeScript module `precisionWheel.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/prompt.test.ts` | frontend-ts | TypeScript module `prompt.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/providers.test.ts` | frontend-ts | TypeScript module `providers.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/queueSubmission.test.ts` | frontend-ts | TypeScript module `queueSubmission.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/reasoning.test.ts` | frontend-ts | TypeScript module `reasoning.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/rpc.test.ts` | frontend-ts | TypeScript module `rpc.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/scroll.test.ts` | frontend-ts | TypeScript module `scroll.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/scrollBoxRendererBounds.test.ts` | frontend-ts | TypeScript module `scrollBoxRendererBounds.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/slashParity.test.ts` | frontend-ts | TypeScript module `slashParity.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/spawnHistoryStore.test.ts` | frontend-ts | TypeScript module `spawnHistoryStore.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/stateIsolation.test.ts` | frontend-ts | TypeScript module `stateIsolation.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/statusBarTicker.test.ts` | frontend-ts | TypeScript module `statusBarTicker.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/statusRule.test.ts` | frontend-ts | TypeScript module `statusRule.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/streamingMarkdown.test.ts` | frontend-ts | TypeScript module `streamingMarkdown.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/subagentTree.test.ts` | frontend-ts | TypeScript module `subagentTree.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/submissionCore.test.ts` | frontend-ts | TypeScript module `submissionCore.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/subscriptionCommand.test.ts` | frontend-ts | TypeScript module `subscriptionCommand.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/subscriptionOverlay.test.tsx` | frontend-tsx | React component `subscriptionOverlay.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/syntax.test.ts` | frontend-ts | TypeScript module `syntax.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/terminalModes.test.ts` | frontend-ts | TypeScript module `terminalModes.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/terminalParity.test.ts` | frontend-ts | TypeScript module `terminalParity.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/terminalSetup.test.ts` | frontend-ts | TypeScript module `terminalSetup.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/termux.test.ts` | frontend-ts | TypeScript module `termux.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/termuxComposerLayout.test.ts` | frontend-ts | TypeScript module `termuxComposerLayout.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/text.test.ts` | frontend-ts | TypeScript module `text.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputBurstInput.test.ts` | frontend-ts | TypeScript module `textInputBurstInput.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputCursorSourceOfTruth.test.ts` | frontend-ts | TypeScript module `textInputCursorSourceOfTruth.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputCut.test.ts` | frontend-ts | TypeScript module `textInputCut.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputFastEcho.test.ts` | frontend-ts | TypeScript module `textInputFastEcho.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputKillLine.test.ts` | frontend-ts | TypeScript module `textInputKillLine.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputLineKill.test.ts` | frontend-ts | TypeScript module `textInputLineKill.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputLineNav.test.ts` | frontend-ts | TypeScript module `textInputLineNav.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputPassThrough.test.ts` | frontend-ts | TypeScript module `textInputPassThrough.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputReturnAction.test.ts` | frontend-ts | TypeScript module `textInputReturnAction.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputReturnBurst.test.ts` | frontend-ts | TypeScript module `textInputReturnBurst.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputRightClick.test.ts` | frontend-ts | TypeScript module `textInputRightClick.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputSubmitClear.test.tsx` | frontend-tsx | React component `textInputSubmitClear.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/textInputWordDelete.test.ts` | frontend-ts | TypeScript module `textInputWordDelete.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/textInputWrap.test.ts` | frontend-ts | TypeScript module `textInputWrap.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/theme.test.ts` | frontend-ts | TypeScript module `theme.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/themeBoot.test.ts` | frontend-ts | TypeScript module `themeBoot.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/thinkingLiveCollapse.test.tsx` | frontend-tsx | React component `thinkingLiveCollapse.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/thinkingMoaReferenceVisibility.test.tsx` | frontend-tsx | React component `thinkingMoaReferenceVisibility.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/topupCommand.test.ts` | frontend-ts | TypeScript module `topupCommand.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/turnControllerNotice.test.ts` | frontend-ts | TypeScript module `turnControllerNotice.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/turnStore.test.ts` | frontend-ts | TypeScript module `turnStore.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/usageCommand.test.ts` | frontend-ts | TypeScript module `usageCommand.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useBatteryPoll.test.ts` | frontend-ts | TypeScript module `useBatteryPoll.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useCompletion.test.ts` | frontend-ts | TypeScript module `useCompletion.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useComposerState.test.ts` | frontend-ts | TypeScript module `useComposerState.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useConfigSync.test.ts` | frontend-ts | TypeScript module `useConfigSync.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useInputHandlers.test.ts` | frontend-ts | TypeScript module `useInputHandlers.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useQueue.test.ts` | frontend-ts | TypeScript module `useQueue.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useSessionLifecycle.test.ts` | frontend-ts | TypeScript module `useSessionLifecycle.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useSubmission.test.ts` | frontend-ts | TypeScript module `useSubmission.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/useVirtualHistoryHeights.test.ts` | frontend-ts | TypeScript module `useVirtualHistoryHeights.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/userWidgets.test.ts` | frontend-ts | TypeScript module `userWidgets.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/viewport.test.ts` | frontend-ts | TypeScript module `viewport.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/viewportStore.test.ts` | frontend-ts | TypeScript module `viewportStore.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/virtualHeights.test.ts` | frontend-ts | TypeScript module `virtualHeights.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/virtualHistoryClamp.test.ts` | frontend-ts | TypeScript module `virtualHistoryClamp.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/virtualHistoryOffsetCache.test.ts` | frontend-ts | TypeScript module `virtualHistoryOffsetCache.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/voiceSubmitModeRenderer.test.tsx` | frontend-tsx | React component `voiceSubmitModeRenderer.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/wakeCommand.test.ts` | frontend-ts | TypeScript module `wakeCommand.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/weatherApp.test.ts` | frontend-ts | TypeScript module `weatherApp.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/wheelAccel.test.ts` | frontend-ts | TypeScript module `wheelAccel.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/widgetGrid.test.ts` | frontend-ts | TypeScript module `widgetGrid.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/__tests__/widgetGridComponent.test.tsx` | frontend-tsx | React component `widgetGridComponent.test.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/__tests__/widgetSdk.test.ts` | frontend-ts | TypeScript module `widgetSdk.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app.tsx` | frontend-tsx | React component `app.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/app/createGatewayEventHandler.ts` | frontend-ts | TypeScript module `createGatewayEventHandler.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/createSlashHandler.ts` | frontend-ts | TypeScript module `createSlashHandler.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/delegationStore.ts` | frontend-ts | TypeScript module `delegationStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/gatewayContext.tsx` | frontend-tsx | React component `gatewayContext.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/app/gatewayRecovery.ts` | frontend-ts | TypeScript module `gatewayRecovery.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/inputSelectionStore.ts` | frontend-ts | TypeScript module `inputSelectionStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/interfaces.ts` | frontend-ts | TypeScript module `interfaces.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/overlayStore.ts` | frontend-ts | TypeScript module `overlayStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/petFlashStore.ts` | frontend-ts | TypeScript module `petFlashStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/scroll.ts` | frontend-ts | TypeScript module `scroll.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/sessionResumeView.test.ts` | frontend-ts | TypeScript module `sessionResumeView.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/sessionResumeView.ts` | frontend-ts | TypeScript module `sessionResumeView.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/setupHandoff.ts` | frontend-ts | TypeScript module `setupHandoff.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/commands/core.ts` | frontend-ts | TypeScript module `core.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/commands/debug.ts` | frontend-ts | TypeScript module `debug.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/commands/ops.ts` | frontend-ts | TypeScript module `ops.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/commands/session.ts` | frontend-ts | TypeScript module `session.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/commands/setup.ts` | frontend-ts | TypeScript module `setup.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/commands/subscription.ts` | frontend-ts | TypeScript module `subscription.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/commands/topup.ts` | frontend-ts | TypeScript module `topup.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/commands/wake.ts` | frontend-ts | TypeScript module `wake.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/fuzzyScore.test.ts` | frontend-ts | TypeScript module `fuzzyScore.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/fuzzyScore.ts` | frontend-ts | TypeScript module `fuzzyScore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/registry.ts` | frontend-ts | TypeScript module `registry.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/slash/types.ts` | frontend-ts | TypeScript module `types.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/spawnHistoryStore.ts` | frontend-ts | TypeScript module `spawnHistoryStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/submissionCore.ts` | frontend-ts | TypeScript module `submissionCore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/turnController.ts` | frontend-ts | TypeScript module `turnController.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/turnStore.ts` | frontend-ts | TypeScript module `turnStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/uiStore.ts` | frontend-ts | TypeScript module `uiStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/useBatteryPoll.ts` | frontend-ts | TypeScript module `useBatteryPoll.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/useComposerState.ts` | frontend-ts | TypeScript module `useComposerState.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/useConfigSync.ts` | frontend-ts | TypeScript module `useConfigSync.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/useInputHandlers.ts` | frontend-ts | TypeScript module `useInputHandlers.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/useLongRunToolCharms.ts` | frontend-ts | TypeScript module `useLongRunToolCharms.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/useMainApp.ts` | frontend-ts | TypeScript module `useMainApp.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/usePet.ts` | frontend-ts | TypeScript module `usePet.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/useSessionLifecycle.ts` | frontend-ts | TypeScript module `useSessionLifecycle.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/useSubmission.ts` | frontend-ts | TypeScript module `useSubmission.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/app/wakeState.ts` | frontend-ts | TypeScript module `wakeState.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/banner.ts` | frontend-ts | TypeScript module `banner.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/components/accordion.tsx` | frontend-tsx | React component `accordion.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/activeSessionSwitcher.tsx` | frontend-tsx | React component `activeSessionSwitcher.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/agentsOverlay.tsx` | frontend-tsx | React component `agentsOverlay.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/appChrome.tsx` | frontend-tsx | React component `appChrome.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/appLayout.tsx` | frontend-tsx | React component `appLayout.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/appOverlays.tsx` | frontend-tsx | React component `appOverlays.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/billingOverlay.tsx` | frontend-tsx | React component `billingOverlay.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/branding.tsx` | frontend-tsx | React component `branding.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/fpsOverlay.tsx` | frontend-tsx | React component `fpsOverlay.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/gridStreamsDemo.tsx` | frontend-tsx | React component `gridStreamsDemo.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/gridTestOverlay.tsx` | frontend-tsx | React component `gridTestOverlay.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/helpHint.tsx` | frontend-tsx | React component `helpHint.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/journey.tsx` | frontend-tsx | React component `journey.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/loaders.tsx` | frontend-tsx | React component `loaders.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/markdown.tsx` | frontend-tsx | React component `markdown.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/maskedPrompt.tsx` | frontend-tsx | React component `maskedPrompt.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/messageLine.tsx` | frontend-tsx | React component `messageLine.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/modelPicker.tsx` | frontend-tsx | React component `modelPicker.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/overlay.tsx` | frontend-tsx | React component `overlay.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/overlayControls.tsx` | frontend-tsx | React component `overlayControls.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/overlayPrimitives.tsx` | frontend-tsx | React component `overlayPrimitives.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/overlayScrollbar.tsx` | frontend-tsx | React component `overlayScrollbar.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/petPicker.tsx` | frontend-tsx | React component `petPicker.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/petSprite.tsx` | frontend-tsx | React component `petSprite.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/pluginsHub.tsx` | frontend-tsx | React component `pluginsHub.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/prompts.tsx` | frontend-tsx | React component `prompts.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/queuedMessages.tsx` | frontend-tsx | React component `queuedMessages.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/skillsHub.tsx` | frontend-tsx | React component `skillsHub.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/streamingAssistant.tsx` | frontend-tsx | React component `streamingAssistant.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/streamingMarkdown.tsx` | frontend-tsx | React component `streamingMarkdown.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/subscriptionOverlay.tsx` | frontend-tsx | React component `subscriptionOverlay.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/textInput.tsx` | frontend-tsx | React component `textInput.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/themed.tsx` | frontend-tsx | React component `themed.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/thinking.tsx` | frontend-tsx | React component `thinking.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/todoPanel.tsx` | frontend-tsx | React component `todoPanel.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/components/widgetGrid.tsx` | frontend-tsx | React component `widgetGrid.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/config/env.ts` | frontend-ts | TypeScript module `env.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/config/limits.ts` | frontend-ts | TypeScript module `limits.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/config/timing.ts` | frontend-ts | TypeScript module `timing.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/content/charms.ts` | frontend-ts | TypeScript module `charms.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/content/faces.ts` | frontend-ts | TypeScript module `faces.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/content/fortunes.ts` | frontend-ts | TypeScript module `fortunes.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/content/hotkeys.ts` | frontend-ts | TypeScript module `hotkeys.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/content/placeholders.ts` | frontend-ts | TypeScript module `placeholders.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/content/setup.ts` | frontend-ts | TypeScript module `setup.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/content/verbs.ts` | frontend-ts | TypeScript module `verbs.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/attachments.ts` | frontend-ts | TypeScript module `attachments.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/blockLayout.ts` | frontend-ts | TypeScript module `blockLayout.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/details.ts` | frontend-ts | TypeScript module `details.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/messages.ts` | frontend-ts | TypeScript module `messages.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/paths.ts` | frontend-ts | TypeScript module `paths.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/providers.ts` | frontend-ts | TypeScript module `providers.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/roles.ts` | frontend-ts | TypeScript module `roles.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/slash.ts` | frontend-ts | TypeScript module `slash.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/usage.ts` | frontend-ts | TypeScript module `usage.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/domain/viewport.ts` | frontend-ts | TypeScript module `viewport.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/entry.tsx` | frontend-tsx | React component `entry.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/gatewayClient.ts` | frontend-ts | TypeScript module `gatewayClient.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/gatewayTypes.ts` | frontend-ts | TypeScript module `gatewayTypes.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/hooks/useCompletion.ts` | frontend-ts | TypeScript module `useCompletion.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/hooks/useGitBranch.ts` | frontend-ts | TypeScript module `useGitBranch.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/hooks/useInputHistory.ts` | frontend-ts | TypeScript module `useInputHistory.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/hooks/useQueue.ts` | frontend-ts | TypeScript module `useQueue.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/hooks/useVirtualHistory.ts` | frontend-ts | TypeScript module `useVirtualHistory.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/billingDialog.test.ts` | frontend-ts | TypeScript module `billingDialog.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/billingDialog.ts` | frontend-ts | TypeScript module `billingDialog.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/charts.ts` | frontend-ts | TypeScript module `charts.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/circularBuffer.ts` | frontend-ts | TypeScript module `circularBuffer.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/clipboard.ts` | frontend-ts | TypeScript module `clipboard.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/color.test.ts` | frontend-ts | TypeScript module `color.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/color.ts` | frontend-ts | TypeScript module `color.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/editor.test.ts` | frontend-ts | TypeScript module `editor.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/editor.ts` | frontend-ts | TypeScript module `editor.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/emoji.ts` | frontend-ts | TypeScript module `emoji.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/externalCli.ts` | frontend-ts | TypeScript module `externalCli.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/externalLink.ts` | frontend-ts | TypeScript module `externalLink.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/forceTruecolor.ts` | frontend-ts | TypeScript module `forceTruecolor.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/fpsStore.ts` | frontend-ts | TypeScript module `fpsStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/fuzzy.test.ts` | frontend-ts | TypeScript module `fuzzy.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/fuzzy.ts` | frontend-ts | TypeScript module `fuzzy.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/gracefulExit.ts` | frontend-ts | TypeScript module `gracefulExit.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/history.ts` | frontend-ts | TypeScript module `history.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/inputMetrics.ts` | frontend-ts | TypeScript module `inputMetrics.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/liveProgress.test.ts` | frontend-ts | TypeScript module `liveProgress.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/liveProgress.ts` | frontend-ts | TypeScript module `liveProgress.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/mathUnicode.ts` | frontend-ts | TypeScript module `mathUnicode.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/memory.test.ts` | frontend-ts | TypeScript module `memory.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/memory.ts` | frontend-ts | TypeScript module `memory.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/memoryMonitor.ts` | frontend-ts | TypeScript module `memoryMonitor.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/messages.test.ts` | frontend-ts | TypeScript module `messages.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/messages.ts` | frontend-ts | TypeScript module `messages.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/model-search-text.test.ts` | frontend-ts | TypeScript module `model-search-text.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/model-search-text.ts` | frontend-ts | TypeScript module `model-search-text.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/openExternalUrl.test.ts` | frontend-ts | TypeScript module `openExternalUrl.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/openExternalUrl.ts` | frontend-ts | TypeScript module `openExternalUrl.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/osc52.ts` | frontend-ts | TypeScript module `osc52.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/parentLog.ts` | frontend-ts | TypeScript module `parentLog.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/perfPane.tsx` | frontend-tsx | React component `perfPane.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/lib/petPolling.ts` | frontend-ts | TypeScript module `petPolling.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/platform.ts` | frontend-ts | TypeScript module `platform.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/precisionWheel.ts` | frontend-ts | TypeScript module `precisionWheel.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/prompt.ts` | frontend-ts | TypeScript module `prompt.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/reasoning.ts` | frontend-ts | TypeScript module `reasoning.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/resizeCoalescer.test.ts` | frontend-ts | TypeScript module `resizeCoalescer.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/resizeCoalescer.ts` | frontend-ts | TypeScript module `resizeCoalescer.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/rpc.ts` | frontend-ts | TypeScript module `rpc.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/starmapPalette.ts` | frontend-ts | TypeScript module `starmapPalette.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/subagentTree.ts` | frontend-ts | TypeScript module `subagentTree.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/syntax.ts` | frontend-ts | TypeScript module `syntax.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/terminalModes.ts` | frontend-ts | TypeScript module `terminalModes.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/terminalParity.ts` | frontend-ts | TypeScript module `terminalParity.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/terminalSetup.ts` | frontend-ts | TypeScript module `terminalSetup.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/termux.ts` | frontend-ts | TypeScript module `termux.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/text.test.ts` | frontend-ts | TypeScript module `text.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/text.ts` | frontend-ts | TypeScript module `text.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/themeBoot.ts` | frontend-ts | TypeScript module `themeBoot.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/todo.test.ts` | frontend-ts | TypeScript module `todo.test.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/todo.ts` | frontend-ts | TypeScript module `todo.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/viewportStore.ts` | frontend-ts | TypeScript module `viewportStore.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/virtualHeights.ts` | frontend-ts | TypeScript module `virtualHeights.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/wheelAccel.ts` | frontend-ts | TypeScript module `wheelAccel.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/lib/widgetGrid.ts` | frontend-ts | TypeScript module `widgetGrid.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/protocol/interpolation.ts` | frontend-ts | TypeScript module `interpolation.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/protocol/paste.ts` | frontend-ts | TypeScript module `paste.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/sdk/apps/dialogTest.tsx` | frontend-tsx | React component `dialogTest.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/sdk/apps/gridTest.tsx` | frontend-tsx | React component `gridTest.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/sdk/apps/gridTestState.ts` | frontend-ts | TypeScript module `gridTestState.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/sdk/apps/index.ts` | frontend-ts | TypeScript module `index.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/sdk/apps/ticker.tsx` | frontend-tsx | React component `ticker.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/sdk/apps/weather.tsx` | frontend-tsx | React component `weather.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/sdk/host.tsx` | frontend-tsx | React component `host.tsx` | Renders part of a frontend surface; bundled by the TS build |  |
| `ui-tui/src/sdk/index.ts` | frontend-ts | TypeScript module `index.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/sdk/registry.ts` | frontend-ts | TypeScript module `registry.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/sdk/types.ts` | frontend-ts | TypeScript module `types.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/sdk/userWidgets.ts` | frontend-ts | TypeScript module `userWidgets.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/theme.ts` | frontend-ts | TypeScript module `theme.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/types.ts` | frontend-ts | TypeScript module `types.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/src/types/hermes-ink.d.ts` | frontend-ts | TypeScript module `hermes-ink.d.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
| `ui-tui/tsconfig.build.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `ui-tui/tsconfig.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `ui-tui/vitest.config.ts` | frontend-ts | TypeScript module `vitest.config.ts` | Frontend/shared TS source consumed by the tsc/vite build |  |
