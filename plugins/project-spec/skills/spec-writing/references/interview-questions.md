# Interview Questions Reference

Complete question bank for project specification interviews. Select questions based on project type and user context.

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

**Core Questions:**
1. Do you have a frontend framework preference?
   - React / Next.js
   - Vue / Nuxt
   - Svelte / SvelteKit
   - Vanilla JS / HTML
   - No frontend (API only)

2. Styling approach?
   - Tailwind CSS
   - CSS Modules
   - Styled Components
   - Plain CSS
   - UI Library (shadcn, Material, etc.)

**Follow-up Questions:**
- Any experience with specific frameworks?
- State management needs? (Redux, Zustand, etc.)
- SSR/SSG requirements?

### Tech Stack - Backend

**Core Questions:**
1. Backend framework preference?
   - Node.js (Express, Fastify, Hono)
   - Python (FastAPI, Flask, Django)
   - Go (Gin, Echo)
   - Serverless functions
   - No backend (static/client-only)

2. Runtime environment?
   - Node.js
   - Deno
   - Bun
   - Python

**Follow-up Questions:**
- API style preference? (REST, GraphQL, tRPC)
- Background job requirements?
- WebSocket/real-time needs?

### Tech Stack - Database

**Core Questions:**
1. What type of data will you store?
2. Database preference?
   - PostgreSQL
   - MySQL
   - SQLite
   - MongoDB
   - Redis
   - No database needed

3. ORM/Query builder preference?
   - Prisma
   - Drizzle
   - TypeORM
   - Raw SQL

**Follow-up Questions:**
- Expected data volume?
- Complex relationships?
- Full-text search needs?
- Time-series data?

### Deployment

**Core Questions:**
1. Where will this be deployed?
   - Vercel
   - Netlify
   - AWS
   - Google Cloud
   - Self-hosted
   - Local only

2. Deployment frequency expectations?
   - Continuous deployment
   - Scheduled releases
   - Manual releases

**Follow-up Questions:**
- Domain name ready?
- SSL requirements?
- CDN needs?
- Multi-region?

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
