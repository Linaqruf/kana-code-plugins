---
name: design:overhaul
version: 1.0.0
description: First-principles design system redesign - audit existing, then rebuild from scratch
argument-hint: ""
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

# Design Overhaul Command v1.0

Complete design system redesign from first principles. Audits existing design, then rebuilds with fresh decisions and provides migration guidance.

## When to Use

- Current design feels inconsistent or outdated
- Major visual rebrand needed
- Accumulated design debt from quick iterations
- Switching component libraries or design approaches
- Want to rethink design decisions from scratch

## Output

Creates `DESIGN_SPEC.md` (or `SPEC/DESIGN-SYSTEM.md`) with:
- New design system specification
- Migration notes from old to new
- Deprecation warnings for old patterns

## Workflow

### 1. Audit Current Design

**Step 1: Scan existing styles**

```
Search for:
- tailwind.config.* / tailwind.config.ts
- globals.css / global.css / styles/
- CSS variables / theme definitions
- Color tokens / design tokens
```

**Step 2: Analyze components**

```
Search for:
- src/components/ui/ (shadcn pattern)
- src/components/ (general)
- Component libraries in package.json (shadcn, radix, mui, etc.)
```

**Step 3: Identify patterns**

Document what exists:
- Color palette in use
- Typography styles
- Spacing patterns
- Component inventory
- Animation patterns

**Step 4: Present audit findings**

```markdown
## Current Design Audit

**Colors Found:**
- Primary: `#3B82F6` (blue-500)
- Background: `#F9FAFB` (gray-50)
- 5 other accent colors in use

**Typography:**
- Font: Inter (via next/font)
- Inconsistent heading sizes (h1 ranges from 24px to 48px)

**Components:**
- Using shadcn/ui: Button, Card, Dialog
- Custom: Sidebar, Header, DataTable

**Issues Identified:**
- 3 different button styles across the app
- No consistent spacing scale
- Color contrast issues on some secondary buttons
- Outdated dialog animation pattern

**What's Working Well:**
- shadcn/ui foundation is solid
- Inter font is well-integrated
- Dark mode support exists
```

### 2. First-Principles Interview

Start fresh, ignoring current implementation.

**Phase 1: Vision Reset** (1 turn)

```typescript
{
  question: "Forget the current design. What aesthetic do you actually want?",
  header: "Vision",
  options: [
    {
      label: "Modern/Clean",
      description: "Subtle shadows, rounded corners, professional"
    },
    {
      label: "Minimal/Sparse",
      description: "Typography-focused, lots of whitespace, monochrome"
    },
    {
      label: "Bold/Vibrant",
      description: "Strong colors, high contrast, energetic"
    },
    {
      label: "Premium/Refined",
      description: "Subtle, sophisticated, attention to detail"
    }
  ]
}
```

**Phase 2: Core Primitives** (2 turns)

```typescript
{
  question: "What are your absolute must-have UI primitives?",
  header: "Components",
  multiSelect: true,
  options: [
    {
      label: "Form controls",
      description: "Input, Select, Checkbox, Radio, Textarea"
    },
    {
      label: "Feedback components",
      description: "Toast, Alert, Dialog, Loading states"
    },
    {
      label: "Navigation",
      description: "Sidebar, Tabs, Breadcrumb, Menu"
    },
    {
      label: "Data display",
      description: "Table, List, Card, Badge"
    }
  ]
}
```

```typescript
{
  question: "Component library approach?",
  header: "Library",
  options: [
    {
      label: "shadcn/ui (Recommended)",
      description: "Keep or adopt - flexible, Tailwind-based"
    },
    {
      label: "Radix primitives only",
      description: "Unstyled, maximum control"
    },
    {
      label: "Custom from scratch",
      description: "Full control, more work"
    },
    {
      label: "Keep current + fix issues",
      description: "Incremental improvement, less disruption"
    }
  ]
}
```

**Phase 3: Accessibility & Motion** (1 turn)

```typescript
{
  question: "Accessibility level?",
  header: "Accessibility",
  options: [
    {
      label: "WCAG AA (Recommended)",
      description: "Standard compliance, good for most projects"
    },
    {
      label: "WCAG AAA",
      description: "Strict compliance, enhanced accessibility"
    },
    {
      label: "Basic accessibility",
      description: "Minimum viable, not recommended"
    }
  ]
}
```

### 3. Generate New Design System

Create comprehensive design spec with migration notes.

```markdown
# Design System: [Project Name] v2.0

## Overview

This design system replaces the previous implementation with a fresh approach based on first-principles decisions.

## Migration Summary

| Aspect | Old | New | Action |
|--------|-----|-----|--------|
| Primary Color | `#3B82F6` | `#2563EB` | Update CSS variables |
| Heading Scale | Inconsistent | 36/30/24/20 | Standardize all headings |
| Button Variants | 3 inconsistent | 4 standardized | Replace all buttons |
| Spacing | Mixed | 4px base scale | Update Tailwind config |

## Brand Identity

### Color Palette

**Primary Colors:**
| Name | Old Value | New Value | Usage |
|------|-----------|-----------|-------|
| Primary | `#3B82F6` | `#2563EB` | CTAs, links |
| Primary Hover | - | `#1D4ED8` | Hover states |

**Semantic Colors:**
| Name | Value | Usage |
|------|-------|-------|
| Success | `#10B981` | Success states |
| Warning | `#F59E0B` | Warnings |
| Error | `#EF4444` | Errors |

### Typography

**Font Family:**
- Keep: Inter for UI text
- Add: JetBrains Mono for code

**Type Scale (NEW):**
| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 36px | 700 | 1.2 |
| H2 | 30px | 600 | 1.3 |
| H3 | 24px | 600 | 1.4 |
| H4 | 20px | 600 | 1.4 |
| Body | 16px | 400 | 1.6 |
| Small | 14px | 400 | 1.5 |

### Spacing Scale

Base unit: 4px

```
0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96
```

## Component Library

### Migration Path

**Components to Update:**
- Button - Standardize 4 variants
- Card - Add consistent padding
- Dialog - Update animation

**Components to Add:**
- Toast (new unified notification system)
- Skeleton (loading states)

**Components to Remove:**
- Legacy Modal (replace with Dialog)
- OldButton variants

### New Component Specs

#### Button

```typescript
variants: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive'
sizes: 'sm' | 'md' | 'lg'
states: 'default' | 'hover' | 'active' | 'disabled' | 'loading'
```

#### Toast

```typescript
variants: 'success' | 'error' | 'warning' | 'info'
position: 'top-right' | 'bottom-right' | 'top-center' | 'bottom-center'
duration: number (default: 5000ms)
```

## Accessibility

- **WCAG Level**: AA
- **Color Contrast**: 4.5:1 minimum
- **Focus States**: Visible ring on all interactive elements
- **Screen Reader**: ARIA labels required
- **Keyboard**: Full navigation support
- **Reduced Motion**: Respect prefers-reduced-motion

## Animation Patterns

| Type | Duration | Easing |
|------|----------|--------|
| Micro-interaction | 150ms | ease-out |
| Component transition | 200ms | ease-in-out |
| Page transition | 300ms | ease-in-out |
| Modal enter | 200ms | ease-out |
| Modal exit | 150ms | ease-in |

## Migration Checklist

### Phase 1: Foundation
- [ ] Update tailwind.config.ts with new colors
- [ ] Update globals.css with new CSS variables
- [ ] Update typography utilities

### Phase 2: Components
- [ ] Replace Button variants
- [ ] Update Card component
- [ ] Add new Toast component
- [ ] Remove deprecated components

### Phase 3: Pages
- [ ] Update landing page
- [ ] Update dashboard
- [ ] Update auth pages
- [ ] Update settings pages

### Phase 4: Cleanup
- [ ] Remove old CSS classes
- [ ] Remove unused variables
- [ ] Update component imports

## Deprecation Warnings

**Deprecated (remove in next sprint):**
```
- .btn-old-primary → Use <Button variant="primary">
- .card-legacy → Use <Card>
- #old-blue-color → Use var(--primary)
```

---

*Design system v2.0 - Generated with project-spec:design:overhaul*
```

### 4. Offer Migration Support

```
Design overhaul complete!

Created: DESIGN_SPEC.md with new design system

Key changes:
- Standardized color palette (5 primary, 4 semantic)
- Consistent typography scale (36/30/24/20/16/14)
- 4px spacing base with clear scale
- Updated component variants

Next steps:
1. Review migration checklist in spec
2. Update tailwind.config.ts first
3. Migrate components incrementally
4. Run frontend-design skill to implement changes
```

## Best Practices

### Audit Phase
- Be thorough - scan all style sources
- Identify both issues AND what's working
- Quantify inconsistencies (e.g., "3 different button styles")

### Interview Phase
- Encourage fresh thinking ("forget current implementation")
- Keep scope realistic
- Prioritize most impactful changes

### Migration Planning
- Break into phases
- Identify breaking changes
- Provide clear deprecation warnings
- Include cleanup tasks

## Error Handling

### No Existing Design
- Skip audit phase
- Proceed with standard design interview
- Output standard design spec

### Minimal Codebase
- Note limited audit scope
- Ask if they want full design or targeted updates

### User Wants to Keep Everything
- Suggest `/design` command instead
- Or focus on specific improvements only

## Reference Materials

Templates:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/output-template.md` (Design System section)

Related commands:
- `/project-spec:design` - Standard design spec without audit
- `/project-spec:sync design` - Sync existing design spec with code changes
