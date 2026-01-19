---
name: spec
version: 3.1.0
description: Generate project specifications with SPEC.md as core file and optional SPEC/ supplements
argument-hint: "[project-type: web-app | cli | api | library]"
allowed-tools:
  - AskUserQuestion
  - Write
  - Read
  - Glob
  - Grep
  - TodoWrite
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
---

# Project Specification Generator v3.1

Generate comprehensive project specifications with SPEC.md as the core file and optional supplements for reference material.

## Core Principle

**SPEC.md is always complete. SPEC/ files are optional lookup references.**

- **SPEC.md** = Things you READ (narrative, decisions, requirements)
- **SPEC/*.md** = Things you LOOK UP (schemas, SDK patterns, external APIs)

## Workflow

### 1. Check for Existing Specs

```
Check for (in order):
- SPEC.md
- SPEC/ folder
- PROJECT_SPEC.md (legacy)

If exists:
- Ask: Update existing or start fresh?
- If update: Load context and continue
```

### 2. Detect Existing Codebase

Check for indicators of existing code:
- `package.json` / `Cargo.toml` / `pyproject.toml` / `go.mod`
- `src/` or `app/` directories
- Config files (`.env`, `*.config.*`)
- Meaningful directory structure

**If existing codebase detected:**

```typescript
{
  question: "I see this is an existing project. What would you like to do?",
  header: "Mode",
  options: [
    {
      label: "Document existing project",
      description: "Analyze codebase and generate spec from what exists"
    },
    {
      label: "Plan new project",
      description: "Start fresh with interview-based planning"
    },
    {
      label: "Both",
      description: "Document existing + plan new features"
    }
  ]
}
```

**Document Existing Mode:**

1. Scan project configuration files:
   - `package.json` for dependencies and scripts
   - Config files for framework/tooling choices
   - Database schemas (Prisma, Drizzle, etc.)

2. Analyze directory structure:
   - Detect patterns (API routes, components, models)
   - Identify architectural style
   - Map existing file organization

3. Extract tech stack:
   - Frontend framework (Next.js, Vite, SvelteKit)
   - Styling approach (Tailwind, CSS Modules)
   - Backend framework (Express, Hono, FastAPI)
   - Database (PostgreSQL, MongoDB, SQLite)
   - ORM (Prisma, Drizzle)

4. Generate SPEC.md documenting what exists:
   - Current architecture and tech stack
   - Existing data models
   - API endpoints (if found)
   - File structure

5. Ask what to add/change:
   ```typescript
   {
     question: "What would you like to do next?",
     header: "Next Steps",
     options: [
       {
         label: "Add new features",
         description: "Continue with interview to plan additions"
       },
       {
         label: "Done for now",
         description: "Use this spec as documentation"
       }
     ]
   }
   ```

**Both Mode:**
- Run document existing first
- Then continue with interview for new features
- Merge into unified SPEC.md

### 3. Handle Project Type Argument

If project type provided:
- `web-app`: Focus on frontend, backend, database
- `cli`: Focus on commands, distribution
- `api`: Focus on endpoints, authentication
- `library`: Focus on public API, publishing

If not provided, determine during interview.

### 4. Conduct Interview

Single adaptive flow with ~15-20 questions grouped 2-4 per turn.

**Phase 1: Vision & Problem** (1-2 turns)
```
1. What problem does this solve? (one sentence)
2. Who is the target user?
3. What does success look like?
```

**Phase 2: Requirements** (2 turns)
```
1. What are the 3-5 must-have features for MVP?
2. What is explicitly OUT of scope?
3. What's the primary user flow?
```

**Phase 3: Architecture** (2 turns)

Present 2-3 alternatives with tradeoffs:

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
      description: "Pay-per-use, auto-scaling, vendor lock-in"
    },
    {
      label: "Microservices",
      description: "Team scaling, complex ops, use only if needed"
    }
  ]
}
```

**Phase 4: Tech Stack** (2-3 turns)

Use opinionated recommendations with override:

```typescript
{
  question: "Which package manager?",
  header: "Package Manager",
  options: [
    {
      label: "bun (Recommended)",
      description: "Fastest, built-in test runner, drop-in npm replacement"
    },
    {
      label: "pnpm",
      description: "Fast, strict deps, good for monorepos"
    },
    {
      label: "npm",
      description: "Universal compatibility, no setup"
    }
  ]
}
```

Similar for:
- Frontend framework (if applicable)
- Backend framework (if applicable)
- Database (if applicable)
- Deployment target

**Phase 5: Design & Security** (1-2 turns)
```
1. Visual style preference? (if frontend)
2. Authentication approach?
3. Any compliance requirements?
```

### 5. Supplement Prompts (Mid-Interview)

When hitting reference-heavy topics, ask:

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

Create supplements only for:
- **Reference material** - Schemas, tables, detailed examples
- **External dependencies** - SDK patterns, library usage, third-party APIs

### 6. Gather Tech Stack Documentation

Use Context7 MCP to fetch relevant docs:

```
1. resolve-library-id for each chosen technology
2. query-docs for setup guides and patterns
3. Include insights in SPEC.md or supplements
```

### 7. Generate SPEC.md

Use template from `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/output-template.md`

Structure:
```markdown
# [Project Name]

## Overview
Problem, solution, target users, success criteria.

## Product Requirements
Core features (MVP), future scope, out of scope, user flows.

## Technical Architecture
Tech stack (with rationale), system design diagram.

## System Maps
- Architecture diagram (ASCII)
- Data model relations
- User flow diagrams
- Wireframes (if applicable)

## Data Models
Entity definitions with TypeScript interfaces.

## API Endpoints (if applicable)
Endpoint table with method, path, description, auth.

## Design System (if frontend)
Colors, typography, components, accessibility.

## File Structure
Project directory layout.

## Development Phases
Phased implementation with checkboxes.

## Open Questions
Decisions to make during development.

---

## References
(If supplements exist)
→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using [SDK]: `SPEC/sdk-patterns.md`
```

### 8. Generate Supplements (If User Agreed)

Create `SPEC/` folder with requested supplements:

| File | Content |
|------|---------|
| `api-reference.md` | Full endpoint schemas, request/response examples |
| `data-models.md` | Complex entity relationships, validation rules |
| `sdk-patterns.md` | External SDK usage patterns and examples |

Each supplement should be self-contained lookup reference.

### 9. Generate CLAUDE.md

Agent-optimized pointer file:

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

### 10. Finalize

```
I've created your project specification:

- SPEC.md (complete specification)
- CLAUDE.md (agent reference)
[- SPEC/api-reference.md (if created)]
[- SPEC/data-models.md (if created)]

Would you like me to:
1. Walk through any section?
2. Add more detail to specific areas?
3. Start development?
```

## Best Practices

### Interview Conduct

- **Multiple choice**: Use AskUserQuestion, not open-ended text
- **Lead with recommendations**: Show preferred option first with rationale
- **2-3 alternatives**: For key decisions, present options with tradeoffs
- **YAGNI**: Ruthlessly simplify - "Do we really need this for MVP?"
- **Supplements on demand**: Only offer when truly reference-heavy

### Output Quality

- Be specific and actionable
- Include ASCII diagrams for system maps
- Include TypeScript interfaces for data models
- Reference Context7 documentation
- Keep scope realistic for MVP

## Error Handling

### User Abandons Interview
- Can resume with `/spec` again

### Context7 Failures
- Continue without external docs
- Note in spec that links need manual addition

### Write Failures
- Check directory permissions
- Offer to output content directly

## Reference Materials

Templates:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/output-template.md`

Questions:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md`

Examples:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/`
