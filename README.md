# cc-plugins

A collection of Claude Code plugins

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add Linaqruf/cc-plugins
```

Then install any plugin:

```bash
/plugin install <plugin-name>@cc-plugins
```

## Available Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [project-spec](./plugins/project-spec) | Generate project specifications with SPEC.md as core and optional SPEC/ supplements | 3.1.0 |
| [suno-composer](./plugins/suno-composer) | Guided workflow for composing Suno AI songs with lyrics, style tags, and arrangements | 4.1.0 |

## Plugins

### project-spec

Generate project specifications with SPEC.md as the core file and optional SPEC/ supplements for reference material.

**Core Principle:** SPEC.md = things you READ, SPEC/ = things you LOOK UP

**Commands:**

| Command | Description | Output |
|---------|-------------|--------|
| `/project-spec:spec` | Project planning interview | `SPEC.md` + `CLAUDE.md` |
| `/project-spec:design` | Design system interview | `DESIGN_SPEC.md` |
| `/project-spec:feature` | Feature planning interview | `FEATURE_SPEC.md` |
| `/project-spec:sync` | Git-aware spec drift detection | Updates existing specs |

**Features:**
- Single adaptive flow (no mode selection needed)
- Opinionated recommendations with user override
- Optional SPEC/ supplements for reference material (API schemas, SDK patterns)
- Git-aware `/sync` command detects when specs are out of date
- System maps (architecture diagrams, data relations, user flows)
- `spec-writer` agent for autonomous planning
- Context7 integration for tech stack documentation

**Install:**
```bash
/plugin install project-spec@cc-plugins
```

**Usage:**
```bash
# Project specification
/project-spec:spec              # Full interview
/project-spec:spec web-app      # Quick-start for web apps

# Design system
/project-spec:design modern     # Clean, subtle preset

# Feature planning
/project-spec:feature comments  # Plan a feature

# Sync specs with codebase
/project-spec:sync spec         # Detect and fix drift
```

See [plugin documentation](./plugins/project-spec/README.md) for details.

---

### suno-composer

A guided workflow for composing Suno AI songs with professional songwriter techniques. Generates complete song specifications including lyrics, style tags, tempo, vocal arrangements, and more.

**Commands:**

| Command | Description |
|---------|-------------|
| `/suno` | Guided composition workflow |
| `/suno [theme]` | Start with a theme |
| `/suno:album [concept]` | Create thematically coherent albums/EPs |
| `/suno:variation` | Generate acoustic, remix, stripped versions |
| `/suno:extend` | Create song continuations (sequel, prequel, response) |

**Features:**
- Preview-first workflow (confirm concepts before full generation)
- Direct-to-file output (saves tokens, no console duplication)
- Selective tagging for proper dynamics (fixes pitch drift)
- Preset moods (upbeat, melancholic, energetic, dreamy, intense, chill)
- Batch generation of 1-10 songs per session
- Multi-genre support (J-pop, K-pop, EDM, Latin, rock, ballads)
- Album mode with journey arc patterns
- Variation mode (acoustic, remix, stripped, extended, cinematic)
- Extend mode (sequel, prequel, response, alternate POV, epilogue)
- Chrome integration for auto-filling Suno forms

**Install:**
```bash
/plugin install suno-composer@cc-plugins
```

**Usage:**
```bash
# Guided workflow
/suno

# With theme
/suno summer heartbreak ballad

# Album mode
/suno:album summer memories

# Variations
/suno:variation
```

See [plugin documentation](./plugins/suno-composer/README.md) for details.

## License

MIT
