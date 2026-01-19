---
name: feature
version: 3.1.0
description: Generate a feature specification for implementing new functionality in an existing project
argument-hint: "[feature-name]"
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

# Feature Specification Generator v3.1

Generate focused feature specifications for planning new features. Output adapts to project structure.

## Output Location

| Project Structure | Output File |
|-------------------|-------------|
| Has `SPEC/` folder | `SPEC/FEATURE-[NAME].md` |
| Has `SPEC.md` | `FEATURE_SPEC.md` (standalone) |
| Neither | `FEATURE_SPEC.md` (standalone) |

## When to Use

- Adding new functionality to an existing codebase
- Planning a feature before implementation
- Documenting feature requirements for team alignment
- Breaking down complex features into implementable steps

## Workflow

### 1. Detect Project Structure

```
1. Check for SPEC/ folder
   - If exists: Will write to SPEC/FEATURE-[NAME].md

2. Check for SPEC.md
   - If exists: Read for project context, write FEATURE_SPEC.md

3. If neither: Proceed with interview, write FEATURE_SPEC.md
```

### 2. Gap Analysis

When SPEC.md exists, perform gap analysis to help users identify what to build next.

**Step 1: Extract specced features from SPEC.md**
- Parse "Core Features (MVP)" section
- Parse "Development Phases" section
- Identify features marked as completed vs pending

**Step 2: Scan codebase for implemented features**
- Search for API routes in `src/api/`, `app/api/`, `routes/`
- Search for components in `src/components/`, `app/`
- Search for models in `src/models/`, `prisma/`, `drizzle/`
- Look for auth implementations, background jobs, integrations

**Step 3: Identify gaps**

```
Gap Types:
1. Specced but not implemented - In SPEC.md but no code found
2. Implemented but not specced - Code exists but not in SPEC.md
3. Pattern-based suggestions - Based on what exists, what's missing
```

**Step 4: Present findings**

```markdown
## Gap Analysis

**Specced but not implemented:**
- [ ] Password reset (SPEC.md → Auth section)
- [ ] Export to PDF (SPEC.md → Features)

**Implemented but not specced:**
- OAuth login (found in src/auth/oauth.ts)
- Rate limiting (found in middleware/rateLimit.ts)

**Suggested features based on patterns:**
- You have auth but no 2FA - want to add?
- You have projects but no project templates
- You have users but no user preferences
```

**Step 5: Ask user to choose**

```typescript
{
  question: "Which feature would you like to spec?",
  header: "Feature",
  options: [
    {
      label: "Password reset",
      description: "Specced but not implemented - complete the auth flow"
    },
    {
      label: "2FA / Two-factor auth",
      description: "Suggested - enhance existing auth security"
    },
    {
      label: "Document OAuth login",
      description: "Implemented but not specced - add to spec"
    },
    {
      label: "Something else",
      description: "Enter a custom feature to spec"
    }
  ]
}
```

**Skip gap analysis if:**
- No SPEC.md exists
- User provides explicit feature name argument
- Codebase is empty/minimal

### 3. Handle Feature Name Argument

If provided, use as starting point.
If not, ask what feature to build.

### 4. Conduct Feature Interview

~10-15 questions grouped 2-4 per turn with recommendations.

**Phase 1: Feature Definition** (1-2 turns)
```
1. What does this feature do? (one sentence)
2. What problem does it solve for users?
3. What is the expected user interaction?
```

**Phase 2: Scope & Requirements** (1-2 turns)
```
1. What are the must-have requirements?
2. What is explicitly out of scope?
3. Any dependencies on other features?
```

**Phase 3: Technical Approach** (2 turns)

Use multiple choice with recommendations:

```typescript
{
  question: "How should this feature store data?",
  header: "Data Storage",
  options: [
    {
      label: "Use existing database tables",
      description: "Extend current schema, simpler integration"
    },
    {
      label: "New dedicated tables",
      description: "Clean separation, more flexible"
    },
    {
      label: "No database changes needed",
      description: "Uses existing data or client-side only"
    }
  ]
}
```

Also ask:
- Which existing components/patterns to follow?
- New API endpoints needed?
- Third-party integrations?

**Phase 4: Edge Cases & Testing** (1 turn)
```
1. Key edge cases to handle?
2. Error states to design?
3. Testing approach?
```

### 5. Analyze Existing Codebase

Use Glob and Grep to understand:
- Existing patterns for similar features
- Related components and utilities
- API structure and conventions
- Database schema if relevant

### 6. Generate Feature Specification

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
- [Explicit exclusion 1]
- [Explicit exclusion 2]

## Technical Design

### Affected Components
- `path/to/component` - [Change description]

### New Components
- `path/to/new/component` - [Purpose]

### API Changes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/feature | Create feature item |

### Database Changes
```sql
-- Migration description
ALTER TABLE ... ADD COLUMN ...
```

## User Flow

```
[Start] → [Step 1] → [Step 2] → [End State]
```

## Implementation Plan

### Phase 1: Foundation
- [ ] Task 1
- [ ] Task 2

### Phase 2: Core Feature
- [ ] Task 3
- [ ] Task 4

### Phase 3: Polish
- [ ] Task 5

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| [Edge case 1] | [Behavior] |
| [Edge case 2] | [Behavior] |

## Testing Strategy

- **Unit**: [Component tests]
- **Integration**: [API tests]
- **E2E**: [User flow tests]

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]
```

### 7. Update SPEC/ Index (if applicable)

If writing to SPEC/ folder:
- Update `SPEC/00-INDEX.md` TOC with new feature file

### 8. Offer Next Steps

```
Feature spec created at [output path]!

Next steps:
1. Review and refine requirements
2. Use feature-dev skill to explore codebase patterns
3. Start implementation following the plan
```

## Integration with feature-dev

The generated feature spec works with feature-dev agents:

1. **code-explorer**: Analyze existing patterns
2. **code-architect**: Design implementation blueprint
3. **code-reviewer**: Review against spec

## Best Practices

### Scope Management
- Keep features focused and atomic
- Break large features into smaller specs
- Be explicit about what is NOT included

### Technical Planning
- Reference existing patterns in codebase
- Consider backwards compatibility
- Plan for incremental rollout if needed

### Quality Focus
- Include edge cases upfront
- Define testing strategy early
- Consider accessibility and performance

## Error Handling

### No Project Context
- Ask user to describe project briefly
- Proceed with interview
- Note assumptions in spec

### Large Feature Scope
- Suggest breaking into multiple specs
- Identify core MVP subset
- Create phased approach

## Reference Materials

Examples:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/feature-spec.md`
