---
description: Adversarial second-harness review of code, PRs, plans, docs, math, or creative content — packet assembly, untrusted-claims verification, findings loop
argument-hint: "[PR #, branch, file(s), or what to review — e.g. 'PR 42', 'docs/design.md as plan', 'this chapter, content lens', 'paranoid']"
allowed-tools: [Task, Read, Glob, Grep, Bash, AskUserQuestion, Write]
---

# kana-review

Run an adversarial, read-only review through the `kana-reviewer` agent. Your
job here is **packet assembly and ferrying** — you never review the target
yourself, and you never pass your own opinion of it to the reviewer.

## Step 1: Resolve the target

| Input shape | Resolution |
|-------------|-----------|
| PR number ("PR 42", "#42") | `gh pr view <N>` for metadata + body; target ref = `pull/<N>/head` |
| branch name | diff vs the default branch; target ref = the branch |
| explicit diff/commit | as given |
| file path(s) | the files as they stand |
| pasted artifact / "this chapter" | the conversation artifact, quoted in full into the packet |

If the target is genuinely ambiguous (and only then), ask via AskUserQuestion.

## Step 2: Assemble the packet

Build exactly these fields — nothing more:

- **Phase:** PLAN REVIEW (target is a plan/spec/design doc) /
  IMPLEMENTATION REVIEW (diff/PR/branch/files) /
  RE-REVIEW (prior findings exist — see Step 4). Overridable by the user.
- **Target:** the resolved target + how to reach it (for PR/branch targets:
  the ref to fetch — the AGENT checks it out inside its own worktree; never
  prepare the user's tree for it).
- **Implementer claims:** harvested from the PR body, commit messages, or the
  user's summary — always tagged **UNVERIFIED CLAIMS**. Claims are WHAT is
  asserted, never WHY: do not summarize rationale, design reasoning, or
  justifications into this field, even if you know them from this
  conversation. If there are none, write "none".
- **Prior findings:** the previous report (Step 4) or "none".
- **Required validation:** user-specified checks, or "use judgment".
- **Domain lens:** auto-detect per the table in
  `${CLAUDE_PLUGIN_ROOT}/references/lenses.md` (code / plan / docs / math /
  content), overridable ("…as plan", "content lens"). Pass the lens name AND
  the lenses file path so the agent reads the tables itself.

## Step 3: Spawn the reviewer

Spawn the `kana-reviewer` agent (Task tool) with the packet.

- Repo-state targets (PR / branch / diff / tracked files): spawn with
  **`isolation: "worktree"`** — the reviewer may run tests and validators, and
  the worktree bounds any mutation away from the user's tree.
- Artifact-only targets (pasted content, standalone doc outside a repo): no
  worktree needed.
- **Paranoid mode** (user said "paranoid" or asked for merge-blocking
  certainty): after the review returns, spawn one refuter agent per
  Critical/High finding — fresh `kana-reviewer` with a packet containing ONLY
  that finding + the target, Phase "RE-REVIEW", and Required validation
  "attempt to refute this finding; default to refuted if evidence is
  ambiguous". Findings that survive carry "crosschecked ✓" in the presented
  report; refuted ones are struck with the refutation evidence shown.

## Step 4: Deliver and loop

1. Present the reviewer's report **inline and verbatim** — the report is the
   deliverable; add nothing, soften nothing, summarize nothing.
2. If the report mentions a lingering (dirty) worktree, surface that in one
   closing line so the user can remove it.
3. **Offer persistence — never auto-save:** one short offer to write the
   report to `.claude/reviews/<target-slug>/rN.md`. If `.claude/` is tracked
   in this repo (`git check-ignore .claude` fails), warn before writing.
   Declining is the expected default; the report lives in chat either way.
4. **Re-review:** when the user comes back after fixes (or says "re-review"),
   build a RE-REVIEW packet whose Prior findings come from the persisted
   `r(N-1)` if it exists, else from the prior report in this conversation,
   else ask the user to paste it. Finding numbers stay stable across rounds;
   the reviewer applies the five dispositions.
5. The loop ends when the reviewer returns an APPROVED status. Approval
   semantics belong to the reviewer — never upgrade a NOT APPROVED into a
   softer summary.

## Boundaries

- This command never edits the target, never fixes findings, and never runs
  the review itself in-context. Fixes belong to the author (the user or their
  authoring session); kana-review only verifies.
- Suno song drafts mid-composition belong to suno-composer's `lyric-critic`,
  not this command.
- For the highest-stakes work, recommend the user's manual two-harness loop —
  this command automates the ferry for the medium-stakes middle, and its
  report format is interchangeable with the manual loop's.
