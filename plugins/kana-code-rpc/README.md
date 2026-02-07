# kana-code-rpc

Claude Code plugin that displays your coding activity as Discord Rich Presence.

## Features

- **Activity display**: Editing, Reading, Running command, Searching, etc.
- **File display**: Shows filename when editing (e.g., "Editing main.py")
- **Project info**: Name (from git remote or folder) + branch
- **Model display**: Opus 4.5, Sonnet 4, Haiku 4.5, etc.
- **Token tracking**: Cycling display showing simple vs cached tokens
- **Cost tracking**: Real-time API cost based on model pricing
- **Multi-session**: Supports multiple Claude Code terminals
- **Idle state**: Shows "Idling" after configurable timeout (default 5 min)
- **Elapsed time**: Time since session start
- **Configurable**: YAML config for custom app ID and display preferences

## Display

```
┌─────────────────────────────────────────┐
│ Kana Code                               │
│ Editing main.py on my-project (main)    │
│ Opus 4.5 • 22.9k tokens • $0.18         │
│ ⏱ 1:23:45                               │
└─────────────────────────────────────────┘
```

The token display cycles every 8 seconds:
- **5s**: Simple view - `Opus 4.5 • 22.9k tokens • $0.18` (input + output only)
- **3s**: Cached view - `Opus 4.5 • 54.3M cached • $0.18` (includes cache tokens)

## Prerequisites

- Python 3.10+
- Discord desktop app running
- pypresence library (required)
- pyyaml library (optional, for config.yaml support)

## Installation

1. Install dependencies:
   ```bash
   pip install pypresence pyyaml
   ```

2. Copy this plugin to your Claude Code plugins directory:
   ```bash
   # Option 1: Global plugins (recommended)
   cp -r kana-code-rpc ~/.claude/plugins/

   # Option 2: Project-level
   cp -r kana-code-rpc /path/to/your/project/.claude-plugins/
   ```

3. Restart Claude Code

## Statusline Setup (Required)

The plugin requires Claude Code's statusline feature for token/cost data.

Add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python /path/to/kana-code-rpc/scripts/statusline.py"
  }
}
```

Replace `/path/to/kana-code-rpc` with your actual plugin path.

**Bonus**: This also displays an Apple Finder-style status bar in Claude Code:
```
Opus 4.5  ›  ████░░░░░░ 42%  ›  29.4k tokens  ›  $0.18  ›  main
```

## Configuration

Edit `.claude-plugin/config.yaml` to customize the plugin:

```yaml
# Custom Discord Application ID (optional)
discord_app_id: null  # Default: 1330919293709324449

# Display settings
display:
  show_tokens: true    # Token count (22.9k tokens)
  show_cost: true      # API cost ($0.18)
  show_model: true     # Model name (Opus 4.5)
  show_branch: true    # Git branch (main)
  show_file: false     # Filename when editing (off by default)

# Idle timeout in seconds (default: 300 = 5 minutes)
idle_timeout: 300
```

Config changes are hot-reloaded every 30 seconds — no daemon restart needed.

## Custom Discord App

To use your own Discord application (for custom branding):

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Copy the Application ID (17-19 digit number)
4. Set `discord_app_id` in `.claude-plugin/config.yaml`
5. Upload assets (optional): Add a "claude" image in Rich Presence > Art Assets

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                   Claude Code                        │
├─────────────────────────────────────────────────────┤
│  Hooks (events)        │  Statusline (token data)   │
│  └─ presence.py        │  └─ statusline.py          │
└───────────┬────────────┴────────────┬───────────────┘
            │                         │
            ▼                         ▼
      ┌─────────────────────────────────┐
      │     state.json (file-locked)    │
      └───────────────┬─────────────────┘
                      │
                      ▼
      ┌─────────────────────────────────┐
      │    Daemon → Discord RPC         │
      └─────────────────────────────────┘
```

| Component | Trigger | Action |
|-----------|---------|--------|
| SessionStart hook | Claude Code opens | Start daemon, set project/branch |
| PreToolUse hook | Before any tool use | Update current activity |
| Statusline | Every ~300ms | Update model/tokens/cost |
| SessionEnd hook | Claude Code exits | Stop daemon if last session |

### Tracked Tools

Edit, Write, Read, Bash, Glob, Grep, LS, Task, WebFetch, WebSearch, NotebookEdit, NotebookRead, AskUserQuestion, TodoRead, TodoWrite, and MCP tools (`mcp__.*`).

## Manual Control

```bash
# Check status
python scripts/presence.py status

# Output:
# Daemon running (PID 12345)
# Active sessions: 1
# Project: my-project
# Branch: main
# Model: Opus 4.5
# Tokens (simple): 22.9k (20k in / 2.9k out)
# Tokens (cached): 54.3M (+51M read / +3.3M write)
# Cost: $0.18

# Force stop all sessions
python scripts/presence.py stop
```

## Data Files

Location: `%APPDATA%/kana-code-rpc/` (Windows) or `~/.local/share/kana-code-rpc/` (Linux/macOS)

| File | Purpose |
|------|---------|
| `state.json` | Current session state (file-locked) |
| `state.lock` | Lock file for state access |
| `sessions.json` | Active session PIDs (file-locked) |
| `sessions.lock` | Lock file for sessions access |
| `daemon.pid` | Background daemon process ID |
| `daemon.log` | Debug log |

## Troubleshooting

**Presence not showing:**
- Make sure Discord desktop app is running
- Check if pypresence is installed: `pip show pypresence`
- Check logs: `%APPDATA%/kana-code-rpc/daemon.log`

**No tokens/cost displayed:**
- Statusline setup is required - see "Statusline Setup" section
- Verify `~/.claude/settings.json` has the statusLine config
- Restart Claude Code after adding statusline config

**"Could not connect" errors:**
- Discord must be running before Claude Code starts
- Try restarting Discord

**Wrong project name:**
- Project name comes from git remote origin URL
- Falls back to folder name if not a git repo

## License

MIT
