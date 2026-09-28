"""Transcript tailing and display names (activity.py)."""
import json
import os

import pytest

import activity
from activity import TranscriptTail, activity_label, model_display_name


class TestModelDisplayName:
    @pytest.mark.parametrize("model_id, expected", [
        # Current models (2026-09)
        ("claude-fable-5-1", "Fable 5.1"),
        ("claude-opus-5-5", "Opus 5.5"),
        ("claude-sonnet-5", "Sonnet 5"),
        ("claude-haiku-4-5-20251001", "Haiku 4.5"),
        # Context-size suffix, as Claude Code shows it
        ("claude-opus-5-5[1m]", "Opus 5.5 (1M context)"),
        # Older ID shapes seen in transcripts on disk
        ("claude-opus-4-8", "Opus 4.8"),
        ("claude-3-5-sonnet-20241022", "Sonnet 3.5"),
        ("opus", "Opus"),
    ])
    def test_formats_ids(self, model_id, expected):
        assert model_display_name(model_id) == expected

    def test_placeholder_and_empty(self):
        assert model_display_name("<synthetic>") == ""
        assert model_display_name("") == ""

    def test_unknown_shape_passes_through(self):
        assert model_display_name("gpt-x-mini-preview") == "gpt-x-mini-preview"


class TestActivityLabel:
    def test_labels(self):
        assert activity_label("Edit") == "Editing"
        assert activity_label("__prompt__") == "Thinking"
        assert activity_label("mcp__github__get_issue") == "Using MCP"
        assert activity_label("SomeFutureTool") == "Working"
        assert activity_label("") == ""

    def test_pseudo_tools_not_in_tool_display(self):
        assert not set(activity.PSEUDO_TOOL_DISPLAY) & set(activity.TOOL_DISPLAY)


def rec(kind, **fields) -> dict:
    return {"type": kind, "isSidechain": False, "gitBranch": "main", **fields}


def assistant(*blocks, stop="tool_use", model="claude-opus-5-5") -> dict:
    return rec("assistant", message={"model": model, "stop_reason": stop, "content": list(blocks)})


def tool_use(name, **tool_input) -> dict:
    return {"type": "tool_use", "id": "toolu_x", "name": name, "input": tool_input}


def user(content, **fields) -> dict:
    return rec("user", message={"role": "user", "content": content}, **fields)


def dumps(record: dict) -> str:
    # Claude Code writes compact JSON; the tail's substring filters rely on it
    return json.dumps(record, separators=(",", ":"))


class Transcript:
    def __init__(self, path):
        self.path = path
        path.write_text("", encoding="utf-8")

    def append(self, *records, raw: str = ""):
        with open(self.path, "a", encoding="utf-8") as f:
            for r in records:
                f.write(dumps(r) + "\n")
            f.write(raw)


@pytest.fixture
def transcript(tmp_path):
    return Transcript(tmp_path / "session.jsonl")


@pytest.fixture
def tail(transcript):
    t = TranscriptTail(str(transcript.path))
    t.poll(1000.0)
    return t


class TestTranscriptTail:
    def test_tool_use_with_file(self, transcript, tail):
        transcript.append(assistant(tool_use("Read", file_path="D:\\repo\\src\\main.py")))
        assert tail.poll(1001.0) is True
        assert (tail.tool, tail.file) == ("Read", "main.py")
        assert tail.branch == "main"
        assert tail.model_id == "claude-opus-5-5"

    def test_agent_records_subagent_type(self, transcript, tail):
        transcript.append(assistant(tool_use("Agent", subagent_type="Explore", prompt="x")))
        tail.poll(1001.0)
        assert (tail.tool, tail.agent) == ("Agent", "Explore")

    def test_prompt_then_turn_end(self, transcript, tail):
        transcript.append(user("fix the bug"))
        tail.poll(1001.0)
        assert tail.tool == "__prompt__"
        transcript.append(assistant({"type": "text", "text": "Done."}, stop="end_turn"))
        tail.poll(1002.0)
        assert tail.tool == "__waiting__"

    def test_turn_duration_means_waiting(self, transcript, tail):
        transcript.append(assistant(tool_use("Bash", command="ls")),
                          rec("system", subtype="turn_duration"))
        tail.poll(1001.0)
        assert tail.tool == "__waiting__"

    def test_tool_result_does_not_change_activity(self, transcript, tail):
        transcript.append(assistant(tool_use("Bash", command="ls")))
        tail.poll(1001.0)
        transcript.append(user([{"type": "tool_result", "tool_use_id": "toolu_x", "content": "ok"}]))
        assert tail.poll(1002.0) is False
        assert tail.tool == "Bash"
        assert tail.seen_at == 1002.0  # but the session is active

    def test_ignored_user_records(self, transcript, tail):
        transcript.append(assistant(tool_use("Bash", command="ls")),
                          user("<command-name>/model</command-name>"),
                          user("injected context", isMeta=True))
        tail.poll(1001.0)
        assert tail.tool == "Bash"

    def test_interrupt_means_waiting(self, transcript, tail):
        transcript.append(assistant(tool_use("Bash", command="sleep 99")),
                          user([{"type": "text", "text": "[Request interrupted by user]"}]))
        tail.poll(1001.0)
        assert tail.tool == "__waiting__"

    def test_sidechain_records_ignored(self, transcript, tail):
        side = assistant(tool_use("Write", file_path="x.py"))
        side["isSidechain"] = True
        transcript.append(side)
        tail.poll(1001.0)
        assert tail.tool == ""

    def test_compact_boundary_recorded(self, transcript, tail):
        transcript.append(rec("system", subtype="compact_boundary"))
        tail.poll(1005.0)
        assert tail.compact_done_at == 1005.0

    def test_partial_line_completes_on_next_poll(self, transcript, tail):
        line = dumps(assistant(tool_use("Edit", file_path="a.py")))
        transcript.append(raw=line[:30])
        tail.poll(1001.0)
        assert tail.tool == ""
        transcript.append(raw=line[30:] + "\n")
        tail.poll(1002.0)
        assert (tail.tool, tail.file) == ("Edit", "a.py")

    def test_bootstrap_reads_only_the_end(self, transcript, monkeypatch):
        monkeypatch.setattr(activity, "TAIL_BOOTSTRAP_BYTES", 2048)
        filler = dumps(user([{"type": "tool_result", "tool_use_id": "t", "content": "x" * 100}]))
        transcript.append(assistant(tool_use("Grep", pattern="old")))
        transcript.append(raw=(filler + "\n") * 100)
        transcript.append(assistant(tool_use("Write", file_path="new.py")))
        t = TranscriptTail(str(transcript.path))
        t.poll(5000.0)
        assert (t.tool, t.file) == ("Write", "new.py")

    def test_bootstrap_uses_file_mtime_not_now(self, transcript):
        transcript.append(assistant(tool_use("Read", file_path="a.py")))
        os.utime(transcript.path, (1000.0, 1000.0))
        t = TranscriptTail(str(transcript.path))
        t.poll(99999.0)
        assert t.seen_at == 1000.0  # an old transcript must not look active

    def test_truncated_file_restarts(self, transcript, tail):
        transcript.append(assistant(tool_use("Read", file_path="a.py")))
        tail.poll(1001.0)
        transcript.path.write_text(dumps(assistant(tool_use("Glob", pattern="*"))) + "\n", encoding="utf-8")
        tail.poll(1002.0)
        assert tail.tool == "Glob"

    def test_oversized_unfinished_line_dropped(self, transcript, tail, monkeypatch):
        monkeypatch.setattr(activity, "MAX_LINE_BYTES", 1000)
        transcript.append(raw='{"type":"user","junk":"' + "y" * 5000)
        tail.poll(1001.0)
        assert tail._partial == b""
        transcript.append(raw='"}\n' + dumps(assistant(tool_use("Bash", command="ls"))) + "\n")
        tail.poll(1002.0)
        assert tail.tool == "Bash"

    def test_missing_file_is_harmless(self, tmp_path):
        t = TranscriptTail(str(tmp_path / "gone.jsonl"))
        assert t.poll(1.0) is False
        assert t.tool == ""

    def test_background_subagents_count_as_delegating(self, transcript, tail):
        # Layout written by Claude Code 2.1.283: <session>/subagents/agent-<id>.jsonl + .meta.json
        subagents = transcript.path.with_suffix("") / "subagents"
        subagents.mkdir(parents=True)
        for agent_id, agent_type, mtime in (("a1", "Explore", 995.0), ("a2", "Plan", 900.0)):
            (subagents / f"agent-{agent_id}.jsonl").write_text("{}\n", encoding="utf-8")
            (subagents / f"agent-{agent_id}.meta.json").write_text(
                json.dumps({"agentType": agent_type}), encoding="utf-8")
            os.utime(subagents / f"agent-{agent_id}.jsonl", (mtime, mtime))
        transcript.append(assistant({"type": "text", "text": "launched"}, stop="end_turn"))
        tail.poll(1000.0)
        tail.scan_subagents(1000.0)
        assert tail.tool == "__waiting__"
        assert tail.subagents_active == ["Explore"]  # a2 last wrote 100 s ago
        assert tail.subagent_seen_at == 995.0
        assert tail.effective_tool() == "Agent"
        tail.scan_subagents(1000.0 + activity.SUBAGENT_ACTIVE_WINDOW + 1)
        assert tail.effective_tool() == "__waiting__"

    def test_no_subagents_dir(self, tail):
        tail.scan_subagents(1000.0)
        assert tail.subagents_active == [] and tail.subagent_seen_at == 0.0

    def test_corrupt_line_skipped(self, transcript, tail):
        transcript.append(raw='{"type":"assistant", not json\n')
        transcript.append(assistant(tool_use("Edit", file_path="b.py")))
        tail.poll(1001.0)
        assert tail.file == "b.py"
