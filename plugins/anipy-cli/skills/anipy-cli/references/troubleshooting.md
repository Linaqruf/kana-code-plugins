# anipy-cli Troubleshooting — Windows

## Encoding and Display Issues

### UnicodeEncodeError with yaspin spinner

**Symptom:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u280b'
```

**Cause:** Piped output on Windows defaults to cp1252 on Python ≤3.14 (UTF-8
becomes the default in 3.15, PEP 686); yaspin's spinner uses Braille Unicode
characters that cp1252 cannot encode.

**Fix:** Prefix all anipy-cli commands with:
```bash
PYTHONIOENCODING=utf-8 anipy-cli ...
```

The spinner variant is cosmetic — verified on 3.8.8: it crashes in a
background thread (`Exception in thread ... (_spin)`) while the main command
completes normally and exits 0. Treat that traceback as a reminder to add the
prefix, not as a command failure. However: a missing prefix can ALSO crash the
MAIN thread when anipy-cli prints non-ASCII titles (e.g. ゼ, ★, —) — that
variant is fatal, and it is why the prefix is mandated on every command.

### ANSI color codes in output

**Symptom:** Raw `[34m`, `[92m`, `[0m` codes in output.

**Cause:** Claude Code's Bash tool doesn't process ANSI escapes.

**Impact:** None — the output is still parseable. Ignore the escape sequences when interpreting results.

## Interactive Mode Issues

### EOFError when running from Claude Code

**Symptom:**
```
A fatal error of type [EOFError] has occurred with message "EOF when reading a line"
```

**Cause:** Claude Code's Bash tool doesn't support interactive stdin. After playback finishes, anipy-cli's interactive menu tries to read user input and fails.

**Impact:** None for playback — the video player still opens and plays correctly. Only the post-play interactive menu (next/prev/replay) fails.

**Workaround:** Always use `-s` flag for non-interactive mode. For sequential operations (next episode), make separate anipy-cli calls.

### History mode (-H) is interactive

**Symptom:** `-H` flag hangs or errors because it requires fzf/menu selection.

**Workaround:** Read the history file directly:
```bash
anipy-cli --config-path  # get user_files_path
# Then read: <user_files_path>/history.json
```

## Player Issues

### PlayerError: Executable not found

**Symptom:**
```
A fatal error of type [PlayerError] has occurred with message "Executable mpv was not found"
```

**Cause:** Player not on PATH or wrong `player_path` in config.

**Fix:**
1. Check if player exists: `where.exe mpv` or `where.exe vlc`
2. Check common install locations for VLC
3. Update config.yaml `player_path` to correct value
4. If using full path in config, use Windows-style backslashes: `C:\Program Files\VideoLAN\VLC\vlc.exe`

### Player opens but no video

**Possible causes:**
- Network/firewall blocking stream URLs
- Antivirus blocking mpv/vlc network access
- Provider returning dead links

**Debug:** Run with `-VVV` (full verbose) to see extracted URLs and debug info. Note: `-V` alone only shows fatal-level messages, `-VVV` gives full info output:
```bash
PYTHONIOENCODING=utf-8 anipy-cli -VVV -s "test:1:sub" 2>&1
```

## Installation Issues

### PowerShell security module broken

**Symptom:**
```
The 'Set-ExecutionPolicy' command was found in the module 'Microsoft.PowerShell.Security', but the module could not be loaded.
```

**Cause:** Corrupted PowerShell 5 installation on Windows 11.

**Fix:** Use PowerShell 7 (`pwsh.exe`) instead of `powershell.exe`:
```bash
pwsh.exe -NoProfile -Command "irm get.scoop.sh | iex"
```

If `pwsh.exe` not available, install from Microsoft Store: "PowerShell" by Microsoft.

### Scoop not found after install

**Symptom:** `scoop: command not found` in bash after installing scoop.

**Cause:** Scoop adds itself to PATH but the current bash session doesn't pick it up.

**Fix:** Use full paths for scoop:
```bash
pwsh.exe -NoProfile -Command "& $env:USERPROFILE\scoop\shims\scoop.ps1 install mpv"
```

Or restart the terminal to refresh PATH.

### uv tool install fails

**Possible causes:**
- Network issues
- Python version incompatibility
- Corrupted uv cache

**Fix:**
```bash
# Clear cache and retry
uv cache clean
uv tool install anipy-cli

# If Python version issue, specify version
uv tool install anipy-cli --python 3.12
```

### mpv in extras bucket not found

**Symptom:** `Couldn't find manifest for 'mpv'`

**Cause:** Scoop extras bucket not added.

**Fix:**
```bash
pwsh.exe -NoProfile -Command "& $env:USERPROFILE\scoop\shims\scoop.ps1 bucket add extras"
# Then retry install
```

## Config Issues

### Multiple player_path entries in config

**Symptom:** Editing config changes wrong line.

**Cause:** config.yaml has `player_path` in both comments (examples) and actual config. There are typically 2+ occurrences.

**Fix:** When editing, match the specific line after the comments block:
```yaml
#     player_path: mpv-controlled # recycle your mpv windows!
player_path: mpv    # <-- THIS is the actual config line
```

Use enough surrounding context in the Edit tool to uniquely identify the correct line.

### Config not generated yet

After `uv tool install`, the config file does not exist until anipy-cli's first actual run. `anipy-cli --config-path` only prints the expected path — it does NOT generate the config.

**Fix:** Run any anipy-cli command to trigger config generation:
```bash
PYTHONIOENCODING=utf-8 anipy-cli --version 2>&1
```
Then verify the config file exists before attempting to edit it. If the file still doesn't exist at the expected path, the user may need to run a search command (e.g., `anipy-cli -s "test:1:sub"`) to trigger full initialization.

## Provider Issues

### Stream extraction crashes: 'NoneType' object is not subscriptable

**Symptom:**
```
A fatal error of type [TypeError] has occurred with message "'NoneType' object is not subscriptable". Logs can be found at C:\Users\<username>\AppData\Local\anipy-cli\logs.
```
Search succeeds (a title is matched), then the "Extracting streams" phase dies. The log file shows a traceback through `anipy_api/provider/providers/...` (e.g., `allanime_provider.py` in `get_video`).

**Cause:** The anime provider changed its API and the installed anipy-cli can no longer parse its responses. Verified live 2026-06-11: 3.8.8 failed against allanime with exactly this error; upgrading to 3.8.12 fixed it immediately. Upstream tracks provider breakage closely — patch releases are frequent, so an installed version goes stale within months.

**Fix** (confirm with the user first):
```bash
uv tool upgrade anipy-cli
```
Then retry the original command once. If it still fails after upgrading, the provider may be down or the fix not yet released — check https://github.com/sdaqo/anipy-cli/issues and try again later, or try alternative search terms.

**Important:** anipy-cli exits 0 even on fatal errors — detect this failure by the "fatal error" text in output, never by exit code.

### No streams found

**Symptom:** Search works but no playable links extracted.

**Possible causes:**
- Provider (allanime) temporarily down
- Anime not available on provider
- Regional blocking

**Workaround:** Check if anime exists on the provider's website manually. Try alternative search terms (romaji vs english title).

### Search returns wrong anime

**Cause:** Fuzzy search matching. Short or common terms may match wrong titles.

**Fix:** Use more specific search terms:
- Instead of `gate` → use `steins gate`
- Instead of `hero` → use `my hero academia`
- Use romaji titles for better matches: `boku no hero academia`

## Performance

### Slow stream extraction

Stream extraction can take 10-30 seconds depending on provider response time. This is normal.

### Downloads very slow

**Fix:** Install yt-dlp for faster HLS downloading:
```bash
uv tool install yt-dlp
# or via scoop
pwsh.exe -NoProfile -Command "& $env:USERPROFILE\scoop\shims\scoop.ps1 install yt-dlp"
```

Without yt-dlp, anipy-cli uses its internal downloader or ffmpeg, which can be slower for m3u8 playlists.

## Security Notes

- anipy-cli does NOT require admin/elevated privileges
- All installations (uv, scoop, anipy-cli) are user-scoped, no system modification
- Never run with `sudo` or admin PowerShell unless explicitly needed
- Config files are in user-local directories only
- No credentials stored unless user configures MAL/AniList tokens
