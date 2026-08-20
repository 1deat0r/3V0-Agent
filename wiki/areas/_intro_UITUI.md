Ink (React) terminal UI — `3v0 --tui`. TypeScript owns the screen; `tui_gateway` (Python) owns sessions/tools. The dashboard embeds the real TUI through a PTY — never re-implement it in React.
