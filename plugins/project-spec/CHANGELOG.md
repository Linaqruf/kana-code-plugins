# Changelog

All notable changes to project-spec will be documented in this file.

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
