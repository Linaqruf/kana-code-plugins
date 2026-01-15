---
name: design
version: 2.0.0
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

# Design System Specification Generator v2.0

Generate comprehensive design system specifications for frontend projects. Adapts output location based on project structure.

## Output Location

| Project Structure | Output File |
|-------------------|-------------|
| Has `SPEC/` folder | `SPEC/XX-DESIGN-SYSTEM.md` (creates or updates) |
| Has `SPEC.md` or `PROJECT_SPEC.md` | `DESIGN_SPEC.md` (standalone) |
| Neither | `DESIGN_SPEC.md` (standalone) |

## When to Use

- Starting a new frontend project and need design direction
- Existing project needs a documented design system
- Want to standardize UI patterns across the codebase
- Planning to use the frontend-design skill for implementation

## Workflow

### 1. Detect Project Structure

Check for existing specs in order:

```
1. Check for SPEC/ folder
   - If exists: Check for existing XX-DESIGN-SYSTEM.md
   - Read SPEC/00-INDEX.md for project context

2. Check for SPEC.md or PROJECT_SPEC.md (legacy)
   - If exists: Read for tech stack context

3. Check for DESIGN_SPEC.md
   - If exists: Ask user to update or start fresh
```

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

### 5. Generate Design Specification

**Determine output file:**

```typescript
if (hasSpecFolder) {
  // Check for existing design-system file
  const existingDesign = glob('SPEC/*-DESIGN-SYSTEM.md')[0];
  if (existingDesign) {
    outputFile = existingDesign; // Update existing
  } else {
    // Find next available number
    const existingFiles = glob('SPEC/*.md');
    const maxNumber = Math.max(...existingFiles.map(f => parseInt(f.split('-')[0])));
    const nextNumber = String(maxNumber + 1).padStart(2, '0');
    outputFile = `SPEC/${nextNumber}-DESIGN-SYSTEM.md`;
  }
} else {
  outputFile = 'DESIGN_SPEC.md';
}
```

**Write the design specification:**

```markdown
# Design System: [Project Name]

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

### 6. Update SPEC/ Index (if applicable)

If writing to SPEC/ folder:
- Update `SPEC/00-INDEX.md` TOC with design system file (if new)
- Note in `SPEC/XX-CHANGELOG.md` if it exists

### 7. Offer Next Steps

After generating, offer:
```
Design spec created at [output path]!

Next steps:
1. Review and adjust color values
2. Run frontend-design skill to implement components
3. Set up Tailwind/CSS configuration
```

## Integration with frontend-design

The generated `DESIGN_SPEC.md` can be used by the `frontend-design` skill:
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
If no SPEC.md/PROJECT_SPEC.md exists:
- Proceed with design-focused interview
- Note that tech stack should be decided separately

### Conflicting Preferences
If user choices conflict (e.g., minimal + rich animations):
- Point out the conflict
- Ask for clarification
- Suggest balanced alternatives
