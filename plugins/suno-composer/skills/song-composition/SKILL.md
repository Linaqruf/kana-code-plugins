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

The skill provides Suno syntax and creative fuel. You provide the artistry.

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
1. **Vocal persona first** (top-anchor strategy - see below)
2. Primary genre and subgenre/era influence
3. Tempo feel (e.g., "slow around 75 bpm", "driving 140 bpm energy")
4. Key instruments
5. Production style tags
6. Mood and energy descriptors
7. **Emotion arc** (Suno V5 reads this well)

### Top-Anchor Strategy

Start your style prompt with 1-2 clear vocal instructions before other elements. This anchors the vocal character before genre/production details:

```
Female pop vocalist, breathy, intimate, 90s R&B groove, mid-tempo around 95 bpm, ...
```

```
Male rock vocalist, powerful raspy delivery, driving energy, ...
```

The vocal description at the start has the strongest influence on the generated voice.

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

> **These are creative springboards, not rules.**
> Every convention below can be bent, blended, or broken when the song demands it.
> Some of the most interesting songs come from unexpected combinations:
> ballad emotion + EDM drops, anisong energy + lo-fi texture, rock power + electronic atmospherics.

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

### Line Length Guidelines

For optimal vocal alignment in Suno v5:
- **Target 6-10 syllables** per line for mid-tempo songs
- Line breaks indicate where musical breaths occur
- Long run-on lines cause word compression or misplaced stress
- Single short sentence = one vocal phrase

See `references/suno-metatags.md` for advanced formatting (ad-libs, punctuation cues, vowel elongation).

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

### Artistic Interpretation (Preferred)

When a user says "like YOASOBI" or "in the style of Aimer", capture the *essence* of the artist—their creative spirit, emotional signature, and sonic identity—rather than exact specifications.

Ask yourself:
- What FEELING does this artist evoke?
- What makes their music recognizable?
- How would they approach THIS theme?

**Example:**
```
User: "like YOASOBI about finding hope"

Your interpretation:
YOASOBI feels like... breathless storytelling, literary depth, urgent piano,
a narrator racing through emotions, clarity in chaos.

→ Craft: "narrative-driven j-pop, urgent piano pulse, clear female vocals
   telling a story, synth layers building momentum, 140 bpm energy,
   emotion arc: desperate searching → glimpse of light → running toward hope"
```

### Profile Reference (Fallback)

If you want specific technical grounding, consult `references/artist-profiles.md` for the **29 artist profiles** across 5 tiers. Use it as a starting point, then add your creative interpretation.

**Key insight:** The profile gives you ingredients. You decide the recipe.

### Unknown Artists

If an artist isn't in the profiles, embrace it:
- Interpret based on what you know about them
- Create something that captures the requested spirit
- Don't say "I don't have a profile"—say "Here's my interpretation..."

## J-pop Tier Presets

### Using Tier Keywords

Instead of specifying individual artists, users can invoke ecosystem-level presets:

```
/suno anisong about never giving up
/suno viral jpop about city nights
/suno mainstream romantic ballad
/suno doujin symphonic fantasy battle
```

### Available Tiers

| Tier | Keywords | Sound |
|------|----------|-------|
| **Anisong** | `anisong`, `anime`, `anime opening` | Anime OP/ED style - dramatic builds, catchy hooks, high energy |
| **Surface** | `surface`, `viral`, `viral jpop` | Viral/producer scene - complex rhythms, narrative, layered synths |
| **Mainstream** | `mainstream`, `normie`, `radio jpop` | Radio-friendly - band sound, accessible, sing-along |
| **Doujin** | `doujin`, `touhou`, `underground` | Convention scene - high production, niche genres |
| **Legacy** | `legacy`, `classic`, `city pop` | Golden age J-pop - foundational artists, warm analog sound |

**Note:** `viral` alone triggers the Surface tier (internet-born J-pop artists). For non-J-pop viral content, specify genre explicitly (e.g., `viral pop` or `viral edm`).

### Doujin Subgenres

Doujin tier has specific subgenres (require "doujin" prefix):
- `doujin symphonic` - Gothic/orchestral (Ariabl'eyeS, Sound Horizon)
- `doujin denpa` - Fast/chaotic/cute (IOSYS, MOSAIC.WAV)
- `doujin eurobeat` - Driving/synth-heavy (Initial D style)

### Tier + Artist Combination

Combine tier with artist reference for blended results:

```
/suno anisong like Aimer about farewell
```

This uses:
- Anisong's dramatic structure and hook timing
- Aimer's husky vocals and cinematic production
- Artist's tempo overrides tier's default

### How Tier Lookup Works

1. Command detects tier keyword in arguments
2. Looks up tier in `references/jpop-tiers.md`
3. If artist also specified, merges profiles
4. Generates style prompt from combined data

See `references/jpop-tiers.md` for full tier profiles and merge logic.

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

## Creative Confidence

### When to Follow the References

- **Suno syntax:** Always follow (structure tags, formatting)—Claude can't know these
- **Output format:** Always follow—must be copy-paste ready for Suno
- **Sparse tagging principle:** Generally follow—over-tagging hurts quality

### When to Trust Your Instincts

- **Tag selection:** Choose what FEELS right for the emotion
- **Genre blending:** Mix freely if it serves the song
- **Artist interpretation:** Capture essence over exact specs
- **Lyric content:** This is pure creative territory
- **Emotional arc:** You design the journey
- **Tempo/energy:** References are guidelines, not mandates

### Signs of Being Too Rigid

Copying tag lists verbatim, being afraid to deviate from conventions, or looking up every artist instead of interpreting are signs to pause and reconnect with creative instinct. The references are fuel, not fences.

## Working with Commands

### Dual-Mode Command Support

The `/suno` command supports two interaction modes:

**Vision-First Mode** (rich input):
- Claude interprets creative direction immediately
- Presents vivid creative vision for user reaction
- Iterates through natural conversation
- User role: React and refine ("darker", "fewer tracks")

**Guided Mode** (`:guided` or sparse input):
- Step-by-step wizard with streamlined questions
- Claude as helpful guide through options
- User role: Select from presented choices

**Your role differs by mode:**

| Aspect | Vision-First | Guided |
|--------|--------------|--------|
| First output | Creative vision | Questions |
| User input | Natural language tweaks | Option selection |
| Iteration | "make it darker" | "modify song 2" |
| Questions | Only genuine ambiguity | Structured choices |

**Regardless of mode:**
- Use sparse tagging (3-4 inflection points)
- Follow Suno v5 output format
- Apply creative interpretation over rigid lookup
- Trust your artistic instincts

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
- **`references/suno-metatags.md`** - Complete Suno v5 metatags, structure tags, vocal styles, production tags, negative prompting, lyric formatting techniques
- **`references/genre-deep-dive.md`** - Extended genre conventions and subgenres
- **`references/japanese-lyric-patterns.md`** - Japanese lyric writing patterns and vocabulary
- **`references/album-composition.md`** - Album coherence, arc patterns, track roles
- **`references/variation-patterns.md`** - Transformation matrices for song variations
- **`references/continuation-patterns.md`** - Callback techniques, narrative bridges for song continuations
- **`references/artist-profiles.md`** - Artist characteristics for reference-based composition
- **`references/jpop-tiers.md`** - J-pop ecosystem tiers (anisong, surface, mainstream, doujin) with auto-tags and style presets

### Working with User Preferences

User preferences are loaded from `.claude/suno-composer.local.md` (project) and `~/.claude/suno-composer.local.md` (global). When both exist, project preferences override matching global sections.

**How to apply loaded preferences:**

| Preference Type | How to Apply |
|-----------------|--------------|
| **Favorite Genres** | Use as style prompt defaults unless session contradicts |
| **Preferred Vocal Styles** | Apply to all songs unless user explicitly overrides |
| **Default Languages** | Use unless theme strongly implies otherwise |
| **Favorite Artists/Influences** | Consider as baseline influences, blend with session requests |
| **Mood Tendencies** | Shape emotional arc and dynamics |
| **Stylistic Notes** | Apply specific guidance (e.g., "prefers vision-first mode") |

**Preference integration principles:**
- Preferences are suggestions, not constraints
- Override when creative direction calls for it
- Session-specific requests take precedence
- Blend preferences with context naturally
- Don't announce "I'm using your preferences" - just use them

**Example integration:**
```
User preferences: "Female vocals, J-pop, emotional depth"
Session request: "/suno epic battle anthem"

Result: J-pop epic battle anthem with female vocals,
but with emotional complexity woven into the battle narrative
(not just generic upbeat energy)
```

**When preferences conflict with session:**
- Session request wins for explicit choices
- Preferences fill gaps where session is silent
- Use judgment for ambiguous cases

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
