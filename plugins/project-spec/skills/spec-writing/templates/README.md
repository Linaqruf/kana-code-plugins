# Templates

Section templates for generating SPEC.md and optional SPEC/ supplements. Each template defines the structure and content guidelines for one section or file.

## SPEC.md Section Templates

These templates define individual sections within SPEC.md:

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

## SPEC/ Supplement Templates

These templates define standalone files in the optional SPEC/ folder:

| Template | Output File | When to Create |
|----------|------------|----------------|
| `index.template.md` | `SPEC/index.md` | When user opts for SPEC/ supplements |

## Process Templates

These templates define tracking and status sections:

| Template | Section | When to Use |
|----------|---------|-------------|
| `status.template.md` | Development Phases | Always — implementation checkboxes |
| `roadmap.template.md` | Future Scope | Always — post-MVP features |
| `changelog.template.md` | References | When project has version history |

## Usage

Templates are referenced by the spec-writing skill during generation. The agent reads relevant templates based on project type and interview answers, then adapts the structure to fit the specific project.

**Key principle**: SPEC.md is always complete and self-sufficient. Templates help maintain consistent structure across generated specs.
