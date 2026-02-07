#!/usr/bin/env python3
"""
Discord Rich Presence for Claude Code
Manages Discord RPC connection and updates presence based on Claude Code activity.
"""

import copy
import sys
import os
import json
import re
import subprocess
import time
import atexit
import signal
from pathlib import Path
from datetime import datetime

# Shared state management (provides process-safe file locking)
from state import (
    DATA_DIR,
    STATE_FILE,
    StateLock,
    read_state,
    write_state,
    update_state,
    clear_state,
    read_state_unlocked,
    write_state_unlocked,
    format_tokens,
)

# Optional YAML support for config file
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Track if YAML warning has been logged (always defined at module level)
_yaml_warning_logged = False

# Discord Application ID
DISCORD_APP_ID = "1330919293709324449"

# Data files (DATA_DIR imported from state module)
PID_FILE = DATA_DIR / "daemon.pid"
LOG_FILE = DATA_DIR / "daemon.log"
SESSIONS_FILE = DATA_DIR / "sessions.json"  # Tracks active session PIDs

# Orphan check interval (seconds) - how often daemon checks for dead sessions
ORPHAN_CHECK_INTERVAL = 30

# Tool to display name mapping (keep short for Discord limit)
## Keep in sync with PreToolUse matcher in hooks/hooks.json
TOOL_DISPLAY = {
    # File operations
    "Edit": "Editing",
    "Write": "Writing",
    "Read": "Reading",
    "Glob": "Searching",
    "Grep": "Grepping",
    "LS": "Browsing",
    # Execution
    "Bash": "Running",
    "Task": "Delegating",
    # Web
    "WebFetch": "Fetching",
    "WebSearch": "Researching",
    # Notebook
    "NotebookEdit": "Editing",
    "NotebookRead": "Reading",
    # Interaction
    "AskUserQuestion": "Asking",
    "TodoRead": "Reviewing",
    "TodoWrite": "Planning",
}

# Default idle timeout - used as fallback when config cannot be loaded
IDLE_TIMEOUT = 5 * 60  # 5 minutes

# Configuration
CONFIG_FILE_NAME = "config.yaml"
DEFAULT_CONFIG = {
    "discord_app_id": None,  # Uses DISCORD_APP_ID constant if None
    "display": {
        "show_tokens": True,
        "show_cost": True,
        "show_model": True,
        "show_branch": True,
        "show_file": False,  # Disabled by default - requires parsing tool_input on each hook call
    },
    "idle_timeout": 300,  # 5 minutes in seconds
}
CONFIG_RELOAD_INTERVAL = 30  # Reload config every 30 seconds

# Discord connection retry limit (12 retries * 5 seconds = 1 minute before giving up)
DISCORD_CONNECT_MAX_RETRIES = 12

# Tools that operate on files (for filename display)
FILE_TOOLS = {"Edit", "Write", "Read", "NotebookEdit", "NotebookRead"}


_log_to_file_failed = False


def log(message: str):
    """Append message to log file, with stderr fallback on failure."""
    global _log_to_file_failed
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
        return  # Success
    except OSError as e:
        # File logging failed - fall back to stderr
        if not _log_to_file_failed:
            _log_to_file_failed = True
            print(f"[presence] Warning: Log file unavailable ({e}), falling back to stderr", file=sys.stderr)

    # Fallback: write to stderr so diagnostics aren't completely lost
    try:
        print(f"[presence] {formatted}", file=sys.stderr)
    except Exception:
        pass  # Last resort - don't crash if even stderr fails


def get_plugin_root() -> Path | None:
    """Get plugin root directory from CLAUDE_PLUGIN_ROOT environment variable."""
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if plugin_root:
        path = Path(plugin_root)
        if path.exists():
            return path
    return None


def load_config() -> dict:
    """Load configuration from YAML file, falling back to defaults.

    Config location: {CLAUDE_PLUGIN_ROOT}/.claude-plugin/config.yaml

    Returns merged config with defaults for any missing keys.
    """
    global _yaml_warning_logged

    config = DEFAULT_CONFIG.copy()
    config["display"] = DEFAULT_CONFIG["display"].copy()

    plugin_root = get_plugin_root()

    # Warn if config.yaml exists but PyYAML is not installed
    if not YAML_AVAILABLE:
        if plugin_root:
            config_path = plugin_root / ".claude-plugin" / CONFIG_FILE_NAME
            if config_path.exists() and not _yaml_warning_logged:
                log(f"Warning: PyYAML not installed - config.yaml is being IGNORED. Install with: pip install pyyaml")
                _yaml_warning_logged = True
        return config

    if not plugin_root:
        return config

    config_path = plugin_root / ".claude-plugin" / CONFIG_FILE_NAME
    if not config_path.exists():
        return config

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}

        # Merge discord_app_id (validate 17-19 digit numeric string)
        if "discord_app_id" in user_config and user_config["discord_app_id"]:
            app_id = str(user_config["discord_app_id"])
            if app_id.isdigit() and 17 <= len(app_id) <= 19:
                config["discord_app_id"] = app_id
            else:
                log(f"Warning: Invalid discord_app_id format '{app_id}', using default")

        # Merge display toggles
        if "display" in user_config and isinstance(user_config["display"], dict):
            for key in config["display"]:
                if key in user_config["display"]:
                    config["display"][key] = bool(user_config["display"][key])

        # Merge idle_timeout (1 second to 24 hours)
        if "idle_timeout" in user_config:
            timeout = user_config["idle_timeout"]
            if isinstance(timeout, (int, float)) and 0 < timeout <= 86400:
                config["idle_timeout"] = int(timeout)
            else:
                log(f"Warning: idle_timeout must be 1-86400 seconds, got '{timeout}', using default")

        log(f"Loaded config from {config_path}")

    except yaml.YAMLError as e:
        log(f"Error parsing config YAML: {e}")
    except OSError as e:
        log(f"Error reading config file: {e}")

    return config


# Global config cache for daemon
_config_cache = None
_config_last_load = 0


def get_config(force_reload: bool = False) -> dict:
    """Get cached config, reloading periodically for hot-reload support.

    Returns a deep copy of the cached config to prevent accidental mutation.
    """
    global _config_cache, _config_last_load

    now = time.time()
    if force_reload or _config_cache is None or (now - _config_last_load > CONFIG_RELOAD_INTERVAL):
        _config_cache = load_config()
        _config_last_load = now

    return copy.deepcopy(_config_cache)


def extract_file_from_tool_input(hook_input: dict) -> str:
    """Extract filename from hook input's tool_input field.

    For Edit/Write/Read tools, tool_input contains:
    {
        "file_path": "/path/to/file.py",
        ...
    }

    For NotebookEdit/NotebookRead tools, tool_input contains:
    {
        "notebook_path": "/path/to/notebook.ipynb",
        ...
    }

    Returns just the filename (not full path), or empty string if not available.
    """
    tool_name = hook_input.get("tool_name", "")
    if tool_name not in FILE_TOOLS:
        return ""

    tool_input = hook_input.get("tool_input")
    if not isinstance(tool_input, dict):
        return ""

    # Check file_path (Edit/Write/Read) or notebook_path (NotebookEdit/NotebookRead)
    file_path = tool_input.get("file_path", "") or tool_input.get("notebook_path", "")
    if not file_path:
        return ""

    try:
        return Path(file_path).name
    except (ValueError, OSError, TypeError) as e:
        log(f"Warning: Could not extract filename from '{file_path}': {e}")
        return ""


def truncate_filename(filename: str, max_length: int = 25) -> str:
    """Truncate filename for Discord display limits.

    If filename exceeds max_length, keeps the start and end of the stem with '...'
    in the middle, preserving the file extension.

    Example: 'very_long_component_name.tsx' (28 chars) -> 'very_long...t_name.tsx' (22 chars)
    """
    if len(filename) <= max_length:
        return filename

    stem = Path(filename).stem
    suffix = Path(filename).suffix

    # Calculate how much of stem we can keep
    available = max_length - len(suffix) - 3  # 3 for '...'
    if available < 5:
        # Very long extension, just truncate from end
        return filename[:max_length - 3] + "..."

    # Keep start and end of stem
    half = available // 2
    return stem[:half] + "..." + stem[-half:] + suffix


# Note: read_state, write_state, update_state, clear_state are imported from state module
# which provides process-safe file locking to prevent race conditions


def get_daemon_pid() -> int | None:
    """Get PID of running daemon, or None if not running."""
    if not PID_FILE.exists():
        return None
    try:
        pid_content = PID_FILE.read_text().strip()
        pid = int(pid_content)
        # Check if process is actually running
        if sys.platform == "win32":
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True, text=True
            )
            if str(pid) in result.stdout:
                return pid
        else:
            os.kill(pid, 0)  # Doesn't kill, just checks
            return pid
    except ValueError as e:
        log(f"Warning: Corrupt PID file content '{pid_content}', removing: {e}")
        try:
            PID_FILE.unlink()
        except OSError:
            pass
    except ProcessLookupError:
        pass  # Process not running - normal case
    except (PermissionError, OSError) as e:
        log(f"Warning: Could not check daemon PID: {e}")
    return None


def write_pid():
    """Write current PID to file."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(os.getpid()))
    except OSError as e:
        log(f"Warning: Could not write PID file: {e}")


def remove_pid():
    """Remove PID file."""
    try:
        PID_FILE.unlink()
    except FileNotFoundError:
        pass  # Already gone, no problem
    except OSError as e:
        log(f"Warning: Could not remove PID file: {e}")


def get_project_name(project_path: str = "") -> str:
    """Get project name from git remote origin or folder name.

    Priority:
    1. Git remote origin repo name (e.g., 'my-repo' from github.com/user/my-repo.git)
    2. Folder name as fallback
    """
    if not project_path:
        project_path = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

    folder_name = Path(project_path).name

    # Try to get git remote origin URL
    try:
        result = subprocess.run(
            ["git", "-C", project_path, "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            # Parse repo name from URL
            # Handles: https://github.com/user/repo.git, git@github.com:user/repo.git
            match = re.search(r'[/:]([^/:]+?)(?:\.git)?$', remote_url)
            if match:
                return match.group(1)
    except subprocess.TimeoutExpired:
        log(f"Git command timed out for {project_path}")
    except FileNotFoundError:
        pass  # git not installed
    except OSError as e:
        log(f"Error running git: {e}")

    return folder_name


def get_git_branch(project_path: str) -> str:
    """Get current git branch name."""
    if not project_path:
        return ""
    try:
        result = subprocess.run(
            ["git", "-C", project_path, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except subprocess.TimeoutExpired:
        log(f"Git branch command timed out for {project_path}")
    except FileNotFoundError:
        pass  # git not installed
    except OSError as e:
        log(f"Error getting git branch: {e}")
    return ""


def is_process_alive(pid: int) -> bool:
    """Check if a process with given PID is still running."""
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        handle = kernel32.OpenProcess(0x1000, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return True
        # Check why OpenProcess failed
        error = ctypes.get_last_error()
        # ERROR_ACCESS_DENIED (5) means process exists but we can't access it
        if error == 5:
            return True
        return False
    else:
        try:
            os.kill(pid, 0)  # Doesn't kill, just checks
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True  # Process exists but we lack permission


def get_claude_ancestor_pid() -> int | None:
    """Find the Claude Code (node) process in our ancestor chain."""
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        # Get process info via Windows API
        CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
        Process32First = ctypes.windll.kernel32.Process32First
        Process32Next = ctypes.windll.kernel32.Process32Next
        CloseHandle = ctypes.windll.kernel32.CloseHandle

        TH32CS_SNAPPROCESS = 0x00000002
        INVALID_HANDLE_VALUE = -1

        class PROCESSENTRY32(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", ctypes.c_void_p),  # ULONG_PTR
                ("th32ModuleID", wintypes.DWORD),
                ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", ctypes.c_long),
                ("dwFlags", wintypes.DWORD),
                ("szExeFile", ctypes.c_char * 260),
            ]

        # Build a map of pid -> (parent_pid, exe_name)
        snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snapshot == INVALID_HANDLE_VALUE:
            return None

        process_map = {}
        try:
            pe32 = PROCESSENTRY32()
            pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)

            if Process32First(snapshot, ctypes.byref(pe32)):
                while True:
                    pid = pe32.th32ProcessID
                    ppid = pe32.th32ParentProcessID
                    exe = pe32.szExeFile.decode("utf-8", errors="ignore").lower()
                    process_map[pid] = (ppid, exe)
                    if not Process32Next(snapshot, ctypes.byref(pe32)):
                        break
        finally:
            CloseHandle(snapshot)

        # Walk up the tree from current process looking for node.exe (Claude Code)
        current_pid = os.getpid()
        visited = set()
        while current_pid in process_map and current_pid not in visited:
            visited.add(current_pid)
            ppid, exe = process_map[current_pid]
            if "node" in exe or "claude" in exe:
                return current_pid
            current_pid = ppid

        return None
    else:
        # Unix: walk up using /proc
        current_pid = os.getpid()
        visited = set()
        while current_pid > 1 and current_pid not in visited:
            visited.add(current_pid)
            try:
                with open(f"/proc/{current_pid}/comm", "r") as f:
                    comm = f.read().strip().lower()
                if "node" in comm or "claude" in comm:
                    return current_pid
                with open(f"/proc/{current_pid}/stat", "r") as f:
                    stat = f.read()
                    ppid = int(stat.split()[3])
                    current_pid = ppid
            except (OSError, ValueError, IndexError):
                break
        return None


def get_session_pid() -> int:
    """Get Claude ancestor PID, falling back to parent PID."""
    pid = get_claude_ancestor_pid()
    if pid:
        return pid
    fallback = os.getppid()
    log(f"Warning: Could not find Claude ancestor, using parent PID {fallback}")
    return fallback


def read_sessions() -> dict:
    """Read active sessions {pid: timestamp}."""
    if SESSIONS_FILE.exists():
        try:
            return json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
            log(f"Warning: Could not read sessions file: {e}")
    return {}


def write_sessions(sessions: dict):
    """Write active sessions to file."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        log(f"Warning: Could not create data directory: {e}")
        return
    if not sessions:
        try:
            SESSIONS_FILE.unlink()
        except FileNotFoundError:
            pass  # Already gone, no problem
        except OSError as e:
            log(f"Warning: Could not remove sessions file: {e}")
    else:
        try:
            SESSIONS_FILE.write_text(json.dumps(sessions), encoding="utf-8")
        except OSError as e:
            log(f"Warning: Could not write sessions: {e}")


def add_session(pid: int):
    """Register a new session by its parent PID."""
    sessions = read_sessions()
    sessions[str(pid)] = int(time.time())
    write_sessions(sessions)
    return len(sessions)


def remove_session(pid: int):
    """Unregister a session by its parent PID."""
    sessions = read_sessions()
    sessions.pop(str(pid), None)
    write_sessions(sessions)
    return len(sessions)


def cleanup_dead_sessions() -> int:
    """Remove sessions whose parent PIDs are no longer alive. Returns remaining count."""
    sessions = read_sessions()
    if not sessions:
        return 0

    alive_sessions = {}
    for pid_str, timestamp in sessions.items():
        try:
            pid = int(pid_str)
        except ValueError:
            log(f"Invalid PID in sessions file: {pid_str}, removing")
            continue
        if is_process_alive(pid):
            alive_sessions[pid_str] = timestamp
        else:
            log(f"Session PID {pid} is dead, removing")

    if len(alive_sessions) != len(sessions):
        write_sessions(alive_sessions)

    return len(alive_sessions)


def read_hook_input() -> dict:
    """Read JSON input from stdin (provided by Claude Code hooks)."""
    try:
        if not sys.stdin.isatty():
            data = sys.stdin.read()
            if data.strip():
                return json.loads(data)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        log(f"Warning: Could not parse hook input: {e}")
    return {}


def run_daemon():
    """Run the Discord RPC daemon loop."""
    from pypresence import Presence

    log("Daemon starting...")
    write_pid()
    atexit.register(remove_pid)

    # Log YAML availability on startup for easier debugging
    if not YAML_AVAILABLE:
        log("Info: PyYAML not installed - config.yaml support disabled. Install with: pip install pyyaml")

    # Load initial config
    config = get_config(force_reload=True)
    app_id = config.get("discord_app_id") or DISCORD_APP_ID
    log(f"Using Discord App ID: {app_id}")

    # Handle graceful shutdown
    def shutdown(signum, frame):
        log("Received shutdown signal")
        remove_pid()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    # Connect to Discord
    rpc = None
    connected = False
    current_app_id = app_id
    last_sent = {}  # Track last sent state to avoid redundant updates
    last_orphan_check = 0  # Track when we last checked for dead sessions
    discord_connect_attempts = 0  # Track connection retry attempts
    consecutive_errors = 0  # Track consecutive loop errors for circuit breaker
    MAX_CONSECUTIVE_ERRORS = 10  # Exit after this many consecutive failures

    while True:
        try:
            # Periodically reload config for hot-reload support
            config = get_config()
            new_app_id = config.get("discord_app_id") or DISCORD_APP_ID

            # Check if app ID changed - need to reconnect
            if new_app_id != current_app_id and connected:
                log(f"App ID changed from {current_app_id} to {new_app_id}, reconnecting...")
                try:
                    rpc.clear()
                    rpc.close()
                except (ConnectionError, ConnectionResetError, BrokenPipeError,
                        TimeoutError, OSError) as e:
                    log(f"Warning: Error during RPC disconnect before reconnect: {e}")
                connected = False
                rpc = None
                current_app_id = new_app_id

            # Periodically check for dead sessions (orphan cleanup)
            now = time.time()
            if now - last_orphan_check > ORPHAN_CHECK_INTERVAL:
                last_orphan_check = now
                active_count = cleanup_dead_sessions()
                if active_count == 0:
                    log("No active sessions remaining, daemon exiting")
                    break

            # Try to connect if not connected
            if not connected:
                discord_connect_attempts += 1
                if discord_connect_attempts > DISCORD_CONNECT_MAX_RETRIES:
                    log(f"ERROR: Cannot connect to Discord after {DISCORD_CONNECT_MAX_RETRIES} attempts. Is Discord running?")
                    break
                try:
                    rpc = Presence(current_app_id)
                    rpc.connect()
                    connected = True
                    discord_connect_attempts = 0  # Reset on successful connection
                    log(f"Connected to Discord with App ID: {current_app_id}")
                except (ConnectionError, ConnectionRefusedError, ConnectionResetError,
                        BrokenPipeError, TimeoutError, OSError) as e:
                    # Expected connection failures - retry
                    log(f"Failed to connect to Discord (attempt {discord_connect_attempts}/{DISCORD_CONNECT_MAX_RETRIES}): {e}")
                    time.sleep(5)
                    continue
                except Exception as e:
                    # Unexpected error (likely a bug) - fail fast with traceback
                    import traceback
                    log(f"FATAL: Unexpected error connecting to Discord: {e}\n{traceback.format_exc()}")
                    break

            # Read current state (pass logger for error visibility)
            state = read_state(log)

            if not state:
                time.sleep(1)
                continue

            # Get display settings from config
            display_cfg = config.get("display", {})
            show_tokens = display_cfg.get("show_tokens", True)
            show_cost = display_cfg.get("show_cost", True)
            show_model = display_cfg.get("show_model", True)
            show_branch = display_cfg.get("show_branch", True)
            show_file = display_cfg.get("show_file", False)

            # Check for idle timeout - show "Idling" instead of clearing
            last_update = state.get("last_update", 0)
            idle_timeout = config.get("idle_timeout", IDLE_TIMEOUT)
            is_idle = time.time() - last_update > idle_timeout

            # Get state values
            tool = state.get("tool", "")
            project = state.get("project", "Claude Code")
            git_branch = state.get("git_branch", "") if show_branch else ""
            model = state.get("model", "") if show_model else ""
            current_file = state.get("file", "") if show_file else ""
            session_start = state.get("session_start", int(time.time()))

            # Get token data (only if needed for display)
            tokens = state.get("tokens", {})
            input_tokens = tokens.get("input", 0)
            output_tokens = tokens.get("output", 0)
            cache_read = tokens.get("cache_read", 0)
            cache_write = tokens.get("cache_write", 0)
            cost = tokens.get("cost", 0.0)
            simple_cost = tokens.get("simple_cost", 0.0)

            # Determine activity - show "Idling" if idle timeout reached
            if is_idle:
                activity = "Idling"
            elif tool in TOOL_DISPLAY:
                activity = TOOL_DISPLAY[tool]
            elif tool.startswith("mcp__"):
                activity = "Using MCP"
            else:
                activity = "Working"
                log(f"Unmapped tool '{tool}', showing generic activity")

            # Only show file for non-idle file operations
            display_file = current_file if not is_idle and tool in FILE_TOOLS else ""

            # Build activity string with optional filename
            if display_file:  # show_file already checked when setting display_file
                truncated_file = truncate_filename(display_file)
                activity_str = f"{activity} {truncated_file}"
            else:
                activity_str = activity

            # Build details line: "Activity [file] on project [(branch)]"
            if git_branch:
                details = f"{activity_str} on {project} ({git_branch})"
            else:
                details = f"{activity_str} on {project}"

            # Truncate details if too long for Discord (max ~128 chars)
            if len(details) > 120:
                if git_branch:
                    details = f"{activity_str} on {project}"
                if len(details) > 120:
                    max_proj = 120 - len(activity_str) - 4
                    details = f"{activity_str} on {project[:max(10, max_proj)]}..."

            # Cycle display between two views every 8 seconds:
            # - Simple (5s): input + output tokens, cost without cache consideration
            # - Cached (3s): total tokens including cache reads/writes
            cycle_pos = int(time.time()) % 8
            show_simple = cycle_pos < 5

            simple_tokens = input_tokens + output_tokens
            cached_tokens = input_tokens + output_tokens + cache_read + cache_write

            # Build state line with config toggles
            parts = []

            if show_model and model:
                parts.append(model)

            if show_tokens:
                if show_simple:
                    parts.append(f"{format_tokens(simple_tokens)} tokens")
                else:
                    parts.append(f"{format_tokens(cached_tokens)} cached")

            if show_cost:
                if show_simple:
                    parts.append(f"${simple_cost:.2f}")
                else:
                    parts.append(f"${cost:.2f}")

            state_line = " \u2022 ".join(parts) if parts else "Claude Code"

            # Only update if something changed (check every cycle)
            current = {"details": details, "state_line": state_line}
            if current != last_sent:
                log(f"Sending to Discord: {details} | {state_line}")
                try:
                    rpc.update(
                        details=details,
                        state=state_line,
                        start=session_start,
                        large_image="claude",
                        large_text="Claude Code",
                    )
                    last_sent = current
                except (ConnectionError, ConnectionResetError, BrokenPipeError,
                        TimeoutError, OSError) as e:
                    # Connection lost - will reconnect on next iteration
                    log(f"Failed to update presence (connection lost): {e}")
                    connected = False
                    rpc = None
                except Exception as e:
                    # Unexpected error (likely a bug in payload construction)
                    import traceback
                    log(f"Failed to update presence (unexpected): {e}\n{traceback.format_exc()}")
                    # Don't disconnect - this might be a transient data issue
                    # Continue to next iteration to try again with fresh state

            time.sleep(1)

        except KeyboardInterrupt:
            break
        except SystemExit:
            raise  # Allow intentional exits to propagate
        except (OSError, IOError, ConnectionError, BrokenPipeError) as e:
            # Expected transient errors - log and continue with circuit breaker
            consecutive_errors += 1
            log(f"Daemon error (recoverable, {consecutive_errors}/{MAX_CONSECUTIVE_ERRORS}): {e}")
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                log(f"ERROR: Too many consecutive errors ({consecutive_errors}), daemon exiting")
                break
            time.sleep(5)
        except Exception as e:
            # Unexpected errors (programming bugs) - log and exit to avoid infinite loop
            import traceback
            log(f"Daemon error (FATAL unexpected): {e}\n{traceback.format_exc()}")
            break  # Exit on programming errors rather than infinite retry loop
        else:
            # Reset error counter on successful iteration
            consecutive_errors = 0

    # Cleanup
    if rpc:
        try:
            rpc.clear()
            rpc.close()
        except Exception as e:
            log(f"Warning: Error during RPC cleanup on shutdown: {e}")
    log("Daemon stopped")


def cmd_start():
    """Handle 'start' command - spawn daemon if needed, update state."""
    hook_input = read_hook_input()
    project = hook_input.get("cwd", os.environ.get("CLAUDE_PROJECT_DIR", ""))
    project_name = get_project_name(project) if project else get_project_name()

    # Register this session by Claude Code's PID
    claude_pid = get_session_pid()
    session_count = add_session(claude_pid)

    # Update state with file locking to prevent race conditions
    now = int(time.time())
    git_branch = get_git_branch(project) if project else ""
    session_id = hook_input.get("session_id", "")

    try:
        with StateLock():
            state = read_state_unlocked()

            # Reset session_start if this is the first/only session (timer starts fresh)
            if session_count == 1:
                state["session_start"] = now

            state["project"] = project_name
            state["project_path"] = project
            state["git_branch"] = git_branch
            state["last_update"] = now
            state["tool"] = ""
            state["session_id"] = session_id
            # Note: model and tokens are populated by statusline.py

            write_state_unlocked(state)
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not write session state: {e}")
        print(f"[presence] Warning: Could not write session state: {e}", file=sys.stderr)

    log(f"Session started for PID {claude_pid} (active sessions: {session_count})")

    # Check if daemon is running
    if get_daemon_pid():
        log("Daemon already running")
        return

    # Spawn daemon in background
    log(f"Starting daemon for project: {project_name}")

    if sys.platform == "win32":
        # Use pythonw if available for windowless execution
        python_exe = sys.executable
        script_path = Path(__file__).resolve()

        try:
            proc = subprocess.Popen(
                [python_exe, str(script_path), "daemon"],
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log(f"Spawned daemon subprocess (PID {proc.pid})")
        except OSError as e:
            log(f"Failed to spawn daemon: {e}")
    else:
        # Unix: fork and detach
        try:
            pid = os.fork()
        except OSError as e:
            log(f"Failed to fork daemon: {e}")
            return
        if pid == 0:
            # Child process
            os.setsid()
            try:
                sys.stdin.close()
                sys.stdout.close()
                sys.stderr.close()
            except (OSError, ValueError):
                pass
            run_daemon()
            sys.exit(0)


def cmd_update():
    """Handle 'update' command - update current activity."""
    hook_input = read_hook_input()
    tool_name = hook_input.get("tool_name", "")

    # Extract filename outside lock to minimize lock time
    config = get_config()
    show_file = config.get("display", {}).get("show_file", False)
    filename = ""
    if show_file:
        filename = extract_file_from_tool_input(hook_input)

    # Update state with file locking to prevent race conditions
    try:
        with StateLock():
            state = read_state_unlocked()
            if not state:
                # No active session, ignore
                return

            state["tool"] = tool_name
            state["last_update"] = int(time.time())

            if show_file:
                if filename:
                    state["file"] = filename
                elif tool_name not in FILE_TOOLS:
                    state["file"] = ""

            # Note: tokens are updated by statusline.py (no JSONL parsing needed)
            write_state_unlocked(state)
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not update session state: {e}")
        return

    log(f"Updated: {tool_name}" + (f" ({filename})" if filename else ""))


def cmd_stop():
    """Handle 'stop' command - clear presence and stop daemon."""
    # Unregister this session by Claude Code's PID
    claude_pid = get_session_pid()
    remaining = remove_session(claude_pid)

    if remaining > 0:
        log(f"Session ended for PID {claude_pid} (active sessions: {remaining})")
        return  # Don't stop daemon, other sessions still active

    log("Last session ended, stopping daemon")

    # Clear state (with locking)
    clear_state(log)

    # Kill daemon if running
    pid = get_daemon_pid()
    if pid:
        try:
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                               capture_output=True)
            else:
                os.kill(pid, signal.SIGTERM)
            log(f"Stopped daemon (PID {pid})")
        except (OSError, subprocess.SubprocessError) as e:
            log(f"Failed to stop daemon: {e}")

    remove_pid()


def cmd_status():
    """Handle 'status' command - show current status."""
    pid = get_daemon_pid()
    state = read_state()
    sessions = read_sessions()

    if pid:
        print(f"Daemon running (PID {pid})")
    else:
        print("Daemon not running")

    print(f"Active sessions: {len(sessions)}")
    if sessions:
        for spid, ts in sessions.items():
            alive = "alive" if is_process_alive(int(spid)) else "DEAD"
            print(f"  - PID {spid}: {alive}")

    if state:
        print(f"Project: {state.get('project', 'Unknown')}")
        git_branch = state.get('git_branch', '')
        if git_branch:
            print(f"Branch: {git_branch}")
        model = state.get('model', '')
        if model:
            print(f"Model: {model}")
        print(f"Last tool: {state.get('tool', 'None')}")

        # Show token stats
        tokens = state.get('tokens', {})
        input_t = tokens.get('input', 0)
        output_t = tokens.get('output', 0)
        cache_read = tokens.get('cache_read', 0)
        cache_write = tokens.get('cache_write', 0)
        cost = tokens.get('cost', 0.0)
        simple_cost = tokens.get('simple_cost', 0.0)

        if input_t or output_t or cache_read:
            simple = input_t + output_t
            cached = simple + cache_read + cache_write
            print(f"Tokens (simple): {format_tokens(simple)} ({format_tokens(input_t)} in / {format_tokens(output_t)} out)")
            print(f"Tokens (cached): {format_tokens(cached)} (+{format_tokens(cache_read)} read / +{format_tokens(cache_write)} write)")
            print(f"Cost: ${cost:.2f} (${simple_cost:.2f} without cache)")

        last_update = state.get("last_update", 0)
        if last_update:
            ago = int(time.time() - last_update)
            print(f"Last update: {ago}s ago")
    else:
        print("No active session")


def main():
    if len(sys.argv) < 2:
        print("Usage: presence.py <start|update|stop|status|daemon>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        cmd_start()
    elif command == "update":
        cmd_update()
    elif command == "stop":
        cmd_stop()
    elif command == "status":
        cmd_status()
    elif command == "daemon":
        run_daemon()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
