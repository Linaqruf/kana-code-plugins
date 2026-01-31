---
name: suno
version: 5.3.2
description: Compose Suno AI songs with creative or guided workflow, adaptive preferences, and session reflection
argument-hint: [creative direction] or :guided/:creative/:album/:variation/:extend
allowed-tools: Read, Glob, AskUserQuestion, Write, Skill
---

# Suno Song Composition

Compose songs optimized for Suno AI v5. Supports two primary modes:
- **Vision-First Mode** (default for rich input) - Claude proposes creative vision, user reacts
- **Guided Mode** (`:guided` flag or sparse input) - Step-by-step wizard with structured choices

---

## Step 0: Load Preferences & Skill

### Load Preferences

Check for preference files in this order:
1. **Global:** `~/.claude/suno-composer.local.md`
2. **Project:** `.claude/suno-composer.local.md`

**Merge Logic:**
- If **NEITHER exists** → Trigger First-Run Wizard (see below)
- If **both exist** → Merge (project sections override matching global sections, global fills gaps)
- If **one exists** → Use that one

When merging:
1. Start with global preferences as base
2. For each section in project file, override the matching global section
3. Sections only in global → keep them
4. Sections only in project → add them

### First-Run Wizard

**Trigger:** No preference file exists at either location.

Before proceeding with composition, run this quick setup wizard using AskUserQuestion:

**Intro prompt:**
> "I don't have your preferences yet. Quick setup? (3-5 questions, ~30 seconds)"

Use AskUserQuestion with options:
- "Yes, let's do it" → Proceed with wizard
- "Skip for now" → Skip wizard, ask again next time
- "Don't ask again" → Create empty marker file and proceed

**If "Don't ask again":**
Write to `.claude/suno-composer.local.md`:
```markdown
# Suno Composer Preferences
<!-- preferences-wizard: dismissed -->
```

**If "Yes, let's do it":**

**Q1: Genres** (multiSelect, pick 1-3)
```
Question: "What genres do you gravitate toward?"
Options:
- J-pop / Anime
- K-pop
- Western Pop/Rock
- EDM / Electronic
- Ballads / Acoustic
```

**Q2: Vocal Style** (single select)
```
Question: "Preferred vocal style?"
Options:
- Female vocals
- Male vocals
- Either / Mixed
- Synth / Vocaloid
```

**Q3: Language** (single select)
```
Question: "Default language for lyrics?"
Options:
- Japanese
- English
- Korean
- Mixed / Flexible
```

**Q4: Artists** (single text question - use AskUserQuestion with open-ended option)
```
Question: "Any favorite artists to reference? (optional - skip if unsure)"
Options:
- "Skip this question"
- Other (allow custom text input)
```

**Q5: Save Location** (single select)
```
Question: "Where should I save these preferences?"
Options:
- "All projects (global)" → Save to ~/.claude/suno-composer.local.md
- "This project only" → Save to .claude/suno-composer.local.md
```

**Write Preferences File:**

After collecting answers, write to the chosen location:

```markdown
# Suno Composer Preferences

## Favorite Genres
- [selected genres, one per line]

## Preferred Vocal Styles
- [selected vocal style]

## Default Languages
- [selected language]

## Favorite Artists/Influences
- [if provided, otherwise omit this section]
```

### Load Knowledge

Use the Skill tool to invoke the `song-composition` skill. This provides comprehensive Suno v5 knowledge.

Store loaded preferences in context for use during composition.

### Mode Detection

Parse $ARGUMENTS to detect mode:

**Explicit flags (check first):**
- `:guided` → Guided Mode
- `:creative` → Vision-First Mode (ask for creative direction if empty)
- `:album` → Album Mode (see Album Mode section)
- `:variation` → Variation Mode (see Variation Mode section)
- `:extend` → Extend Mode (see Extend Mode section)

**No flag - evaluate input richness:**

| Input Type | Examples | Mode |
|------------|----------|------|
| **RICH** (3+ descriptive words, artist+theme, genre+modifier) | `doujin gothic waltz storytelling`, `like YOASOBI about hope`, `anisong energetic battle anthem` | Vision-First |
| **SPARSE** (0-2 generic words) | (empty), `upbeat`, `sad song` | Guided |
| **AMBIGUOUS** (2 specific words) | `epic battle`, `doujin` | Offer choice |

**If offering choice (ambiguous input):**

Use AskUserQuestion:
- "Guide me through options" → Guided Mode
- "Run with this direction" → Vision-First Mode

---

## Reference & Tier Detection

**Before proceeding in either mode**, detect references in $ARGUMENTS:

### Artist Reference Detection

**Patterns:**
- `like [artist]` → extract artist name
- `in the style of [artist]` → extract artist name
- `similar to [artist]` → extract artist name
- `[artist]-style` → extract artist name

**If detected:**
1. Read `skills/song-composition/references/artist-profiles.md`
2. Search for artist name (case-insensitive)
3. Store profile data for creative interpretation

### Tier Detection

**Keywords (case-insensitive):**
- Anisong: `anisong`, `anime`, `anime opening`, `anime op`, `anime ed`
- Surface: `surface`, `viral`, `viral jpop`, `producer scene`, `utaite`, `neo jpop`, `nico nico`
- Mainstream: `mainstream`, `normie`, `normie jpop`, `radio jpop`
- Doujin: `doujin`, `touhou`, `underground`, `convention`, `comiket`
- Doujin subgenres: `doujin symphonic`, `doujin denpa`, `doujin eurobeat`
- Legacy: `legacy`, `classic`, `golden age`, `city pop`

**If detected:**
1. Read `skills/song-composition/references/jpop-tiers.md`
2. Store tier data for style foundation

**Merge logic (tier + artist):**
- Tier provides: base metatags, general sound, structure expectations
- Artist provides: specific vocal style, production quirks, tempo override
- Artist takes precedence for conflicts

---

## Vision-First Mode

> Triggered by rich input or explicit `:creative` flag.

### VF-1: Interpret & Imagine

Parse the creative direction and immediately envision:

- **Concept:** What's the song/EP about? Setting, characters, emotional core
- **Format:** Infer song count from context:
  - "storytelling" / "EP" / "album" → 4-6 tracks
  - Single theme / "song about" → 1-3 tracks
  - "a song" → 1 track
- **Sound:** Genre, tempo feel, production style, key instruments
- **Language:** Infer from genre context:
  - doujin / anisong / j-pop → Japanese
  - k-pop → Korean
  - else → English (or ask if genuinely ambiguous)
- **Vocals:** Infer from style conventions and any artist reference

### VF-2: Present Creative Vision

Present a vivid creative vision (NOT just metadata):

```
I'm imagining "[Evocative Title]" — a [N]-track [format] about [vivid concept description]:

1. "[Track Title]" — [One-line emotional/narrative hook]
2. "[Track Title]" — [Story progression or mood shift]
...

Sound: [Genre description with feeling], [tempo feel], [key production elements].
[Language] lyrics, [vocal description with character].

Shall I compose this? Or adjust the direction?
```

**Key principles:**
- Make specific artistic choices (don't hedge with "could be X or Y")
- Present vivid imagery, not just technical specs
- Mention inferred choices so user can easily correct them

### VF-3: User Reacts

Handle natural iteration:

| User says | Action |
|-----------|--------|
| "yes" / "do it" / "compose" / "perfect" | Proceed to generation (VF-4) |
| "darker" / "lighter" / "more intense" | Adjust tone, re-present vision |
| "only 3 tracks" / "make it an EP" | Adjust count, re-present |
| "make track 3 a duet" | Specific adjustment, re-present |
| "actually make it Korean" | Language change, acknowledge and proceed |
| "not quite, I meant..." | Clarify, re-interpret, re-present |

### VF-4: Generate (After Confirmation)

Once user confirms:

1. **Generate full songs** with lyrics and style prompts
   - Follow the skill's output format
   - Use sparse tagging (3-4 inflection points)
   - Include emotion arc in style prompt
   - Make output copy-paste ready for Suno

2. **Save to files:**
   ```
   ./songs/[timestamp]-[theme-slug]/
   ├── song-1-[title-slug].md
   ├── song-2-[title-slug].md
   └── _index.md
   ```

3. **Show completion summary** with file paths

**Each song file format:**
```markdown
# [Title]

## Style Prompt
[copy-paste ready for Suno "Style of Music" field]

## Lyrics
[copy-paste ready for Suno "Lyrics" field with metatags]

## Specifications
- Tempo: ...
- Vocal: ...
- Mood Arc: ...
- Key Instruments: ...
- Production Style: ...
```

### Vision-First: What to Ask vs. Infer

**Do NOT ask (infer instead):**
- Language (from genre context)
- Vocal type (from style conventions)
- Exact song count (propose reasonable number)
- Save location (use default `./songs/`, mention in output)
- Mood presets (they gave creative direction!)

**DO ask only when:**
- Genuine ambiguity: "Write me a song" (about what?)
- Conflicting signals: "happy sad song"
- Critical confirmation: Before generating 10+ tracks

---

## Guided Mode

> Triggered by `:guided` flag, empty input, or sparse input.

### G-1: Load Knowledge

Load the song-composition skill and user preferences (already done in Step 0).

### G-2: Combined Parameters Question

Ask ONE multi-select question combining key parameters using AskUserQuestion:

**Questions to ask (combine where possible):**

1. **Mood/Theme:** Upbeat, Melancholic, Energetic, Dreamy, Intense, Chill, [Custom]
2. **Song Count:** 1, 2-3, 4-6 (EP), 7-10 (Album)
3. **Language:** Japanese, English, Korean, Mixed, Other
4. **Vocals:** Female, Male, Duet, Composer's Choice

**Smart defaults:** If user provided partial info (e.g., `/suno:guided japanese ballad`):
- Pre-select "Japanese" for language
- Pre-select "Melancholic" for mood (ballad implies this)
- DON'T ask what's already known

**Artist lookup (if reference detected):**
- Show matched profile summary
- Ask for optional theme/mood modifier

### G-3: Save Location

Use AskUserQuestion:
- Current directory (`./songs/`) - Recommended
- Custom path
- Don't save (display in console - uses more tokens)

### G-4: Generate Song Previews

Generate **metadata previews only** (no full lyrics):

```
### Song [N]: [Title]
- **Creative Direction:** [Your artistic vision for this song]
- **Genre/Style:** [primary genre, key descriptors]
- **Tempo:** ~[BPM] BPM, [feel]
- **Vocal:** [type], [character/personality]
- **Emotional Arc:** [journey description]
- **Hook Concept:** [what makes this memorable]
```

### G-5: Confirm or Modify

Use AskUserQuestion:
- Confirm all - Generate full songs
- Modify song N - Adjust that song's direction
- Regenerate all - New set of previews

### G-6: Generate Full Songs

**Only after user confirms**, generate complete songs:

1. **Write Lyrics with Sparse Technique Tags**
   - Match language to user preference
   - Create memorable chorus hooks
   - **Tag only 3-4 inflection points** - intro, breakdown, build, final chorus
   - **Most sections get no tag** - `[Verse 1]`, `[Chorus]` stand alone
   - **Use technique cues** not emotion words: `[half-time]`, `[key change up]`, `[stripped]`

2. **Craft Style Prompt** (8-15 elements in flowing prose)
   - Start with vocal persona (top-anchor strategy)
   - Include genre, tempo feel, instruments, production
   - **Include emotion arc** (e.g., "intimate verse → euphoric chorus → stripped bridge → triumphant finale")

3. **Write to files** (if save location specified):
   ```
   [output-path]/[timestamp]-[theme-slug]/
   ├── song-1-[title-slug].md
   ├── song-2-[title-slug].md
   └── _index.md
   ```

**Quality Standards:**
- Lyrics must be singable with natural rhythm
- Style Prompt includes emotion arc
- Sparse tagging (structure creates contrast)
- Output copy-paste ready for Suno

### G-7: Show Summary

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

---

## Album Mode (:album)

Activated by: `/suno:album [concept]`

### Step A1: Load Knowledge and Preferences
Same as Step 0, plus reference `references/album-composition.md` for album patterns.

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

Same as Guided G-3. Ask where to save before generating previews.

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

Same as Guided G-5. Use AskUserQuestion:
- Confirm all - Generate full album and write to files
- Modify track N - Adjust that track's direction
- Regenerate all - New album concept and previews

### Step A6: Generate Full Album to Files

**Only after user confirms**, generate complete tracks following Guided G-6 quality standards.

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

Same as Guided G-7, but include album-specific info:
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

Same as Guided G-3. Ask where to save before generating previews.

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

Same as Guided G-5. Use AskUserQuestion:
- Confirm all - Generate full variations and write to files
- Modify variation N - Adjust transformation approach
- Regenerate all - New variation concepts

### Step V7: Generate Full Variations to Files

**Only after user confirms**, apply transformations following Guided G-6 quality standards.

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

Same as Guided G-7, with comparison table (tempo, production, instruments).

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

Same as Guided G-3. Ask where to save before generating previews.

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

Same as Guided G-5. Use AskUserQuestion:
- Confirm - Generate full continuation and write to file
- Modify - Adjust direction or callbacks
- Regenerate - New continuation concept

### Step E6: Generate Full Continuation to File

**Only after user confirms**, generate with callbacks following Guided G-6 quality standards:
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

Same as Guided G-7, with listening order recommendation.

---

## Step 8: Session Reflection

> **Skip this step if:**
> - Using `/suno:chrome` (different workflow)
> - Single song session (reflection needs patterns)
> - User explicitly rushed or said "skip"
> - Session was very brief with minimal creative decisions

### When to Reflect

Trigger reflection after completing composition when **any** of these apply:
- Multiple songs were generated (use contextual awareness, not mechanical counting)
- User made repeated creative decisions that reveal a pattern
- Session involved meaningful back-and-forth on style choices

> **Note:** "Multiple songs" means Claude observes this naturally from conversation context—there's no counter to track. If you generated songs, discussed variations, or iterated on ideas, that qualifies.

### Reflection Process

At session end, reflect naturally using these steps:

**1. Observe patterns from this session:**
- What genres/moods did the user gravitate toward?
- Did they override suggestions consistently in one direction?
- Any artist references used repeatedly?
- Did they prefer vision-first or guided mode?
- What language choices emerged?

**2. Compare against loaded preferences:**
- What's NEW that isn't already saved in their `.local.md`?
- Focus only on meaningful patterns, not one-off choices
- Don't reflect on things already documented

**3. If new patterns detected, offer conversationally:**

Use natural, specific language. Don't itemize—make it feel like an observation:

> "I noticed [specific observation]. Want me to remember this for future sessions?"

### Example Reflections

**Mood pattern:**
> "You started asking for upbeat summer vibes, but we ended up with something more bittersweet both times. I think you might prefer emotional depth over pure cheerfulness - want me to remember that?"

**Artist pattern:**
> "You referenced Aimer three times across different songs. Should I default to her style as a starting point for future sessions?"

**Mode pattern:**
> "You skipped my questions and gave direct creative direction each time. Seems like vision-first mode is your style - want me to default to that?"

**Genre pattern:**
> "Both songs ended up with that doujin symphonic vibe even though we started in different places. Should I lean that direction by default?"

**Language pattern:**
> "You went with Japanese for all the songs today, even the upbeat ones. Want me to default to Japanese unless you specify otherwise?"

### Saving Reflections

**If user agrees to save an observation:**

Ask: "Save globally (all projects) or just for this project?"

Then append to the appropriate `.local.md` file in natural language:

```markdown
## Mood Tendencies
- Gravitates toward emotional depth even when requesting upbeat themes
- Prefers bittersweet over pure cheerfulness

## Stylistic Notes
- Default to Aimer as baseline influence
- Prefers vision-first mode - skip guided questions
```

**Writing guidelines:**
- Add to existing sections if they match, otherwise create new section
- Use natural language, not bullet point dumps
- Keep observations specific and actionable
- Don't duplicate what's already in the file

### Skip Gracefully

If no meaningful patterns emerged, simply end the session without reflection. Don't force insights that aren't there.
