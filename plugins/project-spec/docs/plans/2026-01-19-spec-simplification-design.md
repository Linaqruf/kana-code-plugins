# Design: Spec Simplification

**Date**: 2026-01-19
**Status**: Implemented (v3.1.0)

## Problem Statement

The current project-spec plugin has three output modes (Quick, SPEC/, DEEP) that create confusion and maintenance burden:

1. **Single SPEC.md** is effective (complete context) but inefficient as projects grow
2. **Multi-file SPEC/** is efficient (modular) but ineffective in practice:
   - Claude cherry-picks files, misses critical context in unread files
   - Claude over-focuses on paths specified in CLAUDE.md
   - User must maintain both code AND spec files (double burden)
3. **Specs drift from reality** because:
   - Development pivots happen, updating multiple spec files feels like overhead
   - Once coding starts, specs become "out of sight, out of mind"

## Design Goals

1. **Agent-first**: Optimize for Claude's consumption, not human documentation
2. **Single source of truth**: One file to maintain, one file to read
3. **Scalable when needed**: Support supplements for reference-heavy content
4. **Reduce maintenance burden**: Less spec overhead, less drift
5. **Opinionated but flexible**: Recommend best practices, allow override

## Solution

### Core Principle

**SPEC.md is always the complete spec. SPEC/ files are optional lookup supplements.**

```
SPEC.md               # Always created, always self-sufficient
CLAUDE.md             # Generated with spec references

SPEC/                 # Optional, created incrementally when user agrees
├── api-reference.md  # Lookup: endpoint schemas, request/response
├── sdk-patterns.md   # Lookup: external SDK usage examples
└── data-models.md    # Lookup: complex entity schemas
```

Key distinction:
- **SPEC.md** = Things you READ (narrative, decisions, requirements)
- **SPEC/*.md** = Things you LOOK UP (schemas, SDK patterns, external API details)

### Remove Quick/SPEC/DEEP Modes

One adaptive flow replaces three modes:

```
Interview starts
    ↓
Build SPEC.md progressively
    ↓
Hit reference-heavy topic? ──→ Ask: "Create SPEC/[topic].md for lookup?"
    ↓                                    ↓
Continue interview                  User decides (yes/no)
    ↓
Generate SPEC.md + CLAUDE.md
    ↓
If user said yes → Generate SPEC/[topic].md files
```

Supplements are offered organically during interview, not upfront mode selection.

### Supplement Triggers

Create SPEC/ files only for:
- **Reference material** - Stuff you look up, not read through (schemas, tables, examples)
- **External dependencies** - SDK docs, library patterns, third-party API details

Example mid-interview prompt:
> "Your API has 15 endpoints with detailed schemas. Should I:
> - A) Keep it inline in SPEC.md (shorter reference section)
> - B) Create SPEC/api-reference.md as a separate lookup file"

### Connecting SPEC.md to Supplements

When supplements exist, SPEC.md references them with trigger-based links:

**Inline references (in relevant sections):**
```markdown
## API Design

**Endpoints overview:**
- `POST /auth/login` - User authentication
- `GET /projects` - List user projects

→ When implementing endpoints, reference `SPEC/api-reference.md` for full request/response schemas.
```

**References section (bottom of SPEC.md):**
```markdown
---

## References

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using Anthropic SDK: `SPEC/sdk-patterns.md`
```

### SPEC.md Structure

Keep current template structure with maps section:

```markdown
# [Project Name]

## Overview
Problem, solution, target users, success criteria.

## Product Requirements
Core features (MVP), future scope, out of scope, user flows.

## Technical Architecture
Tech stack (with rationale), system design diagram, data models, API endpoints.

## System Maps
- Architecture diagram (ASCII)
- Data model relations
- User flow diagrams
- Wireframes (key screens)

## Design System
(If frontend) Colors, typography, components, accessibility.

## File Structure
Project directory layout.

## Development Phases
Phased implementation plan with checkboxes.

## Open Questions
Decisions to make during development.

---

## References
(If supplements exist) Trigger-based links to SPEC/ files.
```

### CLAUDE.md Generation

Agent-optimized pointer file:

```markdown
# [Project Name]

[One-line description]

## Spec Reference

Primary spec: `SPEC.md`

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using [SDK/Library]: `SPEC/sdk-patterns.md`

## Key Constraints

- [Critical constraint 1 - surfaced from spec]
- [Critical constraint 2]
- [Out of scope reminder]

## Commands

- `[package-manager] run dev` - Start development
- `[package-manager] run test` - Run tests
- `[package-manager] run build` - Production build

## Current Status

→ Check `SPEC.md` → Development Phases section
```

Principles:
- Surface critical constraints directly (prevent missed context)
- Trigger-based supplement references
- Short - pointer, not duplication
- Status points to SPEC.md (single source)

### Git-Aware Sync Command

New `/project-spec:sync` command to detect and resolve spec drift:

```bash
/project-spec:sync spec      # Sync SPEC.md
/project-spec:sync design    # Sync DESIGN_SPEC.md or SPEC/XX-DESIGN-SYSTEM.md
/project-spec:sync feature   # Sync FEATURE_SPEC.md or SPEC/XX-FEATURE-*.md
/project-spec:sync           # Sync all spec files
```

**Command flow:**

```
/project-spec:sync spec
    ↓
1. Find SPEC.md (error if not found)
2. Get last modified commit: git log -1 --format="%H %ci" -- SPEC.md
3. Get commits since: git log --oneline <hash>..HEAD
4. Get changed files: git diff --stat <hash>..HEAD
5. Categorize changes by spec section relevance:
   - src/api/* → API Design section
   - src/models/* → Data Models section
   - src/components/* → Frontend section
   - package.json → Dependencies section
    ↓
6. Present summary:

"SPEC.md last updated: 2026-01-15 (commit abc123)
Since then: 8 commits, 14 files changed

Relevant changes:
- API: Added 3 endpoints in src/api/export.ts
- Models: New field 'exportedAt' in src/models/project.ts
- Dependencies: Added 'pdf-lib' package

Sections to review:
→ API Endpoints
→ Data Models
→ Dependencies

Update these sections now?"
```

**Stateless design:**
- Uses `git log -1 SPEC.md` to find last modification
- No hidden metadata, no tracking files
- User commits updated spec through normal git flow

**File-to-section mapping:**

| File Pattern | Spec Section |
|--------------|--------------|
| `src/api/*`, `routes/*` | API Endpoints |
| `src/models/*`, `prisma/*`, `drizzle/*` | Data Models |
| `src/components/*`, `src/ui/*` | Frontend / Components |
| `package.json`, `bun.lockb`, `pnpm-lock.yaml` | Dependencies |
| `src/lib/*`, `src/utils/*` | Technical Architecture |
| `*.config.*`, `.env*` | Configuration |
| `Dockerfile`, `docker-compose.*` | Deployment |

### Interview Recommendations

Baked-in opinionated recommendations with user override:

```
Which package manager?

- A) bun (Recommended) - Fastest, built-in test runner
- B) pnpm - Strict deps, good for monorepos
- C) npm - Universal compatibility
- D) yarn - If team already uses it
```

Principles:
1. Lead with recommended option + brief rationale
2. Context-aware (desktop app? acknowledge Tauri vs Electron tradeoffs)
3. Acknowledge "it depends" cases (team familiarity, existing codebase)
4. Update recommendations as ecosystem evolves

## Agent Strategy

**Keep single `spec-writer` agent** - handles all spec creation (project, feature, design).

Rationale:
- Fewer agents = easier to trigger (Claude doesn't have to choose)
- The work is similar across spec types (interview → generate markdown)
- `/sync` command works standalone, no dedicated agent needed

The agent will be updated for the new simplified flow (no mode selection, supplement prompts mid-interview).

## Implementation

### Files to Modify

| File | Change |
|------|--------|
| `skills/spec-writing/SKILL.md` | Remove Quick/SPEC/DEEP, single adaptive flow |
| `commands/spec.md` | Remove mode selection, add supplement prompts |
| `commands/feature.md` | Align with new flow |
| `commands/design.md` | Align with new flow |
| `agents/spec-writer.md` | Update to new behavior |
| `references/interview-questions.md` | Consolidate into single set with recommendations |
| `references/interview-questions-deep.md` | Remove (merge into main) |
| `references/output-template.md` | Add maps section, references section |
| `references/spec-folder-template.md` | Update to optional supplements model |

### Files to Add

| File | Purpose |
|------|---------|
| `commands/sync.md` | Git-aware sync command for detecting/resolving spec drift |

### Files to Remove

- `references/interview-questions-deep.md` (consolidate into single question set)

### Behavioral Changes

1. **Interview**: Always produces SPEC.md, asks about supplements mid-interview
2. **Supplements**: Created only when user agrees, for reference material only
3. **CLAUDE.md**: Includes trigger-based references to any supplements
4. **Recommendations**: Baked into interview questions, user can override
5. **Sync**: New command detects drift via git, suggests targeted updates

## Additional Scenarios

### 1. Existing Repository Support

When running `/spec` on an existing codebase, ask upfront:

```typescript
{
  question: "What would you like to do?",
  header: "Mode",
  options: [
    {
      label: "Document existing project",
      description: "Analyze codebase and generate spec from what exists"
    },
    {
      label: "Plan new project",
      description: "Start fresh with interview-based planning"
    },
    {
      label: "Both",
      description: "Document existing + plan new features"
    }
  ]
}
```

**Document existing mode:**
1. Scan `package.json`, config files, directory structure
2. Detect tech stack (framework, database, styling)
3. Analyze existing patterns (API routes, components, models)
4. Generate SPEC.md documenting what exists
5. Ask what to add/change

### 2. Feature Gap Analysis

Enhanced `/feature` command that compares SPEC.md vs codebase:

```
/project-spec:feature
    ↓
1. Read SPEC.md (if exists)
2. Scan codebase for implemented features
3. Identify gaps:
   - Specced but not built
   - Built but not specced
   - Patterns suggesting missing features
    ↓
4. Present findings:

"Gap Analysis:

Specced but not implemented:
- [ ] Password reset (in SPEC.md → Auth section)
- [ ] Export to PDF (in SPEC.md → Features)

Implemented but not specced:
- OAuth login (found in src/auth/oauth.ts)
- Rate limiting (found in middleware)

Suggested features based on patterns:
- You have auth but no 2FA - want to add?
- You have projects but no project templates
- You have users but no user preferences

Which would you like to spec?"
```

### 3. Design Overhaul Command

New `/project-spec:design:overhaul` for first-principles redesign:

```bash
/project-spec:design:overhaul    # Full redesign from scratch
```

**Flow:**
1. Audit current design (if exists)
   - Scan existing components, styles, tokens
   - Identify inconsistencies, outdated patterns
   - Document what works vs what doesn't

2. First-principles interview
   - "Forget current implementation. What aesthetic do you want?"
   - "What are the core UI primitives you need?"
   - "What accessibility requirements?"

3. Generate new design system
   - New color palette
   - New typography scale
   - New component inventory
   - Migration notes from old → new

4. Output: `DESIGN_SPEC.md` with migration section

## Migration

Existing users with SPEC/ folders:
- No breaking change - existing specs remain valid
- New interviews use simplified flow
- Consider adding migration note to README

## Success Criteria

1. Claude reads complete context from SPEC.md alone
2. Supplements used only for lookup during implementation
3. Less spec drift (one file to maintain + sync command)
4. Faster interview (no mode selection overhead)
5. Better decisions from opinionated recommendations
6. Spec stays current via git-aware sync prompts

---

*Generated from brainstorming session 2026-01-19*
