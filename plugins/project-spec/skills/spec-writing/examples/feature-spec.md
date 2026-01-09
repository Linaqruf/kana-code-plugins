# Feature Specification: Task Comments

Adding comment threads to tasks in TaskFlow for team collaboration.

---

## Overview

### Description
Allow users to add comments to tasks, enabling discussion and collaboration without leaving the task context.

### Problem Statement
Team members currently need to use external tools (Slack, email) to discuss tasks, leading to fragmented communication and lost context.

### User Story
As a team member, I want to comment on tasks so that I can discuss details, ask questions, and provide updates without switching tools.

### Success Metrics
- [ ] Users can add comments to any task
- [ ] Comments display with author and timestamp
- [ ] Real-time updates when others comment
- [ ] Comment count visible on task cards

---

## Requirements

### Must Have (MVP)
- [ ] Add comment to a task
- [ ] View all comments on a task in chronological order
- [ ] Display commenter name, avatar, and timestamp
- [ ] Real-time comment updates via Pusher
- [ ] Comment count badge on task cards

### Nice to Have (Post-MVP)
- [ ] Edit own comments (within 5 minutes)
- [ ] Delete own comments
- [ ] @mention team members
- [ ] Markdown formatting in comments
- [ ] Comment reactions (emoji)

### Out of Scope
- Threaded/nested replies (flat comments only for MVP)
- File attachments in comments
- Comment search
- Email notifications for comments

---

## Technical Design

### Affected Components

| Component | Changes |
|-----------|---------|
| `TaskCard.tsx` | Add comment count badge |
| `TaskDetail.tsx` | Add comments section |
| `api/tasks/[id]/route.ts` | Include comments in task response |
| `lib/pusher.ts` | Add comment channel events |
| `prisma/schema.prisma` | Add Comment model |

### New Components

```
src/components/comments/
├── CommentList.tsx      # Renders list of comments
├── CommentItem.tsx      # Single comment display
├── CommentForm.tsx      # Add comment input
└── CommentCount.tsx     # Badge showing count
```

### Database Changes

```prisma
model Comment {
  id        String   @id @default(cuid())
  content   String   @db.Text
  taskId    String
  task      Task     @relation(fields: [taskId], references: [id], onDelete: Cascade)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([taskId])
  @@index([authorId])
}

// Add to Task model:
model Task {
  // ... existing fields
  comments Comment[]
}
```

### API Changes

#### List Comments
```http
GET /api/tasks/:taskId/comments
Authorization: Bearer <token>

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

#### Create Comment
```http
POST /api/tasks/:taskId/comments
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "This looks good to me!"
}

Response: 201 Created
{
  "data": { ... }
}
```

### Real-time Events

```typescript
// Channel: task-{taskId}
// Events:
pusher.trigger(`task-${taskId}`, 'comment:created', {
  comment: { id, content, author, createdAt }
});

pusher.trigger(`task-${taskId}`, 'comment:deleted', {
  commentId: string
});
```

---

## Implementation Plan

### Step 1: Database & API
- [ ] Add Comment model to Prisma schema
- [ ] Run migration
- [ ] Create GET /api/tasks/:taskId/comments endpoint
- [ ] Create POST /api/tasks/:taskId/comments endpoint
- [ ] Add comment count to task queries

### Step 2: UI Components
- [ ] Create CommentItem component
- [ ] Create CommentList component
- [ ] Create CommentForm component
- [ ] Create CommentCount badge component

### Step 3: Integration
- [ ] Add CommentList to TaskDetail modal
- [ ] Add CommentCount to TaskCard
- [ ] Wire up form submission

### Step 4: Real-time
- [ ] Add Pusher events for new comments
- [ ] Subscribe to comment channel in TaskDetail
- [ ] Optimistic UI updates

### Step 5: Polish
- [ ] Loading states for comments
- [ ] Empty state when no comments
- [ ] Error handling for failed submissions
- [ ] Scroll to bottom on new comment

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
|                        [Submit]  |
+----------------------------------+
```

### States

| State | Behavior |
|-------|----------|
| Loading | Skeleton placeholders for comments |
| Empty | "No comments yet. Start the discussion!" |
| Error | Toast notification, retry option |
| Submitting | Disabled input, spinner on button |

---

## Edge Cases

### Error Handling

| Scenario | Handling |
|----------|----------|
| Empty comment submission | Disable submit button, show validation |
| Network error on submit | Show error toast, keep comment in input |
| Task deleted while viewing | Redirect to board, show notification |
| User lacks permission | Hide comment form, show read-only |

### Boundary Conditions

- Maximum comment length: 2000 characters
- Rate limit: 10 comments per minute per user
- Handle very long comments (truncate with "show more")
- Handle rapid sequential comments (debounce real-time updates)

---

## Testing Strategy

### Unit Tests

```typescript
// CommentForm.test.tsx
- renders input and submit button
- disables submit when empty
- calls onSubmit with content
- clears input after submission
- shows error state

// CommentList.test.tsx
- renders list of comments
- shows empty state when no comments
- orders comments chronologically
```

### Integration Tests

```typescript
// comments.test.ts
- POST /api/tasks/:id/comments creates comment
- GET /api/tasks/:id/comments returns comments
- comments are deleted when task is deleted
- unauthorized users cannot comment
```

### E2E Tests

```typescript
// comments.spec.ts
- user can add comment to task
- comment appears in real-time for other users
- comment count updates on task card
```

---

## Open Questions

- [ ] Should we notify task assignees when a comment is added?
- [ ] Should comments be visible to viewers or only members?
- [ ] Do we need comment editing in MVP?

---

## References

### Existing Patterns
- Real-time updates: See `useRealtime.ts` hook
- API structure: Follow `/api/tasks` patterns
- Component styling: Use existing Card and Avatar components

### Design Inspiration
- Linear comments
- GitHub issue comments
- Notion comments

---

*Generated with project-spec plugin for Claude Code*

*Use the `feature-dev` skill to explore existing patterns and implement this feature.*
