# Per-Section Structural Templates

> Legacy from v2.0 — preserved for backward compatibility. These templates provide granular structural guidance when adapting specific sections to unusual project types.

**Primary reference**: `references/output-template.md` (use this for generation)
**These templates**: Optional lookup for adapting individual sections — not required for standard spec generation

## SPEC.md Section Templates

| Template | Section | When to Use |
|----------|---------|-------------|
| `overview.template.md` | Overview | Always — problem, users, success criteria |
| `architecture.template.md` | Technical Architecture | Always — tech stack, system design |
| `frontend.template.md` | Frontend | Web apps with UI |
| `backend.template.md` | Backend | Apps with server-side logic |
| `data-models.template.md` | Data Models | Apps with database |
| `api-reference.template.md` | API Endpoints | Apps with API routes |
| `security.template.md` | Security | Apps with auth or sensitive data |
| `design-system.template.md` | Design System | Frontend projects |
| `configuration.template.md` | Configuration | Apps with env vars or config files |
| `cli-reference.template.md` | Commands | CLI tools |

## Output Templates

| Template | Output File | When to Use |
|----------|------------|-------------|
| `CLAUDE.md.template` | `CLAUDE.md` | Always — agent-optimized pointer file |
