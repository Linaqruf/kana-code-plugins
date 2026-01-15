# project-spec

A Claude Code plugin that generates comprehensive specification documents through interactive interviews - for projects, features, and design systems.

## Overview

**project-spec** helps you front-load critical decisions by interviewing you about your vision, requirements, and technical preferences, then generating structured specification documents that serve as development guidelines.

### Why Use This?

- **Reduce ambiguity** - Document decisions before coding starts
- **Prevent scope creep** - Clear MVP vs future scope boundaries
- **Save time** - Front-load decisions instead of discovering them mid-development
- **Better AI assistance** - Claude Code can reference specs throughout development
- **Design consistency** - Document design systems for frontend projects
- **Feature planning** - Plan features before implementation
- **Reflective behavior** - Auto-generated CLAUDE.md keeps specs and code in sync

## Three Output Modes

| Mode | Output | Interview | Use Case |
|------|--------|-----------|----------|
| **Quick** | `SPEC.md` | Grouped (~15 questions) | Simple apps, prototypes |
| **SPEC/** | `SPEC/` folder | Hybrid (~40 questions) | Production apps |
| **DEEP** | `SPEC/` folder | Socratic (~50 questions) | Complex systems |

## Features

### `/project-spec:spec` Command

Interactive command that guides you through project planning:

```bash
# Full interview process (asks which mode)
/project-spec:spec

# Quick-start with project type template
/project-spec:spec web-app
/project-spec:spec cli
/project-spec:spec api
/project-spec:spec library
```

**Output modes:**
- **Quick**: Single `SPEC.md` file (~6-8 turns)
- **SPEC/**: Adaptive folder structure with validation checkpoints (~15 turns)
- **DEEP**: Full Socratic interview, one question at a time (~50+ turns)

### `/project-spec:feature` Command

Plan new features for existing projects:

```bash
# Full feature interview
/project-spec:feature

# Start with feature name
/project-spec:feature user-authentication
/project-spec:feature comments
/project-spec:feature export-to-pdf
```

**Adaptive output:**
- If `SPEC/` folder exists: writes to `SPEC/XX-FEATURE-[NAME].md`
- Otherwise: writes to `FEATURE_SPEC.md`

Generates feature spec with:
- Requirements (must-have, nice-to-have, out of scope)
- Technical design (components, API, database changes)
- Implementation plan (step-by-step tasks)
- Edge cases and testing strategy

### `/project-spec:design` Command

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
- If `SPEC/` folder exists: writes to `SPEC/XX-DESIGN-SYSTEM.md`
- Otherwise: writes to `DESIGN_SPEC.md`

Generates design spec with:
- Color palette and typography
- Component library selection
- Responsive breakpoints
- Accessibility requirements
- Interaction patterns

### spec-writer Agent

Autonomous agent that triggers when you need planning help:

- "Help me plan this project"
- "I need to write a spec for my app"
- "Let's document the requirements"
- "Plan this feature before I build it"

### Auto-Suggestion Hook

The plugin includes hooks (`hooks/hooks.json`) that gently suggest running `/spec` or `/feature` when you:
- Start describing a new project to build
- Ask to add a new feature to an existing project

### Context7 Integration

Fetches up-to-date documentation for your chosen tech stack.

### feature-dev Integration

The generated specs work with the `feature-dev` skill:

1. Run `/project-spec:spec` to define project requirements
2. Run `/project-spec:feature` to plan a specific feature
3. Use `code-explorer` to analyze existing patterns
4. Use `code-architect` to design implementation
5. Implement following the plan
6. Use `code-reviewer` to verify

### frontend-design Integration

The generated design spec works with the `frontend-design` skill for implementing components.

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

## Usage

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

### Interview Flow

**Project Spec** guides you through:
- Product Requirements (problem, users, features)
- Technical Design (stack, deployment, integrations)
- Constraints (team, budget, existing code)
- Design & UX (for frontend projects)

**Feature Spec** guides you through:
- Feature Definition (what, why, how)
- Scope & Requirements (must-have, out of scope)
- Technical Approach (components, API, database)
- Edge Cases & Testing

## Output Files

### Quick Mode (Single File)

| Command | Output | Purpose |
|---------|--------|---------|
| `/project-spec:spec` | `SPEC.md` + `CLAUDE.md` | Full project specification |
| `/project-spec:feature` | `FEATURE_SPEC.md` | Feature implementation plan |
| `/project-spec:design` | `DESIGN_SPEC.md` | Design system documentation |

### SPEC/ Mode (Folder Structure)

Adaptive folder structure with foundation + conditional files:

```
SPEC/
├── 00-INDEX.md           # Navigation, TOC
├── 01-OVERVIEW.md        # Problem, users, goals
├── 02-ARCHITECTURE.md    # Tech stack, system design
├── XX-FRONTEND.md        # (if has UI)
├── XX-BACKEND.md         # (if has server)
├── XX-DESIGN-SYSTEM.md   # (if needs design tokens)
├── XX-API-REFERENCE.md   # (if has API)
├── XX-CLI-REFERENCE.md   # (if CLI)
├── XX-DATA-MODELS.md     # (if database)
├── XX-SECURITY.md        # (if sensitive data)
├── XX-STATUS.md          # Feature progress
├── XX-ROADMAP.md         # Future plans
└── XX-CHANGELOG.md       # Completed work
```

Plus auto-generated `CLAUDE.md` with reflective behavior.

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
| Command | `commands/spec.md` | `/spec` command |
| Command | `commands/feature.md` | `/feature` command |
| Command | `commands/design.md` | `/design` command |
| Skill | `skills/spec-writing/SKILL.md` | Interview templates and guidance |
| Agent | `agents/spec-writer.md` | Autonomous planning agent |
| Hook | `hooks/hooks.json` | Auto-suggestion for new projects |

## Configuration

No configuration required. The plugin works out of the box.

### Optional: Disable Hook

If you don't want auto-suggestions, remove or rename `hooks/hooks.json`.

## License

MIT

---

*Built with the plugin-dev plugin for Claude Code*
