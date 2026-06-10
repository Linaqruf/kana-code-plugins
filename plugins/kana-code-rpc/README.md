# kana-code-rpc

Display Claude Code activity as Discord Rich Presence.

```
Editing presence.py on kana-code-plugins (master)
Fable 5 • 129k ctx • $6.44 • +309 -104
[View on GitHub]
```

A background daemon watches your Claude Code sessions (via hooks) and updates
Discord. An optional statusline renders the same data in your terminal.

## Features

- **Activity states** — Editing, Running, Searching, Delegating, plus lifecycle
  states: *Thinking* (prompt submitted), *Compacting context*, *Waiting for input*
- **Project context** — repo name from git remote, branch, filename while editing
- **Live metrics** (via statusline integration) — model, current context usage,
  API cost, lines changed (+156 -23), context warning at >80%
- **Repository button** — "View on GitHub" auto-detected from the git remote
  (custom label/URL configurable). Note: Discord shows presence buttons to
  *other* viewers of your profile, not to you.
- **Multi-session** — multiple terminals share one daemon; sessions are tracked
  by Claude Code process PID and cleaned up when processes die
- **Idle detection** — shows "Idling" after inactivity (default 5 min)
- **MCP tool support** — `mcp__*` tools display as "Using MCP"
- **YAML config with hot-reload** — changes apply within ~30s, no restart

## Prerequisites

- Python 3.10+
- Discord desktop app (running locally)
- `pip install pypresence` (required), `pip install pyyaml` (optional, for config.yaml)

## Install

```bash
/plugin marketplace add Linaqruf/kana-code-plugins
/plugin install kana-code-rpc@kana-code-plugins
```

Hooks activate automatically — no commands to run.

### Statusline (recommended)

The statusline feeds model/token/cost data to the Discord display *and* renders
a terminal status bar. In `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python /path/to/kana-code-rpc/scripts/statusline.py"
  }
}
```

Terminal output: `Fable 5 › ⚡ Editing › █░░░░░░░░░ 14% › 145k ctx › $7.18 › 59m › main`

The `ctx` figure is your **current context composition** (what's in the window
now), not cumulative session usage — that's what Claude Code's
`context_window.total_input_tokens` actually reports. A `5h NN%` warning
appears when your 5-hour rate-limit window passes 80%.

## Configuration

`.claude-plugin/config.yaml` in the plugin directory (requires PyYAML):

```yaml
discord_app_id: null          # Custom Discord application ID (optional)

display:
  show_tokens: true           # Context token count (129k ctx)
  show_cost: true             # API cost ($0.18)
  show_model: true            # Model name
  show_branch: true           # Git branch
  show_file: true             # Filename when editing
  show_lines: true            # Lines added/removed
  show_context_warning: true  # Context % warning at >80%
  show_button: true           # Repository link button

custom_button_label: ""       # Override button label (max 31 chars)
custom_button_url: ""         # Override button URL (http(s), max 512 chars)

idle_timeout: 300             # Seconds before "Idling"
```

Config hot-reloads every ~30 seconds while the daemon runs.

## How it works

| Hook | Trigger | Action |
|------|---------|--------|
| `SessionStart` | Claude Code opens | Register session (by PID), start daemon if needed |
| `UserPromptSubmit` | You send a prompt | Show "Thinking" |
| `PreToolUse` | Before each tool | Show tool activity (Editing, Running, …) |
| `PreCompact` | Context compaction | Show "Compacting context" |
| `Stop` | Response finished | Show "Waiting for input" |
| `SubagentStop` | Subagent finished | Clear agent attribution |
| `SessionEnd` | Claude Code exits | Unregister session; stop daemon if last |

Sessions are tracked by walking up the process tree to the Claude Code
process PID; the daemon prunes dead PIDs every 10 seconds and exits when the
last session ends.

Data flow: hooks and the statusline write to a shared `state.json` (file-locked,
atomic writes); the daemon polls it once per second and pushes changes to
Discord via pypresence.

## Debugging

```bash
python scripts/presence.py status   # Daemon PID, sessions, current state
```

- Daemon log: `%APPDATA%\kana-code-rpc\daemon.log` (Windows) /
  `~/.local/share/kana-code-rpc/daemon.log` (Linux/macOS)
- Set `KANA_RPC_DATA_DIR` to relocate state/log files (also used by tests)

## Troubleshooting

- **No presence in Discord** — check Discord is running, Activity Privacy
  ("Share your detected activities") is enabled, and read `daemon.log`. The
  daemon gives up after ~1 minute if Discord is unreachable; it restarts with
  the next Claude Code session.
- **Button doesn't appear for me** — Discord only renders presence buttons to
  other users viewing your profile. Ask a friend, or check `daemon.log` for the
  payload.
- **Config ignored** — install PyYAML (`pip install pyyaml`); check log for
  "config.yaml is being IGNORED".
- **Stale presence after a crash** — dead sessions are pruned within ~10s; if a
  daemon hangs, `python scripts/presence.py status` shows the PID to kill.

## Development

```bash
python -m pytest scripts/tests -v
```

Tests isolate their state via `KANA_RPC_DATA_DIR` and include a consistency
check that every tool in the hooks matcher has a display name — update
`TOOL_DISPLAY` in `presence.py` and the matcher in `hooks/hooks.json` together
when Claude Code adds tools.

## License

MIT
