---
name: sync
version: 1.0.0
description: Git-aware command to detect spec drift and sync specifications with codebase changes
argument-hint: "[spec-type: spec | design | feature | all]"
allowed-tools:
  - Bash
  - AskUserQuestion
  - Write
  - Read
  - Glob
  - Grep
  - TodoWrite
---

# Spec Sync Command v1.0

Git-aware command that detects drift between specifications and codebase, then helps update specs to reflect reality.

## Usage

```bash
/project-spec:sync spec      # Sync SPEC.md
/project-spec:sync design    # Sync DESIGN_SPEC.md or SPEC/DESIGN-SYSTEM.md
/project-spec:sync feature   # Sync FEATURE_SPEC.md or SPEC/FEATURE-*.md
/project-spec:sync           # Sync all spec files (default)
```

## Core Principle

**Stateless design** - Uses git history directly, no tracking files or hidden metadata.

## Workflow

### 1. Verify Git Repository

```bash
git rev-parse --is-inside-work-tree
```

If not a git repo, inform user and exit.

### 2. Find Spec Files

Based on argument, locate spec files:

| Argument | Files to Check |
|----------|----------------|
| `spec` | `SPEC.md` |
| `design` | `DESIGN_SPEC.md`, `SPEC/DESIGN-SYSTEM.md` |
| `feature` | `FEATURE_SPEC.md`, `SPEC/FEATURE-*.md` |
| (none) | All of the above |

If file doesn't exist, inform user and suggest running `/spec`, `/design`, or `/feature`.

### 3. Get Last Modification

For each spec file:

```bash
git log -1 --format="%H %ci" -- SPEC.md
```

Extract:
- Commit hash of last spec update
- Date/time of last update

### 4. Get Changes Since Last Update

```bash
# Commits since last spec update
git log --oneline <hash>..HEAD

# Files changed
git diff --stat <hash>..HEAD

# Detailed changes (for analysis)
git diff --name-only <hash>..HEAD
```

### 5. Categorize Changes

Map file changes to spec sections:

| File Pattern | Spec Section |
|--------------|--------------|
| `src/api/*`, `routes/*`, `app/api/*` | API Endpoints |
| `src/models/*`, `prisma/*`, `drizzle/*` | Data Models |
| `src/components/*`, `src/ui/*` | Frontend / Components |
| `package.json`, `bun.lockb`, `pnpm-lock.yaml` | Dependencies |
| `src/lib/*`, `src/utils/*` | Technical Architecture |
| `*.config.*`, `.env*` | Configuration |
| `Dockerfile`, `docker-compose.*` | Deployment |
| `src/styles/*`, `tailwind.config.*` | Design System |

### 6. Present Summary

```markdown
## Spec Sync Report

**SPEC.md** last updated: 2026-01-15 (commit abc123)

Since then:
- **8 commits** by 2 authors
- **14 files** changed

### Relevant Changes

**API Endpoints**
- Added: `src/api/export.ts` (new export endpoint)
- Modified: `src/api/projects.ts` (added pagination)

**Data Models**
- Modified: `prisma/schema.prisma` (new `exportedAt` field on Project)

**Dependencies**
- Added: `pdf-lib` (v1.17.1)

### Sections to Review

→ API Endpoints
→ Data Models
→ Dependencies

---

Would you like me to update these sections?
```

### 7. Update Sections (If User Agrees)

For each affected section:

1. Read current spec section
2. Analyze code changes
3. Propose updates
4. Ask user to confirm

```typescript
{
  question: "I found 3 new API endpoints. How should I update the spec?",
  header: "API Update",
  options: [
    {
      label: "Add all endpoints to spec",
      description: "Document all 3 new endpoints in API section"
    },
    {
      label: "Add summary only",
      description: "Note that export endpoints were added"
    },
    {
      label: "Skip",
      description: "Don't update API section"
    }
  ]
}
```

### 8. Finalize

After updates:

```markdown
## Sync Complete

Updated sections in SPEC.md:
- API Endpoints (added 3 endpoints)
- Data Models (added exportedAt field)
- Dependencies (added pdf-lib)

The spec now reflects the current codebase state.

**Next step**: Commit the updated spec
```

## Edge Cases

### No Changes Detected

```
SPEC.md is up to date!

Last updated: 2026-01-19 (commit def456)
No relevant code changes since then.
```

### Spec File Not Found

```
No SPEC.md found in this project.

Would you like to:
1. Run /project-spec:spec to create one
2. Specify a different file path
```

### Not a Git Repository

```
This directory is not a git repository.

The sync command requires git history to detect changes.
Initialize git with: git init
```

### Large Number of Changes

If > 50 commits or > 100 files changed:

```
Significant changes detected since last spec update:
- 127 commits
- 243 files changed

This may take a moment to analyze. Continue?
```

## Best Practices

### When to Sync

- After completing a feature
- Before code review
- After merging a large PR
- When resuming work after a break

### What Gets Updated

Focus on:
- Factual changes (new endpoints, schema changes)
- Dependency updates
- Architecture changes

Avoid:
- Implementation details
- Minor refactors
- Test file changes

### Commit After Sync

Always commit spec updates:

```bash
git add SPEC.md
git commit -m "docs: sync spec with recent codebase changes"
```

## Integration

### With /spec Command

If major structural changes detected, suggest re-running full `/spec` interview instead of patching.

### With feature-dev

After syncing, suggest using `code-reviewer` to verify implementation matches updated spec.
