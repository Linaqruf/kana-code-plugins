# Output Formats for Suno Compositions

Templates for generating song output in various formats.

**The paste-clean contract:** the Lyrics block contains ONLY what Suno should sing
or obey. Parentheticals in lyrics are SUNG as ad-libs — never put annotations, kana
counts, voice arrows, or readings there. All craft metadata lives in the
**Readings & Casting** block, which is never pasted.

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

Previews do NOT include full lyrics, and show only the recommended style-prompt
form (both forms go in the file).

## Full Song Format (For File Output)

```markdown
## Song: [Creative Title]

### Style Prompt — Modular (try first)
[4-7 weighted descriptors: genre+subgenre · mood/energy · vocal direction ·
key instruments · production/tempo. One genre anchor. Copy-paste ready.
OMIT vocal descriptors if a Suno Voice/Persona is attached.]

### Style Prompt — Narrative (fallback if the arrangement feels flat)
[Prose describing how the song unfolds in time; emotion arc woven in.
v5-tested form; same Voice rule applies.]

### Exclude (Styles field, Advanced Options — optional)
[≤2 entries, each paired with its replacement, e.g.
"no lead guitar solo — fingerpicked acoustic instead". Omit block if none.]

### Lyrics

[Intro: texture description]
(instrumental)

[Verse 1]
(lyrics — paste-clean: nothing here that should not be sung)

[Pre-Chorus]
(lyrics)

[Chorus]
(lyrics)

[Bridge: stripped, half-time]
(lyrics — parameterized tags at the 3-4 inflection points only)

[Build]

[Final Chorus: key change up]
(lyrics)

[Outro: closing texture]
(closing)

### Specifications
- **Tempo:** [BPM or tempo feel]
- **Vocal:** [type and style; note if a Suno Voice is attached]
- **Key Instruments:** [by prominence]
- **Production Style:** [aesthetic and key effects]
- **Inflection Points:** [where the 3-4 parameterized tags are placed and why]

### Readings & Casting (craft block — NOT for pasting)
- **Voice map:** [section → voice, for duet/dual configs:
  "Verse 1 = Voice A (soprano lead); Verse 2 = Voice B (darker);
  Chorus = unison→harmony; Final Chorus = B descant over A"]
- **Reading declarations:** [every double-reading and non-obvious reading:
  "永遠 → とわ (2 morae) throughout; 紅き → あかき"]
- **Mora/syllable notes:** [per hook line + any flagged line:
  "Chorus L1 あかきつきよ・とわをだいて 6+6; L4 あさはこない・それでもいい 6+6"]
- **Script pasted:** [Japanese kana/kanji | romaji — for regeneration consistency]
```

Most sections carry only the bare marker. Tags appear only at inflection points.
The lyric-critic agent consumes Lyrics + Readings & Casting together — a missing
reading declaration for an ambiguous word is itself a finding.

## Copy-Paste Guide

1. **One Style Prompt** (start with the "try first" form) → Suno's "Style of Music" field
2. **Exclude entries** (if any) → the Exclude Styles field under Advanced Options
3. **Lyrics** (with all [bracket] tags) → Suno's "Lyrics" field
4. **Specifications / Readings & Casting** → reference only, never pasted

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

Album song FILES use the Full Song Format above (both style forms, craft block per
track); chat previews stay metadata-only.

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
