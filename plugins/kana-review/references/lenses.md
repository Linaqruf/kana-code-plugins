# Domain Lenses

The review loop is invariant — untrust, onboard, verify, crosscheck, report,
loop. The lens swaps three things: what to look for, how to validate, and what
each severity means. The command auto-detects the lens from the target type;
the user can override.

## Lens detection

| Target looks like | Lens |
|-------------------|------|
| PR, branch, diff, commit, source files | code |
| design doc, plan, spec, RFC, proposal | plan |
| README, guide, reference prose, API docs | docs |
| proof, derivation, calculation, data analysis | math |
| story, chapter, lyrics, script, worldbuilding, general prose | content |

Mixed targets (e.g. a PR that changes code AND docs): primary lens from the
dominant change, with the secondary lens's look-for list applied to the
relevant files.

## code

**Look for:** logic/correctness bugs; missing edge cases; security,
reliability, concurrency, performance, operational risks; backward
compatibility; rollout/migration gaps; incomplete fixes; tests that don't
actually cover the changed behavior; plan↔implementation↔docs↔tests
mismatches; hidden dependencies and environment assumptions.

**Validate by:** running existing tests/linters/type checks when safe; tracing
callers and usages of changed symbols; committed-tree checks for ship-claims;
reading the tests to confirm they exercise the changed paths (not just touch
the changed files).

**Severity anchors:** Critical = likely data loss, security vulnerability,
production outage, or irreversible failure. High = likely correctness,
reliability, compatibility, or rollout failure. Medium = real issue with
bounded impact, or important missing coverage. Low = minor but actionable.

## plan

**Look for:** false or unverified premises; internal contradictions;
accounting errors (re-derive every number, count, and sum); mismatches with
repository reality (cited paths/lines/commands that don't exist or don't say
that); scope gaps; missing rollout, validation, or test strategy; feasibility
holes; decisions without alternatives.

**Validate by:** re-measuring every claim against source; checking each cited
`file:line` actually supports the claim it anchors; running referenced
commands' read-only forms; verifying premises marked VERIFIED actually carry
evidence and premises marked UNVERIFIED name what they gate.

**Severity anchors:** Critical = executing the plan produces a broken,
destructive, or unrecoverable state. High = a load-bearing premise is wrong;
implementation would diverge materially. Medium = real gap with bounded
blast radius. Low = accounting/clarity issue that will propagate if unfixed.

## docs

**Look for:** claim-vs-source inaccuracy; staleness (versions, names, dates,
paths); dangling references and broken links; internal contradiction between
sections; example code or commands that don't work; instructions that omit a
load-bearing step.

**Validate by:** cross-referencing every checkable claim against the code or
artifact it documents; existence checks on every path/link; running example
commands when safe; version-string sweeps.

**Severity anchors:** Critical = the doc instructs a destructive or
irreversible action incorrectly. High = following the doc fails or misleads on
a primary workflow. Medium = real inaccuracy with bounded effect. Low = minor
staleness or clarity debt.

## math

**Look for:** invalid inference steps; unstated or unjustified assumptions;
definition, domain, and unit errors; boundary and degenerate cases;
counterexamples; numeric errors; conclusions stronger than the derivation
supports.

**Validate by:** re-deriving independently (never follow the author's steps in
order — re-derive, then diff); safe numeric spot-checks; testing boundary and
degenerate cases explicitly; dimensional/unit analysis.

**Severity anchors:** Critical = the central conclusion is false. High = a
step is invalid and the conclusion is unsupported as written. Medium = a gap
that is probably bridgeable but currently unjustified. Low = notation,
precision, or presentation debt.

## content

**Look for:** internal consistency (timeline, character knowledge/motivation,
established world rules); continuity errors; structure vs the work's stated
intent; violations of a supplied rubric or the work's own declared
conventions; POV breaks; setup without payoff and payoff without setup.

**Validate by:** quote-the-text evidence for every claim; checking against the
work's OWN rules and any rubric supplied in the packet — never against the
reviewer's taste.

**Checkability tiers govern this lens:** [M]echanical (countable: syllables,
declared form constraints) and [S]tructural (presence/absence: a thesis, a
setup, a declared POV) violations are findings. **[J]udgment — whether it
lands, whether it's good — is ADVISORY at low confidence, never blocking.**

**Severity anchors:** Critical = a continuity/consistency break that
invalidates the work's premise. High = a contradiction a careful reader will
catch. Medium = bounded inconsistency or structural gap. Low = minor
continuity or convention slip.
