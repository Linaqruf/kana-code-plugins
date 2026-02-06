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

## Codebase-Aware Skipping

When codebase analysis detects answers, pre-fill and confirm instead of asking:

| Detected Signal | Auto-Fill | Confirmation |
|----------------|-----------|-------------|
| `bun.lockb` exists | Package manager: bun | "Detected bun. Continuing with that." |
| `pnpm-lock.yaml` exists | Package manager: pnpm | "Detected pnpm. Continuing with that." |
| `package-lock.json` exists | Package manager: npm | "Detected npm. Continuing with that." |
| `yarn.lock` exists | Package manager: yarn | "Detected yarn. Continuing with that." |
| `next` in package.json dependencies | Frontend: Next.js | "Detected Next.js in dependencies." |
| `tailwindcss` in package.json | Styling: Tailwind CSS | "Detected Tailwind CSS in dependencies. Continuing with that." |
| `prisma/schema.prisma` exists | ORM: Prisma | "Found Prisma schema. Continuing with Prisma." |
| `drizzle/` directory or `drizzle-orm` in deps | ORM: Drizzle | "Found Drizzle config. Continuing with Drizzle." |
| `.github/workflows/` exists | CI/CD: GitHub Actions | "Detected GitHub Actions workflows. Noting in spec." |
| `Dockerfile` exists | Containerized deployment | "Detected Dockerfile. Noting containerized deployment in spec." |

---

## Auto-Detect Project Type

When no project type argument is provided, infer from codebase signals:

| Signal | Inferred Type |
|--------|--------------|
| `bin` field in package.json | CLI |
| `src/app/` or `pages/` directory with frontend deps | Web App |
| `src/api/` or `routes/` without frontend directories | API |
| `exports` or `main` field + `types` field, no `src/app/` | Library |
| `pyproject.toml` with `[tool.poetry.scripts]` | CLI (Python) |
| `Cargo.toml` with `[[bin]]` | CLI (Rust) |
| `cmd/` directory in Go project | CLI (Go) |

If inferred, confirm with user: "This looks like a [type] project. Is that correct?"

---

*Lookup reference. For interview methodology, see SKILL.md.*
