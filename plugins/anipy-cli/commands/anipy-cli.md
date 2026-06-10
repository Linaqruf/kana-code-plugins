---
description: Search, play, download, or manage anime via anipy-cli on Windows (auto-repairs missing dependencies)
argument-hint: "[action and query, e.g. play frieren ep 1 sub]"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

Parse the user's intent from: $ARGUMENTS

Use the anipy-cli skill for all operational knowledge — CLI flags, setup procedures, player routing, configuration, and troubleshooting. Run all anipy-cli operations through the Bash tool (this command is tool-gated to it, and the skill's procedures assume Git Bash semantics).

## Execution First, Fix on Failure

Do NOT check dependencies upfront. Run the anipy-cli command directly first. Only if it fails, diagnose and repair using the skill's Dependency Repair Chain. Two rules always apply, even if the skill content is unavailable:

- For each missing dependency, use `AskUserQuestion` to confirm before installing — never install silently.
- If uv installation fails via both `pwsh.exe` and `powershell.exe`, **STOP**. Tell the user: "uv could not be installed because PowerShell is not working correctly. Install PowerShell 7 from the Microsoft Store, restart your terminal, and try again."

## Execution

Interpret the user's natural language request and map to the appropriate anipy-cli command.

**Always prefix commands with** `PYTHONIOENCODING=utf-8` **and suffix with** `2>&1`. Without the prefix, the progress spinner dumps a non-fatal `UnicodeEncodeError` traceback into the output — and printing a non-ASCII anime title can crash the command for real (main-thread encoding error).

**Timeouts:** Use 60s for search/play commands, 120s for downloads.

**Always use `-s` flag** for non-interactive search: `anipy-cli -s "query:episode:sub/dub"`

**Mapping examples:**
- "play frieren ep 1" → `PYTHONIOENCODING=utf-8 anipy-cli -s "frieren:1:sub" 2>&1`
- "play steins gate episode 3 dubbed" → `PYTHONIOENCODING=utf-8 anipy-cli -s "steins gate:3:dub" 2>&1`
- "download one piece 1-10" → `PYTHONIOENCODING=utf-8 anipy-cli -D -s "one piece:1-10:sub" 2>&1`
- "download frieren 1-3 to D:\anime" → `PYTHONIOENCODING=utf-8 anipy-cli -D -l "D:/anime" -s "frieren:1-3:sub" 2>&1`
- "binge spy x family 1-5 dub" → `PYTHONIOENCODING=utf-8 anipy-cli -B -s "spy x family:1-5:dub" 2>&1`
- "play frieren 1-3 and 7" → `PYTHONIOENCODING=utf-8 anipy-cli -s "frieren:1-3 7:sub" 2>&1` (multi-range)
- "show history" → read `history.json` from anipy-cli's `user_files_path` (do NOT use `-H`, it is interactive and will hang)
- "migrate my history to the current provider" → `PYTHONIOENCODING=utf-8 anipy-cli --migrate-history 2>&1`
- "what version" → `anipy-cli --version 2>&1`
- "change player to vlc" → read and edit config.yaml player_path
- "set quality to 720p" → add `-q 720` to the next play/download command

**Defaults when not specified:**
- sub/dub: `sub`
- quality: `best`
- player: whatever is in config

**After search/play commands:** Check the output for the anime title that was matched. The `-s` flag auto-selects the first search result. If the matched title looks significantly different from what the user requested, inform the user which anime was found and ask if it is correct.

## Error Recovery

A command has failed if **any** of these are true:
- Non-zero exit code
- Output contains error keywords ("command not found", "PlayerError", "fatal error", "not found")
- Output is unexpectedly empty (search/play produced no stream URL or meaningful content)
- For downloads: file was not created or is zero bytes

**Exit codes are unreliable**: anipy-cli exits 0 even on fatal errors (verified live) — always check the output keywords, never trust the exit code alone.

When a failure is detected (max 2 retries before giving up):
1. Read the error message from combined stdout+stderr
2. Consult the anipy-cli skill's troubleshooting section
3. Attempt to fix (e.g., update config, install missing dep)
4. Retry the original command
5. If still failing after retries, explain the full error chain to the user

**Provider-drift self-repair:** if search matched a title but stream extraction then failed with `A fatal error of type [...]` (e.g., `'NoneType' object is not subscriptable`), suspect provider drift — the provider's API changed under the installed version. The traceback is not in the output: read the log file at the "Logs can be found at <path>" location printed with the error and confirm the crash is inside `anipy_api/provider/...`. Then ask the user (AskUserQuestion) to upgrade with `uv tool upgrade anipy-cli` and retry the original command once. Upstream patches provider breakage frequently, so the upgrade usually fixes it.

**Ignore these non-fatal messages:**
- `UserWarning: color, on_color and attrs are not supported` — yaspin TTY warning
- A `UnicodeEncodeError` traceback from the spinner thread (stack mentions `_spin` / yaspin) — cosmetic background-thread crash; the command continues and exits normally. Add the `PYTHONIOENCODING=utf-8` prefix on the next invocation.
- `SyntaxWarning: 'return' in a 'finally' block` — upstream code issue
- `EOFError: EOF when reading a line` — only non-fatal if output also contains a stream URL or "Playing" indication. If EOFError is the only output or appears before any stream/play activity, treat it as a real failure (command likely ran in interactive mode without `-s`)
- Raw ANSI codes like `[34m`, `[0m` — display artifacts
