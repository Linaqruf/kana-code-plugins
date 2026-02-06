# Index Template

> Navigation hub for SPEC/ folder. Created only when user opts for SPEC/ supplements.

```markdown
# [Project Name]

> [One-line project description]

**Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD

## Quick Reference

| Aspect | Value |
|--------|-------|
| **Type** | [Type from interview] |
| **Stack** | [Primary technologies] |
| **Status** | [Planning / Development / Production] |

## Specification Files

### Core
- [SPEC.md](../SPEC.md) - Complete project specification (primary reference)

### Supplements
[List only files that were created during the interview]

- [api-reference.md](api-reference.md) - Endpoint schemas, request/response examples
- [data-models.md](data-models.md) - Complex entity schemas and relations
- [sdk-patterns.md](sdk-patterns.md) - External SDK usage patterns

## Commands

```bash
[Generated based on tech stack]
```

---

*Lookup reference. For project overview, see SPEC.md.*
```

## Generation Notes

- Create only when user agrees to SPEC/ supplements during interview
- Use descriptive filenames (api-reference.md, data-models.md) — not numbered files
- Only list supplement files that were actually created
- SPEC.md is always the primary reference — this index is a convenience navigation file
