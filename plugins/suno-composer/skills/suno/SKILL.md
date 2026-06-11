---
name: suno
version: 6.0.0
description: This skill should be used when the user wants to compose songs for Suno AI, write lyrics, create style prompts, or generate Suno metatags. Supports J-pop, K-pop, EDM, ballads, rock, and Latin genres, plus album/EP composition, variations, and song continuations. Also handles reference-based composition ("like YOASOBI", "in the style of Aimer") and J-pop tier presets ("anisong", "mainstream", "doujin"). Triggers on "write a song", "Suno prompt", "Suno metatags", "style of music", "song lyrics", "Suno AI", "acoustic version", "create an album", "extend this song", "like [artist]", "in the style of", "/suno", "anisong", "doujin", "negative prompting", "ad-libs".
---

# Song Composition for Suno AI

Targets current Suno models (v5/v5.5). Where v5.5 behavior is unverified, guidance
says so and hedges rather than guessing.

## Creative Engine Role

Act as a **songwriter first**, not a rule-follower. The references in this skill are
a creative palette — inspiration, not prescription.

| Reference | Use it as... | NOT as... |
|-----------|--------------|-----------|
| Artist profiles | Vibe inspiration | Exact tag lookup |
| Genre conventions | Starting points | Rigid rules |
| Metatags | Toolkit of options | Required checklist |
| Tier presets | Creative directions | Auto-apply templates |

**Creative latitude:** Blend genres unexpectedly. Interpret "like [artist]" through
artistic essence, not exact specs. Break conventions when the song calls for it.
The Composition Rubric below is the **floor** (craft that must hold), never the
ceiling (taste stays yours).

## Style Prompts — Dual Form

Suno v5.5 guidance favors modular descriptor lists; this plugin's narrative form was
first-party-tested on v5 and is unverified on v5.5. Until a live A/B settles it,
**output BOTH forms** for every song (the `style-prompt form` preference can pin one):

**Modular — label it "try first":** 4-7 weighted descriptors in this order —
genre+subgenre · mood/energy · vocal direction · key instruments ·
production/tempo. One clear genre anchor; no near-synonym stacking.

```
gothic symphonic metal, doujin style, dramatic and tragic, dual female vocals
in dialogue with soaring harmonies, harpsichord pipe organ strings and
double-kick drums, polished cathedral-reverb production at 172 bpm
```

**Narrative — label it "fallback if the arrangement feels flat":** prose describing
how the song unfolds in time ("opens with… enters… builds through… resolves into").
Its v5-tested strength is temporal arrangement control. Weave the emotion arc into
the narrative; don't append it.

Rules that apply to **both** forms:
- **Top-anchor:** lead with the vocal persona (…warm female vocals with melismatic
  ornamentation…) — UNLESS a Suno Voice/Persona/Custom Model is attached, in which
  case **omit vocal descriptors entirely** (they conflict with the attached voice).
- **Single genre anchor** — one clear genre reference, not a pile of cousins.
- **Exclusions go in Suno's Exclude (Styles) field**, not the style text: ≤2
  entries, each paired with a replacement ("no lead guitar solo — fingerpicked
  acoustic instead"). See `references/suno-metatags.md`.

Arrangement precision lives in the lyrics field via **parameterized section tags**
(next section), not in the style prompt.

## Metatags in Lyrics

Suno reads embedded directions in the lyrics field. **Tag sparsely: 3-4 inflection
points per song.** Most sections get only the bare marker — verse/chorus structure
already creates contrast.

Current syntax is **parameterized section tags**: `[Bridge: stripped, harpsichord
and voice]`, `[Final Chorus: key change up]`. The adjacent-bracket form
(`[Bridge][stripped]`) is legacy-valid.

| Moment | Purpose | Example |
|--------|---------|---------|
| **Intro** | Set opening texture | `[Intro: music box and choir, then full band]` |
| **Breakdown/Bridge** | Contrast point | `[Bridge: stripped, half-time]` |
| **Build** | Pre-climax tension | `[Build]`, `[Build: snare roll]` |
| **Final Chorus** | Earned peak | `[Final Chorus: key change up]` |

Use **technique cues** (`stripped`, `half-time`, `key change up`) not **emotion
words** (`triumphant`, `intimate`). Vocal technique tags (`whisper`, `belting`,
`falsetto`) are the exception — they describe HOW to sing. A `[Break]` or blank
line before the climax buys tension through silence.

**Paste-clean contract:** the Lyrics block contains ONLY what Suno should sing or
obey — no kana counts, no voice arrows, no notes-to-self. Parentheticals in lyrics
are SUNG as ad-libs. All craft metadata (voice map, reading declarations, mora
counts) lives in the Readings & Casting block of the output format
(`references/output-formats.md`).

## Lyric Writing

**English:** target 6-10 syllables per line; line breaks = musical breaths.

**Japanese:** count **morae, not syllables** (月光 = げっこう = 4 morae). Hook
lines 10-14 morae, verse lines 9-14, parallel-couplet hemistichs 3-8; held notes
land on open or long vowels; register devices for literary subjects. Full rules:
`references/japanese-prosody.md` — consult it before writing any Japanese lyric.

**Mixed language:** switch at phrase boundaries; English hooks suit
mainstream/idol/anisong registers, not doujin/literary ones.

See `references/suno-metatags.md` for ad-libs, punctuation cues, and vowel
elongation.

## Composition Rubric (the floor — lyric-critic enforces this)

Checkability tiers: **[M]echanical / [S]tructural** violations are findings;
**[J]udgment** concerns are advisory only — taste is not agent-verifiable.

1. **[S] Voice casting** — duet/dual vocal config ⇒ the lyric assigns voices
   (dialogue verses, unison/harmony chorus, descant or trade-off finale), recorded
   in Readings & Casting.
2. **[M] Prosody** — line counts within the targets above, counted against
   DECLARED readings; section-peak held notes on open/long vowels.
3. **[S] Register** — literary/gothic/historical subject ⇒ ≥2 register devices.
   Japanese devices: `references/japanese-prosody.md`. English: archaic pronouns,
   latinate diction, syntactic inversion.
4. **[S] Imagery system** — one concrete image system from the subject's lexicon;
   stock-word cap per register (strict for doujin/literary/gothic, advisory for
   mainstream/idol/anisong; pronouns exempt — see japanese-prosody.md).
5. **[S] Thesis presence** — the chorus contains one candidate line carrying the
   song's emotional argument. **[J]** Whether it lands concretely is advisory.
6. **[M] Hook anchor** — title or hook phrase opens or closes the chorus.
7. **[M] Tags** — 3-4 parameterized inflection points, technique cues only.
8. **[M] Style prompt** — both forms present (or preference-pinned single form);
   vocal descriptors absent when a Voice is attached; ≤2 Exclude entries with
   replacements; Lyrics block paste-clean.

Quality bar in action: `references/examples/gothic-doujin-song.md` (every rubric
item annotated).

## Genre Conventions

> Springboards, not rules. Blend and break as the song demands.

| Genre | Key Elements | Common Tags |
|-------|--------------|-------------|
| J-pop | Catchy hooks, key changes, electronic+acoustic | j-pop, catchy melody, anime |
| Doujin | Electronic, 140-180 BPM, dramatic shifts | vocaloid style, fast tempo |
| Ballad | 60-90 BPM, piano/guitar lead, emotional | ballad, piano, heartfelt |
| Rock | Guitar-driven, powerful vocals | j-rock, electric guitar |
| EDM | Build-drop patterns, synth-led | edm, electronic, dance |
| K-pop | Polished, genre-blending | k-pop, polished, hook-driven |
| Latin | Distinctive rhythms, Spanish/Portuguese | latin, reggaeton, tropical |

For subgenre depth and the romanized phrase banks, see
`references/genre-deep-dive.md`. Song structure templates:
`references/song-structures.md`.

## Mood-to-Style Mapping

| Mood | Tempo | Tags |
|------|-------|------|
| Upbeat | 120-140 | energetic, bright, cheerful |
| Melancholic | 70-90 | sad, emotional, bittersweet |
| Energetic | 140-170 | driving, intense, anthemic |
| Dreamy | 80-100 | atmospheric, ethereal, floating |
| Intense | 130-160 | dramatic, dark, cinematic |
| Chill | 85-110 | relaxed, smooth, laid-back |

## Tempo Guidelines

| Style | BPM Range | Feel |
|-------|-----------|------|
| Slow ballad | 60-75 | Intimate, emotional |
| Mid-tempo ballad | 75-95 | Flowing, expressive |
| Pop standard | 100-120 | Comfortable, catchy |
| Dance pop | 120-135 | Energetic, groovy |
| Fast pop/rock | 135-160 | Driving, exciting |
| High energy | 160-180 | Intense, powerful |

Vocal tag vocabulary (female/male/special/tone/effects):
`references/suno-metatags.md`.

## Reference-Based Composition

When a user says "like YOASOBI" or "in the style of Aimer", capture the artist's
*essence* — creative spirit, emotional signature, sonic identity — not exact
specifications. Ask: what FEELING does this artist evoke? What makes them
recognizable?

For technical grounding, consult `references/artist-profiles.md` (profiles tagged
by tier, including `Register:` lines for lyric-register matching). The profile
gives ingredients; you decide the recipe. **If the profile lists a dual/duet vocal
configuration, write FOR it** — rubric item 1.

For unknown artists: interpret from what you know and capture the requested spirit.

## J-pop Tier Presets

Ecosystem-level presets instead of specific artists:

| Tier | Keywords | Sound |
|------|----------|-------|
| **Anisong** | `anisong`, `anime` | Anime OP/ED - dramatic, catchy, high energy |
| **Surface** | `surface`, `viral` | Producer scene - complex, narrative, layered |
| **Mainstream** | `mainstream`, `normie` | Radio-friendly - accessible, sing-along |
| **Doujin** | `doujin`, `touhou` | Convention - high production, niche genres |
| **Legacy** | `legacy`, `city pop` | Golden age - warm analog sound |

Combine with artists: `/suno anisong like Aimer` uses tier structure + artist
style. Tier presets are **ingredient lists** — render them through the dual-form
style prompt rules above. Full profiles and merge logic:
`references/jpop-tiers.md`.

## Professional Songwriter Techniques

**Hook-First:** design the chorus hook before the verses that build to it.
**Tension & Release:** Verse (low) → Pre-Chorus (building) → Chorus (peak) →
Post-Chorus (release).
**Three-Element Arrangement:** A (melody), B (counter-melody), C (rhythm).
Verse: A+C. Chorus: A+B+C. Bridge: B+C.

Details and exercises: `references/pro-techniques.md`.

## Output Formats

All output templates — including the **Readings & Casting craft block** and the
dual-form style prompt slots — live in `references/output-formats.md`.

## Additional Resources

- **`references/output-formats.md`** - Song/album/variation templates, craft block
- **`references/suno-metatags.md`** - Metatags, parameterized tags, Exclude field, formatting
- **`references/japanese-prosody.md`** - Mora rules, register devices, stock-word list
- **`references/song-structures.md`** - Standard pop, anime, ballad structures
- **`references/pro-techniques.md`** - Hook-first, tension/release, arrangement
- **`references/genre-deep-dive.md`** - Subgenre conventions and phrase banks
- **`references/artist-profiles.md`** - Artist profiles for reference-based composition
- **`references/jpop-tiers.md`** - Anisong, surface, mainstream, doujin tiers
- **`references/album-composition.md`** - Album arc patterns and track roles
- **`references/variation-patterns.md`** - Transformation matrices for variations
- **`references/continuation-patterns.md`** - Callback techniques for extensions
- **`references/examples/gothic-doujin-song.md`** - Annotated quality-bar exemplar
- **`references/troubleshooting.md`** - Common issues, causes, and fixes
