---
name: spec-writing
description: Use when the user wants to create project specs, design systems, or feature plans. Triggers on "create spec", "plan project", "design system", "plan feature", or "write specification".
version: 4.0.0
---

# Spec Writing v4.0

Authoritative methodology for generating project specifications. All commands and agents reference this skill.

## Prompt Principles

### Adaptive Thinking

Mark where deep reasoning adds value vs where to execute directly:

- **Execute directly**: File detection, template application, output formatting, version checks
- **Reason deeply**: Architecture decisions, tech stack tradeoffs, scope boundaries, gap analysis findings, codebase pattern recognition

When presenting choices to the user, include concrete rationale with tradeoffs — not just labels.

### Literal Interpretation

- Use imperative mood: "Ask", "Create", "Skip" — never "consider", "might want to", "you could"
- Make conditions explicit: "If package.json lists react, vue, svelte, or angular as a dependency" — never "if applicable"
- Every AskUserQuestion call must use the options parameter with 2-4 choices
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

## Constraints

These rules are non-negotiable:

1. SPEC.md stands alone — never require SPEC/ files to understand the project
2. Use AskUserQuestion with options for every choice — never ask open-ended questions
3. Lead with recommended option first, include "(Recommended)" in label
4. Create SPEC/ supplements only when: user agrees AND content is reference material (schemas, tables, SDK patterns)
5. If Context7 fails, continue without external docs and note "Documentation links to be added manually" in the References section
6. If Write fails, check directory permissions and offer to output content directly
7. Never invent requirements — only document what the user confirms

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

Present each tech choice with a recommended option. Adapt recommendations based on project type and earlier answers:

- **Package manager**: bun (recommended), pnpm, npm
- **Frontend**: Next.js (recommended for web apps), Vite + React, SvelteKit, None
- **Styling**: Tailwind CSS (recommended), CSS Modules, Styled Components
- **Components**: shadcn/ui (recommended), Radix UI, Material UI, Custom
- **Backend**: Hono (recommended), Express, FastAPI, Next.js API Routes
- **Database**: PostgreSQL (recommended), SQLite, MongoDB, None
- **ORM**: Drizzle (recommended), Prisma, Raw SQL
- **Deployment**: Vercel (recommended for Next.js), Cloudflare Pages, Railway/Fly.io, Self-hosted

Skip categories that do not apply. If the user chose "No frontend" in Phase 3, skip Frontend/Styling/Components.

### Phase 5: Design & Security

Ask only when relevant (has frontend or handles sensitive data):

- Visual style preference (if project has frontend)
- Authentication approach (if project has users)
- Compliance requirements (if project handles sensitive data)

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

## Codebase Analysis

### Detecting Existing Projects

Scan for these indicators to determine if a codebase exists:

**Package managers & configs:**
- `package.json`, `bun.lockb`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`
- `Cargo.toml`, `Cargo.lock`
- `pyproject.toml`, `requirements.txt`, `Pipfile`
- `go.mod`, `go.sum`
- `composer.json`
- `Gemfile`

**Source directories:**
- `src/`, `app/`, `lib/`, `pkg/`, `internal/`
- `pages/`, `routes/`, `api/`
- `components/`, `views/`, `templates/`

**Config files:**
- `.env`, `.env.local`, `.env.example`
- `*.config.ts`, `*.config.js`, `*.config.mjs`
- `tsconfig.json`, `jsconfig.json`
- `Dockerfile`, `docker-compose.yml`
- `.github/workflows/`

### Framework Detection

Read `package.json` dependencies to identify:

| Dependency | Framework |
|-----------|-----------|
| `next` | Next.js |
| `react` | React (check for Next.js first) |
| `vue` | Vue.js |
| `svelte`, `@sveltejs/kit` | SvelteKit |
| `@angular/core` | Angular |
| `express` | Express.js |
| `hono` | Hono |
| `fastify` | Fastify |
| `@prisma/client` | Prisma ORM |
| `drizzle-orm` | Drizzle ORM |
| `tailwindcss` | Tailwind CSS |

For Python: read `pyproject.toml` or `requirements.txt` for `fastapi`, `django`, `flask`.
For Rust: read `Cargo.toml` for `actix-web`, `axum`, `rocket`.
For Go: read `go.mod` for `gin`, `echo`, `fiber`.

### Deep Codebase Scanning

When documenting an existing project, scan these patterns:

| Pattern | What to Extract |
|---------|----------------|
| `src/api/**`, `app/api/**`, `routes/**` | API endpoints |
| `src/components/**`, `app/components/**` | UI components |
| `src/models/**`, `prisma/schema.prisma`, `drizzle/schema.ts` | Data models |
| `src/lib/**`, `src/utils/**`, `src/helpers/**` | Shared utilities |
| `src/hooks/**`, `src/composables/**` | Frontend hooks/composables |
| `middleware/**`, `src/middleware/**` | Middleware (auth, rate limiting) |
| `src/jobs/**`, `src/workers/**`, `src/queues/**` | Background jobs |
| `tests/**`, `__tests__/**`, `*.test.*`, `*.spec.*` | Test coverage |
| `src/styles/**`, `tailwind.config.*` | Styling system |
| `src/types/**`, `src/@types/**` | Type definitions |
| `.github/workflows/**` | CI/CD pipelines |

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

## Design System
(If frontend) Colors, typography, spacing, components, accessibility.

## File Structure
Project directory layout.

## Development Phases
Phased implementation with checkboxes.

## Open Questions
Decisions to resolve during development.

---

## References
(If SPEC/ supplements exist)
→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using [SDK]: `SPEC/sdk-patterns.md`
```

Omit sections that do not apply (e.g., no Design System for CLI tools, no API Endpoints for libraries).

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

After tech choices are finalized, fetch documentation for each technology:

1. Call `resolve-library-id` for each chosen technology (e.g., "next.js", "drizzle-orm", "hono")
2. Call `query-docs` with specific queries:
   - Setup/installation: "How to set up [library] with TypeScript"
   - Key patterns: "[library] recommended project structure"
   - Integration: "How to use [library A] with [library B]"
3. Include relevant patterns and configuration in SPEC.md or supplements

If resolve-library-id returns no results, skip that technology and note it in the References section.

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
- If the user provides a project type argument, skip Phase 1 and adjust Phase 2
- Ruthlessly cut scope: "Is this needed for MVP, or is it future scope?"

### Output Quality
- Be specific: "Store user profiles with id, email, name, avatar, createdAt" not "Handle user data"
- Be actionable: "Return errors as `{ code, message, details }` JSON" not "Implement error handling"
- Include ASCII diagrams for architecture and data model relations
- Include TypeScript interfaces for data models
- Keep scope realistic for MVP

## Reference Files

### Templates
- `references/output-template.md` - SPEC.md structure with all variations
- `references/spec-folder-template.md` - Supplement structure guide
- `templates/` - Individual section templates

### Questions
- `references/interview-questions.md` - Full question bank with recommendations

### Examples
- `examples/web-app-spec.md` - Web application example
- `examples/cli-spec.md` - CLI tool example
- `examples/api-spec.md` - API service example
- `examples/library-spec.md` - Library example
- `examples/design-spec.md` - Design system example
- `examples/feature-spec.md` - Feature specification example

## Related Commands

- `/spec` - Generate project specification (uses this methodology)
- `/feature` - Generate feature specification (uses interview phases from this skill)
- `/design` - Generate design system specification
- `/design:overhaul` - First-principles design redesign
- `/sync` - Git-aware spec drift detection

## Integration with Other Skills

### feature-dev
After creating specs, use feature-dev agents:
1. `code-explorer` - Analyze existing patterns
2. `code-architect` - Design implementation blueprint
3. `code-reviewer` - Review implementation against spec

### frontend-design
Use design specs to implement components following the specification.
