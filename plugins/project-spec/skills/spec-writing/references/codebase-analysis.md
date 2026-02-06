# Codebase Analysis Reference v4.0.0

Lookup reference for detecting existing projects, identifying frameworks, and scanning codebase patterns. See SKILL.md for interview methodology.

---

## Detecting Existing Projects

Scan for these indicators to determine if a codebase exists:

**Package managers & configs:**
- `package.json`, `bun.lockb`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`
- `Cargo.toml`, `Cargo.lock`
- `pyproject.toml`, `requirements.txt`, `Pipfile`
- `go.mod`, `go.sum`
- `composer.json`
- `Gemfile`

**Source directories:**
- `src/`, `app/`, `lib/`, `pkg/`, `internal/`
- `pages/`, `routes/`, `api/`
- `components/`, `views/`, `templates/`

**Config files:**
- `.env`, `.env.local`, `.env.example`
- `*.config.ts`, `*.config.js`, `*.config.mjs`
- `tsconfig.json`, `jsconfig.json`
- `Dockerfile`, `docker-compose.yml`
- `.github/workflows/`

---

## Framework Detection

Read `package.json` dependencies to identify:

| Dependency | Framework |
|-----------|-----------|
| `next` | Next.js |
| `react` | React (check for Next.js first) |
| `vue` | Vue.js |
| `svelte`, `@sveltejs/kit` | SvelteKit |
| `@angular/core` | Angular |
| `express` | Express.js |
| `hono` | Hono |
| `fastify` | Fastify |
| `@prisma/client` | Prisma ORM |
| `drizzle-orm` | Drizzle ORM |
| `tailwindcss` | Tailwind CSS |

For Python: read `pyproject.toml` or `requirements.txt` for `fastapi`, `django`, `flask`.
For Rust: read `Cargo.toml` for `actix-web`, `axum`, `rocket`.
For Go: read `go.mod` for `gin`, `echo`, `fiber`.

---

## Deep Codebase Scanning

When documenting an existing project, scan these patterns:

| Pattern | What to Extract |
|---------|----------------|
| `src/api/**`, `app/api/**`, `routes/**` | API endpoints |
| `src/components/**`, `app/components/**` | UI components |
| `src/models/**`, `prisma/schema.prisma`, `drizzle/schema.ts` | Data models |
| `src/lib/**`, `src/utils/**`, `src/helpers/**` | Shared utilities |
| `src/hooks/**`, `src/composables/**` | Frontend hooks/composables |
| `middleware/**`, `src/middleware/**` | Middleware (auth, rate limiting) |
| `src/jobs/**`, `src/workers/**`, `src/queues/**` | Background jobs |
| `tests/**`, `__tests__/**`, `*.test.*`, `*.spec.*` | Test coverage |
| `src/styles/**`, `tailwind.config.*` | Styling system |
| `src/types/**`, `src/@types/**` | Type definitions |
| `.github/workflows/**` | CI/CD pipelines |

---

*Lookup reference. For interview methodology, see SKILL.md.*
