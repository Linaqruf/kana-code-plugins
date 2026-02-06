# Configuration Template

> Environment and settings documentation. Create if project needs config docs.

```markdown
## Configuration

> Environment configuration for [Project Name]

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | DB connection | `postgresql://...` |
| `[APP]_SECRET` | App secret | `your-secret` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `LOG_LEVEL` | Log level | `info` |
| `NODE_ENV` | Environment | `development` |

## Environment Files

```
.env                 # Local (git-ignored)
.env.example         # Template (committed)
```

### .env.example

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# App
[APP]_SECRET=change-in-production
PORT=3000
```

## Validation

```typescript
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  [APP]_SECRET: z.string().min(32),
  PORT: z.coerce.number().default(3000),
});

export const env = envSchema.parse(process.env);
```

## By Environment

### Development

| Setting | Value |
|---------|-------|
| Log Level | debug |
| HTTPS | Off |

### Production

| Setting | Value |
|---------|-------|
| Log Level | info |
| HTTPS | Required |

## Secrets

- Local: `.env` (git-ignored)
- Production: Platform secrets (Vercel, AWS, etc.)

---

*Related: Architecture*
```

## When to Create

- Project has environment variables
- Project needs configuration documentation
- Project deploys to multiple environments
