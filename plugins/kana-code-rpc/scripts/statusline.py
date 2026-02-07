#!/usr/bin/env python3
"""
Claude Code Statusline with Discord RPC Integration

Displays a breadcrumb-style status bar (inspired by macOS Finder path bar)
showing model, tokens, cost, and git branch.
Also updates state.json to provide token/cost data to the Discord RPC daemon.

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
from datetime import datetime

# Shared state management (provides process-safe file locking and utilities)
from state import StateLock, read_state_unlocked, write_state_unlocked, format_tokens

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


def create_progress_bar(percent: float, width: int = 10) -> str:
    """Create Apple-style progress bar with color coding"""
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
    """Get current git branch from .git/HEAD"""
    try:
        git_head = Path(cwd) / '.git' / 'HEAD'
        if git_head.exists():
            head = git_head.read_text().strip()
            if head.startswith('ref: refs/heads/'):
                return head.replace('ref: refs/heads/', '')
    except (OSError, UnicodeDecodeError):
        # Git branch detection is optional, fail silently
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
        raw = os.read(sys.stdin.fileno(), 65536)
        if not raw:
            print("")
            return
        data = json.loads(raw.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError, OSError) as e:
        print(f"[statusline] Error reading input: {e}", file=sys.stderr)
        print(f"{C.RED}[statusline error]{C.RESET}")
        return

    # Extract data
    model_info = data.get("model", {})
    model = model_info.get("display_name", "")
    model_id = model_info.get("id", "")

    cost_info = data.get("cost", {})
    cost = cost_info.get("total_cost_usd", 0.0)

    context = data.get("context_window", {})
    total_input = context.get("total_input_tokens", 0)
    total_output = context.get("total_output_tokens", 0)
    used_percent = context.get("used_percentage", 0.0)

    current_usage = context.get("current_usage") or {}
    cache_read = current_usage.get("cache_read_input_tokens", 0)
    cache_write = current_usage.get("cache_creation_input_tokens", 0)

    cwd = data.get("workspace", {}).get("current_dir", os.getcwd())
    git_branch = get_git_branch(cwd)

    # Update state.json for Discord RPC (with file locking to prevent race conditions)
    try:
        with StateLock(timeout=1.0):  # Short timeout since statusline runs frequently
            state = read_state_unlocked()
            if state.get("session_start"):  # Only update if session exists
                state["model"] = model
                state["model_id"] = model_id
                state["tokens"] = {
                    "input": total_input,
                    "output": total_output,
                    "cache_read": cache_read,
                    "cache_write": cache_write,
                    "cost": cost,
                }
                state["statusline_update"] = int(datetime.now().timestamp())
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

    # Progress bar with percentage
    progress_bar = create_progress_bar(used_percent)
    percent_str = round(used_percent)
    parts.append(f"{progress_bar} {C.WHITE}{percent_str}%{C.RESET}")

    # Token count
    total_tokens = total_input + total_output
    if total_tokens > 0:
        tokens_str = format_tokens(total_tokens)
        parts.append(f"{C.WHITE}{tokens_str} tokens{C.RESET}")

    # Cost (green for Apple "positive" feel)
    if cost > 0:
        cost_str = format_cost(cost)
        parts.append(f"{C.GREEN}{cost_str}{C.RESET}")

    # Git branch (subtle, at the end)
    if git_branch:
        branch_display = truncate(git_branch, 16)
        parts.append(f"{C.GRAY}{branch_display}{C.RESET}")

    # Join with chevron separators (Finder breadcrumb style)
    status_line = chevron.join(parts)

    print(status_line)


if __name__ == "__main__":
    main()
