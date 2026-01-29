---
description: Compose Suno AI songs with guided workflow
argument-hint: [theme/mode:album|variation|extend]
allowed-tools: Read, Glob, AskUserQuestion, Write, Skill, Bash
---

# Suno Song Composition Workflow

Compose songs optimized for Suno AI v5 based on user preferences and session parameters.

## Mode Detection

Parse $ARGUMENTS to detect mode:
- If starts with `:album` → Album Mode
- If starts with `:variation` → Variation Mode
- If starts with `:extend` → Extend Mode
- Otherwise → Standard Mode (existing behavior)

---

## Standard Mode (Default)

### Step 1: Load Knowledge and Preferences

First, use the Skill tool to invoke the `song-composition` skill. This provides comprehensive Suno v5 knowledge including:
- Style tags and metatags (see `references/suno-metatags.md`)
- Separated style/lyrics prompt best practices
- Advanced metatag syntax (emotion progression, vocal directions, arrangement markers)
- Production tag selection guide by genre/mood
- Genre conventions and patterns
- Song structure templates
- Lyric writing techniques

Then check for user preferences file at `.claude/suno-composer.local.md` in the current project or home directory. If found, read and note:
- Favorite genres
- Favorite artists/influences
- Preferred vocal styles
- Default languages
- Mood tendencies
- Stylistic notes
- Preferred production style (if specified)

### Step 2: Gather Session Parameters

Use AskUserQuestion to gather session-specific parameters:

**If no theme provided in arguments ($ARGUMENTS is empty):**

Ask about mood/theme with preset options:
- Upbeat - Bright, energetic, feel-good vibes
- Melancholic - Sad, bittersweet, emotional depth
- Energetic - High-energy, powerful, driving
- Dreamy - Atmospheric, ethereal, floating
- Intense - Dramatic, powerful, cinematic
- Chill - Relaxed, smooth, laid-back
- (Allow custom description)

**If theme WAS provided in arguments:**
Use the provided theme: $ARGUMENTS

**Always ask:**
1. How many songs to generate (1-10)
2. Language preference (Japanese, English, mixed, or other)
3. Vocal preference (female, male, duet, or leave to composer)

### Step 3: Compose Songs

Using the skill's knowledge directly, compose the requested number of songs following this process:

1. **Understand Parameters**
   - Review mood/theme requirements
   - Note language preferences
   - Consider vocal type preferences
   - Check for any user preferences loaded in Step 1

2. **Design Song Concept** (Hook-First Approach)
   - Start with the chorus hook - design the most memorable element first
   - Create evocative title (often derived from hook)
   - Plan tension/release arc: verse (low) → pre-chorus (build) → chorus (peak/release)
   - Apply three-element arrangement: A (melody) + B (counter) + C (rhythm)
   - Select complementary style elements using skill knowledge

3. **Write Lyrics with Advanced Metatags**
   - Match language to user preference
   - Use genre-appropriate vocabulary (consult skill references)
   - Create memorable chorus hooks
   - Embed section-specific vocal directions: `[Verse 1][soft, breathy]`
   - Add emotion progression markers: `[Bridge][Mood: vulnerable → hopeful]`
   - Include arrangement specifications: `[Chorus: Full band with strings]`
   - For Japanese: provide both characters and romanization

4. **Craft Style Prompt** (Descriptive prose, not just comma-separated tags)
   - Start with primary genre and subgenre/era influence
   - Add tempo feel (e.g., "slow around 75 bpm")
   - Include vocal style description
   - Specify key instruments
   - Add production tags based on genre/mood (see skill's Production Tag Guide)
   - Include mood and energy descriptors
   - Target 8-15 descriptive elements in flowing prose

5. **Specify Technical Details**
   - Set tempo using skill's BPM guidelines
   - Define vocal type and style progression through song
   - Describe mood arc (opening → middle → climax)
   - List key instruments by prominence
   - Note production style and key effects

**Quality Standards:**
- Lyrics must be singable with natural rhythm
- Style Prompt must be descriptive prose (not just comma-separated tags)
- Lyrics must include advanced metatags (section-specific vocal directions, emotion progression, arrangement specs)
- Production tags must match genre/mood
- Each song in a batch must feel distinct
- Japanese lyrics must include romanization
- Output must be copy-paste ready for Suno's two-field interface

### Step 4: Present Results

Display each composed song with:
- Title
- **Style Prompt** (copy-paste ready for Suno's "Style of Music" field)
- **Complete lyrics with advanced metatags:**
  - Section markers with vocal directions
  - Emotion progression markers
  - Arrangement specifications
- **Specifications** (tempo, vocal, mood arc, instruments, production style)

**Remind user:**
> Copy **Style Prompt** → Suno's "Style of Music" field
> Copy **Lyrics** (with all [bracket] tags) → Suno's "Lyrics" field

### Step 5: Save Songs (Optional)

Use AskUserQuestion to ask where to save the songs:

**Options:**
- Current directory (./songs/) - Save to songs folder in current directory
- Custom path - Let me specify a path
- Don't save - Display only, don't create files

**If saving:**

Create directory structure:
```
[output-path]/
├── [timestamp]-[theme-slug]/
│   ├── song-1-[title-slug].md      # Full song spec
│   ├── song-2-[title-slug].md
│   └── _index.md                   # Batch summary
```

**Each song file format:**
```markdown
# [Title]

## Style Prompt
[copy-paste ready for Suno]

## Lyrics
[copy-paste ready with all metatags]

## Specifications
- Tempo: ...
- Vocal: ...
- Mood Arc: ...
- Key Instruments: ...
- Production Style: ...
```

**_index.md format:**
```markdown
# [Theme] Songs - [Date]

Generated [N] songs with theme: [theme description]

## Songs
1. **[Title 1]** - [brief description]
2. **[Title 2]** - [brief description]
...

## Session Parameters
- Language: [language]
- Vocal Style: [vocal]
- User Preferences: [loaded/not loaded]
```

If user wants modifications or additional songs, gather new parameters and compose again.

---

## Album Mode (:album)

Activated by: `/suno:album [concept]`

### Step A1: Load Knowledge and Preferences
Same as Standard Step 1, plus reference `references/album-composition.md` for album patterns.

### Step A2: Gather Album Parameters

Use AskUserQuestion:

1. **Album Concept** (if not provided in arguments)
   - Narrative journey (story arc)
   - Mood exploration (emotional landscape)
   - Concept album (unified theme/character)
   - (Allow custom description)

2. **Album Type**
   - Full Album (8-12 tracks)
   - EP (4-6 tracks)
   - Mini-Album (3-4 tracks)

3. **Arc Style**
   - Journey (opener → build → peak → descent → resolution)
   - Concept (act 1 → act 2 → act 3)
   - Mood Flow (let it develop naturally)

4. **Language and Vocal Consistency**
   - Same throughout
   - Varied (composer's choice per track)

### Step A3: Compose Album

Using the skill's knowledge directly:

1. **Define Album Framework**
   - Extract concept from parameters
   - Determine arc style (journey, concept, mood flow)
   - Define thematic anchor (recurring imagery, vocabulary)
   - Establish sonic palette (core instruments, production family, tempo range)

2. **Plan Track Sequence**
   For each track position, assign:
   - Role (opener, journey, peak, descent, closer)
   - Target energy level
   - Emotional function
   - Key relationship to adjacent tracks

3. **Generate Each Track**
   For each track:
   - Apply position-specific guidelines from `references/album-composition.md`
   - Use sonic palette constraints
   - Include thematic callbacks where appropriate
   - Ensure track works standalone AND in sequence

### Step A4: Present Album

Display:
- **Album Overview** (concept, sonic palette, arc description)
- **Track Listing** with position context
- **Individual Songs** (standard format)
- **Sequencing Notes** (transitions, listening order)

### Step A5: Save Album (Optional)

Same as Standard Step 5, but with album structure:
```
[output-path]/
├── [timestamp]-[album-name]/
│   ├── _album.md                   # Album overview
│   ├── 01-[title-slug].md          # Track 1
│   ├── 02-[title-slug].md          # Track 2
│   └── ...
```

---

## Variation Mode (:variation)

Activated by: `/suno:variation [source]`

### Step V1: Load Knowledge
Load skill plus reference `references/variation-patterns.md`.

### Step V2: Gather Source Material

If source provided in arguments, use it. Otherwise, use AskUserQuestion:

1. **Source Song** - Ask user to paste or describe:
   - Style Prompt of original song
   - Key lyrics/hook
   - Theme summary

### Step V3: Select Variation Types

Use AskUserQuestion with multiSelect:
- Acoustic (organic, intimate transformation)
- Remix (electronic, dance transformation)
- Stripped (minimal, vocal showcase)
- Extended (full arrangement, added sections)
- Cinematic (orchestral, epic treatment)

(User can select multiple)

### Step V4: Generate Variations

Using the skill's knowledge directly:

1. **Analyze Source**
   - Extract core hook (melodic, lyrical, or both)
   - Identify key theme
   - Note original style elements

2. **Apply Transformations**
   For each requested variation type, consult `references/variation-patterns.md`:
   - Apply style prompt modifications
   - Adapt arrangement per transformation matrix
   - Adjust metatags appropriately
   - Preserve core hook identity

### Step V5: Present Variations

Display:
- **Source Summary** (hook, theme, original style)
- **Each Variation** with:
  - Transformation notes (what changed)
  - Style Prompt
  - Lyrics with adapted metatags
  - Specifications
- **Comparison Table** (tempo, production, instruments)

### Step V6: Save Variations (Optional)

Same as Standard Step 5, with variation structure:
```
[output-path]/
├── [timestamp]-[source-title]-variations/
│   ├── _source.md                  # Source summary
│   ├── acoustic-version.md
│   ├── remix-version.md
│   └── ...
```

---

## Extend Mode (:extend)

Activated by: `/suno:extend [direction]`

### Step E1: Load Knowledge
Load skill plus reference `references/continuation-patterns.md`.

### Step E2: Gather Source Context

Use AskUserQuestion:

1. **Previous Song Context** - Ask user to paste:
   - Style Prompt
   - Key lyrics excerpt
   - Ending/final emotion

2. **Continuation Type:**
   - Sequel (story continues forward)
   - Prequel (origin story)
   - Response (answer from different perspective)
   - Alternate POV (same events, different narrator)
   - Epilogue (reflection from distance)

### Step E3: Generate Continuation

Using the skill's knowledge directly:

1. **Extract Source DNA**
   - Identify thematic elements
   - Note sonic characteristics (tempo, key, instruments, production)
   - Find callback opportunities (phrases, imagery)

2. **Plan Continuation**
   Based on continuation type (from `references/continuation-patterns.md`):
   - Sequel: Advance narrative, maintain sonic palette
   - Prequel: Origin story, slightly rawer sound
   - Response: Counter-perspective, mirror structure
   - Alternate POV: Same events, different emotional angle
   - Epilogue: Distant reflection, mature sound

3. **Generate with Callbacks**
   - Include at least 2 lyrical callbacks (direct quote, paraphrase, or inversion)
   - Maintain sonic DNA (tempo ±15 BPM, related key, shared instrument)
   - Create distinct identity while honoring connection

### Step E4: Present Continuation

Display:
- **Connection Summary** (shared elements, narrative bridge)
- **New Song** (standard format with callback annotations)
- **Listening Order** recommendation

### Step E5: Save Continuation (Optional)

Same as Standard Step 5, with continuation structure:
```
[output-path]/
├── [timestamp]-[continuation-title]/
│   ├── _connection.md              # Connection summary
│   ├── [new-song-title].md
│   └── listening-order.md
```
