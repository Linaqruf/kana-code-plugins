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
| [project-spec](./plugins/project-spec) | Generate project, design, and feature specifications through interactive interviews | 1.0.2 |

## Plugins

### project-spec

Generate comprehensive specification documents through interactive interviews - for projects, features, and design systems.

**Commands:**

| Command | Description | Output |
|---------|-------------|--------|
| `/spec` | Project planning interview | `project_spec.md` |
| `/design` | Design system interview | `design_spec.md` |
| `/feature` | Feature planning interview | `feature_spec.md` |

**Features:**
- `/spec` command for guided project planning (web-app, cli, api, library)
- `/design` command for design system specs (colors, typography, components, a11y)
- `/feature` command for feature planning (requirements, technical design, implementation)
- `spec-writer` agent for autonomous planning assistance
- Auto-suggestion hooks for new projects and features
- Context7 integration for tech stack documentation
- Integration with `frontend-design` and `feature-dev` skills

**Install:**
```bash
/plugin install project-spec@cc-plugins
```

**Usage:**
```bash
# Project specification
/spec              # Full interview
/spec web-app      # Quick-start for web apps
/spec cli          # Quick-start for CLI tools
/spec api          # Quick-start for APIs
/spec library      # Quick-start for libraries

# Design system specification
/design            # Full design interview
/design modern     # Clean, subtle preset
/design minimal    # Sparse, typography-focused
/design bold       # Vibrant, high contrast

# Feature specification
/feature           # Full feature interview
/feature comments  # Start with feature name
```

See [plugin documentation](./plugins/project-spec/README.md) for details.

## License

MIT
