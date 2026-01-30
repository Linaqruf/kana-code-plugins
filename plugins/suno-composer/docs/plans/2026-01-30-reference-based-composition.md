# Reference-Based Composition

**Date:** 2026-01-30
**Status:** Approved
**Version:** 1.0

## Overview

Add the ability to compose songs by referencing artists or songs. Instead of selecting from mood presets, users can say "like YOASOBI" or "in the style of Aimer" and have the composer translate that into appropriate Suno parameters.

## Problem

The current input flow uses preset mood options (Upbeat, Melancholic, Energetic, etc.) that don't capture nuanced musical ideas. Users often think in terms of "I want something like [artist]" but have no way to express that.

## Solution

A static artist profile database that maps artist names to their musical characteristics (genre, tempo, vocal style, production, etc.). When a reference is detected, the profile data informs style prompt generation.

## User Experience

### Input Methods

**Primary - Inline with command:**
```
/suno like YOASOBI about finding hope
/suno in the style of Aimer, melancholic ballad
/suno like Eve, energetic
```

**Fallback - Question during flow:**
```
/suno

> Do you have a reference artist or song?
  - Yes, let me specify → prompts for artist name
  - No, use mood presets → existing flow
```

### Output

Reference translates to style prompt with artist name + descriptors:

```
ariabl'eyes style, ethereal female vocals, atmospheric synth layers,
dreamy j-pop, 95 bpm floating tempo, reverb-heavy production,
emotion arc: searching → discovery → transcendence
```

If Suno rejects the artist name, user removes it and retries - descriptors remain as fallback.

## Technical Design

### Artist Profile Schema

```typescript
interface ArtistProfile {
  name: string;                    // "YOASOBI"
  aliases: string[];               // ["yoasobi", "ヨアソビ"]

  // Core characteristics
  genres: string[];                // ["j-pop", "electronic", "synth-pop"]
  tempoRange: { min: number; max: number };
  tempoFeel: string;               // "driving", "upbeat"

  // Vocal
  vocalType: "female" | "male" | "duet" | "group";
  vocalStyle: string[];            // ["clear", "fast melodic runs"]

  // Production
  keyInstruments: string[];        // ["synthesizer", "piano"]
  productionTags: string[];        // ["polished", "compressed"]

  // Songwriting
  themes: string[];                // ["narrative", "youth", "night"]
  moodRange: string[];             // ["energetic", "melancholic"]

  // Discovery
  similarTo: string[];             // ["Yorushika", "Ado"]
}
```

### File Format

Profiles stored as markdown in `references/artist-profiles.md`:

```markdown
## YOASOBI
- **Aliases:** yoasobi, ヨアソビ
- **Genre:** j-pop, electronic, synth-pop, vocaloid-influenced
- **Tempo:** 130-150 BPM, driving energy
- **Vocal:** female, clear enunciation, fast melodic runs, emotional
- **Instruments:** synthesizer, piano, electronic drums, bass
- **Production:** polished, compressed, layered synths, punchy mix
- **Themes:** narrative storytelling, youth, night, fleeting moments
- **Mood:** energetic, melancholic undertones, hopeful
- **Similar:** Yorushika, Ado, Eve, Kenshi Yonezu
```

### Reference Parsing

Command parses `$ARGUMENTS` for reference patterns:
- `like [artist]`
- `in the style of [artist]`
- `[artist]-style`
- `similar to [artist]`

Lookup is case-insensitive and checks aliases.

### Style Prompt Generation

When reference is matched:

1. Pull profile data (genre, tempo, vocal, instruments, production)
2. Include artist name at start (user can remove if Suno rejects)
3. Add descriptors as fallback
4. User's theme shapes the emotion arc
5. User can override any inferred parameter

**Example:**

User: `/suno like YOASOBI about finding hope`

Generated style prompt:
```
YOASOBI-inspired j-pop electronic synth-pop, 140 bpm driving tempo,
female vocals with clear enunciation and fast melodic runs,
synthesizer and piano-driven with electronic drums, polished compressed mix,
emotion arc: searching uncertainty → building momentum → hopeful breakthrough
```

### Unknown Artist Handling

If artist not found in database:

```
I don't have a profile for "[artist name]" yet.

Options:
1. Describe their style briefly (I'll use that)
2. Use mood presets instead
```

## File Changes

| File | Change |
|------|--------|
| `references/artist-profiles.md` | NEW - Artist profile database |
| `commands/suno.md` | Add reference parsing logic in Step 2 |
| `skills/song-composition/SKILL.md` | Document reference feature usage |
| `SPEC.md` | Add to v4.4 features |

## Initial Artist List

**20 J-pop artists for v1:**

1. YOASOBI
2. Yorushika
3. Ado
4. Eve
5. Kenshi Yonezu (米津玄師)
6. LiSA
7. Aimer
8. Official HIGE DANdism
9. King Gnu
10. Vaundy
11. RADWIMPS
12. Mrs. GREEN APPLE
13. Aimyon
14. back number
15. BUMP OF CHICKEN
16. Fujii Kaze
17. imase
18. TUYU (ツユ)
19. Zutomayo (ずっと真夜中でいいのに。)
20. Creepy Nuts

## Out of Scope (YAGNI)

- Web lookup for unknown artists
- Suno-safe flags (let user handle rejections)
- Song-specific profiles (just artists for now)
- Audio file analysis
- YouTube/Spotify URL parsing

## Implementation Phases

### Phase 1: Artist Database
- Create `references/artist-profiles.md`
- Research and document 20 artist profiles
- Define profile format and structure

### Phase 2: Command Integration
- Add reference parsing to `commands/suno.md`
- Implement profile lookup logic
- Add fallback question for no-argument invocation

### Phase 3: Style Generation
- Update style prompt generation to use profile data
- Include artist name + descriptors pattern
- Allow parameter overrides

### Phase 4: Documentation
- Update `SKILL.md` with reference feature
- Update `SPEC.md` with v4.4 features
- Add examples to README

## Success Criteria

- User can say `/suno like YOASOBI` and get appropriate style parameters
- All 20 initial artists are recognized (including aliases)
- Unknown artists gracefully fall back to description or presets
- Style prompts include both artist name and descriptors
