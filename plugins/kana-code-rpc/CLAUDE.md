# kana-code-rpc — Developer Notes

Discord Rich Presence plugin for Claude Code. v0.6.0. Hooks-only (no commands).

## Architecture

```
Claude Code hooks ──► presence.py {start|update|stop} ──► state.json (locked)
Claude Code statusline ──► statusline.py ─────────────────► state.json + sessions.json
                                                                   │
                              presence.py daemon (1s poll) ◄───────┘
                                       │
                                  pypresence ──► Discord
```

- `scripts/presence.py` — hook commands + daemon. One daemon per machine
  (PID file); exits when the last session ends.
- `scripts/statusline.py` — Claude Code statusline; renders the terminal bar
  AND enriches `state.json` with model/tokens/cost/context/duration.
- `scripts/state.py` — shared `StateLock` (cross-platform file lock), atomic
  JSON writes, `DATA_DIR` resolution (`KANA_RPC_DATA_DIR` env override).
- `hooks/hooks.json` — SessionStart, UserPromptSubmit, PreToolUse (tool
  matcher), PreCompact, Stop, SubagentStop, SessionEnd.

## Key invariants

1. **State schema is backward-compatible.** Installed (cached) plugin copies
   and working-copy statuslines can run different versions against the same
   `%APPDATA%\kana-code-rpc` files. Add state keys; don't rename or repurpose.
2. **`TOOL_DISPLAY` mirrors the PreToolUse matcher.** Enforced by
   `tests/test_presence.py::TestHooksConsistency`. When Claude Code adds a tool,
   update both `hooks/hooks.json` and `TOOL_DISPLAY` together.
3. **Pseudo-tools (`__prompt__`, `__compact__`, `__waiting__`) are not real
   tools** — they're written by lifecycle events and live in
   `PSEUDO_TOOL_DISPLAY`, never in `TOOL_DISPLAY`.
4. **Token semantics:** statusline `context_window.total_input_tokens` is the
   CURRENT CONTEXT composition (input includes cache reads/writes), not
   cumulative session totals (verified live on Claude Code 2.1.170). Displays
   say "ctx", not "tokens".
5. **Session tracking is PID-based** (`get_claude_ancestor_pid` walks the
   process tree; `sessions.json` maps PID → timestamp). `session_id` is stored
   for display only. Do not describe it as session_id-based tracking.
6. **One-shot hook commands stay quiet in the log** (`_config_verbose`);
   only the daemon logs config loads/changes.
7. **Statusline writes are throttled** — change-detection excludes
   `duration_ms` (it advances every render), with a 5s heartbeat. Unthrottled
   writes were the main source of state-lock contention.

## Testing

```bash
python -m pytest scripts/tests -v
```

- `tests/fixtures/statusline_payload.json` — sanitized real payload captured
  from Claude Code 2.1.170. Re-capture when the statusline schema changes.
- Subprocess tests isolate state via the `KANA_RPC_DATA_DIR` env var.
- Manual smoke test for hook events:
  `'{"hook_event_name":"Stop"}' | python scripts/presence.py update`
- Live-testing caveat: installed plugins run hooks from the marketplace cache,
  not the repo. Use `claude --plugin-dir` or push + `/plugin update` to test
  hook/daemon changes end-to-end.

## Release checklist

- Bump `plugin.json` AND the marketplace entry in
  `../../.claude-plugin/marketplace.json` (versions must match).
- Re-check the PreToolUse matcher against current Claude Code tool names.
- `claude plugin validate .` from the repo root must pass `--strict`.
