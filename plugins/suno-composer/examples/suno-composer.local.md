# Suno Composer Preferences

This is an example preferences file. Copy this to `.claude/suno-composer.local.md` in your project or `~/.claude/suno-composer.local.md` for global preferences.

## Preference Inheritance

When both global and project preferences exist:
- **Project sections override matching global sections**
- **Global fills gaps** where project is silent
- This lets you have base preferences globally and project-specific overrides

Example:
```
Global: Female vocals, J-pop, Japanese
Project: Male vocals, Korean
Result: Male vocals, Korean, J-pop (vocals + language from project, genre from global)
```

---

## Favorite Genres
- J-pop
- Doujin/Vocaloid style
- City pop
- Anime soundtrack
- Ballads

## Favorite Artists/Influences
- Ariabl'eyes
- Kasane Teto
- Hatsune Miku
- Kobukuro
- back number

## Preferred Vocal Styles
- Female vocal (soft, emotional)
- Synth/Vocaloid aesthetic
- Duets for dramatic pieces

## Default Languages
- Japanese (primary)
- English (mixed sections ok)

## Mood Tendencies
- Blend mainstream J-pop emotion with doujin aesthetics
- Experimental arrangements welcome
- Prefer melodic over heavy
- Gravitates toward emotional depth even when requesting upbeat themes

## Stylistic Notes
- Love complex chord progressions
- Appreciate both acoustic and electronic production
- Enjoy dramatic key changes
- Open to experimentation
- Prefers vision-first mode over guided questions

---

## How Preferences Are Used

Preferences inform composition without constraining it:

| Your Preference | How Claude Uses It |
|-----------------|-------------------|
| Favorite Genres | Default style prompt foundation |
| Vocal Styles | Applied unless you specify otherwise |
| Languages | Used when not obvious from context |
| Artists | Considered as baseline influences |
| Mood Tendencies | Shape emotional arc decisions |
| Stylistic Notes | Applied as creative guidelines |

Session-specific requests always take precedence over preferences.

## Wizard-Generated vs. Session-Learned

Preferences can come from two sources:

1. **First-Run Wizard** - Created when you first run `/suno` with no preferences
2. **Session Reflection** - Added when Claude notices patterns and you confirm

Both are written in natural language and can be edited manually anytime.

## Dismissing the Wizard

If you don't want the first-run wizard, add this marker:

```markdown
<!-- preferences-wizard: dismissed -->
```

The wizard won't trigger when this marker is present.
