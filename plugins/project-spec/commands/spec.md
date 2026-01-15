---
name: spec
version: 2.0.0
description: Generate project specifications with 3 modes - Quick (single file), SPEC/ (folder), DEEP (Socratic interview)
argument-hint: "[project-type: web-app | cli | api | library]"
allowed-tools:
  - AskUserQuestion
  - Write
  - Read
  - Glob
  - Grep
  - TodoWrite
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
---

# Project Specification Generator v2.0

Generate comprehensive project specifications with adaptive structure.

## Three Output Modes

| Mode | Output | Interview | Turns | Use Case |
|------|--------|-----------|-------|----------|
| **Quick** | `SPEC.md` | Grouped (3-4/turn) | ~6-8 | Simple apps, prototypes |
| **SPEC/** | `SPEC/` folder | Hybrid (2-4/turn) + checkpoints | ~15 | Production apps |
| **DEEP** | `SPEC/` folder | Socratic (1/turn) | ~50-60 | Complex systems |

## Workflow

### 1. Check for Existing Specs

```
Check for (in order):
- SPEC/ folder
- SPEC.md (single file)
- PROJECT_SPEC.md (legacy, backward compatibility)

If exists:
- Ask: Update existing or start fresh?
- If update: Load context and continue
```

### 2. Ask Output Mode

**CRITICAL**: Always ask which mode before starting interview.

Use AskUserQuestion with these exact options:

```typescript
{
  question: "Which specification mode would you like?",
  header: "Mode",
  options: [
    {
      label: "Quick",
      description: "Single SPEC.md file, ~15 questions, fast interview"
    },
    {
      label: "SPEC/ folder (Recommended)",
      description: "Adaptive folder structure, ~40 questions, validation checkpoints"
    },
    {
      label: "DEEP",
      description: "Full Socratic interview, one question at a time, maximum detail"
    }
  ],
  multiSelect: false
}
```

### 3. Handle Project Type Argument

If project type provided in command:
- `web-app`: Focus on frontend, backend, database
- `cli`: Focus on commands, distribution
- `api`: Focus on endpoints, authentication
- `library`: Focus on public API, publishing

If not provided, determine during interview.

### 4. Conduct Interview (Mode-Specific)

#### Quick Mode (~15 questions, 4 phases)

Ask 3-4 questions per message. Provide sensible defaults.

**Phase 1: Vision**
```
1. What problem does this solve? (one sentence)
2. Who is the target user?
3. What are the 3-5 must-have features?
```

**Phase 2: Tech**
```
1. Frontend framework? [Options with recommendations]
2. Backend approach?
3. Database needs?
4. Deployment target?
```

**Phase 3: Design**
```
1. Existing brand/colors?
2. Component library preference?
```

**Phase 4: Constraints**
```
1. Solo or team?
2. Budget constraints?
```

Then generate `SPEC.md` + `CLAUDE.md`.

---

#### SPEC/ Mode (~40 questions, ~15 turns)

Use AskUserQuestion with **multiple choice options** where possible.
Group 2-4 related questions per turn.
Present **2-3 alternatives with tradeoffs** for key decisions.

**Phase 1-2: Vision & Requirements** (2 turns)
- Problem, users, success criteria
- MVP features, out of scope

**Phase 3-4: Architecture** (2 turns)
- System type, architecture pattern
- Present alternatives: "Monolith (Recommended for MVP) vs Serverless vs Microservices"

**Phase 5-6: Tech Stack** (2 turns)
- Frontend, backend, database choices
- Use multiple choice with recommendations

**Phase 7-8: Design & Security** (2 turns)
- Visual design, auth approach
- Compliance requirements

**Checkpoint 1**: Generate foundation files (00-02)
- Ask: "I've drafted the core architecture. Does this look right?"

**Phase 9-10: Technical Details** (2 turns based on project)
- Generate conditional files (frontend, backend, API, etc.)

**Checkpoint 2**: Review technical specs
- Ask: "Technical design complete. Any adjustments?"

**Generate remaining files** (status, roadmap, changelog)

**Checkpoint 3**: Final review
- Ask: "Documentation ready. Final review?"

**Generate CLAUDE.md** with reflective behavior

---

#### DEEP Mode (~50 questions, ~50 turns)

**Pure Socratic**: One question per message.

Follow the same 8 phases as SPEC/ mode, but:
- Ask ONE question at a time
- Use multiple choice via AskUserQuestion
- Allow follow-up questions based on answers
- Validate EACH file after generation
- Present 2-3 alternatives for EVERY decision

Example flow:
```
Turn 1: "What problem does this project solve?"
Turn 2: [User answers]
Turn 3: "Who is the primary user of this project?"
Turn 4: [User answers]
...
Turn 20: [Generate 00-INDEX.md]
Turn 21: "I've created the index. Does this capture your project accurately?"
Turn 22: [User confirms or requests changes]
Turn 23: [Generate 01-OVERVIEW.md]
...
```

### 5. Determine Files to Create

Based on interview answers, determine which files to create:

**Always create (foundation):**
- `00-INDEX.md`
- `01-OVERVIEW.md`
- `02-ARCHITECTURE.md`
- `XX-STATUS.md`
- `XX-ROADMAP.md`
- `XX-CHANGELOG.md`

**Conditional (based on project type):**

| Condition | Files |
|-----------|-------|
| Has frontend | `XX-FRONTEND.md`, `XX-DESIGN-SYSTEM.md` |
| Has backend | `XX-BACKEND.md` |
| Has API | `XX-API-REFERENCE.md` |
| Is CLI | `XX-CLI-REFERENCE.md` |
| Has database | `XX-DATA-MODELS.md` |
| Handles sensitive data | `XX-SECURITY.md` |
| Needs config docs | `XX-CONFIGURATION.md` |

Number files sequentially based on what's created.

### 6. Gather Tech Stack Documentation

Use Context7 MCP to fetch relevant docs:

```
1. resolve-library-id for each chosen technology
2. query-docs for setup guides and patterns
3. Include insights in relevant spec files
```

Example:
```
For Next.js + Prisma:
- Query: "Next.js app router authentication patterns"
- Query: "Prisma PostgreSQL best practices"
```

### 7. Generate Specs

Use templates from:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/templates/`

For SPEC/ mode:
1. Create `SPEC/` directory
2. Generate files in order (foundation first, then conditional)
3. Update `00-INDEX.md` TOC as files are created

### 8. Generate CLAUDE.md

**Quick mode**: Simple CLAUDE.md with commands and spec reference

**SPEC/DEEP mode**: Full CLAUDE.md with reflective behavior:

```markdown
# CLAUDE.md

[Project Name] - [Description]

## Reflective Behavior

**When to check SPEC/**: Only when this context insufficient.
Read `SPEC/00-INDEX.md` first.

**Ask before assuming**: Use `AskUserQuestion` for non-obvious decisions.

**Update specs proactively**: After work update status, after phases update changelog.

**Self-correction**: Keep code and spec in sync.

## Commands
[Generated]

## Stack
[Generated]

## Specs
[Generated list of SPEC/ files]
```

### 9. Finalize

After all files generated:

```
I've created [N] specification files:

SPEC/
├── 00-INDEX.md
├── 01-OVERVIEW.md
├── ...
└── CLAUDE.md

Would you like me to:
1. Walk through any section?
2. Add more detail to specific areas?
3. Start development?
```

## Best Practices

### Interview Conduct (Superpowers-Inspired)

- **Multiple choice**: Use AskUserQuestion options, not open-ended text
- **2-3 alternatives**: For key decisions, show options with tradeoffs
- **Validation checkpoints**: SPEC/ mode has 3, DEEP mode validates each file
- **YAGNI**: Ruthlessly simplify - remove unnecessary features

### Output Quality

- Be specific and actionable
- Include code examples for data models
- Reference Context7 documentation
- Keep scope realistic for MVP

### File Numbering

Numbers are for ordering only. Use next available number.
- Foundation files: 00-05 range
- Technical files: 06-15 range
- Process files: last numbers

## Error Handling

### User Abandons Interview
- Save progress as partial spec
- User can resume with `/spec` again

### Context7 Failures
- Continue without external docs
- Note in spec that links need manual addition

### Write Failures
- Check directory permissions
- Offer to output content directly

## Reference Materials

Templates:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/templates/`

Questions:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions.md` (Quick)
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/interview-questions-deep.md` (SPEC/DEEP)

Structure:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/references/spec-folder-template.md`

Examples:
- `${CLAUDE_PLUGIN_ROOT}/skills/spec-writing/examples/`
