---
description: Compose Suno AI songs with creative or guided workflow, adaptive preferences, and session reflection
argument-hint: "[theme, artist, mood, or album/variation/extend intent]"
allowed-tools: Read, Glob, AskUserQuestion, Write, Skill
---

# Suno Song Composition

Compose songs optimized for Suno AI v5.

## Step 0: Load Context

### Preferences

1. Check for preference files: `~/.claude/suno-composer.local.md` (global), `.claude/suno-composer.local.md` (project)
2. If both exist: merge (project sections override matching global sections, global fills gaps)
3. If neither exists: trigger First-Run Wizard

### First-Run Wizard

**Trigger:** No preference file at either location.

1. Offer setup: "No preferences found. Quick setup? (~20 seconds)"
   - Options: "Yes" / "Skip"
2. If yes, ask 2-3 questions via AskUserQuestion:
   - Favorite genres + vocal style (single multiSelect)
   - Default language
   - Save location (global vs project)
3. Write preferences to chosen location:
   ```markdown
   # Suno Composer Preferences
   ## Favorite Genres
   ## Preferred Vocal Styles
   ## Default Languages
   ```

### Load Skill

Invoke the `suno` skill via the Skill tool.

### Detect Intent

| Signal | Mode | Context Load |
|--------|------|-------------|
| Album/EP/multi-track intent ("album about...", "5-track EP", "collection of...") | Album | `references/album-composition.md` |
| Variation intent ("acoustic version", "remix of", "stripped down") | Variation | `references/variation-patterns.md` |
| Continuation intent ("sequel to", "what happens next", "prequel", "response song") | Extend | `references/continuation-patterns.md` |
| Artist reference ("like X", "in the style of X") | Vision-First | `references/artist-profiles.md` |
| Tier keyword (anisong, surface, mainstream, doujin, legacy) | Vision-First | `references/jpop-tiers.md` |
| Rich creative direction (theme + genre/mood) | Vision-First | — |
| Sparse or empty input | Guided | — |
| Ambiguous | Ask via AskUserQuestion | — |

If both tier and artist detected: tier provides base sound, artist provides specific refinements. Artist takes precedence for conflicts.

---

## Shared Workflow

All modes follow this core pattern after gathering parameters:

1. **Preview** — Generate metadata previews (no full lyrics yet)
2. **Confirm** — User approves, modifies, or regenerates via AskUserQuestion
3. **Generate** — Write full songs following these standards:
   - Singable lyrics with natural rhythm (6-10 syllables/line)
   - Narrative style prompt (8-15 elements, temporal flow, emotion arc woven in)
   - Top-anchor strategy (lead style prompt with vocal persona)
   - Sparse tagging (3-4 inflection points only; technique cues, not emotion words)
   - Copy-paste ready for Suno
4. **Save** — Write to `./songs/[timestamp]-[slug]/` directory
   - Each song: `song-N-[title-slug].md` with Style Prompt, Lyrics, Specifications sections
   - Index file: `_index.md` with track listing
   - See `references/output-formats.md` for full templates
5. **Summarize** — Show file paths and quick copy-paste reminder

---

## Vision-First Mode

Default for rich input.

### Interpret & Propose

Parse creative direction and immediately envision concept, format (single/EP/album), sound, language, and vocals. Infer from context; ask only when genuinely ambiguous.

Present a vivid creative vision — imagery, not metadata:

```
I'm imagining "[Title]" — a [N]-track [format] about [vivid concept]:

1. "[Track]" — [emotional/narrative hook]
2. "[Track]" — [story progression or mood shift]
...

Sound: [genre feel], [tempo], [production]. [Language] lyrics, [vocal character].

Shall I compose this? Or adjust the direction?
```

Make specific artistic choices. Don't hedge with "could be X or Y."

### Iterate

Handle natural reactions: "darker", "fewer tracks", "make it Korean", "not quite, I meant..." — adjust and re-present until confirmed. Then proceed to Shared Workflow.

---

## Guided Mode

Triggered by empty or sparse input.

### Gather Parameters

Ask via AskUserQuestion, combining where possible:
1. **Mood/Theme** — Upbeat, Melancholic, Energetic, Dreamy, Intense, Chill, or custom
2. **Song Count** — 1, 2-3, 4-6 (EP)
3. **Language** — Japanese, English, Korean, Mixed
4. **Vocals** — Female, Male, Duet, Composer's Choice

Smart defaults: if user provided partial info (e.g., "japanese ballad"), pre-fill known values and skip those questions.

### Preview & Confirm

Generate metadata previews per song (title, direction, genre, tempo, vocal, arc, hook concept). Then proceed to Shared Workflow.

---

## Album Mode

Activated when user describes an album, EP, or multi-track collection.

### Gather Parameters

1. **Album Concept** (if not in arguments) — narrative journey, mood exploration, or concept album
2. **Album Type** — Full Album (8-12), EP (4-6), Mini-Album (3-4)
3. **Arc Style** — Journey (opener -> build -> peak -> descent -> resolution), Concept (acts), or Mood Flow

### Preview & Confirm

Define album framework: thematic anchor, sonic palette, tempo range. Plan track sequence with roles (opener, journey, peak, descent, closer) and energy levels.

Preview format:
```
## Album: [Title]
Concept: [description] | Sonic Palette: [instruments, production, tempo range]

1. [Title] (Opener) — [genre], ~[BPM] — [theme]
2. [Title] (Journey) — [genre], ~[BPM] — [theme]
...
```

Then proceed to Shared Workflow. Write to album structure: `[timestamp]-[album-name]/` with `_album.md` overview + numbered track files.

---

## Variation Mode

Activated when user requests a transformed version of an existing song.

### Gather Source & Types

1. Ask for source song (style prompt, key lyrics, theme) if not provided
2. Select variation types via multiSelect: Acoustic, Remix, Stripped, Extended, Cinematic

### Preview & Confirm

Analyze source DNA (hook, theme, sonic elements). Preview each variation with key transformations from original.

Then proceed to Shared Workflow. Write to: `[timestamp]-[source]-variations/` with `_source.md` + variation files.

---

## Extend Mode

Activated when user wants a narrative continuation of an existing song.

### Gather Source & Direction

1. Ask for source context (style prompt, key lyrics, ending emotion)
2. Select continuation type: Sequel, Prequel, Response, Alternate POV, Epilogue

### Preview & Confirm

Extract source DNA and plan continuation based on type. Include planned callbacks (2-3 lyrical callbacks per song). Preview with connection description and callback concepts.

Then proceed to Shared Workflow. Maintain sonic DNA (tempo +/-15 BPM, related key, shared instruments). Write to: `[timestamp]-[title]/` with `_connection.md` + song file + `listening-order.md`.

---

## Session Reflection

After composition, naturally reflect on patterns observed during the session. Skip for single-song sessions or brief interactions.

**Reflect when** multiple songs revealed consistent creative patterns (genre, mood, artist, mode, language preferences).

**Offer conversationally** — one specific observation, not a checklist:
> "You referenced Aimer three times. Should I default to her style?"

**If accepted:** Ask global vs project, then append to `.local.md` in natural language. Add to existing sections or create new ones. Keep observations specific and actionable.

**If no patterns emerged:** End session without reflection.
