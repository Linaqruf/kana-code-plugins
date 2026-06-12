# Changelog

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
