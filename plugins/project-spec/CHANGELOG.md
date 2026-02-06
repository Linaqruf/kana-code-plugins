# Changelog

All notable changes to project-spec will be documented in this file.

## [4.0.0] - 2026-02-06

### Breaking Changes
- **Consolidated to single `/spec-writing` command** — All spec types accessible via arguments
  - `/spec-writing feature [name]` replaces `/feature`
  - `/spec-writing design [style]` replaces `/design`
  - `/spec-writing design:overhaul` replaces `/design:overhaul`
  - `/sync` removed — use `/spec-writing` to re-audit project against codebase
- **SKILL.md is the authoritative source** for all shared methodology — commands reference it instead of duplicating
- **Command file renamed** from `spec.md` to `spec-writing.md` — aligns with skill directory name and official plugin conventions
- **`name` and `version` removed from command frontmatter** — follows official plugin conventions (derived from filename)

### Added
- **Spec type routing** in SKILL.md — Unified type detection and flow dispatch table
- **Gap Analysis section** in SKILL.md — Core algorithm for comparing SPEC.md vs codebase
- **Design Audit section** in SKILL.md — Audit workflow for design system overhauls
- **`references/spec-type-flows.md`** — Detailed workflows for feature, design, and overhaul flows
- **`references/codebase-analysis.md`** — Lookup reference for project detection and framework scanning
- **Intent detection** via skill auto-trigger — Routes natural language to appropriate spec type
- **Smart Batching Rules** — 10-turn interview table with explicit skip conditions per turn
- **Codebase-Aware Skipping** — Auto-detect answers from lockfiles, package.json, config files (8 signals)
- **Auto-Detect Project Type** — Infer CLI/web-app/API/library from codebase signals (7 detection rules)
- **Security section** in output template — Auth flow diagram, input validation checklist, sensitive data protection table
- **Error Handling Strategy section** — Structured error format, error code table, error boundary strategy, retry logic
- **Monitoring & Observability section** — Error tracking, logging levels, health checks, performance monitoring
- **State Diagrams** in System Maps — Entity lifecycle visualization for complex status flows
- **Algorithm Specifications** — Explicit rules for non-obvious logic (type inference, search ranking, metadata extraction)
- **Zod validation schemas** alongside TypeScript interfaces in Data Models section
- **Prompt Principles section** in SKILL.md — Adaptive thinking markers and literal interpretation rules
- **Constraints section** in SKILL.md — Non-negotiable rules extracted and centralized
- **Framework Detection table** — Maps package.json dependencies to framework identification
- **LICENSE** file — MIT license
- **`templates/README.md`** — Template index documenting section and supplement templates

### Changed
- **Opus 4.6 optimization** — Restructured all prompts for adaptive thinking and literal interpretation
- **SKILL.md is now the single source of truth** — Command references the skill
- **`/spec-writing` command** handles project, feature, design, and overhaul via argument parsing
- **Tightened prompt language** — Imperative mood, explicit conditions, no hedging
- **Enhanced codebase analysis** — More file patterns for framework detection and deep scanning
- **interview-questions.md** restructured — organized by interview turns with AskUserQuestion format, conditional follow-ups, quick-start compressed flows
- **output-template.md** enhanced — security, error handling, monitoring sections; alternatives column; testability examples
- **All 5 example specs upgraded** — security sections, state diagrams, algorithm specs, validation schemas, bundle size strategies
- **Output quality guidelines** tightened: testable acceptance criteria, Zod validation, state diagrams for entities with lifecycle
- **Updated model IDs** in SDK examples and templates
- **Fixed CLAUDE.md.template** — Removed stale Quick/SPEC/DEEP mode references from v2.0

### Removed
- **`/feature` command** — Use `/spec-writing feature` instead
- **`/design` command** — Use `/spec-writing design` instead
- **`/design:overhaul` command** — Use `/spec-writing design:overhaul` instead
- **`/sync` command** — Deprecated; re-audit via `/spec-writing` is more reliable than git-diff inference
- **`spec-writer` agent** — Removed; interactive interview workflow is a bad fit for autonomous subagents. Skill auto-trigger handles natural language routing.
- **Hooks** (`hooks/hooks.json`) — Auto-suggestion and feature planning hooks removed; skill description triggers are sufficient

## [3.1.0] - 2026-01-19

### Added
- **Existing repository detection** in `/spec` command
  - Detects if running on existing codebase (package.json, src/, configs)
  - Asks: "Document existing project", "Plan new project", or "Both"
  - Document mode: scans codebase, extracts tech stack, generates spec from reality
  - Both mode: documents existing + continues with interview for new features
- **Gap analysis** in `/feature` command
  - Compares SPEC.md requirements vs actual codebase
  - Identifies: specced but not implemented, implemented but not specced
  - Suggests features based on patterns (e.g., "You have auth but no 2FA")
  - Presents options for user to choose which feature to spec
- **`/project-spec:design:overhaul` command** - First-principles design redesign
  - Audits current design (styles, components, tokens)
  - Identifies inconsistencies and outdated patterns
  - Fresh interview: "Forget current implementation. What do you want?"
  - Generates new design system with migration checklist
  - Includes deprecation warnings and phase-by-phase update plan

### Changed
- `/spec` version bumped to 3.1.0
- `/feature` version bumped to 3.1.0
- Section numbers updated in commands to accommodate new steps

## [3.0.0] - 2026-01-19

### Changed
- **Single adaptive flow** - Removed Quick/SPEC/DEEP mode selection
  - SPEC.md is always the core, complete specification
  - SPEC/ files are now optional supplements for reference material only
  - Interview offers supplements mid-flow when hitting reference-heavy topics
- **Core principle**: SPEC.md = things you READ, SPEC/ = things you LOOK UP
- **Opinionated recommendations** baked into interview
  - Lead with recommended option + rationale
  - User can always override
  - Examples: bun over npm, Drizzle for ORM, PostgreSQL for database
- **Trigger-based references** in SPEC.md and CLAUDE.md
  - Format: `→ When implementing API endpoints: SPEC/api-reference.md`
- **System Maps section** added to SPEC.md template
  - Architecture diagrams (ASCII)
  - Data model relations
  - User flow diagrams
  - Wireframes

### Added
- **`/project-spec:sync` command** - Git-aware spec drift detection
  - Detects when spec was last updated
  - Analyzes commits since then
  - Maps file changes to spec sections
  - Suggests targeted updates
  - Arguments: `spec`, `design`, `feature`, or none (all)

### Removed
- Quick/SPEC/DEEP mode selection
- `references/interview-questions-deep.md` (consolidated into main file)
- Complex SPEC/ folder structure with numbered files

### Breaking Changes
- No more mode selection at start of `/spec` command
- SPEC/ folder is now optional, not the default for complex projects
- Interview structure simplified (15-20 questions, always grouped)

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

## [1.0.2] - 2026-01-09

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

## [1.0.1] - 2026-01-08

### Added
- Initial release with `/spec` command
- spec-writer agent for autonomous planning
- Interview workflow with 3 phases (Product, Technical, Constraints)
- Context7 integration for tech stack documentation
- Examples: web-app-spec.md, cli-spec.md, api-spec.md
- Auto-suggestion hook for new projects
