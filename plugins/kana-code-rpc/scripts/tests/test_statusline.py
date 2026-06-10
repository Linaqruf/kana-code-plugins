"""Statusline integration tests.

Runs statusline.py as a subprocess (the way Claude Code invokes it) against
an isolated KANA_RPC_DATA_DIR, feeding captured/synthetic payloads on stdin.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
REAL_PAYLOAD = (FIXTURES / "statusline_payload.json").read_text(encoding="utf-8")
MINIMAL_PAYLOAD = (FIXTURES / "statusline_payload_minimal.json").read_text(encoding="utf-8")


def run_statusline(scripts_dir: Path, data_dir: Path, payload: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, KANA_RPC_DATA_DIR=str(data_dir))
    return subprocess.run(
        [sys.executable, str(scripts_dir / "statusline.py")],
        input=payload.encode("utf-8"),
        capture_output=True,
        env=env,
        timeout=30,
    )


def read_state(data_dir: Path) -> dict:
    state_file = data_dir / "state.json"
    if not state_file.exists():
        return {}
    return json.loads(state_file.read_text(encoding="utf-8"))


def seed_state(data_dir: Path, state: dict):
    (data_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")


class TestRealPayload:
    def test_renders_without_error(self, scripts_dir, isolated_data_dir):
        result = run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        out = result.stdout.decode("utf-8")
        assert result.returncode == 0
        assert "[statusline error]" not in out

    def test_shows_model_context_cost_duration(self, scripts_dir, isolated_data_dir):
        result = run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        out = result.stdout.decode("utf-8")
        assert "Fable 5" in out
        assert "145k ctx" in out  # 141,836 input + 3,246 output = current context
        assert "14%" in out
        assert "$7.18" in out
        assert "59m" in out  # 3,574,429 ms

    def test_rate_limit_hidden_below_threshold(self, scripts_dir, isolated_data_dir):
        # Fixture has five_hour at 39% — below the 80% warning threshold
        result = run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        assert "5h" not in result.stdout.decode("utf-8")

    def test_rate_limit_shown_at_threshold(self, scripts_dir, isolated_data_dir):
        payload = json.loads(REAL_PAYLOAD)
        payload["rate_limits"]["five_hour"]["used_percentage"] = 91
        result = run_statusline(scripts_dir, isolated_data_dir, json.dumps(payload))
        assert "5h 91%" in result.stdout.decode("utf-8")

    def test_no_state_write_without_session(self, scripts_dir, isolated_data_dir):
        run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        # No session_start in state -> statusline must not create session data
        assert read_state(isolated_data_dir) == {}


class TestStateIntegration:
    def test_updates_state_when_session_active(self, scripts_dir, isolated_data_dir):
        seed_state(isolated_data_dir, {"session_start": 1000000000, "tool": "Edit"})
        result = run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        assert result.returncode == 0
        state = read_state(isolated_data_dir)
        assert state["model"] == "Fable 5"
        assert state["tokens"]["input"] == 141836
        assert state["tokens"]["cost"] == 7.1802297
        assert state["context_pct"] == 14
        assert state["statusline_update"] > 0

    def test_tool_indicator_rendered(self, scripts_dir, isolated_data_dir):
        seed_state(isolated_data_dir, {"session_start": 1000000000, "tool": "Edit"})
        result = run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        assert "Editing" in result.stdout.decode("utf-8")

    def test_pseudo_tool_indicator_rendered(self, scripts_dir, isolated_data_dir):
        seed_state(isolated_data_dir, {"session_start": 1000000000, "tool": "__waiting__"})
        result = run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        assert "Waiting for input" in result.stdout.decode("utf-8")

    def test_write_throttle_skips_unchanged_payload(self, scripts_dir, isolated_data_dir):
        seed_state(isolated_data_dir, {"session_start": 1000000000})
        run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        first = read_state(isolated_data_dir)
        assert first["statusline_update"] > 0

        # Re-render with an identical payload within the 5s heartbeat:
        # only duration_ms-equivalent churn -> write must be skipped
        run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)
        second = read_state(isolated_data_dir)
        assert second == first

    def test_changed_payload_writes_through_throttle(self, scripts_dir, isolated_data_dir):
        seed_state(isolated_data_dir, {"session_start": 1000000000})
        run_statusline(scripts_dir, isolated_data_dir, REAL_PAYLOAD)

        payload = json.loads(REAL_PAYLOAD)
        payload["cost"]["total_cost_usd"] = 9.99
        run_statusline(scripts_dir, isolated_data_dir, json.dumps(payload))
        assert read_state(isolated_data_dir)["tokens"]["cost"] == 9.99


class TestEdgeCases:
    def test_minimal_nulls_do_not_crash(self, scripts_dir, isolated_data_dir):
        result = run_statusline(scripts_dir, isolated_data_dir, MINIMAL_PAYLOAD)
        out = result.stdout.decode("utf-8")
        assert result.returncode == 0
        assert "[statusline error]" not in out

    def test_empty_input(self, scripts_dir, isolated_data_dir):
        result = run_statusline(scripts_dir, isolated_data_dir, "")
        assert result.returncode == 0

    def test_garbage_input(self, scripts_dir, isolated_data_dir):
        result = run_statusline(scripts_dir, isolated_data_dir, "not json {{{")
        assert result.returncode == 0

    def test_overflow_percentage_clamped(self, scripts_dir, isolated_data_dir):
        payload = json.loads(REAL_PAYLOAD)
        payload["context_window"]["used_percentage"] = 250
        result = run_statusline(scripts_dir, isolated_data_dir, json.dumps(payload))
        out = result.stdout.decode("utf-8")
        assert result.returncode == 0
        assert "100%" in out
        assert "250" not in out
