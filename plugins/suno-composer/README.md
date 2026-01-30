# Suno Composer

**Version 4.3.0**

A Claude Code plugin for composing Suno AI songs with a guided workflow. Generates complete song specifications including lyrics, style tags, tempo, vocal arrangements, and more - all based on your musical preferences.

## Features

- **Guided Composition**: Interactive workflow that asks key questions about mood, theme, and style
- **Preference-Based**: Stores your taste profile for consistent results across sessions
- **Complete Output**: Generates title, style prompt, lyrics with metatags, and detailed specifications
- **File Output**: Save compositions to markdown files for easy organization
- **Chrome Integration**: Auto-fill Suno forms with real-time iteration (optional)
- **Preset Moods**: Quick-select from common moods (upbeat, melancholic, energetic, dreamy, intense, chill)
- **Batch Generation**: Create multiple song variations in one session
- **Album Mode**: Create thematically coherent multi-track albums and EPs
- **Variation Mode**: Generate acoustic, remix, stripped, extended, or cinematic versions
- **Extend Mode**: Create song continuations (sequels, prequels, responses, alternate POVs)
- **Multi-Genre**: J-pop, K-pop, Western pop/rock, EDM, Latin, and more
- **Language Agnostic**: Supports any language with optional romanization for Japanese

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
4. Where to save the output (optional)

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

### Chrome Integration (New in v4.0)

> **Prerequisite:** This command requires Chrome integration. Start Claude Code with `claude --chrome` first.

```
/suno:chrome
```

Interactive browser session that:
- Opens Suno's creation page in Chrome
- Composes songs and auto-fills the form
- Lets you iterate in real-time before generating
- Supports modifications and tweaks on the fly

To use this feature:
```bash
claude --chrome
```
Then run `/suno:chrome` in the session.

## File Output

When you choose to save compositions, they're organized as:

```
./songs/
├── 2024-01-15-summer-vibes/
│   ├── song-1-endless-summer.md
│   ├── song-2-ocean-breeze.md
│   └── _index.md
```

Each song file is copy-paste ready:
```markdown
# Endless Summer

## Style Prompt
[copy directly to Suno's "Style of Music" field]

## Lyrics
[copy directly to Suno's "Lyrics" field - keep all [bracket] tags]

## Specifications
- Tempo: 120 BPM
- Vocal: Female, soft with building power
- Mood Arc: Nostalgic opening → hopeful build → euphoric release
- Key Instruments: Synths, acoustic guitar, light percussion
- Production Style: Polished, reverb-heavy, summer shimmer
```

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

| Command | Description | Prerequisite |
|---------|-------------|--------------|
| `/suno` | Main composition workflow with file output | None |
| `/suno:album` | Create thematically coherent albums/EPs | None |
| `/suno:variation` | Generate song variations | None |
| `/suno:extend` | Create song continuations | None |
| `/suno:chrome` | Interactive browser workflow | `claude --chrome` |

- **Skill**: `song-composition` - Knowledge about Suno v5, genres, and song structures

## Output Format

Each generated song includes:

```
## Song 1: [Title]

### Style Prompt
emotional j-pop ballad, anime soundtrack influence, slow tempo around 85 bpm,
soft female vocals with emotional delivery, piano-driven with orchestral strings,
reverb-heavy atmospheric mix, bittersweet melancholic mood, building to powerful
climax, polished production

→ Copy to Suno's "Style of Music" field

### Lyrics

[Intro: Piano, atmospheric]
(instrumental)

[Verse 1]
...

[Pre-Chorus]
...

[Chorus]
...

[Verse 2]
...

[Breakdown][stripped, half-time]
...

[Build]

[Final Chorus][key change up]
...

[Outro]

→ Copy to Suno's "Lyrics" field (keep all [bracket] tags)

### Specifications
- **Tempo:** 85 BPM
- **Vocal:** Soft female vocals, building to emotional delivery
- **Key Instruments:** Piano (lead), strings, subtle percussion
- **Production Style:** Reverb-heavy, polished, dynamic
- **Inflection Points:** Intro texture, breakdown contrast, key change finale
```

**Note:** Lyrics use **sparse tagging** - most sections have only the section marker. Technique tags (`[stripped]`, `[key change up]`) appear only at 3-4 inflection points. Emotion arc goes in the style prompt.

## What's New in v4.3

- **Sparse Tagging**: Only 3-4 technique tags at inflection points, not every section
- **Technique Over Emotion**: Use `[half-time]`, `[key change up]`, `[stripped]` instead of `[triumphant]`, `[soaring]`
- **Emotion Arc in Style Prompt**: Suno V5 reads emotion arc from style prompt, not per-section tags
- **Trust the Structure**: Verse/chorus contrast is built-in - don't over-explain with tags
- **Silence Creates Tension**: Added `[Break]` and pause techniques for anticipation
- **Removed Redundant Examples**: Skill knowledge is comprehensive; inline examples are sufficient

## What's New in v4.1

- **Preview-First Workflow**: Generate metadata previews before full lyrics to save tokens
- **Confirm/Modify/Regenerate**: Review song concepts before committing to full generation
- **Dynamic Control**: Guidelines for creating proper energy waves (peaks AND valleys)
- **Direct-to-File**: Full lyrics written directly to files, not duplicated in console

## What's New in v4.0

- **Simplified Architecture**: Removed agent overhead for faster, more direct composition
- **File Output**: Save compositions to organized markdown files
- **Chrome Integration**: New `/suno:chrome` command for interactive browser sessions
- **Real-time Iteration**: Modify and tweak songs before generating on Suno

## Development

Development resources are in the `dev/` directory:

- `dev/prompt.md` - Context prompt for development sessions

See `SPEC.md` for full technical specification, development phases, and roadmap.

## License

MIT
