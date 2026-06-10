#!/usr/bin/env python3
"""
Claude Code Statusline with Discord RPC Integration

Displays a breadcrumb-style status bar (inspired by macOS Finder path bar)
showing model, tokens, cost, and git branch.
Also updates state.json to provide token/cost, duration, lines changed,
agent name, and context data to the Discord RPC daemon.

Setup in ~/.claude/settings.json (use appropriate path for your OS):
{
  "statusLine": {
    "type": "command",
    "command": "python /path/to/kana-code-rpc/scripts/statusline.py"
  }
}
"""
import json
import sys
import os
from pathlib import Path
import time as _time  # used for statusline_update timestamp

# Shared state management (provides process-safe file locking and utilities)
from state import StateLock, read_state_unlocked, write_state_unlocked, format_tokens

# Display name mappings shared with the daemon (presence.py has no import-time
# side effects; pypresence is only imported inside run_daemon)
from presence import TOOL_DISPLAY, PSEUDO_TOOL_DISPLAY

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, OSError) as e:
        # Warn user about potential garbled output
        print(f"[statusline] Warning: UTF-8 encoding unavailable ({e}), output may be garbled", file=sys.stderr)

# ═══════════════════════════════════════════════════════════════
# Apple System Colors (ANSI approximations)
# ═══════════════════════════════════════════════════════════════

class C:
    """ANSI color codes - Apple system colors"""
    RESET = '\x1b[0m'
    BOLD = '\x1b[1m'
    DIM = '\x1b[2m'

    # Apple palette
    WHITE = '\x1b[97m'      # Primary text
    GRAY = '\x1b[90m'       # Secondary/dim
    BLUE = '\x1b[94m'       # System Blue - accent
    GREEN = '\x1b[92m'      # System Green - positive
    ORANGE = '\x1b[93m'     # System Orange - warning
    RED = '\x1b[91m'        # System Red - critical


# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

def format_cost(cost: float) -> str:
    """Format cost with appropriate precision"""
    if cost >= 100:
        return f"${cost:.0f}"
    if cost >= 10:
        return f"${cost:.1f}"
    if cost >= 0.01:
        return f"${cost:.2f}"
    return f"${cost:.3f}"


def format_duration(ms: int) -> str:
    """Format session duration for display (e.g., 42m, 1h05m). '' under a minute."""
    total_min = ms // 60000
    if total_min < 1:
        return ""
    hours, minutes = divmod(total_min, 60)
    return f"{hours}h{minutes:02d}m" if hours else f"{minutes}m"


def create_progress_bar(percent: float, width: int = 10) -> str:
    """Create Apple-style progress bar with color coding"""
    percent = max(0.0, min(100.0, percent))  # Clamp to avoid overdrawing the bar
    filled = round((percent / 100) * width)
    empty = width - filled

    filled_char = '█'
    empty_char = '░'

    # Color based on usage (Apple system colors)
    if percent > 95:
        bar_color = C.RED
    elif percent > 80:
        bar_color = C.ORANGE
    else:
        bar_color = C.WHITE

    return f"{bar_color}{filled_char * filled}{C.GRAY}{empty_char * empty}{C.RESET}"


def get_git_branch(cwd: str) -> str | None:
    """Get current git branch via git rev-parse (handles worktrees and detached HEAD)."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
            return branch if branch != "HEAD" else None  # Detached HEAD
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return None


def truncate(s: str, max_len: int) -> str:
    """Truncate string with ellipsis"""
    if len(s) <= max_len:
        return s
    return s[:max_len - 1] + '…'



# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    # Read JSON from stdin using os.read() to avoid blocking on EOF.
    # os.read() returns immediately when pipe data is available, while
    # sys.stdin.read()/json.load() wait for pipe closure which may hang.
    try:
        if sys.stdin is None:
            print("")
            return
        raw = os.read(sys.stdin.fileno(), 262144)
        if not raw:
            print("")
            return
        data = json.loads(raw.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError, OSError) as e:
        print(f"[statusline] Error reading input: {e}", file=sys.stderr)
        print(f"{C.RED}[statusline error]{C.RESET}")
        return

    # Extract data
    model_info = data.get("model") or {}
    model = model_info.get("display_name") or ""
    model_id = model_info.get("id") or ""

    # `or 0` guards: fields can be present-but-null before the first API response
    cost_info = data.get("cost") or {}
    cost = cost_info.get("total_cost_usd") or 0.0
    duration_ms = cost_info.get("total_duration_ms") or 0
    lines_added = cost_info.get("total_lines_added") or 0
    lines_removed = cost_info.get("total_lines_removed") or 0

    # NOTE: total_input_tokens/total_output_tokens describe the CURRENT CONTEXT
    # composition (input includes cache reads/writes), not cumulative session
    # totals — verified against a live Claude Code 2.1.170 payload.
    context = data.get("context_window") or {}
    total_input = context.get("total_input_tokens") or 0
    total_output = context.get("total_output_tokens") or 0
    used_percent = context.get("used_percentage") or 0.0
    context_size = context.get("context_window_size") or 200000

    current_usage = context.get("current_usage") or {}
    cache_read = current_usage.get("cache_read_input_tokens") or 0
    cache_write = current_usage.get("cache_creation_input_tokens") or 0

    rate_limits = data.get("rate_limits") or {}
    five_hour_pct = (rate_limits.get("five_hour") or {}).get("used_percentage") or 0

    workspace = data.get("workspace") or {}
    cwd = workspace.get("current_dir", os.getcwd())
    project_dir = workspace.get("project_dir", "")
    git_branch = get_git_branch(cwd)

    agent_info = data.get("agent") or {}
    agent_name = agent_info.get("name") or ""

    # Update state.json for Discord RPC (with file locking to prevent race conditions)
    current_tool = ""
    try:
        with StateLock(timeout=1.0):  # Short timeout since statusline runs frequently
            state = read_state_unlocked()
            if state.get("session_start"):  # Only update if session exists
                current_tool = state.get("tool", "")
                updates = {
                    "model": model,
                    "model_id": model_id,
                    "tokens": {
                        "input": total_input,
                        "output": total_output,
                        "cache_read": cache_read,
                        "cache_write": cache_write,
                        "cost": cost,
                    },
                    "duration_ms": duration_ms,
                    "lines_added": lines_added,
                    "lines_removed": lines_removed,
                    "context_pct": used_percent or 0,
                    "context_size": context_size,
                    "agent_name": agent_name,
                }
                if project_dir:
                    # Only update project name when active project changes (multi-session switch).
                    # Preserves git remote name from cmd_start for single session.
                    if state.get("project_path") != project_dir:
                        updates["project"] = Path(project_dir).name
                        updates["project_path"] = project_dir
                    if git_branch:
                        updates["git_branch"] = git_branch

                # Throttle writes: the statusline renders several times per second
                # and unconditional writes are the main source of state-lock
                # contention with the daemon. duration_ms advances with the wall
                # clock on every render, so it is excluded from change detection —
                # a 5s heartbeat keeps it fresh enough for the elapsed timer.
                significant = {k: v for k, v in updates.items() if k != "duration_ms"}
                changed = any(state.get(k) != v for k, v in significant.items())
                now_ts = _time.time()
                if changed or now_ts - state.get("statusline_update", 0) >= 5:
                    state.update(updates)
                    state["statusline_update"] = int(now_ts)
                    write_state_unlocked(state)
    except (OSError, TimeoutError) as e:
        # Don't fail statusline display if state update fails
        print(f"[statusline] Warning: Could not update state: {e}", file=sys.stderr)

    # ─────────────────────────────────────────────────────────────
    # Build Apple Finder Path Bar Statusline
    # ─────────────────────────────────────────────────────────────

    parts = []
    chevron = f"{C.GRAY}  ›  {C.RESET}"

    # Model name (primary, blue accent)
    if model:
        parts.append(f"{C.BLUE}{C.BOLD}{model}{C.RESET}")

    # Current activity indicator (from shared state, written by hook events)
    if current_tool:
        activity_map = {**TOOL_DISPLAY, **PSEUDO_TOOL_DISPLAY}
        if current_tool in activity_map:
            parts.append(f"{C.ORANGE}⚡ {activity_map[current_tool]}{C.RESET}")
        elif current_tool.startswith("mcp__"):
            parts.append(f"{C.ORANGE}⚡ MCP{C.RESET}")

    # Progress bar with percentage
    progress_bar = create_progress_bar(used_percent)
    percent_str = round(max(0.0, min(100.0, used_percent)))
    parts.append(f"{progress_bar} {C.WHITE}{percent_str}%{C.RESET}")

    # Context token count (current context composition, not session totals)
    context_tokens = total_input + total_output
    if context_tokens > 0:
        tokens_str = format_tokens(context_tokens)
        parts.append(f"{C.WHITE}{tokens_str} ctx{C.RESET}")

    # Cost (green for Apple "positive" feel)
    if cost > 0:
        cost_str = format_cost(cost)
        parts.append(f"{C.GREEN}{cost_str}{C.RESET}")

    # Elapsed session time (subtle)
    duration_str = format_duration(duration_ms)
    if duration_str:
        parts.append(f"{C.GRAY}{duration_str}{C.RESET}")

    # Rate-limit warning — only shown when the 5-hour window is nearly used
    if five_hour_pct >= 80:
        limit_color = C.RED if five_hour_pct >= 95 else C.ORANGE
        parts.append(f"{limit_color}5h {round(five_hour_pct)}%{C.RESET}")

    # Git branch (subtle, at the end)
    if git_branch:
        branch_display = truncate(git_branch, 16)
        parts.append(f"{C.GRAY}{branch_display}{C.RESET}")

    # Join with chevron separators (Finder breadcrumb style)
    status_line = chevron.join(parts)

    print(status_line)


if __name__ == "__main__":
    main()
