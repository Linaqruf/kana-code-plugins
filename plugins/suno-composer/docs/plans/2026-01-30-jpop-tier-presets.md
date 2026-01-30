# Japanese Music Tier Presets

**Date:** 2026-01-30
**Status:** Ready for Review
**Version:** 1.2

## Overview

A comprehensive preset system for Japanese music that provides:
1. **Quick reference shortcuts** - User says "anisong" → gets full style preset
2. **Expanded artist profiles** - Add more Japanese artists with tier categorization
3. **Full style presets** - Complete packages with genre + artists + metatags + vocal style + production

## Problem

The current artist profile system is powerful but requires users to know specific artist names. Many users think in broader categories:
- "I want something that sounds like an anime opening"
- "Give me that viral J-pop sound"
- "Something for normie Japanese pop fans"
- "Underground doujin style"

These mental categories represent distinct "tiers" or "layers" of the Japanese music ecosystem, each with characteristic sounds, production styles, and target audiences.

## Solution

A tiered preset system that:
1. **Auto-applies metatags** based on ecosystem layer
2. **Suggests representative artists** for each tier
3. **Provides full style prompts** ready to paste into Suno
4. **Categorizes existing/new artist profiles** by tier

## Tier Taxonomy

### Tier 1: Anisong (Anime Song)

**Characteristics:** Purpose-built for anime openings/endings. Dramatic builds, catchy hooks, high energy, designed to match visual cuts.

**Quick Reference:**
| Element | Value |
|---------|-------|
| **Aliases** | `anisong`, `anime`, `anime-op`, `anime-ed`, `op`, `ed` |
| **Tempo** | 140-180 BPM |
| **Vocal** | Powerful, clear, wide range, emotional belting |
| **Mood** | Inspiring, intense, triumphant, passionate |

**Auto-apply Metatags:**
```
[Anime OP] [J-rock] [Dramatic Build] [Catchy Hook] [High Energy]
[Powerful Vocals] [90-second structure awareness]
```

**Full Style Preset:**
```
J-rock anime opening, 160 bpm high energy, powerful female vocals with emotional
belting and wide range, guitar-forward with synth accents, punchy arena-ready mix,
dramatic builds matching visual cuts, strong hook in first 15 seconds,
emotion arc: determination → struggle → triumphant breakthrough
```

**Production Elements:**
- Guitar-forward with synth accents
- Punchy, arena-ready mix
- Dynamic builds matching anime cuts
- Strong hook in first 15 seconds

**Representative Artists:**

| Artist | Specialty | Example Songs |
|--------|-----------|---------------|
| LiSA | Power rock, belting | Gurenge, Homura |
| Aimer | Emotional ballads, husky voice | Brave Shine, Kataomoi |
| FLOW | Energetic rock, group vocals | GO!!!, Colors |
| TK from Ling Tosite Sigure | Complex, atmospheric | Unravel, Abnormalize |
| ReoNa | Dark, emotional | ANIMA, Forget-me-not |
| SID | Visual-kei influenced | Uso, Rain |
| MAN WITH A MISSION | Wolf-themed rock | Raise Your Flag |
| SPYAIR | Anthemic rock | Imagination, Sakura Mitsutsuki |

**Artist Profiles to Add:** TK from Ling Tosite Sigure, ReoNa, SID, MAN WITH A MISSION, SPYAIR

---

### Tier 2: Surface J-pop (Viral/Producer Scene)

**Characteristics:** Viral hits with complex rhythms, often narrative-driven. Includes ex-Vocaloid producers and utaite origins. The sound that defines 2020s Japanese pop globally.

**Quick Reference:**
| Element | Value |
|---------|-------|
| **Aliases** | `surface`, `viral`, `producer`, `utaite`, `vocaloid-scene` |
| **Tempo** | 120-180 BPM (varied, often complex) |
| **Vocal** | Fast runs, clear enunciation, emotional, distinctive |
| **Mood** | Energetic, melancholic undertones, narrative |

**Auto-apply Metatags:**
```
[J-pop] [Vocaloid-influenced] [Complex Rhythm] [Narrative Lyrics]
[Viral Hook] [Fast Melodic Runs] [Layered Synths]
```

**Full Style Preset:**
```
J-pop electronic synth-pop, 150 bpm driving tempo, female vocals with clear
enunciation and fast melodic runs, piano and synthesizer-driven with electronic
drums, polished compressed mix with layered synths, complex rhythmic patterns,
narrative storytelling in lyrics, emotion arc: discovery → momentum → resolution
```

**Production Elements:**
- Polished, compressed mix
- Piano and synth-driven
- Complex time signatures or rhythmic patterns
- Storytelling in lyrics

**Representative Artists:**

| Artist | Specialty | Example Songs |
|--------|-----------|---------------|
| YOASOBI | Novel adaptations, fast runs | Yoru ni Kakeru, Idol |
| Ado | Powerful/chaotic, extreme range | Usseewa, Odo |
| Kenshi Yonezu | Art pop, distinctive | Lemon, KICK BACK |
| Eve | Art rock, storytelling | Kaikai Kitan, Drama |
| Zutomayo | Experimental, playful | Kan Saete Kuyashiiwa |
| Reol | EDM-influenced, versatile | HYPE MODE, Give me a break |
| Vaundy | R&B-influenced, groovy | Odoriko, Hadaka no Yuusha |
| TUYU | Emotional rock, raw | Iya Iya, Loser Girl |

**Note:** Many artists in this tier came from Vocaloid/utaite scene. The line has blurred as they've gone mainstream. "Surface" = they've surfaced from underground to mainstream visibility.

**Artist Profiles to Add:** TUYU profile exists but check for completeness

---

### Tier 3: Mainstream J-pop (Radio-friendly)

**Characteristics:** Mass appeal, band-driven or singer-songwriter, radio-friendly. The sound normie Japanese listeners know and love.

**Quick Reference:**
| Element | Value |
|---------|-------|
| **Aliases** | `mainstream`, `normie`, `radio`, `band` |
| **Tempo** | 80-140 BPM (mid-tempo comfort zone) |
| **Vocal** | Smooth, relatable, sing-along friendly |
| **Mood** | Warm, accessible, emotional but not chaotic |

**Auto-apply Metatags:**
```
[J-pop] [Band Sound] [Radio-friendly] [Sing-along Chorus]
[Accessible] [Warm Production] [Relatable]
```

**Full Style Preset:**
```
J-pop band sound, 110 bpm mid-tempo, smooth male vocals with emotional delivery
and clear falsetto, guitar bass drums and piano, clean balanced mix with warm
production, straightforward song structure, sing-along chorus,
emotion arc: everyday moment → reflection → hopeful resolution
```

**Production Elements:**
- Clean, balanced mix
- Band instrumentation (guitar, bass, drums, keys)
- Straightforward song structures
- Emotional but not chaotic

**Representative Artists:**

| Artist | Specialty | Example Songs |
|--------|-----------|---------------|
| Official HIGE DANdism | Piano pop, falsetto | Pretender, Subtitle |
| Aimyon | Singer-songwriter, conversational | Marigold, Harunohi |
| back number | Heartbreak ballads | Christmas Song, Takane no Hanako-san |
| Mrs. GREEN APPLE | Upbeat pop-rock | Inferno, Soranji |
| Spitz | Jangly pop-rock, gentle | Robinson, Sora mo Toberu Hazu |
| Mr.Children | Arena rock, anthemic | Sign, HANABI |
| Kobukuro | Folk-pop duo | Tsubomi, Sakura |
| Yuzu | Acoustic pop duo | Natsuiro, Eikoueno Kakehashi |
| Masaki Suda | Actor-singer, emotional | Sayonara Elegy |

**Artist Profiles to Add:** Yuzu, Masaki Suda

---

### Tier 4: Doujin/Underground

**Characteristics:** Convention scene, Touhou arranges, underground electronic, niche communities. High production skill, niche appeal.

**Quick Reference:**
| Element | Value |
|---------|-------|
| **Aliases** | `doujin`, `underground`, `touhou`, `convention`, `comiket` |
| **Tempo** | 140-200+ BPM (often very fast) |
| **Vocal** | Varies by subgenre (operatic, high-pitched, aggressive) |
| **Mood** | Dramatic, niche, intense, community-driven |

**Auto-apply Metatags:**
```
[Doujin] [High Production Value] [Convention Scene] [Niche]
```

**Production Elements:**
- Varies widely (orchestral, denpa, eurobeat, metal)
- Often very high technical skill
- Genre-specific production (see subgenres below)

#### Subgenre: Symphonic/Gothic

**Auto-apply Metatags:** `[Orchestral] [Gothic] [Dramatic] [Epic] [Symphonic Metal]`

**Full Style Preset:**
```
Doujin symphonic gothic metal, 160 bpm dramatic, dual female operatic vocals
with powerful harmonies, piano organ violin electric guitar and full orchestra,
symphonic layered production with gothic atmosphere, fantasy narrative themes,
emotion arc: tragic setup → emotional climax → bittersweet resolution
```

**Representative Artists:** Ariabl'eyeS, Sound Horizon, -LostFairy-, KOKIA, Kalafina

#### Subgenre: Denpa/Chaotic

**Auto-apply Metatags:** `[Denpa] [Fast] [High-pitched] [Chaotic] [Cute] [Electronic]`

**Full Style Preset:**
```
Denpa electronic, 180 bpm hyper fast, high-pitched cute female vocals with
rapid delivery, heavy synths and electronic drums, chaotic layered production,
otaku themes with playful chaos, emotion arc: cute → intense → overwhelming cute
```

**Representative Artists:** IOSYS, MOSAIC.WAV, COOL&CREATE, ARM (IOSYS)

#### Subgenre: Eurobeat/Para Para

**Auto-apply Metatags:** `[Eurobeat] [Fast] [Driving] [Synth-heavy] [Initial D]`

**Full Style Preset:**
```
Eurobeat, 155 bpm driving energy, powerful female vocals with Italian disco
influence, heavy synthesizer leads and electronic drums, punchy compressed mix,
driving energy for night racing, emotion arc: adrenaline → peak → cruise
```

**Representative Artists:** A-One, Eurobeat Brony, various Initial D soundtrack artists

#### Subgenre: Touhou Arrange

**Auto-apply Metatags:** `[Touhou] [Arrange] [ZUN-style] [Melodic]`

**Full Style Preset:**
```
Touhou arrange, 150 bpm energetic, [varies by style - see above subgenres],
respectful of original ZUN melodies while adding [style] elements,
emotion arc follows original stage theme narrative
```

**Representative Artists:** Alstroemeria Records, IOSYS, COOL&CREATE, dBu music, SYNC.ART'S

**Artist Profiles to Add:** Sound Horizon, IOSYS (circle), COOL&CREATE (circle)

---

## User Experience

### Invocation: Pure Natural Language

Users say tier keywords anywhere in their request. No special syntax required.

| Tier | Keywords that trigger |
|------|----------------------|
| Anisong | `anisong`, `anime`, `anime opening`, `anime op`, `anime ed` |
| Surface | `surface`, `viral`, `viral jpop`, `producer scene`, `utaite` |
| Mainstream | `mainstream`, `normie`, `normie jpop`, `radio jpop` |
| Doujin | `doujin`, `touhou`, `underground`, `convention`, `comiket` |

**Examples:**
```
/suno anisong about never giving up
/suno viral jpop about running through the city at night
/suno mainstream romantic ballad for wedding
/suno doujin symphonic fantasy battle
```

Keyword detection is case-insensitive and works anywhere in the prompt.

### Tier + Artist Combination

When both tier and artist are specified, they merge (tier as base, artist refines):

```
/suno anisong like Aimer about farewell
```

**Merge logic:**
1. Start with tier's auto-tags: `[Anime OP] [J-rock] [Dramatic Build] [Catchy Hook]`
2. Add artist's characteristics: `husky vocals`, `cinematic`, `ballad tendency`
3. Artist overrides tier for conflicts (Aimer's 70-130 BPM overrides anisong's 140-180)

**Resulting style prompt:**
```
J-rock anime opening with cinematic ballad influence, 120 bpm dramatic,
husky female vocals with emotional depth building to powerful delivery,
guitar-forward with orchestral strings, atmospheric reverb-heavy mix,
emotion arc: quiet longing → rising tension → bittersweet farewell
```

**Cross-tier artist usage is valid:**

YOASOBI is naturally "surface" tier. If user says:
```
/suno anisong like YOASOBI about friendship
```

This blends anisong's dramatic builds with YOASOBI's synth-driven production. No warnings - user knows what they want.

### Discovery: On-Demand Only

No automatic tier picker. Users learn about tiers through:
- Documentation (SKILL.md, README)
- Asking directly: "what J-pop styles can I use?"
- Seeing examples

### Scope: J-pop Ecosystem Only

These tiers map the Japanese music ecosystem specifically. Not a universal genre system.

**In scope:** Anisong, Surface J-pop, Mainstream J-pop, Doujin
**Out of scope:** K-pop tiers, Western genre tiers, EDM/Latin tiers

Other genres (K-pop, Western, etc.) use existing `genre-deep-dive.md` handling, not the tier system.

## Technical Design

### New Reference File

Create `references/jpop-tiers.md`:

```markdown
# Japanese Music Tier System

## Tier: Anisong
**Aliases:** anisong, anime, anime-song, anime-op, anime-ed, op, ed
**Auto-tags:** [Anime OP] [J-rock] [Dramatic Build] [Catchy Hook]
**Tempo:** 140-180 BPM
**Production:** guitar-forward, punchy, dynamic builds
**Artists:** LiSA, Aimer, FLOW, TK, ReoNa, SID

## Tier: Surface
**Aliases:** surface, viral, producer, utaite, vocaloid-scene
**Auto-tags:** [J-pop] [Vocaloid-influenced] [Complex Rhythm] [Narrative]
...
```

### Tier Profile Schema

```typescript
interface TierProfile {
  name: string;                    // "Anisong"
  aliases: string[];               // ["anisong", "anime-op", ...]

  autoTags: string[];              // Auto-applied metatags
  tempoRange: { min: number; max: number };

  production: {
    description: string;           // Prose description
    keyElements: string[];         // ["guitar-forward", "punchy"]
  };

  representativeArtists: string[]; // For discovery/examples
  subgenres?: SubgenreVariant[];   // For tiers with variants (doujin)
}

interface SubgenreVariant {
  name: string;                    // "symphonic"
  additionalTags: string[];        // Extra tags for this variant
}
```

### Command Integration

Extend `commands/suno.md` Step 2:

1. Scan input for tier keywords (case-insensitive)
2. If tier keyword found, load tier profile
3. If artist reference also found, merge (tier base + artist refinements)
4. Apply merged profile to style prompt generation
5. Continue with normal flow (theme, etc.)

**Keyword matching:** Simple substring match against alias list. "anime opening" matches anisong tier, "viral jpop" matches surface tier.

### Interaction with Artist Profiles

**Tier + Artist combination:**
- Tier provides base metatags
- Artist profile provides specific refinements
- Artist takes precedence for overlapping attributes

**Example:** `/suno tier:anisong like Aimer`
- From tier: `[Anime OP] [Dramatic Build] [High Energy]`
- From Aimer profile: `[Husky Vocals] [Ballad] [Cinematic]`
- Merged: `[Anime OP] [Cinematic] [Husky Vocals] [Dramatic Build]`

## Artist Profile Categorization

Add `tier` field to existing artist profiles in `references/artist-profiles.md`:

```markdown
## YOASOBI
- **Tier:** surface
- **Aliases:** yoasobi, ヨアソビ, Ayase, ikura
...
```

### Existing Artists by Tier

| Tier | Existing Profiles |
|------|-------------------|
| **Anisong** | LiSA, Aimer |
| **Surface** | YOASOBI, Yorushika, Ado, Eve, Kenshi Yonezu, Zutomayo, TUYU, Reol, Vaundy, Hatsune Miku, Kasane Teto |
| **Mainstream** | Official HIGE DANdism, Aimyon, back number, Mrs. GREEN APPLE, RADWIMPS, King Gnu, Fujii Kaze, imase, Bump of Chicken, Spitz, Mr.Children, Kobukuro |
| **Doujin** | Ariabl'eyeS, Yuki Kajiura |
| **Crossover** | Creepy Nuts (mainstream + hip-hop), Tatsuro Yamashita (city pop legacy) |

### New Artists to Add

| Tier | Artists to Add |
|------|----------------|
| **Anisong** | TK from Ling Tosite Sigure, ReoNa, SID, MAN WITH A MISSION, SPYAIR, FLOW |
| **Surface** | (mostly covered) |
| **Mainstream** | Yuzu, Masaki Suda |
| **Doujin** | Sound Horizon, IOSYS (circle profile), COOL&CREATE (circle profile) |

## File Changes

| File | Change |
|------|--------|
| `references/jpop-tiers.md` | NEW - Tier profile database with full presets |
| `references/artist-profiles.md` | ADD `tier` field to existing profiles, ADD new artist profiles |
| `commands/suno.md` | Add tier detection and parsing |
| `skills/song-composition/SKILL.md` | Document tier feature |
| `SPEC.md` | Add to v4.5 features |

## Implementation Phases

### Phase 1: Tier Reference File
- Create `references/jpop-tiers.md` with all 4 tiers
- Include full style presets for each tier
- Add subgenre variants for Doujin tier

### Phase 2: Artist Profile Updates
- Add `tier` field to all existing Japanese artist profiles
- Add new artist profiles for missing tier representatives:
  - Anisong: TK, ReoNa, SID, MAN WITH A MISSION, SPYAIR, FLOW
  - Mainstream: Yuzu, Masaki Suda
  - Doujin: Sound Horizon

### Phase 3: Command Integration
- Add tier parsing to `commands/suno.md`
- Implement tier profile lookup
- Add tier selection question to fallback flow
- Implement tier + artist merge logic

### Phase 4: Documentation
- Update `SKILL.md` with tier feature
- Update `SPEC.md` with v4.5 features
- Add usage examples

## Future Considerations (Out of Scope)

- **Era-based modifiers:** 90s J-pop, 2000s, etc. (could layer on top of tiers)
- **Idol tier:** 48G, Sakamichi, WACK (complex, needs own spec)
- **Visual kei tier:** Distinct enough to warrant separate tier
- **City pop tier:** Revival sound distinct from mainstream
- **Cross-tier blends:** "anisong but doujin production"

## Resolved Questions

1. ~~Should tier detection be case-sensitive?~~ → **No**, case-insensitive matching
2. ~~Should we detect "anime opening" vs "anime ending" separately?~~ → **Same tier**, both are anisong
3. ~~How to handle "vocaloid" as input?~~ → **Not a tier keyword**. "vocaloid" triggers existing Hatsune Miku artist profile, not surface tier. User can say "viral jpop" or "surface" to get the tier.
4. ~~Should there be a tier picker question?~~ → **No**, discovery is on-demand only
5. ~~Should tier syntax use a prefix?~~ → **No**, pure natural language detection

## Open Questions

1. Should doujin subgenres (symphonic, denpa, eurobeat) have their own keywords, or require "doujin symphonic"?

## Success Criteria

- User can invoke `/suno tier:anisong` and get anime-OP-appropriate output
- All 4 tiers recognized with aliases
- Tier + artist combinations work smoothly
- Unknown tier names fall back gracefully to artist lookup or presets
