---
description: Write or update a grounded specification for anything — a project, feature, design system, API, or migration. Scout the codebase with agents, run an adaptive interview, adversarially verify the draft, and deliver SPEC.md + CLAUDE.md + prompt.md for compound engineering. Triggers on "create spec", "plan project", "spec out", "plan feature", "design system spec", "document my project", "write specification", "plan my app", "what should I build next", "audit my design", "update the spec".
argument-hint: "[what to spec — e.g. 'this project', 'a comments feature', 'overhaul the design system']"
allowed-tools:
  - Task
  - AskUserQuestion
  - Write
  - Read
  - Glob
  - Grep
  - TodoWrite
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
---

Subject of this spec engagement: $ARGUMENTS (free-form — infer; if empty, the subject is the whole project)

# The Job

The product is not the spec file — it is **better future agent sessions**. A
spec front-loads decisions into durable contracts: the spec is what a future
session READS, `SPEC/` files are what it LOOKS UP, `CLAUDE.md` points at both,
`prompt.md` restarts the loop. Every choice below serves that: a fresh session
with zero context must be able to act correctly from the artifacts alone.

# The Model: Subject × Mode

Every engagement is one pipeline over two coordinates:

- **Subject** — what is being specified: the whole project, a feature, the
  design system, an API, a migration. Infer from the user's words + scout
  findings. Scale follows: project-scale → `SPEC.md` at root; component-scale
  → `SPEC/<slug>.md`.
- **Mode** — **Plan** (subject doesn't exist yet), **Document** (it exists;
  capture reality), **Overhaul** (it exists; audit it, then re-derive from
  first principles with a phased migration checklist).

There are no other routes. Legacy-style arguments ("feature auth",
"design:overhaul") read naturally as subject/mode hints.

# Pipeline

Steps are tagged: **[execute]** = do directly, no deliberation;
**[reason deeply]** = slow down, this is where judgment earns its keep.

## 1. SCOUT [execute]

ALWAYS spawn the `spec-scout` agent before framing — skipping it is only
allowed for true greenfield (empty directory). Pass: the subject + repo path.
If the repo is large (>~200 source files) or the subject spans clearly
separate concerns, spawn 2-3 scouts **in parallel in the same message**, each
with a narrower beat (e.g. structure+stack / data+API / conventions+tests).

The scout returns a cited map: every claim carries `file:line` evidence or is
marked unknown. Treat it as the interview's pre-fill source, never as
something to re-derive yourself in the main context.

## 2. FRAME [execute]

One AskUserQuestion confirming subject, mode, and scale — options pre-filled
from scout findings (e.g. if the scout found an existing SPEC.md, offer
Update vs Fresh; if the user asked "what next?" with no subject, present the
gap between scout map and existing spec as candidate subjects).

## 3. INTERVIEW [reason deeply at C; execute the mechanics]

Adaptive — phase GOALS, not scripts. Each phase defines what must be KNOWN by
its end. Skip anything the scout already answered (confirm pre-fills, don't
re-ask). Batch 2-3 related questions per AskUserQuestion call.

- **A. Intent** (never skip): the problem, who it's for, what success looks
  like — measurably. In Overhaul mode, run A *after* presenting the audit,
  framed first-principles: "forget the current implementation."
- **B. Boundary**: the MVP set (use **multiSelect** for feature selection),
  explicit out-of-scope, the primary flow. Apply ruthless scoping: ask "if
  you had to cut half of these, which half survives?" when the MVP list
  exceeds ~5 items.
- **C. Shape** [reason deeply]: architecture/approach — present 2-3 options
  via AskUserQuestion **with previews** (ASCII diagram per option). Reason
  through the recommendation from THEIR stated constraints before presenting;
  recommended option first, "(Recommended)", honest tradeoffs in every
  description. Tech choices adapt to scout findings and earlier answers;
  skip categories that don't apply.
- **D. Risks & specifics** (conditional): auth/security when there are users
  or sensitive data; edge cases; compliance; migration sequencing (Overhaul).

Interview conduct rules:
- **Disagree once**: when the user's choice conflicts with their stated goals
  or the scout's evidence, say so once, plainly, with the reason — then defer.
- **Minor choices don't ask**: naming, formatting, defaults, equivalent
  approaches — pick reasonably and note it in the Decision Log. Ask only for
  scope changes and genuinely open tradeoffs.
- Never invent requirements — only document what the user confirms.

## 4. SCOPE CHECK [execute the spawn; the agent reasons]

ALWAYS spawn `spec-critic` with lens A before drafting — it is cheap here and
catches wrong premises at their cheapest point. Pass exactly: the framed
scope + interview-answer summary + scout map, **tagged as UNVERIFIED CLAIMS**,
plus subject and repo path. Never pass your rationale. Apply its findings;
disputes you can't resolve become interview follow-ups or Open Questions.

## 5. ENRICH [execute]

For each finalized tech choice, fetch docs via Context7 (resolve-library-id →
query-docs), in parallel, never blocking the user. Mark everything that lands
in the spec with provenance: fetched-doc vs model-memory. On any Context7
failure: continue, note "[tech] docs not fetched" in References, tell the
user once.

## 6. DRAFT [reason deeply]

Write per `${CLAUDE_PLUGIN_ROOT}/references/output-contracts.md` — structure,
conditional sections, Decision Log, Assumptions & Evidence ledger. Study
`${CLAUDE_PLUGIN_ROOT}/references/examples/web-app-spec.md` (project-scale) or
`examples/feature-spec.md` (component-scale) for the quality bar.

## 7. DRAFT CHECK [execute the spawn]

Spawn `spec-critic` with lens B: pass the draft + scout map + the ledger
(tagged UNVERIFIED CLAIMS) + subject + repo path. Revise per findings, then
have the critic re-check the fixes (cheap — pass only the revised sections +
its own findings). Default: one revise + one re-check. Paranoid mode: loop
until no findings, max 3 rounds. Findings that survive revision become Open
Questions entries — honest, never silently dropped.

## 8. DELIVER [execute]

Write the spec file(s). Project-scale: also write/update CLAUDE.md (pointer
format in output-contracts.md). Offer prompt.md (compound loop) whenever the
spec has `- [ ]` phases. Offer the gitignore block if `.gitignore` exists.
Present a summary: files written, key decisions, open questions.

# Grounding Discipline

- Every statement about the existing codebase cites a path (scout's citations
  flow into the spec). Unknowns are written as unknown.
- The **Assumptions & Evidence ledger** in the spec marks each load-bearing
  premise VERIFIED (with evidence) or UNVERIFIED (with what it gates).
- **Paranoid escalation** — when the subject is large/critical or the user
  asks ("be paranoid"): dual scouts with different lenses, reconciled
  (disagreements surface as UNVERIFIED), plus critique-to-fixed-point.
- **Anti-theater guard**: default is exactly one Scope Check and one Draft
  Check + re-check. Verification scales with consequence. User INTENT is not
  agent-verifiable — the critic checks consistency and grounding only.

# Quality Rubric (the critic enforces these literally)

1. Every acceptance criterion contains a quantity, threshold, or exact
   behavior — "fast" and "good UX" fail.
2. Every tech choice names ≥1 rejected alternative and why.
3. Every codebase claim cites a path; every external claim carries provenance.
4. The MVP list survives the cut-half question without hiding load-bearing
   items in "future scope".
5. Sections that don't apply are omitted, not filled with boilerplate.
6. Reference-heavy material (10+ endpoints, full schemas) goes to SPEC/
   lookups, with the user's consent, never inline by default.
7. **Cold-start test**: a fresh session reading only the artifacts can state
   its first concrete action and answer its own next three questions.
