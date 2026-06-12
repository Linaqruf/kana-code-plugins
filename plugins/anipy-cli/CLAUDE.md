# anipy-cli — Developer Notes

Claude Code interface for anime streaming/downloading via anipy-cli on Windows.
v1.0.0. Prompt-only plugin (no code).

## Architecture & layering contract

```
commands/anipy-cli.md     → /anipy-cli: intent parsing, NL→CLI mapping,
                            result verification, minimal safety net
skills/anipy-cli/
  SKILL.md                → operational knowledge OWNER: repair chain, flags,
                            player routing, config, safe-execution policy
  references/
    setup-guide.md        → exact install commands (uv, scoop, mpv, vlc)
    troubleshooting.md    → Windows error catalog
```

The command always defers to the skill ("use the anipy-cli skill for all
operational knowledge") — do not re-duplicate skill content into the command.
Exception (deliberate defensive redundancy): the command keeps the
AskUserQuestion-before-install rule and the uv/PowerShell STOP message, because
those are safety-critical even if skill loading ever fails.

## Key invariants

1. **Bash tool only (Git Bash).** Claude Code's Bash tool on Windows executes
   the installed Git Bash (MSYS2) — verified `x86_64-pc-msys`. All procedures
   assume MSYS2 semantics (`/c/...`, `~/.local/bin`, `2>/dev/null`). The
   command enforces this via `allowed-tools` (no PowerShell); the skill states
   it as guidance (skills cannot gate tools). PowerShell is not a supported
   path — its env syntax differs and the repair flows are MSYS2-only.
2. **Non-interactive only.** Every anipy-cli call uses `-s`. Interactive modes
   (`-H/-S/-A/-M`, and untested `-ss`) hang Claude Code's Bash tool. History is
   read from `history.json`, never via `-H`.
3. **`PYTHONIOENCODING=utf-8` serves two purposes.** Verified on 3.8.8 /
   Python 3.14 (cp1252 pipes): the yaspin spinner crash is a background-thread
   UnicodeEncodeError — cosmetic, the main command completes and exits 0
   (on the command's non-fatal ignore list, scoped to `_spin`). But non-ASCII
   anime titles printed by the MAIN thread can raise the same error fatally —
   so the prefix is mandated on every invocation, and only the spinner-thread
   variant may ever be ignored.
4. **Execution first, fix on failure** — never check deps upfront; never
   install or upgrade without AskUserQuestion confirmation. The repair chain
   covers both missing deps AND provider drift (installed-but-broken: provider
   API changes crash stream extraction → `uv tool upgrade anipy-cli` → retry
   once). Verified live: 3.8.8 → 3.8.12 fixed an allanime drift TypeError.
5. **Exit codes are unreliable.** anipy-cli exits 0 even on fatal errors
   (verified live) — failure detection must use output keywords ("fatal
   error", "PlayerError", …), never exit codes alone.
6. **Player priority**: mpv > vlc > mpvnet. Config edited via the path from
   `anipy-cli --config-path` (beware: `player_path` also appears in comments —
   match the real key, see troubleshooting.md).

## Verification provenance

Content verified 2026-06-11 against installed anipy-cli **3.8.8** (uv tool venv,
Python 3.14, Windows 11): full `--help` flag audit, config keys (incl. the
`preferred_type: null` interactive-prompt hazard), history.json path, and a live
no-prefix spinner-crash test (nonsense query; nothing played). MAL/AniList/
seasonal flags (`-a`, `--mal-*`, `--anilist-*`) reviewed and deliberately
excluded as interactive-mode-only. When a new anipy-cli major lands, re-audit
`--help` against SKILL.md's tables.

## Release checklist

- Bump `plugin.json` AND the marketplace entry in
  `../../.claude-plugin/marketplace.json` — versions AND descriptions must match.
- `claude plugin validate . --strict` from the repo root must pass. (Plugin-level
  `--strict` warns about this CLAUDE.md — accepted advisory, same pattern as
  kana-code-rpc; this file is repo documentation, not shipped context.)
