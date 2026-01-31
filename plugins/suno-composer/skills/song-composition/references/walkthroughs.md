# Walkthroughs

Complete workflow examples showing the composition process from start to finish.

## Vision-First Workflow Example

This walkthrough demonstrates a complete vision-first composition session.

---

### The User Input

```
/suno like YOASOBI about growing apart from childhood friends - bittersweet summer vibes
```

---

### Step 0: Preference Loading

**What Claude checks:**
1. `~/.claude/suno-composer.local.md` (global) - Found
2. `.claude/suno-composer.local.md` (project) - Not found

**Loaded preferences:**
```markdown
## Favorite Genres
- J-pop / Anime
- Ballads / Acoustic

## Preferred Vocal Styles
- Female vocals

## Default Languages
- Japanese
```

> **Annotation:** Preferences suggest J-pop with female vocals. This aligns with the YOASOBI reference, so no conflict. The preference for "emotional depth" (if present) would reinforce the bittersweet theme.

---

### Step 1: Mode Detection

**Input analysis:**
- `like YOASOBI` → Artist reference detected
- `about growing apart from childhood friends` → Clear theme
- `bittersweet summer vibes` → Mood descriptor

**Richness score:** RICH (3+ descriptive elements)

**Decision:** Vision-First Mode

> **Annotation:** The input has artist reference, theme, and mood - this is rich creative direction. Guided mode would be unnecessary friction.

---

### Step 2: Reference Loading

**Artist profile loaded (YOASOBI):**
- Style: Story-driven J-pop with electronic foundation
- Vocal: ikura's bright, emotional female vocals
- Tempo: 130-160 BPM typically
- Themes: Novel adaptations, youth, night, fleeting moments

> **Annotation:** YOASOBI's characteristics inform the creative vision, but "bittersweet summer" suggests slower tempo than their typical upbeat tracks.

---

### Step 3: Creative Vision Proposal

Claude presents:

---

I'm imagining **"Natsu no Owari" (夏の終わり)** — a 2-track mini-EP about the quiet ache of watching friendships fade:

1. **"Semitransparent Days"** — A nostalgic opener where summer memories flicker like old photographs, vocals floating over piano and synth
2. **"The Distance Between Our Shadows"** — The confession track: standing at the same train platform, but heading different directions now

Sound: Story-driven J-pop with YOASOBI's narrative DNA but gentler - 95 BPM, piano-led with subtle electronic textures that swell in the choruses. Think sunset-colored rather than neon-lit.

Japanese lyrics, bright female vocals with that slight catch of emotion.

Shall I compose this? Or adjust the direction?

---

> **Annotation:** Key choices made:
> - **2 tracks** inferred from "growing apart" (one for memory, one for present)
> - **95 BPM** - slower than typical YOASOBI to match "bittersweet" mood
> - **Piano-led** - softer foundation than YOASOBI's typical electronic drive
> - **Japanese** - inferred from J-pop context + preferences
> - **Vivid imagery** - "sunset-colored", "semitransparent" - makes the vision tangible

---

### Step 4: User Iteration

**User says:** "perfect, but make it one song - the second concept"

**Claude adjusts:**

---

Got it - focusing on **"The Distance Between Our Shadows"** as a single track.

The train platform moment where you realize you're both standing here, but your futures point different directions. Summer cicadas in the background, that specific golden-hour light.

Same sound: 95 BPM piano-driven J-pop with YOASOBI storytelling DNA. Japanese lyrics, emotional female vocals.

Composing now.

---

> **Annotation:** User wanted one song, not two. Claude acknowledged the adjustment without asking unnecessary follow-up questions.

---

### Step 5: Song Composition

Claude generates the full song:

---

## Song: The Distance Between Our Shadows (影の距離)

### Style Prompt

```
This contemplative J-pop ballad at 95 bpm opens with delicate piano arpeggios and filtered synth pads creating a golden-hour atmosphere. Bright female vocals enter with narrative intimacy, carrying YOASOBI's storytelling clarity but softer edges. Electronic elements gradually layer in - subtle bass pulse, crystalline synth accents - as the arrangement builds from introspection through the pre-chorus. The chorus blooms with full production: warm pads, driving eighth-note piano, and vocals that soar with restrained power. A stripped bridge returns to voice and piano before the final chorus peaks with added string textures, then resolves into a sparse outro of fading piano notes.
```

### Lyrics

```
[Intro: Piano, filtered]
(instrumental - 8 bars)

[Verse 1]
夏の終わりのホームで
君と並んで立ってた
同じ空を見上げても
見てる景色は違うんだ

[Pre-Chorus]
あの頃は全部同じだった
夢も、恐れも、明日への道も

[Chorus]
でも今、影の距離が広がっていく
同じ場所にいても、もう届かない
君の背中を見送る夕暮れ
笑顔で手を振るから、振り向かないで

[Verse 2]
思い出だけが鮮やかで
今日の僕らはセピア色
「また会おうね」の約束は
嘘じゃないけど本当でもない

[Pre-Chorus]
大人になるって こういうことなんだ
分かってたはずなのに

[Breakdown][stripped, half-time]
ねえ、覚えてる？
あの夏の約束
永遠を信じてた
あの日の僕ら

[Build]

[Final Chorus][key change up]
それでも、影の距離を抱きしめる
離れていく君も、僕の一部だから
ホームに響く発車のメロディ
涙は見せないよ、君への最後の嘘

[Outro]
(piano fades)
```

### Specifications
- **Tempo:** 95 BPM
- **Vocal:** Female, bright with emotional restraint, YOASOBI-influenced clarity
- **Key Instruments:** Piano (lead), synth pads, subtle electronic bass, string accents
- **Production Style:** Clean, story-focused, golden-hour warmth
- **Inflection Points:**
  - `[Intro: Piano, filtered]` - establishes intimate opening
  - `[Breakdown][stripped, half-time]` - emotional contrast point
  - `[Build]` - tension before climax
  - `[Final Chorus][key change up]` - earned peak moment

---

> **Annotation: Style Prompt Analysis**
>
> Notice the **narrative structure**:
> - "opens with" → "enter" → "gradually layer" → "builds" → "blooms" → "returns" → "peaks" → "resolves"
>
> This temporal flow IS the arrangement instruction. Suno interprets this as:
> - Intro = piano + filtered synth
> - Build through verse/pre-chorus
> - Full production at chorus
> - Strip back at bridge
> - Peak at final chorus
> - Fade out
>
> **Sparse tagging:** Only 4 technique tags in the entire song, at the inflection points.
>
> **Vocal anchor:** "Bright female vocals enter with narrative intimacy" appears early in the style prompt to lock the voice character.

---

### Step 6: File Output

```
Created: ./songs/20260131-shadow-distance/
├── the-distance-between-our-shadows.md
└── _index.md
```

---

### Step 7: Copy-Paste to Suno

| Suno Field | What to Paste |
|------------|---------------|
| **Style of Music** | The entire Style Prompt block |
| **Lyrics** | The entire Lyrics block (including all `[tags]`) |
| **Title** | "The Distance Between Our Shadows" or "影の距離" |

> **Annotation:** The style prompt and lyrics are designed to be copy-paste ready. No editing needed.

---

### Step 8: Session Reflection (If Multi-Song)

Since this was a single-song session, reflection is skipped.

For multi-song sessions (2+), Claude would reflect:

---

I noticed something - you adjusted from my 2-track pitch to a single, more focused song. You seem to prefer depth over breadth. Want me to remember to lean toward single tracks unless you specifically ask for multiple?

---

> **Annotation:** Reflection is conversational, not a checkbox. It observes patterns and offers to save them - user confirms before anything is written.

---

## Key Takeaways

### Why This Worked

1. **Narrative style prompt** described the arrangement journey, not just tagged elements
2. **Sparse tagging** (4 inflection points) let Suno interpret dynamics naturally
3. **YOASOBI reference** was blended, not copied - kept storytelling DNA but adjusted tempo/mood
4. **Preferences filled gaps** - Japanese language wasn't explicitly requested but matched user's stored preference
5. **Vision-first mode** made one pitch, user adjusted naturally, no back-and-forth wizard

### Common Adjustments

| If user said... | Claude would... |
|-----------------|-----------------|
| "darker" | Shift imagery to twilight/night, lower key instruments, add minor progressions to style prompt |
| "faster/more energetic" | Increase BPM, add driving elements, adjust from "contemplative" to "urgent" |
| "English lyrics" | Recompose in English, acknowledge language change |
| "make it a duet" | Add second vocal character, adjust style prompt and lyrics for interplay |

---

## What NOT to Do

### Tag-List Style Prompt (Avoid)

```
J-pop, ballad, piano, synths, female vocals, emotional, YOASOBI style,
95 bpm, summer vibes, bittersweet, nostalgic, train station, friendship
```

**Problems:**
- No temporal structure - Suno doesn't know what happens when
- Genre buried under descriptors
- "YOASOBI style" is vague - what aspect?
- "summer vibes, bittersweet, nostalgic" are feelings, not arrangement instructions

### Over-Tagged Lyrics (Avoid)

```
[Verse 1][soft, intimate, piano only]
[Pre-Chorus][building, adding bass]
[Chorus][powerful, full band, emotional peak]
[Verse 2][slightly brighter, adding synths]
```

**Problems:**
- Tags every section - creates noise, not dynamics
- Describes what the section should feel like, not technique
- Structure already implies contrast - don't over-explain
