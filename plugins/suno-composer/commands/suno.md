---
description: Compose Suno AI songs with creative or guided workflow, adaptive preferences, craft review, and session reflection
argument-hint: "[theme, artist, mood, or album/variation/extend intent]"
allowed-tools: [Read, Glob, AskUserQuestion, Write, Skill, Task]
---

# Suno Song Composition

Compose songs optimized for current Suno models (v5/v5.5).

## Step 0: Load Context

### Preferences

1. Check for preference files: `~/.claude/suno-composer.local.md` (global), `.claude/suno-composer.local.md` (project)
2. If both exist: merge (project sections override matching global sections, global fills gaps)
3. If neither exists: trigger First-Run Wizard
4. Apply preferences silently — don't announce "I'm using your preferences", just use them. Session-specific requests always win.
5. Two preference keys gate workflow behavior:
   - `style-prompt form: both | narrative | modular` (default `both` — see Generate)
   - `lyric-critic: always | album-only | never` (default `always` — see Review)

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
| Rich creative direction (3+ descriptive elements — theme + genre/mood/artist) | Vision-First | — |
| Sparse input (0-2 generic words, or empty) | Guided | — |
| Ambiguous | Ask via AskUserQuestion | — |

If both tier and artist detected: tier provides base sound, artist provides specific
refinements; artist wins conflicts.

**Voice check (any mode):** if the user mentions a Suno Voice, Persona, or Custom
Model, note it — every style prompt this session OMITS vocal descriptors (they
conflict with the attached voice; say so once). Japanese lyrics in play → consult
`references/japanese-prosody.md` before writing any lyric.

---

## Shared Workflow

All modes follow this core pattern after gathering parameters:

1. **Preview** — Generate metadata previews (no full lyrics; recommended style form
   only — see `references/output-formats.md`)
2. **Confirm** — User approves, modifies, or regenerates via AskUserQuestion
3. **Generate** — Write full songs to these standards:
   - Lyrics paste-clean: nothing in the Lyrics block that should not be sung;
     all craft metadata (voice map, reading declarations, mora notes) in the
     Readings & Casting block
   - Language-aware prosody: English 6-10 syllables/line; Japanese by MORAE per
     `references/japanese-prosody.md`
   - Voice casting written into the lyric when the vocal config is a duet/dual
   - Style prompt in BOTH forms — modular "try first" + narrative fallback —
     unless the `style-prompt form` preference pins one; omit vocal descriptors
     if a Voice is attached
   - Exclusions (if any) in the Exclude block: ≤2, each with a replacement
   - Sparse parameterized tags: 3-4 inflection points, technique cues only
   - Copy-paste ready per the guide in `references/output-formats.md`
4. **Review** — Spawn the `lyric-critic` agent (Task tool) with: the draft
   song(s) INCLUDING Readings & Casting, declared language(s), vocal config,
   register/tier, both style forms — tagged UNVERIFIED CLAIMS. Never pass your
   rationale. Apply findings (revise once; re-check covers only revised sections).
   Advisory items are yours to weigh.
   **Skip when:** the user signals speed — any "quick / just give me / no review"
   intent, not a fixed phrase list — or preferences say `lyric-critic: never`.
   **Never skip in Album mode.** The critic is author-side only: it never adds a
   user-facing question round.
5. **Save** — Write to `./songs/[timestamp]-[slug]/` directory
   - Each song: `song-N-[title-slug].md` in the Full Song Format
   - Index file: `_index.md` with track listing
6. **Summarize** — File paths, key creative choices, copy-paste reminder
   (style field → Exclude field → lyrics field)

---

## Vision-First Mode

Default for rich input.

### Interpret & Propose

Parse the creative direction and envision 2-3 distinct concept directions. Present
them in ONE AskUserQuestion call **with previews** — each option: concept blurb,
2 sample hook lines, and the recommended-form style descriptors. Put your
recommended direction first, marked "(Recommended)". Make specific artistic
choices per option — don't hedge with "could be X or Y". "Other" is the built-in
escape hatch.

For album-scale visions, options are album concepts (anchor + arc + palette), not
per-track ideas.

### Iterate

Handle natural reactions: "darker", "fewer tracks", "make it Korean", "not quite,
I meant..." — adjust and re-present until confirmed. Then proceed to Shared
Workflow.

---

## Guided Mode

Triggered by empty or sparse input.

### Gather Parameters

Ask via AskUserQuestion, combining where possible:
1. **Mood/Theme** — Upbeat, Melancholic, Energetic, Dreamy, Intense, Chill, or custom
2. **Song Count** — 1, 2-3, 4-6 (EP)
3. **Language** — Japanese, English, Korean, Mixed
4. **Vocals** — Female, Male, Duet, Composer's Choice

Smart defaults: if the user provided partial info (e.g., "japanese ballad"),
pre-fill known values and skip those questions.

### Preview & Confirm

Generate metadata previews per song (title, direction, genre, tempo, vocal, arc,
hook concept). Then proceed to Shared Workflow.

---

## Album Mode

Activated when the user describes an album, EP, or multi-track collection.

### Gather Parameters

1. **Album Concept** (if not in arguments) — narrative journey, mood exploration, or concept album
2. **Album Type** — Full Album (8-12), EP (4-6), Mini-Album (3-4)
3. **Arc Style** — Journey (opener → build → peak → descent → resolution), Concept (acts), or Mood Flow

### Preview & Confirm

Define the album framework: thematic anchor, sonic palette, tempo range. Plan the
track sequence with roles (opener, journey, peak, descent, closer) and energy
levels.

Preview format:
```
## Album: [Title]
Concept: [description] | Sonic Palette: [instruments, production, tempo range]

1. [Title] (Opener) — [genre], ~[BPM] — [theme]
2. [Title] (Journey) — [genre], ~[BPM] — [theme]
...
```

Then proceed to Shared Workflow. The Review step is mandatory here and adds
cross-track checks (arc roles, palette consistency, tempo spread). Write to album
structure: `[timestamp]-[album-name]/` with `_album.md` overview + numbered track
files (each in Full Song Format, both style forms).

---

## Variation Mode

Activated when the user requests a transformed version of an existing song.

### Gather Source & Types

1. Ask for the source song (style prompt, key lyrics, theme) if not provided
2. Select variation types via multiSelect: Acoustic, Remix, Stripped, Extended, Cinematic

### Preview & Confirm

Analyze source DNA (hook, theme, sonic elements). Preview each variation with key
transformations from the original. Then proceed to Shared Workflow. Write to:
`[timestamp]-[source]-variations/` with `_source.md` + variation files.

---

## Extend Mode

Activated when the user wants a narrative continuation of an existing song.

### Gather Source & Direction

1. Ask for source context (style prompt, key lyrics, ending emotion)
2. Select continuation type: Sequel, Prequel, Response, Alternate POV, Epilogue

### Preview & Confirm

Extract source DNA and plan the continuation. Include 2-3 planned lyrical
callbacks per song. Preview with connection description and callback concepts.

Then proceed to Shared Workflow. Maintain sonic DNA (tempo ±15 BPM, related key,
shared instruments). Write to: `[timestamp]-[title]/` with `_connection.md` + song
file + `listening-order.md`.

---

## Session Reflection

After composition, naturally reflect on patterns observed during the session. Skip
for single-song sessions or brief interactions.

**Reflect when** multiple songs revealed consistent creative patterns (genre, mood,
artist, mode, language preferences) — including workflow patterns: repeated
critic-skips suggest offering `lyric-critic: album-only`; consistently pasting one
style form suggests pinning `style-prompt form`.

**Offer conversationally** — one specific observation, not a checklist:
> "You referenced Aimer three times. Should I default to her style?"

**If accepted:** Ask global vs project, then append to `.local.md` in natural
language. Add to existing sections or create new ones. Keep observations specific
and actionable.

**If no patterns emerged:** End session without reflection.
