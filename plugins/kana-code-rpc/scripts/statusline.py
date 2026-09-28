#!/usr/bin/env python3
"""
Claude Code statusline with Discord RPC integration.

Renders a breadcrumb-style status bar (model, activity, context, cost,
duration, branch) and records the session's model, context and cost in
state.json for the Discord daemon.

Claude Code runs this on every debounced update, so it must stay cheap: no
git process (the branch is read from .git/HEAD), and a hard deadline so a
stalled run cannot linger after Claude Code cancels it.

Setup in ~/.claude/settings.json (use the path of this file on your machine):
{
  "statusLine": {
    "type": "command",
    "command": "python /path/to/kana-code-rpc/scripts/statusline.py"
  }
}
"""
import json
import os
import sys
import time
from pathlib import Path

from state import StateLock, arm_watchdog, format_tokens, read_state_unlocked, write_state_unlocked
from activity import activity_label
from gitinfo import read_branch, read_origin_url, repo_url_from_workspace, repo_web_url

DEADLINE = 3.0            # seconds; Claude Code cancels slower runs anyway
LOCK_TIMEOUT = 0.5
HEARTBEAT = 5             # seconds between writes of unchanged metrics

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError) as e:
        print(f"[statusline] Warning: UTF-8 encoding unavailable ({e}), output may be garbled", file=sys.stderr)


class C:
    """ANSI colors (Apple system palette approximations)."""
    RESET = '\x1b[0m'
    BOLD = '\x1b[1m'
    WHITE = '\x1b[97m'
    GRAY = '\x1b[90m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    ORANGE = '\x1b[93m'
    RED = '\x1b[91m'


def format_cost(cost: float) -> str:
    if cost >= 100:
        return f"${cost:.0f}"
    if cost >= 10:
        return f"${cost:.1f}"
    if cost >= 0.01:
        return f"${cost:.2f}"
    return f"${cost:.3f}"


def format_duration(ms: int) -> str:
    """Session duration (e.g., 42m, 1h05m); '' under a minute."""
    total_min = ms // 60000
    if total_min < 1:
        return ""
    hours, minutes = divmod(total_min, 60)
    return f"{hours}h{minutes:02d}m" if hours else f"{minutes}m"


def create_progress_bar(percent: float, width: int = 10) -> str:
    percent = max(0.0, min(100.0, percent))
    filled = round((percent / 100) * width)
    if percent > 95:
        color = C.RED
    elif percent > 80:
        color = C.ORANGE
    else:
        color = C.WHITE
    return f"{color}{'█' * filled}{C.GRAY}{'░' * (width - filled)}{C.RESET}"


def truncate(s: str, max_len: int) -> str:
    return s if len(s) <= max_len else s[:max_len - 1] + '…'


def read_payload() -> dict | None:
    """The statusline JSON from stdin; {} for no input, None if unparsable."""
    if sys.stdin is None:
        return {}
    chunks = []
    fd = sys.stdin.fileno()
    while True:
        chunk = os.read(fd, 65536)
        if not chunk:
            break
        chunks.append(chunk)
        try:
            data = json.loads(b"".join(chunks).decode("utf-8", errors="replace"))
            return data if isinstance(data, dict) else None
        except ValueError:
            continue
    if not chunks:
        return {}
    try:
        data = json.loads(b"".join(chunks).decode("utf-8", errors="replace"))
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def record_metrics(data: dict, git_branch: str) -> str:
    """Store this session's metrics in state.json. Returns the session's
    current activity (a tool or pseudo-tool name) for the indicator."""
    model_info = data.get("model") or {}
    cost_info = data.get("cost") or {}
    context = data.get("context_window") or {}
    current_usage = context.get("current_usage") or {}
    workspace = data.get("workspace") or {}
    project_dir = workspace.get("project_dir", "")
    session_id = data.get("session_id") or ""

    # `or 0` guards: fields can be present-but-null before the first response.
    # total_input/output_tokens describe the CURRENT context, not session totals.
    metrics = {
        "model": model_info.get("display_name") or "",
        "model_id": model_info.get("id") or "",
        "tokens": {
            "input": context.get("total_input_tokens") or 0,
            "output": context.get("total_output_tokens") or 0,
            "cache_read": current_usage.get("cache_read_input_tokens") or 0,
            "cache_write": current_usage.get("cache_creation_input_tokens") or 0,
            "cost": cost_info.get("total_cost_usd") or 0.0,
        },
        "lines_added": cost_info.get("total_lines_added") or 0,
        "lines_removed": cost_info.get("total_lines_removed") or 0,
        "context_pct": context.get("used_percentage") or 0,
        "context_size": context.get("context_window_size") or 200000,
        "agent_name": (data.get("agent") or {}).get("name") or "",
    }
    repo_url = repo_url_from_workspace(workspace.get("repo"))

    try:
        with StateLock(timeout=LOCK_TIMEOUT):
            state = read_state_unlocked()
            if not state.get("session_start"):
                return ""  # no session registered by the hooks
            activity = (state.get("activity") or {}).get(session_id) or state.get("tool", "")

            # Legacy flat keys (read by 1.0.0 daemons and as a fallback)
            updates = dict(metrics)
            updates["duration_ms"] = cost_info.get("total_duration_ms") or 0
            if project_dir and state.get("project_path") != project_dir:
                # The shown project changed: a stale button URL is worse than none
                updates["project"] = Path(project_dir).name
                updates["project_path"] = project_dir
                updates["repo_url"] = repo_url or repo_web_url(read_origin_url(project_dir))
            if git_branch:
                updates["git_branch"] = git_branch

            by_session = state.get("metrics") if isinstance(state.get("metrics"), dict) else {}
            session_metrics = dict(metrics, repo_url=repo_url) if repo_url else dict(metrics)

            # Write only on change, plus a heartbeat: this runs several times
            # a second, and each write holds the lock the daemon also needs.
            # duration_ms advances every render, so it is not a change.
            changed = (any(state.get(k) != v for k, v in updates.items() if k != "duration_ms")
                       or (session_id and by_session.get(session_id) != session_metrics))
            now = time.time()
            if changed or now - state.get("statusline_update", 0) >= HEARTBEAT:
                state.update(updates)
                if session_id:
                    by_session[session_id] = session_metrics
                    state["metrics"] = by_session
                state["statusline_update"] = int(now)
                write_state_unlocked(state)
            return activity
    except (OSError, TimeoutError) as e:
        print(f"[statusline] Warning: Could not update state: {e}", file=sys.stderr)
        return ""


def main():
    arm_watchdog(DEADLINE)
    try:
        data = read_payload()
    except OSError as e:
        print(f"[statusline] Error reading input: {e}", file=sys.stderr)
        data = None
    if data is None:
        print(f"{C.RED}[statusline error]{C.RESET}")
        return
    if not data:
        print("")
        return

    workspace = data.get("workspace") or {}
    git_branch = read_branch(workspace.get("current_dir") or os.getcwd())
    activity = record_metrics(data, git_branch)

    model = (data.get("model") or {}).get("display_name") or ""
    cost_info = data.get("cost") or {}
    context = data.get("context_window") or {}
    cost = cost_info.get("total_cost_usd") or 0.0
    duration_ms = cost_info.get("total_duration_ms") or 0
    used_percent = context.get("used_percentage") or 0.0
    context_tokens = (context.get("total_input_tokens") or 0) + (context.get("total_output_tokens") or 0)
    five_hour_pct = ((data.get("rate_limits") or {}).get("five_hour") or {}).get("used_percentage") or 0

    parts = []
    if model:
        parts.append(f"{C.BLUE}{C.BOLD}{model}{C.RESET}")
    label = activity_label(activity)
    if label and label != "Working":
        parts.append(f"{C.ORANGE}⚡ {'MCP' if activity.startswith('mcp__') else label}{C.RESET}")
    percent = round(max(0.0, min(100.0, used_percent)))
    parts.append(f"{create_progress_bar(used_percent)} {C.WHITE}{percent}%{C.RESET}")
    if context_tokens > 0:
        parts.append(f"{C.WHITE}{format_tokens(context_tokens)} ctx{C.RESET}")
    if cost > 0:
        parts.append(f"{C.GREEN}{format_cost(cost)}{C.RESET}")
    duration = format_duration(duration_ms)
    if duration:
        parts.append(f"{C.GRAY}{duration}{C.RESET}")
    if five_hour_pct >= 80:
        color = C.RED if five_hour_pct >= 95 else C.ORANGE
        parts.append(f"{color}5h {round(five_hour_pct)}%{C.RESET}")
    if git_branch:
        parts.append(f"{C.GRAY}{truncate(git_branch, 16)}{C.RESET}")

    print(f"{C.GRAY}  ›  {C.RESET}".join(parts))


if __name__ == "__main__":
    main()
