# kana-code-rpc

Display Claude Code activity as Discord Rich Presence.

```
Editing presence.py on kana-code-plugins (master)
Opus 5.5 • 129k ctx • $6.44 • +309 -104
[View on GitHub]
```

A background daemon follows your Claude Code sessions and updates Discord.
An optional statusline renders the same data in your terminal.

## Features

- **Activity states**: Editing, Reading, Running, Searching, and so on, plus
  *Thinking* (prompt submitted), *Delegating to <agent>* (while subagents
  run), *Compacting context* and *Waiting for input*
- **Project context**: repo name from the git remote, branch, and the
  filename while editing
- **Live metrics** (from the statusline): model, current context usage, cost
  as Claude Code reports it, lines changed (+156 -23), context warning above
  80%
- **Repository button**: "View on GitHub", detected from the git remote
  (label and URL configurable). Discord shows presence buttons to *other*
  viewers of your profile, not to you.
- **Multi-session**: one daemon serves every terminal. Discord shows the most
  recently active session, and dead sessions are cleaned up.
- **Idle detection**: shows "Idling" after inactivity (default 5 min)
- **MCP tools** show as "Using MCP"
- **YAML config with hot-reload**: changes apply within ~30 s

## Light by design

The plugin starts no process per tool call. The daemon reads the current
tool from the session transcript (reading only the new bytes, once a
second), so a burst of parallel subagents costs the plugin nothing. Hooks run
only at session start, session end and compaction. Each hook process has a
hard deadline, and the plugin never runs git: it reads `.git/HEAD` and
`.git/config`. Discord accepts one presence update per 15 s, so the daemon
sends at most that.

## Prerequisites

- Python 3.10+, reachable as `python` on your PATH. The hooks call
  `python`; on Debian/Ubuntu the `python-is-python3` package provides it.
- Discord desktop app, running locally
- `pip install pypresence` (required), `pip install pyyaml` (optional, for
  config.yaml)

## Install

```bash
/plugin marketplace add Linaqruf/kana-code-plugins
/plugin install kana-code-rpc@kana-code-plugins
```

Hooks activate automatically. There are no commands to run.

### Statusline (recommended)

The statusline feeds model, context and cost data to the Discord display
*and* renders a terminal status bar. In `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python /path/to/kana-code-rpc/scripts/statusline.py"
  }
}
```

Claude Code runs this command on every update, so start the interpreter
directly. On Windows, `python` is often a launcher (the Microsoft Store alias
or the Python install manager) that starts the real interpreter in a second
process. Use the interpreter's full path, with forward slashes, for example
`C:/Users/you/AppData/Local/Python/pythoncore-3.14-64/python.exe`.
`python -c "import sys; print(sys.executable)"` prints it.

Terminal output: `Opus 5.5 › ⚡ Editing › █░░░░░░░░░ 14% › 145k ctx › $7.18 › 59m › main`

The `ctx` figure is your **current context** (what is in the window now),
not cumulative session usage. That is what Claude Code's
`context_window.total_input_tokens` reports. A `5h NN%` warning appears when
your 5-hour rate-limit window passes 80%.

Without the statusline, Discord still shows the activity, project, branch
and model (read from the transcript). Only context usage, cost and line
counts need it.

## Configuration

`.claude-plugin/config.yaml` in the plugin directory (requires PyYAML):

```yaml
discord_app_id: null          # Custom Discord application ID (optional)

display:
  show_tokens: true           # Context token count (129k ctx)
  show_cost: true             # Cost ($0.18)
  show_model: true            # Model name
  show_branch: true           # Git branch
  show_file: true             # Filename when editing
  show_lines: true            # Lines added/removed
  show_context_warning: true  # Context % warning above 80%
  show_button: true           # Repository link button

custom_button_label: ""       # Override button label (max 31 chars)
custom_button_url: ""         # Override button URL (http(s), max 512 chars)

idle_timeout: 300             # Seconds before "Idling"
```

Config hot-reloads about every 30 seconds while the daemon runs.

## How it works

| Hook | Trigger | Action |
|------|---------|--------|
| `SessionStart` | Claude Code opens, `/clear`, `/resume`, compaction | Register the session and its transcript; start the daemon if needed |
| `PreCompact` | Context compaction | Show "Compacting context" |
| `SessionEnd` | Claude Code exits | Unregister the session; the daemon exits after the last one |

The daemon reads each session's transcript for the current tool, prompts
(*Thinking*) and turn ends (*Waiting for input*). While background subagents
work, it shows *Delegating to <agent>*. Sessions are tracked by the PID of
the Claude Code process, and dead PIDs are pruned every 10 seconds. The
statusline records each session's model, context and cost in a shared
`state.json`. The daemon polls once a second and pushes changes to Discord
through pypresence, at most once per 15 s. If Discord is closed, the daemon
waits and retries (every 15–60 s) for as long as a session is open.

## Debugging

```bash
python scripts/presence.py status   # Daemon PID and version, sessions, state
```

- Daemon log: `%APPDATA%\kana-code-rpc\daemon.log` (Windows) /
  `~/.local/share/kana-code-rpc/daemon.log` (Linux/macOS)
- Set `KANA_RPC_DATA_DIR` to relocate state and log files (also used by
  tests)

## Troubleshooting

- **No presence in Discord**: check that Discord is running and that
  Activity Privacy ("Share your detected activities") is on, then read
  `daemon.log`. `Discord not reachable` means the daemon is still waiting for
  Discord.
- **Button doesn't appear for me**: Discord only renders presence buttons to
  other users viewing your profile. Ask a friend, or check `daemon.log` for
  the payload.
- **Config ignored**: install PyYAML (`pip install pyyaml`) and check the log
  for "config.yaml is being IGNORED".
- **Stale presence after a crash**: dead sessions are pruned within about
  10 s. `python scripts/presence.py status` shows the daemon PID.

## Development

```bash
python -m pytest scripts/tests -v
```

Tests isolate their state through `KANA_RPC_DATA_DIR`. They include a test
that a hook exits by its own deadline when its stdin never closes, and
guards that keep per-tool hooks out of `hooks/hooks.json`.

## License

MIT
