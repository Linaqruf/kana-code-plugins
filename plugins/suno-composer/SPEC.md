# Suno Composer

A Claude Code plugin for composing Suno AI songs with professional songwriter techniques and a guided workflow.

## Overview

**Problem:** Composing effective prompts for Suno AI requires knowledge of style tags, song structure, genre conventions, and lyric writing techniques. Users often create generic or ineffective prompts that don't leverage Suno's full capabilities.

**Solution:** A guided composition workflow that combines professional songwriting best practices with Suno v5-specific prompting techniques, generating production-ready song specifications including lyrics, style tags, and arrangement details.

**Target Users:** Musicians, content creators, and hobbyists using Suno AI who want higher-quality song outputs with less trial and error.

**Success Criteria:**
- Songs generated follow professional structure patterns
- Style tags are optimized for Suno v5
- Output is copy-paste ready for Suno
- User preferences persist across sessions

## Current Implementation

### Components

| Component | File | Purpose |
|-----------|------|---------|
| Command | `commands/suno.md` | `/suno` - Guided composition workflow with file output |
| Command | `commands/chrome.md` | `/suno:chrome` - Interactive browser workflow |
| Skill | `skills/song-composition/SKILL.md` | Suno v5 knowledge base |
| References | `skills/song-composition/references/` | Genre deep-dives, Japanese patterns |
| Settings | `.claude/suno-composer.local.md` | User preferences |

### Workflow (v4.4 - Reference-Based + Sparse Tags)

```
┌─────────────────────────────────────────────────────────────┐
│                     /suno [theme]                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Load Knowledge & Preferences                       │
│  • Load song-composition skill                              │
│  • Check .claude/suno-composer.local.md                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Gather Session Parameters                          │
│  • Mood/theme (presets or custom)                           │
│  • Song count (1-10)                                        │
│  • Language preference                                       │
│  • Vocal preference                                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Ask Save Location                                  │
│  • ./songs/ (recommended)                                   │
│  • Custom path                                              │
│  • Don't save (⚠️ uses more tokens)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: Generate Song Previews (metadata only)             │
│  • Title, genre, tempo, vocal, structure                    │
│  • Theme summary, hook concept                              │
│  • NO full lyrics yet - saves tokens                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 5: Confirm or Modify                                  │
│  • Confirm all → proceed to generation                      │
│  • Modify song N → adjust direction                         │
│  • Regenerate all → new concepts                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 6: Generate Full Songs to Files                       │
│  • Write complete lyrics with selective metatags            │
│  • Craft style prompts (8-15 elements)                      │
│  • Save directly to files (no console duplication)          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 7: Show Summary                                       │
│  • List created files                                       │
│  • Quick reference (titles, genres)                         │
│  • Copy-paste reminder                                      │
└─────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│              /suno:chrome [theme] (v4.0)                    │
│  Requires: claude --chrome                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Interactive browser workflow:                              │
│  • Navigate to suno.com/create                              │
│  • Compose songs using skill knowledge                      │
│  • Auto-fill Suno forms                                     │
│  • Iterate in real-time before generating                   │
│  • Save compositions to files (optional)                    │
└─────────────────────────────────────────────────────────────┘
```

### Output Format (v4.3)

```
═══════════════════════════════════════════════════════════
## Song 1: [Title]
═══════════════════════════════════════════════════════════

### Style Prompt
(Descriptive prose: genre, subgenre/era, tempo feel, vocal style,
instruments, production tags, mood, AND emotion arc. 8-15 elements.
→ Copy to Suno's "Style of Music" field)

Example:
emotional j-pop ballad, anime soundtrack influence, 75 bpm,
soft female vocals building to powerful delivery, piano-driven
with orchestral strings, reverb-heavy,
emotion arc: intimate verse → euphoric chorus → stripped bridge → triumphant finale

### Lyrics

[Intro: Piano, atmospheric]
(instrumental)

[Verse 1]
(lyrics - no tag needed, structure implies lower energy)

[Pre-Chorus]
(lyrics - no tag needed, name implies "building")

[Chorus]
(lyrics - arrangement info goes in style prompt)

[Verse 2]
(lyrics)

[Breakdown][stripped, half-time]
(lyrics - TECHNIQUE TAG: contrast point)

[Build]
(lyrics - tension before climax)

[Final Chorus][key change up]
(lyrics - TECHNIQUE TAG: earned peak)

[Outro]
(closing)

→ Copy to Suno's "Lyrics" field (keep all [bracket] tags)

### Specifications
- **Tempo:** [BPM or tempo feel]
- **Vocal:** [type, style, progression]
- **Mood Arc:** [opening → development → climax]
- **Key Instruments:** [by prominence]
- **Production Style:** [aesthetic and effects]
- **Inflection Points:** [where the 3-4 technique tags are placed and why]
───────────────────────────────────────────────────────────
```

### Sparse Tagging Philosophy (v4.3)

**The 1-3-4 Rule:**
- **1** intro texture tag
- **3** technique tags max in the song body (breakdown, build, final chorus)
- **4** total inflection points maximum

**Tag only at inflection points:**
| Moment | Purpose | Example Tags |
|--------|---------|--------------|
| Intro | Set opening texture | `[Intro: Piano, atmospheric]` |
| Breakdown/Bridge | Contrast point | `[stripped]`, `[half-time]`, `[whisper]` |
| Build | Pre-climax tension | `[Build]`, `[snare roll]` |
| Final Chorus | Earned peak | `[key change up]`, `[double-time]` |

**Use technique cues, not emotion words:**
| ✅ Technique Cues | ❌ Emotion Words |
|-------------------|-----------------|
| `[stripped]`, `[half-time]` | `[vulnerable]`, `[intimate]` |
| `[key change up]` | `[triumphant]`, `[soaring]` |
| `[filtered]`, `[snare roll]` | `[building]`, `[rising tension]` |

**Why sparse works:**
- Verse/chorus contrast is built into structure
- Pre-chorus already implies "building"
- Emotion arc goes in style prompt where Suno V5 reads it
- Technique cues create actual dynamics; emotion words add noise

## Product Requirements

### Current Features (v1.0)

- [x] Guided workflow with preset moods
- [x] User preference persistence
- [x] Batch generation (1-10 songs)
- [x] Language agnostic (Japanese, English, mixed)
- [x] Basic genre support (J-pop, doujin, ballad, rock, city pop)
- [x] Suno v5 style tag generation
- [x] Song structure patterns

### Planned Enhancements (v2.0)

#### Professional Songwriter Techniques ✓

Based on research from [LANDR](https://blog.landr.com/10-songwriting-techniques/), [MI](https://www.mi.edu/in-the-know/unleashing-creativity-songwriting-techniques-every-musician-know/), and [Mixing Monster](https://mixingmonster.com/how-to-write-a-song/):

- [x] **Hook-first composition** - Design memorable hooks before filling in verses
- [x] **Tension & release patterns** - Strategic dissonance → resolution
- [x] **Three melodic elements** - Interacting melodies for arrangement flexibility
- [x] **Emotional authenticity** - Guide users to write from personal experience
- [x] **Rhythmic variation** - Subtle rhythmic changes for 52% higher recall
- [x] **Ed Sheeran method** - "Flush the dirty tap" - encourage volume over perfection

#### Advanced Suno v5 Features ✓

Based on research from [Suno Metatags Guide](https://sunometatagcreator.com/metatags-guide), [How to Prompt Suno](https://howtopromptsuno.com/), and [Suno v5 Patterns](https://plainenglish.io/blog/i-made-10-suno-v5-prompt-patterns-that-never-miss):

- [x] **Separated prompts** - Style prompt vs lyrics prompt (Suno best practice)
- [x] **Advanced metatags** - Full metatag support beyond basic sections
- [x] **Multi-layered emotion tags** - Mood progression markers (e.g., `[Mood: vulnerable → hopeful]`)
- [x] **Vocal style specificity** - "breathy", "melismatic", "monotone", etc.
- [x] **Production tags** - "dry vocal", "reverb-heavy", "side-chained bass"
- [ ] **Suno Studio awareness** - Region editing, clip settings, tempo lock guidance (see Open Questions)

#### Extended Genre Support ✓

- [x] K-pop (with romanized Korean phrases)
- [x] Western pop/rock (mainstream, indie, arena, synth-pop, etc.)
- [x] EDM subgenres (house, techno, dubstep, trance, D&B, hardstyle)
- [x] R&B/Soul (J-R&B, Neo-Soul in existing references)
- [x] Hip-hop/Rap (J-Hip-Hop, Lo-fi Hip-Hop in existing references)
- [x] Latin (reggaeton, bachata, salsa, cumbia, bossa nova, latin trap)
- [ ] Classical crossover

#### Workflow Improvements

- [x] **Album/playlist mode** - Thematic coherence across multiple songs
- [x] **Song variations** - Acoustic, remix, stripped, extended, cinematic versions
- [x] **Extend/continue mode** - Build on existing generations (sequel, prequel, response, alternate POV, epilogue)
- [ ] **Collaborative mode** - Multi-user brainstorming

### Out of Scope

- Direct Suno API integration (no public API available)
- Audio file generation (Suno handles this)
- DAW integration
- Music theory education (beyond practical application)

## Technical Architecture

### Tech Stack

| Layer | Technology |
|-------|------------|
| Platform | Claude Code Plugin |
| Format | Markdown (commands, agents, skills) |
| Config | JSON (plugin.json) |
| User Settings | Markdown (.local.md) |

### File Structure

```
suno-composer/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/
│   ├── suno.md                  # /suno command (main workflow)
│   └── chrome.md                # /suno:chrome command (browser integration)
├── skills/
│   └── song-composition/
│       ├── SKILL.md             # Core skill
│       └── references/
│           ├── album-composition.md     # Album arc patterns and coherence
│           ├── continuation-patterns.md # Song extension/sequel patterns
│           ├── genre-deep-dive.md       # Extended genre conventions
│           ├── japanese-lyric-patterns.md
│           ├── pro-techniques.md        # Professional songwriter techniques
│           ├── suno-metatags.md         # Suno v5 tags reference
│           └── variation-patterns.md    # Song variation transformations
├── examples/
│   └── suno-composer.local.md   # Example preferences
├── dev/
│   └── prompt.md                # Development session context
├── README.md
├── LICENSE
├── SPEC.md
└── CLAUDE.md
```

## Data Models

### User Preferences Schema

```typescript
interface SunoComposerPreferences {
  // Genre preferences
  favoriteGenres: string[];
  favoriteArtists: string[];

  // Vocal preferences
  preferredVocalStyles: string[];
  defaultVocalGender?: 'female' | 'male' | 'duet' | 'any';

  // Language preferences
  defaultLanguages: string[];
  allowMixedLanguage: boolean;

  // Style tendencies
  moodTendencies: string[];
  stylisticNotes: string[];

  // v2.0 additions
  preferredTempoRange?: { min: number; max: number };
  productionStyle?: 'polished' | 'lo-fi' | 'live' | 'any';
  experimentalLevel?: 'conservative' | 'moderate' | 'experimental';
}
```

### Song Output Schema (v4.3)

```typescript
interface SongComposition {
  // Identity
  number: number;
  title: string;
  titleRomanized?: string;  // For non-Latin titles

  // Content - lyrics with sparse technique tags at inflection points
  lyrics: {
    section: string;        // [Verse 1], [Chorus], etc. - most need NO extra tags
    techniqueCue?: string;  // [stripped], [key change up] - only at inflection points
    content: string;
  }[];

  // Suno-specific (v4.3: emotion arc in style prompt)
  stylePrompt: string;      // Descriptive prose, 8-15 elements INCLUDING emotion arc

  // Specifications (v4.3: added inflection points)
  tempo: string;            // BPM or tempo feel
  vocal: string;            // Type, style, and progression
  moodArc: string;          // Opening → development → climax (goes in stylePrompt)
  keyInstruments: string;   // By prominence
  productionStyle: string;  // Aesthetic and key effects
  inflectionPoints: string; // Where 3-4 technique tags are placed and why
}
```

## Suno v5 Metatags Reference

### Structure Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `[Intro]` | Opening section | `[Intro: Acoustic guitar]` |
| `[Verse]` | Narrative section | `[Verse 1]`, `[Verse 2]` |
| `[Pre-Chorus]` | Build tension | `[Pre-Chorus]` |
| `[Chorus]` | Main hook | `[Chorus]` |
| `[Bridge]` | Contrast/pivot | `[Bridge]` |
| `[Hook]` | Memorable phrase | `[Hook]` |
| `[Break]` | Pause/change | `[Break]` |
| `[Instrumental]` | No vocals | `[Instrumental Break]` |
| `[Outro]` | Closing | `[Outro: Fade out]` |
| `[Build]` | Rising intensity | `[Build]` |
| `[Drop]` | EDM climax | `[Drop]` |

### Vocal Style Tags

| Style | Use Case |
|-------|----------|
| `soft female vocals` | Ballads, intimate songs |
| `powerful female belting` | Anthems, climactic moments |
| `breathy vocals` | Dream pop, atmospheric |
| `raspy vocals` | Rock, blues |
| `melismatic` | R&B, soul |
| `monotone` | Indie, experimental rap |
| `whisper` | Intros, bridges |
| `harmonized chorus` | Group vocals |
| `call and response` | Duets, gospel |

### Production Tags

| Tag | Effect |
|-----|--------|
| `dry vocal` | Minimal reverb |
| `reverb-heavy` | Spacious, atmospheric |
| `side-chained bass` | Pumping effect |
| `lo-fi` | Vintage, warm |
| `polished` | Clean, modern |
| `compressed` | Punchy, loud |
| `wide stereo` | Expansive mix |

## Professional Songwriter Techniques

### Hook Development

1. **Melodic hooks** - 3-5 note phrases that stick
2. **Rhythmic hooks** - Distinctive rhythm patterns
3. **Lyrical hooks** - Memorable phrases/titles
4. **Instrumental hooks** - Signature riffs

### Tension & Release

```
Low tension → Building → Peak tension → Release
[Verse]      [Pre-Chorus] [Chorus drop] [Chorus resolve]
```

### Three-Element Arrangement

```
Element A: Main melody (vocals/lead)
Element B: Counter-melody (synth pad/strings)
Element C: Rhythmic hook (bass/percussion)

Combinations create section variety:
- Intro: C only
- Verse: A + C
- Chorus: A + B + C
- Bridge: B + C
```

## Development Phases

### Phase 1: Core (v1.0) ✓
- [x] Basic workflow
- [x] J-pop/doujin focus
- [x] User preferences
- [x] Batch generation

### Phase 2: Pro Techniques (v2.0) ✓
- [x] Add `references/pro-techniques.md`
- [x] Integrate hook-first composition
- [x] Add tension/release guidance
- [x] Implement three-element arrangement suggestions

### Phase 3: Advanced Suno (v2.1) ✓
- [x] Add `references/suno-metatags.md`
- [x] Implement separated style/lyrics prompts
- [x] Add advanced metatag support to output format
- [x] Include production tag suggestions in workflow

### Phase 4: Extended Genres (v2.2) ✓
- [x] Add Western pop/rock patterns
- [x] Add EDM subgenre support
- [x] Add K-pop patterns (with romanized Korean phrases)
- [x] Add Latin genre patterns

### Phase 5: Workflow Enhancements (v3.0) ✓
- [x] Album/playlist coherence mode
- [x] Song variation generation (acoustic, remix, stripped, extended, cinematic)
- [x] Extend/continue mode (sequel, prequel, response, alternate POV, epilogue)

### Phase 6: Simplified Architecture (v4.0) ✓
- [x] Remove agent overhead - inline composition logic directly in command
- [x] Add file output option for saving compositions to organized markdown files
- [x] Add `/suno:chrome` command for interactive browser workflow
- [x] Real-time iteration support with Chrome integration
- [x] Auto-fill Suno forms with composed content

### Phase 7: Preview-First Workflow (v4.1) ✓
- [x] Generate metadata previews before full lyrics (saves tokens)
- [x] Add confirm/modify/regenerate flow
- [x] Dynamic control guidelines for section tagging

### Phase 8: Tagging Refinement (v4.2) ✓
- [x] Restore expressive tags at key moments
- [x] Establish contrast philosophy (breakdown before climax)
- [x] Balance between over-tagging and under-tagging

### Phase 9: Sparse Technique Tags (v4.3) ✓
- [x] Implement 1-3-4 rule (1 intro, 3 body tags, 4 max)
- [x] Move emotion arc to style prompt (Suno V5 reads it there)
- [x] Replace emotion words with technique cues
- [x] Remove romanization from lyric output (clean lyrics only)

### Phase 10: Reference-Based Composition (v4.4) ✓
- [x] Create artist profile database (20 J-pop artists)
- [x] Add reference parsing to /suno command
- [x] Integrate profile data into style prompt generation
- [x] Document feature in SKILL.md

## Open Questions

1. **Suno Studio integration** - Should we add guidance for Suno Studio's region editing workflow?
2. **Chord progression suggestions** - Should we include chord patterns for different genres?
3. **Melody contour guidance** - How detailed should melodic direction be?
4. **BPM precision** - Use exact BPM or tempo feels (mid-tempo, uptempo)?
5. **Custom metatag builder** - Should we add a tool to help construct complex metatags?

---

## References

### Research Sources

- [LANDR - 23 Songwriting Tips](https://blog.landr.com/10-songwriting-techniques/)
- [Musicians Institute - Songwriting Techniques](https://www.mi.edu/in-the-know/unleashing-creativity-songwriting-techniques-every-musician-know/)
- [Mixing Monster - How to Write a Song 2025](https://mixingmonster.com/how-to-write-a-song/)
- [How to Prompt Suno](https://howtopromptsuno.com/)
- [Suno Metatag Creator Guide](https://sunometatagcreator.com/metatags-guide)
- [Suno v5 Prompt Patterns](https://plainenglish.io/blog/i-made-10-suno-v5-prompt-patterns-that-never-miss)
- [Jack Righteous - Suno Meta Tags Guide](https://jackrighteous.com/en-us/pages/suno-ai-meta-tags-guide)

### Internal References

→ When using Suno metatags: `skills/song-composition/references/suno-metatags.md`
→ When implementing genre patterns: `skills/song-composition/references/genre-deep-dive.md`
→ When writing Japanese lyrics: `skills/song-composition/references/japanese-lyric-patterns.md`
