# Changelog

## 1.1.0 (2026-09-28)

Fixes a hook pile-up that helped stall a machine. PreToolUse ran a
Git Bash → bash → python chain on every tool call, including every call
from parallel subagents. Claude Code does not enforce `timeout` on async
hooks, so when the Python launcher stalled, stuck chains kept piling up
until reboot.

- **No hook per tool call.** The daemon reads the current tool from the
  session transcript, reading only the new bytes once a second. The
  PreToolUse, UserPromptSubmit, Stop and SubagentStop hooks are gone; the
  transcript gives the same states. A bounded burst (3 subagents × 8 reads)
  now starts 5 python + 4 bash for the whole session, instead of
  65 python + 69 bash.
- **Every hook process has a hard deadline** (a watchdog), and the async
  hooks lose the `timeout` field that Claude Code never enforced.
- **The daemon cannot hang on Discord.** pypresence's handshake has no
  timeout, so the daemon bounds it (10 s), and a heartbeat exits a daemon
  whose loop ever stops, freeing it to be restarted. `daemon.lock` decides
  whether a daemon runs, so stale PID files after a reboot can neither block
  a new daemon nor get an unrelated python process killed.
- **No git processes**: branch and remote come from `.git` files, the
  transcript, or the statusline's `workspace.repo`. The statusline used to
  run `git` on every render.
- **Discord pacing**: at most one update per 15 s (Discord's limit), the
  latest payload winning. The daemon used to send up to one per second.
- **Discord closed is not fatal**: the daemon retries every 15–60 s while a
  session is open, instead of exiting after a minute.
- **Background subagents** show as "Delegating to <agent>" rather than
  "Waiting for input" until their completion notice arrives. The subagent
  type comes from the Agent call instead of the main agent's name.
- **Multi-session**: shows the most recently active session, and holds it
  for 20 s so two busy sessions don't flip the display. Model, context and
  cost are tracked per session.
- **Model names without a model list**: from the statusline, or derived from
  the transcript's model ID (`claude-opus-5-5` → Opus 5.5) when there is no
  statusline.
- `/clear` and `/resume` no longer unregister the session.
- A 1.0.0 daemon still running at upgrade is replaced (it never exited while
  sessions were alive).
- Log noise removed: the daemon no longer logs "Loaded config" every 30 s.

State stays compatible with 1.0.0: `daemon.pid` keeps its format (the
version is in a new `daemon.version`), `sessions.json` values may be an int
or a dict, and the statusline keeps writing the flat keys.

## 1.0.0 (2026-06-12)

Stability declaration — no functional change. The plugin has been
production-quality since 0.6.0 (41 tests, live-validated against Claude Code
2.1.170, backward-compatible state schema), and semver 0.x ("anything may
change") under-sold it. Versioning policy: root `CLAUDE.md` § Versioning.
Pre-1.0 history: see git log.
