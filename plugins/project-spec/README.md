# project-spec

A Claude Code plugin that generates comprehensive specification documents through interactive interviews - for projects, features, and design systems.

## Overview

**project-spec** helps you front-load critical decisions by interviewing you about your vision, requirements, and technical preferences, then generating structured specification documents that serve as development guidelines.

### Why Use This?

- **Reduce ambiguity** - Document decisions before coding starts
- **Prevent scope creep** - Clear MVP vs future scope boundaries
- **Save time** - Front-load decisions instead of discovering them mid-development
- **Better AI assistance** - Claude Code can reference specs throughout development
- **Sync with reality** - Git-aware `/sync` command detects spec drift

## Core Principle

**SPEC.md is always complete. SPEC/ files are optional lookup references.**

- **SPEC.md** = Things you READ (narrative, decisions, requirements)
- **SPEC/*.md** = Things you LOOK UP (schemas, SDK patterns, external APIs)

## Commands

### `/project-spec:spec` - Project Specification

Interactive command that guides you through project planning:

```bash
# Full interview process
/project-spec:spec

# Quick-start with project type template
/project-spec:spec web-app
/project-spec:spec cli
/project-spec:spec api
/project-spec:spec library
```

**Existing codebase support:**

When run on an existing project, the command detects the codebase and asks:

```
I see this is an existing project. What would you like to do?

- A) Document existing project - Analyze codebase and generate spec from what exists
- B) Plan new project - Start fresh with interview-based planning
- C) Both - Document existing + plan new features
```

**Output:**
- `SPEC.md` - Complete project specification
- `CLAUDE.md` - Agent-optimized reference
- `SPEC/*.md` - Optional supplements (if you agreed during interview)

### `/project-spec:feature` - Feature Specification

Plan new features for existing projects:

```bash
# Full feature interview
/project-spec:feature

# Start with feature name
/project-spec:feature user-authentication
/project-spec:feature comments
/project-spec:feature export-to-pdf
```

**Gap analysis:**

When SPEC.md exists, the command performs gap analysis:

```markdown
Gap Analysis:

Specced but not implemented:
- [ ] Password reset (SPEC.md -> Auth section)
- [ ] Export to PDF (SPEC.md -> Features)

Implemented but not specced:
- OAuth login (found in src/auth/oauth.ts)
- Rate limiting (found in middleware)

Suggested features based on patterns:
- You have auth but no 2FA - want to add?
- You have projects but no project templates
```

**Adaptive output:**
- If `SPEC/` folder exists: writes to `SPEC/FEATURE-[NAME].md`
- Otherwise: writes to `FEATURE_SPEC.md`

### `/project-spec:design` - Design System Specification

Dedicated design system interview for frontend projects:

```bash
# Full design interview
/project-spec:design

# Quick-start with style preset
/project-spec:design modern    # Clean, subtle, rounded
/project-spec:design minimal   # Sparse, typography-focused
/project-spec:design bold      # Vibrant, high contrast
```

**Adaptive output:**
- If `SPEC/` folder exists: writes to `SPEC/DESIGN-SYSTEM.md`
- Otherwise: writes to `DESIGN_SPEC.md`

### `/project-spec:design:overhaul` - Design System Overhaul

First-principles design system redesign:

```bash
/project-spec:design:overhaul
```

**What it does:**

1. **Audits current design** - Scans styles, components, tokens and identifies inconsistencies
2. **First-principles interview** - "Forget current implementation. What do you actually want?"
3. **Generates new design system** - Fresh decisions with migration notes

**Output includes:**
- New design system specification
- Migration checklist (old -> new)
- Deprecation warnings for old patterns
- Phase-by-phase update plan

Use when:
- Current design feels inconsistent or outdated
- Major visual rebrand needed
- Switching component libraries
- Want to rethink design from scratch

### `/project-spec:sync` - Sync Specification with Codebase

Git-aware command to detect and resolve spec drift:

```bash
/project-spec:sync spec      # Sync SPEC.md
/project-spec:sync design    # Sync design spec
/project-spec:sync feature   # Sync feature specs
/project-spec:sync           # Sync all specs
```

**How it works:**
1. Finds when spec was last updated (via git)
2. Analyzes commits since then
3. Maps file changes to spec sections
4. Suggests targeted updates

## Interview Style

The plugin uses **opinionated recommendations** with user override:

```
Which package manager?

- A) bun (Recommended) - Fastest, built-in test runner
- B) pnpm - Fast, strict deps, good for monorepos
- C) npm - Universal compatibility
- D) Other
```

Principles:
- Lead with recommended option + rationale
- Present 2-3 alternatives with tradeoffs
- User can always override
- YAGNI - ruthlessly simplify

## Optional Supplements

During the interview, when hitting reference-heavy topics, you'll be asked:

> "Your API has many endpoints. How should I document them?"
> - A) Inline in SPEC.md
> - B) Create SPEC/api-reference.md as a lookup file

Supplements are created only when:
- Content is truly reference material (schemas, tables, examples)
- External dependencies need documentation (SDK patterns, library usage)

## CLAUDE.md Generation

The generated `CLAUDE.md` is agent-optimized:

```markdown
# [Project Name]

[One-line description]

## Spec Reference

Primary spec: `SPEC.md`

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using Anthropic SDK: `SPEC/sdk-patterns.md`

## Key Constraints

- [Critical constraint surfaced from spec]
- [Out of scope reminder]

## Commands

- `bun run dev` - Start development
- `bun run test` - Run tests
```

## spec-writer Agent

Autonomous agent that triggers when you need planning help:

- "Help me plan this project"
- "I need to write a spec for my app"
- "Let's document the requirements"
- "Plan this feature before I build it"

## Installation

### Via Marketplace (Recommended)

```bash
# Add the marketplace
/plugin marketplace add Linaqruf/cc-plugins

# Install the plugin
/plugin install project-spec@cc-plugins
```

### Via Plugin Directory (Development)

```bash
claude --plugin-dir /path/to/cc-plugins/plugins/project-spec
```

## Usage Examples

### New Project
```bash
/project-spec:spec web-app
```

### New Feature (existing project)
```bash
/project-spec:feature task-comments
```

### Design System
```bash
/project-spec:design modern
```

### Sync After Development
```bash
/project-spec:sync spec
```

## Output Files

| Command | Primary Output | Optional Supplements |
|---------|----------------|----------------------|
| `/spec` | `SPEC.md` + `CLAUDE.md` | `SPEC/api-reference.md`, `SPEC/data-models.md`, `SPEC/sdk-patterns.md` |
| `/feature` | `FEATURE_SPEC.md` or `SPEC/FEATURE-*.md` | - |
| `/design` | `DESIGN_SPEC.md` or `SPEC/DESIGN-SYSTEM.md` | - |

## Examples

Example specifications included:

- `examples/web-app-spec.md` - TaskFlow task manager
- `examples/cli-spec.md` - envcheck CLI tool
- `examples/api-spec.md` - BookmarkAPI service
- `examples/library-spec.md` - timeparse library
- `examples/design-spec.md` - TaskFlow design system
- `examples/feature-spec.md` - Task comments feature

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Command | `commands/spec.md` | `/spec` command with existing repo detection |
| Command | `commands/feature.md` | `/feature` command with gap analysis |
| Command | `commands/design.md` | `/design` command |
| Command | `commands/design-overhaul.md` | `/design:overhaul` command |
| Command | `commands/sync.md` | `/sync` command |
| Skill | `skills/spec-writing/SKILL.md` | Interview templates and guidance |
| Agent | `agents/spec-writer.md` | Autonomous planning agent |

## Integration

### feature-dev Integration

The generated specs work with the `feature-dev` skill:

1. Run `/project-spec:spec` to define project requirements
2. Run `/project-spec:feature` to plan a specific feature
3. Use `code-explorer` to analyze existing patterns
4. Use `code-architect` to design implementation
5. Implement following the plan
6. Use `code-reviewer` to verify
7. Run `/project-spec:sync` to update specs

### frontend-design Integration

The generated design spec works with the `frontend-design` skill for implementing components.

### Context7 Integration

Fetches up-to-date documentation for your chosen tech stack.

## Configuration

No configuration required. The plugin works out of the box.

## License

MIT

---

*Built with the plugin-dev plugin for Claude Code*
