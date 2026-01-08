---
name: spec
description: Generate a comprehensive project specification document through an interactive interview process
argument-hint: "[project-type: web-app | cli | api | library]"
allowed-tools:
  - AskUserQuestion
  - Write
  - Read
  - Glob
  - Grep
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
---

# Project Specification Generator

Generate a comprehensive `project_spec.md` through structured interviews before building.

## Workflow

### 1. Check for Existing Spec

First, check if a project_spec.md already exists:
- If exists, ask user if they want to update it or start fresh
- If not exists, proceed with interview

### 2. Handle Project Type Argument

If a project type argument was provided:
- `web-app`: Focus on frontend, backend, database, auth questions
- `cli`: Focus on commands, arguments, distribution questions
- `api`: Focus on endpoints, authentication, data models questions
- `library`: Focus on public API, documentation, publishing questions

If no argument, determine project type during interview.

### 3. Conduct Interview

Use AskUserQuestion to gather information. Ask 2-4 questions per interaction.

**Phase 1: Product Requirements**

Start with:
```
Questions about your project:
1. What problem does this project solve? (one sentence)
2. Who is the target user?
3. What are the 3-5 must-have features for MVP?
```

Follow up with:
```
Questions about scope:
1. What features are explicitly out of scope for now?
2. Any existing products that inspired this?
```

**Phase 2: Technical Design**

Based on project type, ask about tech stack:
```
Technical preferences:
1. Frontend framework? (Next.js, Vue, Svelte, none)
2. Backend approach? (Node.js, Python, serverless, none)
3. Database needs? (PostgreSQL, MongoDB, SQLite, none)
4. Deployment target? (Vercel, AWS, self-hosted)
```

**Phase 3: Constraints**

```
Project constraints:
1. Solo developer or team?
2. Any existing codebase to integrate with?
3. Budget constraints for paid services?
```

### 4. Gather Tech Stack Documentation

After tech choices are made, use Context7 MCP to fetch relevant documentation:

1. Resolve library IDs for chosen technologies
2. Query for setup guides and best practices
3. Include relevant insights in the spec

Example:
```
For Next.js + Prisma + PostgreSQL:
- Query Next.js: "app router setup authentication"
- Query Prisma: "PostgreSQL schema best practices"
```

### 5. Generate project_spec.md

Write the specification to the project root with all sections:

```markdown
# Project Specification: [Name]

## Overview
- Problem Statement
- Solution
- Target Users
- Success Criteria

## Product Requirements
- Core Features (MVP) with user stories
- Future Scope
- Out of Scope

## Technical Architecture
- Tech Stack table
- System Design diagram
- Data Models
- API Endpoints (if applicable)

## File Structure
- Proposed directory layout

## Dependencies
- Production and dev dependencies

## Environment Variables
- Required configuration

## Development Phases
- Logical groupings of work

## Open Questions
- Unresolved decisions

## References
- Documentation links
```

### 6. Confirm and Finalize

After generating, ask user:
```
I've created project_spec.md with [X] sections covering [summary].

Would you like me to:
1. Walk through any section in detail?
2. Add more details to specific areas?
3. Proceed with development?
```

## Best Practices

### Interview Conduct
- Ask 2-4 questions maximum per interaction
- Provide sensible defaults when user is uncertain
- Skip irrelevant questions based on project type
- Summarize understanding before generating

### Specification Quality
- Be specific and actionable
- Include code examples for data models
- Link to external documentation
- Keep scope realistic for MVP

### Output Location
- Write to `./project_spec.md` in the current working directory
- Use standard markdown formatting
- Include timestamp at bottom

## Reference Materials

For detailed question banks and templates, refer to:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/output-template.md`

For example specifications:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/web-app-spec.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/cli-spec.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/api-spec.md`
