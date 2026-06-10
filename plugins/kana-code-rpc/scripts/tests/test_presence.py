"""Unit tests for presence.py pure helpers and hooks.json consistency."""
import json
import re
from pathlib import Path

import presence
from presence import (
    EVENT_PSEUDO_TOOLS,
    PSEUDO_TOOL_DISPLAY,
    TOOL_DISPLAY,
    get_project_name,
    repo_web_url,
    truncate_filename,
)
from state import format_tokens

HOOKS_JSON = Path(__file__).resolve().parent.parent.parent / "hooks" / "hooks.json"


class TestRepoWebUrl:
    def test_https_with_git_suffix(self):
        assert repo_web_url("https://github.com/user/repo.git") == "https://github.com/user/repo"

    def test_https_without_suffix(self):
        assert repo_web_url("https://gitlab.com/group/project") == "https://gitlab.com/group/project"

    def test_ssh_scp_form(self):
        assert repo_web_url("git@github.com:user/repo.git") == "https://github.com/user/repo"

    def test_ssh_url_form(self):
        assert repo_web_url("ssh://git@github.com/user/repo.git") == "https://github.com/user/repo"

    def test_empty(self):
        assert repo_web_url("") == ""

    def test_non_url_garbage(self):
        assert repo_web_url("/local/path/to/repo") == ""

    def test_nested_group_path(self):
        assert repo_web_url("git@gitlab.com:group/subgroup/repo.git") == "https://gitlab.com/group/subgroup/repo"


class TestGetProjectName:
    def test_name_from_remote_url(self):
        assert get_project_name("/some/dir", "https://github.com/user/my-repo.git") == "my-repo"

    def test_name_from_ssh_remote(self):
        assert get_project_name("/some/dir", "git@github.com:user/other-repo.git") == "other-repo"

    def test_folder_fallback_when_no_remote(self):
        assert get_project_name("/some/dir/folder-name", "") == "folder-name"


class TestTruncateFilename:
    def test_short_unchanged(self):
        assert truncate_filename("main.py") == "main.py"

    def test_long_preserves_extension(self):
        result = truncate_filename("very_long_component_name_indeed.tsx")
        assert len(result) <= 25
        assert result.endswith(".tsx")
        assert "..." in result

    def test_exactly_at_limit(self):
        name = "a" * 21 + ".tsx"  # 25 chars
        assert truncate_filename(name) == name


class TestFormatTokens:
    def test_small(self):
        assert format_tokens(999) == "999"

    def test_thousands(self):
        assert format_tokens(1500) == "1.5k"

    def test_hundred_thousands(self):
        assert format_tokens(150000) == "150k"

    def test_millions(self):
        assert format_tokens(1_200_000) == "1.2M"


class TestHooksConsistency:
    """Guards against the matcher/TOOL_DISPLAY drift that hid PowerShell
    activity for months — every tool in the PreToolUse matcher must have a
    display name, and every lifecycle event wired in hooks.json must be
    handled by cmd_update."""

    def _hooks(self) -> dict:
        return json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]

    def test_every_matcher_tool_has_display(self):
        hooks = self._hooks()
        matcher = hooks["PreToolUse"][0]["matcher"]
        tools = [t for t in matcher.split("|") if not re.search(r"[.*+?\\]", t)]
        assert len(tools) > 20  # Sanity: the split actually produced the tool list
        missing = [t for t in tools if t not in TOOL_DISPLAY]
        assert not missing, f"Matcher tools without TOOL_DISPLAY entry: {missing}"

    def test_no_display_only_tools(self):
        """Tools in TOOL_DISPLAY but not in the matcher never fire — dead config."""
        hooks = self._hooks()
        matcher = hooks["PreToolUse"][0]["matcher"]
        tools = set(matcher.split("|"))
        dead = [t for t in TOOL_DISPLAY if t not in tools]
        assert not dead, f"TOOL_DISPLAY entries never matched by hooks: {dead}"

    def test_lifecycle_events_have_pseudo_tools(self):
        hooks = self._hooks()
        lifecycle = set(hooks) - {"SessionStart", "SessionEnd", "PreToolUse", "SubagentStop"}
        unhandled = [e for e in lifecycle if e not in EVENT_PSEUDO_TOOLS]
        assert not unhandled, f"Hooked events with no pseudo-tool mapping: {unhandled}"

    def test_pseudo_tools_have_display(self):
        for event, pseudo in EVENT_PSEUDO_TOOLS.items():
            assert pseudo in PSEUDO_TOOL_DISPLAY, f"{event} maps to {pseudo} with no display"

    def test_pseudo_tools_not_in_tool_display(self):
        overlap = set(PSEUDO_TOOL_DISPLAY) & set(TOOL_DISPLAY)
        assert not overlap, f"Pseudo-tools must not leak into TOOL_DISPLAY: {overlap}"


class TestButtonConfig:
    def test_default_config_has_button_settings(self):
        assert presence.DEFAULT_CONFIG["display"]["show_button"] is True
        assert presence.DEFAULT_CONFIG["custom_button_label"] == ""
        assert presence.DEFAULT_CONFIG["custom_button_url"] == ""
