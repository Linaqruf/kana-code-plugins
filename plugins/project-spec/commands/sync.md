---
name: sync
version: 2.0.0
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

# Spec Sync Command v2.0

Git-aware command that detects drift between specifications and codebase, then updates specs to reflect reality.

## Core Principle

**Stateless design** — uses git history directly, no tracking files or hidden metadata.

## Usage

```
/project-spec:sync spec      # Sync SPEC.md
/project-spec:sync design    # Sync DESIGN_SPEC.md or SPEC/DESIGN-SYSTEM.md
/project-spec:sync feature   # Sync FEATURE_SPEC.md or SPEC/FEATURE-*.md
/project-spec:sync           # Sync all spec files
```

## Workflow

### 1. Verify Git Repository

Run `git rev-parse --is-inside-work-tree`. If not a git repo, inform user and exit.

### 2. Find Spec Files

| Argument | Files to Check |
|----------|----------------|
| `spec` | `SPEC.md` |
| `design` | `DESIGN_SPEC.md`, `SPEC/DESIGN-SYSTEM.md` |
| `feature` | `FEATURE_SPEC.md`, `SPEC/FEATURE-*.md` |
| (none) | All of the above |

If the target file does not exist, suggest running `/spec`, `/design`, or `/feature` to create it.

### 3. Get Last Modification

```bash
git log -1 --format="%H %ci" -- SPEC.md
```

Extract commit hash and date of last spec update.

### 4. Get Changes Since Last Update

```bash
git log --oneline <hash>..HEAD
git diff --name-only <hash>..HEAD
git diff --stat <hash>..HEAD
```

### 5. Categorize Changes

Map file changes to spec sections:

| File Pattern | Spec Section |
|--------------|--------------|
| `src/api/**`, `routes/**`, `app/api/**` | API Endpoints |
| `src/models/**`, `prisma/**`, `drizzle/**` | Data Models |
| `src/components/**`, `src/ui/**`, `app/components/**` | Frontend / Components |
| `package.json`, `bun.lockb`, `pnpm-lock.yaml`, `package-lock.json` | Dependencies |
| `src/lib/**`, `src/utils/**`, `src/helpers/**` | Technical Architecture |
| `*.config.*`, `.env*` | Configuration |
| `Dockerfile`, `docker-compose.*`, `.github/workflows/**` | Deployment / CI |
| `src/styles/**`, `tailwind.config.*`, `globals.css` | Design System |
| `src/middleware/**`, `middleware/**` | Middleware / Security |
| `src/hooks/**`, `src/composables/**` | Frontend Hooks |
| `src/jobs/**`, `src/workers/**`, `src/queues/**` | Background Jobs |
| `tests/**`, `__tests__/**`, `*.test.*`, `*.spec.*` | Testing |
| `src/types/**`, `src/@types/**` | Type Definitions |

### 6. Present Summary

```markdown
## Spec Sync Report

**SPEC.md** last updated: [date] (commit [hash])

Since then:
- **[N] commits** by [M] authors
- **[N] files** changed

### Relevant Changes

**[Section Name]**
- Added: `path/to/new/file` (description)
- Modified: `path/to/changed/file` (what changed)

### Sections to Review
→ [Section 1]
→ [Section 2]
```

### 7. Update Sections

For each affected section, ask how to update:

```typescript
{
  question: "I found [N] changes to [section]. How should I update the spec?",
  header: "[Section] Update",
  options: [
    { label: "Add details to spec", description: "Document all changes in [section] section" },
    { label: "Add summary only", description: "Note that changes were made without full detail" },
    { label: "Skip", description: "Don't update this section" }
  ]
}
```

### 8. Finalize

```markdown
## Sync Complete

Updated sections in [file]:
- [Section 1] ([summary of changes])
- [Section 2] ([summary of changes])

The spec now reflects the current codebase state.

**Next step**: Commit the updated spec
```

## Edge Cases

- **No changes detected**: Report spec is up to date with last update date
- **Spec file not found**: Suggest running the appropriate creation command
- **Not a git repository**: Inform user sync requires git history
- **Large number of changes** (50+ commits or 100+ files): Warn user and ask to continue
- **Major structural changes detected**: Suggest re-running full `/spec` interview instead of patching

## Best Practices

- Run after completing a feature, before code review, or after merging a large PR
- Focus on factual changes (new endpoints, schema changes, dependency updates)
- Skip: implementation details, minor refactors, test file changes
- Always commit spec updates after sync: `git add SPEC.md && git commit -m "docs: sync spec with recent changes"`
