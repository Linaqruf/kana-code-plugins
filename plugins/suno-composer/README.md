# Suno Composer

A Claude Code plugin for composing Suno AI songs with a guided workflow. Generates complete song specifications including lyrics, style tags, tempo, vocal arrangements, and more - all based on your musical preferences.

## Features

- **Guided Composition**: Interactive workflow that asks key questions about mood, theme, and style
- **Preference-Based**: Stores your taste profile for consistent results across sessions
- **Complete Output**: Generates title, lyrics, Suno v5 style tags, tempo, vocal type, and arrangement notes
- **Preset Moods**: Quick-select from common moods (upbeat, melancholic, energetic, dreamy, intense, chill)
- **Batch Generation**: Create multiple song variations in one session
- **Language Agnostic**: Supports any language for lyrics

## Installation

Add this plugin to your Claude Code configuration:

```bash
claude --plugin-dir /path/to/suno-composer
```

Or add to your `.claude/plugins.json`:

```json
{
  "plugins": [
    "/path/to/suno-composer"
  ]
}
```

## Usage

### Quick Start

```
/suno
```

This starts the guided composition workflow which will ask about:
1. Mood/theme (with presets or custom description)
2. Number of songs to generate
3. Language preference for this session

### With Initial Theme

```
/suno summer heartbreak ballad
```

Start composition with a theme already in mind.

## Configuration

Create a preferences file at `.claude/suno-composer.local.md` in your project or home directory:

```markdown
# Suno Composer Preferences

## Favorite Genres
- J-pop
- Doujin/Vocaloid style
- City pop
- Anime soundtrack

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

## Stylistic Notes
- Love complex chord progressions
- Appreciate both acoustic and electronic production
- Enjoy dramatic key changes
```

## Components

- **Command**: `/suno` - Main composition workflow
- **Agent**: `song-composer` - Generates complete song specifications
- **Skill**: `song-composition` - Knowledge about Suno v5, genres, and song structures

## Output Format

Each generated song includes:

```
═══════════════════════════════════════════════════════════
## Song 1: [Title]
═══════════════════════════════════════════════════════════

### Lyrics

[Verse 1]
...

[Chorus]
...

### Suno Style Tags
j-pop, emotional ballad, female vocals, piano, strings, ...

### Specifications
- **Tempo:** 85 BPM
- **Vocal:** Soft female vocals
- **Mood:** Melancholic
- **Arrangement:** Piano-driven with orchestral swells

───────────────────────────────────────────────────────────
```

## License

MIT
