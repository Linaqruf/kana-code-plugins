---
name: cleanup
version: 1.0.0
description: Comprehensive codebase cleanup analysis with interactive review
argument-hint: "[scope: all | imports | deadcode | assets | deps | configs]"
allowed-tools:
  - AskUserQuestion
  - Read
  - Glob
  - Grep
  - Bash
  - TodoWrite
---

# Codebase Cleanup Command

This command orchestrates comprehensive cleanup analysis for TypeScript/JavaScript codebases. It detects unused imports, dead code, orphaned assets, unused dependencies, and obsolete configurations.

## Workflow

### Step 1: Project Verification

First, verify this is a JavaScript/TypeScript project:

```bash
# Check for package.json
test -f package.json && echo "Found package.json"
```

If no package.json found, inform the user:
```
This doesn't appear to be a JavaScript/TypeScript project.
The /cleanup command requires a package.json file.

Would you like to:
1. Specify a different directory
2. Continue anyway (limited analysis)
3. Cancel
```

### Step 2: Scope Selection

If an argument was provided, validate it first.

**Valid scopes:**
- `all` - Run all analyzers
- `imports` - Unused imports only
- `deadcode` - Dead code only
- `assets` - Unused assets only
- `deps` - Dependencies only
- `configs` - Configuration cleanup only

**Multiple scopes:** Comma-separated values are allowed (e.g., `imports,deadcode`)

**Invalid argument handling:**
If an unrecognized scope is provided, inform the user:
```
Unknown scope: "[provided-value]"

Valid scopes are:
- all, imports, deadcode, assets, deps, configs

You can also combine scopes: "imports,deadcode"

Would you like to:
1. Choose from valid scopes
2. Run full analysis (all)
3. Cancel
```

If no argument provided, ask the user:

```
What would you like to clean up?

1. **all** - Run all analyzers (imports, dead code, assets, dependencies, configs)
2. **imports** - Unused, duplicate, and circular imports
3. **deadcode** - Unreachable code, unused functions and variables
4. **assets** - Unused images, CSS, fonts, and static files
5. **deps** - Unused npm packages, security issues, duplicates
6. **configs** - Unused env vars, obsolete config files, stale feature flags

You can also select multiple: "imports,deadcode" or "deps,configs"
```

### Step 3: Project Detection

Detect project characteristics:

```bash
# Framework detection
grep -l '"next"' package.json 2>/dev/null && echo "Next.js"
grep -l '"vite"' package.json 2>/dev/null && echo "Vite"
grep -l '"react"' package.json 2>/dev/null && echo "React"
grep -l '"vue"' package.json 2>/dev/null && echo "Vue"
grep -l '"svelte"' package.json 2>/dev/null && echo "Svelte"

# TypeScript detection
test -f tsconfig.json && echo "TypeScript"

# Source directory
test -d src && echo "src/"
test -d app && echo "app/"
test -d pages && echo "pages/"
```

### Step 4: Tool Availability Check

Check for optional tools that enhance analysis:

```bash
# TypeScript compiler
npx tsc --version 2>/dev/null

# depcheck for dependency analysis
npx depcheck --version 2>/dev/null

# madge for circular dependencies
npx madge --version 2>/dev/null

# ts-prune for unused exports
npx ts-prune --version 2>/dev/null
```

Report which tools are available and suggest installing missing ones for better analysis.

### Step 5: Run Analysis

Based on scope selection, perform the appropriate analysis:

#### For `imports`:
1. Find all source files (*.ts, *.tsx, *.js, *.jsx)
2. For each file, extract imports
3. Search for usage of each imported identifier
4. Check for duplicate imports from same module
5. Optionally run madge for circular dependencies

#### For `deadcode`:
1. Search for unreachable code patterns (code after return/throw)
2. Find function definitions and search for callers
3. Find variable declarations and search for reads
4. If ts-prune available, find unused exports

#### For `assets`:
1. Find all static assets in public/, assets/, static/
2. For each asset, search codebase for references
3. Calculate file sizes for potential savings
4. Flag dynamically loaded assets for review

#### For `deps`:
1. Read package.json dependencies
2. If depcheck available, run it
3. Otherwise, search for imports of each package
4. Run npm audit for security issues
5. Check npm outdated for updates
6. Identify functional duplicates

#### For `configs`:
1. Parse all .env* files
2. For each variable, search for usage
3. Find config files and check if tools are installed
4. Search for feature flag patterns

#### For `all`:
Run all of the above in sequence, then aggregate results.

### Step 6: Generate Report

Create a structured markdown report:

```markdown
# Codebase Cleanup Report

Generated: [timestamp]
Project: [name from package.json]
Framework: [detected framework]

## Executive Summary

| Category | Issues Found | Est. Savings |
|----------|--------------|--------------|
| Unused Imports | X | - |
| Dead Code | X functions | ~Y LOC |
| Unused Assets | X files | Y MB |
| Unused Dependencies | X packages | Y MB |
| Config Issues | X items | - |
| **Total** | **N issues** | **~Z MB** |

## High Priority (Safe to Remove)

[Issues with high confidence - can be safely removed]

### Unused Imports
[List of files with unused imports and suggested fixes]

### Unused npm Packages
```bash
npm uninstall [packages...]
```

### Unused Asset Files
[List of files with sizes]

## Medium Priority (Review Required)

[Issues that need verification before removal]

### Potentially Unused Functions
[Functions with no callers but could be used dynamically]

### Potentially Unused Exports
[Exports with no importers but could be public API]

## Low Priority (Manual Review)

[Issues that require human judgment]

### Dynamic Asset Directories
[Directories with dynamic loading patterns]

### Feature Flags
[Flags that have been enabled/disabled for extended periods]

## Recommended Actions

### Immediate Actions
1. [Safe removals]

### This Sprint
1. [Medium priority items]

### Backlog
1. [Low priority items]
```

### Step 7: Interactive Confirmation

Present actions to user:

```
## Analysis Complete

Found 63 potential cleanup opportunities across 5 categories.

What would you like to do?

1. **Fix all safe issues** - Remove high-confidence unused items
2. **Review by category** - Go through each category interactively
3. **Export report** - Save report to cleanup-report.md
4. **Show details** - Display full report
5. **Exit** - Done for now
```

#### For "Fix all safe issues":
Present batch of changes:
```
The following changes will be made:

**Imports (23 files):**
- Remove 45 unused imports across 23 files

**Dependencies:**
- npm uninstall moment lodash unused-util

**Assets:**
- Delete 5 unused image files (397 KB)

Proceed? (y/n)
```

#### For "Review by category":
Go through each category one by one:
```
## Category: Unused Imports (23 items)

File: src/components/Button.tsx
- Line 1: remove `useEffect` from react import
- Line 3: remove entire `lodash` import

Actions:
1. Fix this file
2. Skip this file
3. Fix all in this category
4. Skip this category
```

### Step 8: Apply Changes (If Approved)

For imports:
- Show diff of proposed changes
- Get confirmation before editing

For dependencies:
- Generate npm uninstall command
- Let user run it (don't auto-execute)

For assets:
- List files to delete with paths
- Get explicit confirmation before deletion

For configs:
- Show which lines to remove from .env files
- Let user make the changes

### Step 9: Summary

After any actions taken:

```
## Cleanup Summary

Actions completed:
- Removed 45 unused imports from 23 files
- Generated npm uninstall command for 3 packages
- Identified 5 asset files for deletion (manual action required)

Remaining issues:
- 8 medium-priority items (see report)
- 12 low-priority items (manual review needed)

Next steps:
1. Run: npm uninstall moment lodash unused-util
2. Delete identified asset files
3. Review medium-priority items with team
```

## Error Handling

### No package.json
```
Error: No package.json found in current directory.

This command is designed for JavaScript/TypeScript projects.
Please navigate to a project directory or specify the path.
```

### Large Codebase Warning
```
Note: This is a large codebase (500+ files).
Analysis may take a few minutes.

Continue? (y/n)
```

### Missing Tools
```
Some analysis tools are not installed:
- depcheck (for dependency analysis)
- madge (for circular dependency detection)

The analysis will continue with available tools.
Results may be more limited.

Install missing tools? (npm install -g depcheck madge)
```

## Reference

For detailed patterns and examples, refer to:
- `${CLAUDE_PLUGIN_ROOT}/skills/cleanup-patterns/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/cleanup-patterns/references/`
- `${CLAUDE_PLUGIN_ROOT}/skills/cleanup-patterns/examples/`

## Agents

This command can delegate to specialized agents:
- `import-analyzer` - For deep import analysis
- `dead-code-detector` - For comprehensive dead code detection
- `asset-tracker` - For static asset tracking
- `dependency-auditor` - For npm package auditing
- `config-cleaner` - For configuration cleanup
