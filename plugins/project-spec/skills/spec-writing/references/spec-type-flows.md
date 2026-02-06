# Spec Type Flows Reference v4.0.0

Detailed workflows for feature, design, and design overhaul spec types. See SKILL.md for methodology and routing.

---

## Feature Spec Flow

### Prerequisites Check

If no SPEC.md AND no codebase detected (empty project):

```typescript
{
  question: "No project spec or existing codebase found. What would you like to do?",
  header: "Context",
  options: [
    { label: "Create a project spec first (Recommended)", description: "Run /spec to establish project context, then plan the feature" },
    { label: "Continue with standalone feature spec", description: "Proceed without project context — integration details may need manual updates later" }
  ]
}
```

### Gap Analysis

Perform when: SPEC.md exists AND no explicit feature name argument provided AND codebase has 5+ source files.

**Step 1: Extract specced features** from SPEC.md sections:
- "Core Features (MVP)" — feature names and completion status
- "Development Phases" — tasks and checkbox status
- "Future Scope" — planned features

**Step 2: Scan codebase** for implemented features using patterns from `codebase-analysis.md` § Deep Codebase Scanning. Additionally scan `src/auth/**`, `src/middleware/auth*` for authentication patterns.

**Step 3: Categorize gaps:**

1. **Specced but not implemented** — In SPEC.md but no matching code found
2. **Implemented but not specced** — Code exists but not in SPEC.md
3. **Pattern-based suggestions** — Complementary features based on what exists (e.g., "You have auth but no password reset")

**Step 4: Present findings** via AskUserQuestion with options populated from gap results. Prioritize specced-but-not-implemented first.

### Feature Interview

Group 2-3 related questions per turn:

| Phase | Questions |
|-------|-----------|
| 1. Definition | What does this feature do? What problem does it solve? Expected user interaction? |
| 2. Scope | Must-have requirements? Explicitly out of scope? Dependencies on other features? |
| 3. Technical Approach | Data storage approach? Affected components? New API endpoints? Third-party integrations? |
| 4. Edge Cases | Key edge cases? Error states? Testing approach (unit, integration, e2e)? |

→ Full question bank: `interview-questions.md` § Feature Planning Questions

### Feature Codebase Analysis

After interview, scan existing codebase for patterns:
- How similar features are structured
- Naming conventions and code organization
- API route patterns and middleware chain
- Database schema conventions

### Feature Spec Output

```markdown
# Feature: [Feature Name]

## Overview
**Description**: [One sentence]
**Problem**: [What problem this solves]
**User Story**: As a [user], I want to [action] so that [benefit]

## Requirements
### Must Have
- [ ] [Requirement with testable acceptance criteria]
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
[Schema changes with TypeScript interfaces and Zod validation]

## User Flow
[ASCII flow diagram]

## Implementation Plan
### Phase 1: Foundation
- [ ] Task 1 (depends on: nothing)
### Phase 2: Core Feature
- [ ] Task 2 (depends on: Phase 1)
### Phase 3: Polish
- [ ] Task 3 (depends on: Phase 2)

## Edge Cases
| Scenario | Expected Behavior |
|----------|-------------------|
| [Edge case] | [Specific behavior] |

## Testing Strategy
- **Unit**: [What to test]
- **Integration**: [What to test]
- **E2E**: [What to test]

## Open Questions
| Question | Options | Impact |
|----------|---------|--------|
| [Decision] | A vs B | [What changes] |
```

Output location:

| Project Structure | Output File |
|-------------------|-------------|
| Has `SPEC/` folder | `SPEC/FEATURE-[NAME].md` |
| Has `SPEC.md` only | `FEATURE_SPEC.md` |
| Neither | `FEATURE_SPEC.md` |

### Integration with feature-dev (if available)

Generated feature specs work with feature-dev agents:
1. **code-explorer** — Analyze existing patterns relevant to this feature
2. **code-architect** — Design implementation blueprint from the spec
3. **code-reviewer** — Review implementation against spec requirements

---

## Design Spec Flow

### Style Presets

If a style argument is provided, use it as starting preset and skip the aesthetic question:

| Preset | Description |
|--------|-------------|
| `modern` | Clean lines, subtle shadows, rounded corners, neutral palette |
| `minimal` | Sparse, lots of whitespace, monochrome, typography-focused |
| `bold` | Strong colors, large text, geometric shapes, high contrast |
| `custom` | Full interview for custom direction |
| Any other value | Treat as custom direction — confirm with user, run full interview |

### Existing Design Detection

Check for existing `DESIGN_SPEC.md` or `SPEC/DESIGN-SYSTEM.md`. If found, ask: update existing or start fresh.

### Design Interview

| Phase | Questions |
|-------|-----------|
| 1. Brand & Identity | Aesthetic vision (modern/minimal/bold/corporate)? Existing brand colors? Light/dark mode? |
| 2. Components & Layout | Component library (shadcn/Radix/MUI/custom)? Navigation style? Key page types? |
| 3. Accessibility & UX | Animation preferences (subtle/minimal/rich)? Accessibility level (AA recommended)? Loading state style? |

→ Full question bank: `interview-questions.md` § Design System Questions

After interview, fetch component library documentation via Context7.

### Design Spec Output

Generate a complete design spec with:
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

Output location:

| Project Structure | Output File |
|-------------------|-------------|
| Has `SPEC/` folder | `SPEC/DESIGN-SYSTEM.md` |
| Has `SPEC.md` only | `DESIGN_SPEC.md` |
| Neither | `DESIGN_SPEC.md` |

---

## Design Overhaul Flow

### When to Use

- Current design feels inconsistent or outdated
- Major visual rebrand needed
- Accumulated design debt from quick iterations
- Switching component libraries or design approaches

### Audit Workflow

**Scan existing styles:**

| Target | What to Extract |
|--------|----------------|
| `tailwind.config.*` | Color tokens, theme extensions, custom utilities |
| `globals.css`, `global.css`, `styles/` | CSS variables, base styles |
| `src/components/ui/` | shadcn/ui pattern components |
| `src/components/` | Custom components |
| `package.json` | Component libraries (shadcn, radix, mui, chakra) |

**Document findings:**
- Colors in use (extract hex values)
- Typography styles (fonts, sizes, weights)
- Spacing patterns
- Component inventory (count and list)
- Animation patterns
- Inconsistencies found (e.g., "3 different button styles", "heading sizes range from 24px to 48px")
- What works well (preserve these)

**Present audit report** to user before proceeding to interview.

### First-Principles Interview

Start fresh — ignore current implementation.

| Phase | Questions |
|-------|-----------|
| 1. Vision Reset | "Forget the current design. What aesthetic do you actually want?" (modern/minimal/bold/premium) |
| 2. Core Primitives | Must-have UI categories (multiSelect)? Component library approach? |
| 3. Accessibility & Motion | Accessibility level (AA recommended)? Animation preferences? |

### Migration Output

Include in the generated design spec:

**Migration summary table:**
```markdown
| Element | Old Value | New Value | Action |
|---------|-----------|-----------|--------|
| Primary color | #3B82F6 | #6366F1 | Update tailwind.config |
| Font | Inter | Geist | Update globals.css |
```

**Migration checklist:**
```markdown
### Phase 1: Foundation
- [ ] Update tailwind.config.ts with new colors
- [ ] Update globals.css with new CSS variables
- [ ] Update typography utilities

### Phase 2: Components
- [ ] [Component updates based on audit]

### Phase 3: Pages
- [ ] [Page-level updates]

### Phase 4: Cleanup
- [ ] Remove old CSS classes
- [ ] Remove unused variables
- [ ] Update component imports
```

**Deprecation warnings:** List deprecated patterns with their replacements.

### Edge Cases

| Scenario | Action |
|----------|--------|
| No existing design found | Ask user: run standard design spec instead, or specify design file locations manually |
| Minimal codebase (<2 style files) | Inform user of limited audit scope, proceed with available artifacts |
| User wants to keep everything | Focus on targeted fixes only |

---

*Lookup reference. For methodology, see SKILL.md.*
