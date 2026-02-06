# Frontend Template

> Frontend architecture and implementation. Create if project has UI.

```markdown
## Frontend

> UI implementation for [Project Name]

## Framework

| Aspect | Choice |
|--------|--------|
| **Framework** | [React/Vue/Svelte/etc.] |
| **Meta-framework** | [Next.js/Nuxt/SvelteKit/none] |
| **Rendering** | [SSR/SSG/SPA/Hybrid] |

## Directory Structure

```
src/
├── app/              # Pages/routes
├── components/       # UI components
├── hooks/            # Custom hooks
├── store/            # State management
├── lib/              # Utilities
└── types/            # TypeScript types
```

## State Management

| Store | Purpose | Library |
|-------|---------|---------|
| [Name] | [Purpose] | [Zustand/Redux/etc.] |

## Routing

| Route | Page | Purpose |
|-------|------|---------|
| `/` | Home | [Purpose] |
| `/[route]` | [Page] | [Purpose] |

## Styling

| Aspect | Choice |
|--------|--------|
| **Approach** | [Tailwind/CSS Modules/etc.] |
| **Components** | [shadcn/Radix/etc.] |

## Patterns

### Component Structure

```typescript
interface Props {
  // Props
}

export function Component({ prop }: Props) {
  // Implementation
}
```

### Naming

- Components: `PascalCase.tsx`
- Hooks: `useCamelCase.ts`
- Stores: `camelCaseStore.ts`

---

*Related: Design System, Architecture*
```

## When to Create

- Project has web UI
- Project has mobile app
- Project has desktop app with UI
