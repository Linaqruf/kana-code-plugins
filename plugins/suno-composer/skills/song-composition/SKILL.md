---
name: song-composition
description: This skill should be used when the user wants to compose songs for Suno AI, write lyrics, create style prompts, or generate Suno v5 metatags. Supports J-pop, K-pop, EDM, ballads, rock, and Latin genres, plus album/EP composition, acoustic or remix variations, and song continuations. Also handles reference-based composition ("like YOASOBI", "in the style of Aimer"). Triggers on "write a song", "make a song", "Suno prompt", "Suno metatags", "Suno v5", "style of music", "song lyrics", "Suno AI", "acoustic version", "remix version", "create an album", "extend this song", "compose music", "generate lyrics", "like [artist]", "in the style of", "/suno".
---

# Song Composition for Suno AI

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

Apply these J-pop conventions:
- Use catchy melodic hooks
- Include complex chord progressions (borrowed chords work well)
- Mix verse-chorus with bridge sections
- Add dramatic key changes for impact
- Blend electronic and acoustic elements

**Common tags:** j-pop, japanese pop, catchy melody, emotional, anime

### Doujin/Vocaloid Style

Apply these Doujin/Vocaloid conventions:
- Use electronic-heavy production
- Set fast tempos (140-180 BPM)
- Include intricate melodic runs
- Build synth-driven arrangements
- Create dramatic dynamic shifts

**Common tags:** vocaloid style, electronic, synthesizer, fast tempo, dramatic, anime

### Ballad

Apply these ballad conventions:
- Set slow to mid tempo (60-90 BPM)
- Use emotional, expressive vocals
- Lead with piano or guitar
- Build to emotional climax
- Keep percussion minimal in verses

**Common tags:** ballad, emotional, piano, slow tempo, heartfelt, orchestral

### Rock/J-rock

Apply these rock conventions:
- Lead with guitar-driven arrangements
- Establish strong rhythmic foundation
- Use powerful vocals
- Create dynamic verse-chorus contrast
- Include guitar solos where appropriate

**Common tags:** j-rock, rock, electric guitar, powerful vocals, driving drums

### Western Pop/Rock

Apply these Western pop/rock conventions:
- Use polished, radio-ready production
- Create strong hooks and memorable choruses
- Follow verse-chorus-verse structures
- Draw from subgenres (arena rock, indie, synth-pop)

**Common tags:** pop, rock, mainstream, catchy, uplifting, guitar-driven

For detailed subgenres, see `references/genre-deep-dive.md` (Western Pop, Western Rock sections).

### EDM / Electronic Dance

Apply these EDM conventions:
- Use four-on-the-floor or breakbeat rhythms
- Structure around build-drop patterns
- Lead with synthesizers
- Match tempo to subgenre (house 120-130, dubstep 140, D&B 160-180)

**Common tags:** edm, electronic, dance, house, techno, bass heavy

For detailed subgenres (house, techno, dubstep, trance, etc.), see `references/genre-deep-dive.md` (EDM section).

### K-pop

Apply these K-pop conventions:
- Use highly polished production
- Blend genres (pop, hip-hop, R&B, EDM)
- Structure for visual/choreography impact
- Mix Korean and English lyrics

**Common tags:** k-pop, korean pop, polished, energetic, synchronized, hook-driven

For subgenres and common Korean phrases, see `references/genre-deep-dive.md` (K-pop section).

### Latin

Apply these Latin conventions:
- Use distinctive rhythms (dembow, clave, bossa)
- Write in Spanish/Portuguese
- Emphasize percussion and bass
- Range from romantic to party styles

**Common tags:** latin, reggaeton, bachata, tropical, spanish, romantic

For subgenres and common Spanish phrases, see `references/genre-deep-dive.md` (Latin section).

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

When writing Japanese lyrics:
- Count syllables per line (use 7-5 or 5-7 patterns for traditional feel)
- Place particles carefully to maintain rhythm
- Mix hiragana vocabulary with kanji concepts

**Use emotional vocabulary:**
- 切ない (setsunai) - bittersweet longing
- 儚い (hakanai) - fleeting, ephemeral
- 懐かしい (natsukashii) - nostalgic
- 輝く (kagayaku) - to shine, sparkle

### English Lyrics

When writing English lyrics:
- Match natural stress patterns to the melody
- Use rhyme schemes (ABAB, AABB, ABCB)
- Align syllable emphasis with melodic accents
- Add internal rhymes for flow

### Mixed Language (Japanese-English)

When mixing Japanese and English:
- Place English in chorus hooks for catchiness
- Use Japanese verses for emotional depth
- Switch languages at phrase boundaries
- Keep language consistent within sections

## Mood-to-Style Mapping

| Mood | Tempo | Key Feel | Tags |
|------|-------|----------|------|
| Upbeat | 120-140 BPM | Major | energetic, bright, cheerful, danceable |
| Melancholic | 70-90 BPM | Minor | sad, emotional, yearning, bittersweet |
| Energetic | 140-170 BPM | Major/Power | driving, intense, powerful, anthemic |
| Dreamy | 80-100 BPM | Major 7ths | atmospheric, ethereal, soft, floating |
| Intense | 130-160 BPM | Minor | dramatic, powerful, dark, cinematic |
| Chill | 85-110 BPM | Major | relaxed, smooth, laid-back, groovy |

## Reference-Based Composition

### Using Artist References

Users can specify a reference artist instead of mood presets:

```
/suno like YOASOBI about finding hope
/suno in the style of Aimer
/suno Eve-style energetic
```

### How It Works

1. Command detects reference pattern in arguments
2. Looks up artist in `references/artist-profiles.md`
3. Extracts: genre, tempo, vocal style, instruments, production, mood
4. Generates style prompt with artist name + descriptors

### Style Prompt from Reference

**Input:** `/suno like YOASOBI about finding hope`

**Generated style prompt:**
```
YOASOBI-inspired j-pop electronic synth-pop, 140 bpm driving tempo,
female vocals with clear enunciation and fast melodic runs,
synthesizer and piano-driven with electronic drums, polished compressed mix,
emotion arc: searching uncertainty → building momentum → hopeful breakthrough
```

**Note:** Artist name is included for Suno to potentially recognize. If Suno ignores or rejects it, user can remove the "[Artist]-inspired" part and retry - descriptors remain as fallback.

### Supported Artists

See `references/artist-profiles.md` for full list. Initial coverage includes:
- YOASOBI, Yorushika, Ado, Eve, Kenshi Yonezu
- LiSA, Aimer, Official HIGE DANdism, King Gnu, Vaundy
- RADWIMPS, Mrs. GREEN APPLE, Aimyon, back number, BUMP OF CHICKEN
- Fujii Kaze, imase, TUYU, Zutomayo, Creepy Nuts

### Unknown Artists

If artist not in database, user can:
1. Describe the style manually
2. Fall back to mood presets

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

Apply the sparse tagging principle (see "The Sparse Tagging Principle" and "When to Tag" sections above).

**Quick reference:**
- Tag only 3-4 inflection points (intro, breakdown, build, final chorus)
- Use technique cues (`[stripped]`, `[key change up]`), not emotion words
- Put emotion arc in style prompt, not per-section tags
- Most sections need only the section marker - structure creates contrast

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
- **`references/artist-profiles.md`** - Artist characteristics for reference-based composition

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
