# Feature Specification: Task Comments

> Adding comment threads to tasks in TaskFlow for team collaboration.

---

## Overview

### Description
Allow users to add comments to tasks, enabling discussion and collaboration without leaving the task context.

### Problem Statement
Team members currently need to use external tools (Slack, email) to discuss tasks, leading to fragmented communication and lost context.

### User Story
As a team member, I want to comment on tasks so that I can discuss details, ask questions, and provide updates without switching tools.

### Success Metrics
- [ ] Users can add comments to any task they have member+ access to
- [ ] Comments display with author name, avatar, and relative timestamp
- [ ] New comments appear for all viewers within 2 seconds via WebSocket
- [ ] Comment count badge visible on task cards (updates in real-time)

---

## Codebase Analysis

### Existing Patterns Detected

**Dependencies found in `package.json`**:
- `pusher-js` ^8.3.0 — WebSocket client for real-time (reuse for comment events)
- `@prisma/client` ^5.6.0 — ORM (add Comment model to existing schema)
- `zod` ^3.22.0 — validation (create comment validation schema)
- `resend` ^2.0.0 — email (future: notify on comment)

**API route pattern**: All routes follow `src/app/api/[resource]/route.ts` with `GET` and `POST` exports. Single-resource routes use `src/app/api/[resource]/[id]/route.ts`.

**Component pattern**: Feature components live in `src/components/[feature]/`. UI primitives are in `src/components/ui/` (shadcn).

**Real-time pattern**: Existing `useRealtime.ts` hook subscribes to Pusher channels. Events follow `entity:action` naming (e.g., `task:updated`). Subscribe per project channel: `project-${projectId}`.

**Auth pattern**: API routes call `getServerSession(authOptions)` to get current user. Permission checks query `ProjectMember` table for role.

**Existing models**: User, Project, ProjectMember, Column, Task, TaskAssignment — all in `prisma/schema.prisma`.

---

## Requirements

### Must Have (MVP)
- [ ] Add comment to a task (content: 1-2,000 characters)
- [ ] View all comments on a task in chronological order
- [ ] Display commenter name, avatar, and relative timestamp ("2h ago")
- [ ] Real-time comment updates via Pusher (channel: `task-${taskId}`)
- [ ] Comment count badge on task cards (updated via Pusher)

### Nice to Have (Post-MVP)
- [ ] Edit own comments (within 5 minutes of creation)
- [ ] Delete own comments
- [ ] @mention team members (autocomplete from project members)
- [ ] Markdown formatting in comments
- [ ] Comment reactions (emoji)

### Out of Scope
- Threaded/nested replies (flat comments only for MVP)
- File attachments in comments
- Comment search
- Email notifications for comments (future scope)

---

## Technical Design

### Affected Components

| Component | File | Changes |
|-----------|------|---------|
| TaskCard | `src/components/board/TaskCard.tsx` | Add CommentCount badge |
| TaskDetail | `src/components/board/TaskDetail.tsx` | Add comments section below description |
| API: tasks | `src/app/api/tasks/[id]/route.ts` | Include `_count.comments` in GET response |
| Pusher | `src/lib/pusher.ts` | No changes (reuse existing server + client instances) |
| Schema | `prisma/schema.prisma` | Add Comment model |
| Validations | `src/lib/validations.ts` | Add `createCommentSchema` |

### New Components

```
src/components/comments/
├── CommentList.tsx      # Renders list of comments with loading/empty states
├── CommentItem.tsx      # Single comment: avatar, name, time, content
├── CommentForm.tsx      # Textarea + submit button with validation
└── CommentCount.tsx     # Badge: 💬 3 (or hidden if 0)
```

### New API Routes

```
src/app/api/tasks/[id]/comments/route.ts    # GET (list) + POST (create)
```

### Database Changes

```prisma
model Comment {
  id        String   @id @default(cuid())
  content   String   @db.Text    // 1-2,000 chars (validated at API boundary)
  taskId    String
  task      Task     @relation(fields: [taskId], references: [id], onDelete: Cascade)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([taskId])      // Fast lookup: "all comments for this task"
  @@index([authorId])    // Fast lookup: "all comments by this user"
}

// Add to existing Task model:
model Task {
  // ... existing fields
  comments Comment[]
}

// Add to existing User model:
model User {
  // ... existing fields
  comments Comment[]
}
```

### Validation Schema

```typescript
// In src/lib/validations.ts
export const createCommentSchema = z.object({
  content: z.string()
    .min(1, "Comment cannot be empty")
    .max(2000, "Comment must be under 2,000 characters")
    .trim(),
});
```

### API Endpoints

#### List Comments
```http
GET /api/tasks/:taskId/comments
Authorization: Bearer <session>

Response: 200 OK
{
  "data": [
    {
      "id": "cm1abc123",
      "content": "Let's discuss the approach here",
      "author": {
        "id": "user123",
        "name": "Jane Doe",
        "avatar": "https://..."
      },
      "createdAt": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 5
}
```

**Authorization**: User must be a member of the project that owns this task.

#### Create Comment
```http
POST /api/tasks/:taskId/comments
Authorization: Bearer <session>
Content-Type: application/json

{
  "content": "This looks good to me!"
}

Response: 201 Created
{
  "data": {
    "id": "cm1xyz789",
    "content": "This looks good to me!",
    "author": { "id": "user456", "name": "Bob Smith", "avatar": "..." },
    "createdAt": "2024-01-15T11:00:00Z"
  }
}
```

**Authorization**: User must have member or admin role on the project.

### Real-time Events

```typescript
// Server: trigger after successful comment creation
await pusher.trigger(`task-${taskId}`, 'comment:created', {
  comment: { id, content, author: { id, name, avatar }, createdAt }
});

// Client: subscribe in TaskDetail component
useEffect(() => {
  const channel = pusher.subscribe(`task-${taskId}`);
  channel.bind('comment:created', (data) => {
    setComments(prev => [...prev, data.comment]);
  });
  return () => pusher.unsubscribe(`task-${taskId}`);
}, [taskId]);
```

---

## Implementation Plan

### Step 1: Database & Validation
**Depends on**: Nothing
- [ ] Add Comment model to `prisma/schema.prisma`
- [ ] Add `comments` relation to Task and User models
- [ ] Run `prisma migrate dev --name add-comments`
- [ ] Add `createCommentSchema` to `src/lib/validations.ts`

### Step 2: API Routes
**Depends on**: Step 1 (schema must be migrated)
- [ ] Create `src/app/api/tasks/[id]/comments/route.ts`
- [ ] Implement GET: list comments for task (include author name/avatar)
- [ ] Implement POST: create comment (validate with Zod, check project membership)
- [ ] Update GET `/api/tasks/[id]` to include `_count: { comments: true }`

### Step 3: UI Components
**Depends on**: Step 2 (API must exist for data fetching)
- [ ] Create `CommentItem.tsx` — avatar, name, relative time, content
- [ ] Create `CommentList.tsx` — maps comments, handles loading skeleton + empty state
- [ ] Create `CommentForm.tsx` — textarea (max 2,000 chars), submit button, validation error display
- [ ] Create `CommentCount.tsx` — badge showing count (hidden when 0)

### Step 4: Integration
**Depends on**: Step 3 (components must exist)
- [ ] Add CommentList + CommentForm to TaskDetail modal (below description)
- [ ] Add CommentCount badge to TaskCard (bottom-right, next to assignee avatar)
- [ ] Wire up form submission: POST, optimistic add to list, revert on error

### Step 5: Real-time
**Depends on**: Step 4 (comments must be visible in UI)
- [ ] Add Pusher trigger in POST comment route
- [ ] Subscribe to `comment:created` in TaskDetail using existing `useRealtime` pattern
- [ ] Update CommentCount on TaskCard via project channel broadcast

### Step 6: Polish
**Depends on**: Step 5 (everything must be wired up)
- [ ] Loading state: skeleton placeholders for CommentList
- [ ] Empty state: "No comments yet. Start the discussion!"
- [ ] Error handling: toast on failed submission, keep content in textarea
- [ ] Auto-scroll to bottom of CommentList on new comment
- [ ] Debounce real-time updates (batch within 100ms window)

---

## UI/UX Design

### Task Card (with comment count)
```
+---------------------------+
| Task Title                |
| Description preview...    |
|                           |
| [Avatar] Jane  💬 3       |
+---------------------------+
```

### Task Detail (comments section)
```
+----------------------------------+
| Task Title                    X  |
+----------------------------------+
| Description...                   |
|                                  |
| ================================ |
| Comments (3)                     |
| ================================ |
|                                  |
| [Avatar] Jane - 2h ago           |
| This looks good!                 |
|                                  |
| [Avatar] Bob - 1h ago            |
| Agreed, let's proceed.           |
|                                  |
| +------------------------------+ |
| | Add a comment...             | |
| +------------------------------+ |
| 0/2000                  [Submit] |
+----------------------------------+
```

### States

| State | Behavior |
|-------|----------|
| Loading | 3 skeleton placeholders (avatar circle + 2 text lines) |
| Empty | "No comments yet. Start the discussion!" with muted text |
| Error | Toast notification: "Failed to post comment. Try again.", keep content in textarea |
| Submitting | Textarea disabled, spinner on submit button |
| Character limit | Counter turns red at 1,900+ chars, submit disabled at 2,001+ |

---

## Edge Cases

### Error Scenarios

| Scenario | Expected Behavior |
|----------|-------------------|
| Empty comment submission | Submit button disabled when textarea is empty or whitespace-only |
| Comment exceeds 2,000 chars | Character counter shows red, submit button disabled |
| Network error on submit | Toast: "Failed to post comment", content stays in textarea for retry |
| Task deleted while viewing | TaskDetail modal closes, board refreshes, toast: "This task was deleted" |
| User removed from project while commenting | POST returns 403, toast: "You no longer have access to this project" |
| Pusher connection drops | Comments still work via form submit; new comments from others appear on next manual refresh |

### Boundary Conditions

| Condition | Handling |
|-----------|----------|
| Very long comment (2,000 chars) | No truncation in CommentItem (full display, container scrolls) |
| Rapid sequential comments | Debounce Pusher events: batch within 100ms window to avoid UI jank |
| Task with 500+ comments | Paginate: load 50 most recent, "Load earlier comments" button at top |
| Simultaneous comment by 2 users | Both appear via Pusher; server assigns `createdAt` to prevent ordering conflicts |

---

## Testing Strategy

### Unit Tests

```typescript
// CommentForm.test.tsx
- renders textarea and submit button
- submit button disabled when textarea is empty
- submit button disabled when content exceeds 2,000 chars
- calls onSubmit with trimmed content
- clears textarea after successful submission
- shows character count
- keeps content on submission error

// CommentList.test.tsx
- renders list of comments in chronological order
- shows loading skeleton when isLoading=true
- shows empty state when comments array is empty
- displays author name, avatar, and relative timestamp

// CommentCount.test.tsx
- renders count when > 0
- hidden when count is 0
```

### Integration Tests

```typescript
// comments.api.test.ts
- POST /api/tasks/:id/comments creates comment and returns 201
- POST with empty content returns 422 validation error
- POST with content > 2,000 chars returns 422
- GET /api/tasks/:id/comments returns comments in chronological order
- GET includes author name and avatar
- comments cascade-deleted when task is deleted
- viewer role cannot POST comments (returns 403)
- non-project-member cannot GET comments (returns 403)
```

### E2E Tests

```typescript
// comments.e2e.test.ts
- user can add comment to task and see it appear
- comment appears in real-time for another user viewing the same task
- comment count updates on task card after adding comment
```

---

## Open Questions

| # | Question | Options | Impact | Status |
|---|----------|---------|--------|--------|
| 1 | Notify task assignees on new comment? | A) Email notification, B) In-app only, C) Skip for MVP | Email adds Resend dependency per comment | Open |
| 2 | Comments visible to viewers? | A) Yes (read-only), B) Only members+ | Affects permission check in GET route | Open |
| 3 | Comment editing in MVP? | A) Yes (5-min window), B) No (post-MVP) | Adds PATCH endpoint + UI complexity | Open |

---

## References

### Existing Patterns to Follow
- Real-time: `src/hooks/useRealtime.ts` — subscribe/unsubscribe pattern
- API routes: `src/app/api/tasks/route.ts` — auth check + Zod validation pattern
- Components: `src/components/board/TaskCard.tsx` — avatar + badge layout
- Styling: shadcn `Card`, `Avatar`, `Button`, `Textarea` components

### Design Inspiration
- Linear comments (clean, minimal)
- GitHub issue comments (author + timestamp + content)
- Notion comments (inline, non-intrusive)

---

*Generated with project-spec plugin for Claude Code*

*Use the `feature-dev` skill to explore existing patterns and implement this feature.*
