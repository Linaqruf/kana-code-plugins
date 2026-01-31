# Suno Composer v5.4.1 - Walkthroughs & Troubleshooting

## Overview

**Problem:** Users lack practical guidance when compositions fail or produce poor results. The plugin has comprehensive reference material but no real-world examples or failure recovery paths.

**Solution:** Two new reference files providing:

1. **Vision-First Walkthrough** - Complete example from user input to final Suno submission
2. **Troubleshooting Guide** - Common failures, causes, and fixes

**Target Users:**
- New users learning the plugin workflow
- Users getting poor Suno results who don't know why
- Users experiencing Chrome integration failures

**Success Criteria:**
- Users can follow a real example end-to-end
- Common failures have documented solutions
- Chrome integration issues have clear workarounds

---

## Product Requirements

### Core Features

1. **Vision-First Walkthrough**
   - Full annotated example showing every step
   - User input → Claude response → iteration → final output
   - Explains WHY each decision was made
   - Shows narrative style prompt construction in practice
   - Includes actual Suno form fields and copy-paste targets

2. **Troubleshooting Guide**
   - Categorized by failure type:
     - Style prompt issues (Suno ignores tags, wrong mood)
     - Lyric issues (bad phrasing, syllable mismatch)
     - Chrome integration issues (form not found, rate limiting)
     - Preference issues (not loading, conflicts)
   - Each issue includes:
     - Symptoms (what user sees)
     - Cause (why it happens)
     - Fix (how to resolve)
     - Prevention (how to avoid)

### Out of Scope

- Guided mode walkthrough (separate v5.4.2 if needed)
- Chrome integration walkthrough (v5.4.3)
- Video/GIF tutorials (future consideration)
- Automated error detection

### User Flow

```
User encounters problem
    │
    ├─ Doesn't know how to start?
    │   └─ Read: walkthroughs.md → Vision-First section
    │
    ├─ Got poor Suno results?
    │   └─ Read: troubleshooting.md → Style Prompt Issues
    │
    ├─ Chrome integration failed?
    │   └─ Read: troubleshooting.md → Chrome Issues
    │
    └─ Preferences not working?
        └─ Read: troubleshooting.md → Preference Issues
```

---

## Technical Specification

### New Reference Files

| File | Location | Purpose |
|------|----------|---------|
| `walkthroughs.md` | `skills/song-composition/references/` | Complete workflow examples |
| `troubleshooting.md` | `skills/song-composition/references/` | Error recovery guide |

### Walkthrough Structure

```markdown
# Walkthroughs

## Vision-First Workflow Example

### The User Input
> "I want a bittersweet summer song about growing apart from childhood friends,
> something like YOASOBI but with more acoustic elements"

### Step 0: Preference Loading
(Shows what Claude checks and finds)

### Step 1: Mode Detection
(Explains why vision-first was chosen)

### Step 2: Creative Vision Proposal
(Shows Claude's actual response with annotations)

### Step 3: User Reaction & Iteration
(Shows natural iteration like "darker", "slower tempo")

### Step 4: Song Composition
(Full output with annotations explaining each choice)

### Step 5: File Output
(Shows file structure created)

### Step 6: Suno Submission
(Copy-paste guide with field mapping)

### Step 7: Session Reflection
(Example reflection if multi-song session)

### Key Takeaways
- Why narrative style prompt worked for this song
- How artist reference was blended, not copied
- Where sparse tagging was used and why
```

### Troubleshooting Structure

```markdown
# Troubleshooting Guide

## Style Prompt Issues

### Problem: Suno ignores my genre tags
**Symptoms:** Requested J-pop but got generic pop/rock sound
**Cause:** Tag list buried genre under too many descriptors
**Fix:** Move genre to front, use narrative style
**Prevention:** Lead with vocal persona + genre, not production tags

### Problem: Wrong emotional tone
**Symptoms:** Asked for bittersweet but got purely sad
**Cause:** Emotion arc missing or conflicting tags
**Fix:** Weave emotion arc into narrative, remove conflicting tags
**Prevention:** Use "builds from X to Y" phrasing

...

## Lyric Issues

### Problem: Syllables don't fit melody
**Symptoms:** Words sound rushed or stretched in Suno output
**Cause:** Line too long/short for natural phrasing
**Fix:** Rewrite to match target syllable count (8-12 per line)
**Prevention:** Read lyrics aloud with rhythm in mind

...

## Chrome Integration Issues

### Problem: Form fields not found
**Symptoms:** Error message or nothing happens
**Cause:** Suno UI changed, page not fully loaded
**Fix:** Refresh page, wait 3 seconds, retry
**Prevention:** Always verify Suno is logged in before /suno:chrome

### Problem: Rate limiting
**Symptoms:** Generation starts but fails partway
**Cause:** Too many requests in short period
**Fix:** Wait 5 minutes between generations
**Prevention:** Use preview mode to confirm before generating

...

## Preference Issues

### Problem: Project preferences not loading
**Symptoms:** Global preferences used even though project file exists
**Cause:** File in wrong location or malformed YAML
**Fix:** Verify path is `.claude/suno-composer.local.md` (not `~/.claude/`)
**Prevention:** Use first-run wizard to create file

### Problem: Preference merge unexpected
**Symptoms:** Some global preferences missing after project file created
**Cause:** Project sections override entire global sections, not merge line-by-line
**Fix:** Copy desired global content to project file
**Prevention:** Understand merge = section-level override, not deep merge
```

---

## File Structure Changes

### Modified Files

| File | Changes |
|------|---------|
| `skills/song-composition/SKILL.md` | Add reference pointers to new files |
| `README.md` | Add "Troubleshooting" section with link |
| `.claude-plugin/plugin.json` | Bump version to 5.4.1 |

### New Files

| File | Content |
|------|---------|
| `skills/song-composition/references/walkthroughs.md` | Vision-first workflow example |
| `skills/song-composition/references/troubleshooting.md` | Error recovery guide |

---

## Development Phases

### Phase 1: Vision-First Walkthrough
- [x] Write complete vision-first example with annotations
- [x] Include preference loading demonstration
- [x] Show narrative style prompt construction
- [x] Add Suno form field mapping
- [x] Review for accuracy against current command behavior

### Phase 2: Troubleshooting Guide
- [x] Document style prompt issues (5 common problems)
- [x] Document lyric issues (4 common problems)
- [x] Document Chrome integration issues (4 common problems)
- [x] Document preference issues (4 common problems)
- [x] Add prevention tips for each

### Phase 3: Integration
- [x] Add reference pointers to SKILL.md
- [x] Update README.md with troubleshooting section
- [x] Bump version to 5.4.1
- [ ] Test that new files are discoverable

---

## Success Metrics

- Users can complete a composition by following the walkthrough alone
- Common Chrome failures have documented workarounds
- Preference merge behavior is clearly explained
- New reference files are referenced from SKILL.md

---

## Open Questions

1. **Walkthrough depth:** Should we show actual Claude responses verbatim, or summarize?
   - Recommendation: Verbatim excerpts with annotation callouts

2. **Troubleshooting scope:** How many issues per category?
   - Recommendation: 3-7 per category, prioritize most common

3. **Version scope:** Is this truly minor (5.4.1) or feature-level (5.5.0)?
   - Recommendation: 5.4.1 - documentation improvement, no behavioral changes

---

## References

- Current skill: `skills/song-composition/SKILL.md`
- Output formats: `skills/song-composition/references/output-formats.md`
- User preferences: `skills/song-composition/references/user-preferences.md`
- Workflow modes: `skills/song-composition/references/workflow-modes.md`
