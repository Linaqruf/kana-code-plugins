# Changelog

## 1.1.0 (2026-06-13)

Grounding fix + skill-only inline rethink, triggered by the first real dogfood
(an external-fact-heavy design doc), where the reviewer confidently asserted
three real post-cutoff models "don't exist" — violating its own *untrust
yourself* principle. The whole 1.0 build had only ever reviewed repo-internal
targets, so the external-fact axis was never exercised.

- **Untrusts its own training:** external facts (versions, model names, API
  existence) are now claims to web-verify, not memories to assert. A confident
  negation is forbidden as a finding without a search; an unverifiable but
  load-bearing premise is reported as exactly that (severity tracks
  load-bearing-ness, never a guessed truth value). Adds web verification with
  an egress-scope rule (no secrets/private names in queries).
- **Read-only = no authorship, not no execution:** the reviewer runs tests,
  linters, validators, and `git diff` to ground findings; it never authors,
  mutates, installs, or commits; high-risk commands are reported, not run.
- **Skill-only inline architecture:** replaces the command+agent+packet-ferry
  with a single inline review skill. The reviewer is the visible session you
  invoke from a fresh harness — no black-box subagent, no relay, no contract
  drift. `disable-model-invocation` (deliberate slash-only) + `disallowed-tools`
  remove the authoring and subagent-spawning tools at the tool layer. The
  autonomous/batch reviewer is deferred until the unattended loop exists
  (re-addable as a `context: fork` skill).
- Invocation is `/kana-review:kana-review` (namespaced, unchanged from the
  command). Six-round cross-model design review (Opus author + Codex reviewer).

## 1.0.0 (2026-06-12)

Initial release. Distills a manually-run two-harness adversarial review
workflow (13 reviewed rounds across this marketplace's modernization effort,
PRs #32-#38) into a command + agent: packet assembly with rationale exclusion,
read-only reviewer in a disposable worktree, evidence-backed findings with
severity + confidence, domain lenses (code/plan/docs/math/content), re-review
loop with stable finding numbers and five dispositions, opt-in report
persistence, and a paranoid refuter mode. Ships at 1.0.0 because the contract
is field-proven and the plumbing passed a known-answer smoke test before
merge (see the PR).
