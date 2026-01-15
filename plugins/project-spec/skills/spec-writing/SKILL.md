---
name: spec-writing
description: Use when the user wants to create project specs, design systems, or feature plans. Triggers on "create spec", "plan project", "design system", "plan feature", or "write specification".
version: 2.0.0
---

# Spec Writing v2.0

Generate comprehensive project specifications with three output modes and adaptive structure.

## Three Output Modes

| Mode | Output | Interview | Use Case |
|------|--------|-----------|----------|
| **Quick** | `SPEC.md` | Grouped, ~15 questions | Simple apps |
| **SPEC/** | `SPEC/` folder | Hybrid, ~40 questions | Production apps |
| **DEEP** | `SPEC/` folder | Socratic, ~50 questions | Complex systems |

## Quick Mode

Single-file output for simple projects.

**Interview**: 3-4 questions per turn, 4 phases, ~6-8 turns total.

**Output**: `SPEC.md` + `CLAUDE.md`

**Use when**: Simple apps, prototypes, quick start needed.

## SPEC/ Mode (Recommended)

Adaptive folder structure with validation checkpoints.

**Interview**: 2-4 questions per turn with multiple choice options, ~15 turns.

**Output**: `SPEC/` folder with adaptive files + `CLAUDE.md` with reflective behavior.

**Structure**:
```
SPEC/
├── 00-INDEX.md           # Always
├── 01-OVERVIEW.md        # Always
├── 02-ARCHITECTURE.md    # Always
├── XX-[CONDITIONAL].md   # Based on project type
├── XX-STATUS.md          # Always
├── XX-ROADMAP.md         # Always
└── XX-CHANGELOG.md       # Always
```

**Validation Checkpoints**:
1. After foundation files (00-02)
2. After technical files
3. Final review before CLAUDE.md

## DEEP Mode

Full Socratic interview for maximum detail.

**Interview**: One question per turn, ~50-60 turns.

**Output**: Same as SPEC/ mode, but validates each file individually.

**Use when**: Complex systems, power users wanting maximum control.

## Interview Workflow

### Phase 1-2: Vision & Requirements

- Problem statement
- Target users
- Success criteria
- MVP features
- Out of scope

### Phase 3-4: Architecture

- System type
- Architecture pattern (present 2-3 alternatives with tradeoffs)
- Data flow

### Phase 5-6: Tech Stack

- Frontend (if applicable)
- Backend (if applicable)
- Database (if applicable)
- Use multiple choice with recommendations

### Phase 7-8: Design & Security

- Visual design (if frontend)
- Authentication approach
- Compliance requirements

## Conditional Files

Create based on project characteristics:

| Condition | Files to Create |
|-----------|-----------------|
| Has frontend | `FRONTEND.md`, `DESIGN-SYSTEM.md` |
| Has backend | `BACKEND.md` |
| Has API | `API-REFERENCE.md` |
| Is CLI tool | `CLI-REFERENCE.md` |
| Has database | `DATA-MODELS.md` |
| Handles sensitive data | `SECURITY.md` |

## Best Practices (Superpowers-Inspired)

### Interview Conduct

- **Multiple choice**: Use AskUserQuestion options, not open-ended text
- **2-3 alternatives**: For key decisions, show options with tradeoffs
- **Validation checkpoints**: SPEC/ has 3, DEEP validates each file
- **YAGNI**: Ruthlessly simplify - ask "do we really need this?"

### Output Quality

- Be specific and actionable
- Include code examples for data models
- Reference Context7 documentation
- Keep scope realistic for MVP

## Context7 Integration

After tech choices, fetch relevant documentation:

```
1. resolve-library-id for each technology
2. query-docs for setup guides and patterns
3. Include insights in relevant spec files
```

## CLAUDE.md Generation

### Quick Mode

Simple CLAUDE.md with commands and spec reference.

### SPEC/DEEP Mode

Full CLAUDE.md with reflective behavior:

```markdown
# CLAUDE.md

[Project Name] - [Description]

## Reflective Behavior

**When to check SPEC/**: Only when this context insufficient.

**Ask before assuming**: Use AskUserQuestion for non-obvious decisions.

**Update specs proactively**: After work update status, after phases update changelog.

**Self-correction**: Keep code and spec in sync.
```

## Reference Files

### Templates
- `templates/index.template.md`
- `templates/overview.template.md`
- `templates/architecture.template.md`
- `templates/status.template.md`
- `templates/roadmap.template.md`
- `templates/changelog.template.md`
- `templates/frontend.template.md`
- `templates/backend.template.md`
- `templates/design-system.template.md`
- `templates/api-reference.template.md`
- `templates/cli-reference.template.md`
- `templates/data-models.template.md`
- `templates/security.template.md`
- `templates/configuration.template.md`
- `templates/CLAUDE.md.template`

### References
- `references/interview-questions.md` - Quick mode questions
- `references/interview-questions-deep.md` - SPEC/DEEP mode questions
- `references/spec-folder-template.md` - Folder structure guide

### Examples
- `examples/web-app-spec.md`
- `examples/cli-spec.md`
- `examples/api-spec.md`
- `examples/library-spec.md`

## Related Commands

- `/spec` - Generate project specification
- `/feature` - Generate feature specification
- `/design` - Generate design system specification

## Integration with Other Skills

### feature-dev

After creating specs, use feature-dev agents:
1. `code-explorer` - Analyze existing patterns
2. `code-architect` - Design implementation
3. `code-reviewer` - Review implementation

### frontend-design

Use design specs to implement components following the specification.
