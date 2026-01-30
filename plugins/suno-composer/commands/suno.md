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

### Step 3: Ask Save Location

Before composing, ask where to save the songs:

**Options:**
- Current directory (`./songs/`) - Recommended, saves tokens
- Custom path - Let me specify a path
- Don't save - Display full content in console (⚠️ uses more tokens)

**Note:** Saving to files is recommended as it avoids outputting full lyrics to console twice (once for review, once for saving).

### Step 4: Generate Song Previews

Generate **metadata previews only** (no full lyrics yet) for each song:

1. **Design Song Concepts** (Hook-First Approach)
   - Review mood/theme requirements and user preferences
   - Start with the chorus hook concept - the most memorable element
   - Create evocative title (often derived from hook)
   - Plan tension/release arc: verse (low) → pre-chorus (build) → chorus (peak/release)
   - Select complementary style elements using skill knowledge

2. **Output Preview Format** (for each song):

```
### Song [N]: [Title]
- **Genre/Style:** [primary genre, subgenre, key descriptors]
- **Tempo:** ~[BPM] BPM, [feel]
- **Vocal:** [type], [style description]
- **Structure:** [section flow, e.g., Intro → Verse → Pre-Chorus → Chorus → ...]
- **Theme:** [1-line description of emotional/narrative content]
- **Hook Concept:** [brief description of the chorus hook idea]
```

**Important:** Do NOT generate full lyrics at this stage. Only metadata previews.

### Step 5: Confirm or Modify

Use AskUserQuestion to let user review previews:

**Options:**
- Confirm all - Generate full songs and write to files
- Modify song N - Adjust that song's direction (ask which song and what to change)
- Regenerate all - New set of previews with different concepts

**If "Modify song N":**
- Ask what to change (genre, mood, structure, etc.)
- Regenerate only that song's preview
- Return to confirmation step

**If "Regenerate all":**
- Generate entirely new preview set
- Return to confirmation step

### Step 6: Generate Full Songs to Files

**Only after user confirms**, generate complete songs with:

1. **Understand Parameters**
   - Review mood/theme requirements
   - Note language preferences
   - Consider vocal type preferences
   - Check for any user preferences loaded in Step 1

2. **Write Lyrics with Sparse Technique Tags**
   - Match language to user preference
   - Use genre-appropriate vocabulary (consult skill references)
   - Create memorable chorus hooks
   - **Tag only 3-4 inflection points** - intro, breakdown, build, final chorus
   - **Most sections get no tag** - `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]` stand alone
   - **Use technique cues** not emotion words: `[half-time]`, `[key change up]`, `[stripped]`
   - **Avoid** intensity words on every section: `[building]`, `[soaring]`, `[triumphant]`
   - **Emotion arc goes in style prompt** - Suno V5 reads it there
   - For Japanese: provide romanization optionally for pronunciation clarity

3. **Craft Style Prompt** (Descriptive prose, not just comma-separated tags)
   - Start with primary genre and subgenre/era influence
   - Add tempo feel (e.g., "slow around 75 bpm")
   - Include vocal style description
   - Specify key instruments
   - Add production tags based on genre/mood (see skill's Production Tag Guide)
   - Include mood and energy descriptors
   - Target 8-15 descriptive elements in flowing prose

4. **Specify Technical Details**
   - Set tempo using skill's BPM guidelines
   - Define vocal type and style progression through song
   - Describe mood arc (opening → middle → climax)
   - List key instruments by prominence
   - Note production style and key effects

**Quality Standards:**
- Lyrics must be singable with natural rhythm
- Style Prompt must include **emotion arc** (e.g., "intimate verse → euphoric chorus → stripped bridge → triumphant finale")
- Lyrics use **sparse tagging** - only 3-4 technique cues at inflection points
- Most sections have only the section marker - structure creates contrast
- Production tags must match genre/mood
- Each song in a batch must feel distinct
- Output must be copy-paste ready for Suno's two-field interface

**Write directly to files** (if save location was specified):

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

**If "Don't save" was selected:** Output full songs to console (warn that this uses more tokens).

### Step 7: Show Summary

Display brief completion summary:

```
✅ Songs written successfully!

📁 Files created:
- ./songs/[timestamp]-[theme]/song-1-[title].md
- ./songs/[timestamp]-[theme]/song-2-[title].md
- ./songs/[timestamp]-[theme]/_index.md

📋 Quick reference:
1. [Title 1] - [genre, tempo]
2. [Title 2] - [genre, tempo]

💡 Reminder: Copy Style Prompt → Suno's "Style of Music" field
              Copy Lyrics → Suno's "Lyrics" field
```

**Do NOT output full lyrics to console when saving to files.** The summary is sufficient.

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

### Step A3: Ask Save Location

Same as Standard Step 3. Ask where to save before generating previews.

### Step A4: Generate Album Previews

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

3. **Output Album Preview:**

```
## Album: [Album Title]
**Concept:** [1-2 sentence description]
**Sonic Palette:** [core instruments, production style, tempo range]
**Arc:** [journey/concept/mood flow description]

### Track Listing Preview:
1. **[Title]** (Opener) - [genre], ~[BPM] BPM - [1-line theme]
2. **[Title]** (Journey) - [genre], ~[BPM] BPM - [1-line theme]
3. **[Title]** (Build) - [genre], ~[BPM] BPM - [1-line theme]
...
N. **[Title]** (Closer) - [genre], ~[BPM] BPM - [1-line theme]
```

**Important:** Do NOT generate full lyrics at this stage. Only metadata previews.

### Step A5: Confirm or Modify

Same as Standard Step 5. Use AskUserQuestion:
- Confirm all - Generate full album and write to files
- Modify track N - Adjust that track's direction
- Regenerate all - New album concept and previews

### Step A6: Generate Full Album to Files

**Only after user confirms**, generate complete tracks following Standard Step 6 quality standards.

Write to album structure:
```
[output-path]/
├── [timestamp]-[album-name]/
│   ├── _album.md                   # Album overview
│   ├── 01-[title-slug].md          # Track 1
│   ├── 02-[title-slug].md          # Track 2
│   └── ...
```

### Step A7: Show Summary

Same as Standard Step 7, but include album-specific info:
- Album title and concept
- All track files created
- Sequencing notes

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

### Step V4: Ask Save Location

Same as Standard Step 3. Ask where to save before generating previews.

### Step V5: Generate Variation Previews

Using the skill's knowledge directly:

1. **Analyze Source**
   - Extract core hook (melodic, lyrical, or both)
   - Identify key theme
   - Note original style elements

2. **Output Variation Previews:**

```
## Source: [Original Title]
**Hook:** [core hook preserved across variations]
**Theme:** [central theme]

### Variation Previews:
1. **Acoustic Version** - ~[BPM] BPM, [key changes from original]
2. **Remix Version** - ~[BPM] BPM, [key changes from original]
...
```

**Important:** Do NOT generate full lyrics at this stage.

### Step V6: Confirm or Modify

Same as Standard Step 5. Use AskUserQuestion:
- Confirm all - Generate full variations and write to files
- Modify variation N - Adjust transformation approach
- Regenerate all - New variation concepts

### Step V7: Generate Full Variations to Files

**Only after user confirms**, apply transformations following Standard Step 6 quality standards.

Write to variation structure:
```
[output-path]/
├── [timestamp]-[source-title]-variations/
│   ├── _source.md                  # Source summary
│   ├── acoustic-version.md
│   ├── remix-version.md
│   └── ...
```

### Step V8: Show Summary

Same as Standard Step 7, with comparison table (tempo, production, instruments).

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

### Step E3: Ask Save Location

Same as Standard Step 3. Ask where to save before generating previews.

### Step E4: Generate Continuation Preview

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

3. **Output Continuation Preview:**

```
## Continuation: [New Title] ([Type])
**Connection to Source:** [how it relates]
**Genre/Style:** [genre, key sonic DNA elements]
**Tempo:** ~[BPM] BPM
**Theme:** [1-line description]
**Planned Callbacks:** [2-3 callback concepts]
```

**Important:** Do NOT generate full lyrics at this stage.

### Step E5: Confirm or Modify

Same as Standard Step 5. Use AskUserQuestion:
- Confirm - Generate full continuation and write to file
- Modify - Adjust direction or callbacks
- Regenerate - New continuation concept

### Step E6: Generate Full Continuation to File

**Only after user confirms**, generate with callbacks following Standard Step 6 quality standards:
- Include at least 2 lyrical callbacks (direct quote, paraphrase, or inversion)
- Maintain sonic DNA (tempo ±15 BPM, related key, shared instrument)
- Create distinct identity while honoring connection

Write to continuation structure:
```
[output-path]/
├── [timestamp]-[continuation-title]/
│   ├── _connection.md              # Connection summary
│   ├── [new-song-title].md
│   └── listening-order.md
```

### Step E7: Show Summary

Same as Standard Step 7, with listening order recommendation.
