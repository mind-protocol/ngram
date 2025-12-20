# Archived: SYNC_TUI_State.md (Condensed)

Archived on: 2025-12-19
Source: `docs/tui/SYNC_TUI_State.md` (pre-size reduction)

---

## Completed Features (Condensed)

- Two-panel layout (manager left, agents right) with input bar and status bar.
- Agent integration: subprocess-based providers (Claude/Gemini/Codex), streaming output, thinking blocks.
- Command handling: `/help`, `/repair`, `/doctor`, `/quit`, `/clear`, `/run`, `/issues`.
- Input history, tab completion, command detection.
- Conversation history stored in `.ngram/state/conversation_history.json`.
- Agent panels with headers, status colors, auto-collapse, capped output lines.
- Repair session folders under `.ngram/repairs/{timestamp}/` with ISSUE.md per agent.
- Error logging to `.ngram/error_log.txt`.
- Theme: Paper & Parchment (light) with optional dark toggle.

---

## Planned Features (Condensed)

- Syntax highlighting for code blocks.
- `/sync` auto-refresh.
- `/repair --max N`.
- Tab layout for >3 agents.
- Right-click copy (explicit support).

---

## Known Gaps

- Queue processing for >3 issues.
- Tab layout for >3 agents not implemented.

---

## Known Issues (Historical)

- None active as of 2025-12-19.
- Resolved: INCOMPLETE_IMPL false positives in `app.py`, `state.py`, `widgets/*` (see doctor-ignore notes).

---

## Handoff Notes (Historical)

- TUI functional with agent integration; theme and performance updates completed.
- Watch-outs: Textual optional dependency; markup vs Markdown rendering; use chunked stdout.

---

## Agent Observations (Historical)

- Commands split to keep `commands.py` smaller.
- Suggestion: Keep doctor-ignore and SYNC notes aligned.
