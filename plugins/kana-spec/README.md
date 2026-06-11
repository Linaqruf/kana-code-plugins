# project-spec

A Claude Code plugin that generates comprehensive specification documents through interactive interviews — for projects, features, and design systems. Optimized for Opus 4.6 adaptive thinking and literal interpretation.

## Overview

**project-spec** helps you front-load critical decisions by interviewing you about your vision, requirements, and technical preferences, then generating structured specification documents that serve as development guidelines.

### Why Use This?

- **Reduce ambiguity** — Document decisions before coding starts
- **Prevent scope creep** — Clear MVP vs future scope boundaries
- **Save time** — Front-load decisions instead of discovering them mid-development
- **Better AI assistance** — Claude Code can reference specs throughout development
- **Single command** — One `/spec-writing` command handles projects, features, and design systems
- **Opus 4.6 optimized** — Prompts structured for adaptive thinking (deep reasoning on decisions, fast execution on procedures)

## Core Principle

**SPEC.md is always complete. SPEC/ files are optional lookup references.**

- **SPEC.md** = Things you READ (narrative, decisions, requirements)
- **SPEC/*.md** = Things you LOOK UP (schemas, SDK patterns, external APIs)

## Command

### `/project-spec:spec-writing` — Specification Generator

Single command with argument-based routing for all spec types:

```bash
# Project specification (full interview)
/project-spec:spec-writing
/project-spec:spec-writing web-app
/project-spec:spec-writing cli
/project-spec:spec-writing api
/project-spec:spec-writing library

# Feature specification (gap analysis + feature interview)
/project-spec:spec-writing feature
/project-spec:spec-writing feature user-authentication

# Design system specification
/project-spec:spec-writing design
/project-spec:spec-writing design modern
/project-spec:spec-writing design minimal
/project-spec:spec-writing design bold

# Design system overhaul (audit + redesign)
/project-spec:spec-writing design:overhaul
```

### Project Spec

When run on an existing project, the command detects the codebase and asks:

```
I see this is an existing project. What would you like to do?

- A) Document existing project — Analyze codebase and generate spec from what exists
- B) Plan new project — Start fresh with interview-based planning
- C) Both — Document existing + plan new features
```

**Output:**
- `SPEC.md` — Complete project specification
- `CLAUDE.md` — Agent-optimized reference
- `SPEC/*.md` — Optional supplements (if you agreed during interview)

### Feature Spec

When SPEC.md exists, performs **gap analysis**:

```markdown
Gap Analysis:

Specced but not implemented:
- [ ] Password reset (SPEC.md -> Auth section)
- [ ] Export to PDF (SPEC.md -> Features)

Implemented but not specced:
- OAuth login (found in src/auth/oauth.ts)
- Rate limiting (found in middleware)

Suggested features based on patterns:
- You have auth but no 2FA
- You have projects but no project templates
```

**Output:**
- If `SPEC/` folder exists: `SPEC/FEATURE-[NAME].md`
- Otherwise: `FEATURE_SPEC.md`

### Design Spec

Design system interview with optional style presets (`modern`, `minimal`, `bold`).

**Output:**
- If `SPEC/` folder exists: `SPEC/DESIGN-SYSTEM.md`
- Otherwise: `DESIGN_SPEC.md`

### Design Overhaul

First-principles design system redesign:

1. **Audits current design** — Scans styles, components, tokens and identifies inconsistencies
2. **First-principles interview** — "Forget current implementation. What do you actually want?"
3. **Generates new design system** — Fresh decisions with migration checklist and deprecation warnings

## Interview Style

The plugin uses **opinionated recommendations** with user override:

```
Which package manager?

- A) bun (Recommended) — Fastest, built-in test runner
- B) pnpm — Fast, strict deps, good for monorepos
- C) npm — Universal compatibility
- D) Other
```

Principles:
- Lead with recommended option + rationale
- Present 2-3 alternatives with tradeoffs
- User can always override
- YAGNI — ruthlessly simplify

## Architecture (v4.0.0)

```
skills/spec-writing/SKILL.md        <- Single source of truth (methodology)
    ↑ referenced by
commands/spec-writing.md            <- Command (routing + all flows)
```

## Installation

### Via Marketplace (Recommended)

```bash
# Add the marketplace
/plugin marketplace add Linaqruf/kana-code-plugins

# Install the plugin
/plugin install project-spec@kana-code-plugins
```

### Via Plugin Directory (Development)

```bash
claude --plugin-dir /path/to/kana-code-plugins/plugins/project-spec
```

## Output Files

| Argument | Primary Output | Optional Supplements |
|----------|----------------|----------------------|
| (none), `web-app`, `cli`, `api`, `library` | `SPEC.md` + `CLAUDE.md` | `SPEC/api-reference.md`, `SPEC/data-models.md`, `SPEC/sdk-patterns.md` |
| `feature [name]` | `FEATURE_SPEC.md` or `SPEC/FEATURE-*.md` | — |
| `design [style]` | `DESIGN_SPEC.md` or `SPEC/DESIGN-SYSTEM.md` | — |
| `design:overhaul` | `DESIGN_SPEC.md` or `SPEC/DESIGN-SYSTEM.md` + migration | — |

## Examples

Example specifications included:

- `skills/spec-writing/examples/web-app-spec.md` — TaskFlow task manager
- `skills/spec-writing/examples/cli-spec.md` — envcheck CLI tool
- `skills/spec-writing/examples/api-spec.md` — BookmarkAPI service
- `skills/spec-writing/examples/library-spec.md` — timeparse library
- `skills/spec-writing/examples/design-spec.md` — TaskFlow design system
- `skills/spec-writing/examples/design-overhaul-spec.md` — TaskFlow design overhaul with migration
- `skills/spec-writing/examples/feature-spec.md` — Task comments feature

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Skill | `skills/spec-writing/SKILL.md` | Authoritative methodology (single source of truth) |
| Command | `commands/spec-writing.md` | `/spec-writing` command with argument-based routing |

## Integration

### feature-dev Integration (if available)

1. Run `/project-spec:spec-writing` to define project requirements
2. Run `/project-spec:spec-writing feature` to plan a specific feature
3. Use `code-explorer` to analyze existing patterns
4. Use `code-architect` to design implementation
5. Implement following the plan
6. Use `code-reviewer` to verify

### frontend-design Integration (if available)

The generated design spec works with the `frontend-design` skill for implementing components.

### Context7 Integration (Optional)

Fetches up-to-date documentation for your chosen tech stack. Requires the [Context7 MCP server](https://context7.dev) to be configured. The plugin works without it — tech documentation steps are skipped gracefully.

## Configuration

No configuration required. The plugin works out of the box.

## License

MIT

---

*Built with the plugin-dev plugin for Claude Code*
