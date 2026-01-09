# project-spec

A Claude Code plugin that generates comprehensive project specification documents through interactive interviews before you start building.

## Overview

**project-spec** helps you front-load critical decisions by interviewing you about your project vision, requirements, and technical preferences, then generating a structured `project_spec.md` that serves as a development guideline.

### Why Use This?

- **Reduce ambiguity** - Document decisions before coding starts
- **Prevent scope creep** - Clear MVP vs future scope boundaries
- **Save time** - Front-load decisions instead of discovering them mid-development
- **Better AI assistance** - Claude Code can reference the spec throughout development
- **Design consistency** - Document design systems for frontend projects

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

### `/design` Command

Dedicated design system interview for frontend projects:

```bash
# Full design interview
/design

# Quick-start with style preset
/design modern    # Clean, subtle, rounded
/design minimal   # Sparse, typography-focused
/design bold      # Vibrant, high contrast
/design custom    # Full interview
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
- "Create a design document"

### Auto-Suggestion Hook

Gently suggests running `/spec` when you start describing a new project:

> Consider running `/spec` first to plan your project and create a specification document.

### Context7 Integration

Fetches up-to-date documentation for your chosen tech stack to include best practices and setup guidance in your spec.

### frontend-design Integration

The generated design spec works with the `frontend-design` skill:

1. Run `/spec` to define project requirements
2. Run `/design` to define visual design system
3. Use `frontend-design` skill to implement components

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

### Basic Usage

1. Navigate to your project directory (or create a new one)
2. Run `/spec`
3. Answer the interview questions
4. Review the generated `project_spec.md`

### With Project Type

Skip some questions by specifying your project type:

```bash
/spec web-app    # Web application (frontend + backend)
/spec cli        # Command-line tool
/spec api        # REST API service
/spec library    # Reusable library/package
```

### Interview Flow

The command guides you through phases:

**Phase 1: Product Requirements**
- Problem statement
- Target users
- Core features (MVP)
- Future scope
- Inspirations

**Phase 2: Technical Design**
- Tech stack preferences
- Deployment target
- Integrations
- Performance/security needs

**Phase 3: Constraints**
- Team size
- Existing codebase
- Budget constraints

**Phase 4: Design & UX** (for frontend projects)
- Visual identity (colors, typography)
- Component library preference
- Layout and responsiveness
- Accessibility requirements
- Interaction patterns

## Output

### project_spec.md

The generated `project_spec.md` includes:

```markdown
# Project Specification: [Name]

## Overview
- Problem Statement
- Solution
- Target Users
- Success Criteria

## Product Requirements
- Core Features (MVP)
- Future Scope
- Out of Scope
- User Stories

## Technical Architecture
- Tech Stack
- System Design
- Data Models
- API Endpoints

## Design System (for web apps)
- Visual Identity
- Responsive Breakpoints
- Component Library
- Accessibility Requirements

## File Structure
## Dependencies
## Environment Variables
## Development Phases
## Open Questions
## References
```

### design_spec.md

The `/design` command generates a detailed design specification:

```markdown
# Design Specification: [Name]

## Brand Identity
- Color Palette
- Typography Scale
- Spacing System

## Component Library
- Selected library
- Core components
- Component states

## Layouts
- Page templates
- Responsive breakpoints

## Accessibility
- WCAG level
- Focus management
- Screen reader support

## Interaction Patterns
- Animations
- Loading states
- Error handling UX
```

## Examples

Example specifications are included in the plugin:

- `skills/spec-writing/examples/web-app-spec.md` - TaskFlow task manager
- `skills/spec-writing/examples/cli-spec.md` - envcheck CLI tool
- `skills/spec-writing/examples/api-spec.md` - BookmarkAPI service
- `skills/spec-writing/examples/library-spec.md` - timeparse library
- `skills/spec-writing/examples/design-spec.md` - TaskFlow design system

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Command | `commands/spec.md` | `/spec` command |
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
