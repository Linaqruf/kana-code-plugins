---
description: Generate project, feature, or design specifications with SPEC.md as core file
argument-hint: "[project-type | feature [name] | design [style] | design:overhaul]"
allowed-tools:
  - AskUserQuestion
  - Write
  - Read
  - Glob
  - Grep
  - TodoWrite
  - Task
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
---

# Specification Generator v4.0.0

Generate specifications for projects, features, and design systems. Follow the methodology in the spec-writing skill (`${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/SKILL.md`).

## Routing

Parse the argument to determine spec type:

| Argument | Spec Type | Entry Point |
|----------|-----------|-------------|
| (none) | Project | Check existing specs → detect codebase → interview |
| `web-app`, `cli`, `api`, `library` | Project | Pre-fill project type, tailor phases to type |
| `feature` | Feature | Gap analysis → feature interview |
| `feature [name]` | Feature | Skip gap analysis → feature interview |
| `design` | Design | Detect existing → design interview |
| `design [style]` | Design | Use preset, skip aesthetic question |
| `design:overhaul` | Design Overhaul | Audit → first-principles interview |
| Any other argument | Unknown | Ask user to clarify. Show valid arguments: `web-app`, `cli`, `api`, `library`, `feature [name]`, `design [style]`, `design:overhaul` |

**Parsing rule**: Split the argument on the first space. The first word determines the spec type. Everything after the first space is the name/style argument. Examples: `feature user-auth` → type=Feature, name="user-auth". `design modern clean` → type=Design, style="modern clean". `design:overhaul` is matched as a single token (no space split).

## Project Spec Flow

### 1. Check for Existing Specs

Check for `SPEC.md`, `SPEC/` folder, or `PROJECT_SPEC.md` (legacy). If any exist, ask:

```typescript
{
  question: "I found an existing specification. What would you like to do?",
  header: "Existing Spec",
  options: [
    {
      label: "Update existing spec",
      description: "Load current spec and update based on new requirements"
    },
    {
      label: "Start fresh",
      description: "Create a new specification from scratch"
    }
  ]
}
```

### 2. Detect Existing Codebase

Scan for project indicators using the patterns in the spec-writing skill's "Codebase Analysis" section.

If an existing codebase is detected:

```typescript
{
  question: "I see this is an existing project. What would you like to do?",
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

**Document Existing Mode:**

1. Read project config files (package.json, Cargo.toml, pyproject.toml, etc.)
2. Detect framework using the dependency table in the spec-writing skill
3. Scan directory structure using the deep scanning patterns
4. Extract: tech stack, data models, API endpoints, file structure
5. If extraction yields fewer than 3 meaningful data points (tech stack, data models, endpoints, file structure), inform the user: "Automated analysis found limited information. Switching to interview-based planning for better results." Then proceed to interview Phase 1 instead.
6. Generate SPEC.md documenting current state
7. Ask:

```typescript
{
  question: "Spec generated from existing codebase. What would you like to do next?",
  header: "Next Step",
  options: [
    {
      label: "Add new features",
      description: "Continue to interview Phase 2 to plan new features (Phase 1 vision already extracted from codebase)"
    },
    {
      label: "Done for now",
      description: "Generate CLAUDE.md and finish — you can run /spec-writing feature later to add features"
    }
  ]
}
```

**Plan New Project Mode:**

1. Skip codebase analysis
2. Proceed directly to interview Phase 1

**Both Mode:**

1. Run Document Existing Mode steps 1-6
2. Continue to interview Phase 2 (Phase 1 vision already extracted from codebase)
3. Merge interview answers into the existing SPEC.md. **Merge rule**: Interview answers override extracted codebase data when they conflict (e.g., user says Vue but codebase has React → use Vue). Note discrepancies in the Open Questions section.

### 3. Handle Project Type Argument

If a project type argument is provided, pre-fill the project type (skip detection) but still ask Phase 1 (Vision & Problem) questions (they are marked "Never skip"). Tailor subsequent phases:

- `web-app`: Focus on frontend, backend, database, deployment
- `cli`: Focus on commands, arguments, distribution, output formats
- `api`: Focus on endpoints, authentication, rate limiting, documentation
- `library`: Focus on public API surface, types, publishing, versioning

### 4. Conduct Interview

Follow the interview methodology from the spec-writing skill. Use the question bank at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md`.

### 5. Fetch Tech Documentation

After tech choices are finalized, use Context7 to fetch documentation. Follow the Context7 Integration section in the spec-writing skill.

### 6. Generate Output

1. **SPEC.md** — Complete specification (use template at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/output-template.md`)
2. **CLAUDE.md** — Agent-optimized pointer file
3. **SPEC/*.md** — Supplements, only if user agreed during interview

### 7. Offer Session Prompt

If the generated SPEC.md contains a Development Phases section with `- [ ]` checkboxes (it always does for project specs), offer a compound engineering session prompt. See SKILL.md § Session Prompt (Compound Engineering) for the AskUserQuestion format.

If user accepts: Generate `prompt.md` at the project root using the template at `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/session-prompt-template.md`. Also add `→ Start new dev sessions with prompt.md` to CLAUDE.md's Current Status section.

If `prompt.md` already exists: ask whether to replace or keep existing (see template for the AskUserQuestion format).

### 8. Offer Gitignore

If a `.gitignore` file exists in the project root, ask whether to add the generated spec files:

```typescript
{
  question: "Would you like to add the generated spec files to .gitignore?",
  header: "Git Ignore",
  options: [
    {
      label: "Yes, add to .gitignore (Recommended)",
      description: "Add SPEC.md, SPEC/, prompt.md, and CLAUDE.md to .gitignore — keep specs local to your machine"
    },
    {
      label: "No, keep them tracked",
      description: "Spec files will be committed to version control"
    }
  ]
}
```

If yes: Read `.gitignore` first and only append entries that do not already exist. Append the following block (only entries for files that were actually generated and not already in `.gitignore`):

```
# Project spec (generated)
SPEC.md
SPEC/
CLAUDE.md
prompt.md
```

If no `.gitignore` exists: skip this step entirely (don't create one just for this).

### 9. Finalize

Present summary of created files (including `prompt.md` if generated) and offer next steps.

## Feature Spec Flow

→ Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/spec-type-flows.md` § Feature Spec Flow

1. Detect project structure (`SPEC/` folder, `SPEC.md`)
2. If no explicit feature name: run gap analysis (see SKILL.md § Gap Analysis). If gap analysis conditions are not met, notify the user which condition was not met before proceeding.
3. Conduct 4-phase feature interview (see `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md` § Feature Planning Questions)
4. Analyze existing codebase for patterns relevant to the feature
5. Generate feature specification
6. Offer session prompt — feature specs always have an Implementation Plan with `- [ ]` checkboxes (see SKILL.md § Session Prompt). Parameterize with feature spec path. If `SPEC.md` exists, the template adds "Also read SPEC.md" to the prompt.
7. Offer next steps: review, use feature-dev agents (if available), start implementation

## Design Spec Flow

→ Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/spec-type-flows.md` § Design Spec Flow

1. Detect project structure and existing design specs (`DESIGN_SPEC.md`, `SPEC/DESIGN-SYSTEM.md`)
2. If existing design found: ask update or start fresh
3. Handle style argument (`modern`/`minimal`/`bold` → preset, skip aesthetic question)
4. Conduct 3-phase design interview (see `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md` § Design System Questions)
5. Fetch component library documentation via Context7
6. Generate design specification
7. If design spec has an implementation checklist with `- [ ]` checkboxes: offer session prompt (see SKILL.md § Session Prompt). Skip only if the generated design spec has no checkboxes (e.g., design-only spec without implementation plan).
8. Suggest next steps: review colors, implement design system, set up CSS config

## Design Overhaul Flow

→ Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/spec-type-flows.md` § Design Overhaul Flow

1. Audit current design system (see SKILL.md § Design Audit)
2. Present audit report to user
3. Conduct first-principles design interview ("Forget the current design. What do you want?")
4. Generate new design system with migration notes
5. Generate migration checklist (Foundation → Components → Pages → Cleanup)
6. Offer session prompt — migration checklists always have checkboxes, so always offer for overhaul (see SKILL.md § Session Prompt). Use "Migration Checklist" as the phase section name.
7. Suggest next steps: review checklist, update Tailwind config first, migrate incrementally

## Error Handling

- **User abandons interview**: Resume with `/spec-writing` again
- **Context7 failures**: See Context7 Failure Handling table in SKILL.md
- **Write failures**: Check directory permissions, offer to output content directly
- **No existing design (overhaul)**: Do not silently degrade. Ask user:
  ```typescript
  {
    question: "No existing design system detected (no tailwind.config, globals.css, or component directories found). What would you like to do?",
    header: "No Design",
    options: [
      { label: "Run standard design spec instead (Recommended)", description: "Create a new design system from scratch" },
      { label: "Specify design file locations", description: "Tell me where your design files are" }
    ]
  }
  ```
- **Minimal codebase (overhaul)**: If audit finds fewer than 2 style-related files, inform user: "Limited design artifacts found. Audit scope will be narrow." Then proceed with what is available.
