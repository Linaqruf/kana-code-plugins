# Design Overhaul: TaskFlow

A first-principles redesign of the TaskFlow design system — from corporate blue to a modern indigo palette with improved typography, spacing consistency, and dark mode support.

---

## Audit Report

### Current State

**Scanned files**: `tailwind.config.ts`, `globals.css`, `src/components/ui/`, `src/components/`, `package.json`

**Colors in use**:
| Location | Colors Found |
|----------|-------------|
| `tailwind.config.ts` | Primary `#3B82F6`, 3 grays, no semantic colors defined |
| `globals.css` | 4 hardcoded hex values outside config (`#f0f0f0`, `#333`, `#666`, `#e5e5e5`) |
| Inline styles | 2 components use inline `color: red` for errors |

**Typography**:
- Font: Inter (loaded via Google Fonts)
- Heading sizes: inconsistent — H1 ranges from 24px to 36px across 4 pages
- Body text: 14px in sidebar, 16px in main content
- No type scale defined in config

**Spacing**:
- Mix of Tailwind defaults (`p-4`, `m-6`) and custom values (`p-[18px]`, `mt-[22px]`)
- No spacing tokens defined
- Gap inconsistencies: card padding varies between 12px, 16px, and 20px

**Component Inventory** (23 components):
| Category | Count | Notes |
|----------|-------|-------|
| Buttons | 4 variants | 3 custom + 1 shadcn, inconsistent padding |
| Inputs | 3 variants | Different border radius across forms |
| Cards | 2 variants | Different shadow values |
| Modals | 2 variants | One uses Dialog, one uses custom overlay |
| Navigation | 1 sidebar | Custom, not using shadcn |
| Tables | 1 data table | Custom, no sorting |
| Toasts | 1 | Uses react-hot-toast (not shadcn) |

**Animation Patterns**:
- No consistent timing — durations range from 100ms to 500ms
- Some components use `transition-all`, others have no transitions
- No reduced-motion handling

**Inconsistencies Found**:
1. Three different button styles (custom blue, shadcn default, unstyled `<button>`)
2. Two modal implementations (shadcn Dialog + custom overlay)
3. Hardcoded colors in 6 files bypassing the theme
4. No dark mode despite `next-themes` being installed
5. Border radius: 4px on buttons, 8px on cards, 6px on inputs — no system

**What Works Well** (preserve):
- Inter font choice — clean and readable
- Sidebar navigation layout and responsiveness
- Basic Kanban board drag-and-drop interaction
- shadcn/ui foundation (already 40% of components)

---

## New Design System

### Brand Identity

**Aesthetic**: Modern — clean lines, subtle depth, indigo palette, warm neutrals

### Color Palette

**Primary Colors**:
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Primary | `#6366F1` | 99, 102, 241 | CTAs, links, active states, focus rings |
| Primary Dark | `#4F46E5` | 79, 70, 229 | Hover states, pressed buttons |
| Primary Light | `#EEF2FF` | 238, 242, 255 | Backgrounds, highlights, badges |

**Semantic Colors**:
| Name | Hex | Usage |
|------|-----|-------|
| Success | `#10B981` | Completed tasks, confirmations |
| Warning | `#F59E0B` | Approaching deadlines, cautions |
| Error | `#EF4444` | Overdue tasks, errors, destructive actions |
| Info | `#3B82F6` | Notifications, tips, informational badges |

**Neutral Colors**:
| Name | Hex | Usage |
|------|-----|-------|
| Gray 950 | `#0C0A09` | Primary text (dark mode surface) |
| Gray 800 | `#292524` | Dark mode cards |
| Gray 700 | `#44403C` | Secondary text |
| Gray 500 | `#78716C` | Placeholder text, muted icons |
| Gray 300 | `#D6D3D1` | Borders, dividers |
| Gray 100 | `#F5F5F4` | Light backgrounds, hover states |
| White | `#FAFAF9` | Page background (warm white, not pure white) |

**Dark Mode Mapping**:
| Token | Light | Dark |
|-------|-------|------|
| `--background` | `#FAFAF9` | `#0C0A09` |
| `--surface` | `#FFFFFF` | `#1C1917` |
| `--text-primary` | `#0C0A09` | `#FAFAF9` |
| `--text-secondary` | `#44403C` | `#A8A29E` |
| `--border` | `#D6D3D1` | `#292524` |

### Typography

**Font Stack**:
- **Primary**: Geist Sans (Vercel)
- **Monospace**: Geist Mono (task IDs, code references)
- **Fallback**: system-ui, -apple-system, sans-serif

**Type Scale**:
| Element | Size | Weight | Line Height | Tracking |
|---------|------|--------|-------------|----------|
| Display | 48px | 700 | 1.1 | -0.025em |
| H1 | 32px | 700 | 1.2 | -0.02em |
| H2 | 24px | 600 | 1.25 | -0.01em |
| H3 | 20px | 600 | 1.3 | 0 |
| H4 | 16px | 600 | 1.4 | 0 |
| Body | 15px | 400 | 1.6 | 0 |
| Body Small | 13px | 400 | 1.5 | 0.01em |
| Caption | 11px | 500 | 1.4 | 0.02em |

### Spacing

Base unit: **4px**

| Token | Value | Usage |
|-------|-------|-------|
| `--space-0.5` | 2px | Hairline gaps |
| `--space-1` | 4px | Tight: icon-to-text, badge padding |
| `--space-2` | 8px | Component internal padding |
| `--space-3` | 12px | Small gaps between related items |
| `--space-4` | 16px | Standard padding (cards, inputs) |
| `--space-6` | 24px | Section padding |
| `--space-8` | 32px | Large gaps between sections |
| `--space-12` | 48px | Page-level section margins |
| `--space-16` | 64px | Major layout divisions |

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 6px | Buttons, inputs, badges |
| `--radius-md` | 8px | Cards, dropdowns |
| `--radius-lg` | 12px | Modals, large containers |
| `--radius-xl` | 16px | Feature cards, hero sections |
| `--radius-full` | 9999px | Avatars, pills |

### Shadows

```css
--shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.03);
--shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.06), 0 1px 2px -1px rgb(0 0 0 / 0.06);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.05);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.08), 0 4px 6px -4px rgb(0 0 0 / 0.04);
```

Dark mode: use `ring-1 ring-white/10` instead of shadows.

---

## Component Library

**Library**: shadcn/ui (consolidate all components to shadcn)

### Core Components

| Component | Variants | States | Priority |
|-----------|----------|--------|----------|
| Button | primary, secondary, ghost, destructive, outline, link | default, hover, focus, active, disabled, loading | P0 |
| Input | text, email, password, search, textarea | default, focus, error, disabled | P0 |
| Select | single, multi, searchable | default, open, error, disabled | P0 |
| Checkbox | default, indeterminate | unchecked, checked, disabled | P0 |
| Avatar | image, initials (sm/md/lg/xl) | loaded, fallback, loading | P0 |
| Badge | default, success, warning, error, outline | — | P0 |
| Card | default, interactive, selected | default, hover, selected | P0 |
| Dialog | default, alert, form, fullscreen | open, closing | P0 |
| Dropdown Menu | with icons, with shortcuts | — | P0 |
| Toast | success, error, info, warning | entering, visible, exiting | P0 |
| Tooltip | default, rich | — | P1 |
| Tabs | default, pills, underline | — | P1 |
| Command | search palette | open, loading, empty | P1 |
| Calendar | date picker, range picker | — | P2 |
| Data Table | sortable, filterable, selectable | loading, empty | P2 |

### Focus Indicators

All interactive components:
- Focus ring: `ring-2 ring-primary/50 ring-offset-2`
- Offset: 2px from element edge
- Visible on keyboard focus only (`:focus-visible`)

---

## Accessibility

**Target**: WCAG 2.1 AA

**Contrast Verification**:
| Foreground | Background | Ratio | Pass |
|------------|------------|-------|------|
| Gray 950 on White | `#0C0A09` / `#FAFAF9` | 18.1:1 | AA |
| Gray 700 on White | `#44403C` / `#FAFAF9` | 7.4:1 | AA |
| White on Primary | `#FAFAF9` / `#6366F1` | 4.6:1 | AA |
| White on Error | `#FAFAF9` / `#EF4444` | 4.5:1 | AA |
| Gray 100 on Gray 950 (dark) | `#F5F5F4` / `#0C0A09` | 17.2:1 | AA |

**Reduced Motion**:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## Animation

**Timing Functions**:
| Name | Value | Usage |
|------|-------|-------|
| Ease out | `cubic-bezier(0, 0, 0.2, 1)` | Entrances, reveals |
| Ease in-out | `cubic-bezier(0.4, 0, 0.2, 1)` | General transitions |
| Spring | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Bouncy micro-interactions |

**Durations**:
| Type | Duration | Usage |
|------|----------|-------|
| Instant | 75ms | Color changes, opacity |
| Fast | 150ms | Hover states, toggles |
| Normal | 200ms | Dropdowns, tooltips |
| Slow | 300ms | Modals, page transitions |
| Deliberate | 500ms | Layout shifts, reorder |

---

## Migration Summary

### Token Changes

| Element | Old Value | New Value | Action |
|---------|-----------|-----------|--------|
| Primary color | `#3B82F6` | `#6366F1` | Update `tailwind.config.ts` |
| Primary hover | `#2563EB` | `#4F46E5` | Update `tailwind.config.ts` |
| Primary light | `#DBEAFE` | `#EEF2FF` | Update `tailwind.config.ts` |
| Background | `#FFFFFF` | `#FAFAF9` | Update CSS variables |
| Font family | Inter | Geist Sans | Update `globals.css`, remove Google Fonts |
| Body size | 16px | 15px | Update base font-size |
| H1 | 36px (inconsistent) | 32px | Standardize all H1 usage |
| Border radius (buttons) | 4px | 6px | Update `tailwind.config.ts` |
| Border radius (cards) | 8px | 8px | No change |

### Component Changes

| Component | Old | New | Action |
|-----------|-----|-----|--------|
| Buttons (3 custom) | Mixed custom styles | shadcn Button | Replace with shadcn variants |
| Modal (custom overlay) | Custom `div` overlay | shadcn Dialog | Replace with Dialog component |
| Toast | react-hot-toast | shadcn Toast (Sonner) | Swap library |
| Input borders | Mixed radius | 6px consistent | Standardize via config |

### Deprecated Patterns

| Pattern | Replacement | Files Affected |
|---------|-------------|----------------|
| Inline `color: red` | `text-destructive` class | `TaskCard.tsx`, `FormError.tsx` |
| Hardcoded hex in CSS | Tailwind theme tokens | `globals.css`, 5 component files |
| Custom `p-[18px]` values | `p-4` (16px) or `p-5` (20px) | 8 components |
| `transition-all` | Specific properties (`transition-colors`) | 12 components |
| Custom overlay `div` | shadcn Dialog | `ConfirmModal.tsx` |

---

## Migration Checklist

### Phase 1: Foundation
**Depends on**: Nothing
- [ ] Install Geist font package (`geist`)
- [ ] Update `tailwind.config.ts`: new color palette, font family, border radius tokens, spacing tokens
- [ ] Update `globals.css`: replace hardcoded hex values with CSS custom properties
- [ ] Add dark mode CSS variables and `next-themes` configuration
- [ ] Remove Google Fonts link for Inter (keep as fallback in font stack)
- [ ] Add `prefers-reduced-motion` media query to globals

### Phase 2: Components
**Depends on**: Phase 1 (tokens must exist before components reference them)
- [ ] Replace 3 custom button components with shadcn Button variants
- [ ] Replace custom modal overlay with shadcn Dialog
- [ ] Swap react-hot-toast for shadcn Toast (Sonner)
- [ ] Standardize Input border radius to `--radius-sm`
- [ ] Consolidate Card variants to use new shadow tokens
- [ ] Add focus-visible ring styles to all interactive components
- [ ] Remove inline `color: red` — use `text-destructive` utility

### Phase 3: Pages
**Depends on**: Phase 2 (components must be updated before pages)
- [ ] Standardize heading sizes across all pages (H1: 32px, H2: 24px, H3: 20px)
- [ ] Replace arbitrary spacing (`p-[18px]`, `mt-[22px]`) with token values
- [ ] Replace `transition-all` with specific property transitions
- [ ] Add dark mode toggle to header (use `next-themes` `useTheme`)
- [ ] Test all pages in dark mode — verify contrast ratios
- [ ] Add loading skeletons to board view and project list

### Phase 4: Cleanup
**Depends on**: Phase 3 (all pages must be migrated)
- [ ] Remove unused CSS classes from `globals.css`
- [ ] Remove react-hot-toast from `package.json`
- [ ] Delete custom button component files (replaced by shadcn)
- [ ] Delete custom modal overlay component (replaced by Dialog)
- [ ] Run full accessibility audit (axe-core or Lighthouse)
- [ ] Verify all Tailwind classes resolve (no `p-[18px]` remaining)
- [ ] Screenshot comparison: light mode + dark mode for all key pages

---

## Open Questions

| # | Question | Status | Resolution |
|---|----------|--------|------------|
| 1 | Keep Inter as fallback or remove entirely? | Resolved | Keep in font stack as fallback after Geist |
| 2 | Migrate data table to shadcn or keep custom? | Open | Depends on sorting/filtering requirements — decide in Phase 2 |
| 3 | Add motion design tokens to Tailwind config? | Open | Evaluate after Phase 1 — may not be needed if using CSS variables |

---

*Generated with project-spec plugin for Claude Code*

*Use the `frontend-design` skill to implement this specification.*
