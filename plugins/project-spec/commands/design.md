---
name: design
version: 4.1.0
description: Generate a design system specification for frontend projects through an interactive interview
argument-hint: "[style: modern | minimal | bold | custom]"
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

# Design System Specification Generator v4.1

Generate design system specifications for frontend projects. Follow the spec-writing skill at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/SKILL.md` for interview conduct and output quality.

## Output Location

| Project Structure | Output File |
|-------------------|-------------|
| Has `SPEC/` folder | `SPEC/DESIGN-SYSTEM.md` |
| Has `SPEC.md` only | `DESIGN_SPEC.md` |
| Neither | `DESIGN_SPEC.md` |

## Workflow

### 1. Detect Project Structure

Check for `SPEC/` folder, `SPEC.md` (read for tech stack context), and existing `DESIGN_SPEC.md`. If a design spec exists, ask: update or start fresh.

### 2. Handle Style Argument

If a style argument is provided, use it as the starting preset and skip the aesthetic question:

- `modern`: Clean lines, subtle shadows, rounded corners, neutral palette
- `minimal`: Sparse, lots of whitespace, monochrome, typography-focused
- `bold`: Strong colors, large text, geometric shapes, high contrast
- `custom`: Full interview for custom direction

### 3. Conduct Design Interview

**Phase 1: Brand & Identity**

```typescript
{
  question: "What aesthetic best describes your vision?",
  header: "Style",
  options: [
    { label: "Modern/Clean (Recommended)", description: "Subtle shadows, rounded corners, professional" },
    { label: "Minimal", description: "Sparse, typography-focused, lots of whitespace" },
    { label: "Bold/Colorful", description: "Vibrant colors, high contrast, energetic" },
    { label: "Corporate", description: "Traditional, trustworthy, conservative" }
  ]
}
```

Also ask: existing brand colors/guidelines, light/dark mode preference.

**Phase 2: Components & Layout**

```typescript
{
  question: "Which component library?",
  header: "Components",
  options: [
    { label: "shadcn/ui (Recommended)", description: "Copy-paste components, Tailwind-based, customizable" },
    { label: "Radix UI", description: "Unstyled primitives, full control" },
    { label: "Material UI", description: "Comprehensive, opinionated, Google style" },
    { label: "Custom components", description: "Build from scratch, maximum flexibility" }
  ]
}
```

Also ask: navigation style (top nav, sidebar, tabs), key page types.

**Phase 3: Accessibility & UX**

```typescript
{
  question: "Animation preferences?",
  header: "Motion",
  options: [
    { label: "Subtle (Recommended)", description: "Micro-interactions, 150-300ms, professional" },
    { label: "Minimal", description: "Only essential transitions, respects reduced-motion" },
    { label: "Rich", description: "Expressive animations, delightful but heavier" }
  ]
}
```

Also ask: accessibility level (AA recommended), loading state style.

### 4. Fetch Component Documentation

Use Context7 to fetch docs for chosen component library and CSS framework.

### 5. Generate Design Specification

Output a complete design spec with:
- Color palette (primary, semantic colors with hex values and usage)
- Typography scale (font, size, weight for each heading level and body)
- Spacing scale (base unit and full scale)
- Component library selection with rationale
- Core components checklist with states
- Responsive breakpoints
- Page layout templates
- Accessibility requirements (WCAG level, contrast ratios, focus indicators)
- Animation timing and patterns
- CSS architecture and theme configuration

### 6. Finalize

If writing to `SPEC/`, update `SPEC/00-INDEX.md`. Present created files and suggest next steps: review colors, run frontend-design skill, set up Tailwind/CSS config.
