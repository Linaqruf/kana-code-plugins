#!/usr/bin/env python3
"""
Discord Rich Presence for Claude Code.

Commands:
  start   SessionStart hook: register the session, start the daemon if needed
  update  PreCompact hook: show "Compacting context"
  stop    SessionEnd hook: unregister the session
  status  print daemon, sessions and state (for debugging)
  daemon  the long-running process that talks to Discord

No hook runs per tool call. The daemon reads each session's transcript to
learn the current tool (see activity.py), so a burst of tool calls from
parallel subagents starts no plugin process at all. Each hook command has a
hard deadline (state.arm_watchdog), because Claude Code does not enforce
`timeout` on async hooks.
"""

import copy
import json
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from state import (
    DATA_DIR,
    StateLock,
    arm_watchdog,
    atomic_write_json,
    clear_state,
    format_tokens,
    read_state,
    read_state_unlocked,
    release_lock,
    try_exclusive_lock,
    write_state_unlocked,
)
from activity import (
    DELEGATE_TOOLS,
    FILE_TOOLS,
    PSEUDO_TOOL_DISPLAY,
    TOOL_DISPLAY,
    TranscriptTail,
    activity_label,
    model_display_name,
)
from gitinfo import project_name, read_branch, read_origin_url, repo_web_url

# Keep in sync with .claude-plugin/plugin.json (enforced by a test). The PID
# file records it, so a newer `start` can replace an older daemon.
VERSION = "1.1.0"

DISCORD_APP_ID = "1330919293709324449"

PID_FILE = DATA_DIR / "daemon.pid"          # bare PID: the format 1.0.0 hooks parse
VERSION_FILE = DATA_DIR / "daemon.version"  # "<pid> <version>", 1.1.0 and later
DAEMON_LOCK_FILE = DATA_DIR / "daemon.lock"
LOG_FILE = DATA_DIR / "daemon.log"
SESSIONS_FILE = DATA_DIR / "sessions.json"
SESSIONS_LOCK_FILE = DATA_DIR / "sessions.lock"

# Hook deadlines (seconds). `start` also walks the process tree and may
# spawn the daemon.
HOOK_DEADLINE = 5.0
START_DEADLINE = 8.0
HOOK_LOCK_TIMEOUT = 2.0

# Daemon pacing
POLL_INTERVAL = 1.0          # transcript tail + state read
LIVENESS_INTERVAL = 10       # dead-session pruning
FOCUS_HOLD = 20              # keep the shown session unless it is quiet this long
DISCORD_MIN_INTERVAL = 15    # Discord accepts one presence update per 15 s
DISCORD_RETRY_DELAYS = (15, 30, 60)
DISCORD_HANDSHAKE_TIMEOUT = 10  # pypresence's own handshake read has no timeout
DAEMON_HANG_LIMIT = 120      # loop stalled this long: exit and free the lock
DAEMON_LOCK_WAIT = 15        # a new daemon waits this long for a retiring one
COMPACT_OVERLAY_MAX = 300    # stop showing "Compacting" after this, whatever happens
REPO_CACHE_TTL = 60
LOG_MAX_SIZE = 1_048_576     # 1 MB; rotation keeps the last half
MAX_CONSECUTIVE_ERRORS = 10

IDLE_TIMEOUT = 5 * 60
CONFIG_FILE_NAME = "config.yaml"
CONFIG_RELOAD_INTERVAL = 30
DEFAULT_CONFIG = {
    "discord_app_id": None,  # Uses DISCORD_APP_ID if None
    "display": {
        "show_tokens": True,
        "show_cost": True,
        "show_model": True,
        "show_branch": True,
        "show_file": True,
        "show_lines": True,
        "show_context_warning": True,
        "show_button": True,
    },
    "custom_button_label": "",  # max 31 chars (Discord limit)
    "custom_button_url": "",    # http(s), max 512 chars
    "idle_timeout": 300,
}

# Discord field limits
DISCORD_TEXT_MAX = 128


# ═══════════════════════════════════════════════════════════════
# Logging
# ═══════════════════════════════════════════════════════════════

_log_to_file_failed = False


def log(message: str):
    """Append message to the log file, with stderr fallback on failure."""
    global _log_to_file_failed
    formatted = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
        return
    except OSError as e:
        if not _log_to_file_failed:
            _log_to_file_failed = True
            print(f"[presence] Warning: Log file unavailable ({e}), falling back to stderr", file=sys.stderr)
    try:
        print(f"[presence] {formatted}", file=sys.stderr)
    except (OSError, ValueError, TypeError):
        pass


def _rotate_log():
    """Keep the log under LOG_MAX_SIZE by dropping its older half."""
    try:
        if LOG_FILE.exists() and LOG_FILE.stat().st_size > LOG_MAX_SIZE:
            content = LOG_FILE.read_bytes()
            cut = len(content) - LOG_MAX_SIZE // 2
            newline = content.find(b"\n", cut)
            if newline != -1:
                cut = newline + 1
            LOG_FILE.write_bytes(content[cut:])
            log("Log file rotated (exceeded 1MB)")
    except OSError:
        pass


def _sweep_stale_tmp_files():
    """Remove atomic-write temp files (tmp*.tmp) older than 1 hour.

    A process killed between mkstemp and os.replace leaks one. The age guard
    avoids racing a write in flight.
    """
    try:
        cutoff = time.time() - 3600
        for tmp in DATA_DIR.glob("tmp*.tmp"):
            try:
                if tmp.stat().st_mtime < cutoff:
                    tmp.unlink()
                    log(f"Removed stale temp file: {tmp.name}")
            except OSError:
                pass
    except OSError:
        pass


# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

_yaml_warning_logged = False


def get_plugin_root() -> Path | None:
    """Plugin root from CLAUDE_PLUGIN_ROOT, else the directory above scripts/."""
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if root and Path(root).exists():
        return Path(root)
    return Path(__file__).resolve().parent.parent


def load_config() -> dict:
    """Load {plugin root}/.claude-plugin/config.yaml over the defaults."""
    global _yaml_warning_logged
    config = copy.deepcopy(DEFAULT_CONFIG)
    config_path = get_plugin_root() / ".claude-plugin" / CONFIG_FILE_NAME
    if not config_path.exists():
        return config
    try:
        import yaml  # optional; imported here so hooks and statusline skip its cost
    except ImportError:
        if not _yaml_warning_logged:
            log("Warning: PyYAML not installed - config.yaml is being IGNORED. Install with: pip install pyyaml")
            _yaml_warning_logged = True
        return config

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        log(f"ERROR: {config_path} has invalid YAML, using all defaults: {e}")
        return config
    except OSError as e:
        log(f"ERROR: Could not read {config_path}: {e}")
        return config
    if not isinstance(user_config, dict):
        log(f"ERROR: {config_path} is not a mapping, using all defaults")
        return config

    app_id = user_config.get("discord_app_id")
    if app_id:
        app_id = str(app_id)
        if app_id.isdigit() and 17 <= len(app_id) <= 19:
            config["discord_app_id"] = app_id
        else:
            log(f"Warning: Invalid discord_app_id format '{app_id}', using default")

    display = user_config.get("display")
    if isinstance(display, dict):
        for key in config["display"]:
            if key in display:
                config["display"][key] = bool(display[key])

    if "idle_timeout" in user_config:
        timeout = user_config["idle_timeout"]
        if isinstance(timeout, (int, float)) and 1 <= timeout <= 86400:
            config["idle_timeout"] = int(timeout)
        else:
            log(f"Warning: idle_timeout must be 1-86400 seconds, got '{timeout}', using default")

    label = user_config.get("custom_button_label")
    if isinstance(label, str) and label.strip():
        config["custom_button_label"] = label.strip()[:31]
    url = user_config.get("custom_button_url")
    if isinstance(url, str) and url.strip():
        url = url.strip()
        if url.startswith(("http://", "https://")) and len(url) <= 512:
            config["custom_button_url"] = url
        else:
            log("Warning: custom_button_url must be http(s) and <=512 chars, ignoring")
    return config


_config_cache = None
_config_last_load = 0.0


def get_config() -> dict:
    """Cached config, reloaded every CONFIG_RELOAD_INTERVAL seconds."""
    global _config_cache, _config_last_load
    now = time.time()
    if _config_cache is None or now - _config_last_load > CONFIG_RELOAD_INTERVAL:
        new_config = load_config()
        if _config_cache is not None and new_config != _config_cache:
            log("Config change detected, applying new settings")
        _config_cache = new_config
        _config_last_load = now
    return copy.deepcopy(_config_cache)


# ═══════════════════════════════════════════════════════════════
# Processes
# ═══════════════════════════════════════════════════════════════

_kernel32_cache = None


def _get_kernel32():
    """kernel32 with typed signatures (ctypes defaults to c_int, which
    truncates 64-bit handles)."""
    global _kernel32_cache
    if _kernel32_cache is not None:
        return _kernel32_cache
    import ctypes
    from ctypes import wintypes

    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.OpenProcess.restype = wintypes.HANDLE
    k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k.GetExitCodeProcess.restype = wintypes.BOOL
    k.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    k.TerminateProcess.restype = wintypes.BOOL
    k.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    k.GetProcessTimes.restype = wintypes.BOOL
    k.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    k.CloseHandle.restype = wintypes.BOOL
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    k.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    _kernel32_cache = k
    return k


def _snapshot_process_map() -> dict | None:
    """Windows: {pid: (parent_pid, exe_name_lower)} for all processes, or None."""
    import ctypes
    from ctypes import wintypes

    kernel32 = _get_kernel32()
    TH32CS_SNAPPROCESS = 0x00000002
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.c_void_p),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", ctypes.c_char * 260),
        ]

    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot == INVALID_HANDLE_VALUE:
        log(f"Warning: CreateToolhelp32Snapshot failed (error {ctypes.get_last_error()})")
        return None
    process_map = {}
    try:
        entry = PROCESSENTRY32()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
        if kernel32.Process32First(snapshot, ctypes.byref(entry)):
            while True:
                exe = entry.szExeFile.decode("utf-8", errors="ignore").lower()
                process_map[entry.th32ProcessID] = (entry.th32ParentProcessID, exe)
                if not kernel32.Process32Next(snapshot, ctypes.byref(entry)):
                    break
    finally:
        kernel32.CloseHandle(snapshot)
    return process_map


def is_process_alive(pid: int) -> bool:
    """True if a process with this PID is running."""
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        kernel32 = _get_kernel32()
        handle = kernel32.OpenProcess(0x1000, False, pid)  # QUERY_LIMITED_INFORMATION
        if not handle:
            if ctypes.get_last_error() == 5:
                # ACCESS_DENIED: exists but not ours; confirm with a snapshot
                process_map = _snapshot_process_map()
                return True if process_map is None else pid in process_map
            return False
        try:
            exit_code = wintypes.DWORD()
            if kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                return exit_code.value == 259  # STILL_ACTIVE
            return False
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _process_name(pid: int) -> str:
    """Lower-case executable name of a process, or '' if unknown."""
    if sys.platform == "win32":
        process_map = _snapshot_process_map() or {}
        return process_map.get(pid, (0, ""))[1]
    try:
        with open(f"/proc/{pid}/comm", "r") as f:
            return f.read().strip().lower()
    except OSError:
        pass
    try:  # macOS: no /proc. Runs only when replacing an old daemon.
        out = subprocess.run(["ps", "-p", str(pid), "-o", "comm="], capture_output=True,
                             text=True, timeout=2)
        return Path(out.stdout.strip()).name.lower()
    except (OSError, subprocess.SubprocessError):
        return ""


def _process_start_time(pid: int) -> float | None:
    """Epoch seconds when a process started, or None if unknown."""
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        kernel32 = _get_kernel32()
        handle = kernel32.OpenProcess(0x1000, False, pid)  # QUERY_LIMITED_INFORMATION
        if not handle:
            return None
        try:
            created, exited, kernel, user = (wintypes.FILETIME() for _ in range(4))
            if not kernel32.GetProcessTimes(handle, ctypes.byref(created), ctypes.byref(exited),
                                            ctypes.byref(kernel), ctypes.byref(user)):
                return None
            ticks = (created.dwHighDateTime << 32) | created.dwLowDateTime  # 100 ns since 1601
            return ticks / 10_000_000 - 11_644_473_600
        finally:
            kernel32.CloseHandle(handle)
    try:
        with open(f"/proc/{pid}/stat", "r") as f:
            start_ticks = int(f.read().rsplit(")", 1)[1].split()[19])
        with open("/proc/stat", "r") as f:
            boot = next(int(line.split()[1]) for line in f if line.startswith("btime "))
        return boot + start_ticks / os.sysconf("SC_CLK_TCK")
    except (OSError, ValueError, IndexError, StopIteration):
        pass
    try:  # macOS: no /proc. Runs only when replacing an old daemon.
        out = subprocess.run(["ps", "-p", str(pid), "-o", "etime="], capture_output=True,
                             text=True, timeout=2)
        elapsed = parse_etime(out.stdout)
        return None if elapsed is None else time.time() - elapsed
    except (OSError, subprocess.SubprocessError):
        return None


def parse_etime(text: str) -> int | None:
    """Seconds from ps's elapsed time, "[[dd-]hh:]mm:ss"; None if unparsable."""
    text = text.strip()
    try:
        days = 0
        if "-" in text:
            day_part, text = text.split("-", 1)
            days = int(day_part)
        fields = [int(f) for f in text.split(":")]
    except ValueError:
        return None
    if not 2 <= len(fields) <= 3:
        return None
    hours, minutes, seconds = ([0] * (3 - len(fields)) + fields)
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds


def terminate_process(pid: int) -> bool:
    """Terminate a process we started earlier (the old daemon)."""
    if sys.platform == "win32":
        kernel32 = _get_kernel32()
        handle = kernel32.OpenProcess(0x0001, False, pid)  # PROCESS_TERMINATE
        if not handle:
            return False
        try:
            return bool(kernel32.TerminateProcess(handle, 0))
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except OSError:
        return False


def get_claude_ancestor_pid() -> int | None:
    """PID of the Claude Code process (node or claude executable) above us."""
    if sys.platform == "win32":
        process_map = _snapshot_process_map()
        if process_map is None:
            return None
        current, visited = os.getpid(), set()
        while current in process_map and current not in visited:
            visited.add(current)
            ppid, exe = process_map[current]
            if "node" in exe or "claude" in exe:
                return current
            current = ppid
        return None
    if os.path.isdir("/proc"):
        current, visited = os.getpid(), set()
        while current > 1 and current not in visited:
            visited.add(current)
            try:
                with open(f"/proc/{current}/comm", "r") as f:
                    comm = f.read().strip().lower()
                if "node" in comm or "claude" in comm:
                    return current
                with open(f"/proc/{current}/stat", "r") as f:
                    # comm may contain spaces; fields after the closing paren
                    current = int(f.read().rsplit(")", 1)[1].split()[1])
            except (OSError, ValueError, IndexError):
                break
        return None
    # macOS and others: `sh -c` execs its single command, so our parent is
    # Claude Code (get_session_pid falls back to it)
    return None


def get_session_pid() -> int:
    """Claude Code's PID, falling back to our parent's."""
    return get_claude_ancestor_pid() or os.getppid()


# ═══════════════════════════════════════════════════════════════
# Sessions
# ═══════════════════════════════════════════════════════════════
# sessions.json maps Claude Code PID -> session record. Version 1.0.0 stored
# an int timestamp as the value; 1.1.0 stores {"ts", "started", "session_id",
# "transcript", "cwd"}. Old readers never look inside the value, and new
# readers accept both (session_record()).

def session_record(value) -> dict:
    """Normalise a sessions.json value (1.0.0 int or 1.1.0 dict)."""
    if isinstance(value, dict):
        return value
    if isinstance(value, (int, float)):
        return {"ts": int(value), "started": int(value)}
    return {}


def _read_sessions_unlocked() -> dict:
    try:
        data = json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        log(f"Warning: Could not read sessions file: {e}")
        return {}


def read_sessions(timeout: float = HOOK_LOCK_TIMEOUT) -> dict | None:
    """{pid_str: record} with locking, or None if the lock is unavailable."""
    try:
        with StateLock(timeout=timeout, lock_file=SESSIONS_LOCK_FILE):
            return _read_sessions_unlocked()
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not read sessions: {e}")
        return None


def register_session(pid: int, hook_input: dict, cwd: str) -> tuple[int, bool]:
    """Add or refresh this Claude Code process's record.

    Returns (session count, whether the PID is new), or (-1, False) on
    failure. SessionStart also fires on /clear, /resume and compaction, which
    refresh an existing record.
    """
    now = int(time.time())
    try:
        with StateLock(timeout=HOOK_LOCK_TIMEOUT, lock_file=SESSIONS_LOCK_FILE):
            # Drop sessions left over from a crash or reboot, so the count
            # (which decides whether state starts fresh) is the live count
            sessions = {k: v for k, v in _read_sessions_unlocked().items()
                        if k == str(pid) or (k.isdigit() and is_process_alive(int(k)))}
            is_new = str(pid) not in sessions
            previous = session_record(sessions.get(str(pid)))
            record = {
                "ts": now,
                "started": previous.get("started", now),
                "session_id": hook_input.get("session_id", "") or previous.get("session_id", ""),
                "transcript": previous.get("transcript", ""),
                "cwd": cwd or previous.get("cwd", ""),
            }
            transcript = hook_input.get("transcript_path") or ""
            if transcript and "subagents" not in Path(transcript).parts:
                record["transcript"] = transcript
            sessions[str(pid)] = record
            atomic_write_json(SESSIONS_FILE, sessions)
            return len(sessions), is_new
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not register session PID {pid}: {e}")
        return -1, False


def unregister_session(pid: int) -> int:
    """Remove this process's record. Returns the remaining count, or -1."""
    try:
        with StateLock(timeout=HOOK_LOCK_TIMEOUT, lock_file=SESSIONS_LOCK_FILE):
            sessions = _read_sessions_unlocked()
            if sessions.pop(str(pid), None) is not None:
                atomic_write_json(SESSIONS_FILE, sessions)
            return len(sessions)
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not unregister session PID {pid}: {e}")
        return -1


def prune_dead_sessions() -> dict | None:
    """Drop sessions whose process has exited. Returns the survivors."""
    try:
        with StateLock(timeout=HOOK_LOCK_TIMEOUT, lock_file=SESSIONS_LOCK_FILE):
            sessions = _read_sessions_unlocked()
            alive = {}
            for pid_str, value in sessions.items():
                try:
                    pid = int(pid_str)
                except ValueError:
                    log(f"Invalid PID in sessions file: {pid_str}, removing")
                    continue
                if is_process_alive(pid):
                    alive[pid_str] = value
                else:
                    log(f"Session PID {pid} is dead, removing")
            if len(alive) != len(sessions):
                atomic_write_json(SESSIONS_FILE, alive)
            return alive
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not prune sessions: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
# Hook input and daemon bookkeeping
# ═══════════════════════════════════════════════════════════════

def read_hook_input() -> dict:
    """Read the hook's JSON from stdin.

    Stops as soon as the bytes read parse as JSON, so a stdin pipe that is
    never closed cannot hold the process. The caller's watchdog bounds the
    worst case.
    """
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return {}
        fd = sys.stdin.fileno()
        chunks = []
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            chunks.append(chunk)
            try:
                data = json.loads(b"".join(chunks).decode("utf-8", errors="replace"))
                return data if isinstance(data, dict) else {}
            except ValueError:
                continue  # incomplete; read more
        if chunks:
            data = json.loads(b"".join(chunks).decode("utf-8", errors="replace"))
            return data if isinstance(data, dict) else {}
    except (ValueError, OSError) as e:
        log(f"Warning: Could not parse hook input: {e}")
    return {}


def read_pid_file() -> tuple[int | None, str | None]:
    """(pid, version) of the recorded daemon. The version is None for a
    daemon older than 1.1.0, which writes no version file."""
    try:
        pid = int(PID_FILE.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None, None
    try:
        fields = VERSION_FILE.read_text(encoding="utf-8").split()
        if len(fields) == 2 and fields[0] == str(pid):
            return pid, fields[1]
    except OSError:
        pass
    return pid, None


def _version_tuple(version: str | None) -> tuple:
    try:
        return tuple(int(p) for p in (version or "0").split("."))
    except ValueError:
        return (0,)


def get_daemon_pid() -> int | None:
    """PID of a running daemon, or None."""
    pid, _ = read_pid_file()
    return pid if pid and is_process_alive(pid) else None


def _stop_legacy_daemon():
    """Stop a pre-1.1.0 daemon, which never exits while any session is alive
    and so would outlive the upgrade indefinitely.

    Only a process that already existed when the PID file was written can be
    that daemon. Checking this keeps a stale PID file (after a reboot or a
    hard kill) from naming some unrelated python process that reused the PID.
    """
    pid, version = read_pid_file()
    if not pid or version is not None or not is_process_alive(pid):
        return
    try:
        written = PID_FILE.stat().st_mtime
    except OSError:
        return
    started = _process_start_time(pid)
    if not _process_name(pid).startswith("python") or started is None or started > written + 2:
        return
    if terminate_process(pid):
        log(f"Stopped pre-1.1.0 daemon (PID {pid})")
    else:
        log(f"Warning: Could not stop pre-1.1.0 daemon PID {pid}")


def ensure_daemon():
    """Start the daemon unless a current one runs.

    `daemon.lock` is the source of truth: a 1.1.0+ daemon holds it for its
    whole life, and the OS drops it when the daemon dies, so stale PID files
    cannot mislead this check.
    """
    probe = try_exclusive_lock(DAEMON_LOCK_FILE)
    if probe is not None:
        release_lock(probe)       # no 1.1.0+ daemon runs
        _stop_legacy_daemon()
    else:
        pid, version = read_pid_file()
        if version is not None and _version_tuple(version) >= _version_tuple(VERSION):
            return                # a current daemon runs
        if version is not None and pid and _process_name(pid).startswith("python"):
            terminate_process(pid)  # an older 1.1.0+ daemon: replace it
            log(f"Stopping older daemon (PID {pid}, version {version})")
        # No version file while the lock is held: the daemon is retiring (it
        # removes its files first). The new daemon waits for the lock.

    command = [sys.executable, str(Path(__file__).resolve()), "daemon"]
    try:
        if sys.platform == "win32":
            flags = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
                     | subprocess.CREATE_NO_WINDOW)
            proc = subprocess.Popen(command, creationflags=flags, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            proc = subprocess.Popen(command, start_new_session=True, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log(f"Spawned daemon (PID {proc.pid})")
    except OSError as e:
        log(f"Failed to spawn daemon: {e}")


# ═══════════════════════════════════════════════════════════════
# Hook commands
# ═══════════════════════════════════════════════════════════════

def cmd_start():
    """SessionStart: register the session, seed state, start the daemon."""
    hook_input = read_hook_input()
    if hook_input.get("agent_id"):
        # A subagent is part of its parent's session, not a new one. (Agent
        # tool subagents did not fire SessionStart on 2.1.283; this guards
        # other kinds.)
        return
    cwd = hook_input.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    claude_pid = get_session_pid()
    count, is_new = register_session(claude_pid, hook_input, cwd)
    if count == -1:
        return

    # Seed the legacy flat state keys. The statusline only writes metrics
    # while `session_start` is set, and a 1.0.0 daemon still reads these.
    # Only the first session of a fresh start resets the state.
    fresh = count == 1 and is_new
    remote = read_origin_url(cwd)
    try:
        with StateLock(timeout=HOOK_LOCK_TIMEOUT):
            state = {} if fresh else read_state_unlocked()
            if fresh or not state.get("project"):
                state.update({
                    "session_start": int(time.time()),
                    "project": project_name(cwd, remote),
                    "project_path": cwd,
                    "git_branch": read_branch(cwd),
                    "repo_url": repo_web_url(remote),
                    "tool": "",
                })
            state["last_update"] = int(time.time())
            state["session_id"] = hook_input.get("session_id", "")
            write_state_unlocked(state)
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not seed session state: {e}")

    log(f"Session started for PID {claude_pid} (active sessions: {count})")
    ensure_daemon()


def cmd_update():
    """PreCompact: mark the session as compacting. The transcript cannot show
    this: nothing is written to it until compaction ends."""
    hook_input = read_hook_input()
    if hook_input.get("hook_event_name") != "PreCompact":
        return
    session_id = hook_input.get("session_id") or ""
    if not session_id:
        return
    try:
        with StateLock(timeout=HOOK_LOCK_TIMEOUT):
            state = read_state_unlocked()
            if not state:
                return
            compacting = state.get("compacting") if isinstance(state.get("compacting"), dict) else {}
            compacting[session_id] = time.time()
            state["compacting"] = compacting
            write_state_unlocked(state)
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not record compaction: {e}")


def cmd_stop():
    """SessionEnd: unregister the session. The daemon notices within a second
    and exits, clearing the presence, when no session is left."""
    hook_input = read_hook_input()
    # /clear and /resume end one session and start another in the same
    # process; its SessionStart re-registers it.
    if hook_input.get("reason") in ("clear", "resume"):
        return
    claude_pid = get_session_pid()
    remaining = unregister_session(claude_pid)
    if remaining >= 0:
        log(f"Session ended: PID {claude_pid} (active sessions: {remaining})")


# ═══════════════════════════════════════════════════════════════
# Daemon
# ═══════════════════════════════════════════════════════════════

def truncate_filename(filename: str, max_length: int = 25) -> str:
    """Shorten a long filename in the middle, keeping its extension.

    'very_long_component_name.tsx' (28 chars) -> 'very_long...nent_name.tsx' (25 chars)
    """
    if len(filename) <= max_length:
        return filename
    stem, suffix = Path(filename).stem, Path(filename).suffix
    available = max_length - len(suffix) - 3
    if available < 5:
        return filename[:max_length - 3] + "..."
    front = (available + 1) // 2
    back = available - front
    return stem[:front] + "..." + stem[-back:] + suffix


def _clip(text: str, limit: int = DISCORD_TEXT_MAX) -> str:
    return text if len(text) <= limit else text[:limit - 1] + "…"


class SessionView:
    """What the daemon knows about one registered session."""

    def __init__(self, pid: str, record: dict):
        self.pid = pid
        self.record = record
        self.tail = TranscriptTail(record["transcript"]) if record.get("transcript") else None

    @property
    def session_id(self) -> str:
        return self.record.get("session_id", "")

    def last_active(self, state: dict) -> float:
        if self.tail is not None:
            seen = max(self.tail.seen_at, self.tail.subagent_seen_at)
            return seen or float(self.record.get("ts", 0))
        return float(state.get("last_update", 0))  # 1.0.0 session: its hooks write this

    def poll(self, now: float):
        tail = self.tail
        if tail is None:
            return
        tail.poll(now)
        # Only a waiting or delegating main thread can hide running subagents
        if tail.tool == "__waiting__" or tail.tool in DELEGATE_TOOLS:
            tail.scan_subagents(now)
        else:
            tail.subagents_active = []


class RepoCache:
    """Project name and repository URL per working directory, from files."""

    def __init__(self):
        self._cache: dict[str, tuple[float, str, str]] = {}

    def get(self, cwd: str, now: float) -> tuple[str, str]:
        hit = self._cache.get(cwd)
        if hit and now - hit[0] < REPO_CACHE_TTL:
            return hit[1], hit[2]
        remote = read_origin_url(cwd)
        value = (project_name(cwd, remote) or "Claude Code", repo_web_url(remote))
        self._cache[cwd] = (now, *value)
        return value


def build_presence(view: SessionView, state: dict, config: dict, now: float,
                   repos: RepoCache) -> dict:
    """The Discord payload for the shown session."""
    display = config.get("display", {})
    tail = view.tail
    metrics = None
    if tail is not None and view.session_id:
        metrics = (state.get("metrics") or {}).get(view.session_id)

    if tail is not None:
        cwd = view.record.get("cwd", "")
        project, repo_url = repos.get(cwd, now)
        branch = tail.branch or read_branch(cwd)
        tool, file, agent = tail.effective_tool(), tail.file, tail.agent
        if tool != tail.tool:  # waiting, but background subagents still run
            running = tail.subagents_active
            file, agent = "", running[0] if len(running) == 1 else f"{len(running)} agents"
        compacting = (state.get("compacting") or {}).get(view.session_id, 0)
        if (compacting > tail.changed_at and compacting > tail.compact_done_at
                and now - compacting < COMPACT_OVERLAY_MAX):
            tool, file, agent = "__compact__", "", ""
        started = view.record.get("started") or view.record.get("ts") or int(now)
    else:
        # 1.0.0 session (no transcript known): its hooks keep the flat keys fresh
        project = state.get("project") or "Claude Code"
        repo_url = state.get("repo_url", "")
        branch = state.get("git_branch", "")
        tool, file, agent = state.get("tool", ""), state.get("file", ""), ""
        started = state.get("session_start") or int(now)

    if not isinstance(metrics, dict):
        # No per-session metrics (a 1.0.0 statusline, or none yet): use the
        # flat keys, which hold whichever session rendered last
        metrics = {
            "model": state.get("model", ""),
            "tokens": state.get("tokens") or {},
            "lines_added": state.get("lines_added", 0),
            "lines_removed": state.get("lines_removed", 0),
            "context_pct": state.get("context_pct", 0),
        }
    if metrics.get("repo_url"):
        repo_url = metrics["repo_url"]

    idle = now - view.last_active(state) > config.get("idle_timeout", IDLE_TIMEOUT)
    if idle:
        activity = "Idling"
    elif tool in DELEGATE_TOOLS and agent:
        activity = f"Delegating to {agent}"
    else:
        activity = activity_label(tool) or "Working"
    if not idle and display.get("show_file", True) and file and tool in FILE_TOOLS:
        activity = f"{activity} {truncate_filename(file)}"

    branch = branch if display.get("show_branch", True) else ""
    details = f"{activity} on {project}" + (f" ({branch})" if branch else "")
    if len(details) > DISCORD_TEXT_MAX:
        details = _clip(f"{activity} on {project}")

    parts = []
    model = metrics.get("model") or (model_display_name(tail.model_id) if tail else "")
    if display.get("show_model", True) and model:
        parts.append(model)
    tokens = metrics.get("tokens") or {}
    context_tokens = (tokens.get("input") or 0) + (tokens.get("output") or 0)
    if display.get("show_tokens", True) and context_tokens > 0:
        parts.append(f"{format_tokens(context_tokens)} ctx")
    cost = tokens.get("cost") or 0
    if display.get("show_cost", True) and cost > 0:
        parts.append(f"${cost:.2f}")
    added, removed = metrics.get("lines_added") or 0, metrics.get("lines_removed") or 0
    if display.get("show_lines", True) and (added or removed):
        parts.append(f"+{added} -{removed}")
    pct = metrics.get("context_pct") or 0
    if display.get("show_context_warning", True) and pct > 80:
        icon = "\U0001f534" if pct > 95 else "⚠"
        parts.append(f"{icon} {int(pct)}% ctx")
    state_line = _clip(" • ".join(parts) if parts else "Claude Code")

    buttons = None
    if display.get("show_button", True):
        url = config.get("custom_button_url") or repo_url
        if url:
            if config.get("custom_button_label"):
                label = config["custom_button_label"][:31]
            elif "github.com" in url:
                label = "View on GitHub"
            else:
                label = "View Repository"
            buttons = [{"label": label, "url": url}]

    return {"details": details, "state": state_line, "start": int(started), "buttons": buttons}


def choose_focus(views: dict, state: dict, current: str | None, now: float) -> str | None:
    """The session to show: the most recently active one, but keep showing
    the current one until it has been quiet for FOCUS_HOLD seconds, so two
    busy sessions do not flip the presence back and forth."""
    if not views:
        return None
    latest = max(views, key=lambda pid: views[pid].last_active(state))
    if current in views and now - views[current].last_active(state) < FOCUS_HOLD:
        return current
    return latest


def _connect_bounded(rpc):
    """rpc.connect() with a deadline.

    pypresence's connect() is `loop.run_until_complete(handshake())`, and
    the handshake reads Discord's reply with no timeout: a Discord that
    accepts the pipe but never answers would block forever. Same steps,
    bounded.
    """
    import asyncio

    if not (hasattr(rpc, "handshake") and hasattr(rpc, "update_event_loop")):
        rpc.connect()  # unknown pypresence internals: fall back to the plain call
        return
    rpc.update_event_loop(asyncio.new_event_loop())
    rpc.loop.run_until_complete(asyncio.wait_for(rpc.handshake(), DISCORD_HANDSHAKE_TIMEOUT))


def _abandon(rpc):
    """Release what a failed connect left open (pipe, event loop)."""
    if rpc is None:
        return
    writer = getattr(rpc, "sock_writer", None)
    if writer is not None:
        try:
            writer.close()
        except Exception:
            pass
    loop = getattr(rpc, "loop", None)
    if loop is not None:
        try:
            loop.close()
        except Exception:
            pass


class DiscordLink:
    """Connection to the local Discord client, with backoff and pacing."""

    def __init__(self, app_id: str):
        self.app_id = app_id
        self.rpc = None
        self.failures = 0
        self.next_attempt = 0.0
        self.last_sent = None
        self.last_send_at = 0.0

    def set_app_id(self, app_id: str):
        if app_id != self.app_id:
            log(f"App ID changed from {self.app_id} to {app_id}, reconnecting")
            self.close()
            self.app_id = app_id
            self.next_attempt = 0.0

    def _connect(self, now: float) -> bool:
        if now < self.next_attempt:
            return False
        rpc = None
        try:
            from pypresence import Presence

            rpc = Presence(self.app_id)
            _connect_bounded(rpc)
        except ImportError:
            log("ERROR: pypresence is not installed (pip install pypresence); retrying in 60s")
            self.next_attempt = now + 60
            return False
        except Exception as e:  # DiscordNotFound, InvalidPipe, InvalidID, TimeoutError, ...
            _abandon(rpc)
            self.failures += 1
            delay = DISCORD_RETRY_DELAYS[min(self.failures, len(DISCORD_RETRY_DELAYS)) - 1]
            self.next_attempt = now + delay
            # Log the first failure and then every 10th, not every retry
            if self.failures == 1 or self.failures % 10 == 0:
                log(f"Discord not reachable ({type(e).__name__}: {e}); retrying every {delay}s "
                    f"(attempt {self.failures})")
            return False
        self.rpc = rpc
        self.failures = 0
        self.last_sent = None
        log(f"Connected to Discord with App ID: {self.app_id}")
        return True

    def tick(self, payload: dict, now: float):
        """Send `payload` if it changed and the rate limit allows."""
        if self.rpc is None and not self._connect(now):
            return
        if payload == self.last_sent or now - self.last_send_at < DISCORD_MIN_INTERVAL:
            return
        try:
            self.rpc.update(large_image="claude", large_text="Claude Code", **payload)
        except Exception as e:
            log(f"Failed to update presence ({type(e).__name__}: {e}); reconnecting")
            self._drop()
            self.next_attempt = now + DISCORD_RETRY_DELAYS[0]
            return
        self.last_sent = payload
        self.last_send_at = now
        log(f"Sent to Discord: {payload['details']} | {payload['state']}")

    def _drop(self):
        rpc, self.rpc = self.rpc, None
        if rpc is not None:
            try:
                rpc.close()
            except Exception:
                pass

    def close(self):
        if self.rpc is not None:
            try:
                self.rpc.clear()
            except Exception as e:
                log(f"Warning: Could not clear presence: {e}")
        self._drop()


class LoopHeartbeat:
    """Last-resort guard for the daemon loop.

    Every Discord call is bounded (see DiscordLink._connect), but a loop that
    stops for any unforeseen reason would keep holding daemon.lock, and no
    new daemon could start. If the loop has not beaten for `limit` seconds,
    the process exits; the OS releases the lock, and the next SessionStart
    starts a fresh daemon.
    """

    def __init__(self, limit: float, on_hang=None):
        self.limit = limit
        self.last = time.monotonic()
        self._on_hang = on_hang or self._exit
        thread = threading.Thread(target=self._watch, name="heartbeat", daemon=True)
        thread.start()

    def beat(self):
        self.last = time.monotonic()

    def _watch(self):
        while True:
            time.sleep(min(10.0, self.limit / 4))
            stuck = time.monotonic() - self.last
            if stuck > self.limit:
                self._on_hang(stuck)
                return

    @staticmethod
    def _exit(stuck: float):
        log(f"ERROR: daemon loop stuck for {stuck:.0f}s; exiting so a new daemon can start")
        os._exit(1)


def _write_pid_files():
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    VERSION_FILE.write_text(f"{os.getpid()} {VERSION}", encoding="utf-8")


def _remove_pid_files():
    pid, _ = read_pid_file()
    if pid == os.getpid():
        for path in (VERSION_FILE, PID_FILE):
            try:
                path.unlink()
            except OSError:
                pass


def _acquire_daemon_lock() -> int | None:
    """Take daemon.lock, or return None if another daemon keeps it.

    A retiring daemon holds the lock while it clears the presence, with its
    PID files already removed, so wait for it a little. Stop as soon as a
    current daemon is recorded: this one is then a duplicate.
    """
    deadline = time.monotonic() + DAEMON_LOCK_WAIT
    while True:
        fd = try_exclusive_lock(DAEMON_LOCK_FILE)
        if fd is not None:
            return fd
        pid, version = read_pid_file()
        current = version is not None and _version_tuple(version) >= _version_tuple(VERSION)
        if (current and pid and is_process_alive(pid)) or time.monotonic() >= deadline:
            return None
        time.sleep(0.2)


def _retire() -> bool:
    """Called when no session is left. True means exit now.

    The PID files go first, so a SessionStart racing with this exit does not
    trust a daemon that is leaving: it spawns a successor, which waits for
    our lock. Then check once more, holding the sessions lock while the
    state is cleared, so a session that registers now cannot lose its fresh
    state to this clear.
    """
    _remove_pid_files()
    try:
        with StateLock(timeout=HOOK_LOCK_TIMEOUT, lock_file=SESSIONS_LOCK_FILE):
            if _read_sessions_unlocked():
                _write_pid_files()
                return False
            clear_state(log)
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not confirm that no session is left: {e}")
        _write_pid_files()
        return False
    return True


def _write_activity(state_activity: dict, last_written: dict) -> dict:
    """Publish per-session activity for the statusline's indicator."""
    if state_activity == last_written:
        return last_written
    try:
        with StateLock(timeout=HOOK_LOCK_TIMEOUT):
            state = read_state_unlocked()
            if state:
                state["activity"] = state_activity
                write_state_unlocked(state)
        return state_activity
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not write activity: {e}")
        return last_written


def _prune_state(live_session_ids: set):
    """Drop per-session state of sessions that ended."""
    try:
        with StateLock(timeout=HOOK_LOCK_TIMEOUT):
            state = read_state_unlocked()
            changed = False
            for key in ("metrics", "activity", "compacting"):
                table = state.get(key)
                if isinstance(table, dict):
                    kept = {k: v for k, v in table.items() if k in live_session_ids}
                    if kept != table:
                        state[key] = kept
                        changed = True
            if changed:
                write_state_unlocked(state)
    except (OSError, TimeoutError) as e:
        log(f"Warning: Could not prune state: {e}")


def run_daemon():
    """Tail session transcripts and keep Discord's presence current."""
    # Wait a little: a daemon that is retiring holds the lock while it clears
    # the presence
    lock_fd = _acquire_daemon_lock()
    if lock_fd is None:
        return  # another daemon runs
    try:
        _write_pid_files()
    except OSError as e:
        log(f"FATAL: Could not write PID file: {e}")
        release_lock(lock_fd)
        return
    log(f"Daemon {VERSION} starting (PID {os.getpid()})")
    _rotate_log()
    _sweep_stale_tmp_files()

    def shutdown(signum, frame):
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    config = get_config()
    link = DiscordLink(config.get("discord_app_id") or DISCORD_APP_ID)
    heartbeat = LoopHeartbeat(DAEMON_HANG_LIMIT)
    views: dict[str, SessionView] = {}
    repos = RepoCache()
    focus = None
    last_liveness = 0.0
    last_rotate = time.time()
    activity_written: dict = {}
    unmapped_logged: set = set()
    errors = 0

    try:
        while True:
            try:
                now = time.time()
                config = get_config()
                app_id = config.get("discord_app_id") or DISCORD_APP_ID
                heartbeat.beat()
                link.set_app_id(app_id)

                if now - last_liveness >= LIVENESS_INTERVAL:
                    last_liveness = now
                    sessions = prune_dead_sessions()
                    if sessions is not None:
                        _prune_state({session_record(v).get("session_id", "") for v in sessions.values()})
                else:
                    sessions = read_sessions(timeout=0.5)
                if sessions is not None and not sessions:
                    if _retire():
                        log("No active sessions remaining, daemon exiting")
                        break
                    sessions = None  # a session registered while we were leaving
                if sessions is not None:
                    for pid in list(views):
                        if pid not in sessions:
                            del views[pid]
                    for pid, value in sessions.items():
                        record = session_record(value)
                        view = views.get(pid)
                        if view is None or view.record.get("transcript") != record.get("transcript"):
                            views[pid] = SessionView(pid, record)
                        else:
                            view.record = record

                for view in views.values():
                    if view.tail is not None:
                        view.poll(now)
                        tool = view.tail.tool
                        if (tool and tool not in TOOL_DISPLAY and tool not in PSEUDO_TOOL_DISPLAY
                                and not tool.startswith("mcp__") and tool not in unmapped_logged):
                            unmapped_logged.add(tool)
                            log(f"Unmapped tool '{tool}', showing 'Working'")

                state = read_state(log)
                if state is None:
                    time.sleep(3)  # lock trouble: back off
                    continue

                activity_written = _write_activity(
                    {v.session_id: v.tail.effective_tool() for v in views.values()
                     if v.tail and v.session_id},
                    activity_written)

                focus = choose_focus(views, state, focus, now)
                payload = (build_presence(views[focus], state, config, now, repos)
                           if focus is not None else None)
                if payload is not None:
                    link.tick(payload, now)

                if now - last_rotate > 3600:
                    last_rotate = now
                    _rotate_log()
                errors = 0
            except Exception as e:  # noqa: BLE001 - log, count, carry on
                import traceback

                errors += 1
                log(f"Daemon error ({errors}/{MAX_CONSECUTIVE_ERRORS}): {e}\n{traceback.format_exc()}")
                if errors >= MAX_CONSECUTIVE_ERRORS:
                    log("ERROR: Too many consecutive errors, daemon exiting")
                    break
            time.sleep(POLL_INTERVAL)
    except (KeyboardInterrupt, SystemExit):
        log("Received shutdown signal")
    finally:
        link.close()
        _remove_pid_files()
        release_lock(lock_fd)
        log("Daemon stopped")


# ═══════════════════════════════════════════════════════════════
# Status
# ═══════════════════════════════════════════════════════════════

def cmd_status():
    """Print the daemon, sessions and shared state."""
    pid, version = read_pid_file()
    if pid and is_process_alive(pid):
        print(f"Daemon running (PID {pid}, version {version or '1.0.0 or earlier'})")
    else:
        print("Daemon not running")

    sessions = read_sessions() or {}
    print(f"Active sessions: {len(sessions)}")
    for pid_str, value in sessions.items():
        record = session_record(value)
        try:
            alive = "alive" if is_process_alive(int(pid_str)) else "dead"
        except ValueError:
            alive = "corrupt"
        transcript = record.get("transcript", "")
        where = f"transcript {Path(transcript).name}" if transcript else "no transcript (1.0.0 hooks)"
        print(f"  - PID {pid_str}: {alive}, {where}")

    state = read_state()
    if state is None:
        print("Could not read state (lock timeout or read error)")
        return
    if not state:
        print("No active session state")
        return
    print(f"Project: {state.get('project', 'Unknown')}")
    if state.get("git_branch"):
        print(f"Branch: {state['git_branch']}")
    for session_id, metrics in (state.get("metrics") or {}).items():
        tokens = metrics.get("tokens") or {}
        context = (tokens.get("input") or 0) + (tokens.get("output") or 0)
        print(f"Session {session_id[:8]}: {metrics.get('model', '?')}, "
              f"{format_tokens(context)} ctx, ${tokens.get('cost') or 0:.2f}")
    for session_id, tool in (state.get("activity") or {}).items():
        print(f"Activity {session_id[:8]}: {activity_label(tool) or '-'}")


def main():
    # Windows consoles may use a legacy code page; `status` prints Unicode
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    commands = {
        "start": (cmd_start, START_DEADLINE),
        "update": (cmd_update, HOOK_DEADLINE),
        "stop": (cmd_stop, HOOK_DEADLINE),
        "status": (cmd_status, None),
        "daemon": (run_daemon, None),
    }
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("Usage: presence.py <start|update|stop|status|daemon>")
        sys.exit(1)
    handler, deadline = commands[sys.argv[1]]
    if deadline:
        arm_watchdog(deadline)
    handler()


if __name__ == "__main__":
    main()
