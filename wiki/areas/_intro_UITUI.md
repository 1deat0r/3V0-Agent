Ink (React) terminal UI — `hermes --tui`. TypeScript owns the screen; `tui_gateway` (Python) owns sessions/tools. The dashboard embeds the real TUI through a PTY — never re-implement it in React.
