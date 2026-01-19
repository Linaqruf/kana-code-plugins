# Interview Questions Reference v3.0

Complete question bank for project specification interviews with opinionated recommendations.

## Core Principles

1. **Lead with recommendations** - Always show preferred option first with rationale
2. **Multiple choice** - Use AskUserQuestion options, not open-ended text
3. **2-3 alternatives** - For key decisions, present options with tradeoffs
4. **YAGNI** - Ruthlessly simplify, question necessity

## Opinionated Recommendations

When presenting options, use this format:

```typescript
{
  question: "Which [choice]?",
  header: "[Category]",
  options: [
    {
      label: "[Choice] (Recommended)",
      description: "[Why this is preferred]"
    },
    {
      label: "[Alternative 1]",
      description: "[Tradeoffs]"
    },
    {
      label: "[Alternative 2]",
      description: "[Tradeoffs]"
    }
  ]
}
```

---

## Product Requirements Questions

### Problem & Purpose

**Core Questions:**
1. What problem does this project solve?
2. What is the core value proposition in one sentence?
3. Why does this need to exist? What gap does it fill?

**Follow-up Questions:**
- How is this problem currently being solved?
- What makes your approach different/better?
- What happens if this project doesn't get built?

### Target Users

**Core Questions:**
1. Who is the primary user of this project?
2. What is their technical level? (developer, technical user, non-technical)
3. How will they discover and access this project?

**Follow-up Questions:**
- Are there secondary user types?
- What is the expected user volume?
- Any accessibility requirements?

### Core Features (MVP)

**Core Questions:**
1. What are the 3-5 must-have features for launch?
2. What is the single most important feature?
3. What does "done" look like for MVP?

**Follow-up Questions:**
- What features would you cut if pressed for time?
- Are there features that seem simple but are actually complex?
- What features do users expect based on similar products?

### Future Scope

**Core Questions:**
1. What features are explicitly out of scope for now?
2. What would version 2.0 include?
3. Any features you're uncertain about including?

**Follow-up Questions:**
- What features might become necessary based on user feedback?
- Are there monetization features planned?
- Integration features for later?

### Inspirations & References

**Core Questions:**
1. Any existing products or projects that inspired this?
2. What do you like about those products?
3. What would you do differently?

**Follow-up Questions:**
- Any design or UX references?
- Open source projects to study?
- Anti-patterns to avoid?

---

## Technical Design Questions

### Tech Stack - Frontend

**Recommended Options:**

```typescript
// Framework
{
  question: "Which frontend framework?",
  header: "Frontend",
  options: [
    {
      label: "Next.js (Recommended)",
      description: "React-based, SSR/SSG, API routes, Vercel deploy"
    },
    {
      label: "Vite + React",
      description: "Lighter, faster dev, more control, SPA-focused"
    },
    {
      label: "SvelteKit",
      description: "Great DX, smaller bundle, growing ecosystem"
    },
    {
      label: "No frontend (API only)",
      description: "Backend/CLI project, no UI needed"
    }
  ]
}

// Styling
{
  question: "Which styling approach?",
  header: "Styling",
  options: [
    {
      label: "Tailwind CSS (Recommended)",
      description: "Utility-first, consistent, rapid development"
    },
    {
      label: "CSS Modules",
      description: "Scoped CSS, no runtime, simple"
    },
    {
      label: "Styled Components",
      description: "CSS-in-JS, dynamic theming, runtime cost"
    }
  ]
}

// Component Library
{
  question: "Which component library?",
  header: "Components",
  options: [
    {
      label: "shadcn/ui (Recommended)",
      description: "Copy-paste, Tailwind-based, fully customizable"
    },
    {
      label: "Radix UI",
      description: "Unstyled primitives, full styling control"
    },
    {
      label: "Material UI",
      description: "Comprehensive, opinionated, Google design"
    },
    {
      label: "Build custom",
      description: "Maximum flexibility, more work"
    }
  ]
}
```

**Follow-up Questions:**
- State management needs? (Zustand recommended over Redux)
- SSR/SSG requirements?

### Tech Stack - Backend

**Recommended Options:**

```typescript
// Package Manager (ask first)
{
  question: "Which package manager?",
  header: "Package Manager",
  options: [
    {
      label: "bun (Recommended)",
      description: "Fastest, built-in test runner, drop-in npm replacement"
    },
    {
      label: "pnpm",
      description: "Fast, strict deps, great for monorepos"
    },
    {
      label: "npm",
      description: "Universal compatibility, no setup needed"
    }
  ]
}

// Framework
{
  question: "Which backend framework?",
  header: "Backend",
  options: [
    {
      label: "Hono (Recommended)",
      description: "Ultra-fast, edge-ready, TypeScript-first"
    },
    {
      label: "Express",
      description: "Mature, huge ecosystem, well-documented"
    },
    {
      label: "FastAPI (Python)",
      description: "Fast, auto-docs, Python ecosystem"
    },
    {
      label: "Next.js API Routes",
      description: "If already using Next.js, keep it simple"
    }
  ]
}

// API Style
{
  question: "Which API style?",
  header: "API",
  options: [
    {
      label: "REST (Recommended)",
      description: "Simple, well-understood, cacheable"
    },
    {
      label: "tRPC",
      description: "End-to-end type safety, great for TypeScript"
    },
    {
      label: "GraphQL",
      description: "Flexible queries, complex but powerful"
    }
  ]
}
```

**Follow-up Questions:**
- Background job requirements? (BullMQ recommended)
- WebSocket/real-time needs?

### Tech Stack - Database

**Recommended Options:**

```typescript
// Database
{
  question: "Which database?",
  header: "Database",
  options: [
    {
      label: "PostgreSQL (Recommended)",
      description: "Reliable, feature-rich, scales well"
    },
    {
      label: "SQLite",
      description: "Simple, file-based, great for prototypes"
    },
    {
      label: "MongoDB",
      description: "Document-based, flexible schema"
    },
    {
      label: "No database",
      description: "Static data or external API only"
    }
  ]
}

// ORM
{
  question: "Which ORM/query builder?",
  header: "ORM",
  options: [
    {
      label: "Drizzle (Recommended)",
      description: "Type-safe, lightweight, SQL-like syntax"
    },
    {
      label: "Prisma",
      description: "Great DX, auto-migrations, heavier"
    },
    {
      label: "Raw SQL",
      description: "Full control, no abstraction overhead"
    }
  ]
}
```

**Follow-up Questions:**
- Expected data volume?
- Full-text search needs? (Consider Meilisearch)
- Caching needs? (Consider Redis)

### Deployment

**Recommended Options:**

```typescript
{
  question: "Where will this be deployed?",
  header: "Deployment",
  options: [
    {
      label: "Vercel (Recommended for Next.js)",
      description: "Seamless, auto-preview, great DX"
    },
    {
      label: "Cloudflare Pages",
      description: "Fast edge network, good free tier"
    },
    {
      label: "Railway / Fly.io",
      description: "Easy backend hosting, containers"
    },
    {
      label: "Self-hosted / VPS",
      description: "Full control, more ops work"
    }
  ]
}
```

**Follow-up Questions:**
- Domain name ready?
- CI/CD preferences? (GitHub Actions recommended)
- Multi-region needs?

### Integrations

**Core Questions:**
1. What third-party services are needed?
   - Payment processing (Stripe, etc.)
   - Email service (SendGrid, Resend, etc.)
   - File storage (S3, Cloudflare R2, etc.)
   - Analytics

2. External APIs to integrate?
3. Authentication provider?
   - Built-in auth
   - OAuth providers (Google, GitHub, etc.)
   - Auth service (Auth0, Clerk, etc.)

**Follow-up Questions:**
- Webhook requirements?
- Rate limiting concerns?
- API key management?

### Performance & Scale

**Core Questions:**
1. Expected user volume?
   - Personal project (1-10 users)
   - Small team (10-100)
   - Production app (100-10,000)
   - Large scale (10,000+)

2. Performance requirements?
   - Response time expectations
   - Concurrent user handling
   - Data processing volume

**Follow-up Questions:**
- Caching strategy needed?
- CDN for assets?
- Database scaling plan?

### Security

**Core Questions:**
1. What sensitive data will be handled?
   - User credentials
   - Personal information
   - Payment data
   - None

2. Security requirements?
   - Authentication
   - Authorization/roles
   - Data encryption
   - Audit logging

**Follow-up Questions:**
- Compliance requirements? (GDPR, HIPAA, SOC2)
- Penetration testing plans?
- Security review process?

---

## Constraint Questions

### Team & Timeline

**Core Questions:**
1. Solo developer or team?
2. Any deadline or milestone expectations?
3. Time commitment available?

**Follow-up Questions:**
- Team skill levels?
- Communication tools?
- Code review process?

### Existing Codebase

**Core Questions:**
1. Starting fresh or integrating with existing code?
2. Any legacy systems to consider?
3. Existing design system or components?

**Follow-up Questions:**
- Migration requirements?
- Backwards compatibility?
- Deprecation concerns?

### Budget & Resources

**Core Questions:**
1. Budget for paid services?
   - Free tier only
   - Limited budget
   - No constraints

2. Hosting budget expectations?
3. Third-party service costs acceptable?

**Follow-up Questions:**
- Open source preference?
- Self-hosted vs managed services?
- Support requirements?

---

## Quick-Start Question Sets

### Web Application (Minimal)
1. What does this app do? (1 sentence)
2. Who uses it?
3. Top 3 features?
4. Tech stack preference? (suggest: Next.js + Tailwind + Prisma)
5. Where will it be deployed?

### CLI Tool (Minimal)
1. What does this tool do?
2. Main commands/subcommands?
3. Input/output formats?
4. Language preference? (suggest: Node.js or Python)
5. Distribution method? (npm, pip, binary)

### REST API (Minimal)
1. What data/resources does this API manage?
2. Main endpoints needed?
3. Authentication method?
4. Framework preference? (suggest: FastAPI or Express)
5. Database needs?

### Library (Minimal)
1. What functionality does this library provide?
2. Who is the target developer?
3. Public API surface?
4. Language/ecosystem?
5. Publishing target? (npm, PyPI, crates.io)

---

## AskUserQuestion Formatting Tips

### Effective Question Grouping

**Good: 2-4 related questions**
```
Questions about your project's core functionality:
1. What problem does this solve?
2. Who is the primary user?
3. What are the top 3 must-have features?
```

**Bad: Too many unrelated questions**
```
Questions:
1. What's the problem?
2. Database preference?
3. Deployment target?
4. Team size?
5. Budget?
6. Timeline?
```

### Providing Options

When asking about tech choices, provide clear options:
```
What frontend framework would you like to use?
- Next.js (React, recommended for most web apps)
- SvelteKit (Svelte, great DX, smaller bundle)
- Nuxt (Vue, good for Vue developers)
- None (API-only or static HTML)
```

### Handling Uncertainty

When user is unsure, provide recommendations:
```
Since you're building a full-stack web app and are open to suggestions,
I recommend:
- Next.js for the frontend (popular, great ecosystem)
- Prisma + PostgreSQL for data (type-safe, reliable)
- Tailwind CSS for styling (rapid development)
- Vercel for deployment (seamless Next.js hosting)

Does this sound good, or would you like alternatives?
```

---

## Design & UX Questions

### Visual Design

**Core Questions:**
1. Do you have existing brand guidelines or colors?
   - Yes, existing brand
   - No, need to create
   - Use a preset theme (shadcn, etc.)

2. Typography preferences?
   - System fonts (fast loading)
   - Google Fonts (Inter, Roboto, etc.)
   - Custom/brand fonts

3. Overall aesthetic?
   - Minimal / Clean
   - Bold / Colorful
   - Professional / Corporate
   - Playful / Friendly

**Follow-up Questions:**
- Any color palette preferences?
- Light mode, dark mode, or both?
- Reference sites for design inspiration?

### Component Library

**Core Questions:**
1. Component library preference?
   - shadcn/ui (Recommended, customizable)
   - Radix UI (Unstyled primitives)
   - Material UI (Google design)
   - Chakra UI (Accessible)
   - Build custom components

2. Icon library?
   - Lucide Icons (Recommended)
   - Heroicons
   - Phosphor Icons
   - Custom icons

**Follow-up Questions:**
- Need charts/data visualization?
- Complex table requirements?
- Form builder needs?

### Layout & Responsiveness

**Core Questions:**
1. Primary device target?
   - Desktop-first
   - Mobile-first
   - Equal priority

2. Key page layouts needed?
   - Landing / Marketing
   - Dashboard / App shell
   - Auth pages
   - Settings / Profile
   - Content / Blog

**Follow-up Questions:**
- Sidebar navigation or top nav?
- Multi-column layouts?
- Full-width or contained?

### Accessibility

**Core Questions:**
1. Accessibility requirements?
   - WCAG AA (Standard)
   - WCAG AAA (Strict)
   - Basic accessibility

2. Specific accessibility needs?
   - Screen reader support
   - Keyboard navigation
   - High contrast mode
   - Reduced motion

### User Experience

**Core Questions:**
1. Loading state preferences?
   - Skeleton screens
   - Spinners
   - Progress bars

2. Error handling UX?
   - Inline validation
   - Toast notifications
   - Modal dialogs

3. Animation preferences?
   - Minimal (performance)
   - Subtle transitions
   - Rich animations

**Follow-up Questions:**
- Onboarding flow needed?
- Empty states design?
- Confirmation dialogs?

---

## Quick-Start Design Sets

### Modern SaaS
```
- shadcn/ui components
- Inter font
- Tailwind CSS
- Lucide icons
- Dark mode support
- Skeleton loaders
```

### Marketing Site
```
- Custom components
- Brand fonts
- Bold colors
- Hero sections
- Animation-rich
- Mobile-first
```

### Dashboard App
```
- shadcn/ui + charts
- System fonts
- Sidebar navigation
- Data tables
- Toast notifications
- Desktop-first
```

### MVP / Prototype
```
- shadcn/ui defaults
- System fonts
- Minimal styling
- Basic layouts
- Skip animations
- Focus on function
```

---

## Feature Planning Questions

Use these questions when planning a new feature for an existing project.

### Feature Definition

**Core Questions:**
1. What does this feature do in one sentence?
2. What problem does it solve for users?
3. How will users interact with this feature?

**Follow-up Questions:**
- What triggers this feature? (user action, system event, scheduled)
- Is this a user-facing feature or internal tooling?
- What is the expected frequency of use?

### Scope & Requirements

**Core Questions:**
1. What are the must-have requirements (MVP)?
2. What is explicitly out of scope for this iteration?
3. Are there dependencies on other features or systems?

**Follow-up Questions:**
- What would make this feature "done"?
- Are there any hard constraints (performance, compatibility)?
- What happens if this feature fails?

### Technical Approach

**Core Questions:**
1. Which existing patterns/components should this follow?
2. Does this require new API endpoints?
3. Does this require database schema changes?
4. Any third-party integrations needed?

**Follow-up Questions:**
- Can this be built incrementally or is it all-or-nothing?
- Are there feature flags or gradual rollout needs?
- What existing code can be reused?

### User Experience

**Core Questions:**
1. What is the primary user flow?
2. What feedback should users receive?
3. How should errors be presented?

**Follow-up Questions:**
- Loading states needed?
- Empty states to design?
- Confirmation dialogs required?

### Edge Cases & Error Handling

**Core Questions:**
1. What are the key edge cases?
2. What happens with invalid input?
3. What if external services are unavailable?

**Follow-up Questions:**
- Rate limiting considerations?
- Concurrent access handling?
- Data validation requirements?

### Testing Strategy

**Core Questions:**
1. What are the critical paths to test?
2. What edge cases need test coverage?
3. Any integration tests needed?

**Follow-up Questions:**
- Performance benchmarks needed?
- Accessibility testing requirements?
- Cross-browser/device testing?

---

## Quick-Start Feature Sets

### CRUD Feature
```
1. What resource is being managed?
2. Who can create/read/update/delete?
3. What fields are required vs optional?
4. Any validation rules?
5. Soft delete or hard delete?
```

### Integration Feature
```
1. What external service are we integrating?
2. Authentication method? (API key, OAuth)
3. What data flows in/out?
4. Rate limits or quotas?
5. Fallback if service is unavailable?
```

### User-Facing Feature
```
1. Where does this appear in the UI?
2. What user action triggers it?
3. What feedback does the user see?
4. Mobile considerations?
5. Accessibility requirements?
```

### Background Job Feature
```
1. What triggers the job? (schedule, event, manual)
2. How long does it typically run?
3. What happens on failure?
4. Retry strategy?
5. Monitoring/alerting needs?
```

### Auth/Permission Feature
```
1. What resource is being protected?
2. What roles/permissions are involved?
3. How is authorization checked?
4. Audit logging needed?
5. Session/token considerations?
```
