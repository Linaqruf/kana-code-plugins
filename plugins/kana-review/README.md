# kana-review

Adversarial second-harness review for anything — code, PRs, plans, docs,
math, and creative content. A read-only reviewer agent that **trusts nothing
and verifies everything**, distilled from a manually-run two-harness review
workflow that caught real findings in all 13 reviewed rounds of this
marketplace's own modernization effort.

## Install

```
/plugin marketplace add Linaqruf/kana-code-plugins
/plugin install kana-review@kana-code-plugins
```

## Use

```
/kana-review PR 42
/kana-review feat/my-branch
/kana-review docs/design.md as plan
/kana-review this chapter, content lens
/kana-review PR 42 paranoid        ← refuter pass per Critical/High finding
```

After fixes land: `/kana-review re-review` — prior findings carry over with
stable numbers and explicit dispositions (Resolved / Partially / Not resolved /
Superseded / No longer applicable) until the reviewer returns an explicit
APPROVED status.

## What makes it different

- **The packet is the API.** The command assembles exactly what a human ferry
  would: phase, target, implementer claims (always tagged UNVERIFIED), prior
  findings, required validation, domain lens. The author's *rationale* is
  structurally excluded — the reviewer sees what is claimed, never why.
- **Verification obligations, not vibes.** Every finding carries evidence (on
  a declared hierarchy), a severity AND a confidence, and the reviewer's own
  refutation attempt. Numbers are re-derived, never adopted. Ship-claims are
  checked against the committed tree. One found instance triggers a sweep for
  the class.
- **No severity self-censorship.** The evidence bar is the only filter —
  verified Low findings are reported, speculation is not. Taste-level
  observations go to a separate non-blocking Advisory section.
- **Read-only by identity, worktree by blast radius.** The reviewer never
  fixes anything, and runs in a disposable git worktree pinned in its own
  manifest — so even test runs and validations can't touch your checkout; it
  reports the worktree's end state when it finishes.
- **Domain lenses.** The loop is invariant; the lens swaps what to look for,
  how to validate, and what severities mean — code, plan, docs, math, and
  content (where mechanical/structural violations are findings but judgment
  stays advisory: taste is not agent-verifiable).
- **Reports stay inline.** Copy-paste-friendly, and old reviews don't bloat
  future sessions. Persisting to `.claude/reviews/` is offered, never
  automatic.

## Scope honesty

kana-review never implements fixes — read-only is its identity, not a mode.
Read-only is enforced by contract, not sandbox: the disposable worktree bounds
repo damage, and the reviewer reports exactly what it ran — but a misbehaving
run could still touch system state outside the repo. It is a local,
interactive loop (no CI integration). For the highest-stakes
work, a true second harness — a separate fresh session, ideally a different
model — remains the gold standard; this plugin automates the ferry for the
medium-stakes middle, and its report format is interchangeable with the
manual loop's, so escalating costs nothing. Suno song drafts mid-composition
belong to suno-composer's `lyric-critic`, not this plugin.

## Layout

```
commands/kana-review.md     packet assembly, lens detection, review loop
agents/kana-reviewer.md     the reviewer contract
references/lenses.md        domain lenses + severity anchors
```

## License

MIT
