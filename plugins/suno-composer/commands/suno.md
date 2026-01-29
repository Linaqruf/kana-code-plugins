---
description: Compose Suno AI songs with guided workflow
argument-hint: [theme/mode:album|variation|extend]
allowed-tools: Read, Glob, AskUserQuestion, Task
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

Use the Task tool to invoke the `song-composer` agent with the gathered parameters:
- Mode: standard
- Theme/mood from Step 2
- Song count
- Language preference
- Vocal preference
- User preferences from Step 1 (if loaded)

The agent will generate complete compositions using the skill's knowledge of Suno v5 conventions.

### Step 4: Present Results

Display the agent's output directly. Each song should include:
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

If user wants modifications or additional songs, gather new parameters and invoke the agent again.

---

## Album Mode (:album)

Activated by: `/suno:album [concept]`

### Step A1: Load Knowledge and Preferences
Same as Standard Step 1, plus load `references/album-composition.md` for album patterns.

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

Use the Task tool to invoke the `song-composer` agent with:
- Mode: album
- Concept from Step A2
- Track count
- Arc style
- Coherence preferences
- User preferences

The agent will:
1. Define thematic anchor and sonic palette
2. Plan track sequence with position roles
3. Generate each track with framework constraints
4. Ensure coherence while maintaining variety

### Step A4: Present Album

Display:
- **Album Overview** (concept, sonic palette, arc description)
- **Track Listing** with position context
- **Individual Songs** (standard format)
- **Sequencing Notes** (transitions, listening order)

---

## Variation Mode (:variation)

Activated by: `/suno:variation [source]`

### Step V1: Load Knowledge
Load skill plus `references/variation-patterns.md`.

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

Use the Task tool to invoke the `song-composer` agent with:
- Mode: variation
- Source material from Step V2
- Selected variation types
- User preferences

The agent will apply transformation patterns from reference file.

### Step V5: Present Variations

Display:
- **Source Summary** (hook, theme, original style)
- **Each Variation** with:
  - Transformation notes (what changed)
  - Style Prompt
  - Lyrics with adapted metatags
  - Specifications
- **Comparison Table** (tempo, production, instruments)

---

## Extend Mode (:extend)

Activated by: `/suno:extend [direction]`

### Step E1: Load Knowledge
Load skill plus `references/continuation-patterns.md`.

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

Use the Task tool to invoke the `song-composer` agent with:
- Mode: extend
- Source context from Step E2
- Continuation type
- User preferences

The agent will:
1. Extract thematic elements and sonic DNA
2. Plan narrative bridge
3. Include appropriate callbacks
4. Generate connected but distinct song

### Step E4: Present Continuation

Display:
- **Connection Summary** (shared elements, narrative bridge)
- **New Song** (standard format with callback annotations)
- **Listening Order** recommendation
