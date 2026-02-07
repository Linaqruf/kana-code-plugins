"""
Shared state management for Discord Rich Presence.
Provides process-safe state file operations with cross-platform file locking.
"""

import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

# Platform-specific imports for file locking
if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

# ═══════════════════════════════════════════════════════════════
# Data Directory Setup
# ═══════════════════════════════════════════════════════════════

if sys.platform == "win32":
    _appdata = os.environ.get("APPDATA")
    if _appdata:
        DATA_DIR = Path(_appdata) / "kana-code-rpc"
    else:
        DATA_DIR = Path.home() / ".kana-code-rpc"
else:
    DATA_DIR = Path.home() / ".local" / "share" / "kana-code-rpc"

STATE_FILE = DATA_DIR / "state.json"
LOCK_FILE = DATA_DIR / "state.lock"


# ═══════════════════════════════════════════════════════════════
# Shared Utilities
# ═══════════════════════════════════════════════════════════════

def format_tokens(count: int) -> str:
    """Format token count for display (e.g., 12.5k, 1.2M).

    Shared utility used by both presence.py and statusline.py.
    """
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 100_000:
        return f"{count / 1_000:.0f}k"
    if count >= 1_000:
        return f"{count / 1_000:.1f}k"
    return f"{count:,}"


# ═══════════════════════════════════════════════════════════════
# File Locking
# ═══════════════════════════════════════════════════════════════

class StateLock:
    """
    Cross-platform file lock for state operations.

    Usage:
        with StateLock():
            state = read_state_unlocked()
            state["key"] = "value"
            write_state_unlocked(state)

    Note: Use the _unlocked variants inside StateLock context.
    The locking variants (read_state, write_state) acquire their own locks.

    Args:
        timeout: Max seconds to wait for lock acquisition.
        lock_file: Path to lock file. Defaults to state.lock.
                   Pass a different path for independent locks (e.g., sessions.lock).
    """

    def __init__(self, timeout: float = 5.0, lock_file: Path | None = None):
        self.timeout = timeout
        self._lock_file = lock_file or LOCK_FILE
        self._lock_fd = None

    def __enter__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        start = time.time()

        while True:
            try:
                # Open lock file (create if doesn't exist)
                self._lock_fd = os.open(str(self._lock_file), os.O_CREAT | os.O_RDWR)

                if sys.platform == "win32":
                    # Windows: lock first byte exclusively
                    msvcrt.locking(self._lock_fd, msvcrt.LK_NBLCK, 1)
                else:
                    # Unix: exclusive non-blocking lock
                    fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

                return self

            except (OSError, IOError):
                # Lock acquisition failed, close and retry
                if self._lock_fd is not None:
                    try:
                        os.close(self._lock_fd)
                    except OSError:
                        pass
                    self._lock_fd = None

                if time.time() - start > self.timeout:
                    raise TimeoutError(f"Could not acquire state lock within {self.timeout}s")

                time.sleep(0.01)  # 10ms retry interval

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._lock_fd is not None:
            try:
                if sys.platform == "win32":
                    msvcrt.locking(self._lock_fd, msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
            except (OSError, IOError) as e:
                # Log unlock failures - can cause future lock timeouts
                print(f"[state] Warning: Failed to unlock state file: {e}", file=sys.stderr)
            finally:
                try:
                    os.close(self._lock_fd)
                except OSError:
                    pass
                self._lock_fd = None
        return False


# ═══════════════════════════════════════════════════════════════
# State Read/Write (Low-level, no locking)
# ═══════════════════════════════════════════════════════════════

def read_state_unlocked() -> dict:
    """
    Read current state from state file without locking.
    Use read_state() or wrap with StateLock for safe access.

    Returns empty dict if file doesn't exist or is corrupt.
    Logs to stderr on corruption since this is a low-level function
    that may be called before presence.py logging is available.
    """
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
            # Log corruption to stderr - this is critical for debugging
            print(f"[state] Warning: State file corrupt or unreadable: {e}", file=sys.stderr)
    return {}


def write_state_unlocked(state: dict):
    """
    Write state to state file using atomic write pattern (no locking).
    Use write_state() or wrap with StateLock for safe access.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    content = json.dumps(state, indent=2)

    fd, tmp_path = tempfile.mkstemp(dir=DATA_DIR, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        # shutil.move handles cross-platform atomic rename (including Windows overwrite)
        shutil.move(tmp_path, STATE_FILE)
    except (OSError, IOError):
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ═══════════════════════════════════════════════════════════════
# State Read/Write (Safe, with locking)
# ═══════════════════════════════════════════════════════════════

def read_state(logger=None) -> dict | None:
    """
    Read current state from state file with locking.

    Args:
        logger: Optional logging function for warnings

    Returns:
        State dict on success (may be empty {}), or None on lock/read error
    """
    try:
        with StateLock():
            return read_state_unlocked()
    except (OSError, TimeoutError) as e:
        if logger:
            logger(f"Warning: Could not read state: {e}")
        return None


def write_state(state: dict, logger=None) -> bool:
    """
    Write state to state file with locking.

    Args:
        state: State dict to write
        logger: Optional logging function for warnings

    Returns:
        True if write succeeded, False on error
    """
    try:
        with StateLock():
            write_state_unlocked(state)
        return True
    except (OSError, TimeoutError) as e:
        if logger:
            logger(f"Warning: Could not write state: {e}")
        return False


def update_state(updates: dict, logger=None) -> dict | None:
    """
    Atomically update state with locking (read-modify-write).
    Only updates specified keys, preserving other state.

    Args:
        updates: Dict of key-value pairs to update
        logger: Optional logging function for warnings

    Returns:
        Updated state dict on success, or None on lock/write error
    """
    try:
        with StateLock():
            state = read_state_unlocked()
            state.update(updates)
            write_state_unlocked(state)
            return state
    except (OSError, TimeoutError) as e:
        if logger:
            logger(f"Warning: Could not update state: {e}")
        return None


def clear_state(logger=None):
    """
    Clear state file with locking.

    Args:
        logger: Optional logging function for warnings
    """
    try:
        with StateLock():
            write_state_unlocked({})
    except (OSError, TimeoutError) as e:
        if logger:
            logger(f"Warning: Could not clear state: {e}")
