# Suno v5 Metatags Reference

Complete reference for Suno AI v5 metatags, structure tags, vocal styles, and production techniques.

## Structure Tags

Use these section labels in the lyrics field to control arrangement:

| Tag | Purpose | Example |
|-----|---------|---------|
| `[Intro]` | Opening section | `[Intro: Acoustic guitar]` |
| `[Verse]` | Narrative section | `[Verse 1]`, `[Verse 2]` |
| `[Pre-Chorus]` | Build tension | `[Pre-Chorus]` |
| `[Chorus]` | Main hook | `[Chorus]` |
| `[Bridge]` | Contrast/pivot | `[Bridge]` |
| `[Hook]` | Memorable phrase | `[Hook]` |
| `[Break]` | Pause/change | `[Break]` |
| `[Instrumental]` | No vocals | `[Instrumental Break]` |
| `[Outro]` | Closing | `[Outro: Fade out]` |
| `[Build]` | Rising intensity | `[Build]` |
| `[Drop]` | EDM climax | `[Drop]` |
| `[Interlude]` | Musical passage | `[Interlude]` |
| `[Refrain]` | Repeated phrase | `[Refrain]` |

### Structure Best Practices

- Place most important tags at section beginnings
- Use numbered verses: `[Verse 1]`, `[Verse 2]`
- Combine with instruments: `[Intro: Piano]`, `[Outro: Fade out]`
- Clear order: `[Intro] → [Verse 1] → [Pre-Chorus] → [Chorus] → [Verse 2] → [Chorus] → [Bridge] → [Chorus x2]`

### Note on [Intro] Reliability

The `[Intro]` tag can be inconsistent in Suno v5. Alternatives if it's not working:
- Describe in style prompt: "short instrumental intro with piano"
- Use `[Instrumental Intro]` for clearer intent
- Start directly with `[Verse 1]` and let arrangement handle intro naturally

## Vocal Style Tags

### Female Vocals

| Style | Tags | Use Case |
|-------|------|----------|
| Soft/Gentle | `soft female vocals`, `breathy`, `intimate`, `gentle voice` | Ballads, intimate songs |
| Powerful | `female belting`, `powerful vocals`, `strong voice`, `emotional delivery` | Anthems, climactic moments |
| Cute/Idol | `cute vocals`, `bright voice`, `idol style`, `youthful` | J-pop, K-pop, upbeat songs |

### Male Vocals

| Style | Tags | Use Case |
|-------|------|----------|
| Soft/Gentle | `soft male vocals`, `tender`, `warm voice`, `gentle delivery` | Ballads, acoustic |
| Powerful | `male belting`, `rock vocals`, `powerful`, `passionate` | Rock, anthems |
| Low/Smooth | `deep voice`, `smooth baritone`, `rich vocals` | R&B, jazz |

### Special Vocal Styles

| Style | Tags | Use Case |
|-------|------|----------|
| Duet | `male and female duet`, `harmonies`, `call and response` | Romantic songs |
| Choir | `choir vocals`, `layered harmonies`, `group vocals` | Gospel, anthems |
| Synth/Vocaloid | `vocaloid style`, `synthesized vocals`, `electronic voice` | Doujin, electronic |
| Whisper | `whisper`, `intimate whisper`, `ASMR-like` | Intros, bridges |
| Raspy | `raspy vocals`, `gritty voice`, `raw` | Rock, blues |
| Melismatic | `melismatic`, `vocal runs`, `R&B style` | Soul, R&B |
| Monotone | `monotone`, `spoken word`, `talk-singing` | Indie, rap |

### Vocal Tone Tags

| Tag | Effect | Use Case |
|-----|--------|----------|
| `airy` | Light, floating quality | Dream pop, ethereal |
| `crisp` | Clear, articulated | Pop, precise delivery |
| `gritty` | Rough texture | Rock, blues, raw emotion |
| `smooth` | Even, polished | R&B, jazz |
| `deep` | Low register emphasis | Ballads, dramatic |

### Vocal Effects Tags

| Tag | Effect | Use Case |
|-----|--------|----------|
| `auto-tuned` | Pitch correction effect | Modern pop, hip-hop |
| `distorted` | Processed/clipped | Experimental, rock |
| `reverbed` | Spacious echo | Atmospheric, dreamy |

### Vocal Register Tags

| Tag | Effect | Use Case |
|-----|--------|----------|
| `low-pitched` | Bass register | Deep ballads, dramatic |
| `high-pitched` | Treble register | Bright pop, soaring |
| `mid-range` | Middle register | Versatile, natural |

## Production Tags

### Reverb & Space

| Tag | Effect |
|-----|--------|
| `dry vocal` | Minimal reverb, close/intimate |
| `reverb-heavy` | Spacious, atmospheric |
| `wide stereo` | Expansive mix |
| `intimate` | Close mic, small room |
| `cathedral reverb` | Large, epic space |

### Compression & Dynamics

| Tag | Effect |
|-----|--------|
| `compressed` | Punchy, loud, consistent |
| `dynamic` | Natural volume variation |
| `pumping` | Side-chain compression effect |
| `brick wall` | Maximum loudness |

### Production Style

| Tag | Effect |
|-----|--------|
| `lo-fi` | Vintage, warm, imperfect |
| `polished` | Clean, modern, professional |
| `raw` | Unprocessed, live feel |
| `overproduced` | Dense, layered |
| `minimalist` | Sparse, essential elements |

### Mix Elements

| Tag | Effect |
|-----|--------|
| `side-chained bass` | Pumping bass effect |
| `layered synths` | Multiple synth textures |
| `heavy bass` | Prominent low end |
| `crisp drums` | Sharp, defined percussion |
| `808 bass` | Hip-hop/trap bass style |

## Mood & Energy Tags

| Mood | Tags |
|------|------|
| Upbeat | `energetic`, `bright`, `cheerful`, `danceable`, `happy` |
| Melancholic | `sad`, `emotional`, `yearning`, `bittersweet`, `nostalgic` |
| Energetic | `driving`, `intense`, `powerful`, `anthemic`, `explosive` |
| Dreamy | `atmospheric`, `ethereal`, `soft`, `floating`, `hazy` |
| Intense | `dramatic`, `powerful`, `dark`, `cinematic`, `epic` |
| Chill | `relaxed`, `smooth`, `laid-back`, `groovy`, `mellow` |
| Aggressive | `angry`, `fierce`, `raw`, `heavy`, `brutal` |
| Romantic | `loving`, `tender`, `passionate`, `sensual`, `warm` |

## Genre-Specific Tag Combinations

### J-pop Ballad
```
j-pop, emotional ballad, female vocals, soft voice, piano, strings, melancholic, anime soundtrack
```

### Energetic Doujin
```
j-pop, electronic, vocaloid style, fast tempo, synthesizer, driving beat, energetic, anime opening
```

### City Pop
```
city pop, 80s, funky bass, saxophone, groovy, nostalgic, japanese, smooth vocals
```

### EDM Drop
```
edm, progressive house, build, drop, synth lead, side-chained bass, euphoric, festival
```

### Lo-fi Hip-hop
```
lo-fi hip hop, chill, jazzy samples, vinyl crackle, relaxed, study music, mellow
```

### Rock Anthem
```
rock, powerful vocals, electric guitar, driving drums, anthem, stadium, epic chorus
```

## Advanced Techniques

### The Sparse Tagging Principle

**Tag only 3-4 inflection points** in a song. Most sections need just the section marker. The verse/chorus structure already creates contrast.

```
✅ GOOD - sparse technique cues:
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
[Verse 2][tender]
[Bridge][vulnerable, stripped]
[Final Chorus][soaring, triumphant]
```

### Technique Cues (Recommended)

Use technique/arrangement cues that CREATE dynamics:
```
[Breakdown][stripped, half-time]
[Build][snare roll, filtered]
[Final Chorus][key change up]
[Bridge][a cappella]
[Drop]
```

### Vocal Technique (Use Sparingly)

Vocal technique tags are useful at specific contrast moments:
```
[Bridge][whisper]      ← contrast point only
[Breakdown][belting]   ← specific effect needed
```

NOT on every section - the style prompt handles general vocal character.

### Emotion Arc in Style Prompt

Put the emotional journey in the style prompt, not in section tags:
```
Style: emotional j-pop ballad, 75 bpm, soft female vocals,
emotion arc: intimate verse → building anticipation → euphoric chorus → stripped reflection → triumphant finale
```

This is where Suno V5 reads emotion arc effectively.

## Dynamic Control

### The Problem: Over-Tagging

When every section has tags, you're describing dynamics instead of creating them:
```
❌ Describing dynamics (adds noise):
[Verse 1][soft, intimate]
[Pre-Chorus][building tension]
[Chorus][powerful, soaring]
```

### The Solution: Sparse Technique Tags

Let structure create dynamics. Tag only where you need a TECHNIQUE change:
```
✅ Creating dynamics (sparse cues):
[Verse 1]
[Pre-Chorus]
[Chorus]
[Breakdown][half-time, filtered]
[Build]
[Final Chorus][key change up]
```

### Technique Tags That Work

| Tag | What It Does | When to Use |
|-----|--------------|-------------|
| `[stripped]` | Removes instruments | Breakdown, bridge |
| `[half-time]` | Halves the tempo feel | Breakdown, contrast |
| `[double-time]` | Doubles the tempo feel | Energy boost |
| `[key change up]` | Modulates up | Final chorus climax |
| `[filtered]` | Low-pass filter effect | Build tension |
| `[drop]` | Full arrangement returns | After build (EDM) |
| `[breakdown]` | Stripped section | Before climax |
| `[build]` | Rising tension | Before drop/chorus |
| `[a cappella]` | Voice only | Dramatic contrast |
| `[whisper]` | Soft vocal technique | Specific effect |

### Tags to Avoid (Emotion Words)

These describe feelings but don't create dynamics:
- `[intimate]`, `[vulnerable]`, `[tender]`
- `[building]`, `[rising]`, `[soaring]`
- `[powerful]`, `[triumphant]`, `[explosive]`
- `[emotional]`, `[passionate]`, `[intense]`

The structure and technique tags handle energy. Emotion words just add noise.

## Style Prompt vs Lyrics Prompt

**Best Practice**: Separate style description from lyrics.

**Style Prompt** (goes in Style field):
```
dreamy bass house, dreamstep influence, 126 bpm feel, deep sub bass, crisp drums, wide synth pads, airy topline, modern clean mix, festival-ready drop, emotional but restrained
```

**Lyrics Prompt** (goes in Lyrics field):
```
[Verse 1]
Walking through the neon lights...

[Chorus]
We're dancing in the moonlight...
```

## Tag Count Guidelines

- **Minimum**: 6 tags for basic direction
- **Optimal**: 8-12 tags for balanced control
- **Maximum**: 15+ tags may cause conflicts

> **Artistic License:** These tags are options, not requirements. A great song
> might use 3 tags or 12. Choose what serves the music, not what fills a quota.

## Negative Prompting

Include exclusions in your style prompt to remove unwanted elements. Suno v5 handles exclusions more reliably than previous versions.

### Syntax Examples

```
instrumental only, no vocals, no choir, no spoken words
upbeat pop with drums and bass, no guitars
trap beat with piano and synths, no 808s
cinematic underscore, no vocals, no choir, wide reverb
```

### Precision Stacking

Be specific to avoid over-exclusion:

| Instead of | Use |
|------------|-----|
| "no guitar" | "no lead guitar solo" (keeps rhythm) |
| "no hi-hats" | "no harsh hi-hats" |
| "no bass" | "no 808 sub" (keeps other bass) |
| "no backing vocals" | "no choir, no oohs/ahhs" |

### Genre-Aware Exclusions

| Genre | Common Removal | Replace With |
|-------|----------------|--------------|
| EDM/Dance | harsh hats, screech leads | smooth plucks, clean supersaw |
| Rock | distortion (if muddy) | clean crunch, tight rhythm |
| Hip-hop | 808s (if swamping mix) | tight bass, short sub |
| Lo-fi | pads/wash (if muddy) | dry piano, simple chords |

### Best Practices

- **Limit to 1-2 exclusions** - over-exclusion hollows arrangements or causes weird substitutions
- **Pair negatives with replacements** - "no electric guitar, add fingerpicked acoustic"
- **Avoid conflicts** - don't say "instrumental only" and "strong vocals"
- **Use for problem-solving** - remove elements that are hurting the mix, not for micromanaging

## Lyric Formatting Techniques

Beyond section tags, Suno v5 interprets formatting cues in your lyrics.

### Ad-libs

Add short vocal additions in parentheses:

```
I can feel it (oh yeah)
Here we go (hey!)
One more time (woah)
Let's go (uh-huh)
```

Ad-libs appear as backing vocals or exclamations, not replacing the main lyric.

### Punctuation as Performance Cues

| Punctuation | Effect | Example |
|-------------|--------|---------|
| Comma `,` | Short pause | "Wait, I need you" |
| Dash `-` | Linked syllables | "To-night we fly" |
| Ellipsis `...` | Breath point, trailing off | "If only I knew..." |
| CAPS | Stress/emphasis | "I am ALIVE" |

### Vowel Elongation

Hyphenate syllables for sustained notes:

```
lo-ove (held note)
sooo-long (drawn out)
ye-eah (extended)
no-o-o (melismatic run)
```

Use sparingly - works best on chorus hooks or emotional peaks.

### Breath Markers

Insert explicit breath points:

```
Running through the fire (breath)
Nothing's gonna stop me now
```

Helps with pacing in fast sections or when lines run together.

### Prevent Lyric Changes

When exact lyrics matter, add this directive at the start of your lyrics:

```
(Do not change any words. Sing exactly as written.)

[Verse 1]
...
```

Useful for:
- Specific word choices that matter
- Lyrics with intentional unusual phrasing
- When Suno keeps altering your words

### Line Length Guidelines

- **Target 6-10 syllables** per line for mid-tempo songs
- Line breaks indicate where musical breaths occur
- Long run-on lines cause word compression or misplaced stress
- Single short sentence = one vocal phrase

```
✅ GOOD (clear phrasing):
Walking through the city lights
Every shadow tells a story
I can feel you next to me

❌ AVOID (too long):
Walking through the city lights at midnight while the shadows dance around me telling stories
```

## Production Tag Selection Guide

Quick reference for selecting production tags based on genre and mood:

| Genre/Mood | Recommended Production Tags |
|------------|----------------------------|
| Ballad | reverb-heavy, intimate, dynamic, piano-driven |
| J-pop Energetic | polished, compressed, crisp drums, layered synths |
| EDM/Dance | side-chained bass, wide stereo, compressed, 808 bass |
| Lo-fi/Chill | lo-fi, warm, vinyl texture, relaxed mix |
| Rock/Anthem | powerful, stadium reverb, driving drums, guitar-forward |
| Dreamy/Atmospheric | reverb-heavy, wide stereo, ethereal, floating pads |
| Intense/Cinematic | epic, orchestral, dynamic, building, dramatic |

### By Energy Level

| Energy | Production Tags |
|--------|-----------------|
| Low | intimate, dry vocal, minimal, stripped |
| Medium | balanced mix, natural reverb, full arrangement |
| High | compressed, punchy, layered, side-chained, crisp |

## Sources

- [How to Prompt Suno](https://howtopromptsuno.com/)
- [How to Prompt Suno - Voice Tags](https://howtopromptsuno.com/making-music/voice-tags)
- [Suno Metatag Creator Guide](https://sunometatagcreator.com/metatags-guide)
- [Jack Righteous - Suno Meta Tags Guide](https://jackrighteous.com/en-us/pages/suno-ai-meta-tags-guide)
- [Jack Righteous - Negative Prompting in Suno v5](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/negative-prompting-suno-v5-guide)
- [CometAPI - How to Instruct Suno v5 with Lyrics](https://www.cometapi.com/how-to-instruct-suno-v5-with-lyrics/)
- [Suno v5 Prompt Patterns](https://plainenglish.io/blog/i-made-10-suno-v5-prompt-patterns-that-never-miss)
