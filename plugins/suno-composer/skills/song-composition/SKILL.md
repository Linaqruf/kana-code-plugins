---
name: song-composition
description: This skill should be used when the user wants to compose songs for Suno AI, write lyrics, create style prompts, or generate Suno v5 metatags. Supports J-pop, K-pop, EDM, ballads, rock, and Latin genres, plus album/EP composition, acoustic or remix variations, and song extensions. Triggers on "write a song", "Suno prompt", "Suno metatags", "style of music", "acoustic version", "create an album", "extend this song".
version: 4.0.0
---

# Song Composition for Suno AI

## Overview

Compose songs optimized for Suno AI music generation. This skill covers style tag syntax, genre conventions, song structure patterns, and lyric writing techniques across multiple languages and styles.

## Suno v5 Style Tags

### Style Elements

Suno v5 accepts style information in the "Style of Music" field. While individual tags can be comma-separated, **the recommended approach is descriptive prose combining 8-15 elements** (see "Style Prompt Construction" below). The following element categories should be included:

1. **Genre tags**: Primary musical style (j-pop, electronic, rock, ballad)
2. **Mood tags**: Emotional quality (melancholic, upbeat, dreamy, intense)
3. **Vocal tags**: Voice characteristics (female vocals, soft voice, powerful belting)
4. **Instrument tags**: Key instruments (piano, synthesizer, acoustic guitar)
5. **Production tags**: Sound quality (lo-fi, polished, reverb-heavy)
6. **Era/influence tags**: Time period or artist influence (80s, city pop, anime)

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

### Style Prompt Construction

Combine these elements into flowing prose (target 8-15 descriptive elements):
1. Primary genre and subgenre/era influence
2. Tempo feel (e.g., "slow around 75 bpm", "driving 140 bpm energy")
3. Vocal characteristics
4. Key instruments
5. Production style tags
6. Mood and energy descriptors

**Example Style Prompt:**
```
emotional j-pop ballad, anime soundtrack influence, slow tempo around 75 bpm,
soft female vocals with emotional delivery, piano-driven with orchestral strings,
reverb-heavy atmospheric mix, bittersweet melancholic mood, building to powerful
climax, polished production
```

## Advanced Metatags in Lyrics

Enhance lyrics with embedded directions that Suno interprets:

### Section-Specific Vocal Directions
```
[Verse 1][soft, breathy]
[Chorus][powerful belting]
[Bridge][whisper, intimate]
```

### Emotion Progression Markers
```
[Bridge][Mood: vulnerable → building hope]
[Verse 2][Mood: reflective → determined]
```

### Instrument/Arrangement Specification
```
[Intro: Piano only, atmospheric]
[Chorus: Full band with brass section]
[Bridge: Stripped back, acoustic only]
[Outro: Fade out, strings only]
```

### Combined Advanced Tags
```
[Verse 2][whisper → building power][sparse arrangement]
[Final Chorus][Mood: triumphant][Full arrangement, key change up]
```

## Genre Conventions

### J-pop

**Characteristics:**
- Catchy melodic hooks
- Complex chord progressions (borrowed chords common)
- Mix of verse-chorus with bridge sections
- Often includes dramatic key changes
- Blend of electronic and acoustic elements

**Common tags:** j-pop, japanese pop, catchy melody, emotional, anime

### Doujin/Vocaloid Style

**Characteristics:**
- Electronic-heavy production
- Fast tempos common (140-180 BPM)
- Intricate melodic runs
- Synth-driven arrangements
- Often features dramatic dynamics

**Common tags:** vocaloid style, electronic, synthesizer, fast tempo, dramatic, anime

### Ballad

**Characteristics:**
- Slow to mid tempo (60-90 BPM)
- Emotional, expressive vocals
- Piano or guitar-driven
- Builds to emotional climax
- Minimal percussion in verses

**Common tags:** ballad, emotional, piano, slow tempo, heartfelt, orchestral

### Rock/J-rock

**Characteristics:**
- Guitar-driven arrangements
- Strong rhythmic foundation
- Powerful vocals
- Dynamic verse-chorus contrast
- Often includes guitar solos

**Common tags:** j-rock, rock, electric guitar, powerful vocals, driving drums

### Western Pop/Rock

**Characteristics:**
- Polished, radio-ready production
- Strong hooks and memorable choruses
- Verse-chorus-verse structures
- Wide range of subgenres (arena rock, indie, synth-pop)

**Common tags:** pop, rock, mainstream, catchy, uplifting, guitar-driven

For detailed subgenres, see `references/genre-deep-dive.md` → Western Pop, Western Rock sections.

### EDM / Electronic Dance

**Characteristics:**
- Four-on-the-floor or breakbeat rhythms
- Build-drop structures
- Synthesizer-driven
- Genre-specific tempos (house 120-130, dubstep 140, D&B 160-180)

**Common tags:** edm, electronic, dance, house, techno, bass heavy

For detailed subgenres (house, techno, dubstep, trance, etc.), see `references/genre-deep-dive.md` → EDM section.

### K-pop

**Characteristics:**
- Highly polished production
- Genre-blending (pop, hip-hop, R&B, EDM)
- Strong visual/choreography influence on song structure
- Mix of Korean and English lyrics

**Common tags:** k-pop, korean pop, polished, energetic, synchronized, hook-driven

For subgenres and common Korean phrases, see `references/genre-deep-dive.md` → K-pop section.

### Latin

**Characteristics:**
- Distinctive rhythms (dembow, clave, bossa)
- Spanish/Portuguese lyrics
- Strong percussion and bass
- Wide range from romantic to party

**Common tags:** latin, reggaeton, bachata, tropical, spanish, romantic

For subgenres and common Spanish phrases, see `references/genre-deep-dive.md` → Latin section.

## Song Structure Patterns

### Standard Pop Structure

```
[Intro] - 4-8 bars
[Verse 1] - 8-16 bars
[Pre-chorus] - 4-8 bars
[Chorus] - 8-16 bars
[Verse 2] - 8-16 bars
[Pre-chorus] - 4-8 bars
[Chorus] - 8-16 bars
[Bridge] - 8 bars
[Final Chorus] - 8-16 bars
[Outro] - 4-8 bars
```

### Japanese Pop Variations

**Anime opening style (90 seconds):**
```
[Intro] - Short instrumental hook
[Verse 1] - Quick setup
[Chorus] - Catchy, memorable
[Verse 2] - Development
[Chorus] - With variation
[Outro] - Instrumental fade or tag
```

**Ballad structure:**
```
[Intro] - Atmospheric, sets mood
[Verse 1] - Soft, intimate
[Verse 2] - Building slightly
[Chorus] - Emotional release
[Verse 3] - Deeper lyrics
[Chorus] - More intensity
[Bridge] - Key change or breakdown
[Final Chorus] - Full emotional climax
[Outro] - Gentle resolution
```

## Lyric Writing Techniques

### Japanese Lyrics

**Considerations:**
- Syllable count per line (7-5 or 5-7 patterns traditional)
- Particle placement affects rhythm
- Romanization for Suno input
- Mix of hiragana vocabulary and kanji concepts

**Emotional vocabulary:**
- 切ない (setsunai) - bittersweet longing
- 儚い (hakanai) - fleeting, ephemeral
- 懐かしい (natsukashii) - nostalgic
- 輝く (kagayaku) - to shine, sparkle

### English Lyrics

**Considerations:**
- Natural stress patterns
- Rhyme schemes (ABAB, AABB, ABCB)
- Syllable emphasis matching melody
- Internal rhymes for flow

### Mixed Language (Japanese-English)

**Effective techniques:**
- English in chorus hooks for catchiness
- Japanese verses for emotional depth
- Code-switching at phrase boundaries
- Consistent language per section

## Mood-to-Style Mapping

| Mood | Tempo | Key Feel | Tags |
|------|-------|----------|------|
| Upbeat | 120-140 BPM | Major | energetic, bright, cheerful, danceable |
| Melancholic | 70-90 BPM | Minor | sad, emotional, yearning, bittersweet |
| Energetic | 140-170 BPM | Major/Power | driving, intense, powerful, anthemic |
| Dreamy | 80-100 BPM | Major 7ths | atmospheric, ethereal, soft, floating |
| Intense | 130-160 BPM | Minor | dramatic, powerful, dark, cinematic |
| Chill | 85-110 BPM | Major | relaxed, smooth, laid-back, groovy |

## Vocal Specifications

### Female Vocals

**Soft/Gentle:** soft female vocals, breathy, intimate, gentle voice
**Powerful:** female belting, powerful vocals, strong voice, emotional delivery
**Cute/Idol:** cute vocals, bright voice, idol style, youthful

### Male Vocals

**Soft/Gentle:** soft male vocals, tender, warm voice, gentle delivery
**Powerful:** male belting, rock vocals, powerful, passionate
**Low/Smooth:** deep voice, smooth baritone, rich vocals

### Special Styles

**Duet:** male and female duet, harmonies, call and response
**Choir:** choir vocals, layered harmonies, group vocals
**Synth/Vocaloid:** vocaloid style, synthesized vocals, electronic voice

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

Apply these proven techniques for more memorable, emotionally resonant songs:

### Hook-First Composition

Design the most memorable part first (usually chorus hook), then build around it:
1. Write the chorus hook (melodic, lyrical, or rhythmic)
2. Test memorability - can you hum it after one listen?
3. Build verses that create anticipation for the hook
4. Use pre-chorus to build tension before hook release

### Tension & Release

Structure emotional dynamics throughout the song:

```
Low Tension → Building → Peak → Release
[Verse]      [Pre-Chorus] [Chorus] [Post-Chorus]
```

**Build tension with:** rising pitch, added layers, syncopation, harmonic tension
**Release tension with:** landing on tonic, full instrumentation, longer notes

### Three-Element Arrangement

Limit to three main elements for clarity and flexibility:

| Element | Role | Example |
|---------|------|---------|
| A | Main melody | Vocals, lead line |
| B | Counter-melody | Pads, strings |
| C | Rhythmic foundation | Bass, drums |

**Section combinations:**
- Verse: A + C (vocals over rhythm)
- Chorus: A + B + C (full impact)
- Bridge: B + C (contrast, rest vocals)

For detailed techniques including emotional authenticity and rhythmic variation, see `references/pro-techniques.md`.

## Production Tag Selection Guide

Select production tags based on genre and mood:

| Genre/Mood | Recommended Production Tags |
|------------|----------------------------|
| Ballad | reverb-heavy, intimate, dynamic, piano-driven |
| J-pop Energetic | polished, compressed, crisp drums, layered synths |
| EDM/Dance | side-chained bass, wide stereo, compressed, 808 bass |
| Lo-fi/Chill | lo-fi, warm, vinyl texture, relaxed mix |
| Rock/Anthem | powerful, stadium reverb, driving drums, guitar-forward |
| Dreamy/Atmospheric | reverb-heavy, wide stereo, ethereal, floating pads |
| Intense/Cinematic | epic, orchestral, dynamic, building, dramatic |

**By Energy Level:**
- Low: intimate, dry vocal, minimal, stripped
- Medium: balanced mix, natural reverb, full arrangement
- High: compressed, punchy, layered, side-chained, crisp

## Output Format

When composing songs, generate each song with:

```markdown
## Song: [Creative Title]

### Style Prompt
(Descriptive prose for Suno's "Style of Music" field. Combine: genre, subgenre/era,
tempo feel, vocal style, key instruments, production tags, mood descriptors.
Target 8-15 elements. Copy-paste ready.)

### Lyrics

[Intro: Instrument/mood description]
(instrumental direction or opening lyrics)

[Verse 1][vocal-direction]
(lyrics)

[Pre-Chorus][building]
(lyrics)

[Chorus][Mood: emotion][Arrangement: instruments]
(lyrics)

[Verse 2][vocal-direction][arrangement notes]
(lyrics)

[Bridge][Mood: start → end][Arrangement: stripped/full]
(lyrics)

[Final Chorus][peak-intensity markers]
(lyrics)

[Outro: fade/end description]
(closing)

### Specifications
- **Tempo:** [BPM or tempo feel]
- **Vocal:** [type, style, and progression]
- **Mood Arc:** [opening → middle → climax]
- **Key Instruments:** [by prominence]
- **Production Style:** [aesthetic and key effects]
```

**Copy-Paste Guide:**
1. **Style Prompt** → Suno's "Style of Music" field
2. **Lyrics** (with all [bracket] tags) → Suno's "Lyrics" field
3. **Specifications** → Reference for tempo lock and settings

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/pro-techniques.md`** - Hook-first composition, tension/release, three-element arrangement, emotional authenticity
- **`references/suno-metatags.md`** - Complete Suno v5 metatags, structure tags, vocal styles, production tags
- **`references/genre-deep-dive.md`** - Extended genre conventions and subgenres
- **`references/japanese-lyric-patterns.md`** - Japanese lyric writing patterns and vocabulary
- **`references/album-composition.md`** - Album coherence, arc patterns, track roles
- **`references/variation-patterns.md`** - Transformation matrices for song variations
- **`references/continuation-patterns.md`** - Callback techniques, narrative bridges for song continuations

### Working with User Preferences

When composing, check for user preferences in `.claude/suno-composer.local.md`:
- Favorite genres and artists inform style choices
- Preferred vocal types guide voice selection
- Mood tendencies shape emotional direction
- Language preferences determine lyric language

Blend user preferences with session-specific requests for personalized results.

## Workflow Modes

The song-composition skill supports multiple workflow modes:

### Standard Mode
Default single or batch song generation. See main documentation above.

### Album Mode
Generate thematically coherent multi-track albums. Reference: `references/album-composition.md`

Key concepts:
- **Thematic Anchor:** Shared conceptual thread across tracks
- **Sonic Palette:** Constrained but varied production elements
- **Arc Structure:** Journey, concept, or mood exploration patterns
- **Track Roles:** Opener, journey, peak, descent, closer

### Variation Mode
Generate transformed versions of a source song. Reference: `references/variation-patterns.md`

Variation types:
- **Acoustic:** Organic, intimate, stripped arrangement
- **Remix:** Electronic, dance transformation
- **Stripped:** Minimal, vocal showcase
- **Extended:** Full arrangement with added sections
- **Cinematic:** Orchestral, epic treatment

### Extend Mode
Generate narratively connected songs. Reference: `references/continuation-patterns.md`

Continuation types:
- **Sequel:** Story continues forward
- **Prequel:** Origin story
- **Response:** Answer from different perspective
- **Alternate POV:** Same events, different narrator
- **Epilogue:** Reflection from distance
