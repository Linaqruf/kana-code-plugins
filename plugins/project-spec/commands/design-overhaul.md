---
name: design:overhaul
version: 4.1.0
description: First-principles design system redesign - audit existing, then rebuild from scratch
argument-hint: ""
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

# Design Overhaul Command v4.1

Complete design system redesign from first principles. Audits existing design, then rebuilds with fresh decisions and provides migration guidance.

## When to Use

- Current design feels inconsistent or outdated
- Major visual rebrand needed
- Accumulated design debt from quick iterations
- Switching component libraries or design approaches

## Output

Creates `DESIGN_SPEC.md` (or `SPEC/DESIGN-SYSTEM.md`) with:
- New design system specification
- Migration notes from old to new
- Deprecation warnings for old patterns

## Workflow

### 1. Audit Current Design

**Scan existing styles:**
- `tailwind.config.*` — color tokens, theme extensions, custom utilities
- `globals.css`, `global.css`, `styles/` — CSS variables, base styles
- `src/components/ui/` — shadcn/ui pattern components
- `src/components/` — custom components
- `package.json` — component libraries (shadcn, radix, mui, chakra, etc.)

**Document findings:**
- Colors in use (extract hex values)
- Typography styles (fonts, sizes, weights)
- Spacing patterns
- Component inventory (count and list)
- Animation patterns
- Inconsistencies found (e.g., "3 different button styles", "heading sizes range from 24px to 48px")
- What works well (preserve these)

**Present audit report** to user before proceeding.

### 2. First-Principles Interview

Start fresh — ignore current implementation.

**Phase 1: Vision Reset**

```typescript
{
  question: "Forget the current design. What aesthetic do you actually want?",
  header: "Vision",
  options: [
    { label: "Modern/Clean", description: "Subtle shadows, rounded corners, professional" },
    { label: "Minimal/Sparse", description: "Typography-focused, lots of whitespace, monochrome" },
    { label: "Bold/Vibrant", description: "Strong colors, high contrast, energetic" },
    { label: "Premium/Refined", description: "Subtle, sophisticated, attention to detail" }
  ]
}
```

**Phase 2: Core Primitives**

Ask about must-have UI primitive categories (multiSelect) and component library approach.

**Phase 3: Accessibility & Motion**

Ask accessibility level (AA recommended) and animation preferences.

### 3. Generate New Design System

Create comprehensive design spec including:

- **Migration summary table**: Old value → New value → Action required
- **New color palette** with old/new comparison
- **New typography scale** standardized
- **New spacing scale**
- **Component migration path**: components to update, add, and remove
- **Accessibility requirements**
- **Animation patterns**

### 4. Generate Migration Checklist

```markdown
## Migration Checklist

### Phase 1: Foundation
- [ ] Update tailwind.config.ts with new colors
- [ ] Update globals.css with new CSS variables
- [ ] Update typography utilities

### Phase 2: Components
- [ ] [Component updates based on audit]

### Phase 3: Pages
- [ ] [Page updates]

### Phase 4: Cleanup
- [ ] Remove old CSS classes
- [ ] Remove unused variables
- [ ] Update component imports

## Deprecation Warnings
[List deprecated patterns with their replacements]
```

### 5. Finalize

Present key changes summary and suggest next steps: review checklist, update Tailwind config first, migrate components incrementally, run frontend-design skill.

## Error Handling

- **No existing design found**: Skip audit, proceed with standard design interview (suggest `/design` instead)
- **Minimal codebase**: Note limited audit scope, ask if user wants full design or targeted updates
- **User wants to keep everything**: Suggest `/design` command instead, or focus on specific fixes only
