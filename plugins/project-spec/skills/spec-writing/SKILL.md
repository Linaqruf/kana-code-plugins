---
name: spec-writing
description: This skill should be used when the user wants to create project specifications, feature specifications, design system documentation, or update existing specs. Triggers on "create spec", "plan project", "design system", "plan feature", "write specification", "generate SPEC.md", "document my project", "scaffold a spec", "plan my app", "spec out a feature", "create a project plan", "create a CLAUDE.md", "document architecture", "set up my project", "bootstrap a new app", "help me plan", "redesign my UI", "audit my design", "update my spec", or "revise the spec". Covers interview-based specification workflow with codebase analysis, tech stack recommendations, gap analysis, design audit, and optional SPEC/ supplements.
version: 4.0.0
---

# Spec Writing v4.0.0

Authoritative methodology for generating specifications. The `/spec-writing` command references this skill.

## Prompt Principles

### Adaptive Thinking

Mark where deep reasoning adds value vs where to execute directly:

- **Execute directly**: File detection, template application, output formatting, version checks
- **Reason deeply**: Architecture decisions, tech stack tradeoffs, scope boundaries, gap analysis findings, codebase pattern recognition

When presenting choices to the user, include concrete rationale with tradeoffs — not just labels.

### Literal Interpretation

- Use imperative mood: "Ask", "Create", "Skip" — never "consider", "might want to", "you could"
- Make conditions explicit: "If package.json lists react, vue, svelte, or angular as a dependency" — never "if applicable"
- Every AskUserQuestion call presenting a **choice** must use the options parameter with 2-4 choices. Open-ended information-gathering questions (problem statement, feature lists, user flows) may use free-text format
- Follow the interview phases in order — do not skip phases without explicit user signal

## Core Principle

**SPEC.md is always the complete spec. SPEC/ files are optional lookup supplements.**

```
SPEC.md               # Always created, always self-sufficient
CLAUDE.md             # Generated with spec references

SPEC/                 # Optional, created only when user agrees
├── api-reference.md  # Lookup: endpoint schemas, request/response
├── sdk-patterns.md   # Lookup: external SDK usage patterns
└── data-models.md    # Lookup: complex entity schemas
```

- **SPEC.md** = Things you READ (narrative, decisions, requirements)
- **SPEC/*.md** = Things you LOOK UP (schemas, SDK patterns, external API details)

## Spec Types

The `/spec-writing` command handles four spec types. Detect or ask which type based on arguments and context.

| Type | Trigger | Output | Interview |
|------|---------|--------|-----------|
| Project | No argument, or `web-app`/`cli`/`api`/`library` | SPEC.md + CLAUDE.md + optional SPEC/ | Full 5-phase |
| Feature | `feature` argument, or user describes a feature | SPEC/FEATURE-[NAME].md or FEATURE_SPEC.md | 4-phase feature |
| Design | `design` argument, or user wants design system | SPEC/DESIGN-SYSTEM.md or DESIGN_SPEC.md | 3-phase design |
| Design Overhaul | `design:overhaul` argument | Same as Design + migration checklist | Audit-first + 3-phase design |

→ Full workflows, interview phases, and output templates: `references/spec-type-flows.md`

## Constraints

These rules are non-negotiable:

1. SPEC.md stands alone — never require SPEC/ files to understand the project
2. Use AskUserQuestion with options for every choice — open-ended information-gathering questions may use free-text format
3. Lead with recommended option first, include "(Recommended)" in label
4. Create SPEC/ supplements only when: user agrees AND content is reference material (schemas, tables, SDK patterns)
5. If Context7 fails, continue without external docs (see § Context7 Integration for failure handling)
6. If Write fails, check directory permissions and offer to output content directly
7. If a reference file cannot be read, continue with built-in knowledge for that section. Inform user once: "Reference file [name] unavailable — using built-in defaults."
8. Never invent requirements — only document what the user confirms

## Interview Methodology

### Single Adaptive Flow

One interview replaces all previous modes. Supplement prompts appear mid-flow when hitting reference-heavy topics.

```
Detect context (existing specs, codebase)
    ↓
Interview: Vision → Requirements → Architecture → Tech Stack → Design & Security
    ↓
Reference-heavy topic? → Ask: "Create SPEC/[topic].md for lookup?"
    ↓                              ↓
Continue interview            User decides (yes/no)
    ↓
Generate SPEC.md + CLAUDE.md
    ↓
If user agreed → Generate SPEC/[topic].md files
```

### Phase 1: Vision & Problem

Ask these questions (group related ones, 2-3 per AskUserQuestion turn):

- What problem does this project solve?
- Who is the target user?
- What does success look like?

### Phase 2: Requirements

- What are the 3-5 must-have features for MVP?
- What is explicitly OUT of scope?
- What is the primary user flow?

### Phase 3: Architecture

Present architecture options with tradeoffs. Reason through the recommendation based on the user's stated requirements before presenting:

```typescript
{
  question: "What architecture pattern fits best?",
  header: "Architecture",
  options: [
    {
      label: "Monolith (Recommended for MVP)",
      description: "Single deployable unit, simpler ops, faster iteration"
    },
    {
      label: "Serverless",
      description: "Pay-per-use, auto-scaling, vendor lock-in risk"
    },
    {
      label: "Microservices",
      description: "Team scaling, complex ops — use only if team size demands it"
    }
  ]
}
```

### Phase 4: Tech Stack

Present each tech choice with a recommended option first. Adapt recommendations based on project type and earlier answers. Skip categories that do not apply (e.g., no Frontend/Styling/Components for CLI/API/library).

→ Full defaults and ecosystem-specific rules: `references/interview-questions.md` § Turn 5 through Turn 10

### Phase 5: Design & Security

Ask only when relevant (has frontend or handles sensitive data):

- Visual style preference (if project has frontend)
- Authentication approach (if project has users)
- Compliance requirements (if project handles sensitive data)

These 5 conceptual phases map to 10 interview turns via smart batching — see `references/interview-questions.md` § Smart Batching Summary for the full turn-by-turn table.

### Smart Batching, Detection, and Auto-Detect

Group questions that share context into single AskUserQuestion turns. Skip turns when codebase analysis or prior answers already provide the answer. When codebase analysis detects answers (lockfiles, configs, dependencies), pre-fill and confirm instead of asking. When no project type argument is provided, infer from codebase signals and confirm with user.

→ Full 10-turn batching table with skip conditions: `references/interview-questions.md` § Smart Batching Summary
→ Codebase signal detection and auto-fill rules: `references/codebase-analysis.md`

### Supplement Prompts (Mid-Interview)

When a topic generates substantial reference material (10+ API endpoints, complex SDK integration, detailed schemas), ask:

```typescript
{
  question: "Your API has many endpoints. How should I document them?",
  header: "API Docs",
  options: [
    {
      label: "Inline in SPEC.md",
      description: "Keep everything in one file, shorter reference table"
    },
    {
      label: "Create SPEC/api-reference.md",
      description: "Separate lookup file for full schemas and examples"
    }
  ]
}
```

## Gap Analysis

Perform when spec type is Feature AND SPEC.md exists AND no explicit feature name provided AND codebase has 5+ source files.

**If gap analysis is skipped**, notify the user which condition was not met:
- No SPEC.md: "Gap analysis skipped: no SPEC.md found. Create a project spec first with `/spec-writing` for full gap analysis."
- Fewer than 5 source files: "Gap analysis skipped: codebase has fewer than 5 source files."
- Explicit feature name provided: skip silently (user already knows what they want).

1. **Extract specced features** from SPEC.md: "Core Features (MVP)", "Development Phases", "Future Scope"
2. **Scan codebase** for implemented features using patterns in `references/codebase-analysis.md`
3. **Categorize gaps**: specced-not-implemented, implemented-not-specced, pattern-based suggestions (e.g., "You have auth but no password reset")
4. **Present findings** via AskUserQuestion with options populated from gap results — prioritize specced-but-not-implemented

→ Full algorithm with scan patterns: `references/spec-type-flows.md` § Gap Analysis

## Design Audit

Perform when spec type is Design Overhaul. Runs before the design interview.

1. **Scan**: `tailwind.config.*`, `globals.css`, `src/components/ui/`, `src/components/`, `package.json`
2. **Document**: colors in use (hex values), typography, spacing, component inventory, animation patterns, inconsistencies, what works well
3. **Present**: audit report to user before proceeding to first-principles design interview

Output includes migration summary table (old → new → action) and phased migration checklist.

→ Full audit workflow and migration output: `references/spec-type-flows.md` § Design Overhaul Flow

If no existing design found: ask user whether to run standard design spec or specify design file locations manually. If minimal codebase (<2 style-related files): inform user of limited audit scope, then proceed with available artifacts.

## Codebase Analysis

→ Full detection patterns, framework mapping, and scanning tables: `references/codebase-analysis.md`

When analyzing an existing codebase:
1. Check for package managers and config files to confirm a project exists
2. Read `package.json` (or equivalent) to identify frameworks and dependencies
3. Scan source directories to map existing components, routes, models, and utilities
4. Use detected signals to pre-fill interview answers (see `references/codebase-analysis.md` § Codebase-Aware Skipping)

## Output Structures

### SPEC.md Structure

```markdown
# [Project Name]

> [One-line description]

## Overview
Problem statement, solution, target users, success criteria.

## Product Requirements
Core features (MVP) with user stories and acceptance criteria.
Future scope. Out of scope. User flows.

## Technical Architecture
Tech stack table with rationale.

## System Maps
- Architecture diagram (ASCII)
- Data model relations
- User flow diagrams
- Wireframes (if frontend project)

## Data Models
Entity definitions with TypeScript interfaces.

## API Endpoints
Endpoint table: method, path, description, auth requirement.

## Security
(If project has users or handles data)
Auth flow, input validation, sensitive data protection.

## Error Handling Strategy
Error format, error boundaries, retry logic.

## Design System
(If frontend) Colors, typography, spacing, components, accessibility.

## File Structure
Project directory layout.

## Monitoring & Observability
(If production app) Error tracking, logging, health checks.

## Development Phases
Phased implementation with checkboxes and task dependencies.

## Open Questions
Decisions to resolve, with proposed options and impact analysis.

---

## References
(If SPEC/ supplements exist)
→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using [SDK]: `SPEC/sdk-patterns.md`
```

Omit sections that do not apply (e.g., no Design System for CLI tools, no API Endpoints for libraries).

### Feature Spec & Design Spec Output

→ Templates and output location logic: `references/spec-type-flows.md`
→ Feature example: `examples/feature-spec.md`
→ Design example: `examples/design-spec.md`

### CLAUDE.md Structure

Agent-optimized pointer file — short, not a duplication of SPEC.md:

```markdown
# [Project Name]

[One-line description]

## Spec Reference

Primary spec: `SPEC.md`

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using [SDK/Library]: `SPEC/sdk-patterns.md`

## Key Constraints

- [Critical constraint 1 - surfaced from spec]
- [Critical constraint 2]
- [Out of scope reminder]

## Commands

- `[package-manager] run dev` - Start development
- `[package-manager] run test` - Run tests
- `[package-manager] run build` - Production build

## Current Status

→ Check `SPEC.md` → Development Phases section
```

### Supplement Structure

Each SPEC/ file follows this format:

```markdown
# [Title] Reference

> Lookup reference for [purpose]. See SPEC.md for full specification.

---

## [Section 1]
[Detailed reference content]

## [Section 2]
[Detailed reference content]

---

*Lookup reference. For project overview, see SPEC.md.*
```

## Context7 Integration

After tech choices are finalized, fetch documentation for each technology. Fetch multiple technologies in parallel when possible.

**Step 1**: Call `resolve-library-id` for each chosen technology.

**Step 2**: Call `query-docs` with targeted queries per technology category:

| Category | Query Templates |
|----------|----------------|
| Frontend framework | "How to set up [framework] with TypeScript", "[framework] app router file structure" |
| CSS framework | "[framework] configuration with custom theme", "[framework] dark mode setup" |
| Component library | "[library] installation and setup", "[library] form components" |
| Backend framework | "[framework] project structure with TypeScript", "[framework] middleware patterns" |
| Database + ORM | "[ORM] schema definition with [database]", "[ORM] migration workflow" |
| Auth | "[auth library] setup with [framework]", "[auth] JWT vs session comparison" |
| Deployment | "[platform] deployment configuration for [framework]" |

**Step 3**: Extract and include in SPEC.md:
- Recommended project structure from docs
- Configuration snippets (tsconfig, tailwind.config, etc.)
- Key patterns the framework expects (file-based routing, middleware chains, etc.)

### Context7 Failure Handling

| Failure | Action |
|---------|--------|
| `resolve-library-id` returns no match | Note in References: "Documentation for [tech] to be added manually." |
| `query-docs` returns no results | Note in References: "[Tech] documentation not available via Context7." |
| Context7 MCP tools unavailable | Skip all Context7 calls. Note in References: "External documentation not fetched (Context7 unavailable)." Inform user once. |

## Opinionated Recommendations

When presenting choices:

1. Place recommended option first with "(Recommended)" in the label
2. Include a one-sentence rationale in the description
3. Present 2-3 alternatives with honest tradeoffs
4. If the user's earlier answers suggest a different recommendation, adapt (e.g., if they chose Python backend, recommend FastAPI not Hono)

## Best Practices

### Interview Conduct
- Group 2-3 related questions per AskUserQuestion turn
- Skip questions whose answers are already known from codebase analysis
- If the user provides a project type argument, pre-fill the project type (skip detection) but still ask Phase 1 vision questions (marked "Never skip")
- Ruthlessly cut scope: "Is this needed for MVP, or is it future scope?"

### Output Quality
- Be specific: "Store user profiles with id, email, name, avatar, createdAt" not "Handle user data"
- Be actionable: "Return errors as `{ code, message, details }` JSON" not "Implement error handling"
- Include ASCII diagrams for architecture and data model relations
- Include TypeScript interfaces for data models
- Include Zod validation schemas alongside interfaces for input validation
- Keep scope realistic for MVP
- Include state diagrams for entities with lifecycle (e.g., task: pending → in_progress → completed → archived)
- Include algorithm specs for non-obvious behavior (e.g., search ranking, type inference, retry logic)
- Tech stack rationale must include: why chosen AND what was considered as alternative
- Acceptance criteria must be testable: include quantities, thresholds, or exact behaviors

## Reference Files

All paths below are relative to `skills/spec-writing/`. Commands use `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/` prefix for the same files.

### Templates
- `references/output-template.md` - Complete SPEC.md structure with all variations (primary reference)
- `references/spec-folder-template.md` - Supplement structure guide
- `templates/` - Per-section structural templates (legacy from v2.0, optional lookup when adapting individual sections — `output-template.md` is the primary reference for generation)

### Spec Type Flows
- `references/spec-type-flows.md` - Feature, design, and design overhaul workflows

### Codebase Analysis
- `references/codebase-analysis.md` - Detection patterns, framework mapping, scanning tables

### Session Prompt
- `references/session-prompt-template.md` - Compound engineering session prompt template

### Questions
- `references/interview-questions.md` - Full question bank with recommendations

### Examples
- `examples/web-app-spec.md` - Web application example
- `examples/cli-spec.md` - CLI tool example
- `examples/api-spec.md` - API service example
- `examples/library-spec.md` - Library example
- `examples/design-spec.md` - Design system example
- `examples/design-overhaul-spec.md` - Design overhaul with migration example
- `examples/feature-spec.md` - Feature specification example

## Integration with Other Skills

### feature-dev (if available)
After creating specs, use feature-dev agents:
1. `code-explorer` - Analyze existing patterns
2. `code-architect` - Design implementation blueprint
3. `code-reviewer` - Review implementation against spec

### frontend-design (if available)
Use design specs to implement components following the specification.

## Session Prompt (Compound Engineering)

After generating a spec with implementation phases, offer to create `prompt.md` at the project root. This bootstraps a compound engineering loop where each session: **Read** (find next unchecked phase) → **Ask** (clarify ambiguities) → **Plan** (Plan Mode) → **Work** (execute, test) → **Compound** (update checkboxes, record learnings) → **Report** (summarize progress). Each session makes the next smarter.

**Offer when**: Generated output has `- [ ]` checkboxes (always for project/feature/overhaul, conditional for design).
**Skip when**: No implementation phases, or "Document existing project" mode without new features.

→ Full template, parameterization rules, adaptation logic, and AskUserQuestion format: `references/session-prompt-template.md`

When `prompt.md` is generated, add to CLAUDE.md's Current Status: `→ Start new dev sessions with prompt.md`
