# Data Models Template

> Database schema and data structures. Create if project has database.

```markdown
## Data Models

> Database schema for [Project Name]

## Database

| Aspect | Choice |
|--------|--------|
| **Database** | [PostgreSQL/MySQL/SQLite/MongoDB] |
| **ORM** | [Prisma/Drizzle/TypeORM/etc.] |

## Entity Relationship

```
┌─────────────┐       ┌─────────────┐
│    User     │       │   [Entity]  │
├─────────────┤       ├─────────────┤
│ id      PK  │───┐   │ id      PK  │
│ email       │   └──▶│ user_id FK  │
│ name        │       │ [field]     │
└─────────────┘       └─────────────┘
```

## Models

### User

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `email` | VARCHAR(255) | No | Unique email |
| `name` | VARCHAR(100) | Yes | Display name |
| `created_at` | TIMESTAMP | No | Creation time |

**Schema:**

```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now()) @map("created_at")

  @@map("users")
}
```

---

### [Entity]

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `[field]` | [TYPE] | [Yes/No] | [Description] |

---

## Enums

### [EnumName]

| Value | Description |
|-------|-------------|
| `VALUE_1` | [Description] |
| `VALUE_2` | [Description] |

## Migrations

```bash
# Generate
npx prisma migrate dev --name [name]

# Apply
npx prisma migrate deploy
```

---

*Related: Backend, API Reference*
```

## When to Create

- Project has database
- Project stores persistent data
