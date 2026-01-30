# J-pop Tier Presets Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a tier-based preset system for Japanese music that auto-applies metatags based on ecosystem layer (anisong, surface, mainstream, doujin).

**Architecture:** Natural language keyword detection in command arguments triggers tier lookup. Tier profiles provide base metatags and style elements. Tiers merge with artist profiles when both are specified (tier base + artist refinements).

**Tech Stack:** Markdown reference files, command workflow modifications.

---

## Task 1: Create Tier Reference File

**Files:**
- Create: `skills/song-composition/references/jpop-tiers.md`

**Step 1: Create the tier reference file**

Create `skills/song-composition/references/jpop-tiers.md` with the following content:

```markdown
# Japanese Music Tier System

Reference database for J-pop ecosystem tiers. When user mentions a tier keyword, look up the profile and use it to inform style prompt generation.

## How to Use This File

1. Scan user input for tier keywords (case-insensitive)
2. If keyword found, load tier profile
3. Apply auto-tags and style preset to generation
4. If artist reference also present, merge (tier base + artist refinements)

## Keyword Matching

| Tier | Keywords |
|------|----------|
| Anisong | `anisong`, `anime`, `anime opening`, `anime op`, `anime ed` |
| Surface | `surface`, `viral`, `viral jpop`, `producer scene`, `utaite` |
| Mainstream | `mainstream`, `normie`, `normie jpop`, `radio jpop` |
| Doujin | `doujin`, `touhou`, `underground`, `convention`, `comiket` |
| Doujin Symphonic | `doujin symphonic` |
| Doujin Denpa | `doujin denpa` |
| Doujin Eurobeat | `doujin eurobeat` |

---

## Tier: Anisong

**Aliases:** anisong, anime, anime opening, anime op, anime ed

**Auto-tags:**
- [Anime OP]
- [J-rock]
- [Dramatic Build]
- [Catchy Hook]
- [High Energy]
- [Powerful Vocals]

**Quick Reference:**
- **Tempo:** 140-180 BPM
- **Vocal:** Powerful, clear, wide range, emotional belting
- **Mood:** Inspiring, intense, triumphant, passionate

**Style Preset:**
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

**Representative Artists:** LiSA, Aimer, FLOW, TK from Ling Tosite Sigure, ReoNa, SID, MAN WITH A MISSION, SPYAIR

---

## Tier: Surface

**Aliases:** surface, viral, viral jpop, producer scene, utaite

**Auto-tags:**
- [J-pop]
- [Vocaloid-influenced]
- [Complex Rhythm]
- [Narrative Lyrics]
- [Viral Hook]
- [Fast Melodic Runs]
- [Layered Synths]

**Quick Reference:**
- **Tempo:** 120-180 BPM (varied, often complex)
- **Vocal:** Fast runs, clear enunciation, emotional, distinctive
- **Mood:** Energetic, melancholic undertones, narrative

**Style Preset:**
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

**Representative Artists:** YOASOBI, Ado, Kenshi Yonezu, Eve, Zutomayo, Reol, Vaundy, TUYU

**Note:** Many artists came from Vocaloid/utaite scene. "Surface" = surfaced from underground to mainstream.

---

## Tier: Mainstream

**Aliases:** mainstream, normie, normie jpop, radio jpop

**Auto-tags:**
- [J-pop]
- [Band Sound]
- [Radio-friendly]
- [Sing-along Chorus]
- [Accessible]
- [Warm Production]

**Quick Reference:**
- **Tempo:** 80-140 BPM (mid-tempo comfort zone)
- **Vocal:** Smooth, relatable, sing-along friendly
- **Mood:** Warm, accessible, emotional but not chaotic

**Style Preset:**
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

**Representative Artists:** Official HIGE DANdism, Aimyon, back number, Mrs. GREEN APPLE, Spitz, Mr.Children, Kobukuro

---

## Tier: Doujin

**Aliases:** doujin, touhou, underground, convention, comiket

**Auto-tags:**
- [Doujin]
- [High Production Value]
- [Convention Scene]
- [Niche]

**Quick Reference:**
- **Tempo:** 140-200+ BPM (often very fast)
- **Vocal:** Varies by subgenre (operatic, high-pitched, aggressive)
- **Mood:** Dramatic, niche, intense, community-driven

**Production Elements:**
- Varies widely (orchestral, denpa, eurobeat, metal)
- Often very high technical skill
- Genre-specific production

**Representative Artists:** Alstroemeria Records, IOSYS, Sound Horizon, Ariabl'eyeS, COOL&CREATE

**Note:** For specific doujin styles, use subgenre keywords below.

---

## Subgenre: Doujin Symphonic

**Trigger:** `doujin symphonic`

**Additional Auto-tags:**
- [Orchestral]
- [Gothic]
- [Dramatic]
- [Epic]
- [Symphonic Metal]

**Style Preset:**
```
Doujin symphonic gothic metal, 160 bpm dramatic, dual female operatic vocals
with powerful harmonies, piano organ violin electric guitar and full orchestra,
symphonic layered production with gothic atmosphere, fantasy narrative themes,
emotion arc: tragic setup → emotional climax → bittersweet resolution
```

**Representative Artists:** Ariabl'eyeS, Sound Horizon, -LostFairy-, KOKIA, Kalafina

---

## Subgenre: Doujin Denpa

**Trigger:** `doujin denpa`

**Additional Auto-tags:**
- [Denpa]
- [Fast]
- [High-pitched]
- [Chaotic]
- [Cute]
- [Electronic]

**Style Preset:**
```
Denpa electronic, 180 bpm hyper fast, high-pitched cute female vocals with
rapid delivery, heavy synths and electronic drums, chaotic layered production,
otaku themes with playful chaos, emotion arc: cute → intense → overwhelming cute
```

**Representative Artists:** IOSYS, MOSAIC.WAV, COOL&CREATE, ARM (IOSYS)

---

## Subgenre: Doujin Eurobeat

**Trigger:** `doujin eurobeat`

**Additional Auto-tags:**
- [Eurobeat]
- [Fast]
- [Driving]
- [Synth-heavy]
- [Initial D]

**Style Preset:**
```
Eurobeat, 155 bpm driving energy, powerful female vocals with Italian disco
influence, heavy synthesizer leads and electronic drums, punchy compressed mix,
driving energy for night racing, emotion arc: adrenaline → peak → cruise
```

**Representative Artists:** A-One, various Initial D soundtrack artists

---

## Tier + Artist Merging

When both tier and artist reference are present:

1. Start with tier's auto-tags
2. Add artist's specific characteristics
3. Artist overrides tier for conflicts (e.g., tempo, vocal type)
4. User's theme shapes the emotion arc

**Example:** `/suno anisong like Aimer about farewell`

Merge process:
- From tier: `[Anime OP]`, `[Dramatic Build]`, `[High Energy]`
- From Aimer profile: husky vocals, cinematic, ballad tendency, 70-130 BPM
- Result: Anisong structure + Aimer's vocal style + slower tempo

**Generated style prompt:**
```
J-rock anime opening with cinematic ballad influence, 120 bpm dramatic,
husky female vocals with emotional depth building to powerful delivery,
guitar-forward with orchestral strings, atmospheric reverb-heavy mix,
emotion arc: quiet longing → rising tension → bittersweet farewell
```
```

**Step 2: Verify file was created**

Run: `ls -la skills/song-composition/references/jpop-tiers.md`
Expected: File exists with ~200 lines

**Step 3: Commit**

```bash
git add skills/song-composition/references/jpop-tiers.md
git commit -m "feat(suno-composer): add J-pop tier reference file

Defines 4 tiers (anisong, surface, mainstream, doujin) with:
- Keyword aliases for detection
- Auto-apply metatags
- Full style presets
- Representative artists
- Doujin subgenres (symphonic, denpa, eurobeat)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 2: Add Tier Field to Artist Profiles

**Files:**
- Modify: `skills/song-composition/references/artist-profiles.md`

**Step 1: Add tier field to each Japanese artist profile**

Add `- **Tier:** [tier]` line after each artist's `## Name` header. Categorization:

| Artist | Tier |
|--------|------|
| YOASOBI | surface |
| Yorushika | surface |
| Ado | surface |
| Eve | surface |
| Kenshi Yonezu | surface |
| LiSA | anisong |
| Aimer | anisong |
| Official HIGE DANdism | mainstream |
| King Gnu | mainstream |
| Vaundy | surface |
| RADWIMPS | mainstream |
| Mrs. GREEN APPLE | mainstream |
| Aimyon | mainstream |
| back number | mainstream |
| BUMP OF CHICKEN | mainstream |
| Fujii Kaze | mainstream |
| imase | mainstream |
| TUYU | surface |
| Zutomayo | surface |
| Creepy Nuts | mainstream |
| Ariabl'eyeS | doujin |
| Kobukuro | mainstream |
| Reol | surface |
| Hatsune Miku | surface |
| Kasane Teto | surface |
| Spitz | mainstream |
| Mr.Children | mainstream |
| Tatsuro Yamashita | legacy (city pop) |
| Yuki Kajiura | doujin |

For each artist, insert the tier line. Example transformation:

```markdown
## YOASOBI

- **Tier:** surface
- **Aliases:** yoasobi, ヨアソビ, Ayase, ikura
...
```

**Step 2: Verify changes**

Run: `grep -c "^\- \*\*Tier:\*\*" skills/song-composition/references/artist-profiles.md`
Expected: 29 (one per artist)

**Step 3: Commit**

```bash
git add skills/song-composition/references/artist-profiles.md
git commit -m "feat(suno-composer): add tier field to artist profiles

Categorizes all 29 artists by J-pop ecosystem tier:
- anisong: LiSA, Aimer
- surface: YOASOBI, Ado, Eve, Kenshi Yonezu, etc.
- mainstream: Higedan, Aimyon, back number, etc.
- doujin: Ariabl'eyeS, Yuki Kajiura

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 3: Add Tier Detection to Command

**Files:**
- Modify: `commands/suno.md`

**Step 1: Add tier detection section after Reference Detection**

Insert after line ~39 (after Reference Detection section, before Standard Mode):

```markdown
## Tier Detection

Before gathering parameters, check if $ARGUMENTS contains a J-pop tier keyword:

**Tier keywords to detect (case-insensitive):**
- Anisong: `anisong`, `anime`, `anime opening`, `anime op`, `anime ed`
- Surface: `surface`, `viral`, `viral jpop`, `producer scene`, `utaite`
- Mainstream: `mainstream`, `normie`, `normie jpop`, `radio jpop`
- Doujin: `doujin`, `touhou`, `underground`, `convention`, `comiket`
- Doujin subgenres: `doujin symphonic`, `doujin denpa`, `doujin eurobeat`

**If tier keyword detected:**
1. Read `skills/song-composition/references/jpop-tiers.md`
2. Find matching tier profile
3. Store tier data (auto-tags, style preset, tempo, production elements)
4. If artist reference ALSO detected: merge tier + artist (tier base, artist refinements)
5. Continue with normal flow

**Tier + Artist merge logic:**
- Tier provides: base metatags, general sound, structure expectations
- Artist provides: specific vocal style, production quirks, tempo override
- Artist takes precedence for conflicts (tempo, vocal type)
- User's theme shapes the emotion arc

**Example parsing:**
- `/suno anisong about courage` → tier: "anisong", theme: "about courage"
- `/suno viral jpop melancholic` → tier: "surface", theme: "melancholic"
- `/suno doujin symphonic fantasy` → tier: "doujin", subgenre: "symphonic", theme: "fantasy"
- `/suno anisong like Aimer` → tier: "anisong", artist: "Aimer" (merged)

---
```

**Step 2: Update Step 4 to use tier data**

In Step 4 (Generate Song Previews), add tier awareness. Find the "Design Song Concepts" section and update:

```markdown
2. **Design Song Concepts** (Hook-First Approach)
   - Review mood/theme requirements and user preferences
   - **If tier detected:** Start from tier's style preset as foundation
   - **If tier + artist:** Blend tier structure with artist characteristics
   - Start with the chorus hook concept - the most memorable element
   - Create evocative title (often derived from hook)
   - Plan tension/release arc: verse (low) → pre-chorus (build) → chorus (peak/release)
   - Select complementary style elements using skill knowledge
```

**Step 3: Update Step 6 to include tier in style prompt**

In Step 6 (Generate Full Songs), find "Craft Style Prompt" section and add tier handling:

```markdown
3. **Craft Style Prompt** (Descriptive prose, not just comma-separated tags)

   **If tier was detected (with or without artist):**
   - Start from tier's style preset as foundation
   - If artist also matched: blend artist characteristics (vocal, production)
   - Artist overrides tier for tempo and vocal type conflicts
   - User's theme shapes the emotion arc
   - Include tier's auto-tags in the overall style
   - Example: "J-rock anime opening [from tier], 120 bpm [from Aimer], husky female vocals [from Aimer]..."

   **If artist reference was matched (no tier):**
   ...existing content...
```

**Step 4: Verify changes**

Run: `grep -c "Tier Detection\|tier detected\|tier keyword" commands/suno.md`
Expected: At least 5 matches

**Step 5: Commit**

```bash
git add commands/suno.md
git commit -m "feat(suno-composer): add tier detection to /suno command

Scans arguments for J-pop tier keywords (anisong, surface, mainstream, doujin).
Loads tier profile from jpop-tiers.md reference.
Merges tier + artist when both specified (tier base, artist refinements).
Integrates tier data into preview and full generation steps.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 4: Update SKILL.md with Tier Documentation

**Files:**
- Modify: `skills/song-composition/SKILL.md`

**Step 1: Add tier section after Reference-Based Composition**

Find the "Reference-Based Composition" section (around line 341) and add after it:

```markdown
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

### How It Works

1. Command detects tier keyword in arguments
2. Looks up tier in `references/jpop-tiers.md`
3. If artist also specified, merges profiles
4. Generates style prompt from combined data

See `references/jpop-tiers.md` for full tier profiles and merge logic.
```

**Step 2: Update the description frontmatter**

Update the `description` field in the YAML frontmatter to include tier triggers:

```yaml
---
name: song-composition
description: This skill should be used when the user wants to compose songs for Suno AI, write lyrics, create style prompts, or generate Suno v5 metatags. Supports J-pop, K-pop, EDM, ballads, rock, and Latin genres, plus album/EP composition, acoustic or remix variations, and song continuations. Also handles reference-based composition ("like YOASOBI", "in the style of Aimer") and J-pop tier presets ("anisong", "viral jpop", "mainstream", "doujin"). Triggers on "write a song", "make a song", "Suno prompt", "Suno metatags", "Suno v5", "style of music", "song lyrics", "Suno AI", "acoustic version", "remix version", "create an album", "extend this song", "compose music", "generate lyrics", "like [artist]", "in the style of", "anisong", "viral jpop", "mainstream jpop", "doujin", "/suno".
---
```

**Step 3: Add reference to Additional Resources**

In the "Reference Files" section at the end, add:

```markdown
- **`references/jpop-tiers.md`** - J-pop ecosystem tiers (anisong, surface, mainstream, doujin) with auto-tags and style presets
```

**Step 4: Commit**

```bash
git add skills/song-composition/SKILL.md
git commit -m "docs(suno-composer): document J-pop tier presets in SKILL.md

Adds:
- J-pop Tier Presets section with usage examples
- Tier + artist combination documentation
- Updated description frontmatter with tier triggers
- Reference to jpop-tiers.md

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 5: Update SPEC.md with v4.5 Features

**Files:**
- Modify: `SPEC.md`

**Step 1: Add Phase 11 to Development Phases**

Find "Phase 10: Reference-Based Composition (v4.4)" and add after it:

```markdown
### Phase 11: J-pop Tier Presets (v4.5) ✓
- [x] Create tier reference file with 4 tiers (anisong, surface, mainstream, doujin)
- [x] Add tier field to existing artist profiles
- [x] Implement tier detection in /suno command
- [x] Support tier + artist merging
- [x] Add doujin subgenres (symphonic, denpa, eurobeat)
- [x] Document tier feature in SKILL.md
```

**Step 2: Add tier reference to Internal References**

In the "Internal References" section at the end, add:

```markdown
→ When using J-pop tier presets: `skills/song-composition/references/jpop-tiers.md`
```

**Step 3: Commit**

```bash
git add SPEC.md
git commit -m "docs(suno-composer): add v4.5 J-pop tier presets to SPEC.md

Documents Phase 11 implementation:
- Tier reference file with 4 ecosystem tiers
- Artist profile categorization
- Command integration
- Tier + artist merging

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 6: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Add tier reference to Reference files section**

Find "**Reference files:**" and add:

```markdown
- J-pop tiers: `skills/song-composition/references/jpop-tiers.md`
```

**Step 2: Update Commands section**

Add tier examples to the `/suno` command documentation:

```markdown
- `/suno` - Start guided composition workflow with file output
- `/suno [theme]` - Start with pre-defined theme
- `/suno like <artist>` - Compose using artist profile (e.g., `/suno like YOASOBI about hope`)
- `/suno anisong|surface|mainstream|doujin [theme]` - Use J-pop tier preset
- `/suno:album [concept]` - Create thematically coherent album/EP
...
```

**Step 3: Update Current Status**

Add v4.5 to the version history:

```markdown
**v4.5 (Current):** J-pop tier presets (anisong, surface, mainstream, doujin)
```

And change v4.4's "(Current)" label to just the description.

**Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(suno-composer): update CLAUDE.md for v4.5

Adds:
- Tier reference file to reference list
- Tier invocation examples to commands
- v4.5 version in status

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 7: Final Verification

**Step 1: Verify all files exist and have expected content**

```bash
# Check tier reference file
ls -la skills/song-composition/references/jpop-tiers.md

# Check artist profiles have tier field
grep -c "^\- \*\*Tier:\*\*" skills/song-composition/references/artist-profiles.md

# Check command has tier detection
grep -c "Tier Detection" commands/suno.md

# Check SKILL.md has tier section
grep -c "J-pop Tier Presets" skills/song-composition/SKILL.md

# Check SPEC.md has Phase 11
grep -c "Phase 11" SPEC.md
```

Expected:
- jpop-tiers.md exists
- 29 tier fields in artist-profiles.md
- Tier Detection in command
- J-pop Tier Presets section in SKILL.md
- Phase 11 in SPEC.md

**Step 2: Test the feature manually**

Invoke `/suno anisong about courage` and verify:
- Tier is detected
- Tier profile is loaded from jpop-tiers.md
- Style prompt uses anisong characteristics

**Step 3: Final commit (if any fixes needed)**

If any fixes were made during verification, commit them.

---

## Summary

| Task | Files | Purpose |
|------|-------|---------|
| 1 | `references/jpop-tiers.md` | Create tier profiles |
| 2 | `references/artist-profiles.md` | Add tier field to artists |
| 3 | `commands/suno.md` | Add tier detection logic |
| 4 | `SKILL.md` | Document tier feature |
| 5 | `SPEC.md` | Add v4.5 phase |
| 6 | `CLAUDE.md` | Update reference docs |
| 7 | - | Verify implementation |

Total: 6 tasks, ~7 commits
