# Interview Questions Reference v4.0.0

Question bank organized by interview turns with skip conditions and AskUserQuestion format.

## Principles

1. **Lead with recommendations** — Place preferred option first with "(Recommended)" label
2. **AskUserQuestion format** — Every choice uses options parameter with 2-4 choices
3. **Smart batching** — Group 2-3 related questions per turn
4. **Skip when known** — If codebase analysis already detected the answer, pre-fill and confirm
5. **YAGNI** — Push anything non-essential to "Future Scope"

---

## Smart Batching Summary

| Turn | Questions | Skip When |
|------|-----------|-----------|
| 1 | Problem + Target User + Success Criteria | Never skip |
| 2 | MVP Features + Out of Scope | Never skip |
| 3 | Primary User Flow | CLI or library project (no interactive user flow) |
| 4 | Architecture Pattern | Project type is "library" |
| 5 | Package Manager + Frontend Framework | Skip package manager if lockfile detected. Skip frontend if CLI/API/library |
| 6 | Styling + Component Library | No frontend selected |
| 7 | Backend Framework + API Style | Skip API Style if user chose Next.js API Routes. Skip entire turn if project is a library |
| 8 | Database + ORM | User said "no database" |
| 9 | Deployment + Auth Approach | Skip auth if project has no users |
| 10 | Visual Style + Accessibility | No frontend selected |

---

## Turn 1: Vision & Problem (Never Skip)

Ask all three together in one turn:

```typescript
// Ask as grouped text questions, not multiple choice
```

**Questions:**
1. What problem does this project solve? (one sentence)
2. Who is the primary user? (developer / technical user / non-technical)
3. What does success look like? (1-3 measurable outcomes)

**Skip condition:** Never skip. Even for existing codebases, confirm the problem statement.

---

## Turn 2: Requirements (Never Skip)

**Questions:**
1. What are the 3-5 must-have features for MVP?
2. What is explicitly OUT of scope for v1?

```typescript
{
  question: "How would you describe the scope of this MVP?",
  header: "Scope",
  options: [
    { label: "Focused (Recommended)", description: "3-4 core features, ship fast, iterate" },
    { label: "Moderate", description: "5-7 features, covers main use cases" },
    { label: "Comprehensive", description: "8+ features, longer to build but more complete" }
  ]
}
```

**Skip condition:** Never skip.

---

## Turn 3: User Flow / Command Sequence

**For web apps and APIs:**
1. What is the primary user flow from start to finish?

**For CLIs:**
1. What is the primary command sequence from start to finish?

**For libraries:**
Skip entirely. Libraries have API surface documentation instead of user flows.

**Skip condition:** Skip only if project type is "library".

---

## Turn 4: Architecture

```typescript
{
  question: "What architecture pattern fits best?",
  header: "Architecture",
  options: [
    { label: "Monolith (Recommended for MVP)", description: "Single deployable unit, simpler ops, faster iteration" },
    { label: "Serverless", description: "Pay-per-use, auto-scaling, vendor lock-in risk" },
    { label: "Microservices", description: "Team scaling, complex ops — use only if team size demands it" }
  ]
}
```

**Skip condition:** Skip if project type is "library". Libraries do not have architecture patterns.

**Context-aware adaptation:**
- If solo developer → strongly recommend Monolith
- If 10+ team members → consider Microservices
- If cost-sensitive → consider Serverless

---

## Turn 5: Package Manager + Frontend

**Package Manager:**

```typescript
{
  question: "Which package manager?",
  header: "Package Manager",
  options: [
    { label: "bun (Recommended)", description: "Fastest, built-in test runner, drop-in npm replacement" },
    { label: "pnpm", description: "Fast, strict deps, great for monorepos" },
    { label: "npm", description: "Universal compatibility, no setup needed" }
  ]
}
```

**Skip condition:** Skip if lockfile detected (`bun.lockb` → bun, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm).

**Frontend Framework:**

```typescript
{
  question: "Which frontend framework?",
  header: "Frontend",
  options: [
    { label: "Next.js (Recommended)", description: "React-based, SSR/SSG, API routes, Vercel deploy" },
    { label: "Vite + React", description: "Lighter, faster dev, SPA-focused" },
    { label: "SvelteKit", description: "Great DX, smaller bundle, growing ecosystem" },
    { label: "No frontend", description: "API-only, CLI, or library project" }
  ]
}
```

**Skip condition:** Skip if project type is CLI, API, or library. Skip if `next` detected in package.json.

---

## Turn 6: Styling + Components

```typescript
{
  question: "Which styling approach?",
  header: "Styling",
  options: [
    { label: "Tailwind CSS (Recommended)", description: "Utility-first, consistent, rapid development" },
    { label: "CSS Modules", description: "Scoped CSS, no runtime cost, simple" },
    { label: "Styled Components", description: "CSS-in-JS, dynamic theming, has runtime cost" }
  ]
}
```

```typescript
{
  question: "Which component library?",
  header: "Components",
  options: [
    { label: "shadcn/ui (Recommended)", description: "Copy-paste, Tailwind-based, fully customizable" },
    { label: "Radix UI", description: "Unstyled primitives, full styling control" },
    { label: "Material UI", description: "Comprehensive, opinionated, Google design" },
    { label: "Build custom", description: "Maximum flexibility, more work" }
  ]
}
```

**Skip condition:** Skip entire turn if user chose "No frontend" in Turn 5.
**Pre-fill:** If `tailwindcss` detected in package.json, skip styling question. If `@shadcn/ui` detected, skip component question.

---

## Turn 7: Backend + API Style

```typescript
{
  question: "Which backend framework?",
  header: "Backend",
  options: [
    { label: "Hono (Recommended)", description: "Ultra-fast, edge-ready, TypeScript-first" },
    { label: "Express", description: "Mature ecosystem, well-documented, large community" },
    { label: "FastAPI (Python)", description: "Fast, auto-docs, great for Python teams" },
    { label: "Next.js API Routes", description: "Keep it simple if already using Next.js" }
  ]
}
```

**Context-aware adaptation:**
- If user chose Next.js frontend → add "Next.js API Routes" as recommended
- If user mentioned Python → recommend FastAPI
- If user mentioned edge/serverless → recommend Hono

```typescript
{
  question: "Which API style?",
  header: "API Style",
  options: [
    { label: "REST (Recommended)", description: "Simple, well-understood, cacheable" },
    { label: "tRPC", description: "End-to-end type safety, great for TypeScript monorepos" },
    { label: "GraphQL", description: "Flexible queries, higher complexity" }
  ]
}
```

**Skip condition:** Skip if user chose Next.js API Routes (implies REST). Skip if project is a library.

---

## Turn 8: Database + ORM

```typescript
{
  question: "Which database?",
  header: "Database",
  options: [
    { label: "PostgreSQL (Recommended)", description: "Reliable, feature-rich, scales well" },
    { label: "SQLite", description: "Simple, file-based, great for prototypes and CLIs" },
    { label: "MongoDB", description: "Document-based, flexible schema, good for unstructured data" },
    { label: "No database", description: "Static data, external API, or client-side only" }
  ]
}
```

```typescript
{
  question: "Which ORM?",
  header: "ORM",
  options: [
    { label: "Drizzle (Recommended)", description: "Type-safe, lightweight, SQL-like syntax" },
    { label: "Prisma", description: "Great DX, auto-migrations, heavier runtime" },
    { label: "Raw SQL", description: "Full control, no abstraction overhead" }
  ]
}
```

**Skip condition:** Skip ORM if user chose "No database". Skip if `prisma/schema.prisma` or `drizzle/` detected.
**Pre-fill:** If Prisma schema found, note "Using existing Prisma setup."

---

## Turn 9: Deployment + Auth

```typescript
{
  question: "Where will this be deployed?",
  header: "Deployment",
  options: [
    { label: "Vercel (Recommended for Next.js)", description: "Seamless deploys, preview URLs, great DX" },
    { label: "Cloudflare Pages", description: "Fast edge network, good free tier" },
    { label: "Railway / Fly.io", description: "Easy container hosting, good for backends" },
    { label: "Self-hosted / VPS", description: "Full control, more ops work" }
  ]
}
```

**Context-aware adaptation:**
- If Next.js → recommend Vercel
- If Hono/edge → recommend Cloudflare
- If Docker detected → recommend Railway/Fly.io

```typescript
{
  question: "How will users authenticate?",
  header: "Auth",
  options: [
    { label: "Email + Password (Recommended for MVP)", description: "Simple, built-in, no third-party dependency" },
    { label: "OAuth providers (Google, GitHub)", description: "Social login, less friction, requires provider setup" },
    { label: "Auth service (Clerk, Auth0)", description: "Full-featured, managed, has cost" },
    { label: "No auth needed", description: "Public-facing, no user accounts" }
  ]
}
```

**Skip condition:** Skip auth if project has no user accounts (CLI tools, public APIs, libraries).

---

## Turn 10: Design & Security

```typescript
{
  question: "What visual style?",
  header: "Style",
  options: [
    { label: "Modern/Clean (Recommended)", description: "Subtle shadows, rounded corners, professional" },
    { label: "Minimal", description: "Typography-focused, lots of whitespace" },
    { label: "Bold/Colorful", description: "Vibrant colors, high contrast, energetic" }
  ]
}
```

**Skip condition:** Skip if no frontend. Skip if user already provided design preferences.

---

## Conditional Follow-Up Questions

Ask these only when the user's earlier answers trigger them:

### Real-Time Features (if user mentioned real-time, collaboration, or live updates)

```typescript
{
  question: "How should real-time features work?",
  header: "Real-time",
  options: [
    { label: "WebSocket (Recommended)", description: "Full-duplex, low latency, good for collaboration" },
    { label: "Server-Sent Events", description: "Simpler, one-way, good for notifications" },
    { label: "Polling", description: "Simplest, higher latency, works everywhere" }
  ]
}
```

### File Storage (if user mentioned uploads, images, or documents)

```typescript
{
  question: "Where should files be stored?",
  header: "File Storage",
  options: [
    { label: "Cloudflare R2 (Recommended)", description: "S3-compatible, no egress fees, good pricing" },
    { label: "AWS S3", description: "Industry standard, mature, egress costs" },
    { label: "Local filesystem", description: "Simplest for development, not scalable" }
  ]
}
```

### Payments (if user mentioned billing, subscriptions, or commerce)

```typescript
{
  question: "Which payment provider?",
  header: "Payments",
  options: [
    { label: "Stripe (Recommended)", description: "Best DX, comprehensive, global coverage" },
    { label: "Lemon Squeezy", description: "Simpler, handles tax/compliance, Merchant of Record" },
    { label: "No payments for MVP", description: "Add later, focus on core features first" }
  ]
}
```

### Email (if user mentioned notifications, invitations, or transactional email)

```typescript
{
  question: "Which email service?",
  header: "Email",
  options: [
    { label: "Resend (Recommended)", description: "Modern API, React Email support, great DX" },
    { label: "SendGrid", description: "Mature, high volume, comprehensive" },
    { label: "Skip for MVP", description: "Console log emails in development, add service later" }
  ]
}
```

### Background Jobs (if user mentioned scheduled tasks, queues, or async processing)

```typescript
{
  question: "How should background jobs run?",
  header: "Jobs",
  options: [
    { label: "BullMQ + Redis (Recommended)", description: "Reliable queues, retries, scheduling" },
    { label: "Inngest", description: "Serverless-friendly, event-driven, managed" },
    { label: "Cron jobs", description: "Simple scheduled tasks, no queue needed" }
  ]
}
```

---

## Quick-Start Question Sets

Use these compressed flows when the user provides a project type argument:

### `/spec-writing web-app` (5 turns)
1. Problem + Users + Success Criteria
2. MVP Features + Out of Scope
3. User Flow + Architecture
4. Full Tech Stack (batch: frontend + backend + database)
5. Design Style + Auth + Deployment

### `/spec-writing cli` (4 turns)
1. Problem + Users + Success Criteria
2. Commands + Arguments + Output Formats
3. Language + Distribution + Package Manager
4. Error Handling + Testing Strategy

### `/spec-writing api` (5 turns)
1. Problem + Users + Success Criteria
2. Resources + Main Endpoints
3. Auth Method + Rate Limiting
4. Backend Framework + Database + ORM
5. Deployment + Monitoring

### `/spec-writing library` (4 turns)
1. Problem + Target Developers + Success Criteria
2. Public API Surface + Core Functions
3. Language + Build Tool + Publishing Target
4. Testing Strategy + Documentation Approach

---

## Feature Planning Questions

Use these for `/spec-writing feature` interviews:

### Turn 1: Feature Definition
1. What does this feature do? (one sentence)
2. What problem does it solve for users?

### Turn 2: Scope

```typescript
{
  question: "What is the scope of this feature?",
  header: "Scope",
  options: [
    { label: "Small (1-2 days)", description: "Single component, minor API changes" },
    { label: "Medium (3-5 days)", description: "Multiple components, new endpoints, schema changes" },
    { label: "Large (1-2 weeks)", description: "New subsystem, multiple integrations, complex logic" }
  ]
}
```

### Turn 3: Technical Approach

```typescript
{
  question: "How should this feature store data?",
  header: "Data Storage",
  options: [
    { label: "Extend existing tables", description: "Add columns/relations to current schema" },
    { label: "New dedicated tables", description: "Clean separation, more flexible" },
    { label: "No database changes", description: "Uses existing data or client-side only" }
  ]
}
```

### Turn 4: Edge Cases + Testing
1. What are the key edge cases?
2. What testing approach? (unit / integration / e2e)

---

## Design System Questions

Use these for `/spec-writing design` interviews:

### Turn 1: Aesthetic + Brand

```typescript
{
  question: "What aesthetic do you want?",
  header: "Style",
  options: [
    { label: "Modern/Clean (Recommended)", description: "Subtle shadows, rounded corners, professional" },
    { label: "Minimal", description: "Typography-focused, whitespace, monochrome" },
    { label: "Bold/Colorful", description: "Vibrant, high contrast, energetic" },
    { label: "Corporate", description: "Traditional, trustworthy, conservative" }
  ]
}
```

### Turn 2: Components + Layout

```typescript
{
  question: "Which component library?",
  header: "Components",
  options: [
    { label: "shadcn/ui (Recommended)", description: "Copy-paste, Tailwind-based, customizable" },
    { label: "Radix UI", description: "Unstyled primitives, full control" },
    { label: "Material UI", description: "Comprehensive, Google design" },
    { label: "Custom", description: "Build from scratch" }
  ]
}
```

### Turn 3: Accessibility + Motion

```typescript
{
  question: "Accessibility level?",
  header: "Accessibility",
  options: [
    { label: "WCAG AA (Recommended)", description: "Standard compliance, 4.5:1 contrast" },
    { label: "WCAG AAA", description: "Strict compliance, 7:1 contrast" },
    { label: "Basic", description: "Keyboard nav and screen reader basics only" }
  ]
}
```

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
