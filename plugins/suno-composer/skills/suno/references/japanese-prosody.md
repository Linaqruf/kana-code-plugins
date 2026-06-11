# Japanese Prosody for Songwriting

Craft rules for singable, register-true Japanese lyrics. This file replaces
vocabulary lists with checkable rules: the Composition Rubric in SKILL.md cites
them, and the `lyric-critic` agent counts against the **declared readings** in each
song's Readings & Casting block (see `output-formats.md`).

## Morae, Not Syllables

Japanese lyric meter counts **morae** (拍, *haku*) — not syllables. Each mora
occupies one beat-slot in the melody; miscounting produces the rushed or stretched
delivery that sounds "off" in generated vocals.

Counting rules:

| Unit | Morae | Example |
|------|-------|---------|
| Ordinary kana | 1 each | さくら = 3 |
| Small っ (sokuon) | 1 | きって = 3 |
| ん (hatsuon) | 1 | しんじる = 4 |
| Long vowel (う/あ/ー extension) | +1 | とう = 2, スター = 3 |
| 拗音 (small ゃゅょ: きゃ, じゅ…) | 1 with its carrier | じゅ = 1 |

Worked examples — note how mora and syllable counts diverge:

| Word | Kana | Morae | Syllables |
|------|------|-------|-----------|
| 月光 | げっこう | **4** (げ・っ・こ・う) | 2 |
| 切ない | せつない | 4 | 3 |
| 永遠 | えいえん | 4 — but sung とわ = **2** (see Double Readings) | 2 |
| 東京 | とうきょう | **4** (と・う・きょ・う) | 2 |

**Always count from kana, never from kanji or romaji.** When a line's reading is
ambiguous or non-standard, declare it in the Readings & Casting block — neither the
singer nor the critic can guess.

## Line Targets by Section

**Hemistich** = a breath-group within a line; lines have one or two, separated by a
caesura (write it as a space in the lyric).

| Section class | Rule |
|---------------|------|
| Hook (chorus) | Full lines 10-14 morae. Parallel-couplet lines: hemistichs 3-8. |
| Verse, pre-chorus | Full lines 9-14 morae |
| Bridge / whisper / spoken | Exempt — short fragments are the point |

Scoping note: the hemistich bound applies **only to parallel-couplet lines**
(matched pairs like 紅き月よ 永遠を抱いて ↔ 薔薇のように 紅く咲いて, both 6+6).
A standalone closing or extension line — a final-chorus climax tail — is checked by
the full-line range alone.

Traditional anchors: 7-5 (七五調) and 5-7 groupings feel classical and "sung";
modern pop floats freely in verses but tends to resolve into clean parallel
groupings at the hook. Use the tradition as gravity, not law.

## Held Notes and Melisma

Sustained notes need open or long vowels:

- **Good sustains:** /a/ and /o/ vowels, and long vowels — それでもいい (held い),
  永遠に— (held に → open vowel), こころ (ends on o).
- **Choked sustains:** lines ending in る/く/つ consonant-tight morae fight the
  singer. Fine for clipped, tense verse endings (窓を裂く — deliberately sharp);
  wrong for the chorus peak.
- Place the section's longest note on the emotional keyword, and make sure that
  word ends open: 朝は来ない それでもいい puts the sustain on the surrender, not a
  particle.
- Melisma runs (one vowel over many notes): write the lyric normally and note the
  run in Readings & Casting; only use explicit hyphenated stretching
  (あ-あ-あ) in the pasted lyrics when you intend Suno to vocalize it literally.

## Register Devices

When the subject is literary, gothic, historical, or high-fantasy, the lyric's
grammar must match — modern conversational Japanese under a cathedral-organ
arrangement is a register clash. Rubric item 3 requires **≥2 devices** for such
subjects:

| Device | Example | Note |
|--------|---------|------|
| Archaic negative 〜ぬ | 届か**ぬ**部屋 | replaces 〜ない |
| Classical adjectival 〜き | 永**き**夜, 紅**き**月 | replaces 〜い |
| Double reading (義訓) | write 永遠 sing **とわ**; 運命→**さだめ**; 宇宙→**そら** | MUST be declared in Readings & Casting |
| Literary verb forms | 〜ゆ, 〜せし, 〜けり | use sparingly — one per song is seasoning |
| Orthographic styling | katakana ノ in titles (紅月ノ檻) | visual register, costs nothing sung |

Double readings are the signature move of doujin/gothic lyrics — the eye reads the
formal kanji, the ear hears the intimate reading. They are also exactly why the
critic counts against declared readings: 永遠 is 4 morae as written, 2 as sung.

For **English** subjects in the same registers, the equivalent device list lives in
SKILL.md's rubric: archaic pronouns (thee/thy), latinate diction, syntactic
inversion.

## Rhyme: Assonance Over End-Rhyme

Japanese end-rhyme is weak — nearly every word ends in one of five vowels, so
rhyming line-ends is cheap and reads as accidental. The working devices:

- **Vowel-line matching:** hold one vowel color through a phrase — the a-i line
  (愛/会い/開い), the o-u line (空→とおく). Strongest when the matched vowels carry
  the held notes.
- **Rhythmic repetition:** どこまでも、どこまでも / ずっと、ずっと — repetition as
  percussion, common at pre-chorus tails.
- **Deliberate dense rhyme (韻):** hip-hop-adjacent acts (Creepy Nuts) rhyme hard
  and on purpose. Genre-conditional — do not import it into ballads.

## Stock Words — the Anti-Default List

These words are the statistical median of J-pop. They are not banned; they are
**defaults**, and a song built from defaults is wallpaper (demonstrated: the
calibration demo's Track B). Treat presence as a signal to check whether an image
is doing any work.

Stock list: 涙 夢 光 想い 心 未来 奇跡 翼 明日 永遠 桜 風 空 約束 瞬間
Pronouns — exempt, they are function words: 君 あなた 僕 私 俺

**Rule (register-conditional — rubric item 4):**
- doujin / literary / gothic register: **≤2 stock-word instances per section** is
  the bar; more is a finding.
- mainstream / idol / anisong register: advisory only — these words ARE the idiom
  there, and policing them is taste, not craft.
- A fresh modification resets the clock: 涙 alone is stock; 銀貨より重い口づけ-class
  modification (concrete, surprising, subject-derived) is imagery.

The constructive half of the rule: build **one concrete image system per song** out
of the subject's own lexicon (a gothic song: moon/rose/cage/silver/bell; a city-pop
song: neon/taillights/vending machine/last train) and let recurring images develop
across sections instead of swapping in new stock each line.

## Mixed Language

- Switch at **phrase boundaries**, not mid-clause: a Japanese verse into an English
  chorus hook is natural; mid-phrase splices need the loan-word pattern.
- Loan-word insertion (mainstream register): この feeling 止まらない — the English
  word takes Japanese phrase rhythm.
- Call-and-response echo: 忘れない → *Never forget* — translation as harmony line.
- English hooks suit mainstream/idol/anisong registers. They are NOT a default for
  doujin/literary registers — an English chorus in a gothic waltz breaks register
  unless the concept demands it (declare the intent in the Decision notes if so).

## Line Breaks and Breath

Line breaks are breath marks. Break at natural phrase boundaries — after particles,
after て-form verbs, between hemistichs:

```
GOOD: 君のことを いつも / 思い出してる     (particle boundary, then verb phrase)
BAD:  君のことを / いつも思い出してる      (orphans the を phrase mid-thought)
```

If reading a line aloud forces a breath where no break is written, restructure the
line — Suno inherits the same problem.

## Romanization

Suno sings Japanese from kana/kanji directly — paste the Japanese. Romaji is the
fallback when pronunciation drifts on a specific word; if you paste romaji, use
Hepburn (し=shi, ち=chi, つ=tsu, じ=ji), double long vowels (とうきょう=toukyou),
and particle readings は=wa, を=wo, へ=e. Record which script was pasted in
Readings & Casting so regeneration attempts stay consistent.
