"""presence.py: hooks.json shape, sessions, hook deadline, presence payload,
focus and Discord pacing."""
import json
import os
import subprocess
import sys
import threading
import time
import types
from pathlib import Path

import pytest

import presence
from activity import TranscriptTail
from presence import (
    DISCORD_MIN_INTERVAL,
    DiscordLink,
    RepoCache,
    SessionView,
    build_presence,
    choose_focus,
    session_record,
    truncate_filename,
)
from state import format_tokens

PLUGIN_DIR = Path(__file__).resolve().parent.parent.parent
HOOKS_JSON = PLUGIN_DIR / "hooks" / "hooks.json"
PLUGIN_JSON = PLUGIN_DIR / ".claude-plugin" / "plugin.json"


class TestHooksShape:
    """The 2026-09-28 pile-up came from a python chain per tool call. These
    guard the fix: no per-tool hook, no shell layer, no ignored timeouts."""

    def _hooks(self) -> dict:
        return json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]

    def test_no_per_tool_or_per_turn_hooks(self):
        hooks = self._hooks()
        for event in ("PreToolUse", "PostToolUse", "PostToolBatch", "UserPromptSubmit",
                      "Stop", "SubagentStart", "SubagentStop"):
            assert event not in hooks, f"{event} fires per tool call or turn; the transcript covers it"
        assert set(hooks) == {"SessionStart", "PreCompact", "SessionEnd"}

    def test_async_without_timeout(self):
        for event, groups in self._hooks().items():
            for group in groups:
                for hook in group["hooks"]:
                    assert hook["type"] == "command"
                    assert hook["async"] is True
                    # Claude Code ignores timeout on async hooks; don't pretend
                    assert "timeout" not in hook, f"{event}: timeout is not enforced on async hooks"

    def test_hook_commands_exist(self):
        # Shell form on purpose: exec form cannot start .bat shims such as
        # pyenv-win's `python`, and with three hooks per session the shell
        # layer costs little
        commands = set()
        for groups in self._hooks().values():
            for group in groups:
                for hook in group["hooks"]:
                    assert "args" not in hook
                    assert hook["command"].startswith('python "${CLAUDE_PLUGIN_ROOT}/scripts/presence.py" ')
                    commands.add(hook["command"].rsplit(" ", 1)[1])
        assert commands == {"start", "update", "stop"}


def test_version_matches_plugin_json():
    assert presence.VERSION == json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"]


class TestSessions:
    @pytest.fixture(autouse=True)
    def isolated(self, tmp_path, monkeypatch):
        monkeypatch.setattr(presence, "SESSIONS_FILE", tmp_path / "sessions.json")
        monkeypatch.setattr(presence, "SESSIONS_LOCK_FILE", tmp_path / "sessions.lock")
        self.file = tmp_path / "sessions.json"

    def test_session_record_accepts_both_formats(self):
        assert session_record(1700000000) == {"ts": 1700000000, "started": 1700000000}
        assert session_record({"ts": 1, "transcript": "t"})["transcript"] == "t"
        assert session_record("junk") == {}

    def test_register_keeps_legacy_entries(self, monkeypatch):
        # A live 1.0.0 session (int value) must survive a 1.1.0 registration
        monkeypatch.setattr(presence, "is_process_alive", lambda pid: True)
        self.file.write_text(json.dumps({"111": 1700000000}), encoding="utf-8")
        count, is_new = presence.register_session(
            222, {"session_id": "s2", "transcript_path": "/p/s2.jsonl"}, "/proj")
        data = json.loads(self.file.read_text(encoding="utf-8"))
        assert (count, is_new) == (2, True)
        assert data["111"] == 1700000000
        assert data["222"]["transcript"] == "/p/s2.jsonl"

    def test_reregister_keeps_started(self):
        presence.register_session(222, {"session_id": "a", "transcript_path": "/p/a.jsonl"}, "/proj")
        first = json.loads(self.file.read_text(encoding="utf-8"))["222"]["started"]
        time.sleep(1.1)
        count, is_new = presence.register_session(
            222, {"session_id": "b", "transcript_path": "/p/b.jsonl"}, "/proj")
        record = json.loads(self.file.read_text(encoding="utf-8"))["222"]
        assert is_new is False
        assert record["started"] == first
        assert (record["session_id"], record["transcript"]) == ("b", "/p/b.jsonl")

    def test_register_drops_dead_sessions(self, monkeypatch):
        # After a reboot, dead PIDs must not make a new session look like a
        # second one (the count decides whether state starts fresh)
        monkeypatch.setattr(presence, "is_process_alive", lambda pid: pid != 999)
        self.file.write_text(json.dumps({"999": 1700000000}), encoding="utf-8")
        count, is_new = presence.register_session(222, {"session_id": "s"}, "/proj")
        assert (count, is_new) == (1, True)
        assert "999" not in json.loads(self.file.read_text(encoding="utf-8"))

    def test_subagent_session_start_ignored(self, monkeypatch):
        monkeypatch.setattr(presence, "read_hook_input", lambda: {"agent_id": "a1", "session_id": "s"})
        monkeypatch.setattr(presence, "register_session",
                            lambda *a: pytest.fail("a subagent must not register a session"))
        presence.cmd_start()

    def test_subagent_transcript_not_adopted(self):
        presence.register_session(222, {"session_id": "a", "transcript_path": "/p/a.jsonl"}, "/proj")
        presence.register_session(222, {"session_id": "a", "agent_id": "x",
                                        "transcript_path": "/p/a/subagents/agent-x.jsonl"}, "/proj")
        assert json.loads(self.file.read_text(encoding="utf-8"))["222"]["transcript"] == "/p/a.jsonl"


class TestPidFile:
    @pytest.fixture(autouse=True)
    def isolated(self, tmp_path, monkeypatch):
        monkeypatch.setattr(presence, "PID_FILE", tmp_path / "daemon.pid")
        monkeypatch.setattr(presence, "VERSION_FILE", tmp_path / "daemon.version")
        self.dir = tmp_path

    def test_legacy_pid_file_has_no_version(self):
        (self.dir / "daemon.pid").write_text("4242", encoding="utf-8")
        assert presence.read_pid_file() == (4242, None)

    def test_version_file_must_match_pid(self):
        (self.dir / "daemon.pid").write_text("4242", encoding="utf-8")
        (self.dir / "daemon.version").write_text("4242 1.1.0", encoding="utf-8")
        assert presence.read_pid_file() == (4242, "1.1.0")
        (self.dir / "daemon.version").write_text("1111 1.1.0", encoding="utf-8")
        assert presence.read_pid_file() == (4242, None)


class TestEnsureDaemon:
    """daemon.lock decides whether a 1.1.0+ daemon runs; PID files can be
    stale after a reboot or a hard kill."""

    @pytest.fixture(autouse=True)
    def isolated(self, tmp_path, monkeypatch):
        monkeypatch.setattr(presence, "PID_FILE", tmp_path / "daemon.pid")
        monkeypatch.setattr(presence, "VERSION_FILE", tmp_path / "daemon.version")
        monkeypatch.setattr(presence, "DAEMON_LOCK_FILE", tmp_path / "daemon.lock")
        self.dir = tmp_path
        self.spawned, self.killed = [], []
        monkeypatch.setattr(presence.subprocess, "Popen",
                            lambda *a, **kw: self.spawned.append(a) or types.SimpleNamespace(pid=1))
        monkeypatch.setattr(presence, "terminate_process", lambda pid: self.killed.append(pid) or True)
        monkeypatch.setattr(presence, "is_process_alive", lambda pid: True)
        monkeypatch.setattr(presence, "_process_name", lambda pid: "python.exe")

    def write_pid(self, pid, version=None):
        (self.dir / "daemon.pid").write_text(str(pid), encoding="utf-8")
        if version:
            (self.dir / "daemon.version").write_text(f"{pid} {version}", encoding="utf-8")

    def test_stale_legacy_pid_reused_by_other_python_is_not_killed(self, monkeypatch):
        self.write_pid(4242)
        written = (self.dir / "daemon.pid").stat().st_mtime
        monkeypatch.setattr(presence, "_process_start_time", lambda pid: written + 3600)
        presence.ensure_daemon()
        assert self.killed == [] and len(self.spawned) == 1

    def test_live_legacy_daemon_is_replaced(self, monkeypatch):
        self.write_pid(4242)
        written = (self.dir / "daemon.pid").stat().st_mtime
        monkeypatch.setattr(presence, "_process_start_time", lambda pid: written - 1)
        presence.ensure_daemon()
        assert self.killed == [4242] and len(self.spawned) == 1

    def test_stale_current_version_files_do_not_block_spawn(self):
        # Lock free: whatever the files say, no 1.1.0 daemon runs
        self.write_pid(4242, presence.VERSION)
        presence.ensure_daemon()
        assert self.killed == [] and len(self.spawned) == 1

    def test_running_current_daemon_is_kept(self):
        held = presence.try_exclusive_lock(presence.DAEMON_LOCK_FILE)
        try:
            self.write_pid(4242, presence.VERSION)
            presence.ensure_daemon()
        finally:
            presence.release_lock(held)
        assert self.killed == [] and self.spawned == []

    def test_retiring_daemon_gets_a_successor(self):
        held = presence.try_exclusive_lock(presence.DAEMON_LOCK_FILE)
        try:
            # Lock held, but the retiring daemon has removed its PID files
            presence.ensure_daemon()
        finally:
            presence.release_lock(held)
        assert self.killed == [] and len(self.spawned) == 1

    def test_older_daemon_is_replaced(self):
        held = presence.try_exclusive_lock(presence.DAEMON_LOCK_FILE)
        try:
            self.write_pid(4242, "1.0.9")
            presence.ensure_daemon()
        finally:
            presence.release_lock(held)
        assert self.killed == [4242] and len(self.spawned) == 1


class TestRetire:
    @pytest.fixture(autouse=True)
    def isolated(self, tmp_path, monkeypatch):
        monkeypatch.setattr(presence, "PID_FILE", tmp_path / "daemon.pid")
        monkeypatch.setattr(presence, "VERSION_FILE", tmp_path / "daemon.version")
        self.dir = tmp_path

    def test_exits_when_still_empty(self, monkeypatch):
        presence._write_pid_files()
        monkeypatch.setattr(presence, "read_sessions", lambda timeout=0: {})
        assert presence._retire() is True
        assert not (self.dir / "daemon.pid").exists()

    def test_stays_when_a_session_arrived(self, monkeypatch):
        presence._write_pid_files()
        seen_files = []

        def sessions(timeout=0):
            # By the time we check again, the PID files must already be gone
            seen_files.append((self.dir / "daemon.version").exists())
            return {"222": {"ts": 1}}

        monkeypatch.setattr(presence, "read_sessions", sessions)
        assert presence._retire() is False
        assert seen_files == [False]
        assert presence.read_pid_file() == (os.getpid(), presence.VERSION)


class TestDiscordWorker:
    def test_hung_handshake_does_not_block_the_daemon(self, monkeypatch):
        release = threading.Event()

        class Presence:
            def __init__(self, app_id):
                pass

            def connect(self):
                release.wait(10)  # Discord accepted the pipe and never answers
                raise RuntimeError("gave up")

        monkeypatch.setitem(sys.modules, "pypresence", types.SimpleNamespace(Presence=Presence))
        monkeypatch.setattr(presence, "DISCORD_STALL_LIMIT", 0.2)
        worker = presence.DiscordWorker("1")
        started = time.monotonic()
        worker.submit({"details": "d", "state": "s", "start": 1, "buttons": None}, "1")
        assert time.monotonic() - started < 0.1  # submit never waits for Discord
        deadline = time.monotonic() + 5
        while not worker.stalled() and time.monotonic() < deadline:
            time.sleep(0.05)
        assert worker.stalled()
        worker.retire(wait=0, clear=False)
        release.set()


class TestHookDeadline:
    def test_hook_exits_even_if_stdin_never_closes(self, scripts_dir, isolated_data_dir):
        """The regression test for the pile-up: a hook whose stdin stays open
        and empty must still exit, by its own watchdog."""
        env = dict(os.environ, KANA_RPC_DATA_DIR=str(isolated_data_dir))
        proc = subprocess.Popen([sys.executable, str(scripts_dir / "presence.py"), "update"],
                                stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, env=env)
        started = time.monotonic()
        try:
            proc.wait(timeout=presence.HOOK_DEADLINE + 10)
        except subprocess.TimeoutExpired:
            proc.kill()
            pytest.fail("hook outlived its deadline")
        finally:
            proc.stdin.close()
        assert time.monotonic() - started < presence.HOOK_DEADLINE + 5

    def test_precompact_marks_session(self, scripts_dir, isolated_data_dir):
        (isolated_data_dir / "state.json").write_text(json.dumps({"session_start": 1}), encoding="utf-8")
        env = dict(os.environ, KANA_RPC_DATA_DIR=str(isolated_data_dir))
        payload = json.dumps({"hook_event_name": "PreCompact", "session_id": "s1"})
        subprocess.run([sys.executable, str(scripts_dir / "presence.py"), "update"],
                       input=payload.encode(), env=env, timeout=30, check=True)
        state = json.loads((isolated_data_dir / "state.json").read_text(encoding="utf-8"))
        assert state["compacting"]["s1"] > 0


def make_view(tool="", file="", agent="", branch="main", seen_at=1000.0, session_id="s1"):
    view = SessionView("123", {"transcript": "unused.jsonl", "session_id": session_id,
                               "cwd": "", "started": 900, "ts": 900})
    tail = view.tail
    tail.tool, tail.file, tail.agent, tail.branch = tool, file, agent, branch
    tail.seen_at = tail.changed_at = seen_at
    tail.model_id = "claude-opus-5-5"
    return view


CONFIG = presence.DEFAULT_CONFIG


class TestBuildPresence:
    def test_editing_with_metrics(self):
        state = {"metrics": {"s1": {"model": "Opus 5.5", "tokens": {"input": 120000, "output": 3000,
                                                                     "cost": 6.44},
                                    "lines_added": 309, "lines_removed": 104, "context_pct": 12,
                                    "repo_url": "https://github.com/u/r"}}}
        p = build_presence(make_view("Edit", "presence.py"), state, CONFIG, 1001.0, RepoCache())
        assert p["details"] == "Editing presence.py on Claude Code (main)"
        assert p["state"] == "Opus 5.5 • 123k ctx • $6.44 • +309 -104"
        assert p["buttons"] == [{"label": "View on GitHub", "url": "https://github.com/u/r"}]
        assert p["start"] == 900

    def test_model_from_transcript_without_statusline(self):
        p = build_presence(make_view("Bash"), {}, CONFIG, 1001.0, RepoCache())
        assert p["details"].startswith("Running on")
        assert p["state"] == "Opus 5.5"

    def test_delegating_names_subagent_type(self):
        p = build_presence(make_view("Agent", agent="Explore"), {}, CONFIG, 1001.0, RepoCache())
        assert p["details"].startswith("Delegating to Explore")

    def test_waiting_with_background_subagents_is_delegating(self):
        view = make_view("__waiting__")
        view.tail.subagents_active = ["general-purpose", "general-purpose", "Explore"]
        p = build_presence(view, {}, CONFIG, 1001.0, RepoCache())
        assert p["details"].startswith("Delegating to 3 agents")
        view.tail.subagents_active = ["Explore"]
        assert build_presence(view, {}, CONFIG, 1001.0, RepoCache())["details"].startswith(
            "Delegating to Explore")

    def test_subagent_activity_keeps_session_from_idling(self):
        view = make_view("__waiting__", seen_at=1000.0)
        view.tail.subagent_seen_at = 1290.0
        assert not build_presence(view, {}, CONFIG, 1310.0, RepoCache())["details"].startswith("Idling")

    def test_idle_after_timeout(self):
        view = make_view("Edit", "a.py", seen_at=1000.0)
        p = build_presence(view, {}, CONFIG, 1000.0 + 301, RepoCache())
        assert p["details"].startswith("Idling on")

    def test_compacting_overlay_until_boundary(self):
        view = make_view("Bash", seen_at=1000.0)
        state = {"compacting": {"s1": 1005.0}}
        assert build_presence(view, state, CONFIG, 1010.0, RepoCache())["details"].startswith("Compacting")
        view.tail.compact_done_at = 1030.0
        assert build_presence(view, state, CONFIG, 1031.0, RepoCache())["details"].startswith("Running")

    def test_compacting_shows_when_tool_was_read_after_the_hook(self):
        # Auto-compaction right after a fast tool: the tool_use line was
        # written at 1000.1, the PreCompact hook stamped 1000.4, and the daemon
        # read the line at 1000.7. changed_at is the write time (1000.1).
        view = make_view("Read", "a.py", seen_at=1000.7)
        view.tail.changed_at = 1000.1
        state = {"compacting": {"s1": 1000.4}}
        assert build_presence(view, state, CONFIG, 1001.0, RepoCache())["details"].startswith("Compacting")

    def test_legacy_session_uses_flat_keys(self):
        view = SessionView("111", session_record(900))
        state = {"tool": "Write", "file": "x.py", "project": "old-proj", "git_branch": "dev",
                 "last_update": 1000, "model": "Opus 5.5", "tokens": {"input": 5000, "cost": 1.5}}
        p = build_presence(view, state, CONFIG, 1001.0, RepoCache())
        assert p["details"] == "Writing x.py on old-proj (dev)"
        assert p["state"].startswith("Opus 5.5 • 5.0k ctx • $1.50")

    def test_fields_fit_discord_limits(self):
        view = make_view("Edit", "f.py", branch="b" * 200)
        p = build_presence(view, {"metrics": {"s1": {"model": "M" * 300}}}, CONFIG, 1001.0, RepoCache())
        assert len(p["details"]) <= 128 and len(p["state"]) <= 128


class TestChooseFocus:
    def test_holds_current_until_quiet(self):
        a, b = make_view(seen_at=1000.0), make_view(seen_at=1005.0, session_id="s2")
        views = {"a": a, "b": b}
        assert choose_focus(views, {}, "a", 1010.0) == "a"      # a quiet for 10 s < hold
        assert choose_focus(views, {}, "a", 1000.0 + 25) == "b"  # a quiet for 25 s
        assert choose_focus(views, {}, None, 1010.0) == "b"
        assert choose_focus({}, {}, "a", 1010.0) is None


class FakeRPC:
    def __init__(self):
        self.sent = []

    def update(self, **kw):
        self.sent.append(kw)

    def clear(self):
        pass

    def close(self):
        pass


class TestDiscordLink:
    def payload(self, details):
        return {"details": details, "state": "s", "start": 1, "buttons": None}

    def test_coalesces_to_one_update_per_interval(self):
        link = DiscordLink("1")
        link.rpc = FakeRPC()
        link.tick(self.payload("a"), 100.0)
        link.tick(self.payload("b"), 101.0)
        link.tick(self.payload("c"), 102.0)
        assert [s["details"] for s in link.rpc.sent] == ["a"]
        link.tick(self.payload("c"), 100.0 + DISCORD_MIN_INTERVAL)
        assert [s["details"] for s in link.rpc.sent] == ["a", "c"]  # latest wins

    def test_unchanged_payload_not_resent(self):
        link = DiscordLink("1")
        link.rpc = FakeRPC()
        link.tick(self.payload("a"), 100.0)
        link.tick(self.payload("a"), 200.0)
        assert len(link.rpc.sent) == 1

    def test_discord_absent_backs_off_without_exiting(self, monkeypatch):
        attempts = []

        class Presence:
            def __init__(self, app_id):
                pass

            def connect(self):
                attempts.append(1)
                raise RuntimeError("Could not find Discord installed and running on this machine.")

        monkeypatch.setitem(sys.modules, "pypresence", types.SimpleNamespace(Presence=Presence))
        link = DiscordLink("1")
        for t in range(0, 120):
            link.tick(self.payload("a"), float(t))
        # Retries at t=0, 15, 45, 105: backoff 15 -> 30 -> 60, never gives up
        assert len(attempts) == 4
        assert link.rpc is None


class TestSmallHelpers:
    def test_truncate_filename(self):
        assert truncate_filename("main.py") == "main.py"
        result = truncate_filename("very_long_component_name_indeed.tsx")
        assert len(result) <= 25 and result.endswith(".tsx") and "..." in result
        assert truncate_filename("a" * 21 + ".tsx") == "a" * 21 + ".tsx"

    def test_format_tokens(self):
        assert [format_tokens(n) for n in (999, 1500, 150000, 1_200_000)] == ["999", "1.5k", "150k", "1.2M"]

    def test_default_config_has_button_settings(self):
        assert presence.DEFAULT_CONFIG["display"]["show_button"] is True
        assert presence.DEFAULT_CONFIG["custom_button_label"] == ""


class TestLockWarnRateLimit:
    def test_contention_log_is_rate_limited(self, monkeypatch):
        import state

        class AlwaysLocked:
            def __init__(self, *a, **kw):
                pass

            def __enter__(self):
                raise TimeoutError("Could not acquire state lock within 5.0s")

            def __exit__(self, *a):
                return False

        monkeypatch.setattr(state, "StateLock", AlwaysLocked)
        monkeypatch.setattr(state, "_last_lock_warn", 0.0)
        messages = []
        for _ in range(3):
            assert state.read_state(messages.append) is None
        assert len(messages) == 1, "repeated lock failures must log once per interval"
        assert "suppressed" in messages[0]
