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
| [project-spec](./plugins/project-spec) | Generate project, feature, and design specifications with a single `/spec` command | 4.0.0 |
| [suno-composer](./plugins/suno-composer) | Compose Suno AI songs with adaptive preferences, dual-mode workflows, and narrative style prompts | 5.4.1 |

## Plugins

### project-spec

Generate project, feature, and design specifications with a single `/spec` command. Optimized for Opus 4.6 adaptive thinking.

**Core Principle:** SPEC.md = things you READ, SPEC/ = things you LOOK UP

**Command:**

| Command | Description | Output |
|---------|-------------|--------|
| `/project-spec:spec` | Project specification | `SPEC.md` + `CLAUDE.md` |
| `/project-spec:spec feature [name]` | Feature specification | `FEATURE_SPEC.md` or `SPEC/FEATURE-*.md` |
| `/project-spec:spec design [style]` | Design system specification | `DESIGN_SPEC.md` or `SPEC/DESIGN-SYSTEM.md` |
| `/project-spec:spec design:overhaul` | Design audit + redesign | Same + migration checklist |

**Features:**
- Single `/spec` command with argument-based routing for all spec types
- Opinionated recommendations with user override
- Codebase-aware interview — auto-detects answers from lockfiles, configs, and dependencies
- Gap analysis compares SPEC.md against codebase implementation
- Design audit for first-principles redesigns
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

# Feature planning
/project-spec:spec feature comments  # Plan a feature

# Design system
/project-spec:spec design modern     # Clean, subtle preset

# Design overhaul
/project-spec:spec design:overhaul   # Audit + redesign
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
| `/suno like <artist>` | Compose using artist profile (29 artists) |
| `/suno <tier>` | Use J-pop tier preset (anisong, surface, mainstream, doujin, legacy) |
| `/suno:album [concept]` | Create thematically coherent albums/EPs |
| `/suno:variation` | Generate acoustic, remix, stripped versions |
| `/suno:extend` | Create song continuations (sequel, prequel, response) |

**Features:**
- **Dual-mode workflow** - Vision-first (Claude proposes) or guided (step-by-step wizard)
- **Adaptive preferences** - First-run wizard + session reflection learns your taste
- **Narrative style prompts** - Arrangement descriptions that Suno v5 interprets as instructions
- **Reference-based composition** - 29 artist profiles (YOASOBI, Ado, Aimer, etc.)
- **J-pop tier presets** - anisong, surface, mainstream, doujin, legacy
- Preview-first workflow (confirm concepts before full generation)
- Sparse tagging for proper dynamics (3-4 technique tags at inflection points)
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

# With artist reference
/suno like YOASOBI about finding hope

# With tier preset
/suno anisong about never giving up

# Album mode
/suno:album summer memories

# Variations
/suno:variation
```

See [plugin documentation](./plugins/suno-composer/README.md) for details.

## License

MIT
