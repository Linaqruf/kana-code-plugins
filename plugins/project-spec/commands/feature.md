---
name: feature
version: 4.1.0
description: Generate a feature specification for implementing new functionality in an existing project
argument-hint: "[feature-name]"
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

# Feature Specification Generator v4.1

Generate focused feature specifications. Follow the spec-writing skill methodology at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/SKILL.md` for interview conduct, output quality, and Context7 integration.

## Output Location

| Project Structure | Output File |
|-------------------|-------------|
| Has `SPEC/` folder | `SPEC/FEATURE-[NAME].md` |
| Has `SPEC.md` only | `FEATURE_SPEC.md` |
| Neither | `FEATURE_SPEC.md` |

## Workflow

### 1. Detect Project Structure

Check for `SPEC/` folder and `SPEC.md`. Read SPEC.md if it exists to extract project context.

### 2. Gap Analysis

Perform gap analysis when SPEC.md exists AND the user did not provide an explicit feature name argument.

**Step 1: Extract specced features**

Parse these SPEC.md sections:
- "Core Features (MVP)" — extract feature names and completion status
- "Development Phases" — extract tasks and checkbox status
- "Future Scope" — extract planned features

**Step 2: Scan codebase for implemented features**

Scan these patterns to find what actually exists:

| Pattern | What to Find |
|---------|-------------|
| `src/api/**`, `app/api/**`, `routes/**` | API endpoints |
| `src/components/**`, `app/components/**` | UI components |
| `src/models/**`, `prisma/schema.prisma`, `drizzle/schema.ts` | Data models |
| `src/auth/**`, `src/middleware/auth*` | Authentication |
| `middleware/**`, `src/middleware/**` | Middleware (rate limiting, CORS, etc.) |
| `src/hooks/**`, `src/composables/**` | Frontend hooks |
| `src/jobs/**`, `src/workers/**`, `src/queues/**` | Background jobs |
| `tests/**`, `__tests__/**`, `*.test.*`, `*.spec.*` | Test coverage |
| `src/lib/**`, `src/utils/**` | Shared utilities |

**Step 3: Identify gaps**

Categorize findings:

1. **Specced but not implemented** — In SPEC.md but no matching code found
2. **Implemented but not specced** — Code exists but not documented in SPEC.md
3. **Pattern-based suggestions** — Based on what exists, suggest missing complementary features (e.g., "You have auth but no password reset", "You have users but no user preferences")

**Step 4: Present findings and ask user to choose**

```typescript
{
  question: "Which feature would you like to spec?",
  header: "Feature",
  options: [
    // Populate from gap analysis results — prioritize specced-but-not-implemented
    {
      label: "[Gap 1 name]",
      description: "[Gap type] — [brief context]"
    },
    {
      label: "[Gap 2 name]",
      description: "[Gap type] — [brief context]"
    },
    {
      label: "[Suggestion]",
      description: "Suggested — [rationale from pattern analysis]"
    }
  ]
}
```

**Skip gap analysis when:**
- No SPEC.md exists
- User provides an explicit feature name argument
- Codebase has fewer than 5 source files

### 3. Conduct Feature Interview

Group 2-3 related questions per turn:

**Phase 1: Feature Definition**
- What does this feature do? (one sentence)
- What problem does it solve for users?
- What is the expected user interaction?

**Phase 2: Scope & Requirements**
- What are the must-have requirements?
- What is explicitly out of scope for this iteration?
- Dependencies on other features or systems?

**Phase 3: Technical Approach**

Use AskUserQuestion with options for key decisions:

```typescript
{
  question: "How should this feature store data?",
  header: "Data Storage",
  options: [
    {
      label: "Extend existing tables",
      description: "Add columns/relations to current schema"
    },
    {
      label: "New dedicated tables",
      description: "Clean separation, more flexible"
    },
    {
      label: "No database changes",
      description: "Uses existing data or client-side only"
    }
  ]
}
```

Also determine: affected components, new API endpoints, third-party integrations.

**Phase 4: Edge Cases & Testing**
- Key edge cases to handle
- Error states to design
- Testing approach (unit, integration, e2e)

### 4. Analyze Existing Codebase

Use Glob and Grep to understand existing patterns:
- How similar features are structured
- Naming conventions and code organization
- API route patterns and middleware chain
- Database schema conventions

### 5. Generate Feature Specification

```markdown
# Feature: [Feature Name]

## Overview
**Description**: [One sentence]
**Problem**: [What problem this solves]
**User Story**: As a [user], I want to [action] so that [benefit]

## Requirements

### Must Have
- [ ] [Requirement 1]
- [ ] [Requirement 2]

### Nice to Have
- [ ] [Optional feature]

### Out of Scope
- [Explicit exclusion]

## Technical Design

### Affected Components
- `path/to/component` — [Change description]

### New Components
- `path/to/new/component` — [Purpose]

### API Changes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/feature | Create feature item |

### Database Changes
[Migration SQL or schema changes]

## User Flow
[ASCII flow diagram]

## Implementation Plan
### Phase 1: Foundation
- [ ] Task 1
### Phase 2: Core Feature
- [ ] Task 2
### Phase 3: Polish
- [ ] Task 3

## Edge Cases
| Scenario | Expected Behavior |
|----------|-------------------|
| [Edge case] | [Behavior] |

## Testing Strategy
- **Unit**: [What to test]
- **Integration**: [What to test]
- **E2E**: [What to test]

## Open Questions
- [ ] [Unresolved decision]
```

### 6. Offer Next Steps

```
Feature spec created at [output path].

Next steps:
1. Review and refine requirements
2. Use feature-dev agents to explore codebase patterns and design implementation
3. Start implementation following the plan
```

## Integration with feature-dev

Generated feature specs work with feature-dev agents:
1. **code-explorer** — Analyze existing patterns relevant to this feature
2. **code-architect** — Design implementation blueprint from the spec
3. **code-reviewer** — Review implementation against spec requirements
