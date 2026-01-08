# Project Specification: TaskFlow

## Overview

### Problem Statement
Teams struggle to track tasks across multiple projects, leading to missed deadlines and unclear accountability.

### Solution
TaskFlow is a collaborative task management web application that provides clear project organization, real-time updates, and team visibility.

### Target Users
- **Primary**: Small to medium teams (5-50 people)
- **Secondary**: Project managers, team leads
- **Technical Level**: Non-technical to technical users

### Success Criteria
- [ ] Users can create, assign, and complete tasks
- [ ] Real-time updates when team members make changes
- [ ] Projects can be organized with boards and lists

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: User Authentication
**Description**: Secure sign-up and login with email or OAuth providers.
**User Story**: As a user, I want to create an account so that I can access my tasks from any device.
**Acceptance Criteria**:
- [ ] Email/password registration with validation
- [ ] Google OAuth sign-in option
- [ ] Password reset via email
- [ ] Session persistence across browser refreshes

#### Feature 2: Project Management
**Description**: Create and organize projects to group related tasks.
**User Story**: As a team lead, I want to create projects so that I can organize tasks by initiative.
**Acceptance Criteria**:
- [ ] Create, edit, delete projects
- [ ] Add team members to projects
- [ ] Project-level permissions (admin, member, viewer)

#### Feature 3: Task Board
**Description**: Kanban-style board for visualizing task progress.
**User Story**: As a user, I want to drag tasks between columns so that I can update their status quickly.
**Acceptance Criteria**:
- [ ] Create custom columns (To Do, In Progress, Done, etc.)
- [ ] Drag-and-drop task movement
- [ ] Task details: title, description, assignee, due date
- [ ] Real-time sync across users

#### Feature 4: Task Assignment
**Description**: Assign tasks to team members with notifications.
**User Story**: As a project manager, I want to assign tasks so that team members know their responsibilities.
**Acceptance Criteria**:
- [ ] Assign one or multiple users to a task
- [ ] Filter tasks by assignee
- [ ] Email notification on assignment

### Future Scope (Post-MVP)
1. Due date reminders and calendar integration
2. File attachments on tasks
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

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | Next.js 14 | App Router, RSC, great DX |
| Styling | Tailwind CSS | Rapid development, consistent design |
| UI Components | shadcn/ui | Accessible, customizable |
| Backend | Next.js API Routes | Unified codebase, serverless |
| Database | PostgreSQL | Reliable, relational data |
| ORM | Prisma | Type-safe, great migrations |
| Real-time | Pusher | Easy WebSocket integration |
| Auth | NextAuth.js | Flexible, supports OAuth |
| Deployment | Vercel | Seamless Next.js hosting |

### System Design

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Next.js App   │────▶│  API Routes     │────▶│   PostgreSQL    │
│   (React RSC)   │◀────│  (Serverless)   │◀────│   (Neon/Supabase)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   Pusher        │     │   Resend        │
│   (Real-time)   │     │   (Email)       │
└─────────────────┘     └─────────────────┘
```

### Data Models

#### User
```typescript
interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  createdAt: Date;
  updatedAt: Date;
}
```

#### Project
```typescript
interface Project {
  id: string;
  name: string;
  description?: string;
  ownerId: string;        // User who created
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
  name: string;
  order: number;
  createdAt: Date;
}
```

#### Task
```typescript
interface Task {
  id: string;
  columnId: string;
  title: string;
  description?: string;
  order: number;
  dueDate?: Date;
  createdAt: Date;
  updatedAt: Date;
}
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

### API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /api/projects | List user's projects | Required |
| POST | /api/projects | Create project | Required |
| GET | /api/projects/:id | Get project details | Required |
| PUT | /api/projects/:id | Update project | Admin |
| DELETE | /api/projects/:id | Delete project | Admin |
| GET | /api/projects/:id/board | Get board with columns/tasks | Required |
| POST | /api/columns | Create column | Admin |
| PATCH | /api/columns/:id | Update/reorder column | Admin |
| POST | /api/tasks | Create task | Member+ |
| PATCH | /api/tasks/:id | Update task | Member+ |
| PATCH | /api/tasks/:id/move | Move task between columns | Member+ |
| DELETE | /api/tasks/:id | Delete task | Admin |

### Authentication & Authorization

**Strategy**: NextAuth.js with JWT sessions

**Providers**:
- Credentials (email/password)
- Google OAuth

**User Roles per Project**:
- **Admin**: Full control, manage members, delete project
- **Member**: Create/edit tasks, move tasks
- **Viewer**: Read-only access

### Third-Party Integrations

| Service | Purpose | Notes |
|---------|---------|-------|
| Pusher | Real-time updates | Free tier: 200k messages/day |
| Resend | Email notifications | Free tier: 3k emails/month |
| Neon | PostgreSQL hosting | Free tier: 512MB storage |

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
│   │   │   ├── columns/route.ts
│   │   │   └── tasks/route.ts
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
│   │   ├── pusher.ts            # Pusher client
│   │   └── email.ts             # Resend client
│   ├── hooks/
│   │   ├── useBoard.ts
│   │   └── useRealtime.ts
│   └── types/
│       └── index.ts
├── prisma/
│   └── schema.prisma
├── public/
├── .env.example
├── package.json
└── README.md
```

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
    "resend": "^2.0.0",
    "@dnd-kit/core": "^6.0.0",
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
    "eslint": "^8.54.0"
  }
}
```

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection string | Yes | - |
| NEXTAUTH_SECRET | Auth encryption secret | Yes | - |
| NEXTAUTH_URL | App URL for auth callbacks | Yes | - |
| GOOGLE_CLIENT_ID | Google OAuth client ID | Yes | - |
| GOOGLE_CLIENT_SECRET | Google OAuth secret | Yes | - |
| PUSHER_APP_ID | Pusher app ID | Yes | - |
| PUSHER_KEY | Pusher public key | Yes | - |
| PUSHER_SECRET | Pusher secret key | Yes | - |
| RESEND_API_KEY | Resend API key | Yes | - |

---

## Development Phases

### Phase 1: Foundation
- [ ] Next.js project setup with TypeScript
- [ ] Prisma schema and database setup
- [ ] NextAuth.js configuration (credentials + Google)
- [ ] Basic layout and navigation

### Phase 2: Core Features
- [ ] Project CRUD operations
- [ ] Team member management
- [ ] Board view with columns
- [ ] Task CRUD with drag-and-drop

### Phase 3: Real-time & Notifications
- [ ] Pusher integration for real-time updates
- [ ] Email notifications via Resend
- [ ] Optimistic UI updates

### Phase 4: Polish & Launch
- [ ] Error handling and validation
- [ ] Loading states and skeletons
- [ ] Mobile responsiveness
- [ ] Deployment to Vercel

---

## Open Questions

- [ ] Should we support task labels/tags in MVP?
- [ ] Email frequency preferences - immediate or digest?
- [ ] Dark mode support?

---

## References

### Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [Prisma Docs](https://prisma.io/docs)
- [NextAuth.js Docs](https://next-auth.js.org)
- [Pusher Docs](https://pusher.com/docs)

### Inspirations
- Trello (board UI)
- Linear (clean design)
- Notion (project organization)

---

*Generated with project-spec plugin for Claude Code*
