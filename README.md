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
| [project-spec](./plugins/project-spec) | Generate project, design, and feature specifications through interactive interviews | 1.0.6 |
| [fuwari-md](./plugins/fuwari-md) | Fuwari's markdown stack - admonitions, math, GitHub cards, code highlighting | 1.0.2 |
| [codebase-cleanup](./plugins/codebase-cleanup) | Comprehensive cleanup analysis for TypeScript/JavaScript codebases | 1.0.4 |

## Plugins

### project-spec

Generate comprehensive specification documents through interactive interviews - for projects, features, and design systems.

**Commands:**

| Command | Description | Output |
|---------|-------------|--------|
| `/project-spec:spec` | Project planning interview | `project_spec.md` |
| `/project-spec:design` | Design system interview | `design_spec.md` |
| `/project-spec:feature` | Feature planning interview | `feature_spec.md` |

**Features:**
- `/project-spec:spec` command for guided project planning (web-app, cli, api, library)
- `/project-spec:design` command for design system specs (colors, typography, components, a11y)
- `/project-spec:feature` command for feature planning (requirements, technical design, implementation)
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
/project-spec:spec              # Full interview
/project-spec:spec web-app      # Quick-start for web apps
/project-spec:spec cli          # Quick-start for CLI tools
/project-spec:spec api          # Quick-start for APIs
/project-spec:spec library      # Quick-start for libraries

# Design system specification
/project-spec:design            # Full design interview
/project-spec:design modern     # Clean, subtle preset
/project-spec:design minimal    # Sparse, typography-focused
/project-spec:design bold       # Vibrant, high contrast

# Feature specification
/project-spec:feature           # Full feature interview
/project-spec:feature comments  # Start with feature name
```

See [plugin documentation](./plugins/project-spec/README.md) for details.

---

### fuwari-md

Fuwari's production-ready markdown processing stack for any framework. Includes admonitions, math equations, GitHub repository cards, enhanced code blocks, and more.

**Commands:**

| Command | Description |
|---------|-------------|
| `/fuwari-md:syntax` | Quick markdown syntax reference |
| `/fuwari-md:setup` | Generate config for your framework |
| `/fuwari-md:component` | Create custom remark/rehype plugins |

**Features:**
- Admonitions (`:::note`, `:::tip`, `> [!WARNING]`)
- Math equations (KaTeX)
- GitHub repository cards (`::github{repo="owner/repo"}`)
- Enhanced code blocks (line numbers, copy button, language badges)
- Reading time calculation
- Fuwari source code included as references
- `markdown-architect` agent for debugging

**Install:**
```bash
/plugin install fuwari-md@cc-plugins
```

**Quick Syntax:**
```markdown
:::note[Title]
Admonition content
:::

$E = mc^2$  <!-- inline math -->

::github{repo="withastro/astro"}
```

See [plugin documentation](./plugins/fuwari-md/README.md) for details.

---

### codebase-cleanup

Comprehensive cleanup analysis for TypeScript/JavaScript codebases. Detect and remove unused imports, dead code, orphaned assets, unused dependencies, and obsolete configurations.

**Commands:**

| Command | Description |
|---------|-------------|
| `/cleanup` | Interactive cleanup analysis |
| `/cleanup all` | Full analysis (all categories) |
| `/cleanup imports` | Unused/duplicate/circular imports |
| `/cleanup deadcode` | Unreachable code, unused functions |
| `/cleanup assets` | Unused images, CSS, fonts |
| `/cleanup deps` | Unused npm packages |
| `/cleanup configs` | Unused env vars, obsolete configs |

**Features:**
- Unused import detection with duplicate and circular dependency checks
- Dead code detection (unreachable code, unused functions, variables, exports)
- Asset tracking for unused images, CSS, fonts, and static resources
- Dependency auditing with security vulnerability detection
- Configuration cleanup for env vars, feature flags, and obsolete configs
- Interactive review with confidence levels (High/Medium/Low)
- Structured markdown reports with actionable recommendations

**Agents:**

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `import-analyzer` | "find unused imports" | Import statement analysis |
| `dead-code-detector` | "find dead code" | Unreachable/unused code detection |
| `asset-tracker` | "find unused assets" | Static file tracking |
| `dependency-auditor` | "audit dependencies" | npm package analysis |
| `config-cleaner` | "clean up configs" | Configuration file cleanup |

**Install:**
```bash
/plugin install codebase-cleanup@cc-plugins
```

**Usage:**
```bash
# Interactive mode
/cleanup

# Full analysis
/cleanup all

# Specific categories
/cleanup imports,deadcode
/cleanup deps,configs
```

See [plugin documentation](./plugins/codebase-cleanup/README.md) for details.

## License

MIT
