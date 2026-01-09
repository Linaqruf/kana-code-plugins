# codebase-cleanup

Comprehensive cleanup analysis for TypeScript/JavaScript codebases. Detect and remove unused imports, dead code, orphaned assets, unused dependencies, and obsolete configurations.

## Features

- **Unused Import Detection** - Find imports that are never used, duplicates, and circular dependencies
- **Dead Code Detection** - Identify unreachable code, unused functions, variables, and exports
- **Asset Tracking** - Find unused images, CSS files, fonts, and static resources
- **Dependency Auditing** - Detect unused npm packages, security vulnerabilities, and duplicates
- **Configuration Cleanup** - Find unused environment variables, obsolete configs, and stale feature flags
- **Interactive Review** - Review findings before any changes are made
- **Structured Reports** - Get organized markdown reports with actionable recommendations

## Installation

Add to your Claude Code plugins:

```bash
# From the plugins repository
claude --plugin-dir path/to/codebase-cleanup
```

Or add to your project's `.claude-plugin/` directory.

## Commands

### `/cleanup`

Main command for codebase analysis.

```bash
# Full analysis (all categories)
/cleanup all

# Specific categories
/cleanup imports    # Unused/duplicate/circular imports
/cleanup deadcode   # Unreachable code, unused functions
/cleanup assets     # Unused images, CSS, fonts
/cleanup deps       # Unused npm packages
/cleanup configs    # Unused env vars, obsolete configs

# Multiple categories
/cleanup imports,deadcode
/cleanup deps,configs
```

### Interactive Mode

Running `/cleanup` without arguments starts interactive mode:

1. Select which categories to analyze
2. Review findings organized by confidence level
3. Choose to fix issues individually or in batches
4. Export reports for team review

## Agents

Specialized agents are available for focused analysis:

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `import-analyzer` | "find unused imports" | Import statement analysis |
| `dead-code-detector` | "find dead code" | Unreachable/unused code detection |
| `asset-tracker` | "find unused assets" | Static file tracking |
| `dependency-auditor` | "audit dependencies" | npm package analysis |
| `config-cleaner` | "clean up configs" | Configuration file cleanup |

## Example Output

```markdown
# Codebase Cleanup Report

## Summary
| Category | Issues | Est. Savings |
|----------|--------|--------------|
| Unused Imports | 23 | - |
| Dead Code | 15 | ~500 LOC |
| Unused Assets | 12 | 2.3 MB |
| Unused Dependencies | 5 | 4.1 MB |
| Config Issues | 8 | - |

## High Priority (Safe to Remove)
- 3 unused npm packages: lodash, moment, unused-lib
- 5 unused image files in public/images/legacy/
- 12 unused imports across 8 files

## Recommended Actions
1. npm uninstall lodash moment unused-lib
2. Delete files listed in "Unused Assets" section
3. Review feature flags older than 6 months
```

## Proactive Suggestions

The plugin includes hooks that suggest running `/cleanup` when you mention:
- "refactor"
- "clean up"
- "remove unused"
- "technical debt"
- "dead code"

## Optional Tools

For enhanced analysis, install these tools globally:

```bash
# Better unused dependency detection
npm install -g depcheck

# Circular dependency detection
npm install -g madge

# Unused export detection (uses ts-prune)
npx ts-prune
```

The plugin works without these tools but provides more comprehensive results when they're available.

## Confidence Levels

Findings are categorized by confidence:

| Level | Meaning | Action |
|-------|---------|--------|
| **High** | Definitely unused | Safe to remove |
| **Medium** | Likely unused | Verify before removing |
| **Low** | Possibly unused | Manual review required |

## What's Detected

### Imports
- Unused named imports (`import { unused } from 'module'`)
- Unused default imports (`import unused from 'module'`)
- Duplicate imports from same module
- Circular import dependencies
- Side-effect only imports (flagged for review)

### Dead Code
- Code after return/throw statements
- Functions with no callers
- Variables declared but never read
- Unused class methods and properties
- Exports never imported elsewhere

### Assets
- Images not referenced in code
- CSS files not imported
- Font files not used in @font-face
- Other static files with no references

### Dependencies
- Packages in package.json never imported
- Security vulnerabilities (via npm audit)
- Functional duplicates (moment + dayjs, etc.)
- Misplaced dev/prod dependencies
- Outdated packages

### Configuration
- Environment variables defined but never used
- Config files for uninstalled tools
- Stale feature flags (always on/off)
- Redundant default settings

## Framework Support

Works with:
- React / Next.js
- Vue / Nuxt
- Svelte / SvelteKit
- Vite projects
- Plain TypeScript/JavaScript

## Safety

- **No auto-deletion** - All changes require explicit confirmation
- **Confidence levels** - Clear indication of removal safety
- **Interactive review** - Review each finding before action
- **Report export** - Save findings for team discussion

## Requirements

- Node.js project with `package.json`
- TypeScript or JavaScript codebase

## License

MIT
