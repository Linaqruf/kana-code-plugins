---
name: spec
version: 4.0.0
description: Generate project specifications with SPEC.md as core file and optional SPEC/ supplements
argument-hint: "[project-type: web-app | cli | api | library]"
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

# Project Specification Generator v4.0

Generate comprehensive project specifications. Follow the methodology in the spec-writing skill (`${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/SKILL.md`).

## Workflow

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

**Both Mode:** Run document existing first, then continue with interview for new features.

### 3. Handle Project Type Argument

If a project type argument is provided, skip Phase 1 of the interview and tailor subsequent phases:

- `web-app`: Focus on frontend, backend, database, deployment
- `cli`: Focus on commands, arguments, distribution, output formats
- `api`: Focus on endpoints, authentication, rate limiting, documentation
- `library`: Focus on public API surface, types, publishing, versioning

### 4. Conduct Interview

Follow the interview methodology from the spec-writing skill. Use the question bank at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md` for detailed question options.

### 5. Fetch Tech Documentation

After tech choices are finalized, use Context7 to fetch documentation for each chosen technology. Follow the Context7 Integration section in the spec-writing skill.

### 6. Generate Output

Generate files using the output structures defined in the spec-writing skill:

1. **SPEC.md** — Complete specification (use template at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/output-template.md`)
2. **CLAUDE.md** — Agent-optimized pointer file
3. **SPEC/*.md** — Supplements, only if user agreed during interview

### 7. Finalize

Present summary of created files and offer next steps:

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

## Error Handling

- **User abandons interview**: Can resume with `/spec` again
- **Context7 failures**: Continue without external docs, note in References section
- **Write failures**: Check directory permissions, offer to output content directly
