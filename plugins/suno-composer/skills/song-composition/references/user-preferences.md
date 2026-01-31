# Working with User Preferences

User preferences are loaded from `~/.claude/suno-composer.local.md` (global) and `.claude/suno-composer.local.md` (project). When both exist, project preferences override matching global sections.

## How to Apply Loaded Preferences

| Preference Type | How to Apply |
|-----------------|--------------|
| **Favorite Genres** | Use as style prompt defaults unless session contradicts |
| **Preferred Vocal Styles** | Apply to all songs unless user explicitly overrides |
| **Default Languages** | Use unless theme strongly implies otherwise |
| **Favorite Artists/Influences** | Consider as baseline influences, blend with session requests |
| **Mood Tendencies** | Shape emotional arc and dynamics |
| **Stylistic Notes** | Apply specific guidance (e.g., "prefers vision-first mode") |

## Preference Integration Principles

- Preferences are suggestions, not constraints
- Override when creative direction calls for it
- Session-specific requests take precedence
- Blend preferences with context naturally
- Don't announce "I'm using your preferences" - just use them

## Example Integration

```
User preferences: "Female vocals, J-pop, emotional depth"
Session request: "/suno epic battle anthem"

Result: J-pop epic battle anthem with female vocals,
but with emotional complexity woven into the battle narrative
(not just generic upbeat energy)
```

## When Preferences Conflict with Session

- Session request wins for explicit choices
- Preferences fill gaps where session is silent
- Use judgment for ambiguous cases
