# Reference-Based Composition Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Enable users to compose songs by referencing artists (e.g., `/suno like YOASOBI`) instead of only using mood presets.

**Architecture:** Static markdown database of artist profiles in `references/artist-profiles.md`. Command parses arguments for reference patterns, looks up profile, and uses characteristics to inform style prompt generation.

**Tech Stack:** Markdown files only (Claude Code plugin)

---

## Task 1: Create Artist Profile Database Structure

**Files:**
- Create: `plugins/suno-composer/skills/song-composition/references/artist-profiles.md`

**Step 1: Create the file with header and format documentation**

Create `references/artist-profiles.md` with:

```markdown
# Artist & Song Reference Profiles

Reference database for artist-based composition. When user provides a reference like "make it sound like YOASOBI", look up the profile and use it to inform style prompt generation.

## How to Use This File

1. Search for artist name (case-insensitive) or alias
2. Extract profile fields for style prompt generation
3. Include artist name + descriptors in output (user can remove name if Suno rejects)

## Profile Format

Each artist entry contains:
- **Aliases:** Alternative names/spellings for matching
- **Genre:** Primary genres and subgenres
- **Tempo:** BPM range and feel
- **Vocal:** Type and style characteristics
- **Instruments:** Key instruments in arrangements
- **Production:** Mix and sound characteristics
- **Themes:** Common lyrical/conceptual themes
- **Mood:** Emotional range
- **Similar:** Related artists for discovery

---

```

**Step 2: Commit structure**

```bash
git add plugins/suno-composer/skills/song-composition/references/artist-profiles.md
git commit -m "feat(suno-composer): add artist profiles reference structure"
```

---

## Task 2: Add First 5 Artist Profiles (Tier 1A)

**Files:**
- Modify: `plugins/suno-composer/skills/song-composition/references/artist-profiles.md`

**Step 1: Add YOASOBI profile**

Append to file:

```markdown
## YOASOBI

- **Aliases:** yoasobi, ヨアソビ, Ayase, ikura
- **Genre:** j-pop, electronic, synth-pop, vocaloid-influenced
- **Tempo:** 130-150 BPM, driving energy
- **Vocal:** female, clear enunciation, fast melodic runs, emotional delivery, wide range
- **Instruments:** synthesizer, piano, electronic drums, bass, strings (occasional)
- **Production:** polished, compressed, layered synths, punchy mix, crisp highs
- **Themes:** narrative storytelling, novel adaptations, youth, night, fleeting moments, running
- **Mood:** energetic, melancholic undertones, hopeful, bittersweet
- **Similar:** Yorushika, Ado, Eve, Kenshi Yonezu

---

```

**Step 2: Add Yorushika profile**

Append:

```markdown
## Yorushika

- **Aliases:** yorushika, ヨルシカ, n-buna, suis
- **Genre:** j-rock, indie pop, acoustic-electronic blend, literary rock
- **Tempo:** 100-140 BPM, varied (ballads to uptempo)
- **Vocal:** female, delicate, breathy, emotional restraint, clear diction
- **Instruments:** acoustic guitar, electric guitar, piano, bass, drums, strings
- **Production:** organic feel, balanced mix, guitar-forward, atmospheric reverb
- **Themes:** literature references, seasons, nostalgia, loss, fleeting youth, rain
- **Mood:** melancholic, wistful, contemplative, quietly hopeful
- **Similar:** YOASOBI, Ado, Aimer, back number

---

```

**Step 3: Add Ado profile**

Append:

```markdown
## Ado

- **Aliases:** ado, アド
- **Genre:** j-pop, rock, electronic, chaotic pop, vocaloid-influenced
- **Tempo:** 120-180 BPM, high energy
- **Vocal:** female, powerful belting, aggressive delivery, screams, whispers, extreme range
- **Instruments:** heavy bass, distorted synths, electronic drums, guitar
- **Production:** loud, compressed, bass-heavy, chaotic layering, dynamic extremes
- **Themes:** rebellion, inner turmoil, self-expression, breaking free, darkness
- **Mood:** intense, aggressive, chaotic, vulnerable moments, explosive
- **Similar:** YOASOBI, Eve, Kenshi Yonezu, Reol

---

```

**Step 4: Add Eve profile**

Append:

```markdown
## Eve

- **Aliases:** eve, イブ
- **Genre:** j-rock, alternative, vocaloid-influenced, art rock
- **Tempo:** 120-160 BPM, driving
- **Vocal:** male, distinctive nasal tone, rapid-fire delivery, emotional, storytelling
- **Instruments:** electric guitar, bass, drums, synth accents, piano
- **Production:** guitar-driven, punchy drums, layered, energetic mix
- **Themes:** identity, relationships, anime tie-ins, emotional struggles, duality
- **Mood:** energetic, introspective, bittersweet, intense
- **Similar:** YOASOBI, Kenshi Yonezu, Yorushika, Zutomayo

---

```

**Step 5: Add Kenshi Yonezu profile**

Append:

```markdown
## Kenshi Yonezu

- **Aliases:** kenshi yonezu, 米津玄師, yonezu kenshi, hachi
- **Genre:** j-pop, alternative, electronic, art pop
- **Tempo:** 90-140 BPM, varied
- **Vocal:** male, smooth, distinctive vibrato, emotional depth, clear articulation
- **Instruments:** guitar, piano, synths, bass, drums, orchestral elements
- **Production:** polished, layered, cinematic, attention to detail, dynamic
- **Themes:** human connection, loneliness, growth, anime/film soundtracks, surreal imagery
- **Mood:** contemplative, hopeful, melancholic, uplifting, complex
- **Similar:** YOASOBI, Eve, King Gnu, Vaundy

---

```

**Step 6: Commit first batch**

```bash
git add plugins/suno-composer/skills/song-composition/references/artist-profiles.md
git commit -m "feat(suno-composer): add artist profiles - YOASOBI, Yorushika, Ado, Eve, Kenshi Yonezu"
```

---

## Task 3: Add Next 5 Artist Profiles (Tier 1B)

**Files:**
- Modify: `plugins/suno-composer/skills/song-composition/references/artist-profiles.md`

**Step 1: Add LiSA profile**

Append:

```markdown
## LiSA

- **Aliases:** lisa, リサ, risa oribe
- **Genre:** j-rock, anisong, pop-rock, power pop
- **Tempo:** 140-180 BPM, high energy
- **Vocal:** female, powerful belting, rock edge, emotional intensity, wide range
- **Instruments:** electric guitar, bass, drums, synth accents
- **Production:** rock-forward, punchy, energetic, arena-ready, crisp
- **Themes:** fighting spirit, never giving up, anime themes, passion, strength
- **Mood:** energetic, inspiring, passionate, intense, triumphant
- **Similar:** Aimer, YOASOBI, Ado, ReoNa

---

```

**Step 2: Add Aimer profile**

Append:

```markdown
## Aimer

- **Aliases:** aimer, エメ
- **Genre:** j-pop, ballad, rock, electronic, cinematic
- **Tempo:** 70-130 BPM, varied (ballads to mid-tempo)
- **Vocal:** female, husky, breathy, emotional depth, distinctive rasp, intimate
- **Instruments:** piano, guitar, strings, synths, full orchestra (ballads)
- **Production:** atmospheric, cinematic, reverb-heavy, dynamic, lush arrangements
- **Themes:** love, loss, longing, anime soundtracks, night, stars, distance
- **Mood:** melancholic, romantic, bittersweet, powerful, ethereal
- **Similar:** Yorushika, LiSA, back number, Uru

---

```

**Step 3: Add Official HIGE DANdism profile**

Append:

```markdown
## Official HIGE DANdism

- **Aliases:** official hige dandism, ヒゲダン, higedan, ohd
- **Genre:** j-pop, pop-rock, piano pop, sophisticated pop
- **Tempo:** 80-140 BPM, varied
- **Vocal:** male, smooth, high register, clear falsetto, emotional control
- **Instruments:** piano, guitar, bass, drums, strings, brass
- **Production:** polished, rich arrangements, layered harmonies, radio-ready
- **Themes:** love, relationships, everyday emotions, growth, sincerity
- **Mood:** uplifting, romantic, heartfelt, joyful, bittersweet
- **Similar:** King Gnu, back number, Mrs. GREEN APPLE, Vaundy

---

```

**Step 4: Add King Gnu profile**

Append:

```markdown
## King Gnu

- **Aliases:** king gnu, キングヌー
- **Genre:** j-rock, alternative, art rock, progressive pop
- **Tempo:** 90-150 BPM, varied and complex
- **Vocal:** male (dual vocalists), contrast between smooth and raw, harmonies
- **Instruments:** guitar, bass, drums, piano, synths, experimental elements
- **Production:** artistic, layered, dynamic shifts, genre-blending, intricate
- **Themes:** duality, society, human nature, artistic expression, philosophy
- **Mood:** complex, intense, contemplative, unpredictable, powerful
- **Similar:** Official HIGE DANdism, Kenshi Yonezu, Vaundy, RADWIMPS

---

```

**Step 5: Add Vaundy profile**

Append:

```markdown
## Vaundy

- **Aliases:** vaundy, バウンディ
- **Genre:** j-pop, r&b, rock, genre-fluid
- **Tempo:** 90-140 BPM, groove-oriented
- **Vocal:** male, soulful, smooth, rhythmic delivery, emotional range
- **Instruments:** guitar, bass, drums, synths, keys
- **Production:** modern, r&b influenced, tight groove, polished, warm
- **Themes:** youth, relationships, self-discovery, everyday feelings, city life
- **Mood:** cool, introspective, groovy, emotional, laid-back energy
- **Similar:** Kenshi Yonezu, King Gnu, Fujii Kaze, imase

---

```

**Step 6: Commit second batch**

```bash
git add plugins/suno-composer/skills/song-composition/references/artist-profiles.md
git commit -m "feat(suno-composer): add artist profiles - LiSA, Aimer, HIGE DANdism, King Gnu, Vaundy"
```

---

## Task 4: Add Remaining 10 Artist Profiles (Tier 2)

**Files:**
- Modify: `plugins/suno-composer/skills/song-composition/references/artist-profiles.md`

**Step 1: Add RADWIMPS, Mrs. GREEN APPLE, Aimyon, back number, BUMP OF CHICKEN**

Append all 5:

```markdown
## RADWIMPS

- **Aliases:** radwimps, ラッドウィンプス
- **Genre:** j-rock, alternative, soundtrack, emotional rock
- **Tempo:** 80-150 BPM, varied
- **Vocal:** male, emotional, raw, distinctive phrasing, english mixing
- **Instruments:** guitar, bass, drums, piano, strings, orchestral
- **Production:** cinematic, dynamic, film-quality, atmospheric, layered
- **Themes:** love, cosmos, "Your Name" soundtrack, weather, human connection
- **Mood:** emotional, epic, intimate, hopeful, bittersweet
- **Similar:** King Gnu, back number, Kenshi Yonezu, Bump of Chicken

---

## Mrs. GREEN APPLE

- **Aliases:** mrs green apple, ミセスグリーンアップル, mga
- **Genre:** j-pop, pop-rock, synth-pop, upbeat pop
- **Tempo:** 120-160 BPM, energetic
- **Vocal:** male, bright, high register, youthful energy, clear
- **Instruments:** synths, guitar, bass, drums, keys
- **Production:** bright, polished, synth-forward, radio-friendly, punchy
- **Themes:** youth, positivity, moving forward, everyday struggles, hope
- **Mood:** upbeat, cheerful, inspiring, energetic, youthful
- **Similar:** Official HIGE DANdism, Vaundy, YOASOBI, Aimyon

---

## Aimyon

- **Aliases:** aimyon, あいみょん
- **Genre:** j-pop, folk-pop, acoustic, singer-songwriter
- **Tempo:** 90-130 BPM, mid-tempo
- **Vocal:** female, natural, conversational, warm, relatable
- **Instruments:** acoustic guitar, piano, bass, drums, strings
- **Production:** organic, warm, singer-songwriter feel, intimate, clean
- **Themes:** everyday life, relationships, nostalgia, simple moments, youth
- **Mood:** warm, nostalgic, relatable, gentle, bittersweet
- **Similar:** back number, Yorushika, Vaundy, Fujii Kaze

---

## back number

- **Aliases:** back number, バックナンバー
- **Genre:** j-rock, ballad rock, emotional rock, pop-rock
- **Tempo:** 70-120 BPM, often slower
- **Vocal:** male, emotional, raw vulnerability, heartfelt delivery
- **Instruments:** guitar, bass, drums, piano, strings
- **Production:** guitar-driven, emotional dynamics, clear vocals forward, warm
- **Themes:** unrequited love, heartbreak, relationships, everyday sadness
- **Mood:** melancholic, vulnerable, romantic, bittersweet, heartfelt
- **Similar:** Official HIGE DANdism, Aimyon, RADWIMPS, Aimer

---

## BUMP OF CHICKEN

- **Aliases:** bump of chicken, バンプオブチキン, bump
- **Genre:** j-rock, alternative rock, emotional rock
- **Tempo:** 100-150 BPM, varied
- **Vocal:** male, gentle, storytelling quality, emotional restraint
- **Instruments:** guitar, bass, drums, synth accents
- **Production:** guitar-forward, atmospheric, layered, stadium-ready, warm
- **Themes:** friendship, journey, games/anime tie-ins, perseverance, stars
- **Mood:** hopeful, nostalgic, inspiring, gentle intensity, warm
- **Similar:** RADWIMPS, back number, Mr.Children, Spitz

---

```

**Step 2: Add Fujii Kaze, imase, TUYU, Zutomayo, Creepy Nuts**

Append all 5:

```markdown
## Fujii Kaze

- **Aliases:** fujii kaze, 藤井風, kaze fujii
- **Genre:** j-pop, r&b, soul, funk, piano pop
- **Tempo:** 80-120 BPM, groove-based
- **Vocal:** male, soulful, smooth, Okayama dialect, emotional, falsetto
- **Instruments:** piano, keys, bass, drums, brass, strings
- **Production:** retro-modern, warm, soul-influenced, organic, rich
- **Themes:** home, dialect, self-acceptance, spirituality, simple life
- **Mood:** soulful, warm, groovy, contemplative, uplifting
- **Similar:** Vaundy, Kenshi Yonezu, imase, tofubeats

---

## imase

- **Aliases:** imase, いませ
- **Genre:** j-pop, city pop revival, r&b, groovy pop
- **Tempo:** 100-130 BPM, mid-tempo groove
- **Vocal:** male, smooth, laid-back, youthful, catchy hooks
- **Instruments:** synths, bass, guitar, drums, retro keys
- **Production:** city pop influenced, groovy, polished, nostalgic-modern blend
- **Themes:** night drives, city life, romance, carefree youth
- **Mood:** groovy, nostalgic, romantic, carefree, cool
- **Similar:** Vaundy, Fujii Kaze, Tani Yuuki, 80s city pop

---

## TUYU

- **Aliases:** tuyu, ツユ, つゆ
- **Genre:** j-rock, emotional rock, vocaloid-influenced, emo
- **Tempo:** 140-180 BPM, fast and intense
- **Vocal:** female, raw emotion, crying quality, intense delivery, vulnerable
- **Instruments:** guitar, bass, drums, piano, synth
- **Production:** emotional, dynamic, rock-forward, raw, intense
- **Themes:** mental health, anxiety, self-doubt, inner struggles, rain
- **Mood:** intense, vulnerable, cathartic, dark, emotional release
- **Similar:** Yorushika, Ado, Eve, Zutomayo

---

## Zutomayo

- **Aliases:** zutomayo, ずっと真夜中でいいのに。, ztmy, zutomayonightforever
- **Genre:** j-rock, art rock, experimental pop, vocaloid-influenced
- **Tempo:** 130-170 BPM, energetic and complex
- **Vocal:** female (ACAね), unique tone, fast delivery, playful, emotional
- **Instruments:** guitar, bass, drums, synths, experimental sounds
- **Production:** intricate, layered, genre-blending, detailed, artistic
- **Themes:** night, emotions, surreal imagery, relationships, artistic expression
- **Mood:** energetic, playful, complex, melancholic undertones, artistic
- **Similar:** YOASOBI, Eve, Yorushika, Ado

---

## Creepy Nuts

- **Aliases:** creepy nuts, クリーピーナッツ, r-指定, dj松永
- **Genre:** j-hip-hop, rap, hip-hop, comedic rap
- **Tempo:** 90-140 BPM, hip-hop grooves
- **Vocal:** male rap, fast flow, wordplay, storytelling, comedic timing
- **Instruments:** turntables, samples, bass, drums, funk elements
- **Production:** hip-hop beats, sample-based, punchy, groove-heavy, clean
- **Themes:** otaku culture, everyday life, humor, self-deprecation, battle rap
- **Mood:** fun, clever, energetic, comedic, confident
- **Similar:** RIP SLYME, RHYMESTER, Kreva, Scha Dara Parr

---

```

**Step 3: Commit final batch**

```bash
git add plugins/suno-composer/skills/song-composition/references/artist-profiles.md
git commit -m "feat(suno-composer): add artist profiles - remaining 10 artists (Tier 2)"
```

---

## Task 5: Update Command with Reference Parsing

**Files:**
- Modify: `plugins/suno-composer/commands/suno.md`

**Step 1: Update argument-hint in frontmatter**

Change line 3 from:
```yaml
argument-hint: [theme/mode:album|variation|extend]
```
To:
```yaml
argument-hint: [theme/like <artist>/mode:album|variation|extend]
```

**Step 2: Add Reference Detection section after Mode Detection**

Insert after line 17 (after "Otherwise → Standard Mode"):

```markdown

## Reference Detection

Before gathering parameters, check if $ARGUMENTS contains an artist reference:

**Reference patterns to detect:**
- `like [artist]` → extract artist name
- `in the style of [artist]` → extract artist name
- `similar to [artist]` → extract artist name
- `[artist]-style` → extract artist name

**If reference detected:**
1. Read `skills/song-composition/references/artist-profiles.md`
2. Search for artist name (case-insensitive) or alias match
3. If found: Store profile data for style prompt generation
4. If not found: Ask user to describe the style or use presets

**Example parsing:**
- `/suno like YOASOBI about hope` → artist: "YOASOBI", theme: "about hope"
- `/suno in the style of Aimer` → artist: "Aimer", theme: none
- `/suno Eve-style energetic` → artist: "Eve", theme: "energetic"

```

**Step 3: Update Step 2 (Gather Session Parameters)**

Replace the "If no theme provided" section (lines 47-56) with:

```markdown
**If artist reference was detected:**
Show the matched profile summary:
```
Found artist profile: [Artist Name]
- Genre: [genres]
- Tempo: [tempo range]
- Vocal: [vocal type and style]
- Mood: [mood range]

Using this as the base style. You can specify a theme to add (e.g., "about finding hope").
```
Then ask for optional theme/mood modifier.

**If artist reference was NOT found (but attempted):**
```
I don't have a profile for "[artist name]" yet.

Options:
1. Describe their style briefly (I'll use that)
2. Use mood presets instead
```

**If no reference in arguments and $ARGUMENTS is empty:**

Ask about reference or mood:
```
Do you have a reference artist in mind?
- Yes, let me specify
- No, use mood presets
```

If "Yes": Ask for artist name, then lookup profile.
If "No": Show mood presets (existing behavior):
- Upbeat - Bright, energetic, feel-good vibes
- Melancholic - Sad, bittersweet, emotional depth
- Energetic - High-energy, powerful, driving
- Dreamy - Atmospheric, ethereal, floating
- Intense - Dramatic, powerful, cinematic
- Chill - Relaxed, smooth, laid-back
- (Allow custom description)

**If theme WAS provided in arguments (no reference):**
Use the provided theme: $ARGUMENTS
```

**Step 4: Update Step 6 style prompt generation**

In Step 6 (Generate Full Songs to Files), after "3. **Craft Style Prompt**", add:

```markdown
   **If artist reference was matched:**
   - Lead with "[Artist]-inspired" or "[Artist] style" (user can remove if Suno rejects)
   - Include all profile descriptors: genre, tempo feel, vocal style, instruments, production
   - User's theme shapes the emotion arc
   - Example: "YOASOBI-inspired j-pop electronic synth-pop, 140 bpm driving tempo, female vocals with clear enunciation and fast melodic runs, synthesizer and piano-driven, polished compressed mix, emotion arc: [from user theme]"

```

**Step 5: Commit command update**

```bash
git add plugins/suno-composer/commands/suno.md
git commit -m "feat(suno-composer): add artist reference parsing to /suno command"
```

---

## Task 6: Update SKILL.md with Reference Documentation

**Files:**
- Modify: `plugins/suno-composer/skills/song-composition/SKILL.md`

**Step 1: Add Reference-Based Composition section**

After the "Mood-to-Style Mapping" section (around line 340), add:

```markdown
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

```

**Step 2: Update Additional Resources section**

Add to the reference files list:

```markdown
- **`references/artist-profiles.md`** - Artist characteristics for reference-based composition
```

**Step 3: Commit skill update**

```bash
git add plugins/suno-composer/skills/song-composition/SKILL.md
git commit -m "docs(suno-composer): add reference-based composition to SKILL.md"
```

---

## Task 7: Update SPEC.md with v4.4 Feature

**Files:**
- Modify: `plugins/suno-composer/SPEC.md`

**Step 1: Add Phase 10 to Development Phases**

After Phase 9 (v4.3), add:

```markdown
### Phase 10: Reference-Based Composition (v4.4) ✓
- [x] Create artist profile database (29 artists across 5 tiers)
- [x] Add reference parsing to /suno command
- [x] Integrate profile data into style prompt generation
- [x] Document feature in SKILL.md
```

**Step 2: Update workflow diagram description**

Change:
```
### Workflow (v4.3 - Sparse Tags + Preview-First)
```
To:
```
### Workflow (v4.4 - Reference-Based + Sparse Tags)
```

**Step 3: Commit spec update**

```bash
git add plugins/suno-composer/SPEC.md
git commit -m "docs(suno-composer): add v4.4 reference-based composition to SPEC"
```

---

## Task 8: Final Review and Push

**Step 1: Review all changes**

```bash
git log --oneline -10
git diff main..HEAD --stat
```

**Step 2: Push feature branch**

```bash
git push -u origin feature/suno-reference-composition
```

**Step 3: Report completion**

List all files created/modified and summary of feature.

---

## Success Criteria Checklist

- [x] `references/artist-profiles.md` exists with 29 artist profiles
- [x] Each profile has: aliases, genre, tempo, vocal, instruments, production, themes, mood, similar
- [x] `commands/suno.md` parses "like [artist]" patterns
- [x] Unknown artists show fallback options
- [x] Style prompts include artist name + descriptors
- [x] `SKILL.md` documents the feature
- [x] `SPEC.md` updated to v4.5
- [x] All commits are clean and atomic
