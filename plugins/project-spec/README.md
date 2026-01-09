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

## Features

### `/spec` Command

Interactive command that guides you through project planning:

```bash
# Full interview process
/spec

# Quick-start with project type template
/spec web-app
/spec cli
/spec api
/spec library
```

### `/feature` Command

Plan new features for existing projects:

```bash
# Full feature interview
/feature

# Start with feature name
/feature user-authentication
/feature comments
/feature export-to-pdf
```

Generates `feature_spec.md` with:
- Requirements (must-have, nice-to-have, out of scope)
- Technical design (components, API, database changes)
- Implementation plan (step-by-step tasks)
- Edge cases and testing strategy

### `/design` Command

Dedicated design system interview for frontend projects:

```bash
# Full design interview
/design

# Quick-start with style preset
/design modern    # Clean, subtle, rounded
/design minimal   # Sparse, typography-focused
/design bold      # Vibrant, high contrast
```

Generates `design_spec.md` with:
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

Gently suggests running `/spec` when you start describing a new project.

### Context7 Integration

Fetches up-to-date documentation for your chosen tech stack.

### feature-dev Integration

The generated specs work with the `feature-dev` skill:

1. Run `/spec` to define project requirements
2. Run `/feature` to plan a specific feature
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
/spec web-app
```

### New Feature (existing project)
```bash
/feature task-comments
```

### Design System
```bash
/design modern
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

| Command | Output | Purpose |
|---------|--------|---------|
| `/spec` | `project_spec.md` | Full project specification |
| `/feature` | `feature_spec.md` | Feature implementation plan |
| `/design` | `design_spec.md` | Design system documentation |

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
