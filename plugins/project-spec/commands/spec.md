---
name: spec
version: 4.0.0
description: Generate project, feature, or design specifications with SPEC.md as core file
argument-hint: "[project-type | feature [name] | design [style] | design:overhaul]"
allowed-tools:
  - AskUserQuestion
  - Write
  - Read
  - Glob
  - Grep
  - TodoWrite
  - Task
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
---

# Specification Generator v4.0

Generate specifications for projects, features, and design systems. Follow the methodology in the spec-writing skill (`${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/SKILL.md`).

## Routing

Parse the argument to determine spec type:

| Argument | Spec Type | Entry Point |
|----------|-----------|-------------|
| (none) | Project | Check existing specs → detect codebase → interview |
| `web-app`, `cli`, `api`, `library` | Project | Skip Phase 1, tailor to type |
| `feature` | Feature | Gap analysis → feature interview |
| `feature [name]` | Feature | Skip gap analysis → feature interview |
| `design` | Design | Detect existing → design interview |
| `design [style]` | Design | Use preset, skip aesthetic question |
| `design:overhaul` | Design Overhaul | Audit → first-principles interview |

## Project Spec Flow

### 1. Check for Existing Specs

Check for `SPEC.md`, `SPEC/` folder, or `PROJECT_SPEC.md` (legacy). If any exist, ask:

```typescript
{
  question: "I found an existing specification. What would you like to do?",
  header: "Existing Spec",
  options: [
    {
      label: "Update existing spec",
      description: "Load current spec and update based on new requirements"
    },
    {
      label: "Start fresh",
      description: "Create a new specification from scratch"
    }
  ]
}
```

### 2. Detect Existing Codebase

Scan for project indicators using the patterns in the spec-writing skill's "Codebase Analysis" section.

If an existing codebase is detected:

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

1. Read project config files (package.json, Cargo.toml, pyproject.toml, etc.)
2. Detect framework using the dependency table in the spec-writing skill
3. Scan directory structure using the deep scanning patterns
4. Extract: tech stack, data models, API endpoints, file structure
5. Generate SPEC.md documenting current state
6. Ask if user wants to add new features (continue to interview) or stop

### 3. Handle Project Type Argument

If a project type argument is provided, skip Phase 1 of the interview and tailor subsequent phases:

- `web-app`: Focus on frontend, backend, database, deployment
- `cli`: Focus on commands, arguments, distribution, output formats
- `api`: Focus on endpoints, authentication, rate limiting, documentation
- `library`: Focus on public API surface, types, publishing, versioning

### 4. Conduct Interview

Follow the interview methodology from the spec-writing skill. Use the question bank at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md`.

### 5. Fetch Tech Documentation

After tech choices are finalized, use Context7 to fetch documentation. Follow the Context7 Integration section in the spec-writing skill.

### 6. Generate Output

1. **SPEC.md** — Complete specification (use template at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/output-template.md`)
2. **CLAUDE.md** — Agent-optimized pointer file
3. **SPEC/*.md** — Supplements, only if user agreed during interview

### 7. Finalize

Present summary of created files and offer next steps.

## Feature Spec Flow

→ Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/spec-type-flows.md` § Feature Spec Flow

1. Detect project structure (`SPEC/` folder, `SPEC.md`)
2. If no explicit feature name: run gap analysis (see SKILL.md § Gap Analysis)
3. Conduct 4-phase feature interview (see `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md` § Feature Planning)
4. Analyze existing codebase for patterns relevant to the feature
5. Generate feature specification
6. Offer next steps: review, use feature-dev agents, start implementation

## Design Spec Flow

→ Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/spec-type-flows.md` § Design Spec Flow

1. Detect project structure and existing design specs (`DESIGN_SPEC.md`, `SPEC/DESIGN-SYSTEM.md`)
2. If existing design found: ask update or start fresh
3. Handle style argument (`modern`/`minimal`/`bold` → preset, skip aesthetic question)
4. Conduct 3-phase design interview (see `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md` § Design System)
5. Fetch component library documentation via Context7
6. Generate design specification
7. Suggest next steps: review colors, run frontend-design skill, set up CSS config

## Design Overhaul Flow

→ Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/spec-type-flows.md` § Design Overhaul Flow

1. Audit current design system (see SKILL.md § Design Audit)
2. Present audit report to user
3. Conduct first-principles design interview ("Forget the current design. What do you want?")
4. Generate new design system with migration notes
5. Generate migration checklist (Foundation → Components → Pages → Cleanup)
6. Suggest next steps: review checklist, update Tailwind config first, migrate incrementally

## Error Handling

- **User abandons interview**: Resume with `/spec` again
- **Context7 failures**: Continue without external docs, note in References section
- **Write failures**: Check directory permissions, offer to output content directly
- **No existing design (overhaul)**: Skip audit, run standard design flow
- **Minimal codebase (overhaul)**: Note limited audit scope
