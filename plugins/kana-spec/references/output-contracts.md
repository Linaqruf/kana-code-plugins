# Output Contracts

Structural contracts for every artifact kana-spec produces. Structure lives
here; quality illustration lives in `examples/web-app-spec.md` (project-scale)
and `examples/feature-spec.md` (component-scale).

**Core principle: the spec is READ, SPEC/ is LOOKED UP.** The spec file is
always complete and self-sufficient — never require a SPEC/ file to
understand the subject. SPEC/ supplements hold reference material you look up
mid-implementation (schemas, endpoint details, SDK patterns), created only
with the user's consent.

---

## Project-scale spec → `SPEC.md` at repo root

Sections in order. Conditional sections are marked — OMIT them when they
don't apply (no boilerplate); adapt freely to the subject.

```markdown
# [Project Name]

> [One-line description]

## Overview
### Problem Statement        — 1-2 sentences
### Solution                 — 1-2 sentences
### Target Users             — primary / secondary / technical level
### Success Criteria         — checkboxed, each with a quantity or threshold

## Product Requirements
### Core Features (MVP)      — per feature: description, user story,
                               testable acceptance criteria (checkboxed)
### Future Scope (Post-MVP)  — numbered list
### Out of Scope             — explicit exclusions
### User Flows               — numbered user/system steps for primary flow(s)

## Technical Architecture
### Tech Stack               — table: Layer | Technology | Rationale |
                               Alternatives Considered (NEVER omit the
                               alternatives column — rubric item 2)

## System Maps               — ASCII diagrams:
                               architecture; data-model relations;
                               state diagram (entities with lifecycle);
                               user flow; wireframe (frontend subjects only)

## Data Models               (if the subject has persistent data)
                             — TypeScript interfaces + validation schemas
                               (Zod or ecosystem equivalent)

## API Endpoints             (if the subject exposes an API)
                             — table: Method | Endpoint | Description |
                               Auth | Rate Limit

## Security                  (if users or sensitive data)
                             — auth flow diagram; input validation rules;
                               sensitive-data protection table;
                               authorization roles table

## Error Handling Strategy   — error response format (JSON shape);
                               error-code table (code | HTTP | when);
                               boundaries (API / UI / jobs / network retry)

## Design System             (frontend subjects only)
                             — brand colors table; typography table; spacing
                               scale; breakpoints; component inventory with
                               states; accessibility requirements (WCAG
                               level, contrast ratios, focus, keyboard,
                               reduced motion)

## File Structure            — annotated directory tree

## Monitoring & Observability (production apps/APIs only)
                             — tool table (error tracking, logging, health
                               check, performance, uptime); log-level table

## Environment Variables     (if any) — Variable | Description | Required |
                               Default

## Development Phases        — phased checkboxes with explicit
                               "**Depends on**: Phase N (why)" lines.
                               This section powers prompt.md — always
                               checkboxed.

## Decision Log              — see contract below

## Assumptions & Evidence    — see contract below

## Open Questions            — table: # | Question | Options | Impact | Status

## References                (if SPEC/ supplements or fetched docs exist)
                             — "→ When implementing X: `SPEC/x.md`" lines
                               + external doc links with provenance
```

### Subject-type variations

**CLI tools** — replace frontend/design sections with: Commands table
(command | description | arguments); Exit Codes table; Output Formats
(text/json/quiet); Algorithm specs for non-obvious logic (input, output,
ordered rules, worked examples table); Distribution (package manager,
binaries). Omit: Design System, wireframes, breakpoints, Monitoring (unless
the CLI is a daemon).

**APIs** — expand API Endpoints into full per-resource documentation: HTTP
request/response examples with query params and status codes; API key
management (generation format, hashed storage, rotation with grace period,
prefix-only display); rate-limit table per endpoint pattern. Omit: Design
System, wireframes, breakpoints.

**Libraries** — replace deployment/server sections with: Public API (per
function: description, parameters, returns, example); exported Types; bundle
size strategy (target KB, dependency policy, tree-shaking, subpath exports);
Publishing (registry, semver policy). Omit: Design System, deployment, auth,
Monitoring, Security (unless the library handles crypto/auth).

---

## Component-scale spec → `SPEC/<slug>.md`

For features, design systems, migrations — any subject smaller than the
project. Write `SPEC/<slug>.md` (slug from the subject, kebab-case). Discovery
of older specs is by globbing, never by naming convention.

```markdown
# [Subject Name]

> [One-line description] — component spec; project context in `SPEC.md`
  (link only if it exists)

## Overview                  — problem, why now, success criteria (measurable)

## Requirements
### Must Have                — checkboxed, testable
### Nice to Have
### Out of Scope

## Technical Design
### Affected Components      — existing files/modules touched, with paths
### New Components           — what gets created, where
### API Changes              (if any)
### Data Changes             (if any — schema migrations spelled out)

## User Flow                 — numbered steps

## Implementation Plan       — phased checkboxes with dependencies
                               (powers prompt.md)

## Edge Cases                — case → handling, one line each

## Testing Strategy          — what gets unit/integration/manual coverage

## Decision Log
## Assumptions & Evidence
## Open Questions
```

Overhaul mode additionally produces a **Migration Checklist** as the
Implementation Plan: Foundation → Components → Pages → Cleanup phases, plus a
migration summary table (old → new → action) derived from the audit.

---

## `CLAUDE.md` (project-scale engagements only)

Agent-optimized pointer file — short, never a duplication of SPEC.md:

```markdown
# [Project Name]

[One-line description]

## Spec Reference

Primary spec: `SPEC.md`

→ When implementing API endpoints: `SPEC/api-reference.md`   (only lines for
→ When using [SDK]: `SPEC/sdk-patterns.md`                    files that exist)

## Key Constraints

- [Critical constraint surfaced from the spec]
- [Out-of-scope reminder]

## Commands

- `[pm] run dev` / `test` / `build`   (the project's real commands)

## Current Status

→ Check `SPEC.md` § Development Phases
→ Start new dev sessions with prompt.md   (only if prompt.md generated)
```

If a CLAUDE.md already exists, UPDATE the Spec Reference and Current Status
sections; never clobber user content elsewhere in the file.

---

## SPEC/ supplements

Create only when BOTH hold: the user agreed (ask mid-interview when a topic
turns reference-heavy — 10+ endpoints, complex SDK usage, detailed schemas),
AND the content is lookup material, not narrative. Typical files:
`api-reference.md`, `data-models.md`, `sdk-patterns.md`.

Supplement format:

```markdown
# [Title] Reference

> Lookup reference for [purpose]. See SPEC.md for full specification.

---
## [Section]
[Reference content — full schemas, request/response examples, SDK snippets]
---
*Lookup reference. For project overview, see SPEC.md.*
```

Wire supplements in twice: an inline pointer in the relevant SPEC.md section
("→ When implementing endpoints, see `SPEC/api-reference.md`") and a line in
SPEC.md § References. Never create supplements for requirements, architecture,
or decisions — those are READ material and belong in the spec.

---

## Decision Log (contract)

Every major decision the engagement made, so future sessions don't relitigate:

```markdown
## Decision Log

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Postgres over SQLite | concurrent writers expected (stated: 3 services) | SQLite (single-writer), Mongo (no relational need) |
```

Minor choices the interview made without asking (naming, defaults) get
one-line entries — that is the "note it" half of minor-choices-don't-ask.

## Assumptions & Evidence ledger (contract)

Each load-bearing premise, marked:

```markdown
## Assumptions & Evidence

- VERIFIED — "API is Express 4": package.json:12, src/server.ts:1
- VERIFIED (fetched docs) — "Next 15 App Router supports X": Context7/nextjs
- UNVERIFIED — "peak load ~100 rps" (user estimate) — gates the
  architecture choice in § Tech Stack; revisit before Phase 3
- WEB-SOURCED — [claim] ([source])
```

Rules: every UNVERIFIED entry names what it gates. Codebase claims inherit
the scout's citations. Model-memory claims about external tech are marked as
such or upgraded via Enrich. A future session should be able to re-verify
this spec mechanically.

---

## `prompt.md` (compound engineering bootstrapper)

Offer whenever the generated spec contains `- [ ]` phases. Output at project
root. If prompt.md exists, ask: Replace / Keep existing.

~~~markdown
# [Project Name] — Dev Session

Spec: `[Spec File]` | Status: `[Spec File]` § [Phase Section Name]

## Loop

1. **Read** — Open `[Spec File]` § [Phase Section Name]. Find the next
   unchecked `- [ ]` phase. Read the spec sections relevant to that phase.[Supplement Line][Project Context Line]
2. **Ask** — If anything is ambiguous for this phase, ask via
   AskUserQuestion. Do not ask what the spec already answers.
3. **Plan** — Enter Plan Mode. Implementation plan with file paths, code
   patterns, and test coverage.
4. **Work** — Execute the plan. Run tests and lint.
5. **Compound** — Update `[Spec File]`: check off `- [x]` completed items,
   add discoveries to Open Questions (status: Resolved), update the
   Assumptions & Evidence ledger if a premise was verified or broken.[CLAUDE.md Line]
6. **Report** — What was done, what's next, open questions needing input.
~~~

Parameterization:

| Parameter | Fill |
|-----------|------|
| `[Project Name]` | First `# ` heading of the spec; fallback: directory name |
| `[Spec File]` | `SPEC.md` or `SPEC/<slug>.md` — the file actually written |
| `[Phase Section Name]` | The actual checkboxed section heading ("Development Phases" / "Implementation Plan" / "Migration Checklist"); fallback "Development Phases" |
| `[Supplement Line]` | If SPEC/ supplements exist: " Reference supplements: → `SPEC/x.md` for [purpose]." — list only files that exist; else omit |
| `[Project Context Line]` | Component-scale only, and only if SPEC.md exists: " Also read `SPEC.md` for project-wide context." |
| `[CLAUDE.md Line]` | If CLAUDE.md exists: " If new constraints found, add to `CLAUDE.md` § Key Constraints."; else omit |

Output checks: numbered steps; real paths, not placeholders; no duplication
of spec content; the compound step present; under 20 lines excluding header.
When prompt.md is written, add `→ Start new dev sessions with prompt.md` to
CLAUDE.md § Current Status.

---

## gitignore block

If `.gitignore` exists, offer (Recommended = yes) to append — only entries
for files actually generated and not already present:

```
# Project spec (generated)
/SPEC.md
/SPEC/
/prompt.md
```

The leading slashes are LOAD-BEARING: unanchored patterns match in every
directory, case-insensitively on Windows/macOS, and will silently swallow any
source file named `spec.md` or directory named `spec/` anywhere in the user's
tree. Anchor to where the artifacts are actually written (repo root for
project-scale; the SPEC/ rule also covers component-scale specs). Never offer
unanchored variants. If no `.gitignore` exists, skip silently — don't create
one for this.

---

## Writing guidelines (apply everywhere)

- **Specific**: "Store user profiles with id, email, name, avatar, createdAt"
  — not "handle user data".
- **Testable**: "API responses under 200ms at p95 for list endpoints" — not
  "fast". "If metadata fetch fails after 10s timeout, save bookmark with URL
  as title" — not "graceful fallback".
- **Alternatives recorded**: "Prisma (migration tooling). Considered Drizzle
  (lighter, SQL-first) — rejected for weaker migration story."
- **MVP ruthless**: viability-critical only; everything else is named and
  moved to Future Scope, not silently kept.
