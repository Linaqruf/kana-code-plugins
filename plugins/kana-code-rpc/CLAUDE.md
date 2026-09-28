# kana-code-rpc — Developer Notes

Discord Rich Presence plugin for Claude Code. v1.1.0. Hooks-only (no commands).

## Architecture

```
SessionStart / PreCompact / SessionEnd hooks ──► presence.py {start|update|stop}
        │                                             │
        │                              sessions.json (PID → transcript) + state.json
        │                                             │
session transcripts (JSONL) ──► presence.py daemon (1 s poll) ──► pypresence ──► Discord
                                              ▲
Claude Code statusline ──► statusline.py ─────┘ (per-session model/context/cost in state.json)
```

- `scripts/presence.py`: hook commands and the daemon. One daemon per
  machine (`daemon.lock`); it exits when the last session ends.
- `scripts/activity.py`: `TranscriptTail` (current tool from the transcript),
  display maps, model-name formatting.
- `scripts/gitinfo.py`: branch, origin URL and project name from `.git`
  files.
- `scripts/statusline.py`: the statusline. It renders the terminal bar and
  records per-session metrics in `state.json`.
- `scripts/state.py`: `StateLock`, atomic JSON writes, `arm_watchdog`,
  `DATA_DIR` (`KANA_RPC_DATA_DIR` override).

## Key invariants

1. **No hook per tool call, turn or subagent.** The 2026-09-28 incident:
   PreToolUse ran a Git Bash → bash → Python-launcher → python chain on every
   tool call, including every subagent call. When the launcher stalled, the
   chains piled up for hours. Activity comes from the transcript instead.
   `TestHooksShape` keeps PreToolUse, UserPromptSubmit, Stop and Subagent*
   out of `hooks.json`.
2. **Every one-shot process arms `arm_watchdog` before anything can block.**
   Claude Code ignores `timeout` on `async: true` hooks (hooks docs, "Run
   hooks in the background"). Don't add `timeout` to them.
3. **Hooks stay in shell form** (`python "${CLAUDE_PLUGIN_ROOT}/…" cmd`).
   Exec form would drop the bash layer, but it cannot start `.bat` shims such
   as pyenv-win's `python`. With three hooks per session, the layer costs
   little.
4. **Never spawn git.** Use `gitinfo.py`, the transcript's `gitBranch`, or
   the statusline's `workspace.repo`.
5. **Transcripts can be gigabytes.** Read from the end only
   (`TAIL_BOOTSTRAP_BYTES`), and filter lines by substring before
   `json.loads`. Never hold the file open between polls.
6. **State stays backward-compatible with 1.0.0.** Hooks and the daemon run
   from the plugin cache, while the statusline may run from a working copy,
   and 1.0.0 sessions keep running until restarted. So:
   `daemon.pid` stays a bare PID (1.0.0 `int()`s it); the version lives in
   `daemon.version`. `sessions.json` values are an int (1.0.0) or a dict
   (1.1.0); read them through `session_record()`. The statusline still
   writes the flat state keys. Add keys; don't rename or repurpose.
7. **Discord pacing:** at most one update per `DISCORD_MIN_INTERVAL` (15 s);
   the latest payload wins.
8. **Token semantics:** `context_window.total_input_tokens` is the CURRENT
   context composition, not a cumulative total. Displays say "ctx".
9. **Cost is Claude Code's** (`cost.total_cost_usd`). Never compute it and
   never keep a price table. The model name comes from the statusline's
   `display_name`, else `model_display_name()` of the transcript's model ID.
   Neither needs a list of models.
10. **Every Discord call is bounded.** pypresence's `connect()` reads the
    handshake reply with no timeout; use `_connect_bounded` (the same steps
    under `asyncio.wait_for`). `LoopHeartbeat` exits a daemon whose loop
    stops for 2 minutes, so the OS frees `daemon.lock`. That lock, not the
    PID files (stale after a reboot), decides whether a daemon runs. A
    retiring daemon removes its PID files, then re-checks sessions and
    clears state under the sessions lock.

## Transcript facts (verified on Claude Code 2.1.283)

- Records are compact JSON: `type` is user / assistant / system / others.
  Assistant `message.content[]` holds `tool_use` blocks (`name`, `input`),
  and `message.stop_reason` is `end_turn` at the end of a turn. System
  `subtype` values include `turn_duration` (turn end) and
  `compact_boundary`. Every record has `gitBranch`.
- Agent calls run in the background by default: the main turn ends at once
  (tool result "Async agent launched successfully"), and each completion
  arrives as a `<task-notification>` user record carrying the call's
  `<tool-use-id>`. Subagent transcripts live in
  `<session>/subagents/agent-<id>.jsonl`, next to a `.meta.json` with
  `agentType`. Agent-tool subagents do not fire SessionStart.
- After `/compact`: a `compact_boundary` record, then a user record with
  `isCompactSummary: true` (not `isMeta`), which is not a prompt.
- Every record has an ISO `timestamp`. Order transcript events against hook
  timestamps by it, not by the time the daemon read the line.

## Testing

```bash
python -m pytest scripts/tests -v
```

- `tests/fixtures/statusline_payload.json` is a sanitized real payload from
  Claude Code 2.1.170. The fields used here still match the 2.1.283 docs.
- Subprocess tests isolate state through `KANA_RPC_DATA_DIR`.
- Hook smoke test:
  `'{"hook_event_name":"PreCompact","session_id":"x"}' | python scripts/presence.py update`
- Live burst test: `claude -p` with `--plugin-dir <this dir>`,
  `--setting-sources project,local` (loads only this plugin) and an isolated
  `KANA_RPC_DATA_DIR`. Count the processes under the claude process while 3
  subagents make reads. 1.1.0 starts 5 python + 4 bash for the whole session,
  however many tool calls it makes; 1.0.0 started 65 python + 69 bash for the
  same prompt.

## Release checklist

- Bump `plugin.json`, `VERSION` in `presence.py` (a test enforces it), and
  the marketplace entry in `../../.claude-plugin/marketplace.json`.
- `claude plugin validate .` and the marketplace `--strict` check, from a
  clean `git archive` export.
