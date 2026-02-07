# Troubleshooting Guide

Common issues, causes, and fixes for suno-composer workflows.

---

## Style Prompt Issues

### Problem: Suno ignores my genre

**Symptoms:** Requested J-pop but got generic pop/rock. Asked for doujin symphonic but got standard orchestral.

**Cause:** Genre tag buried under production descriptors. Suno prioritizes early tokens.

**Fix:**
```
❌ BAD: piano, emotional, reverb-heavy, female vocals, building dynamics, J-pop ballad
✅ GOOD: This J-pop ballad opens with delicate piano...
```

Move genre to the front of the style prompt, ideally in the first sentence.

**Prevention:** Use narrative style prompts. The genre naturally appears early when describing "This [genre] song..."

---

### Problem: Wrong emotional tone

**Symptoms:** Asked for bittersweet but got purely sad. Requested energetic but got frantic.

**Cause:** Emotion arc missing from style prompt, or conflicting descriptors.

**Fix:**
1. Check for conflicting tags (e.g., "melancholic" and "uplifting" together)
2. Add temporal emotion arc: "builds from X to Y"

```
❌ BAD: emotional, powerful, intimate, vulnerable
✅ GOOD: ...builds from intimate introspection to emotionally charged climax
```

**Prevention:** Weave emotion arc into the narrative. Don't append it as a separate tag list.

---

### Problem: Vocals don't match description

**Symptoms:** Asked for soft vocals, got belting. Requested male, got ambiguous.

**Cause:** Vocal description too late in prompt or too vague.

**Fix:** Use the top-anchor strategy. Vocal description should appear within the first 20 words:

```
❌ BAD: J-pop ballad at 90 bpm with piano and strings, soft female vocals...
✅ GOOD: Soft female vocals with gentle vibrato open this J-pop ballad...
```

**Prevention:** Start every style prompt with vocal character description.

---

### Problem: Arrangement doesn't build/peak

**Symptoms:** Song stays flat throughout. No dynamic contrast between verse and chorus.

**Cause:** Style prompt lacks temporal progression words.

**Fix:** Add arrangement journey to the narrative:

```
❌ BAD: piano, synths, drums, bass, strings, full production
✅ GOOD: Opens with solo piano, synth pads enter at verse, full production blooms
         at chorus, strips back to voice and piano at bridge, peaks with added strings
```

**Prevention:** Use temporal words: "opens with", "enters", "builds through", "resolves into", "peaks at".

---

### Problem: Too many instruments competing

**Symptoms:** Muddy mix, no clear lead, everything playing at once.

**Cause:** Listed too many instruments without hierarchy.

**Fix:** Establish lead instrument and describe how others support:

```
❌ BAD: piano, guitar, synths, strings, bass, drums, percussion
✅ GOOD: Piano-led arrangement with synth pads providing atmosphere,
         subtle bass pulse anchoring the low end
```

**Prevention:** Pick 1-2 lead instruments, 2-3 supporting elements. Don't list everything.

---

## Lyric Issues

### Problem: Syllables don't fit melody

**Symptoms:** Words sound rushed or stretched in Suno output. Awkward phrasing.

**Cause:** Line too long or too short for natural phrasing.

**Fix:** Target 6-10 syllables per line for most genres. Read aloud with rhythm:

```
❌ BAD: I remember all the times we spent together in the summer (15 syllables)
✅ GOOD: I remember summer days (7) / all the time we spent (5)
```

**Prevention:** Read lyrics aloud while tapping the beat before finalizing.

---

### Problem: Section markers ignored

**Symptoms:** Suno treats `[Verse 2]` as lyrics. Tags appear in the vocal.

**Cause:** Malformed brackets or unsupported marker format.

**Fix:** Use standard Suno section markers:
- `[Intro]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`
- Technique tags inline: `[Verse 1][soft]` not `[Verse 1, soft]`

**Prevention:** Check that all brackets are closed and markers match Suno's vocabulary.

---

### Problem: Technique tags not working

**Symptoms:** `[whisper]` doesn't whisper. `[key change up]` sounds the same.

**Cause:** Tag not in Suno's vocabulary, or too many competing tags.

**Fix:**
1. Use Suno-supported tags: `[whisper]`, `[stripped]`, `[half-time]`, `[key change up]`, `[spoken word]`
2. Remove redundant tags - sparse tagging (3-4 per song) works better

```
❌ BAD: [Chorus][powerful][full band][emotional peak][soaring]
✅ GOOD: [Chorus]  (no tag needed - structure implies power)
```

**Prevention:** Tag only inflection points. Trust the verse/chorus structure to create contrast.

---

### Problem: Japanese lyrics sound unnatural

**Symptoms:** Awkward pronunciation, words cut off mid-syllable.

**Cause:** Line breaks mid-word or phrase, syllable count mismatched.

**Fix:**
1. Break at natural phrase boundaries (助詞 after nouns, て-form verbs)
2. Match syllable count to melodic phrase length

```
❌ BAD: 君のことを / いつも (breaks between を and いつも awkwardly)
✅ GOOD: 君のことを いつも / 思い出してる (natural phrase break)
```

**Prevention:** Read Japanese lyrics aloud. If breath pauses feel unnatural, restructure.

---

## Preference Issues

### Problem: Preferences not loading

**Symptoms:** First-run wizard triggers even though preferences exist. Loaded preferences don't match file content.

**Cause:** File in wrong location or malformed format.

**Fix:**
1. Verify file path:
   - Global: `~/.claude/suno-composer.local.md`
   - Project: `.claude/suno-composer.local.md`
2. Check file format - must be valid Markdown with `## Section` headers
3. Ensure no syntax errors in YAML frontmatter (if present)

**Prevention:** Use first-run wizard to create preference files instead of manually writing them.

---

### Problem: Project preferences not overriding global

**Symptoms:** Global preference appears even though project file specifies different value.

**Cause:** Section names don't match exactly, or project file incomplete.

**Fix:**
1. Section names must match exactly: `## Favorite Genres` (not `## Genres`)
2. Project file overrides by section - if you want to override one genre, include the entire Favorite Genres section

```markdown
# Project file - overrides global's genre section entirely
## Favorite Genres
- K-pop

# Global's "Preferred Vocal Styles" section still applies since not overridden
```

**Prevention:** Copy section headers exactly from global file when creating project overrides.

---

### Problem: Session reflection not offering to save

**Symptoms:** Completed multi-song session but no reflection prompt appeared.

**Cause:** Single-song session (reflection triggers on 2+ songs), or explicit skip/rush signals.

**Fix:** This is expected behavior:
- Reflection only triggers for sessions with 2+ songs
- If you said "quick" or "skip" during composition, reflection is suppressed
**Prevention:** If you want reflection, compose 2+ songs in a single session without rushing.

---

### Problem: Preference conflicts not visible

**Symptoms:** Unsure why a certain preference was applied. Can't tell global vs project source.

**Cause:** Merge logic is silent by design.

**Fix:** Understand the merge behavior:
1. Start with global as base
2. Project sections override matching global sections entirely
3. Global-only sections remain
4. Project-only sections are added

To debug:
1. Read `~/.claude/suno-composer.local.md` (global)
2. Read `.claude/suno-composer.local.md` (project)
3. Mentally merge: project wins for any matching section names

**Prevention:** Keep preferences simple. Use project file only when you need project-specific overrides.

---

## General Issues

### Problem: Song quality inconsistent

**Symptoms:** Some compositions work great, others produce poor Suno output.

**Cause:** Multiple possible factors - style prompt quality, lyric pacing, or Suno randomness.

**Fix:**
1. Compare working vs non-working style prompts - look for narrative structure differences
2. Check lyric syllable counts match expected phrase lengths
3. Suno has inherent randomness - try regenerating with same prompt
4. Review inflection point tags - too many or too few?

**Prevention:** Follow the walkthrough example as a template. Narrative style prompt + sparse tagging is the most reliable pattern.

---

### Problem: Can't find generated songs

**Symptoms:** Composition completed but can't locate files.

**Cause:** Files saved to default location, or path confusion.

**Fix:**
1. Check `./songs/` directory in current working directory
2. Look for folders with timestamp prefix: `20260131-[theme-slug]/`
3. Each song has its own `.md` file plus an `_index.md`

**Prevention:** Note the file paths shown in the completion summary.

---

### Problem: Want to undo session reflection save

**Symptoms:** Accidentally approved a reflection that doesn't match your actual preference.

**Cause:** Reflection was saved to `.local.md` file.

**Fix:**
1. Open the preference file (global or project, depending on where it was saved)
2. Find the section that was added (usually at the bottom)
3. Delete or modify the unwanted lines
4. Save the file

**Prevention:** Read reflection summaries carefully before confirming. You can always say "no, don't save that."

---

## Quick Reference

| Issue | First Thing to Try |
|-------|-------------------|
| Wrong genre | Move genre to first sentence |
| Flat dynamics | Add temporal words ("opens with", "builds to") |
| Vocal mismatch | Describe vocals in first 20 words |
| Tags ignored | Reduce to 3-4 inflection points |
| Prefs not loading | Check file path exactly |
| No reflection | Need 2+ songs per session |
