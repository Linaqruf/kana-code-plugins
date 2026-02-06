# API Reference Template

> Endpoint documentation. Create if project exposes API.

```markdown
## API Reference

> API documentation for [Project Name]

## Base URL

| Environment | URL |
|-------------|-----|
| Development | `http://localhost:[port]/api` |
| Production | `https://api.[domain].com` |

## Authentication

```
Authorization: Bearer <token>
```

## Endpoints

### [Resource]

#### List [Resources]

```http
GET /[resources]
```

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `limit` | int | 20 | Items per page |

**Response:**

```json
{
  "success": true,
  "data": [{ "id": "...", ... }],
  "meta": { "page": 1, "total": 100 }
}
```

---

#### Get [Resource]

```http
GET /[resources]/:id
```

---

#### Create [Resource]

```http
POST /[resources]
```

**Body:**

```json
{
  "name": "string",
  "description": "string?"
}
```

---

#### Update [Resource]

```http
PUT /[resources]/:id
```

---

#### Delete [Resource]

```http
DELETE /[resources]/:id
```

---

## Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `NOT_FOUND` | 404 | Not found |
| `UNAUTHORIZED` | 401 | Auth required |
| `VALIDATION_ERROR` | 400 | Invalid input |

## Rate Limits

| Type | Limit | Window |
|------|-------|--------|
| Auth | 5 | 15 min |
| Read | 100 | 1 min |
| Write | 20 | 1 min |

---

*Related: Backend, Data Models*
```

## When to Create

- Project exposes REST API
- Project has GraphQL API
- Project has public endpoints
