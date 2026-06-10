# anipy-cli

Claude Code plugin that provides a natural language interface for
[anipy-cli](https://github.com/sdaqo/anipy-cli) — search, play, download, and
manage anime from the terminal on Windows.

```
/anipy-cli play frieren ep 1 sub
"watch steins gate episode 3 dubbed"     ← also triggers via natural language
```

## Features

- **Natural language mapping**: "play frieren ep 1 sub" → `anipy-cli -s "frieren:1:sub"`
- **Self-healing dependencies**: installs uv, anipy-cli, mpv/vlc only when a
  command fails — never upfront, never without asking you first. Also detects
  provider drift (a provider API change crashing stream extraction) and offers
  `uv tool upgrade anipy-cli` as the fix
- **Player routing**: mpv > vlc > mpvnet, auto-configured in anipy-cli's `config.yaml`
- **Non-interactive by design**: every call uses the `-s` flag; interactive
  modes that would hang Claude Code (`-H`, `-S`, `-A`, `-M`) are avoided
  (history is read from `history.json` directly)
- **Download & binge modes**: episode ranges (including multi-range
  `1-3 7-12`), quality selection, per-invocation download location (`-l`)
- **Windows-specific**: handles cp1252 encoding quirks, PATH-lag after
  installs, and broken PowerShell 5 security modules

## Prerequisites

- **Windows with Git Bash** (ships with [Git for Windows](https://git-scm.com/download/win)).
  Claude Code's Bash tool on Windows runs the installed Git Bash (MSYS2) — it is
  not bundled — and this plugin's commands and repair flows assume MSYS2 path
  semantics (`/c/...`, `~/.local/bin`). WSL bash will not work.
- Everything else is auto-installed on first failure, with your confirmation:
  [uv](https://docs.astral.sh/uv/), anipy-cli (any 3.x), and a video player
  (mpv via scoop, or VLC)

## Installation

```bash
/plugin marketplace add Linaqruf/kana-code-plugins
/plugin install anipy-cli@kana-code-plugins
```

## Usage

```bash
/anipy-cli play frieren ep 1 sub
/anipy-cli download one piece 1-10 dub
/anipy-cli download frieren 1-3 to D:/anime
/anipy-cli binge spy x family 1-5 dub
/anipy-cli show history
/anipy-cli continue watching frieren
/anipy-cli change player to vlc
/anipy-cli migrate my history
```

Or just talk: "play anime steins gate episode 5", "what's in my anime history".

## How it works

| Layer | Role |
|-------|------|
| `/anipy-cli` command | Parses intent, maps to CLI invocations, verifies results |
| `anipy-cli` skill | Operational knowledge: flags, repair chain, player routing, config |
| `references/setup-guide.md` | Exact install commands (uv, scoop, mpv, VLC) |
| `references/troubleshooting.md` | Windows error catalog and fixes |

Dependency philosophy: **execution first, fix on failure**. Commands run
immediately; missing tools are diagnosed from the failure and installed only
after you confirm via a prompt.

## Debugging

- `anipy-cli --config-path` — locate `config.yaml` (player, download folder, providers)
- History lives at `<user_files_path>/history.json`
- Verbose runs: `-VVV` (full info), `--stack-always` (always show stack traces)
- A `UnicodeEncodeError` traceback mentioning `_spin` in command output is the
  progress spinner crashing cosmetically (cp1252 pipes on Python ≤3.14) — the
  command still succeeded; the `PYTHONIOENCODING=utf-8` prefix suppresses it

## Limitations

- Windows only (by design — paths, players, and fixes are Windows-specific)
- One provider configured by default (allanime); availability varies by region
- Seasonal/MAL/AniList modes are interactive-only upstream and not supported

## License

MIT
