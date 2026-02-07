# Workflow Modes

The suno skill supports multiple workflow modes for different composition scenarios.

## Standard Mode

Default single or batch song generation.

**Triggered by:** `/suno [creative direction]`

**Workflow:**
1. Parse creative direction
2. Generate song previews (metadata only)
3. User confirms or modifies
4. Generate full songs with lyrics
5. Save to files

**Best for:** One-off songs, quick compositions, batch generation of 1-5 songs.

## Album Mode

Generate thematically coherent multi-track albums.

**Triggered by:** Album/EP/multi-track intent (e.g., "album about summer memories", "5-track EP")

**Reference:** `references/album-composition.md` for detailed patterns.

### Key Concepts

- **Thematic Anchor:** Shared conceptual thread across tracks (imagery, vocabulary, narrative)
- **Sonic Palette:** Constrained but varied production elements (core instruments, tempo range)
- **Arc Structure:** Journey, concept, or mood exploration patterns
- **Track Roles:** Each position serves a function in the album arc

### Track Roles

| Role | Position | Function |
|------|----------|----------|
| Opener | Track 1 | Set tone, establish palette |
| Journey | Tracks 2-3 | Develop themes, explore variations |
| Peak | Track 4-5 | Emotional/energy climax |
| Descent | Track 6-7 | Cool down, reflection |
| Closer | Final track | Resolution, callbacks to opener |

### Album Types

- **Full Album:** 8-12 tracks
- **EP:** 4-6 tracks
- **Mini-Album:** 3-4 tracks

## Variation Mode

Generate transformed versions of a source song.

**Triggered by:** Variation intent (e.g., "acoustic version of", "remix of", "stripped down")

**Reference:** `references/variation-patterns.md` for transformation matrices.

### Variation Types

| Type | Transformation |
|------|----------------|
| **Acoustic** | Organic, intimate, stripped arrangement. Piano/guitar lead, minimal production. |
| **Remix** | Electronic, dance transformation. Added synths, new rhythms, club-ready. |
| **Stripped** | Minimal, vocal showcase. Voice + single instrument, raw emotion. |
| **Extended** | Full arrangement with added sections. New bridge, extended outro, instrumental breaks. |
| **Cinematic** | Orchestral, epic treatment. Strings, brass, dramatic dynamics. |

### Variation Principles

- Preserve core hook (melodic, lyrical, or both)
- Transform arrangement while maintaining recognizability
- Each variation should stand alone as a complete song
- Consider tempo/key changes for dramatic effect

## Extend Mode

Generate narratively connected songs (sequels, prequels, responses).

**Triggered by:** Continuation intent (e.g., "sequel to", "what happens next", "prequel")

**Reference:** `references/continuation-patterns.md` for callback techniques.

### Continuation Types

| Type | Relationship |
|------|--------------|
| **Sequel** | Story continues forward. Same narrator, later timeline. |
| **Prequel** | Origin story. How it began, slightly rawer sound. |
| **Response** | Answer from different perspective. Counter-narrator, mirror structure. |
| **Alternate POV** | Same events, different narrator. New emotional angle. |
| **Epilogue** | Reflection from distance. Mature sound, wisdom gained. |

### Continuation Principles

- Include at least 2 lyrical callbacks (direct quote, paraphrase, or inversion)
- Maintain sonic DNA (tempo ±15 BPM, related key, shared instrument)
- Create distinct identity while honoring connection
- Consider listening order for both standalone and paired experience

## Dual-Mode Command Support

The `/suno` command supports two interaction modes:

### Vision-First Mode (Rich Input)

- Claude interprets creative direction immediately
- Presents vivid creative vision for user reaction
- Iterates through natural conversation
- User role: React and refine ("darker", "fewer tracks")

### Guided Mode (Sparse Input)

- Step-by-step wizard with streamlined questions
- Claude as helpful guide through options
- User role: Select from presented choices

### Mode Selection

| Input Type | Examples | Mode |
|------------|----------|------|
| Rich (3+ descriptive words) | `doujin gothic waltz`, `like YOASOBI about hope` | Vision-First |
| Sparse (0-2 generic words) | (empty), `upbeat`, `sad song` | Guided |
| Album/variation/extend intent | `album about summer`, `acoustic version`, `sequel to` | Auto-detected |

**Regardless of mode:**
- Use sparse tagging (3-4 inflection points)
- Follow Suno v5 output format
- Apply creative interpretation over rigid lookup
- Trust artistic instincts
