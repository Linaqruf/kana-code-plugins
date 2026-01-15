# Deep Interview Questions Reference

Extended question bank for SPEC/ and DEEP modes. Use for comprehensive project specifications.

## Interview Modes

| Mode | Questions | Turns | Style |
|------|-----------|-------|-------|
| **Quick** | ~15 | ~6-8 | Grouped (3-4 per turn) |
| **SPEC/** | ~40 | ~15 | Grouped (2-4 per turn) + multiple choice |
| **DEEP** | ~50 | ~50-60 | One question at a time (Socratic) |

---

## Phase 1: Vision & Problem (5-6 questions)

### Core Questions

1. **Problem Statement**
   - What specific problem does this project solve?
   - Options for context: "User frustration with X", "Missing tool for Y", "Inefficiency in Z"

2. **Value Proposition**
   - What is the core value in one sentence?
   - Why does this need to exist? What gap does it fill?

3. **Current Solutions**
   - How is this problem currently being solved?
   - What makes your approach different/better?

4. **Success Criteria**
   - What does success look like 6 months after launch?
   - Key metrics to track?

### Follow-up Questions (DEEP mode)

5. What happens if this project doesn't get built?
6. Is this a vitamin (nice-to-have) or painkiller (must-have)?

### AskUserQuestion Format

```typescript
{
  question: "What problem does this project solve?",
  header: "Problem",
  options: [
    { label: "User frustration", description: "Existing tools are frustrating or hard to use" },
    { label: "Missing functionality", description: "No tool exists for this specific need" },
    { label: "Efficiency gap", description: "Current solutions are slow or manual" },
    { label: "Cost reduction", description: "Existing solutions are too expensive" }
  ],
  multiSelect: false
}
```

---

## Phase 2: Requirements & Users (6-8 questions)

### Core Questions

1. **Primary User**
   - Who is the primary user of this project?
   - Technical level? (Developer, Technical user, Non-technical, Mixed)

2. **User Personas** (SPEC/DEEP only)
   - Describe 2-3 user personas
   - What are their goals and pain points?

3. **MVP Features**
   - What are the 3-5 must-have features for launch?
   - What is the single most critical feature?

4. **MoSCoW Prioritization**
   - Must have (MVP blockers)?
   - Should have (important but not blocking)?
   - Could have (nice to have)?
   - Won't have (explicitly out of scope)?

5. **User Stories** (SPEC/DEEP only)
   - As a [user], I want to [action], so that [benefit]
   - Provide 3-5 key user stories

### Follow-up Questions (DEEP mode)

6. What features would you cut if pressed for time?
7. What features seem simple but are actually complex?
8. What features do users expect based on similar products?

### AskUserQuestion Format

```typescript
{
  question: "What is the technical level of your primary user?",
  header: "User Tech",
  options: [
    { label: "Developer", description: "Comfortable with CLI, APIs, code" },
    { label: "Technical user", description: "Power user, some scripting" },
    { label: "Non-technical", description: "Expects GUI, simple UX" },
    { label: "Mixed audience", description: "Both technical and non-technical" }
  ],
  multiSelect: false
}
```

---

## Phase 3: Architecture & Scale (6-8 questions)

### Core Questions

1. **System Type**
   - What type of system is this?
   - Options: Web app, CLI tool, API service, Library, Desktop app, Mobile app, Hybrid

2. **Architecture Pattern**
   - Monolith vs microservices?
   - Serverless vs traditional servers?

3. **Data Flow**
   - What is the main data flow? (User → Frontend → API → DB)
   - Real-time requirements?

4. **Scale Expectations**
   - Expected user volume?
   - Options: Personal (1-10), Team (10-100), Production (100-10K), Large (10K+)

5. **Integration Points**
   - External services to integrate?
   - Third-party APIs?

### Follow-up Questions (DEEP mode)

6. Caching strategy needed?
7. CDN requirements?
8. Multi-region deployment?

### Present 2-3 Alternatives

For architecture decisions, always present options:

```markdown
**Architecture Options:**

1. **Monolith (Recommended for MVP)**
   - Pros: Simple, fast to build, easy to deploy
   - Cons: Harder to scale specific parts
   - Best for: Small teams, early-stage products

2. **Serverless**
   - Pros: Auto-scaling, pay-per-use, no server management
   - Cons: Cold starts, vendor lock-in, harder debugging
   - Best for: Variable traffic, event-driven workloads

3. **Microservices**
   - Pros: Independent scaling, team autonomy
   - Cons: Complex, requires DevOps maturity
   - Best for: Large teams, high-scale production
```

---

## Phase 4: Frontend (4-6 questions)

*Skip if project has no frontend*

### Core Questions

1. **Framework**
   - Frontend framework preference?
   - Options: Next.js, React, Vue/Nuxt, Svelte/SvelteKit, Vanilla JS, None

2. **Styling**
   - Styling approach?
   - Options: Tailwind CSS, CSS Modules, Styled Components, Plain CSS, UI Library

3. **State Management**
   - State management needs?
   - Options: React Context, Zustand, Redux, Jotai, None

4. **Routing**
   - SSR, SSG, or SPA?
   - App Router vs Pages Router (Next.js)?

### Follow-up Questions (DEEP mode)

5. Component library preference? (shadcn, Radix, MUI, custom)
6. Animation requirements? (Framer Motion, CSS transitions, none)

---

## Phase 5: Backend (4-6 questions)

*Skip if project has no backend*

### Core Questions

1. **Framework**
   - Backend framework preference?
   - Options: Node.js (Express/Fastify/Hono), Python (FastAPI/Django), Go, Serverless, None

2. **Runtime**
   - Runtime environment?
   - Options: Node.js, Deno, Bun, Python, Go

3. **API Style**
   - API style preference?
   - Options: REST, GraphQL, tRPC, gRPC

4. **Database**
   - Database preference?
   - Options: PostgreSQL, MySQL, SQLite, MongoDB, Redis, None

5. **ORM**
   - ORM preference?
   - Options: Prisma, Drizzle, TypeORM, Sequelize, Raw SQL

### Follow-up Questions (DEEP mode)

6. Background job requirements?
7. WebSocket/real-time needs?
8. Message queue needs? (Redis, RabbitMQ, SQS)

---

## Phase 6: Security (4-5 questions)

### Core Questions

1. **Authentication**
   - Authentication approach?
   - Options: Built-in auth, OAuth (Google/GitHub), Auth service (Clerk/Auth0), None

2. **Authorization**
   - Role-based access control needed?
   - Options: Simple (user/admin), Role-based (RBAC), Attribute-based (ABAC), None

3. **Sensitive Data**
   - What sensitive data will be handled?
   - Options: User credentials, Personal info (PII), Payment data, None

4. **Compliance**
   - Compliance requirements?
   - Options: None, GDPR, HIPAA, SOC2, PCI-DSS

### Follow-up Questions (DEEP mode)

5. Audit logging needed?
6. Rate limiting strategy?
7. Input validation approach?

---

## Phase 7: Design & UX (4-6 questions)

*Skip if no UI*

### Core Questions

1. **Brand**
   - Existing brand guidelines?
   - Options: Yes (provide), No (create new), Use preset theme

2. **Theme**
   - Overall aesthetic?
   - Options: Minimal/Clean, Bold/Colorful, Professional, Playful, Dark mode default

3. **Layout**
   - Primary device target?
   - Options: Desktop-first, Mobile-first, Equal priority

4. **Components**
   - Component library?
   - Options: shadcn/ui, Radix UI, MUI, Chakra UI, Custom

### Follow-up Questions (DEEP mode)

5. Icon library preference?
6. Typography preference? (System fonts, Google Fonts, Custom)
7. Accessibility level? (WCAG AA, WCAG AAA, Basic)

---

## Phase 8: Process & Workflow (3-4 questions)

### Core Questions

1. **Team**
   - Solo developer or team?
   - If team: size and skill levels?

2. **Phases**
   - How should development be broken into phases?
   - Suggested: Foundation → Core Features → Polish → Launch

3. **Testing**
   - Testing strategy?
   - Options: Unit tests, Integration tests, E2E tests, Manual only

4. **CI/CD**
   - Deployment approach?
   - Options: Continuous deployment, Scheduled releases, Manual

### Follow-up Questions (DEEP mode)

5. Code review process?
6. Branch strategy? (trunk-based, GitFlow, feature branches)
7. TDD approach? (test-first, test-after, no tests)

---

## Validation Checkpoints

### SPEC/ Mode (4-5 checkpoints)

1. **After 00-04**: Vision, Architecture, Frontend, Backend, Security
   - "I've drafted the core architecture. Does this look right?"

2. **After 05-10**: Design, Components, UI, API, CLI, Models
   - "Technical design complete. Any adjustments?"

3. **After 11-17**: Config, Troubleshooting, Phases, Roadmap, Status, Analysis
   - "Process documentation ready. Final review?"

4. **After CLAUDE.md**: Generated CLAUDE.md with reflective behavior
   - "CLAUDE.md generated. Confirm and finalize?"

### DEEP Mode (Per-file validation)

After generating each file, ask:
- "I've created [filename]. Does this capture your intent?"
- Wait for confirmation before proceeding to next file

---

## Context7 Integration

After tech choices are made, query Context7 for documentation:

```markdown
For Next.js + Prisma + PostgreSQL:
1. resolve-library-id: "next.js app router authentication"
2. query-docs: "Next.js app router setup with server components"
3. resolve-library-id: "prisma postgresql"
4. query-docs: "Prisma schema best practices PostgreSQL"
```

Include relevant insights in:
- `01-ARCHITECTURE.md` - Framework patterns
- `02-FRONTEND.md` - Component patterns
- `03-BACKEND.md` - API patterns
- `10-DATA-MODELS.md` - Schema patterns

---

## Quick Reference: Question Count by Mode

| Phase | Quick | SPEC/ | DEEP |
|-------|-------|-------|------|
| 1. Vision | 3 | 5 | 6 |
| 2. Requirements | 3 | 6 | 8 |
| 3. Architecture | 2 | 6 | 8 |
| 4. Frontend | 2 | 4 | 6 |
| 5. Backend | 2 | 4 | 6 |
| 6. Security | 2 | 4 | 5 |
| 7. Design | 2 | 4 | 6 |
| 8. Process | 2 | 3 | 4 |
| **Total** | **~18** | **~36** | **~49** |
