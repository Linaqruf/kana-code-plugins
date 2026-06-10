---
name: anipy-cli
description: This skill should be used when the user asks to play, watch, stream, search, download, or binge anime; continue watching or check anime history; install, setup, configure, update, or fix anipy-cli; change video player or set anime quality; troubleshoot anime playback issues; or mentions anipy-cli by name. Triggers on "play anime", "watch frieren", "stream one piece dubbed", "download anime episodes", "binge naruto 1-10", "show anime history", "next episode", "continue watching", "change player to mpv", "set quality to 1080", "anipy-cli not working", "player not found", "anipy-cli", "anime from terminal".
version: 0.2.0
---

# anipy-cli — Anime Streaming via Claude Code

## Overview

anipy-cli is a Python CLI tool for searching, streaming, and downloading anime. This skill enables Claude Code to act as a natural language interface for anipy-cli on Windows, handling dependency management, player routing, and all CLI operations non-interactively.

## Shell Requirement: the Bash Tool (Git Bash)

Run all anipy-cli operations through the **Bash tool**. On Windows, Claude Code's Bash tool executes the installed **Git Bash (MSYS2)** — it is a real prerequisite, not bundled. Every procedure in this skill and its references assumes MSYS2 semantics: `/c/...` drive paths, `~/.local/bin`, `2>/dev/null`.

**PowerShell is NOT a working alternative.** The setup and repair flows only work in Git Bash. If a single bare invocation must run in PowerShell for some reason, the env-prefix form is `$env:PYTHONIOENCODING='utf-8'; anipy-cli ... 2>&1` — bare invocations only; switch back to the Bash tool for everything else.

## Dependency Repair Chain

When a command fails due to a missing dependency, diagnose and repair using this chain. Do NOT run these checks upfront — only when a failure occurs. Each installation requires `AskUserQuestion` confirmation — never install silently.

**Repair order:**

1. **uv** — `uv --version` → if missing, install (see `references/setup-guide.md` section 1). If both `pwsh.exe` and `powershell.exe` install methods fail, **STOP** and tell the user to install PowerShell 7 from the Microsoft Store, then restart their terminal.
2. **anipy-cli** — `anipy-cli --version` → if missing, `uv tool install anipy-cli`
3. **Video player** — check mpv (`where.exe mpv`), then vlc (`where.exe vlc` + common paths) → if neither found, ask user which to install (see `references/setup-guide.md` sections 3-5)
4. **Config player_path** — run `anipy-cli --config-path` to get the path, then verify the config file exists. If not, run `anipy-cli --version 2>&1` to attempt generation; if config still missing, run a search command like `anipy-cli -s "test:1:sub" 2>&1` to trigger full initialization. Then verify `player_path` matches an installed player, update if needed

**Important**: After installing scoop or any tool, the current shell session may not have updated PATH. Use full paths or `pwsh.exe` to invoke scoop commands. For exact install commands, see `references/setup-guide.md`.

## Non-Interactive CLI Usage

anipy-cli supports non-interactive mode via the `-s` flag, which is essential for Claude Code integration since Claude cannot interact with terminal prompts.

### Search and Play

```
anipy-cli -s "query:episode:sub/dub"
```

**Format:** `{search_term}:{episode_or_range}:{sub|dub}` (default: `sub` when user doesn't specify). Multiple ranges are space-separated within the episode field.

Examples:
- `anipy-cli -s "frieren:1:sub"` — Play Frieren episode 1, subbed
- `anipy-cli -s "steins gate:1:sub"` — Play Steins;Gate episode 1
- `anipy-cli -s "one piece:1-10:dub"` — Binge One Piece episodes 1-10, dubbed
- `anipy-cli -s "spy x family:3:dub"` — Play Spy x Family episode 3, dubbed
- `anipy-cli -s "frieren:1-3 7-12:dub"` — Multi-range: episodes 1-3 and 7-12

### Modes

| Flag | Mode | Description |
|------|------|-------------|
| (none) | Default | Interactive search and play |
| `-s` | Search | Non-interactive search with `query:ep:type` |
| `-D` | Download | Download mode, combine with `-s` |
| `-B` | Binge | Binge mode for episode ranges |
| `-H` | History | Show watch history (interactive — will hang, read history.json instead) |
| `-S` | Seasonal | Seasonal anime tracking (interactive — will hang, do not use) |
| `-A` | AniList | AniList integration (interactive — will hang, do not use) |
| `-M` | MAL | MyAnimeList integration (interactive — will hang, do not use) |

The `-ss "{year}:{season}"` seasonal-search option is untested for interactivity — treat it as interactive-risk and avoid it. The MAL/AniList helper flags (`-a/--auto-update`, `--mal-user`, `--mal-password`, `--mal-sync-to-seasonals`, `--anilist-sync-to-seasonals`) only apply to the interactive modes above and are deliberately not used.

### Common Options

| Flag | Purpose |
|------|---------|
| `-p mpv\|vlc\|syncplay\|mpvnet\|mpv-controlled` | Override player |
| `-q best\|worst\|720\|1080` | Set quality |
| `-l <path>` | Override download location for this invocation ("download to D:/anime") |
| `-f` | Use ffmpeg for m3u8 downloads (more stable, slower) |
| `-so` | Download subtitles only |
| `-v` | Show version |
| `-h` | Show help |
| `-VVV` | Verbose debug output (`-V` = fatal only, `-VVV` = full info) |
| `--stack-always` | Always show stack traces on log output (debug aid alongside `-VVV`) |
| `--config-path` | Print config file path |
| `--delete-history` | Clear history |
| `--migrate-history` | Migrate watch history to the current provider |

### Download Mode

Combine `-D` with `-s` for downloading:
```
anipy-cli -D -s "frieren:1-5:sub"
```

Download location is set in config.yaml under `download_folder_path`.

### Binge Mode

Combine `-B` with `-s` for binge watching:
```
anipy-cli -B -s "frieren:1-5:sub"
```

### History

To view history non-interactively, read `history.json` from the `user_files_path` directory specified in config.yaml. Do NOT use the `-H` flag — it is interactive and will hang in Claude Code's Bash tool. Always discover the config path dynamically via `anipy-cli --config-path`.

If `history.json` does not exist, tell the user "No watch history found."

### Continue Watching

To resume where the user left off:
1. Read `history.json` from `user_files_path` (discover via `anipy-cli --config-path` → read config → get `user_files_path`)
2. Find the entry for the requested anime (match by title)
3. Get the last watched episode number and increment by 1
4. Play the next episode: `anipy-cli -s "title:next_ep:sub" 2>&1`

If the user says "next episode" without specifying an anime, show recent history entries and ask which one to continue.

### Search Tips

The `-s` flag auto-selects the first search result via fuzzy matching. To improve accuracy:
- Use specific titles: `steins gate` not `gate`, `my hero academia` not `hero`
- Romaji titles often match better: `boku no hero academia`
- Include distinguishing words for common titles

## Player Routing

Priority order for player detection and configuration:

1. **mpv** (preferred) — better subtitle rendering, hardware decoding, scriptable
2. **vlc** — widely installed, good fallback
3. **mpvnet** — mpv fork with GUI, Windows-native
4. **mpv-controlled** — reuses existing mpv windows
5. **syncplay** — synchronized playback with others

Note: `iina` is also supported but macOS-only (not relevant for Windows).

When updating config.yaml `player_path`:
- If player is on PATH: use just the name (`mpv`, `vlc`)
- If not on PATH: use full path (`C:\Program Files\VideoLAN\VLC\vlc.exe`)
- Always verify the path resolves before writing config

## Configuration

Always discover the config path dynamically via `anipy-cli --config-path` (typically `C:\Users\<username>\AppData\Local\anipy-cli\config.yaml`).

Key fields:
- `player_path` — video player executable or path
- `download_folder_path` — download directory
- `preferred_type` — `sub` or `dub`. **Warning:** if set to `null`, anipy-cli will prompt interactively for sub/dub choice, which hangs in Claude Code. Always specify `:sub` or `:dub` in the `-s` search string, or set this config value to `sub` or `dub`
- `providers` — anime source providers per mode (default: allanime)
- `mpv_commandline_options` — extra mpv flags
- `vlc_commandline_options` — extra vlc flags

## Safe Execution

- Always use the `PYTHONIOENCODING=utf-8` prefix. Without it, the progress
  spinner crashes with a `UnicodeEncodeError` in a background thread (Bash-tool
  pipes default to cp1252 on Python ≤3.14). The crash is **non-fatal** — the
  command still completes and exits 0 — but it dumps a ~20-line traceback that
  pollutes the output you need to parse. The prefix is output hygiene, not a
  correctness requirement.
- Always add `2>&1` to capture stderr
- Set reasonable timeouts (60s for search/play, 120s for downloads)
- Never run anipy-cli with sudo or admin privileges — it doesn't need them

For Windows-specific errors and solutions, see `references/troubleshooting.md`.

## Additional Resources

### Reference Files

- **`references/setup-guide.md`** — Step-by-step dependency installation flows with exact commands
- **`references/troubleshooting.md`** — Windows-specific issues, error catalog, and solutions
