---
name: cleanup-patterns
description: This skill should be used when the user asks about "code cleanup", "remove unused", "dead code", "unused imports", "dependency audit", "technical debt", "refactoring", "codebase maintenance", "orphaned files", "unused assets", or wants guidance on identifying and removing unused code, imports, dependencies, or assets.
version: 1.0.0
---

# Cleanup Patterns

Comprehensive patterns and strategies for cleaning up TypeScript/JavaScript codebases. This skill provides guidance on identifying unused code, assets, and dependencies to reduce technical debt and improve maintainability.

## Quick Reference

### Cleanup Commands

| Task | Command | Agent |
|------|---------|-------|
| Find unused imports | `/cleanup imports` | import-analyzer |
| Find dead code | `/cleanup deadcode` | dead-code-detector |
| Find unused assets | `/cleanup assets` | asset-tracker |
| Audit dependencies | `/cleanup deps` | dependency-auditor |
| Clean configs | `/cleanup configs` | config-cleaner |
| Full analysis | `/cleanup all` | All agents |

### Detection Tools

| Tool | Purpose | Install |
|------|---------|---------|
| TypeScript | Unused locals/params | Built-in with `tsc` |
| ESLint | Unused vars, unreachable code | `npm install eslint` |
| depcheck | Unused npm packages | `npm install -g depcheck` |
| madge | Circular dependencies | `npm install -g madge` |
| ts-prune | Unused exports | `npx ts-prune` |

## Import Cleanup

### Common Import Issues

1. **Unused imports** - Imported but never referenced
2. **Duplicate imports** - Same module imported multiple times
3. **Circular imports** - Module A imports B, B imports A
4. **Side-effect only imports** - Execute code but export nothing

### Detection Strategy

```bash
# TypeScript compiler check
npx tsc --noEmit --noUnusedLocals

# ESLint with unused-imports plugin
npx eslint . --rule 'no-unused-vars: error'

# Circular dependency detection
npx madge --circular --extensions ts,tsx src/
```

### Quick Fixes

```typescript
// Before: Multiple unused imports
import { useState, useEffect, useCallback, useMemo } from 'react';
import lodash from 'lodash';

// After: Only used imports remain
import { useState, useCallback } from 'react';
```

See `references/import-patterns.md` for detailed patterns.

## Dead Code Detection

### Categories

1. **Unreachable code** - Code after return/throw statements
2. **Unused functions** - Defined but never called
3. **Unused variables** - Declared but never read
4. **Unused exports** - Exported but never imported elsewhere
5. **Unused class members** - Methods/properties never accessed

### Detection Strategy

```bash
# TypeScript checks
npx tsc --noEmit --noUnusedLocals --noUnusedParameters

# Find unused exports
npx ts-prune

# ESLint rules
npx eslint . --rule 'no-unreachable: error'
```

### Confidence Levels

| Level | Criteria | Action |
|-------|----------|--------|
| High | Zero references, private scope | Safe to remove |
| Medium | Only test references | Verify with user |
| Low | Dynamic usage patterns | Manual review required |

See `references/dead-code-patterns.md` for detailed patterns.

## Asset Tracking

### Asset Types

| Type | Extensions | Common Locations |
|------|------------|------------------|
| Images | png, jpg, svg, webp, gif | public/, src/assets/ |
| Styles | css, scss, sass, less | src/styles/, public/ |
| Fonts | woff, woff2, ttf, otf | public/fonts/ |
| Data | json, yaml | src/data/, public/ |

### Reference Patterns to Search

```typescript
// Direct imports
import logo from './logo.png';

// HTML/JSX references
<img src="/images/hero.png" />

// CSS references
background-image: url('/images/bg.jpg');

// Dynamic (flag for review)
const img = require(`./images/${name}.png`);
```

See `references/asset-patterns.md` for detailed patterns.

## Dependency Auditing

### Analysis Categories

1. **Unused packages** - In package.json but never imported
2. **Security vulnerabilities** - Known CVEs in dependencies
3. **Duplicate packages** - Same functionality, different packages
4. **Misplaced dependencies** - devDeps vs deps incorrect
5. **Outdated packages** - Behind latest versions

### Quick Commands

```bash
# Find unused packages
npx depcheck

# Security audit
npm audit

# Check outdated
npm outdated

# Package size analysis
npx package-size lodash moment axios
```

### Common Functional Duplicates

| Category | Packages (pick one) |
|----------|---------------------|
| Dates | moment, dayjs, date-fns |
| HTTP | axios, node-fetch, got, ky |
| Utilities | lodash, ramda, underscore |
| UUID | uuid, nanoid, cuid |
| Schema | zod, yup, joi |

See `references/dependency-patterns.md` for detailed patterns.

## Configuration Cleanup

### What to Check

1. **Environment variables** - Defined in .env but never used
2. **Config files** - For tools no longer installed
3. **Feature flags** - Stale or always-on flags
4. **Build configs** - Redundant or default options

### Common Obsolete Configs

| File | Check If |
|------|----------|
| .babelrc | Babel in dependencies |
| tslint.json | TSLint deprecated, use ESLint |
| .travis.yml | Still using Travis CI |
| webpack.config.js | Using Vite/Next.js instead |

## Best Practices

### Before Cleanup

1. **Commit current state** - Ensure clean git status
2. **Run tests** - Verify tests pass before changes
3. **Document public APIs** - Know what shouldn't be removed
4. **Backup configs** - Save current configuration

### During Cleanup

1. **Start with high confidence** - Remove obvious dead code first
2. **Batch similar changes** - Group related removals
3. **Test incrementally** - Run tests after each batch
4. **Use git diff** - Review changes before committing

### After Cleanup

1. **Run full test suite** - Verify nothing broke
2. **Check bundle size** - Measure improvement
3. **Update documentation** - Remove references to deleted code
4. **Commit with clear message** - Document what was removed

## Common Pitfalls

### False Positives to Avoid

1. **Dynamic usage** - `obj[methodName]()` patterns
2. **Framework magic** - Decorated methods, lifecycle hooks
3. **External consumers** - Public library exports
4. **Test utilities** - Only used in test files
5. **Generated code** - Files with `@generated` comments

### Edge Cases

```typescript
// Looks unused but called dynamically
export function helper_a() { }
export function helper_b() { }
const fn = helpers[`helper_${type}`];

// Framework-managed lifecycle
@Component({})
class MyComponent {
  ngOnInit() { }  // Called by Angular
}

// Re-exports for public API
export { Button } from './Button';  // Used by consumers
```

## Report Format

The `/cleanup` command generates reports in this format:

```markdown
# Codebase Cleanup Report

## Summary
| Category | Issues | Est. Savings |
|----------|--------|--------------|
| Unused Imports | 23 | - |
| Dead Code | 15 | ~500 LOC |
| Unused Assets | 12 | 2.3 MB |
| Unused Dependencies | 5 | 4.1 MB |

## High Priority (Safe to Remove)
[Detailed findings with file paths and line numbers]

## Medium Priority (Review Required)
[Findings that need verification]

## Low Priority (Manual Review)
[Potential issues with dynamic patterns]
```

## References

- `references/import-patterns.md` - Import analysis patterns
- `references/dead-code-patterns.md` - Dead code detection strategies
- `references/asset-patterns.md` - Asset tracking methodology
- `references/dependency-patterns.md` - Dependency audit procedures

## Examples

- `examples/cleanup-examples.md` - Before/after cleanup examples
