# kana-review

Adversarial second-harness review for anything — code, PRs, plans, docs, math,
and creative content. A read-only reviewer that **trusts nothing and verifies
everything**, run **inline** in a fresh session so you watch every step.
Distilled from a manually-run two-harness workflow that caught real findings in
all 13 reviewed rounds of this marketplace's own modernization.

## Install

```
/plugin marketplace add Linaqruf/kana-code-plugins
/plugin install kana-review@kana-code-plugins
```

## Use

Open it in a **fresh session** that did not author what you're reviewing — that
separation is where the review's independence comes from. Then:

```
/kana-review:kana-review PR 42
/kana-review:kana-review feat/my-branch
/kana-review:kana-review docs/design.md as plan
/kana-review:kana-review this chapter, content lens
/kana-review:kana-review PR 42 paranoid
```

After fixes land, run it again — prior findings carry over with stable numbers
and explicit dispositions (Resolved / Partially / Not resolved / Superseded /
No longer applicable) until the reviewer returns an explicit APPROVED status.

## What makes it different

- **Inline, not a black box.** kana-review runs in your session with full tools.
  You see every command; the reviewer narrates what it checks. Independence
  comes from *you opening a separate review session*, not from hiding the work
  in a subagent.
- **Read-only = no authorship, not no execution.** The reviewer never edits,
  commits, installs, or mutates — but it *does* run tests, linters, validators,
  and `git diff` to ground its findings. A reviewer that can't run the test
  can't verify it. High-risk commands (installs, migrations, anything touching
  credentials) are reported, not run.
- **Untrusts its own training.** External facts — library versions, model
  names, API existence — are claims to web-verify, not memories to assert.
  A confident "that doesn't exist" is forbidden as a finding without a search;
  an unverifiable but load-bearing premise is reported as exactly that.
- **Evidence or it doesn't ship.** Every finding carries an evidence level, a
  severity AND a confidence, and the reviewer's own refutation attempt. Numbers
  are re-derived, never adopted. One found bug triggers a sweep for its class.
- **No severity self-censorship.** The evidence bar is the only filter —
  verified Lows are reported; speculation is not. Taste-level observations go to
  a separate, non-blocking Advisory section.
- **Domain lenses.** One invariant loop; the lens swaps what to look for, how to
  validate, and what severities mean — code, plan, docs, math, and content
  (where mechanical/structural violations are findings but judgment stays
  advisory: taste is not agent-verifiable).
- **Reports stay inline.** Copy-paste-friendly, and the read-only reviewer never
  writes them to disk — so old reviews don't bloat future sessions. Save one
  yourself if you want it; for a re-review, paste the prior report back.

## Scope honesty

kana-review never implements fixes — read-only is its identity, not a mode.
Read-only is enforced by contract, plus tool-level removal of the authoring
tools (`Write`/`Edit`/`NotebookEdit`), the subagent/orchestration/team tools
(`Agent`/`Workflow`/`SendMessage`/`TeamCreate`/`TeamDelete`), skill invocation
(`Skill`), and external-state tools (`CronCreate`/`CronDelete`/`RemoteTrigger`/
`ShareOnboardingGuide`/`PushNotification`) — the known orchestration and
external-state tools, verified against the current tools reference (session-local
read-only task-list tools are left available). Shell and web stay (grounding
needs them), so the discipline is real and you are watching. It is a local, interactive loop
(no CI integration). Independence depends on you running it from a session that
did not author the target. For the highest-stakes work, a true second harness —
a separate fresh session, ideally a different model — remains the gold standard;
this skill is that same review constitution, runnable inline. Suno song drafts
mid-composition belong to suno-composer's `lyric-critic`, not this plugin.

## Layout

```
skills/kana-review/SKILL.md                       the inline review flow
skills/kana-review/references/reviewer-contract.md  the constitution + obligations
skills/kana-review/references/lenses.md             domain lenses + severity anchors
```

## License

MIT
