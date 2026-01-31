# Output Formats for Suno Compositions

Templates for generating song output in various formats.

## Preview Format (Token-Efficient)

When generating song previews (before user confirmation), output metadata only:

```markdown
### Song [N]: [Title]
- **Genre/Style:** [primary genre, subgenre, key descriptors]
- **Tempo:** ~[BPM] BPM, [feel]
- **Vocal:** [type], [style description]
- **Structure:** [section flow, e.g., Intro → Verse → Pre-Chorus → Chorus → ...]
- **Theme:** [1-line description of emotional/narrative content]
- **Hook Concept:** [brief description of the chorus hook idea]
```

**Important:** Previews do NOT include full lyrics. This saves tokens by letting users confirm direction before full generation.

## Full Song Format (For File Output)

When composing full songs (after user confirmation), generate each song with:

```markdown
## Song: [Creative Title]

### Style Prompt
(Descriptive prose for Suno's "Style of Music" field. Include: genre, subgenre/era,
tempo feel, vocal style, key instruments, production tags, mood descriptors,
AND emotion arc. Target 8-15 elements. Copy-paste ready.)

Example:
emotional j-pop ballad, anime soundtrack influence, 75 bpm, soft female vocals
building to powerful delivery, piano-driven with orchestral strings, reverb-heavy,
emotion arc: intimate verse → building anticipation → euphoric chorus → stripped bridge → triumphant finale

### Lyrics

[Intro: Piano, atmospheric]
(instrumental)

[Verse 1]
(lyrics)

[Pre-Chorus]
(lyrics)

[Chorus]
(lyrics)

[Verse 2]
(lyrics)

[Breakdown][stripped, half-time]
(lyrics - contrast point, pull back before climax)

[Build]

[Final Chorus][key change up]
(lyrics)

[Outro]
(closing)

### Specifications
- **Tempo:** [BPM or tempo feel]
- **Vocal:** [type and style]
- **Key Instruments:** [by prominence]
- **Production Style:** [aesthetic and key effects]
- **Inflection Points:** [where the 3-4 technique tags are placed and why]
```

**Note:** Most sections have only the section marker. Tags appear only at inflection points (intro texture, breakdown contrast, build, final chorus peak).

## Copy-Paste Guide

1. **Style Prompt** → Suno's "Style of Music" field
2. **Lyrics** (with all [bracket] tags) → Suno's "Lyrics" field
3. **Specifications** → Reference for tempo lock and settings

## Album Preview Format

```markdown
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

## Variation Preview Format

```markdown
## Source: [Original Title]
**Hook:** [core hook preserved across variations]
**Theme:** [central theme]

### Variation Previews:
1. **Acoustic Version** - ~[BPM] BPM, [key changes from original]
2. **Remix Version** - ~[BPM] BPM, [key changes from original]
...
```

## Continuation Preview Format

```markdown
## Continuation: [New Title] ([Type])
**Connection to Source:** [how it relates]
**Genre/Style:** [genre, key sonic DNA elements]
**Tempo:** ~[BPM] BPM
**Theme:** [1-line description]
**Planned Callbacks:** [2-3 callback concepts]
```

## File Output Structure

When saving to files:

### Single/Batch Songs
```
./songs/[timestamp]-[theme-slug]/
├── song-1-[title-slug].md
├── song-2-[title-slug].md
└── _index.md
```

### Albums
```
./songs/[timestamp]-[album-name]/
├── _album.md                   # Album overview
├── 01-[title-slug].md          # Track 1
├── 02-[title-slug].md          # Track 2
└── ...
```

### Variations
```
./songs/[timestamp]-[source-title]-variations/
├── _source.md                  # Source summary
├── acoustic-version.md
├── remix-version.md
└── ...
```

### Continuations
```
./songs/[timestamp]-[continuation-title]/
├── _connection.md              # Connection summary
├── [new-song-title].md
└── listening-order.md
```
