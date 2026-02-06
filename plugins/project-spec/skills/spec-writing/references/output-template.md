# Project Specification Template v4.0.0

Use this template as the base structure for generating `SPEC.md`. Adapt sections based on project type — omit sections that do not apply.

See SKILL.md § Core Principle. In short: SPEC.md is always complete and self-sufficient; SPEC/ supplements are optional for reference material only.

---

```markdown
# [Project Name]

> [One-line description of what this project does]

## Overview

### Problem Statement
[1-2 sentences describing the problem this project solves]

### Solution
[1-2 sentences describing how this project solves the problem]

### Target Users
- **Primary**: [Who is the main user?]
- **Secondary**: [Any other user types?]
- **Technical Level**: [Developer / Technical User / Non-Technical]

### Success Criteria
- [ ] [Measurable outcome 1 — include quantity or threshold]
- [ ] [Measurable outcome 2 — include quantity or threshold]
- [ ] [Measurable outcome 3 — include quantity or threshold]

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: [Feature Name]
**Description**: [What does this feature do?]
**User Story**: As a [user type], I want to [action] so that [benefit].
**Acceptance Criteria**:
- [ ] [Testable criterion with specific behavior or threshold]
- [ ] [Testable criterion with specific behavior or threshold]

#### Feature 2: [Feature Name]
**Description**: [What does this feature do?]
**User Story**: As a [user type], I want to [action] so that [benefit].
**Acceptance Criteria**:
- [ ] [Testable criterion with specific behavior or threshold]
- [ ] [Testable criterion with specific behavior or threshold]

### Future Scope (Post-MVP)
1. [Future feature 1]
2. [Future feature 2]
3. [Future feature 3]

### Out of Scope
- [Explicitly not included 1]
- [Explicitly not included 2]

### User Flows

#### [Primary User Flow Name]
1. User [action 1]
2. System [response 1]
3. User [action 2]
4. System [response 2]

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale | Alternatives Considered |
|-------|------------|-----------|------------------------|
| Frontend | [Framework] | [Why chosen — specific advantage] | [Alt 1: why not], [Alt 2: why not] |
| Styling | [CSS Solution] | [Why chosen] | [Alternatives] |
| Backend | [Framework] | [Why chosen] | [Alternatives] |
| Database | [Database] | [Why chosen] | [Alternatives] |
| ORM | [ORM/Query Builder] | [Why chosen] | [Alternatives] |
| Auth | [Solution] | [Why chosen] | [Alternatives] |
| Deployment | [Platform] | [Why chosen] | [Alternatives] |

---

## System Maps

### Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Server    │────▶│  Database   │
│  (Next.js)  │◀────│   (API)     │◀────│ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
```

### Data Model Relations

```
User (1) ──────< (N) Project
Project (1) ───< (N) Task
Task (N) >─────< (N) Tag
```

### State Diagram: [Entity with Lifecycle]

```
                    ┌──────────┐
                    │ pending  │
                    └────┬─────┘
                         │ assign
                         ▼
┌──────────┐       ┌──────────┐
│ archived │◀──────│  active  │
└──────────┘       └────┬─────┘
                        │ complete
                        ▼
                   ┌──────────┐
                   │   done   │
                   └──────────┘
```

### User Flow: [Primary Flow Name]

```
[Start] → [Step 1] → [Step 2] → [Step 3] → [End State]
    ↓
[Alternative Path]
```

### Wireframe: [Key Screen] (if applicable)

```
┌────────────────────────────────┐
│  Logo              [User] [⚙] │
├────────────────────────────────┤
│ ┌────────┐  ┌─────────────────┐│
│ │  Nav   │  │                 ││
│ │        │  │   Main Content  ││
│ │ • Home │  │                 ││
│ │ • List │  │                 ││
│ │ • New  │  │                 ││
│ └────────┘  └─────────────────┘│
└────────────────────────────────┘
```

---

## Data Models

#### [Model 1 Name]
```typescript
interface ModelName {
  id: string;           // Primary key (cuid2)
  field1: string;       // Description
  field2: number;       // Description
  status: 'pending' | 'active' | 'done';  // Lifecycle state
  createdAt: Date;
  updatedAt: Date;
}
```

#### [Model 1] Validation Schema
```typescript
const createModelSchema = z.object({
  field1: z.string().min(1).max(255),
  field2: z.number().int().positive(),
});

const updateModelSchema = createModelSchema.partial();
```

#### [Model 2 Name]
```typescript
interface ModelName {
  id: string;
  field1: string;
  foreignId: string;    // Reference to [Other Model]
}
```

---

## API Endpoints

| Method | Endpoint | Description | Auth | Rate Limit |
|--------|----------|-------------|------|------------|
| GET | /api/resource | List all resources | Required | 100/min |
| GET | /api/resource/:id | Get single resource | Required | 100/min |
| POST | /api/resource | Create resource | Required | 30/min |
| PUT | /api/resource/:id | Update resource | Required | 30/min |
| DELETE | /api/resource/:id | Delete resource | Admin | 10/min |

---

## Security

### Authentication Flow

```
Client → POST /api/auth/login → Server validates credentials
    ↓
Server returns JWT (access token: 15min, refresh token: 7d)
    ↓
Client stores tokens → sends Authorization: Bearer <token>
    ↓
Server validates token on each request via middleware
```

### Input Validation
- All user input validated at API boundary using Zod schemas
- SQL injection: Parameterized queries via ORM (never raw string interpolation)
- XSS: Output encoding in React (default), CSP headers in production
- CSRF: SameSite cookie attribute + token-based protection for state-changing requests

### Sensitive Data

| Data Type | Protection |
|-----------|-----------|
| Passwords | bcrypt hash, min 12 rounds |
| API keys | SHA-256 hash, prefix-only display (sk_...xxxx) |
| Sessions | httpOnly, secure, sameSite=lax cookies |
| Secrets | Environment variables, never in source code |

### Authorization

**Strategy**: [RBAC / ABAC / Simple ownership checks]

**User Roles**:
| Role | Permissions |
|------|------------|
| Admin | Full CRUD, manage users, delete resources |
| Member | Create/edit own resources, read all |
| Viewer | Read-only access |

---

## Error Handling Strategy

### Error Response Format
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Task with id 'abc123' not found",
    "details": { "resourceType": "task", "id": "abc123" }
  }
}
```

### Error Codes

| Code | HTTP Status | When |
|------|-------------|------|
| VALIDATION_ERROR | 400 | Request body fails Zod validation |
| UNAUTHORIZED | 401 | Missing or invalid auth token |
| FORBIDDEN | 403 | Valid token but insufficient permissions |
| RESOURCE_NOT_FOUND | 404 | Entity does not exist or user has no access |
| CONFLICT | 409 | Duplicate unique field (email, slug) |
| RATE_LIMITED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Unexpected server error |

### Error Boundaries
- **API layer**: Catch-all middleware returns structured JSON errors, logs to error tracker
- **UI layer**: React error boundaries per feature section, fallback UI per boundary
- **Background jobs**: Dead letter queue after 3 retries, alert on DLQ threshold
- **Network errors**: Client-side retry with exponential backoff (max 3 attempts, base 1s)

---

## Design System

*Include for web applications and frontend projects. Omit for CLI, API, or library projects.*

### Visual Identity

**Brand Colors**:
| Name | Value | Usage |
|------|-------|-------|
| Primary | `#3B82F6` | CTAs, links, focus states |
| Secondary | `#6366F1` | Accents, highlights |
| Success | `#10B981` | Success states, confirmations |
| Warning | `#F59E0B` | Warnings, cautions |
| Error | `#EF4444` | Errors, destructive actions |
| Neutral | `#6B7280` | Text, borders, backgrounds |

**Typography**:
| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | Inter | 36px | 700 |
| H2 | Inter | 30px | 600 |
| H3 | Inter | 24px | 600 |
| Body | Inter | 16px | 400 |
| Small | Inter | 14px | 400 |
| Code | JetBrains Mono | 14px | 400 |

**Spacing Scale**: 4px base unit (4, 8, 12, 16, 24, 32, 48, 64, 96)

### Responsive Breakpoints

| Name | Width | Target |
|------|-------|--------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablet |
| lg | 1024px | Desktop |
| xl | 1280px | Large desktop |

### Component Library

**UI Components Needed**:
- [ ] Button (primary, secondary, ghost, destructive)
- [ ] Input (text, email, password, search)
- [ ] Select / Dropdown
- [ ] Modal / Dialog
- [ ] Toast / Notification
- [ ] Card
- [ ] Table
- [ ] Navigation (header, sidebar, tabs)

**Component States**: Default, Hover, Focus, Active, Disabled, Loading, Error

### Accessibility Requirements

- **WCAG Level**: AA (minimum)
- **Color contrast**: 4.5:1 for normal text, 3:1 for large text
- **Focus indicators**: Visible on all interactive elements
- **Screen reader**: ARIA labels on icons and complex components
- **Keyboard navigation**: Full tab, enter, escape support
- **Reduced motion**: Respect `prefers-reduced-motion`

---

## File Structure

```
project-name/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── (public)/        # Public routes
│   │   ├── (auth)/          # Authenticated routes
│   │   ├── api/             # API routes
│   │   └── layout.tsx       # Root layout
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   └── [feature]/       # Feature-specific components
│   ├── lib/                 # Utilities and helpers
│   ├── hooks/               # Custom React hooks
│   └── types/               # TypeScript types
├── prisma/
│   └── schema.prisma        # Database schema
├── public/                  # Static assets
├── tests/                   # Test files
├── .env.example             # Environment template
├── package.json
├── tsconfig.json
└── README.md
```

---

## Monitoring & Observability

*Include for production web applications and APIs. Omit for libraries and local-only CLIs.*

| Aspect | Tool | Purpose |
|--------|------|---------|
| Error tracking | Sentry | Capture runtime errors with context |
| Logging | Pino / Winston | Structured JSON logs with request IDs |
| Health check | `GET /health` | Return `{ status: "ok", version, uptime }` |
| Performance | Web Vitals | Track LCP, FID, CLS in production |
| Uptime | BetterUptime / UptimeRobot | Alert on downtime |

### Log Levels

| Level | When |
|-------|------|
| error | Unhandled exceptions, failed critical operations |
| warn | Deprecated usage, approaching rate limits, fallback behavior |
| info | Request/response lifecycle, business events (user created, payment processed) |
| debug | Query execution, cache hits/misses (development only) |

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | Database connection string | Yes | - |
| NEXT_PUBLIC_API_URL | Public API base URL | Yes | - |
| [OTHER_VAR] | [Description] | [Yes/No] | [Default] |

---

## Development Phases

### Phase 1: Foundation
**Depends on**: Nothing
- [ ] Project setup and configuration
- [ ] Database schema design and initial migration
- [ ] Authentication implementation
- [ ] Basic UI scaffolding

### Phase 2: Core Features
**Depends on**: Phase 1 (auth + database must exist)
- [ ] [Core feature 1]
- [ ] [Core feature 2]
- [ ] [Core feature 3]

### Phase 3: Integration & Polish
**Depends on**: Phase 2 (core features must work)
- [ ] Error handling and validation
- [ ] Loading states and UX polish
- [ ] Real-time features (if applicable)

### Phase 4: Launch
**Depends on**: Phase 3 (app must be functional)
- [ ] Testing (unit + integration)
- [ ] Deployment setup and CI/CD
- [ ] Monitoring and error tracking
- [ ] Documentation

---

## Open Questions

Decisions that need to be made during development:

| # | Question | Options | Impact | Status |
|---|----------|---------|--------|--------|
| 1 | [Question] | A) [Option], B) [Option] | [What it affects] | Open |
| 2 | [Question] | A) [Option], B) [Option] | [What it affects] | Open |
| 3 | [Question] | A) [Option], B) [Option] | [What it affects] | Open |

---

## References

(Include if SPEC/ supplements exist)

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When working with data models: `SPEC/data-models.md`
→ When using [SDK/Library]: `SPEC/sdk-patterns.md`

### External Documentation
- [Tech 1 Docs](url)
- [Tech 2 Docs](url)

---

*Generated with project-spec plugin for Claude Code*
```

---

## Template Variations

### CLI Tool Template

For CLI tools, replace frontend/design sections with:

````markdown
## Commands

### Main Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `tool init` | Initialize configuration | `--template <name>` |
| `tool run` | Run the main operation | `--input <file>` |
| `tool help` | Show help | - |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Validation errors found |
| 2 | Configuration error (missing schema, bad YAML) |
| 3 | Runtime error (file not found, permission denied) |

### Output Formats
- Text (default) — human-readable with colors
- JSON (`--format json`) — machine-readable for CI/CD
- Quiet (`--quiet`) — errors only

### Algorithm: [Non-Obvious Logic Name]

**Input**: [What goes in]
**Output**: [What comes out]

**Rules** (evaluated in order):
1. If [condition], then [result]
2. If [condition], then [result]
3. Otherwise, [default result]

**Examples**:
| Input | Output | Rule Applied |
|-------|--------|-------------|
| `"3000"` | `number` | Numeric string |
| `"true"` | `boolean` | Boolean literal |
| `"https://..."` | `url` | URL pattern match |

### Distribution
- npm package: `npm install -g tool-name`
- Binary releases: GitHub Releases
````

**Omit for CLI**: Design System, Wireframes, Responsive Breakpoints, Monitoring (unless CLI is a long-running daemon)

### API-Only Template

For pure APIs, replace frontend sections with detailed endpoint documentation:

````markdown
## API Design

### Resource: [Resource Name]

**Base URL**: `/api/v1/resource`

#### List Resources
```http
GET /api/v1/resource
Authorization: Bearer <token>

Query Parameters:
- page (int): Page number, default 1
- limit (int): Items per page, default 20, max 100
- sort (string): Sort field, default "-createdAt"

Response: 200 OK
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

#### Create Resource
```http
POST /api/v1/resource
Authorization: Bearer <token>
Content-Type: application/json

{
  "field1": "value",
  "field2": "value"
}

Response: 201 Created
{
  "data": { ... }
}
```

### Security

#### API Key Management
- Keys generated as `sk_live_` + 32 random bytes (base64)
- Stored as SHA-256 hash (original never persisted)
- Key rotation: new key generated, old key valid for 24h grace period
- Display: show only prefix `sk_live_...xxxx` (last 4 chars)

#### Rate Limiting
| Endpoint Pattern | Limit | Window |
|-----------------|-------|--------|
| `GET /api/v1/*` | 100 | 1 minute |
| `POST /api/v1/*` | 30 | 1 minute |
| `DELETE /api/v1/*` | 10 | 1 minute |
| Auth endpoints | 5 | 1 minute |

### Algorithm: [Non-Obvious Logic Name]

**Purpose**: [What this algorithm does]

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Edge cases**:
- [Edge case] → [How handled]
- [Edge case] → [How handled]
````

**Omit for API**: Design System, Wireframes, Responsive Breakpoints

### Library Template

For libraries/packages, replace deployment/server sections with:

````markdown
## Public API

### Core Functions

#### functionName(params)
**Description**: [What it does]
**Parameters**:
- `param1` (type): Description
- `param2` (type, optional): Description

**Returns**: `ReturnType` — Description

**Example**:
```typescript
import { functionName } from 'library-name';

const result = functionName(param1, param2);
```

### Types

```typescript
export interface ConfigOptions {
  option1: string;
  option2?: number;
}

export type ResultType = {
  success: boolean;
  data: unknown;
};
```

### Bundle Size Strategy
- Target: < [N]KB minified + gzipped
- Zero runtime dependencies
- Tree-shakeable exports (ESM + named exports)
- Subpath exports for optional features: `library/extra`

### Publishing

**npm**:
```bash
npm publish
```

**Version Strategy**: Semantic Versioning
- Major: Breaking API changes
- Minor: New features, backward-compatible
- Patch: Bug fixes
````

**Omit for Library**: Design System, Deployment, Auth, Monitoring, Wireframes, Security (unless library handles crypto/auth)

---

## Writing Guidelines

### Be Specific
- "Handle user data" → "Store user profiles with fields: id, email, name, avatar, createdAt"
- "Fast response times" → "API responses under 200ms at p95 for list endpoints"

### Be Testable
- "Good error handling" → "Return `{ error: { code, message, details } }` JSON with appropriate HTTP status"
- "Graceful fallback" → "If metadata fetch fails after 10s timeout, save bookmark with URL as title and empty description"

### Include Alternatives
- "Use Prisma for database" → "Use Prisma (type-safe, auto-migrations). Considered: Drizzle (lighter, SQL-like — chose Prisma for migration tooling)"

### Keep MVP Focused
- "Implement social features, notifications, chat..." → "MVP: User profiles, basic messaging. Future: Notifications, real-time chat"
