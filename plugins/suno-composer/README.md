# Suno Composer

**Version 3.0.0**

A Claude Code plugin for composing Suno AI songs with a guided workflow. Generates complete song specifications including lyrics, style tags, tempo, vocal arrangements, and more - all based on your musical preferences.

## Features

- **Guided Composition**: Interactive workflow that asks key questions about mood, theme, and style
- **Preference-Based**: Stores your taste profile for consistent results across sessions
- **Complete Output**: Generates title, style prompt, lyrics with metatags, and detailed specifications
- **Preset Moods**: Quick-select from common moods (upbeat, melancholic, energetic, dreamy, intense, chill)
- **Batch Generation**: Create multiple song variations in one session
- **Album Mode**: Create thematically coherent multi-track albums and EPs
- **Variation Mode**: Generate acoustic, remix, stripped, extended, or cinematic versions
- **Extend Mode**: Create song continuations (sequels, prequels, responses, alternate POVs)
- **Multi-Genre**: J-pop, K-pop, Western pop/rock, EDM, Latin, and more
- **Language Agnostic**: Supports any language with Japanese romanization support

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

### Album Mode

```
/suno:album summer memories
```

Create thematically coherent multi-track albums or EPs with:
- Journey arc (opener → build → peak → descent → resolution)
- Shared sonic palette across tracks
- Track-specific roles and transitions

### Variation Mode

```
/suno:variation
```

Generate transformed versions of an existing song:
- **Acoustic** - Organic, intimate arrangement
- **Remix** - Electronic, dance transformation
- **Stripped** - Minimal, vocal showcase
- **Extended** - Full arrangement with added sections
- **Cinematic** - Orchestral, epic treatment

### Extend Mode

```
/suno:extend
```

Create narratively connected songs:
- **Sequel** - Story continues forward
- **Prequel** - Origin story
- **Response** - Answer from different perspective
- **Alternate POV** - Same events, different narrator
- **Epilogue** - Reflection from distance

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

### Style Prompt
emotional j-pop ballad, anime soundtrack influence, slow tempo around 85 bpm,
soft female vocals with emotional delivery, piano-driven with orchestral strings,
reverb-heavy atmospheric mix, bittersweet melancholic mood, building to powerful
climax, polished production

→ Copy to Suno's "Style of Music" field

### Lyrics

[Intro: Piano, atmospheric]
(instrumental)

[Verse 1][soft, breathy]
...

[Pre-Chorus][building, add layers]
...

[Chorus][Mood: yearning → release][Full arrangement]
...

[Bridge][Mood: vulnerable → hopeful][Stripped back]
...

[Outro: Fade with piano]

→ Copy to Suno's "Lyrics" field (keep all [bracket] tags)

### Specifications
- **Tempo:** 85 BPM
- **Vocal:** Soft female vocals, building to emotional delivery
- **Mood Arc:** Intimate opening → building tension → emotional climax
- **Key Instruments:** Piano (lead), strings, subtle percussion
- **Production Style:** Reverb-heavy, polished, dynamic

───────────────────────────────────────────────────────────
```

## Development

Development resources are in the `dev/` directory:

- `dev/prompt.md` - Context prompt for development sessions

See `SPEC.md` for full technical specification, development phases, and roadmap.

## License

MIT
