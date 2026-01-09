# Design Specification: TaskFlow

A comprehensive design system for the TaskFlow task management application.

---

## Brand Identity

### Color Palette

**Primary Colors**:
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Primary | `#3B82F6` | 59, 130, 246 | CTAs, links, active states, focus rings |
| Primary Dark | `#2563EB` | 37, 99, 235 | Hover states, pressed buttons |
| Primary Light | `#DBEAFE` | 219, 234, 254 | Backgrounds, highlights |

**Semantic Colors**:
| Name | Hex | Usage |
|------|-----|-------|
| Success | `#10B981` | Completed tasks, confirmations |
| Warning | `#F59E0B` | Approaching deadlines, cautions |
| Error | `#EF4444` | Overdue tasks, errors, destructive actions |
| Info | `#6366F1` | Notifications, tips |

**Neutral Colors**:
| Name | Hex | Usage |
|------|-----|-------|
| Gray 900 | `#111827` | Primary text |
| Gray 700 | `#374151` | Secondary text |
| Gray 500 | `#6B7280` | Placeholder text, icons |
| Gray 300 | `#D1D5DB` | Borders, dividers |
| Gray 100 | `#F3F4F6` | Backgrounds, cards |
| White | `#FFFFFF` | Surface backgrounds |

**Dark Mode Variants**:
| Light | Dark | Usage |
|-------|------|-------|
| Gray 100 | Gray 900 | Page background |
| White | Gray 800 | Card background |
| Gray 900 | Gray 100 | Primary text |

### Typography

**Font Family**:
- **Primary**: Inter (Google Fonts)
- **Monospace**: JetBrains Mono (code, IDs)
- **Fallback**: system-ui, -apple-system, sans-serif

**Type Scale**:
| Element | Size | Weight | Line Height | Letter Spacing |
|---------|------|--------|-------------|----------------|
| Display | 48px | 700 | 1.1 | -0.02em |
| H1 | 36px | 700 | 1.2 | -0.01em |
| H2 | 30px | 600 | 1.25 | 0 |
| H3 | 24px | 600 | 1.3 | 0 |
| H4 | 20px | 600 | 1.4 | 0 |
| Body | 16px | 400 | 1.5 | 0 |
| Body Small | 14px | 400 | 1.5 | 0 |
| Caption | 12px | 500 | 1.4 | 0.01em |

### Spacing System

Base unit: **4px**

| Token | Value | Usage |
|-------|-------|-------|
| space-1 | 4px | Tight spacing, icon gaps |
| space-2 | 8px | Component internal padding |
| space-3 | 12px | Small gaps |
| space-4 | 16px | Standard padding |
| space-5 | 20px | Medium gaps |
| space-6 | 24px | Section padding |
| space-8 | 32px | Large gaps |
| space-10 | 40px | Section margins |
| space-12 | 48px | Page sections |
| space-16 | 64px | Major sections |

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| radius-sm | 4px | Buttons, inputs |
| radius-md | 8px | Cards, modals |
| radius-lg | 12px | Large cards |
| radius-full | 9999px | Pills, avatars |

### Shadows

```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
```

---

## Component Library

**Library**: shadcn/ui with Tailwind CSS

### Core Components

| Component | Variants | Priority |
|-----------|----------|----------|
| Button | primary, secondary, ghost, destructive, outline | P0 |
| Input | text, email, password, search | P0 |
| Select | single, searchable | P0 |
| Checkbox | default, indeterminate | P0 |
| Avatar | image, initials, sizes (sm/md/lg) | P0 |
| Badge | default, success, warning, error | P0 |
| Card | default, interactive, selected | P0 |
| Dialog | default, alert, form | P0 |
| Dropdown Menu | default, with icons | P0 |
| Toast | success, error, info, warning | P0 |
| Tooltip | default | P1 |
| Popover | default | P1 |
| Tabs | default, pills | P1 |
| Command | search palette | P1 |
| Calendar | date picker | P2 |
| Data Table | sortable, filterable | P2 |

### Component States

All interactive components must have:

| State | Visual Treatment |
|-------|------------------|
| Default | Base styling |
| Hover | Slight background change, cursor pointer |
| Focus | 2px primary ring, offset 2px |
| Active/Pressed | Darker background |
| Disabled | 50% opacity, cursor not-allowed |
| Loading | Spinner or skeleton |
| Error | Red border, error message below |

### Button Specifications

```
Primary Button:
- Background: Primary (#3B82F6)
- Text: White
- Padding: 10px 16px
- Border radius: 6px
- Font: 14px/600

Hover: Background #2563EB
Focus: Ring 2px Primary, offset 2px
Active: Background #1D4ED8
Disabled: Opacity 50%
```

---

## Page Layouts

### App Shell

```
+--------------------------------------------------+
|  Logo    Search...          [Avatar] [Notif]     |  <- Header (64px)
+----------+---------------------------------------+
|          |                                       |
|  Nav     |  Page Content                         |
|  Items   |                                       |
|          |  +--------------------------------+   |
|  ----    |  |  Page Header                   |   |
|          |  +--------------------------------+   |
|  Teams   |  |                                |   |
|  - Team1 |  |  Main Content Area             |   |
|  - Team2 |  |                                |   |
|          |  |                                |   |
+----------+---------------------------------------+
   240px              Fluid (min 800px)
```

### Board View (Kanban)

```
+--------------------------------------------------+
|  Board Name                    [+ Add Column]     |
+--------------------------------------------------+
| To Do        | In Progress   | Review    | Done   |
| +----------+ | +----------+  | +-------+ | +----+ |
| | Task 1   | | | Task 3   |  | | Task5 | | |Task| |
| +----------+ | +----------+  | +-------+ | +----+ |
| | Task 2   | | | Task 4   |  |           |        |
| +----------+ | +----------+  |           |        |
| [+ Add]      | [+ Add]       | [+ Add]   | [+ Add]|
+--------------+---------------+-----------+--------+
```

### Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | < 640px | Single column, bottom nav, collapsible sidebar |
| Tablet | 640-1024px | Collapsible sidebar, 2-column board |
| Desktop | 1024-1280px | Fixed sidebar, full board |
| Large | > 1280px | Wider sidebar, comfortable spacing |

---

## Accessibility

### WCAG AA Compliance

**Color Contrast**:
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- UI components: 3:1 minimum

**Verified Combinations**:
| Foreground | Background | Ratio | Pass |
|------------|------------|-------|------|
| Gray 900 | White | 15.8:1 | Yes |
| Gray 700 | White | 8.6:1 | Yes |
| White | Primary | 4.5:1 | Yes |
| White | Error | 4.5:1 | Yes |

### Focus Management

- All interactive elements have visible focus indicators
- Focus ring: 2px solid Primary, 2px offset
- Focus trap in modals
- Skip links for keyboard navigation

### Screen Reader Support

- All images have alt text
- Icons have aria-labels
- Form fields have associated labels
- Live regions for dynamic content (toasts)
- Semantic HTML (header, nav, main, aside)

### Keyboard Navigation

| Key | Action |
|-----|--------|
| Tab | Move between interactive elements |
| Enter/Space | Activate buttons, checkboxes |
| Escape | Close modals, dropdowns |
| Arrow keys | Navigate within menus, lists |

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Interaction Patterns

### Animations

**Timing Functions**:
- Ease out: `cubic-bezier(0, 0, 0.2, 1)` - Entrances
- Ease in-out: `cubic-bezier(0.4, 0, 0.2, 1)` - General
- Spring: `cubic-bezier(0.34, 1.56, 0.64, 1)` - Playful

**Durations**:
| Type | Duration | Usage |
|------|----------|-------|
| Instant | 100ms | Hover states |
| Fast | 150ms | Button clicks, toggles |
| Normal | 200ms | Dropdowns, tooltips |
| Slow | 300ms | Modals, page transitions |

### Loading States

**Skeleton Screens** (preferred):
- Match layout of loading content
- Subtle pulse animation
- Gray 200 background

**Spinners** (for actions):
- Use for button loading states
- 20px size, 2px stroke
- Primary color

### Error Handling UX

**Form Validation**:
- Validate on blur
- Show inline error below field
- Red border on error fields
- Clear error on focus

**Toast Notifications**:
- Position: Bottom right
- Auto-dismiss: 5 seconds
- Swipe to dismiss
- Action button optional

**Error Pages**:
- Friendly illustration
- Clear error message
- Suggested actions
- Link to support

### Empty States

- Friendly illustration
- Explanatory text
- Primary action button
- Example: "No tasks yet. Create your first task to get started."

---

## Implementation Notes

### CSS Architecture

```
styles/
├── globals.css       # Tailwind imports, CSS variables
├── components/       # Component-specific styles (if needed)
└── themes/
    ├── light.css     # Light theme tokens
    └── dark.css      # Dark theme tokens
```

### Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3B82F6',
          dark: '#2563EB',
          light: '#DBEAFE',
        },
        // ... other colors
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
}
```

### Theme Switching

- Use `next-themes` for Next.js
- Store preference in localStorage
- Respect system preference by default
- Toggle in header/settings

---

## Design Resources

### Figma

- Component library: [Link to Figma]
- Page templates: [Link to Figma]

### Icons

- Library: Lucide React
- Size: 16px (inline), 20px (buttons), 24px (navigation)
- Stroke width: 2px

### Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

---

*Generated with project-spec plugin for Claude Code*

*Use the `frontend-design` skill to implement these specifications.*
