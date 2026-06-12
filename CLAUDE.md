# kana-code-plugins — maintainer instructions

Claude Code plugin marketplace (4 plugins under `plugins/`, manifest at
`.claude-plugin/marketplace.json`). These rules are incident-proven — each one
exists because its violation shipped or nearly shipped a bug.

## Hard rules

1. **plugin.json and marketplace.json stay byte-identical** on `version` AND
   `description` for every plugin. Compare programmatically (`-ceq`), don't
   eyeball. They have drifted before.
2. **Ship-verification runs against the COMMITTED tree, never the working
   tree**: `git cat-file -e HEAD:<path>` for must-exist files, and
   `git archive HEAD` → temp dir → `claude plugin validate` (+ marketplace
   `--strict`) before any push. A working-tree validate once passed while the
   entry-point file was silently gitignored out of the commit (PR #35), and a
   clean-export validate caught broken agent frontmatter (PR #36).
3. **The root `.gitignore` spec rules (`/SPEC.md`, `/SPEC/`, `/spec/`,
   `/specs/`, `/prompt.md`, `/dev/`) are root-anchored ON PURPOSE — never widen
   them back to `**/` patterns.** Unanchored patterns match every directory,
   case-insensitively on Windows, and silently swallowed plugin source once.
   Corollary: root `SPEC.md`/`prompt.md` are RESERVED, ignored output slots for
   kana-spec runs on this repo — never commit tracked files at those paths.
4. **`docs/` is local-only** (listed in `.git/info/exclude`) — design docs and
   review logs live there and are never committed.
5. **Validation gates before any plugin PR**: `claude plugin validate
   <plugin-dir>` and `claude plugin validate .claude-plugin/marketplace.json
   --strict` must pass clean — from the clean export per rule 2. Agent/skill
   frontmatter is YAML: an unquoted `:` inside a description silently drops ALL
   frontmatter at runtime; use folded block scalars (`>-`) for long
   descriptions.
6. **Stage by exact path** (`git add plugins/<name> .claude-plugin/...`) —
   never `git add -A` / `commit -a`. Unrelated working-tree state must not ride
   along in a plugin PR.

## Workflow

Changes go through an adversarial review loop: design doc (local `docs/`) →
independent review → implement on a feature branch → single PR → implementation
review → fix → re-review → merge. Make deliverables review-ready: cite
`file:line` for every claim, mark premises VERIFIED (with evidence) or
UNVERIFIED (with what they gate), and keep review logs in the design doc.
Numbers and findings from agents, old reports, or reviewers are claims —
re-measure before building on them.

Measurement notes (Windows): `(Get-Content f).Count` for `wc -l` parity
(`Measure-Object -Line` skips blank lines); a grep gate returning zero matches
when you expected whitelisted hits is a FAILED gate (lookahead regexes can
silently no-op) — re-run with a plain pattern and read the hits.

## Per-plugin notes

- **kana-spec** — entry is `commands/kana-spec.md` (surfaces as
  `/kana-spec:kana-spec`); deliberately NOT named `spec.md` (gitignore-swallow
  history, rule 3) — don't rename it back. No plugin-level CLAUDE.md by design.
- **suno-composer** — Lyrics blocks are paste-clean by contract (parentheticals
  are sung); craft metadata goes in Readings & Casting. The exemplar
  (`references/examples/gothic-doujin-song.md`) is a golden test: it must pass
  the SKILL.md rubric — if a rubric edit fails it, the rubric is wrong. Suno
  behavior claims carry provenance or hedges; keep it that way.
- **kana-code-rpc** — hooks/daemon run from the plugin cache, but a local
  statusline may run from a working copy via `settings.json`; keep the
  `%APPDATA%\kana-code-rpc` state schema backward-compatible. Valid hook events
  only (`SubagentStart` does not exist).
- **anipy-cli** — Windows + Git Bash assumptions are load-bearing; the
  self-repair chain asks before mutating the system. anipy-cli can exit 0 on
  fatal errors — parse output, not exit codes.
