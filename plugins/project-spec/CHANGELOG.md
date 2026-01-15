# Changelog

All notable changes to project-spec will be documented in this file.

## [2.0.0] - 2026-01-15

### Added
- **Three output modes**: Quick, SPEC/, and DEEP
  - **Quick**: Single `SPEC.md` file, grouped interview (~15 questions, ~6-8 turns)
  - **SPEC/**: Adaptive folder structure, hybrid interview (~40 questions, ~15 turns)
  - **DEEP**: Full Socratic interview, one question at a time (~50 questions, ~50+ turns)
- **Adaptive SPEC/ folder structure** (UPPERCASE filenames)
  - Foundation files (always): `00-INDEX.md`, `01-OVERVIEW.md`, `02-ARCHITECTURE.md`, `XX-STATUS.md`, `XX-ROADMAP.md`, `XX-CHANGELOG.md`
  - Conditional files (based on project): `XX-FRONTEND.md`, `XX-BACKEND.md`, `XX-DESIGN-SYSTEM.md`, `XX-API-REFERENCE.md`, `XX-CLI-REFERENCE.md`, `XX-DATA-MODELS.md`, `XX-SECURITY.md`, `XX-CONFIGURATION.md`
  - Numbers for ordering only, not fixed positions
- **CLAUDE.md auto-generation** with reflective behavior
  - When to check SPEC/
  - Ask before assuming (use AskUserQuestion)
  - Update specs proactively
  - Self-correction (keep code and spec in sync)
- **Superpowers-inspired interview patterns**
  - Multiple choice inputs via AskUserQuestion options
  - 2-3 alternatives with tradeoffs for key decisions
  - Validation checkpoints (SPEC/ mode: 3 checkpoints, DEEP mode: per-file)
- **Extended interview questions** for SPEC/DEEP modes
  - 8-phase deep interview (Vision, Requirements, Architecture, Frontend, Backend, Security, Design, Process)
  - AskUserQuestion format examples with options
- **15 template files** for SPEC/ folder generation
  - Foundation: index, overview, architecture, status, roadmap, changelog
  - Conditional: frontend, backend, design-system, api-reference, cli-reference, data-models, security, configuration
  - CLAUDE.md template with tech-stack specific commands

### Changed
- **Renamed `project_spec.md` to `SPEC.md`** (more universal, backward compatible with `PROJECT_SPEC.md`)
- **All spec filenames now UPPERCASE** (`SPEC.md`, `FEATURE_SPEC.md`, `DESIGN_SPEC.md`, `SPEC/00-INDEX.md`, etc.)
- `/feature` command now adapts output location
  - If `SPEC/` exists: writes to `SPEC/XX-FEATURE-[NAME].md`
  - Otherwise: writes to `FEATURE_SPEC.md`
- `/design` command now adapts output location
  - If `SPEC/` exists: writes to `SPEC/XX-DESIGN-SYSTEM.md`
  - Otherwise: writes to `DESIGN_SPEC.md`
- spec-writer agent updated to support 3 modes
- SKILL.md updated with dual-mode documentation

### Breaking Changes
- Mode selection now required at start of `/spec` command
- SPEC/ folder structure is adaptive (not fixed 00-17)
- Output filenames changed to UPPERCASE (`SPEC.md` instead of `project_spec.md`)
- Still checks for `PROJECT_SPEC.md` for backward compatibility

## [1.0.3] - 2026-01-09

### Fixed
- Fix hooks.json format: use event-keyed object instead of array wrapper

## [1.0.2] - 2025-01-09

### Added
- `/design` command for design system specifications
  - Style presets: modern, minimal, bold, custom
  - Generates design_spec.md with colors, typography, components, accessibility
- `/feature` command for feature planning
  - Generates feature_spec.md with requirements, technical design, implementation plan
  - Integration with feature-dev skill (code-explorer, code-architect, code-reviewer)
- Design System section in project_spec.md template
  - Visual identity (colors, typography, spacing)
  - Responsive breakpoints
  - Component library selection
  - Accessibility requirements
  - Interaction patterns
- Feature planning hook for `/feature` suggestions
- New examples: library-spec.md, design-spec.md, feature-spec.md
- Error handling guidance in commands
- TodoWrite tool for tracking interview progress

### Changed
- Hook regex improved to reduce false positives (requires sentence-start patterns)
- Skill description trimmed for better display
- Updated keywords in plugin.json for discoverability

### Fixed
- Regex escaping in hooks.json (`\s` → `\\s`)
- Version sync between plugin.json and SKILL.md

## [1.0.1] - 2025-01-08

### Added
- Initial release with `/spec` command
- spec-writer agent for autonomous planning
- Interview workflow with 3 phases (Product, Technical, Constraints)
- Context7 integration for tech stack documentation
- Examples: web-app-spec.md, cli-spec.md, api-spec.md
- Auto-suggestion hook for new projects
