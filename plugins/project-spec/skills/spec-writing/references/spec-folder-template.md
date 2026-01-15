# SPEC/ Folder Structure

Adaptive documentation structure. Numbers are for ordering only - extend as needed.

## Design Principles

1. **Adaptive** - File count depends on project complexity
2. **Extensible** - Add new files with next available number
3. **Project-specific** - Only create files that make sense for the project
4. **Flat structure** - All files at root level, no subdirectories

## Foundation Files (Always Create)

These 6 files form the core of any SPEC/ folder:

| # | File | Purpose |
|---|------|---------|
| 00 | `INDEX.md` | Navigation, TOC, quick reference |
| 01 | `OVERVIEW.md` | Problem statement, users, goals, success criteria |
| 02 | `ARCHITECTURE.md` | Tech stack, system design, key decisions |
| 03 | `STATUS.md` | Feature completion, implementation progress |
| 04 | `ROADMAP.md` | Future phases, backlog, planning |
| 05 | `CHANGELOG.md` | Completed work, version history |

## Conditional Files

Create based on project characteristics. Use next available number.

### If Has Frontend (Web/Mobile/Desktop UI)

| File | Purpose |
|------|---------|
| `XX-FRONTEND.md` | Framework, state management, routing |
| `XX-DESIGN-SYSTEM.md` | Colors, typography, spacing tokens |
| `XX-COMPONENTS.md` | Component inventory, patterns |
| `XX-SCREENS.md` | Page layouts, user flows |

### If Has Backend (Server/API)

| File | Purpose |
|------|---------|
| `XX-BACKEND.md` | Framework, services, runtime |
| `XX-API-REFERENCE.md` | Endpoints, schemas, examples |
| `XX-DATA-MODELS.md` | Database schema, relationships |

### If Is CLI Tool

| File | Purpose |
|------|---------|
| `XX-CLI-REFERENCE.md` | Commands, flags, usage examples |

### If Handles Sensitive Data

| File | Purpose |
|------|---------|
| `XX-SECURITY.md` | Auth, authorization, compliance |

### If Needs Configuration Docs

| File | Purpose |
|------|---------|
| `XX-CONFIGURATION.md` | Environment variables, settings |
| `XX-TROUBLESHOOTING.md` | Common issues, solutions |

### Feature-Specific (As Needed)

| File | Purpose |
|------|---------|
| `XX-[FEATURE-NAME].md` | Dedicated docs for complex features |
| `XX-INTEGRATIONS.md` | Third-party service integrations |
| `XX-TESTING.md` | Test strategy, coverage |
| `XX-DEPLOYMENT.md` | Deploy process, environments |

## Examples

### Web Application (Full Stack)

```
SPEC/
├── 00-INDEX.md
├── 01-OVERVIEW.md
├── 02-ARCHITECTURE.md
├── 03-FRONTEND.md
├── 04-BACKEND.md
├── 05-DESIGN-SYSTEM.md
├── 06-API-REFERENCE.md
├── 07-DATA-MODELS.md
├── 08-SECURITY.md
├── 09-STATUS.md
├── 10-ROADMAP.md
└── 11-CHANGELOG.md
```

### CLI Tool

```
SPEC/
├── 00-INDEX.md
├── 01-OVERVIEW.md
├── 02-ARCHITECTURE.md
├── 03-CLI-REFERENCE.md
├── 04-CONFIGURATION.md
├── 05-STATUS.md
├── 06-ROADMAP.md
└── 07-CHANGELOG.md
```

### API Service

```
SPEC/
├── 00-INDEX.md
├── 01-OVERVIEW.md
├── 02-ARCHITECTURE.md
├── 03-API-REFERENCE.md
├── 04-DATA-MODELS.md
├── 05-SECURITY.md
├── 06-STATUS.md
├── 07-ROADMAP.md
└── 08-CHANGELOG.md
```

### Library/Package

```
SPEC/
├── 00-INDEX.md
├── 01-OVERVIEW.md
├── 02-ARCHITECTURE.md
├── 03-API-REFERENCE.md
├── 04-STATUS.md
├── 05-ROADMAP.md
└── 06-CHANGELOG.md
```

## Numbering Convention

- **00-09**: Foundation and core docs
- **10-19**: Technical reference (API, CLI, data models)
- **20-29**: Design and UI docs
- **30+**: Feature-specific and extended docs

This is a guideline, not a requirement. The key is consistency within each project.

## Extending Later

Add new documentation anytime:

```bash
# Add a complex feature spec
echo "# Authentication" > SPEC/12-AUTHENTICATION.md

# Add research
echo "# Competitive Analysis" > SPEC/13-ANALYSIS.md

# Add deployment docs
echo "# Deployment" > SPEC/14-DEPLOYMENT.md
```

## File Header Template

Every SPEC file should start with:

```markdown
# [Title]

> [One-line description]

**Last Updated**: YYYY-MM-DD

## Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

---

[Content...]
```

## Cross-References

Use relative links:

```markdown
See [Architecture](02-ARCHITECTURE.md) for tech stack.
See [API Reference](06-API-REFERENCE.md#endpoints) for endpoints.
```

## Integration with CLAUDE.md

The generated CLAUDE.md references SPEC/:

```markdown
## Reflective Behavior

**When to check SPEC/**: Only when CLAUDE.md context insufficient.
Read `SPEC/00-INDEX.md` first, then specific files.

**Update specs proactively**:
- After work: Update `SPEC/XX-STATUS.md`
- After phase: Update `SPEC/XX-CHANGELOG.md`
- New findings: Add to relevant SPEC file
```
