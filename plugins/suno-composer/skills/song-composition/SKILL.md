---
name: song-composition
description: This skill should be used when the user asks to "compose a song", "write lyrics", "create Suno prompts", "generate song ideas", "make a J-pop song", "write music for Suno", or mentions Suno AI, song composition, or lyric writing. Provides comprehensive knowledge about Suno v5 style tags, genre conventions, song structures, and lyric writing techniques.
version: 1.0.0
---

# Song Composition for Suno AI

## Overview

This skill provides specialized knowledge for composing songs optimized for Suno AI music generation. It covers style tag syntax, genre conventions, song structure patterns, and lyric writing techniques across multiple languages and styles.

## Suno v5 Style Tags

### Tag Format

Suno v5 uses comma-separated style tags in the "Style of Music" field. Effective tags combine:

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

### Tag Best Practices

- Place most important genre tags first
- Use 6-12 tags for optimal results
- Avoid contradictory tags (e.g., "calm" and "intense")
- Include vocal descriptor for consistent voice
- Specify tempo feel (fast, mid-tempo, slow) when important

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

## Output Format

When composing songs, generate each song with:

```markdown
## Song: [Creative Title]

### Lyrics

[Verse 1]
(lyrics here)

[Pre-chorus]
(lyrics here)

[Chorus]
(lyrics here)

[Verse 2]
(lyrics here)

[Chorus]
(lyrics here)

[Bridge]
(lyrics here)

[Final Chorus]
(lyrics here)

### Suno Style Tags
(comma-separated tags for copy-paste)

### Specifications
- **Tempo:** [BPM or range]
- **Vocal:** [type and style]
- **Mood:** [primary mood]
- **Arrangement:** [key instruments and production notes]
```

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/genre-deep-dive.md`** - Extended genre conventions and subgenres
- **`references/japanese-lyric-patterns.md`** - Japanese lyric writing patterns and vocabulary

### Working with User Preferences

When composing, check for user preferences in `.claude/suno-composer.local.md`:
- Favorite genres and artists inform style choices
- Preferred vocal types guide voice selection
- Mood tendencies shape emotional direction
- Language preferences determine lyric language

Blend user preferences with session-specific requests for personalized results.
