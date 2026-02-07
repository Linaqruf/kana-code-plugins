# Suno Composer

**Version 5.5.0**

A Claude Code plugin for composing Suno AI songs with a guided workflow. Generates complete song specifications including lyrics, style tags, tempo, vocal arrangements, and more - all based on your musical preferences.

> **Note:** This plugin is optimized for **J-pop and Japanese music** styles, with deep knowledge of artists like YOASOBI, Yorushika, Ado, and others. However, it fully supports general music composition across all genres including K-pop, Western pop/rock, EDM, Latin, and more.

## Features

- **Reference-Based**: Compose using artist profiles (`/suno like YOASOBI`) with built-in artist profiles
- **Guided Composition**: Interactive workflow that asks key questions about mood, theme, and style
- **Preference-Based**: Stores your taste profile for consistent results across sessions
- **Complete Output**: Generates title, style prompt, lyrics with metatags, and detailed specifications
- **File Output**: Save compositions to markdown files for easy organization
- **Preset Moods**: Quick-select from common moods (upbeat, melancholic, energetic, dreamy, intense, chill)
- **Batch Generation**: Create multiple song variations in one session
- **Album Mode**: Create thematically coherent multi-track albums and EPs
- **Variation Mode**: Generate acoustic, remix, stripped, extended, or cinematic versions
- **Extend Mode**: Create song continuations (sequels, prequels, responses, alternate POVs)
- **Multi-Genre**: J-pop, K-pop, Western pop/rock, EDM, Latin, and more
- **Language Agnostic**: Supports any language (Japanese, English, Korean, mixed, etc.)

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

### With Artist Reference

```
/suno like YOASOBI about finding hope
/suno in the style of Aimer
/suno Eve-style energetic
```

Compose using an artist's characteristics as the base style. The plugin includes artist profiles spanning J-pop, J-rock, Vocaloid, city pop, doujin, and anime soundtrack genres.

### With J-pop Tier Preset

```
/suno anisong about never giving up
/suno surface city nights theme
/suno mainstream romantic ballad
/suno doujin symphonic fantasy battle
```

Use ecosystem-level presets instead of specific artists:

| Tier | Sound | Example Artists |
|------|-------|-----------------|
| `anisong` | Anime OP/ED - dramatic builds, catchy hooks | LiSA, Aimer |
| `surface` | Viral/producer scene - complex rhythms, layered synths | YOASOBI, Ado |
| `mainstream` | Radio-friendly - band sound, sing-along | Official HIGE DANdism |
| `doujin` | Convention scene - high production, niche genres | Ariabl'eyeS |
| `legacy` | Golden age - city pop, warm analog | Tatsuro Yamashita |

Combine tier + artist for blended results: `/suno anisong like Aimer about farewell`

### Album Mode

```
/suno album about summer memories
/suno 5-track EP exploring city nights
```

Create thematically coherent multi-track albums or EPs with:
- Journey arc (opener → build → peak → descent → resolution)
- Shared sonic palette across tracks
- Track-specific roles and transitions

### Variation Mode

```
/suno make an acoustic version of that last song
/suno remix of Midnight Train
```

Generate transformed versions of an existing song:
- **Acoustic** - Organic, intimate arrangement
- **Remix** - Electronic, dance transformation
- **Stripped** - Minimal, vocal showcase
- **Extended** - Full arrangement with added sections
- **Cinematic** - Orchestral, epic treatment

### Extend Mode

```
/suno sequel to Midnight Train
/suno what happens next in the story
```

Create narratively connected songs:
- **Sequel** - Story continues forward
- **Prequel** - Origin story
- **Response** - Answer from different perspective
- **Alternate POV** - Same events, different narrator
- **Epilogue** - Reflection from distance

## File Output

When you choose to save compositions, they're organized as:

```
./songs/
├── [date]-summer-vibes/
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

## Preference System

Suno Composer learns your preferences over time for personalized compositions.

### First-Run Wizard

When you first run `/suno` without any preferences, a quick wizard (2-3 questions) helps set up your defaults:
- Favorite genres + vocal style
- Default language
- Save location (global vs project)

Choose to save globally (`~/.claude/suno-composer.local.md`) or per-project (`.claude/suno-composer.local.md`).

### Preference Inheritance

| Level | Path | Scope |
|-------|------|-------|
| Global | `~/.claude/suno-composer.local.md` | All projects |
| Project | `.claude/suno-composer.local.md` | Current project only |

When both exist, **project overrides matching sections**, global fills gaps.

### Session Reflection

After multi-song sessions, Claude may notice patterns in your choices:

> "You referenced Aimer three times across different songs. Should I default to her style as a starting point?"

Accept to update your preferences. Decline to keep things as-is.

### Skip the Wizard

If you prefer manual setup, the wizard offers "Don't ask again" to create an empty marker file.

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
| `/suno like <artist>` | Compose using artist profile | None |
| `/suno <tier>` | Compose using J-pop tier preset (anisong, surface, mainstream, doujin, legacy) | None |
| `/suno album about [concept]` | Album mode (auto-detected from intent) | None |
| `/suno acoustic version of [song]` | Variation mode (auto-detected from intent) | None |
| `/suno sequel to [song]` | Extend mode (auto-detected from intent) | None |

- **Skill**: `suno` - Knowledge about Suno v5, genres, and song structures

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

## What's New in v5.5.0

- **Opus 4.6 Optimization**: Prompts restructured for Claude's improved creative reasoning
  - Trust-based guidance replaces defensive guardrails
  - Shared workflow pattern across all modes reduces redundancy
  - Conversational guidance replaces mechanical wizards and algorithms
- **Conversational Intent Detection**: Album, variation, and extend modes now auto-detected from natural language — no explicit flags needed
- **Simplified First-Run Wizard**: Reduced from 4-5 questions to 2-3 essentials (genres + vocal style, language, save location)
- **Removed Chrome Integration**: Simplified plugin surface — copy-paste workflow is sufficient
- **Leaner SKILL.md**: ~22% reduction through removing redundant sections (Creative Confidence, Style Prompt Best Practices, When NOT to Tag, Working with Commands)
- **Leaner suno.md**: ~54% reduction through shared workflow extraction and mode-delta pattern
- **Reference Deduplication**: Consolidated overlapping content between metatags and techniques files
- **Fixed**: Added missing `version` field to SKILL.md frontmatter

## What's New in v5.4.1

- **Vision-First Walkthrough**: Complete annotated example showing the full composition workflow
  - Step-by-step from user input to Suno submission
  - Explains WHY each decision was made
  - Shows narrative style prompt construction in practice
- **Troubleshooting Guide**: Common issues, causes, and fixes
  - Style prompt issues (genre ignored, wrong tone, vocal mismatch)
  - Lyric issues (syllable mismatch, tags not working)
  - Chrome integration issues (form not found, rate limiting)
  - Preference issues (not loading, conflicts)
- **Quick Reference Table**: First thing to try for each common problem

## What's New in v5.4.0

- **Narrative Style Prompts**: Style prompts now generated as narrative descriptions of how the song unfolds, not comma-separated tag lists
  - Suno v5 interprets narrative flow as arrangement instructions
  - Uses temporal words: "opens with", "enters", "builds through", "resolves into"
  - Weaves emotion arc into the narrative itself
  - Produces more balanced, intentional results
- **Before/After Examples**: Real-world tested examples showing tag-list vs narrative approaches
- **Updated SKILL.md**: Replaced checklist-based guidance with narrative principle

## What's New in v5.3.2

- **Documentation fixes**: Standardized preference file path listing order across all docs
- **Session Reflection clarity**: Clarified that multi-song detection is contextual, not mechanical
- **Command description**: Expanded frontmatter to mention adaptive preferences

## What's New in v5.3.1

- **Reduced duplication**: Removed duplicate content between SKILL.md and reference files
- **Leaner SKILL.md**: Extracted user preferences section to dedicated reference file
- **Style consistency**: Fixed minor second-person language in skill body

## What's New in v5.3

- **First-Run Wizard**: Quick 4-5 question setup when no preferences exist
  - Choose favorite genres, vocal style, language, and optional artists
  - Save globally or per-project
  - Skip option with "don't ask again" dismissal
- **Preference Inheritance**: Global + project preferences with smart merging
  - Project sections override matching global sections
  - Global fills gaps where project is silent
- **Session Reflection**: Claude observes patterns and offers insights
  - Notices consistent choices (mood, artists, genres)
  - Conversationally offers to remember patterns
  - Updates preferences with natural language
- **Enhanced SKILL.md**: Preference-aware composition guidance

## What's New in v5.2

- **Dual-Mode Command**: Automatic mode detection based on input richness
  - **Vision-First Mode** (rich input): Claude proposes creative vision, you react naturally
  - **Guided Mode** (sparse input or `:guided`): Step-by-step wizard with structured choices
- **Explicit Mode Flags**: Use `:creative` or `:guided` to force a mode
- **Natural Iteration**: Say "darker", "fewer tracks", "make it Korean" to refine

## What's New in v5.1

- **Creative Engine Mode**: Claude as songwriter first, not rule-follower
- **Artistic Interpretation**: Artist profiles as inspiration, not exact templates
- **50/50 Balance**: Skill provides Suno syntax and creative fuel; Claude provides artistry
- **Blend & Break**: Freedom to blend genres unexpectedly and break conventions

## What's New in v4.6

- **Suno v5 Prompt Techniques**: Negative prompting, ad-libs, lyric formatting
- **Top-Anchor Strategy**: Start style prompts with vocal persona for better results
- **Breath Markers**: Use `(breath)` for natural phrasing
- **Elongation**: Use `lo-ove` for sustained notes

## What's New in v4.5

- **J-pop Tier Presets**: Use ecosystem-level presets (`/suno anisong`, `/suno surface`, `/suno mainstream`, `/suno doujin`)
  - Note: `viral` is an alias for `surface` tier (both work)
- **Doujin Subgenres**: Support for symphonic, denpa, and eurobeat doujin styles
- **Tier + Artist Merging**: Combine tier base sound with specific artist characteristics (`/suno anisong like Aimer`)
- **Legacy Tier**: Added for foundational artists like Tatsuro Yamashita

## What's New in v4.4

- **Reference-Based Composition**: Say `/suno like YOASOBI` to compose using an artist's style
- **29 Artist Profiles**: Comprehensive artist database covering J-pop, J-rock, Vocaloid, city pop, doujin, and anime soundtrack genres
- **Artists Include**: YOASOBI, Yorushika, Ado, Eve, Kenshi Yonezu, LiSA, Aimer, Official HIGE DANdism, King Gnu, Vaundy, RADWIMPS, Mrs. GREEN APPLE, Aimyon, back number, BUMP OF CHICKEN, Fujii Kaze, imase, TUYU, Zutomayo, Creepy Nuts, Ariabl'eyeS, Kobukuro, Reol, Hatsune Miku, Kasane Teto, Spitz, Mr.Children, Tatsuro Yamashita, Yuki Kajiura
- **Smart Style Generation**: Artist name + descriptors in style prompt (user can remove name if Suno rejects)
- **Fallback Handling**: Unknown artists prompt for manual description or mood presets

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

## License

MIT
