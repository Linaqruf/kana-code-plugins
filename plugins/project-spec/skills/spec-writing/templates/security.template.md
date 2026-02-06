# Security Template

> Security architecture. Create if project handles sensitive data.

```markdown
## Security

> Security implementation for [Project Name]

## Authentication

| Aspect | Implementation |
|--------|----------------|
| **Method** | [Session/JWT/OAuth] |
| **Provider** | [Built-in/Clerk/Auth0] |

### Auth Flow

1. User submits credentials
2. Server validates
3. Server issues token
4. Client stores token
5. Client sends token with requests

## Authorization

### Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| Admin | Full access | All |
| User | Standard | Own resources |

### Permission Matrix

| Resource | Admin | User |
|----------|-------|------|
| [Resource] | CRUD | CR |

## Data Protection

| Data Type | Protection |
|-----------|------------|
| Passwords | Hashed (bcrypt) |
| PII | Encrypted at rest |
| Tokens | Secure storage |

## Input Validation

```typescript
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});
```

## Security Headers

```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000
```

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| Auth | 5 | 15 min |
| API | 100 | 1 min |

## Compliance

| Standard | Status |
|----------|--------|
| GDPR | [Status] |

---

*Related: Backend*
```

## When to Create

- Project handles user credentials
- Project stores personal data
- Project has compliance requirements
