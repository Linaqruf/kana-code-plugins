# Session Prompt Template v4.0.0

> Template for generating `prompt.md` — a compound engineering session bootstrapper placed at the project root. Each session builds on the last by feeding discoveries back into the spec.

## Template

Adapt based on parameters. Output file: `prompt.md` at the project root.

~~~markdown
# [Project Name] — Dev Session

Spec: `[Spec File]` | Status: `[Spec File]` § [Phase Section Name]

## Loop

1. **Read** — Open `[Spec File]` § [Phase Section Name]. Find the next unchecked `- [ ]` phase. Read spec sections relevant to that phase (architecture, data models, endpoints, design system — whatever applies).[Supplement Line]
2. **Ask** — If anything is ambiguous or underspecified for this phase, ask via AskUserQuestion. Do not ask what the spec already answers.
3. **Plan** — Enter Plan Mode. Create implementation plan with file paths, code patterns, and test coverage.
4. **Work** — Execute the plan. Run tests and lint.
5. **Compound** — Update `[Spec File]`: check off completed items `- [x]`, add discoveries to **Open Questions** (status: Resolved).[CLAUDE.md Line]
6. **Report** — Summarize: what was done, what's next, open questions needing input.
~~~

## Parameterization

| Parameter | How to Fill |
|-----------|-------------|
| `[Project Name]` | First `# ` heading in the generated spec. **Fallback**: use the project directory name if no `# ` heading found. |
| `[Spec File]` | `SPEC.md` for project specs, `FEATURE_SPEC.md` or `SPEC/FEATURE-[NAME].md` for feature specs, `DESIGN_SPEC.md` or `SPEC/DESIGN-SYSTEM.md` for design specs |
| `[Phase Section Name]` | Actual section heading containing `- [ ]` checkboxes: "Development Phases" (project), "Implementation Plan" (feature), "Migration Checklist" (design overhaul). **Fallback**: use "Development Phases" if no section with checkboxes found. |
| `[Supplement Line]` | See Adaptation Rules below. Omit entirely if no supplements. |
| `[CLAUDE.md Line]` | See Adaptation Rules below. Omit entirely if no CLAUDE.md. |

## Adaptation Rules

### Supplement references

If SPEC/ supplement files were created, append to step 1:

```
 Reference supplements for implementation details: → `SPEC/api-reference.md` for endpoint schemas, → `SPEC/sdk-patterns.md` for SDK usage.
```

List only the supplements that actually exist.

### CLAUDE.md update

If CLAUDE.md exists, append to step 5:

```
 If new constraints found, add to `CLAUDE.md` § Key Constraints.
```

If no CLAUDE.md exists, omit this line.

### Feature specs

If the spec is a feature spec (not the full project spec), append to step 1 after the first sentence:

```
Also read `SPEC.md` for project-wide context (architecture, tech stack, existing patterns).
```

Only add this if `SPEC.md` exists in the project.

### Design overhaul

If the spec is a design overhaul with migration checklist, append to step 1:

```
Follow migration phases in order — Foundation → Components → Pages → Cleanup. Do not skip phases.
```

## Output Checklist

Before writing `prompt.md`, verify:

- [ ] Uses numbered step format (not paragraphs)
- [ ] References actual file paths (not generic placeholders)
- [ ] Does not duplicate spec content — only references it
- [ ] Includes the compound step (updating checkboxes and recording learnings)
- [ ] Uses correct phase section name from the generated spec
- [ ] Total length is under 20 lines (excluding the header)

## Edge Case: Existing prompt.md

If `prompt.md` already exists at the project root, ask before overwriting:

```typescript
{
  question: "A prompt.md already exists. What would you like to do?",
  header: "Session Prompt",
  options: [
    {
      label: "Replace with new prompt",
      description: "Overwrite existing prompt.md with updated spec references"
    },
    {
      label: "Keep existing",
      description: "Leave the current prompt.md unchanged"
    }
  ]
}
```

---

*Template reference. See SKILL.md § Session Prompt (Compound Engineering) for methodology.*
