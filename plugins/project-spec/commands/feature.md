---
name: feature
description: Generate a feature specification document for implementing new functionality in an existing project
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

# Feature Specification Generator

Generate a focused `feature_spec.md` for planning and implementing new features in existing projects.

## When to Use

- Adding new functionality to an existing codebase
- Planning a feature before implementation
- Documenting feature requirements for team alignment
- Breaking down complex features into implementable steps

## Workflow

### 1. Understand Context

First, gather project context:
- Read `project_spec.md` if it exists
- Scan codebase structure with Glob
- Identify relevant existing patterns

### 2. Handle Feature Name Argument

If a feature name was provided, use it as the starting point.
If not, ask the user what feature they want to build.

### 3. Conduct Feature Interview

Use AskUserQuestion to gather feature requirements. Ask 2-4 questions per interaction.

**Phase 1: Feature Definition**

```
Feature overview:
1. What does this feature do? (one sentence)
2. What problem does it solve for users?
3. What is the expected user interaction?
```

**Phase 2: Scope & Requirements**

```
Feature scope:
1. What are the must-have requirements for this feature?
2. What is explicitly out of scope?
3. Are there any dependencies on other features?
```

**Phase 3: Technical Approach**

```
Implementation questions:
1. Which existing components/patterns should this follow?
2. Does this require new API endpoints?
3. Does this require database changes?
4. Are there any third-party integrations needed?
```

**Phase 4: Edge Cases & Testing**

```
Quality considerations:
1. What are the key edge cases to handle?
2. What error states need to be designed?
3. How should this feature be tested?
```

### 4. Analyze Existing Codebase

Use Glob and Grep to understand:
- Existing patterns for similar features
- Related components and utilities
- API structure and conventions
- Database schema if relevant

### 5. Generate feature_spec.md

Write the feature specification:

```markdown
# Feature Specification: [Feature Name]

## Overview
- Description
- Problem Statement
- User Story

## Requirements
- Must Have
- Nice to Have
- Out of Scope

## Technical Design
- Affected Components
- New Components
- API Changes
- Database Changes

## Implementation Plan
- Step-by-step tasks
- Dependencies between steps

## UI/UX (if applicable)
- User flow
- Component designs
- States and interactions

## Edge Cases
- Error handling
- Boundary conditions

## Testing Strategy
- Unit tests
- Integration tests
- E2E scenarios

## Open Questions
```

### 6. Offer Next Steps

After generating, offer:
```
Feature spec created! Next steps:
1. Review and refine requirements
2. Use feature-dev skill to explore codebase patterns
3. Start implementation following the plan
```

## Integration with feature-dev

The generated `feature_spec.md` works with the `feature-dev` skill:

1. **code-explorer**: Analyze existing patterns relevant to the feature
2. **code-architect**: Design detailed implementation blueprint
3. **code-reviewer**: Review implementation against the spec

Suggest using these agents after the spec is created.

## Best Practices

### Scope Management
- Keep features focused and atomic
- Break large features into smaller specs
- Be explicit about what is NOT included

### Technical Planning
- Reference existing patterns in the codebase
- Consider backwards compatibility
- Plan for incremental rollout if needed

### Quality Focus
- Include edge cases upfront
- Define testing strategy early
- Consider accessibility and performance

## Error Handling

### No Project Context
If no project_spec.md or recognizable project structure:
- Ask user to describe the project briefly
- Proceed with feature interview
- Note assumptions in the spec

### Unclear Requirements
If user requirements are vague:
- Ask clarifying questions
- Provide examples of similar features
- Suggest starting with MVP scope

### Large Feature Scope
If the feature seems too large:
- Suggest breaking into multiple feature specs
- Identify the core MVP subset
- Create a phased approach

## Reference Materials

For feature interview questions:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md` (Feature section)

For example feature specifications:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/feature-spec.md`
