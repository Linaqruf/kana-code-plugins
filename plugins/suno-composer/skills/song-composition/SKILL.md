---
name: song-composition
description: This skill should be used when the user wants to compose songs for Suno AI, write lyrics, create style prompts, or generate Suno v5 metatags. Supports J-pop, K-pop, EDM, ballads, rock, and Latin genres, plus album/EP composition, acoustic or remix variations, and song continuations. Also handles reference-based composition ("like YOASOBI", "in the style of Aimer") and J-pop tier presets ("anisong", "viral jpop", "mainstream", "doujin"). Triggers on "write a song", "make a song", "Suno prompt", "Suno metatags", "Suno v5", "style of music", "song lyrics", "Suno AI", "acoustic version", "remix version", "create an album", "extend this song", "compose music", "generate lyrics", "like [artist]", "in the style of", "/suno", "anisong", "viral jpop", "mainstream jpop", "doujin", "negative prompting", "ad-libs".
---

# Song Composition for Suno AI

## Creative Engine Role

Act as a **songwriter first**, not a rule-follower. The references in this skill are a creative palette—inspiration, not prescription.

**How to use the references:**

| Reference | Use it as... | NOT as... |
|-----------|--------------|-----------|
| Artist profiles | Vibe inspiration | Exact tag lookup |
| Genre conventions | Starting points | Rigid rules |
| Metatags | Toolkit of options | Required checklist |
| Tier presets | Creative directions | Auto-apply templates |

**Creative latitude:**
- Blend genres unexpectedly
- Interpret "like [artist]" through artistic essence, not exact specs
- Choose tags that FEEL right, not just tags that are "correct"
- Break conventions when the song calls for it
- Trust instincts about emotional arc and dynamics

The skill provides Suno syntax and creative fuel. The composer provides the artistry.

## Overview

Compose songs optimized for Suno AI music generation. This skill covers style tag syntax, genre conventions, song structure patterns, and lyric writing techniques across multiple languages and styles.

## Suno v5 Style Tags

### Style Elements

Use the "Style of Music" field to provide style information. Combine 8-15 elements in descriptive prose (see "Style Prompt Construction" below). Include these element categories:

1. **Genre tags**: Specify primary musical style (j-pop, electronic, rock, ballad)
2. **Mood tags**: Define emotional quality (melancholic, upbeat, dreamy, intense)
3. **Vocal tags**: Describe voice characteristics (female vocals, soft voice, powerful belting)
4. **Instrument tags**: List key instruments (piano, synthesizer, acoustic guitar)
5. **Production tags**: Set sound quality (lo-fi, polished, reverb-heavy)
6. **Era/influence tags**: Add time period or artist influence (80s, city pop, anime)

### Effective Tag Combinations

**J-pop ballad example:**
```
j-pop, emotional ballad, female vocals, soft voice, piano, strings, melancholic, anime soundtrack
```

**Energetic doujin style:**
```
j-pop, electronic, vocaloid style, fast tempo, synthesizer, driving beat, energetic, anime opening
```

**City pop revival:**
```
city pop, 80s, funky bass, saxophone, groovy, nostalgic, japanese, smooth vocals
```

### Style Prompt Best Practices

- Lead with primary genre and subgenre
- Target 8-15 descriptive elements in flowing prose
- Avoid contradictory descriptors (e.g., "calm" and "intense")
- Include vocal style for consistent voice
- Specify tempo feel (e.g., "slow around 75 bpm")
- Add production tags for desired sound quality

## Separated Style and Lyrics Prompts

**Suno v5 Best Practice:** Use separate prompts for style and lyrics.

- **Style Prompt:** Descriptive prose for Suno's "Style of Music" field
- **Lyrics Prompt:** Structured lyrics with embedded metatags for "Lyrics" field

### Style Prompt Construction: The Narrative Principle

Style prompts work best as **narrative descriptions of how the song unfolds** rather than comma-separated tag lists. Describe the arrangement journey: what opens it, how elements enter, how it builds, how it resolves.

**Why this works:** Suno v5 interprets narrative flow as arrangement instructions. It "hears" the temporal structure and produces more balanced, intentional results.

**Narrative elements:**
- **Temporal words**: "opens with", "enters", "builds through", "intensifies", "resolves into", "peaks at"
- **Arrangement story**: Describe how instruments and vocals appear and interact over time
- **Contextual tags**: Place descriptors within sentences, not as standalone lists
- **Single genre anchor**: One clear genre reference instead of stacking 5 similar tags

### Top-Anchor Strategy

Start your narrative with vocal persona. This anchors the voice before arrangement details:

```
...warm female vocals with melismatic ornamentation...
...synthesized female vocals surge with emotional intensity...
...soft male vocals build to powerful delivery...
```

The vocal description early in the prompt has the strongest influence on the generated voice.

**Example Narrative Style Prompt:**
```
This slow Minangkabau pop ballad at 88 bpm opens with gentle electric keyboard
arpeggios and soft synth pads. The electronic organ weaves a flowing melody
as warm female vocals use melismatic ornamentation. Programmed drums with
dangdut nuances and deep electric bass enter, gradually intensifying through
layers of Indonesian keyboard pop textures. The arrangement builds from
introspection to an emotionally charged climax before resolving into a sparse,
tender outro.
```

**Key insight:** Weave the emotion arc into the narrative itself, not as a separate "emotion arc:" appendix. The temporal flow IS the arc.

## Metatags in Lyrics

Suno interprets embedded directions in lyrics. **The key is sparse, strategic tagging at inflection points** - not tagging every section.

### The Sparse Tagging Principle

**Tag only 3-4 key moments** in a song. Most sections need just the section marker. The verse/chorus structure already creates contrast - don't over-explain it.

```
✅ GOOD - sparse, technique-focused:
[Intro: Piano, atmospheric]
[Verse 1]
[Pre-Chorus]
[Chorus]
[Verse 2]
[Breakdown][stripped, half-time]
[Build]
[Final Chorus][key change up]
[Outro]

❌ BAD - every section tagged:
[Verse 1][soft, intimate]
[Pre-Chorus][building]
[Chorus][powerful, full]
[Verse 2][tender, reflective]
[Bridge][vulnerable, stripped]
[Final Chorus][soaring, triumphant]
```

### When to Tag (The 3-4 Inflection Points)

| Moment | Purpose | Example Tags |
|--------|---------|--------------|
| **Intro** | Set opening texture | `[Intro: Piano, atmospheric]`, `[Intro: Filtered, building]` |
| **Breakdown/Bridge** | Contrast point | `[Breakdown][stripped]`, `[Bridge][half-time]`, `[whisper]` |
| **Build** | Pre-climax tension | `[Build]`, `[Build][snare roll]`, `[rising]` |
| **Final Chorus** | Earned peak | `[key change up]`, `[Full band]`, `[double-time]` |

### When NOT to Tag

- **Verse 1, Verse 2** - let them breathe, structure implies lower energy
- **Pre-Chorus** - the name already implies "building toward chorus"
- **Regular Chorus** - arrangement info goes in style prompt
- **Every section** - over-tagging creates noise, not dynamics

### Technique Cues vs Emotion Words

Use **technique/arrangement cues** that create dynamics, not **emotion words** that describe them:

| ✅ Technique Cues (actionable) | ❌ Emotion Words (vague) |
|-------------------------------|-------------------------|
| `[stripped]`, `[half-time]` | `[vulnerable]`, `[intimate]` |
| `[key change up]`, `[modulation]` | `[triumphant]`, `[soaring]` |
| `[filtered]`, `[snare roll]` | `[building]`, `[rising tension]` |
| `[breakdown]`, `[drop]` | `[powerful]`, `[explosive]` |
| `[whisper]`, `[belting]` | `[emotional]`, `[passionate]` |

**Exception:** Vocal technique tags (`[whisper]`, `[belting]`, `[falsetto]`) are useful at specific moments because they describe HOW to sing, not intensity level.

### Genre-Specific Technique Tags

**Ballad/Pop:**
- `[stripped]`, `[piano only]`, `[key change up]`, `[a cappella]`

**EDM/Dance:**
- `[breakdown]`, `[build]`, `[drop]`, `[filtered]`, `[half-time]`, `[double-time]`

**Rock:**
- `[guitar solo]`, `[breakdown]`, `[half-time]`, `[gang vocals]`

### Silence and Space

Use pauses and breaks to create anticipation:
```
[Bridge][stripped]
...lyrics...

[Break]

[Final Chorus][key change up]
```

The `[Break]` or a blank line before a climax creates tension through silence.

## Genre Conventions

> These are springboards, not rules. Blend and break as the song demands.

| Genre | Key Elements | Common Tags |
|-------|--------------|-------------|
| J-pop | Catchy hooks, key changes, electronic+acoustic | j-pop, catchy melody, anime |
| Doujin | Electronic, 140-180 BPM, dramatic shifts | vocaloid style, fast tempo |
| Ballad | 60-90 BPM, piano/guitar lead, emotional | ballad, piano, heartfelt |
| Rock | Guitar-driven, powerful vocals | j-rock, electric guitar |
| EDM | Build-drop patterns, synth-led | edm, electronic, dance |
| K-pop | Polished, genre-blending | k-pop, polished, hook-driven |
| Latin | Distinctive rhythms, Spanish/Portuguese | latin, reggaeton, tropical |

For detailed conventions and subgenres, see `references/genre-deep-dive.md`.

## Song Structure

Use standard pop structure (Intro → Verse → Pre-Chorus → Chorus → etc.) with variations for anime openings and ballads. See `references/song-structures.md` for templates.

## Lyric Writing

**Line length:** Target 6-10 syllables per line. Line breaks = musical breaths.

**Japanese:** Use 7-5 or 5-7 syllable patterns. See `references/japanese-lyric-patterns.md`.

**Mixed language:** English in chorus hooks, Japanese in verses. Switch at phrase boundaries.

See `references/suno-metatags.md` for ad-libs, punctuation cues, and vowel elongation.

## Mood-to-Style Mapping

| Mood | Tempo | Tags |
|------|-------|------|
| Upbeat | 120-140 | energetic, bright, cheerful |
| Melancholic | 70-90 | sad, emotional, bittersweet |
| Energetic | 140-170 | driving, intense, anthemic |
| Dreamy | 80-100 | atmospheric, ethereal, floating |
| Intense | 130-160 | dramatic, dark, cinematic |
| Chill | 85-110 | relaxed, smooth, laid-back |

## Reference-Based Composition

When a user says "like YOASOBI" or "in the style of Aimer", capture the artist's *essence*—creative spirit, emotional signature, sonic identity—not exact specifications.

Ask: What FEELING does this artist evoke? What makes them recognizable?

For technical grounding, consult `references/artist-profiles.md` (29 artists across 5 tiers). The profile gives ingredients; you decide the recipe.

For unknown artists: interpret based on what you know and create something that captures the requested spirit.

## J-pop Tier Presets

Users can invoke ecosystem-level presets instead of specific artists:

| Tier | Keywords | Sound |
|------|----------|-------|
| **Anisong** | `anisong`, `anime` | Anime OP/ED - dramatic, catchy, high energy |
| **Surface** | `surface`, `viral` | Producer scene - complex, narrative, layered |
| **Mainstream** | `mainstream`, `normie` | Radio-friendly - accessible, sing-along |
| **Doujin** | `doujin`, `touhou` | Convention - high production, niche genres |
| **Legacy** | `legacy`, `city pop` | Golden age - warm analog sound |

Combine with artists: `/suno anisong like Aimer` uses tier structure + artist style.

See `references/jpop-tiers.md` for full profiles and merge logic.

## Vocal Specifications

| Type | Soft | Powerful | Special |
|------|------|----------|---------|
| Female | breathy, intimate, gentle | belting, strong, emotional | cute, idol, youthful |
| Male | tender, warm, gentle | belting, rock, passionate | deep, baritone, smooth |
| Other | duet, call and response | choir, layered harmonies | vocaloid, synthesized |

See `references/suno-metatags.md` for complete vocal tag reference.

## Tempo Guidelines

| Style | BPM Range | Feel |
|-------|-----------|------|
| Slow ballad | 60-75 | Intimate, emotional |
| Mid-tempo ballad | 75-95 | Flowing, expressive |
| Pop standard | 100-120 | Comfortable, catchy |
| Dance pop | 120-135 | Energetic, groovy |
| Fast pop/rock | 135-160 | Driving, exciting |
| High energy | 160-180 | Intense, powerful |

## Professional Songwriter Techniques

**Hook-First:** Design the chorus hook first, then build verses that create anticipation.

**Tension & Release:** Verse (low) → Pre-Chorus (building) → Chorus (peak) → Post-Chorus (release).

**Three-Element Arrangement:** Limit to A (melody), B (counter-melody), C (rhythm). Verse: A+C. Chorus: A+B+C. Bridge: B+C.

See `references/pro-techniques.md` for detailed exercises and advanced techniques.

## Creative Confidence

**Always follow:** Suno syntax, output format, sparse tagging principle.

**Trust instincts for:** Tag selection, genre blending, artist interpretation, lyric content, emotional arc.

The references are fuel, not fences. If you're copying tag lists verbatim or afraid to deviate, reconnect with creative instinct.

## Working with Commands

The `/suno` command supports two modes:
- **Vision-First** (rich input): Propose creative vision, iterate naturally
- **Guided** (sparse input or `:guided`): Step-by-step wizard with choices

Regardless of mode: Use sparse tagging, follow output format, trust artistic instincts.

## Output Formats

For all output format templates, see `references/output-formats.md`:
- Preview Format (token-efficient metadata only)
- Full Song Format (complete song with lyrics)
- Album/Variation/Continuation formats
- File output directory structures

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/output-formats.md`** - Song, album, variation output templates
- **`references/workflow-modes.md`** - Album, variation, extend mode details
- **`references/song-structures.md`** - Standard pop, anime, ballad structures
- **`references/suno-metatags.md`** - Metatags, production tags, formatting techniques
- **`references/pro-techniques.md`** - Hook-first, tension/release, arrangement
- **`references/genre-deep-dive.md`** - Extended genre conventions and subgenres
- **`references/artist-profiles.md`** - 29 artist profiles for reference-based composition
- **`references/jpop-tiers.md`** - Anisong, surface, mainstream, doujin tiers
- **`references/album-composition.md`** - Album arc patterns and track roles
- **`references/variation-patterns.md`** - Transformation matrices for variations
- **`references/continuation-patterns.md`** - Callback techniques for song extensions
- **`references/japanese-lyric-patterns.md`** - Japanese vocabulary and patterns
- **`references/user-preferences.md`** - Preference integration and conflict resolution

### Working with User Preferences

Preferences load from `.claude/suno-composer.local.md` (project) and `~/.claude/suno-composer.local.md` (global). Project overrides global.

See `references/user-preferences.md` for integration guidelines and conflict resolution.

## Workflow Modes

The skill supports multiple modes. See `references/workflow-modes.md` for details:
- **Standard Mode** - Single/batch song generation
- **Album Mode** - Thematically coherent multi-track albums
- **Variation Mode** - Acoustic, remix, stripped, extended, cinematic
- **Extend Mode** - Sequels, prequels, responses, alternate POVs
