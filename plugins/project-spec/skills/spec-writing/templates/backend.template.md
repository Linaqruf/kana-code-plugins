# Backend Template

> Server-side architecture. Create if project has backend/API.

```markdown
## Backend

> Server implementation for [Project Name]

## Framework

| Aspect | Choice |
|--------|--------|
| **Framework** | [Express/FastAPI/Hono/etc.] |
| **Runtime** | [Node.js/Deno/Bun/Python] |
| **API Style** | [REST/GraphQL/tRPC] |

## Directory Structure

```
src/
├── routes/           # API routes
├── services/         # Business logic
├── models/           # Data models
├── middleware/       # Request middleware
└── utils/            # Utilities
```

## API Design

### Base URL

```
Development: http://localhost:[port]
Production: https://api.[domain].com
```

### Response Format

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

## Services

| Service | Purpose |
|---------|---------|
| [Name] | [Purpose] |

## Error Handling

| Code | HTTP | Description |
|------|------|-------------|
| `NOT_FOUND` | 404 | Resource not found |
| `UNAUTHORIZED` | 401 | Auth required |
| `VALIDATION_ERROR` | 400 | Invalid input |

---

*Related: API Reference, Data Models*
```

## When to Create

- Project has server component
- Project exposes API
- Project processes data server-side
