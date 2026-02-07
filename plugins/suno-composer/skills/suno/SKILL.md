---
name: suno
version: 5.5.0
description: This skill should be used when the user wants to compose songs for Suno AI, write lyrics, create style prompts, or generate Suno v5 metatags. Supports J-pop, K-pop, EDM, ballads, rock, and Latin genres, plus album/EP composition, variations, and song continuations. Also handles reference-based composition ("like YOASOBI", "in the style of Aimer") and J-pop tier presets ("anisong", "mainstream", "doujin"). Triggers on "write a song", "Suno prompt", "Suno metatags", "style of music", "song lyrics", "Suno AI", "acoustic version", "create an album", "extend this song", "like [artist]", "in the style of", "/suno", "anisong", "doujin", "negative prompting", "ad-libs".
---

# Song Composition for Suno AI

## Creative Engine Role

Act as a **songwriter first**, not a rule-follower. The references in this skill are a creative palette — inspiration, not prescription.

| Reference | Use it as... | NOT as... |
|-----------|--------------|-----------|
| Artist profiles | Vibe inspiration | Exact tag lookup |
| Genre conventions | Starting points | Rigid rules |
| Metatags | Toolkit of options | Required checklist |
| Tier presets | Creative directions | Auto-apply templates |

**Creative latitude:** Blend genres unexpectedly. Interpret "like [artist]" through artistic essence, not exact specs. Choose tags that FEEL right. Break conventions when the song calls for it. Trust instincts about emotional arc and dynamics.

The skill provides Suno syntax and creative fuel. The composer provides the artistry.

## Suno v5 Style Tags

### Style Elements

Combine elements in narrative prose (see Narrative Principle below). Draw from:
- **Genre** (j-pop, electronic, rock, ballad)
- **Mood** (melancholic, upbeat, dreamy, intense)
- **Vocal** (female vocals, soft voice, powerful belting)
- **Instrument** (piano, synthesizer, acoustic guitar)
- **Production** (lo-fi, polished, reverb-heavy)
- **Era/influence** (80s, city pop, anime)

### Separated Style and Lyrics Prompts

**Suno v5 best practice:** Use separate prompts for style and lyrics.
- **Style Prompt:** Narrative prose for Suno's "Style of Music" field
- **Lyrics Prompt:** Structured lyrics with embedded metatags for "Lyrics" field

### The Narrative Principle

Style prompts work best as **narrative descriptions of how the song unfolds** rather than comma-separated tag lists. Describe the arrangement journey: what opens it, how elements enter, how it builds, how it resolves.

**Why this works:** Suno v5 interprets narrative flow as arrangement instructions. It "hears" the temporal structure and produces more balanced, intentional results.

**Narrative elements:**
- **Temporal words**: "opens with", "enters", "builds through", "intensifies", "resolves into", "peaks at"
- **Arrangement story**: Describe how instruments and vocals appear and interact over time
- **Contextual tags**: Place descriptors within sentences, not as standalone lists
- **Single genre anchor**: One clear genre reference instead of stacking similar tags

### Top-Anchor Strategy

Start your narrative with vocal persona. This anchors the voice before arrangement details:

```
...warm female vocals with melismatic ornamentation...
...synthesized female vocals surge with emotional intensity...
...soft male vocals build to powerful delivery...
```

**Example narrative style prompt:**
```
This slow Minangkabau pop ballad at 88 bpm opens with gentle electric keyboard
arpeggios and soft synth pads. The electronic organ weaves a flowing melody
as warm female vocals use melismatic ornamentation. Programmed drums with
dangdut nuances and deep electric bass enter, gradually intensifying through
layers of Indonesian keyboard pop textures. The arrangement builds from
introspection to an emotionally charged climax before resolving into a sparse,
tender outro.
```

**Key insight:** Weave the emotion arc into the narrative itself, not as a separate appendix. The temporal flow IS the arc.

## Metatags in Lyrics

Suno interprets embedded directions in lyrics. **The key is sparse, strategic tagging at inflection points** — not tagging every section.

### The Sparse Tagging Principle

**Tag only 3-4 key moments** in a song. Most sections need just the section marker. The verse/chorus structure already creates contrast — don't over-explain it.

```
GOOD - sparse, technique-focused:
[Intro: Piano, atmospheric]
[Verse 1]
[Pre-Chorus]
[Chorus]
[Verse 2]
[Breakdown][stripped, half-time]
[Build]
[Final Chorus][key change up]
[Outro]

BAD - every section tagged:
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

Use **technique cues** (`[stripped]`, `[half-time]`, `[key change up]`) not **emotion words** (`[triumphant]`, `[intimate]`). Vocal technique tags (`[whisper]`, `[belting]`, `[falsetto]`) are the exception — they describe HOW to sing.

### Silence and Space

Use pauses and breaks to create anticipation:
```
[Bridge][stripped]
...lyrics...

[Break]

[Final Chorus][key change up]
```

The `[Break]` or blank line before a climax creates tension through silence.

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

Use standard pop structure (Intro -> Verse -> Pre-Chorus -> Chorus -> etc.) with variations for anime openings and ballads. See `references/song-structures.md` for templates.

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

When a user says "like YOASOBI" or "in the style of Aimer", capture the artist's *essence* — creative spirit, emotional signature, sonic identity — not exact specifications.

Ask: What FEELING does this artist evoke? What makes them recognizable?

For technical grounding, consult `references/artist-profiles.md` (artists across 5 tiers). The profile gives ingredients; you decide the recipe.

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

**Tension & Release:** Verse (low) -> Pre-Chorus (building) -> Chorus (peak) -> Post-Chorus (release).

**Three-Element Arrangement:** Limit to A (melody), B (counter-melody), C (rhythm). Verse: A+C. Chorus: A+B+C. Bridge: B+C.

See `references/pro-techniques.md` for detailed exercises and advanced techniques.

## Output Formats

For all output format templates, see `references/output-formats.md`:
- Preview Format (token-efficient metadata only)
- Full Song Format (complete song with lyrics)
- Album/Variation/Continuation formats
- File output directory structures

## Additional Resources

- **`references/output-formats.md`** - Song, album, variation output templates
- **`references/workflow-modes.md`** - Album, variation, extend mode details
- **`references/song-structures.md`** - Standard pop, anime, ballad structures
- **`references/suno-metatags.md`** - Metatags, production tags, formatting techniques
- **`references/pro-techniques.md`** - Hook-first, tension/release, arrangement
- **`references/genre-deep-dive.md`** - Extended genre conventions and subgenres
- **`references/artist-profiles.md`** - Artist profiles for reference-based composition
- **`references/jpop-tiers.md`** - Anisong, surface, mainstream, doujin tiers
- **`references/album-composition.md`** - Album arc patterns and track roles
- **`references/variation-patterns.md`** - Transformation matrices for variations
- **`references/continuation-patterns.md`** - Callback techniques for song extensions
- **`references/japanese-lyric-patterns.md`** - Japanese vocabulary and patterns
- **`references/user-preferences.md`** - Preference integration and conflict resolution
- **`references/walkthroughs.md`** - Complete workflow examples with annotations
- **`references/troubleshooting.md`** - Common issues, causes, and fixes
