# Dependency Audit Patterns

Strategies for auditing npm package dependencies.

## Unused Dependencies

### Detection Tools

```bash
# depcheck - comprehensive unused detection
npx depcheck

# With custom config
npx depcheck --ignores="@types/*,eslint-*,prettier"

# npm-check - interactive mode
npx npm-check -u
```

### Manual Detection Strategy

```javascript
// 1. Parse package.json
const { dependencies, devDependencies } = require('./package.json');
const allDeps = Object.keys({ ...dependencies, ...devDependencies });

// 2. For each dependency, search for imports
for (const pkg of allDeps) {
  const patterns = [
    `from '${pkg}'`,
    `from "${pkg}"`,
    `from '${pkg}/`,  // Subpath imports
    `require('${pkg}')`,
    `require("${pkg}")`,
    `import('${pkg}')`,
  ];

  const refs = searchCodebase(patterns);
  if (refs.length === 0 && !isSpecialPackage(pkg)) {
    report('Unused dependency', pkg);
  }
}
```

### Special Package Patterns

Not imported directly but still used:

```javascript
const specialPackages = {
  // CLI tools - check scripts
  'eslint': 'scripts',
  'prettier': 'scripts',
  'jest': 'scripts',
  'typescript': 'scripts',
  'tsc': 'scripts',

  // Config-based
  '@babel/*': 'babel.config.js',
  'postcss-*': 'postcss.config.js',
  'tailwindcss': 'tailwind.config.js',
  'eslint-*': '.eslintrc.*',
  'prettier-*': '.prettierrc',

  // TypeScript types
  '@types/*': 'tsconfig.json',

  // Git hooks
  'husky': '.husky/',
  'lint-staged': 'package.json',

  // Peer dependencies
  'react': 'peerDependencies',
};

function isSpecialPackage(pkg) {
  return Object.entries(specialPackages).some(([pattern, location]) => {
    if (pattern.endsWith('*')) {
      return pkg.startsWith(pattern.slice(0, -1));
    }
    return pkg === pattern;
  });
}
```

## Duplicate Dependencies

### Version Duplicates

```bash
# Check for multiple versions in lockfile
npm ls lodash
# Output:
# lodash@4.17.21
# lodash@4.17.15 (via some-package)

# Deduplicate
npm dedupe

# Why is a package installed?
npm why lodash
```

### Functional Duplicates

Same purpose, different packages:

| Category | Duplicates | Recommended |
|----------|------------|-------------|
| **Dates** | moment, dayjs, date-fns, luxon | dayjs (smallest) |
| **HTTP** | axios, node-fetch, got, ky | native fetch or ky |
| **Utilities** | lodash, ramda, underscore | lodash-es (tree-shakeable) |
| **UUID** | uuid, nanoid, cuid | nanoid (smallest) |
| **Schema** | zod, yup, joi, io-ts | zod (TypeScript-first) |
| **Class names** | classnames, clsx | clsx (smaller) |
| **Deep clone** | lodash.clonedeep, clone-deep, rfdc | structuredClone (native) |

### Detection

```javascript
const duplicateGroups = {
  dates: ['moment', 'dayjs', 'date-fns', 'luxon'],
  http: ['axios', 'node-fetch', 'got', 'ky', 'superagent'],
  utils: ['lodash', 'ramda', 'underscore'],
  uuid: ['uuid', 'nanoid', 'cuid', 'shortid'],
  schema: ['zod', 'yup', 'joi', 'io-ts', 'superstruct'],
  classnames: ['classnames', 'clsx'],
};

for (const [category, packages] of Object.entries(duplicateGroups)) {
  const installed = packages.filter(p => allDeps.includes(p));
  if (installed.length > 1) {
    report('Functional duplicates', { category, packages: installed });
  }
}
```

## Security Audit

### npm audit

```bash
# Standard audit
npm audit

# JSON output for parsing
npm audit --json

# Production only
npm audit --production

# Auto-fix (safe updates only)
npm audit fix

# Force fix (may have breaking changes)
npm audit fix --force
```

### Severity Levels

| Level | CVSS Score | Action |
|-------|------------|--------|
| Critical | 9.0-10.0 | Immediate fix |
| High | 7.0-8.9 | Fix this sprint |
| Moderate | 4.0-6.9 | Plan to fix |
| Low | 0.1-3.9 | Track for later |

### Common Vulnerabilities

| Package | Issue | Fix |
|---------|-------|-----|
| lodash < 4.17.21 | Prototype pollution | Upgrade |
| axios < 0.21.1 | SSRF | Upgrade |
| minimist < 1.2.6 | Prototype pollution | Upgrade |
| node-fetch < 2.6.7 | Bypass | Upgrade |
| express < 4.17.3 | Open redirect | Upgrade |
| json5 < 2.2.2 | Prototype pollution | Upgrade |

### Alternative: Snyk

```bash
# Install snyk CLI
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor continuously
snyk monitor
```

## Misplaced Dependencies

### Should Be devDependencies

```json
{
  "dependencies": {
    // WRONG - these should be in devDependencies:
    "@types/node": "^18.0.0",     // Type definitions
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0",       // Build tool
    "jest": "^29.0.0",            // Testing
    "vitest": "^0.34.0",
    "eslint": "^8.0.0",           // Linting
    "prettier": "^3.0.0",         // Formatting
    "webpack": "^5.0.0",          // Bundler
    "vite": "^4.0.0",
    "@testing-library/react": "^14.0.0"  // Testing
  }
}
```

### Should Be dependencies

```json
{
  "devDependencies": {
    // WRONG if used in src/ code:
    "lodash": "^4.17.21",
    "axios": "^1.4.0",
    "dayjs": "^1.11.0"
  }
}
```

### Detection

```javascript
// Packages that should always be devDependencies
const devOnlyPatterns = [
  /^@types\//,
  /^typescript$/,
  /^eslint/,
  /^prettier/,
  /^jest$/,
  /^vitest$/,
  /^webpack/,
  /^vite$/,
  /^rollup/,
  /^@testing-library\//,
  /^@playwright\//,
  /^cypress$/,
];

// Check if package is imported in src/
function isRuntimeDependency(pkg) {
  return searchCodebase(`from '${pkg}'`, ['src/**/*']).length > 0;
}

// Find misplaced
for (const pkg of Object.keys(dependencies)) {
  if (devOnlyPatterns.some(p => p.test(pkg))) {
    report('Should be devDependency', pkg);
  }
}

for (const pkg of Object.keys(devDependencies)) {
  if (isRuntimeDependency(pkg)) {
    report('Should be dependency', pkg);
  }
}
```

## Outdated Dependencies

### Check for Updates

```bash
# List outdated
npm outdated

# JSON format
npm outdated --json

# Long format with details
npm outdated --long
```

### Update Strategies

| Update Type | Risk | Approach |
|-------------|------|----------|
| Patch (x.x.1 -> x.x.2) | Low | Auto-update safe |
| Minor (x.1.x -> x.2.x) | Medium | Test then update |
| Major (1.x.x -> 2.x.x) | High | Review changelog, test thoroughly |

### Batch Updates

```bash
# Update all to latest within semver range
npm update

# Update specific package to latest
npm install package@latest

# Interactive updates
npx npm-check -u

# Update all (including major - dangerous)
npx npm-check-updates -u && npm install
```

## Size Analysis

### Check Package Size

```bash
# Package size tool
npx package-size lodash moment axios dayjs

# Output:
# lodash: 71.5 kB (minified), 25.2 kB (gzipped)
# moment: 290 kB (minified), 72 kB (gzipped)
# axios: 13.5 kB (minified), 4.9 kB (gzipped)
# dayjs: 2.9 kB (minified), 1.3 kB (gzipped)
```

### Bundle Analysis

```bash
# Webpack bundle analyzer
npx webpack-bundle-analyzer dist/stats.json

# Vite bundle visualizer
npx vite-bundle-visualizer

# Next.js bundle analyzer
npm install @next/bundle-analyzer
# Configure in next.config.js
```

### Size Recommendations

| Package | Size | Alternative | Savings |
|---------|------|-------------|---------|
| moment | 290 KB | dayjs (3 KB) | 99% |
| lodash | 70 KB | lodash-es + tree-shaking | 80%+ |
| axios | 13 KB | native fetch | 100% |
| uuid | 9 KB | nanoid (1 KB) | 89% |
| classnames | 1 KB | clsx (0.5 KB) | 50% |

## Lock File Health

### Verify Integrity

```bash
# Clean install from lock file
npm ci

# Verify lock file is in sync
npm install --package-lock-only
git diff package-lock.json  # Should be empty
```

### Deduplicate

```bash
# npm
npm dedupe

# Verify deduplication
npm ls --all | grep -E "^\s+\w+@" | sort | uniq -d
```

### Regenerate Lock File

```bash
# If lock file is corrupted or out of sync
rm -rf node_modules package-lock.json
npm install
```

## Report Format

```markdown
## Dependency Audit Report

### Summary
| Category | Count | Severity |
|----------|-------|----------|
| Unused | 5 | - |
| Security | 3 | 1 High, 2 Moderate |
| Misplaced | 4 | - |
| Duplicates | 2 groups | - |
| Outdated | 12 | 3 Major |

### Unused Dependencies
| Package | Type | Confidence |
|---------|------|------------|
| moment | dependency | High |
| unused-util | dependency | High |
| @types/lodash | devDependency | Medium (lodash not used) |

**Estimated savings:** 3.2 MB node_modules, 300 KB bundle

### Security Vulnerabilities
| Severity | Package | Issue | Fix |
|----------|---------|-------|-----|
| High | lodash@4.17.15 | Prototype pollution | npm install lodash@4.17.21 |
| Moderate | axios@0.21.0 | SSRF | npm install axios@1.4.0 |

### Misplaced Dependencies
**Should be devDependencies:**
- `@types/react` - Type definitions
- `typescript` - Build tool

**Should be dependencies:**
- `dayjs` - Used in src/utils.ts

### Functional Duplicates
| Category | Installed | Recommendation |
|----------|-----------|----------------|
| Dates | moment, dayjs | Keep dayjs only |
| Class names | classnames, clsx | Keep clsx only |

### Outdated (Major Updates)
| Package | Current | Latest | Breaking Changes |
|---------|---------|--------|------------------|
| react | 17.0.2 | 18.2.0 | [Changelog](url) |
| next | 12.3.0 | 14.0.0 | [Changelog](url) |
```

## Commands Reference

```bash
# Unused packages
npx depcheck
npx depcheck --ignores="pattern"

# Security
npm audit
npm audit fix
npm audit --json

# Outdated
npm outdated
npm outdated --json

# Package info
npm why <package>
npm ls <package>
npm view <package>

# Size
npx package-size <packages...>
npx bundlephobia-cli <package>

# Updates
npm update
npx npm-check -u
npx npm-check-updates
```
