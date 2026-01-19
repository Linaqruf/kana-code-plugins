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
| [fuwari-md](./plugins/fuwari-md) | Fuwari's markdown stack - admonitions, math, GitHub cards, code highlighting | 1.0.2 |
| [codebase-cleanup](./plugins/codebase-cleanup) | Comprehensive cleanup analysis for TypeScript/JavaScript codebases | 1.0.4 |

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
