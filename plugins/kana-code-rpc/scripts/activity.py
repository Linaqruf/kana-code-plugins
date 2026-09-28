"""
Current activity of a Claude Code session, read from its transcript.

The daemon tails each session's transcript (JSONL, one record per line)
instead of running a hook on every tool call. A tool call therefore costs the
plugin nothing, however many subagents run in parallel. The records used here:

- assistant record, `tool_use` block  -> the tool (and file, or subagent type)
- assistant record, stop_reason `end_turn`, or system `turn_duration`
                                      -> waiting for input
- user record with a real prompt      -> thinking
- user record "[Request interrupted"  -> waiting for input
- system `compact_boundary`           -> compaction finished

Every record also carries `gitBranch`, so no git process is needed either.
"""

import json
import os
import re
from pathlib import Path

# Display names for tools. A tool not listed here shows as "Working", and
# `mcp__*` tools show as "Using MCP", so a new Claude Code tool degrades
# gracefully instead of breaking anything.
TOOL_DISPLAY = {
    # Files
    "Edit": "Editing",
    "Write": "Writing",
    "Read": "Reading",
    "NotebookEdit": "Editing",
    "NotebookRead": "Reading",
    "Glob": "Searching",
    "Grep": "Grepping",
    "LS": "Browsing",
    "LSP": "Inspecting code",
    # Execution
    "Bash": "Running",
    "PowerShell": "Running",
    "Monitor": "Monitoring",
    # Delegation & orchestration
    "Agent": "Delegating",
    "Task": "Delegating",  # older name of Agent, kept for old transcripts
    "SendMessage": "Delegating",
    "ListAgents": "Delegating",
    "Workflow": "Orchestrating",
    # Web
    "WebFetch": "Fetching",
    "WebSearch": "Researching",
    # Interaction
    "AskUserQuestion": "Asking",
    # Planning & task lists
    "TodoRead": "Reviewing",
    "TodoWrite": "Planning",
    "EnterPlanMode": "Planning",
    "ExitPlanMode": "Planning",
    "TaskCreate": "Planning",
    "TaskUpdate": "Planning",
    "TaskList": "Reviewing",
    "TaskGet": "Reviewing",
    "TaskOutput": "Reviewing",
    "TaskStop": "Managing",
    # Skills, search, scheduling, publishing
    "Skill": "Running",
    "ToolSearch": "Searching",
    "CronCreate": "Scheduling",
    "CronDelete": "Scheduling",
    "CronList": "Scheduling",
    "ScheduleWakeup": "Scheduling",
    "Artifact": "Publishing",
    "EnterWorktree": "Managing",
    "ExitWorktree": "Managing",
}

# Pseudo-tools: states that are not a tool call. Kept out of TOOL_DISPLAY.
PSEUDO_TOOL_DISPLAY = {
    "__prompt__": "Thinking",
    "__compact__": "Compacting context",
    "__waiting__": "Waiting for input",
}

# Tools whose input names a file worth showing ("Editing main.py")
FILE_TOOLS = {"Edit", "Write", "Read", "NotebookEdit", "NotebookRead"}

# Tools that start a subagent ("Delegating to Explore")
DELEGATE_TOOLS = {"Agent", "Task"}


def activity_label(tool: str) -> str:
    """Display verb for a tool or pseudo-tool; '' for no activity."""
    if not tool:
        return ""
    if tool in PSEUDO_TOOL_DISPLAY:
        return PSEUDO_TOOL_DISPLAY[tool]
    if tool in TOOL_DISPLAY:
        return TOOL_DISPLAY[tool]
    if tool.startswith("mcp__"):
        return "Using MCP"
    return "Working"


_CONTEXT_SUFFIX = re.compile(r"\[(\d+)([km])\]$", re.IGNORECASE)
_DATE_SUFFIX = re.compile(r"-\d{8}$")


def model_display_name(model_id: str) -> str:
    """Readable name from a model ID, without a list of known models.

    claude-opus-5-5 -> "Opus 5.5", claude-haiku-4-5-20251001 -> "Haiku 4.5",
    claude-sonnet-5 -> "Sonnet 5", claude-opus-5-5[1m] -> "Opus 5.5 (1M context)",
    claude-3-5-sonnet-20241022 -> "Sonnet 3.5". An ID of another shape is
    returned unchanged; placeholders such as "<synthetic>" return ''.
    """
    if not model_id or model_id.startswith("<"):
        return ""
    ident = model_id.strip()
    suffix = ""
    m = _CONTEXT_SUFFIX.search(ident)
    if m:
        suffix = f" ({m.group(1)}{m.group(2).upper()} context)"
        ident = ident[:m.start()]
    ident = _DATE_SUFFIX.sub("", ident)
    parts = [p for p in ident.split("-") if p]
    if parts and parts[0].lower() == "claude":
        parts = parts[1:]
    words = [p for p in parts if p.isalpha()]
    numbers = [p for p in parts if p.isdigit()]
    if len(words) != 1 or len(words) + len(numbers) != len(parts):
        return model_id[:40]
    name = words[0].capitalize()
    return (f"{name} {'.'.join(numbers)}" if numbers else name) + suffix


# Transcripts reach gigabytes; never read one from the start.
TAIL_BOOTSTRAP_BYTES = 64 * 1024   # read on first open, from the end
MAX_READ_BYTES = 4 * 1024 * 1024   # per poll; a bigger backlog is skipped
MAX_LINE_BYTES = 8 * 1024 * 1024   # a longer unfinished line is dropped

# A subagent counts as running while its transcript grew this recently
SUBAGENT_ACTIVE_WINDOW = 15

# Local slash commands (/model, /resume, ...) echo into the transcript as user
# records, but no model turn follows them.
_LOCAL_COMMAND_PREFIXES = ("<command-name>", "<command-message>", "<local-command")


def _prompt_text(content) -> str | None:
    """Text of a user record if it is a prompt, else None (tool results)."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return None
    texts = []
    for block in content:
        if not isinstance(block, dict):
            continue
        kind = block.get("type")
        if kind == "tool_result":
            return None
        if kind == "text":
            texts.append(block.get("text") or "")
        elif kind == "image":
            texts.append("[image]")
    return "\n".join(texts) if texts else None


class TranscriptTail:
    """Follows one transcript file and keeps its latest activity.

    Opens and closes the file on every poll, so it never holds a handle that
    could block Claude Code from rotating or deleting the file.
    """

    def __init__(self, path: str):
        self.path = path
        self.offset: int | None = None
        self._partial = b""
        self._skip_to_newline = False
        self.tool = ""        # tool name or pseudo-tool
        self.file = ""        # basename, for FILE_TOOLS
        self.agent = ""       # subagent type, for DELEGATE_TOOLS
        self.branch = ""
        self.model_id = ""
        self.seen_at = 0.0         # local time a new line was last read
        self.changed_at = 0.0      # local time `tool` was last set
        self.compact_done_at = 0.0
        self.subagents_active: list[str] = []  # agent types of running subagents
        self.subagent_seen_at = 0.0            # last write to any subagent transcript
        self._agent_types: dict[str, str] = {}

    def scan_subagents(self, now: float):
        """Find subagents that are still working.

        Agent calls run in the background by default: the main transcript
        ends its turn at once and hears back later through
        <task-notification> prompts. Each subagent writes its own transcript
        to <session>/subagents/agent-<id>.jsonl, next to a meta.json that
        names its type. A directory listing gives their mtimes without
        opening them.
        """
        directory = Path(self.path).with_suffix("") / "subagents"
        active, latest = [], 0.0
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    if not entry.name.endswith(".jsonl"):
                        continue
                    mtime = entry.stat().st_mtime
                    latest = max(latest, mtime)
                    if now - mtime <= SUBAGENT_ACTIVE_WINDOW:
                        active.append(self._agent_type(directory, entry.name))
        except OSError:
            pass
        self.subagents_active = active
        self.subagent_seen_at = min(latest, now)

    def _agent_type(self, directory: Path, name: str) -> str:
        if name in self._agent_types:
            return self._agent_types[name]
        try:
            meta = json.loads((directory / (name[:-len(".jsonl")] + ".meta.json"))
                              .read_text(encoding="utf-8"))
            agent_type = str(meta.get("agentType") or "")
        except (OSError, ValueError, AttributeError):
            agent_type = ""
        if agent_type:
            self._agent_types[name] = agent_type  # meta.json may lag; retry until it exists
        return agent_type or "agent"

    def effective_tool(self) -> str:
        """`tool`, except that a waiting main thread with subagents still
        running is delegating, not waiting."""
        if self.tool == "__waiting__" and self.subagents_active:
            return "Agent"
        return self.tool

    def poll(self, now: float) -> bool:
        """Read what was appended since the last poll. True if `tool`,
        `file` or `agent` changed."""
        try:
            st = os.stat(self.path)
        except OSError:
            return False
        size = st.st_size
        # Lines from a catch-up read (first open, or a skipped backlog) are
        # stamped with the file's mtime, not `now`: an old transcript must
        # not look active just because the daemon has only now read it.
        stamp = now
        if self.offset is None or size < self.offset:
            # First open, or the file was truncated or replaced: start near the end
            self.offset = max(0, size - TAIL_BOOTSTRAP_BYTES)
            self._partial = b""
            self._skip_to_newline = self.offset > 0
            stamp = min(now, st.st_mtime)
        if size == self.offset:
            return False
        if size - self.offset > MAX_READ_BYTES:
            self.offset = size - TAIL_BOOTSTRAP_BYTES
            self._partial = b""
            self._skip_to_newline = True
            stamp = min(now, st.st_mtime)
        try:
            with open(self.path, "rb") as f:
                f.seek(self.offset)
                data = f.read(size - self.offset)
        except OSError:
            return False
        self.offset += len(data)
        return self._feed(data, stamp)

    def _feed(self, data: bytes, now: float) -> bool:
        buf = self._partial + data
        if self._skip_to_newline:
            cut = buf.find(b"\n")
            if cut == -1:
                self._partial = b""
                return False
            buf = buf[cut + 1:]
            self._skip_to_newline = False
        lines = buf.split(b"\n")
        self._partial = lines.pop()
        if len(self._partial) > MAX_LINE_BYTES:
            self._partial = b""
            self._skip_to_newline = True

        before = (self.tool, self.file, self.agent)
        for line in lines:
            if line.strip():
                self.seen_at = now
                self._handle_line(line, now)
        return (self.tool, self.file, self.agent) != before

    def _set(self, now: float, tool: str, file: str = "", agent: str = ""):
        self.tool, self.file, self.agent = tool, file, agent
        self.changed_at = now

    def _handle_line(self, line: bytes, now: float):
        # Cheap substring checks first: most bytes in a transcript are tool
        # results, and those never change the activity.
        if b'"type":"assistant"' in line:
            pass
        elif b'"type":"user"' in line:
            if b'"tool_result"' in line:
                return
        elif b'"type":"system"' in line:
            if b'"turn_duration"' not in line and b'"compact_boundary"' not in line:
                return
        else:
            return
        try:
            record = json.loads(line)
        except (ValueError, UnicodeDecodeError):
            return
        if not isinstance(record, dict) or record.get("isSidechain"):
            return
        branch = record.get("gitBranch")
        if isinstance(branch, str) and branch and branch != "HEAD":
            self.branch = branch
        kind = record.get("type")
        message = record.get("message") if isinstance(record.get("message"), dict) else {}

        if kind == "assistant":
            model = message.get("model")
            if isinstance(model, str) and model and not model.startswith("<"):
                self.model_id = model
            saw_tool = False
            for block in message.get("content") or []:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                saw_tool = True
                name = block.get("name") or ""
                tool_input = block.get("input") if isinstance(block.get("input"), dict) else {}
                file = agent = ""
                if name in FILE_TOOLS:
                    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
                    if isinstance(path, str) and path:
                        file = Path(path.replace("\\", "/")).name
                elif name in DELEGATE_TOOLS:
                    agent = str(tool_input.get("subagent_type") or "")
                self._set(now, name, file, agent)
            if not saw_tool and message.get("stop_reason") == "end_turn":
                self._set(now, "__waiting__")
        elif kind == "user":
            if record.get("isMeta"):
                return
            text = _prompt_text(message.get("content"))
            if text is None:
                return
            stripped = text.lstrip()
            if stripped.startswith("[Request interrupted"):
                self._set(now, "__waiting__")
            elif not stripped.startswith(_LOCAL_COMMAND_PREFIXES):
                self._set(now, "__prompt__")
        elif kind == "system":
            subtype = record.get("subtype")
            if subtype == "turn_duration":
                self._set(now, "__waiting__")
            elif subtype == "compact_boundary":
                self.compact_done_at = now
