---
description: Compose Suno AI songs with guided workflow
argument-hint: [theme/concept]
allowed-tools: Read, Glob, AskUserQuestion, Task
---

# Suno Song Composition Workflow

Compose songs optimized for Suno AI v5 based on user preferences and session parameters.

## Step 1: Load Knowledge and Preferences

First, use the Skill tool to invoke the `song-composition` skill. This provides comprehensive Suno v5 knowledge including:
- Style tags and metatags (see `references/suno-metatags.md`)
- **Separated style/lyrics prompt best practices**
- **Advanced metatag syntax (emotion progression, vocal directions, arrangement markers)**
- **Production tag selection guide by genre/mood**
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
- **Preferred production style (if specified)**

## Step 2: Gather Session Parameters

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

## Step 3: Compose Songs

Use the Task tool to invoke the `song-composer` agent with the gathered parameters:
- Theme/mood from Step 2
- Song count
- Language preference
- Vocal preference
- User preferences from Step 1 (if loaded)

The agent will generate complete compositions using the skill's knowledge of Suno v5 conventions.

## Step 4: Present Results

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
