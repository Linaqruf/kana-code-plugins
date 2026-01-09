---
name: design
version: 1.0.2
description: Generate a design system specification for frontend projects through an interactive interview
argument-hint: "[style: modern | minimal | bold | custom]"
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

# Design System Specification Generator

Generate a comprehensive `design_spec.md` for frontend projects through structured interviews about visual design, components, and UX patterns.

## When to Use

- Starting a new frontend project and need design direction
- Existing project needs a documented design system
- Want to standardize UI patterns across the codebase
- Planning to use the frontend-design skill for implementation

## Workflow

### 1. Check Context

First, check for existing files:
- If `project_spec.md` exists, read it for tech stack context
- If `design_spec.md` exists, ask user if they want to update or start fresh

### 2. Handle Style Argument

If a style argument was provided:
- `modern`: Clean lines, subtle shadows, rounded corners, neutral palette
- `minimal`: Sparse, lots of whitespace, monochrome, typography-focused
- `bold`: Strong colors, large text, geometric shapes, high contrast
- `custom`: Full interview for custom design direction

### 3. Conduct Design Interview

Use AskUserQuestion to gather design preferences. Ask 2-4 questions per interaction.

**Phase 1: Brand & Identity**

```
Design direction questions:
1. Do you have existing brand colors/guidelines?
2. What aesthetic best describes your vision?
   - Modern/Clean - subtle, professional
   - Minimal - sparse, typography-focused
   - Bold/Colorful - vibrant, energetic
   - Corporate - traditional, trustworthy
3. Light mode, dark mode, or both?
```

**Phase 2: Components & Layout**

```
UI component questions:
1. Component library preference?
   - shadcn/ui (Recommended)
   - Radix UI
   - Material UI
   - Custom components
2. Primary navigation style?
   - Top navbar
   - Sidebar
   - Bottom tabs (mobile)
3. Key page types needed?
```

**Phase 3: Accessibility & UX**

```
UX requirements:
1. Accessibility level? (AA recommended)
2. Animation preferences? (minimal/subtle/rich)
3. Loading state style? (skeleton/spinner)
```

### 4. Gather Component Documentation

Use Context7 MCP to fetch documentation for chosen libraries:
- shadcn/ui component APIs
- Tailwind CSS configuration
- Radix UI primitives

### 5. Generate design_spec.md

Write the design specification with all sections:

```markdown
# Design Specification: [Project Name]

## Brand Identity
- Color Palette (with hex values and usage)
- Typography Scale
- Spacing System

## Component Library
- Selected library and rationale
- Core components list
- Component states

## Layouts
- Page templates
- Responsive breakpoints
- Grid system

## Accessibility
- WCAG level
- Focus states
- Screen reader considerations

## Interaction Patterns
- Animation guidelines
- Loading states
- Error handling UX

## Implementation Notes
- CSS architecture
- Token organization
- Theme configuration
```

### 6. Offer Next Steps

After generating, offer:
```
Design spec created! Next steps:
1. Review and adjust color values
2. Run frontend-design skill to implement components
3. Set up Tailwind/CSS configuration
```

## Integration with frontend-design

The generated `design_spec.md` can be used by the `frontend-design` skill:
- Reference the spec when implementing components
- Use defined colors and typography
- Follow the documented patterns

## Best Practices

### Color Selection
- Ensure sufficient contrast ratios
- Define semantic colors (success, error, warning)
- Include hover/active variants

### Typography
- Limit to 2-3 font families max
- Define clear hierarchy
- Consider loading performance

### Components
- Document all interactive states
- Include accessibility requirements
- Note animation timing

## Reference Materials

For design questions and examples:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md` (Design & UX section)
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/design-spec.md`

## Error Handling

### No Project Context
If no project_spec.md exists:
- Proceed with design-focused interview
- Note that tech stack should be decided separately

### Conflicting Preferences
If user choices conflict (e.g., minimal + rich animations):
- Point out the conflict
- Ask for clarification
- Suggest balanced alternatives
