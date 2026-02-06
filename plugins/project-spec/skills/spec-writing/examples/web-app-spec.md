# Project Specification: TaskFlow

> Collaborative task management for small teams with real-time updates and kanban boards.

## Overview

### Problem Statement
Teams struggle to track tasks across multiple projects, leading to missed deadlines and unclear accountability.

### Solution
TaskFlow is a collaborative task management web application that provides clear project organization, real-time updates, and team visibility through kanban boards.

### Target Users
- **Primary**: Small to medium teams (5-50 people)
- **Secondary**: Project managers, team leads
- **Technical Level**: Non-technical to technical users

### Success Criteria
- [ ] Users can create, assign, and complete tasks in under 3 clicks
- [ ] Board updates appear for all viewers within 2 seconds of a change
- [ ] Projects support at least 3 custom columns and 500 tasks without performance degradation

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: User Authentication
**Description**: Secure sign-up and login with email or OAuth providers.
**User Story**: As a user, I want to create an account so that I can access my tasks from any device.
**Acceptance Criteria**:
- [ ] Email/password registration with validation (min 8 chars, 1 uppercase, 1 number)
- [ ] Google OAuth sign-in option
- [ ] Password reset via email (link valid for 1 hour)
- [ ] Session persists across browser refreshes for 7 days

#### Feature 2: Project Management
**Description**: Create and organize projects to group related tasks.
**User Story**: As a team lead, I want to create projects so that I can organize tasks by initiative.
**Acceptance Criteria**:
- [ ] Create, edit, delete projects (soft delete, restorable for 30 days)
- [ ] Invite team members by email
- [ ] Project-level permissions: admin (full control), member (create/edit tasks), viewer (read-only)

#### Feature 3: Task Board
**Description**: Kanban-style board for visualizing task progress.
**User Story**: As a user, I want to drag tasks between columns so that I can update their status quickly.
**Acceptance Criteria**:
- [ ] Create up to 10 custom columns per project
- [ ] Drag-and-drop task movement between columns (reorder within column)
- [ ] Task fields: title (required, max 255 chars), description (markdown, max 10,000 chars), assignee, due date, priority (low/medium/high/urgent)
- [ ] Board syncs across all viewers within 2 seconds via WebSocket

#### Feature 4: Task Assignment
**Description**: Assign tasks to team members with notifications.
**User Story**: As a project manager, I want to assign tasks so that team members know their responsibilities.
**Acceptance Criteria**:
- [ ] Assign 1-5 users per task
- [ ] Filter tasks by assignee, status, priority, due date
- [ ] Email notification sent within 60 seconds of assignment

### Future Scope (Post-MVP)
1. Due date reminders and calendar integration
2. File attachments on tasks (up to 10MB per file)
3. Task comments and activity log
4. Mobile app (React Native)
5. Time tracking per task

### Out of Scope
- Gantt charts and complex project timelines
- Invoice generation
- Built-in chat/messaging

### User Flows

#### Create and Assign Task
1. User navigates to project board
2. User clicks "Add Task" in desired column
3. User enters task details (title, description, due date)
4. User selects assignee from team member dropdown
5. System creates task and sends notification to assignee
6. Task appears on board in real-time for all viewers

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale | Alternatives Considered |
|-------|------------|-----------|------------------------|
| Frontend | Next.js 14 | App Router with RSC reduces client bundle, API routes unify codebase | Vite+React (no SSR), Remix (smaller ecosystem) |
| Styling | Tailwind CSS | Utility-first enables rapid iteration without CSS file sprawl | CSS Modules (more verbose), Styled Components (runtime cost) |
| UI Components | shadcn/ui | Copy-paste ownership, Tailwind-native, accessible by default | Radix (unstyled — more work), MUI (opinionated, large bundle) |
| Backend | Next.js API Routes | Unified deployment, no separate server, serverless scaling | Hono (faster but separate deploy), Express (mature but needs hosting) |
| Database | PostgreSQL (Neon) | Relational integrity for projects/tasks/members, full-text search built-in | SQLite (no concurrent writes), MongoDB (weak relations) |
| ORM | Prisma | Type-safe queries, migration CLI, visual studio | Drizzle (lighter but newer tooling), raw SQL (no type safety) |
| Real-time | Pusher | Managed WebSocket infrastructure, generous free tier (200k msg/day) | Socket.io (self-hosted ops), Ably (more expensive) |
| Auth | NextAuth.js | Drop-in with Next.js, supports OAuth + credentials | Clerk (managed but costs), Lucia (lighter but more manual) |
| Deployment | Vercel | Zero-config Next.js hosting, preview deployments, edge functions | Railway (more control, more ops), Cloudflare (edge but no Prisma adapter) |

---

## System Maps

### Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Next.js App   │────▶│  API Routes     │────▶│   PostgreSQL    │
│   (React RSC)   │◀────│  (Serverless)   │◀────│   (Neon)        │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   Pusher        │     │   Resend        │
│   (Real-time)   │     │   (Email)       │
└─────────────────┘     └─────────────────┘
```

### Data Model Relations

```
User (1) ──────< (N) ProjectMember >──────(1) Project
Project (1) ───< (N) Column
Column (1) ────< (N) Task
Task (1) ──────< (N) TaskAssignment >─────(1) User
```

### State Diagram: Task Lifecycle

```
                    ┌──────────┐
        create      │  To Do   │
       ────────▶    └────┬─────┘
                         │ start work
                         ▼
                    ┌──────────┐
                    │In Progress│
                    └────┬─────┘
                    │         │
          complete  │         │ block
                    ▼         ▼
              ┌──────────┐  ┌──────────┐
              │   Done   │  │ Blocked  │
              └──────────┘  └────┬─────┘
                                 │ unblock
                                 ▼
                           ┌──────────┐
                           │In Progress│
                           └──────────┘
```

### User Flow: Create and Assign Task

```
[Board View] → [Click "Add Task"] → [Fill Details] → [Select Assignee] → [Submit]
                                                                              │
                                                              ┌───────────────┤
                                                              ▼               ▼
                                                    [Pusher: broadcast]  [Resend: email]
                                                              │
                                                              ▼
                                                    [All viewers see task]
```

---

## Data Models

#### User
```typescript
interface User {
  id: string;           // cuid2
  email: string;        // unique, lowercase
  name: string;         // display name
  avatar?: string;      // URL to avatar image
  passwordHash?: string; // null for OAuth-only users
  createdAt: Date;
  updatedAt: Date;
}
```

#### Project
```typescript
interface Project {
  id: string;
  name: string;         // max 100 chars
  description?: string; // max 500 chars
  ownerId: string;      // User who created
  isArchived: boolean;  // soft delete
  createdAt: Date;
  updatedAt: Date;
}
```

#### ProjectMember
```typescript
interface ProjectMember {
  id: string;
  projectId: string;
  userId: string;
  role: 'admin' | 'member' | 'viewer';
  joinedAt: Date;
}
```

#### Column
```typescript
interface Column {
  id: string;
  projectId: string;
  name: string;         // max 50 chars
  order: number;        // 0-indexed position
  createdAt: Date;
}
```

#### Task
```typescript
interface Task {
  id: string;
  columnId: string;
  title: string;        // max 255 chars
  description?: string; // markdown, max 10,000 chars
  priority: 'low' | 'medium' | 'high' | 'urgent';
  order: number;        // position within column
  dueDate?: Date;
  createdAt: Date;
  updatedAt: Date;
}
```

#### Task Validation Schema
```typescript
const createTaskSchema = z.object({
  title: z.string().min(1).max(255),
  description: z.string().max(10_000).optional(),
  priority: z.enum(['low', 'medium', 'high', 'urgent']).default('medium'),
  dueDate: z.coerce.date().min(new Date()).optional(),
  assigneeIds: z.array(z.string()).max(5).optional(),
});
```

#### TaskAssignment
```typescript
interface TaskAssignment {
  id: string;
  taskId: string;
  userId: string;
  assignedAt: Date;
}
```

---

## API Endpoints

| Method | Endpoint | Description | Auth | Rate Limit |
|--------|----------|-------------|------|------------|
| GET | /api/projects | List user's projects | Required | 100/min |
| POST | /api/projects | Create project | Required | 30/min |
| GET | /api/projects/:id | Get project details | Required | 100/min |
| PUT | /api/projects/:id | Update project | Admin | 30/min |
| DELETE | /api/projects/:id | Archive project (soft delete) | Admin | 10/min |
| GET | /api/projects/:id/board | Get board with columns/tasks | Required | 100/min |
| POST | /api/projects/:id/members | Invite member | Admin | 30/min |
| POST | /api/columns | Create column | Admin | 30/min |
| PATCH | /api/columns/:id | Update/reorder column | Admin | 30/min |
| POST | /api/tasks | Create task | Member+ | 30/min |
| PATCH | /api/tasks/:id | Update task | Member+ | 60/min |
| PATCH | /api/tasks/:id/move | Move task between columns | Member+ | 60/min |
| DELETE | /api/tasks/:id | Delete task | Admin | 10/min |

---

## Security

### Authentication Flow

```
User → POST /api/auth/signin → NextAuth validates credentials or OAuth
    ↓
NextAuth creates JWT session (access: 15 min, refresh: 7 days)
    ↓
Client receives httpOnly cookie → included automatically on requests
    ↓
API routes call getServerSession() to validate
```

### Input Validation
- All request bodies validated with Zod schemas at API boundary
- SQL injection: Prisma parameterized queries (never raw string interpolation)
- XSS: React auto-escapes output, CSP header in next.config.js
- CSRF: NextAuth uses CSRF tokens for auth endpoints, SameSite=lax cookies

### Sensitive Data

| Data Type | Protection |
|-----------|-----------|
| Passwords | bcrypt hash, 12 rounds |
| OAuth tokens | Encrypted in database via NextAuth |
| Session cookies | httpOnly, secure, sameSite=lax |
| API keys (Pusher, Resend) | Environment variables only |

### Authorization
- Every API route checks `getServerSession()` for authentication
- Project-level RBAC: middleware checks `ProjectMember.role` before mutation
- Users can only access projects they are members of (query filtered by userId)

---

## Error Handling Strategy

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title is required",
    "details": { "field": "title", "constraint": "min 1 character" }
  }
}
```

### Error Boundaries
- **API layer**: try/catch wrapper on all route handlers, returns JSON errors
- **UI layer**: React error boundaries around Board, ProjectList, and TaskDetail
- **Real-time**: If Pusher connection drops, show "Reconnecting..." banner and poll every 5s
- **Email**: If Resend fails, log error and retry once after 30s; do not block task creation

---

## File Structure

```
taskflow/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── projects/page.tsx
│   │   │   └── projects/[id]/page.tsx
│   │   ├── api/
│   │   │   ├── auth/[...nextauth]/route.ts
│   │   │   ├── projects/route.ts
│   │   │   ├── projects/[id]/route.ts
│   │   │   ├── projects/[id]/board/route.ts
│   │   │   ├── projects/[id]/members/route.ts
│   │   │   ├── columns/route.ts
│   │   │   ├── columns/[id]/route.ts
│   │   │   ├── tasks/route.ts
│   │   │   ├── tasks/[id]/route.ts
│   │   │   └── tasks/[id]/move/route.ts
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/                  # shadcn components
│   │   ├── auth/
│   │   │   └── LoginForm.tsx
│   │   ├── board/
│   │   │   ├── Board.tsx
│   │   │   ├── Column.tsx
│   │   │   └── TaskCard.tsx
│   │   └── projects/
│   │       └── ProjectList.tsx
│   ├── lib/
│   │   ├── auth.ts              # NextAuth config
│   │   ├── db.ts                # Prisma client
│   │   ├── pusher.ts            # Pusher server + client
│   │   ├── email.ts             # Resend client
│   │   └── validations.ts       # Zod schemas
│   ├── hooks/
│   │   ├── useBoard.ts
│   │   └── useRealtime.ts
│   └── types/
│       └── index.ts
├── prisma/
│   └── schema.prisma
├── public/
├── tests/
│   ├── api/
│   │   ├── projects.test.ts
│   │   └── tasks.test.ts
│   └── components/
│       └── Board.test.tsx
├── .env.example
├── package.json
└── README.md
```

---

## Third-Party Integrations

| Service | Purpose | Free Tier Limits |
|---------|---------|-----------------|
| Pusher | Real-time board updates | 200k messages/day, 100 connections |
| Resend | Email notifications | 3,000 emails/month |
| Neon | PostgreSQL hosting | 512MB storage, 1 compute |
| Vercel | Deployment | 100GB bandwidth/month |

---

## Monitoring & Observability

| Aspect | Tool | Purpose |
|--------|------|---------|
| Error tracking | Sentry | Capture runtime errors with session replay |
| Health check | `GET /api/health` | Return `{ status, version, dbConnected }` |
| Performance | Vercel Analytics | Core Web Vitals (LCP < 2.5s, CLS < 0.1) |

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection string | Yes | - |
| NEXTAUTH_SECRET | Auth encryption secret (32+ chars) | Yes | - |
| NEXTAUTH_URL | App URL for auth callbacks | Yes | - |
| GOOGLE_CLIENT_ID | Google OAuth client ID | Yes | - |
| GOOGLE_CLIENT_SECRET | Google OAuth secret | Yes | - |
| PUSHER_APP_ID | Pusher app ID | Yes | - |
| NEXT_PUBLIC_PUSHER_KEY | Pusher public key (client-side) | Yes | - |
| PUSHER_SECRET | Pusher secret key | Yes | - |
| RESEND_API_KEY | Resend API key | Yes | - |
| SENTRY_DSN | Sentry error tracking DSN | No | - |

---

## Dependencies

### Production Dependencies
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "next-auth": "^4.24.0",
    "@prisma/client": "^5.6.0",
    "pusher-js": "^8.3.0",
    "pusher": "^5.2.0",
    "resend": "^2.0.0",
    "@dnd-kit/core": "^6.0.0",
    "@dnd-kit/sortable": "^7.0.0",
    "zod": "^3.22.0",
    "tailwindcss": "^3.3.0"
  }
}
```

### Development Dependencies
```json
{
  "devDependencies": {
    "typescript": "^5.3.0",
    "prisma": "^5.6.0",
    "@types/react": "^18.2.0",
    "eslint": "^8.54.0",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.0.0"
  }
}
```

---

## Development Phases

### Phase 1: Foundation
**Depends on**: Nothing
- [ ] Next.js project setup with TypeScript, Tailwind, shadcn/ui
- [ ] Prisma schema (User, Project, ProjectMember, Column, Task, TaskAssignment)
- [ ] Database migration and seed script
- [ ] NextAuth.js configuration (credentials + Google OAuth)
- [ ] Basic layout (header, sidebar, auth pages)

### Phase 2: Core Features
**Depends on**: Phase 1 (auth + database must exist)
- [ ] Project CRUD with member management
- [ ] Board view: columns with drag-and-drop tasks (@dnd-kit)
- [ ] Task CRUD: create, edit, move, delete with Zod validation
- [ ] Task assignment and filtering (by assignee, priority, due date)

### Phase 3: Real-time & Notifications
**Depends on**: Phase 2 (tasks must exist to broadcast changes)
- [ ] Pusher integration: broadcast task/column changes to project channel
- [ ] useRealtime hook: subscribe to project channel, optimistic UI updates
- [ ] Email notifications via Resend: assignment, due date reminder

### Phase 4: Polish & Launch
**Depends on**: Phase 3 (app must be functional)
- [ ] Error handling: API error middleware, React error boundaries, Pusher reconnection
- [ ] Loading states: skeleton screens for board, spinner for mutations
- [ ] Mobile responsiveness (board horizontal scroll on mobile)
- [ ] Sentry integration for error tracking
- [ ] Deployment to Vercel with preview environments

---

## Open Questions

| # | Question | Options | Impact | Status |
|---|----------|---------|--------|--------|
| 1 | Support task labels/tags in MVP? | A) Yes (adds filtering dimension), B) No (add post-MVP) | Adds 1 model + UI — ~2 days effort | Open |
| 2 | Email frequency for notifications? | A) Immediate, B) Daily digest, C) User preference | Digest requires background job queue | Open |
| 3 | Dark mode in v1? | A) Yes (Tailwind dark: variants), B) No (add later) | Low effort with Tailwind but doubles visual QA | Open |

---

## References

### Documentation
- [Next.js App Router](https://nextjs.org/docs/app)
- [Prisma with Next.js](https://prisma.io/docs/guides/nextjs)
- [NextAuth.js](https://next-auth.js.org/getting-started/introduction)
- [Pusher Channels](https://pusher.com/docs/channels)
- [@dnd-kit](https://docs.dndkit.com)

### Inspirations
- Trello (board UI, drag-and-drop)
- Linear (clean design, keyboard shortcuts)
- Notion (project organization, flexible views)

---

*Generated with project-spec plugin for Claude Code*
