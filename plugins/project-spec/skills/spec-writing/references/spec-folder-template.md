# SPEC/ Folder - Optional Supplements

SPEC/ is an **optional** folder for reference material that would bloat SPEC.md. The core specification always lives in SPEC.md.

## Core Principle

**SPEC.md is always complete. SPEC/ files are optional lookup references.**

- **SPEC.md** = Things you READ (narrative, decisions, requirements)
- **SPEC/*.md** = Things you LOOK UP (schemas, SDK patterns, external APIs)

## When to Create Supplements

Only create SPEC/ files for:

1. **Reference material** - Schemas, tables, detailed examples you look up, not read through
2. **External dependencies** - SDK patterns, library usage, third-party API details

## Supplement Types

| File | When to Create | Content |
|------|----------------|---------|
| `api-reference.md` | Many endpoints (10+) with detailed schemas | Full request/response schemas, examples |
| `data-models.md` | Complex entity relationships | Entity schemas, validation rules, relations |
| `sdk-patterns.md` | Heavy use of external SDK | Usage patterns, code examples, gotchas |

## Structure

```
SPEC.md               # Always created, always self-sufficient
CLAUDE.md             # Generated with spec references

SPEC/                 # Optional, created when user agrees
├── api-reference.md  # Lookup: endpoint schemas
├── data-models.md    # Lookup: entity schemas
└── sdk-patterns.md   # Lookup: SDK usage
```

## Connecting to SPEC.md

When supplements exist, reference them in SPEC.md:

### Inline References (in relevant sections)

```markdown
## API Design

**Endpoints overview:**
- `POST /auth/login` - User authentication
- `GET /projects` - List user projects
- `POST /projects/:id/tasks` - Create task

→ When implementing endpoints, reference `SPEC/api-reference.md` for full request/response schemas.
```

### References Section (bottom of SPEC.md)

```markdown
---

## References

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using Anthropic SDK: `SPEC/sdk-patterns.md`
→ When designing data models: `SPEC/data-models.md`
```

## Supplement File Template

Each supplement should follow this structure:

```markdown
# [Title] Reference

> Lookup reference for [purpose]. See SPEC.md for full specification.

---

## [Section 1]

[Detailed reference content...]

## [Section 2]

[Detailed reference content...]

---

*This is a lookup reference. For project overview, see SPEC.md*
```

## Example: API Reference Supplement

```markdown
# API Reference

> Lookup reference for API endpoints. See SPEC.md for overview.

---

## Authentication

### POST /auth/login

**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  }
}
```

**Errors:**
- `401` - Invalid credentials
- `429` - Too many attempts

---

## Projects

### GET /projects

**Query Parameters:**
- `page` (number, default: 1)
- `limit` (number, default: 20)
- `status` (string, optional): "active" | "archived"

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

*This is a lookup reference. For project overview, see SPEC.md*
```

## Example: SDK Patterns Supplement

```markdown
# SDK Patterns Reference

> Lookup reference for Anthropic SDK usage. See SPEC.md for architecture.

---

## Client Setup

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

## Message Creation

```typescript
const message = await client.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }],
});
```

## Streaming

```typescript
const stream = await client.messages.stream({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }],
});

for await (const event of stream) {
  // Handle events
}
```

## Error Handling

```typescript
try {
  const message = await client.messages.create({...});
} catch (error) {
  if (error instanceof Anthropic.APIError) {
    console.error(error.status, error.message);
  }
}
```

---

*This is a lookup reference. For project overview, see SPEC.md*
```

## When NOT to Create Supplements

- Simple projects with few endpoints
- When all content fits comfortably in SPEC.md
- For content that should be read, not looked up
- For project requirements, architecture, or decisions (these belong in SPEC.md)

## Integration with CLAUDE.md

CLAUDE.md references supplements with triggers:

```markdown
## Spec Reference

Primary spec: `SPEC.md`

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using Anthropic SDK: `SPEC/sdk-patterns.md`
```
