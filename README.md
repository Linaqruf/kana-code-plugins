# kana-code-plugins

Claude Code plugins by [Linaqruf](https://github.com/Linaqruf) — a personal
marketplace of four plugins, each rebuilt in mid-2026 through an adversarial
design-review loop (every plugin's plan and implementation passed independent
review before merging).

## Install

```
/plugin marketplace add Linaqruf/kana-code-plugins
/plugin install <plugin-name>@kana-code-plugins
```

## Plugins

| Plugin | Version | What it does |
|--------|---------|--------------|
| [kana-review](plugins/kana-review/) | 1.0.0 | Adversarial second-harness review of code, PRs, plans, docs, math, and creative content |
| [kana-spec](plugins/kana-spec/) | 5.0.0 | Grounded specifications via an agentic pipeline — scouts, adaptive interview, adversarial critic |
| [suno-composer](plugins/suno-composer/) | 6.0.0 | Craft-reviewed Suno AI songwriting — dual-form prompts, mora-accurate Japanese lyrics, lyric-critic agent |
| [kana-code-rpc](plugins/kana-code-rpc/) | 1.0.0 | Claude Code activity as Discord Rich Presence — multi-session, statusline, live state |
| [anipy-cli](plugins/anipy-cli/) | 1.0.0 | Natural-language anime search/play/download via anipy-cli on Windows, with self-healing dependency repair |

### kana-review — `/kana-review`

Adversarial review with verification obligations: a read-only `kana-reviewer`
agent receives a task packet (claims tagged UNVERIFIED, author rationale
structurally excluded), verifies everything against the repository from a
disposable worktree, and reports evidence-backed findings with severity and
confidence — looping with stable finding numbers and explicit dispositions
until an explicit APPROVED status. Domain lenses cover code, plans, docs,
math, and creative content. Distilled from the manually-run two-harness
workflow that reviewed every PR in this repo's own modernization.

### kana-spec — `/kana-spec`

Write or update a spec for anything: a project, feature, design system, API, or
migration. One pipeline over Subject × Mode (Plan / Document / Overhaul):
citation-required scout agents map the codebase, an adaptive interview fills only
the gaps, and a spec-critic agent adversarially checks scope before drafting and
the draft before delivery. Outputs `SPEC.md` (+ `SPEC/` lookups, `CLAUDE.md`
pointer, `prompt.md` compound-engineering loop) with a Decision Log and an
Assumptions & Evidence ledger a future session can re-verify mechanically.

### suno-composer — `/suno`

Compose songs for current Suno models (v5/v5.5). Every song ships both
style-prompt forms (modular "try first" + narrative fallback), Exclude-field
negatives, paste-clean lyrics with a separate Readings & Casting craft block,
and is reviewed by default by a `lyric-critic` agent enforcing an 8-item
composition rubric —
mora-based Japanese prosody, duet voice casting, register devices, imagery
systems. 29 artist profiles, a 5-tier J-pop ecosystem map, album/variation/
continuation modes, adaptive preferences. Craft is checked; taste stays yours.

### kana-code-rpc

Daemon-backed Discord Rich Presence for Claude Code: project, activity state
(tool use / thinking / compacting / waiting), model, context usage, cost, git
branch, repo link button. PID-keyed multi-session tracking, deterministic state
via hooks, YAML config with hot-reload, plus a rich statusline. Windows-first.

### anipy-cli

Talk to [anipy-cli](https://github.com/sdaqo/anipy-cli) in natural language:
"play frieren ep 3 dubbed", "binge naruto 1-10", "continue watching". Handles
non-interactive execution via Git Bash, UTF-8 pipe encoding, and a guided
self-repair chain (uv → scoop → mpv/vlc → provider-drift upgrade) that asks
before fixing. Windows-focused.

## Repo layout

```
.claude-plugin/marketplace.json   the marketplace manifest
plugins/<name>/                   one directory per plugin
  .claude-plugin/plugin.json      plugin manifest (version/description mirrored
                                  byte-identically in marketplace.json)
  commands/ agents/ skills/ …     plugin components
  README.md / CHANGELOG.md        per-plugin docs
```

Maintainer conventions (validation gates, gitignore rules, review workflow) live
in [CLAUDE.md](CLAUDE.md).

## License

MIT — see per-plugin LICENSE files.
