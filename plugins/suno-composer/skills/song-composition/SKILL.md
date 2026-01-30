---
name: song-composition
description: This skill should be used when the user wants to compose songs for Suno AI, write lyrics, create style prompts, or generate Suno v5 metatags. Supports J-pop, K-pop, EDM, ballads, rock, and Latin genres, plus album/EP composition, acoustic or remix variations, and song extensions. Triggers on "write a song", "Suno prompt", "Suno metatags", "style of music", "song lyrics", "Suno AI", "acoustic version", "remix version", "create an album", "extend this song", "compose music".
version: 4.3.0
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
7. **Emotion arc** (Suno V5 reads this well)

**Example Style Prompt:**
```
emotional j-pop ballad, anime soundtrack influence, slow tempo around 75 bpm,
soft female vocals building to powerful delivery, piano-driven with orchestral strings,
reverb-heavy atmospheric mix, bittersweet mood,
emotion arc: intimate verse → building anticipation → euphoric chorus → stripped reflection → triumphant finale
```

**Key insight:** Put the emotion journey in the style prompt, not in per-section lyric tags. Suno V5 handles this effectively.

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
- Mix of hiragana vocabulary and kanji concepts
- Romanization optional - can help Suno with pronunciation clarity

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

Apply these core techniques for memorable songs. For detailed exercises and advanced techniques, see `references/pro-techniques.md`.

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

## Output Formats

### Preview Format (Token-Efficient)

When generating song previews (before user confirmation), output metadata only:

```markdown
### Song [N]: [Title]
- **Genre/Style:** [primary genre, subgenre, key descriptors]
- **Tempo:** ~[BPM] BPM, [feel]
- **Vocal:** [type], [style description]
- **Structure:** [section flow, e.g., Intro → Verse → Pre-Chorus → Chorus → ...]
- **Theme:** [1-line description of emotional/narrative content]
- **Hook Concept:** [brief description of the chorus hook idea]
```

**Important:** Previews do NOT include full lyrics. This saves tokens by letting users confirm direction before full generation.

### Full Song Format (For File Output)

When composing full songs (after user confirmation), generate each song with:

```markdown
## Song: [Creative Title]

### Style Prompt
(Descriptive prose for Suno's "Style of Music" field. Include: genre, subgenre/era,
tempo feel, vocal style, key instruments, production tags, mood descriptors,
AND emotion arc. Target 8-15 elements. Copy-paste ready.)

Example:
emotional j-pop ballad, anime soundtrack influence, 75 bpm, soft female vocals
building to powerful delivery, piano-driven with orchestral strings, reverb-heavy,
emotion arc: intimate verse → building anticipation → euphoric chorus → stripped bridge → triumphant finale

### Lyrics

[Intro: Piano, atmospheric]
(instrumental)

[Verse 1]
(lyrics)

[Pre-Chorus]
(lyrics)

[Chorus]
(lyrics)

[Verse 2]
(lyrics)

[Breakdown][stripped, half-time]
(lyrics - contrast point, pull back before climax)

[Build]

[Final Chorus][key change up]
(lyrics)

[Outro]
(closing)

### Specifications
- **Tempo:** [BPM or tempo feel]
- **Vocal:** [type and style]
- **Key Instruments:** [by prominence]
- **Production Style:** [aesthetic and key effects]
- **Inflection Points:** [where the 3-4 technique tags are placed and why]
```

**Note:** Most sections have only the section marker. Tags appear only at inflection points (intro texture, breakdown contrast, build, final chorus peak).

### Lyric Tagging Guidelines

**Sparse tagging at inflection points.** Dynamics come from structure and contrast, not from describing every section.

**The 1-3-4 Rule:**
- **1** intro texture tag
- **3** technique tags max in the song body (breakdown, build, final chorus)
- **4** total inflection points maximum

**What creates great dynamics:**
```
✅ Sparse technique cues at key moments:
[Intro: Piano, atmospheric]
[Verse 1]
[Pre-Chorus]
[Chorus]
[Verse 2]
[Breakdown][stripped, half-time]
[Build]
[Final Chorus][key change up]
[Outro]
```

**What causes problems (avoid):**
```
❌ Tagging every section with emotion words:
[Verse 1][soft, intimate]
[Pre-Chorus][building]
[Chorus][powerful, soaring]
[Verse 2][tender, reflective]
[Bridge][vulnerable, stripped]
[Final Chorus][triumphant, explosive]
```

**Why sparse works better:**
- Verse/chorus contrast is built into the structure
- Pre-chorus already implies "building" - don't need to say it
- Emotion arc goes in style prompt where Suno V5 reads it
- Technique cues (`[half-time]`, `[key change]`) create actual dynamics
- Emotion words (`[triumphant]`, `[soaring]`) just add noise

**Dynamic Wave Pattern:**
```
Energy:  ▁▂▃▅▃▂▅▆▅▃▂▁
Section: I V1 PC C V2 PC C Br FC O
              ↑           ↑  ↑
           (no tag)    stripped key change
```
- Most sections need no tag - structure handles the energy
- Tag only where you need a TECHNIQUE change (breakdown, build, modulation)
- Bridge should pull back (stripped, vulnerable) before final push
- Final Chorus earns intensity through contrast, not accumulation

**Copy-Paste Guide:**
1. **Style Prompt** → Suno's "Style of Music" field
2. **Lyrics** (with all [bracket] tags) → Suno's "Lyrics" field
3. **Specifications** → Reference for tempo lock and settings

### Album Preview Format

```markdown
## Album: [Album Title]
**Concept:** [1-2 sentence description]
**Sonic Palette:** [core instruments, production style, tempo range]
**Arc:** [journey/concept/mood flow description]

### Track Listing Preview:
1. **[Title]** (Opener) - [genre], ~[BPM] BPM - [1-line theme]
2. **[Title]** (Journey) - [genre], ~[BPM] BPM - [1-line theme]
...
```

### Variation Preview Format

```markdown
## Source: [Original Title]
**Hook:** [core hook preserved across variations]
**Theme:** [central theme]

### Variation Previews:
1. **Acoustic Version** - ~[BPM] BPM, [key changes from original]
2. **Remix Version** - ~[BPM] BPM, [key changes from original]
...
```

### Continuation Preview Format

```markdown
## Continuation: [New Title] ([Type])
**Connection to Source:** [how it relates]
**Genre/Style:** [genre, key sonic DNA elements]
**Tempo:** ~[BPM] BPM
**Theme:** [1-line description]
**Planned Callbacks:** [2-3 callback concepts]
```

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
