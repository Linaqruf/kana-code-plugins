---
name: design
version: 3.0.0
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

# Design System Specification Generator v3.0

Generate comprehensive design system specifications for frontend projects. Output adapts to project structure.

## Output Location

| Project Structure | Output File |
|-------------------|-------------|
| Has `SPEC/` folder | `SPEC/DESIGN-SYSTEM.md` |
| Has `SPEC.md` | `DESIGN_SPEC.md` (standalone) |
| Neither | `DESIGN_SPEC.md` (standalone) |

## When to Use

- Starting a new frontend project and need design direction
- Existing project needs a documented design system
- Standardizing UI patterns across the codebase
- Planning to use frontend-design skill for implementation

## Workflow

### 1. Detect Project Structure

```
1. Check for SPEC/ folder
   - If exists: Will write to SPEC/DESIGN-SYSTEM.md

2. Check for SPEC.md
   - If exists: Read for tech stack context, write DESIGN_SPEC.md

3. Check for existing DESIGN_SPEC.md
   - If exists: Ask to update or start fresh
```

### 2. Handle Style Argument

If style provided, use as starting preset:
- `modern`: Clean lines, subtle shadows, rounded corners, neutral palette
- `minimal`: Sparse, lots of whitespace, monochrome, typography-focused
- `bold`: Strong colors, large text, geometric shapes, high contrast
- `custom`: Full interview for custom direction

### 3. Conduct Design Interview

~10-15 questions grouped 2-4 per turn with recommendations.

**Phase 1: Brand & Identity** (2 turns)

```typescript
{
  question: "What aesthetic best describes your vision?",
  header: "Style",
  options: [
    {
      label: "Modern/Clean (Recommended)",
      description: "Subtle shadows, rounded corners, professional"
    },
    {
      label: "Minimal",
      description: "Sparse, typography-focused, lots of whitespace"
    },
    {
      label: "Bold/Colorful",
      description: "Vibrant colors, high contrast, energetic"
    },
    {
      label: "Corporate",
      description: "Traditional, trustworthy, conservative"
    }
  ]
}
```

Also ask:
- Existing brand colors/guidelines?
- Light mode, dark mode, or both?

**Phase 2: Components & Layout** (2 turns)

```typescript
{
  question: "Which component library?",
  header: "Components",
  options: [
    {
      label: "shadcn/ui (Recommended)",
      description: "Copy-paste components, Tailwind-based, customizable"
    },
    {
      label: "Radix UI",
      description: "Unstyled primitives, full control"
    },
    {
      label: "Material UI",
      description: "Comprehensive, opinionated, Google style"
    },
    {
      label: "Custom components",
      description: "Build from scratch, maximum flexibility"
    }
  ]
}
```

Also ask:
- Primary navigation style? (top nav, sidebar, tabs)
- Key page types needed?

**Phase 3: Accessibility & UX** (1-2 turns)

```typescript
{
  question: "Animation preferences?",
  header: "Motion",
  options: [
    {
      label: "Subtle (Recommended)",
      description: "Micro-interactions, 150-300ms, professional"
    },
    {
      label: "Minimal",
      description: "Only essential transitions, respects reduced-motion"
    },
    {
      label: "Rich",
      description: "Expressive animations, delightful but heavier"
    }
  ]
}
```

Also ask:
- Accessibility level? (AA recommended)
- Loading state style? (skeleton/spinner)

### 4. Gather Component Documentation

Use Context7 MCP for chosen libraries:
- shadcn/ui component APIs
- Tailwind CSS configuration
- Radix UI primitives

### 5. Generate Design Specification

```markdown
# Design System: [Project Name]

## Brand Identity

### Color Palette

| Name | Value | Usage |
|------|-------|-------|
| Primary | `#3B82F6` | CTAs, links, focus states |
| Secondary | `#6366F1` | Accents, highlights |
| Success | `#10B981` | Success states, confirmations |
| Warning | `#F59E0B` | Warnings, cautions |
| Error | `#EF4444` | Errors, destructive actions |
| Neutral | `#6B7280` | Text, borders, backgrounds |

### Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | Inter | 36px | 700 |
| H2 | Inter | 30px | 600 |
| H3 | Inter | 24px | 600 |
| Body | Inter | 16px | 400 |
| Small | Inter | 14px | 400 |
| Code | JetBrains Mono | 14px | 400 |

### Spacing Scale

Base unit: 4px

`4, 8, 12, 16, 24, 32, 48, 64, 96`

## Component Library

**Selected**: [Library name]
**Rationale**: [Why this choice]

### Core Components

- [ ] Button (primary, secondary, ghost, destructive)
- [ ] Input (text, email, password, search)
- [ ] Select / Dropdown
- [ ] Checkbox / Radio
- [ ] Modal / Dialog
- [ ] Toast / Notification
- [ ] Card
- [ ] Table
- [ ] Navigation (header, sidebar, tabs)

### Component States

All interactive components must handle:
- Default, Hover, Focus, Active, Disabled, Loading, Error

## Layouts

### Responsive Breakpoints

| Name | Width | Target |
|------|-------|--------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablet |
| lg | 1024px | Desktop |
| xl | 1280px | Large desktop |

### Page Templates

| Page | Layout | Key Components |
|------|--------|----------------|
| Dashboard | App shell | Sidebar, Header, Main |
| Auth | Centered | Form card, Logo |
| Settings | Two-column | Nav, Content panel |

## Accessibility

- **WCAG Level**: AA
- **Color contrast**: 4.5:1 normal text, 3:1 large text
- **Focus indicators**: Visible on all interactive elements
- **Screen reader**: ARIA labels on icons and complex components
- **Keyboard**: Full tab, enter, escape support
- **Reduced motion**: Respect `prefers-reduced-motion`

## Interaction Patterns

### Animations

- **Micro**: 150ms ease-out
- **Page**: 300ms ease-in-out
- **Loading**: Skeleton screens preferred

### Error Handling UX

- Inline validation on blur
- Form-level errors at top
- Toast for async failures

## Implementation Notes

### CSS Architecture

```
styles/
├── globals.css      # Base styles, CSS variables
├── components/      # Component-specific styles
└── utilities/       # Custom utilities
```

### Theme Configuration

```typescript
// tailwind.config.ts
{
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        // ...
      }
    }
  }
}
```
```

### 6. Update SPEC/ Index (if applicable)

If writing to SPEC/ folder:
- Update `SPEC/00-INDEX.md` TOC

### 7. Offer Next Steps

```
Design spec created at [output path]!

Next steps:
1. Review and adjust color values
2. Run frontend-design skill to implement components
3. Set up Tailwind/CSS configuration
```

## Integration with frontend-design

The design spec works with frontend-design skill:
- Reference when implementing components
- Use defined colors and typography
- Follow documented patterns

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

## Error Handling

### No Project Context
- Proceed with design-focused interview
- Note tech stack should be decided separately

### Conflicting Preferences
- Point out conflicts (e.g., minimal + rich animations)
- Ask for clarification
- Suggest balanced alternatives

## Reference Materials

Examples:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/design-spec.md`
