# Exemplar: Gothic Doujin Song (Quality Bar)

A complete song in the Full Song Format (`output-formats.md`), annotated against
the Composition Rubric (SKILL.md). Brief: "japanese underground/doujin music, in
the spirit of Ariabl'eyeS" — dual female vocals, gothic symphonic metal.
This exemplar PASSES every rubric item; the counter-example at the bottom shows
what the rubric prevents.

---

## Song: 紅月ノ檻 (Kougetsu no Ori — "Cage of the Crimson Moon")

### Style Prompt — Modular (try first)
gothic symphonic metal, doujin style, dramatic and tragic, dual female vocals in
dialogue building to soaring harmonies, harpsichord pipe organ strings and
double-kick drums, polished cathedral-reverb production at 172 bpm

### Style Prompt — Narrative (fallback if the arrangement feels flat)
Gothic symphonic metal in the Japanese doujin style at 172 bpm. A fragile music box
and cathedral choir open before the full band crashes in — double-kick drums,
tremolo-picked guitars, harpsichord runs and pipe organ under sweeping strings. Two
female vocalists in dialogue: a clear soaring soprano lead answered by a darker
second voice, merging into layered harmonies for each chorus. A stripped
harpsichord-and-voice bridge whispers before a snare-roll build and a final
key-change chorus with a descant counter-melody, resolving into a music-box
reprise under a single fading voice. Dramatic, tragic, ornate —
minor-key Baroque flourishes, polished symphonic production with cathedral reverb.

### Exclude (Styles field, Advanced Options)
no harsh vocals — clean operatic delivery instead

### Lyrics

[Intro: music box and choir, then full band]

[Verse 1]
月光が 窓を裂く
銀の棘 胸に深く
祈りさえ 届かぬ部屋で
貴方の声だけ 響く

[Verse 2]
永き夜を 彷徨う影
渇きだけを 連れて
触れた指の 温もりに
壊れてゆく 永遠の掟

[Pre-Chorus]
「逃げて」と囁く唇が
「行かないで」と泣いている
矛盾の中で 月が満ちる

[Chorus]
紅き月よ 永遠を抱いて
堕ちてゆく 二人だけの夜
薔薇のように 紅く咲いて
朝は来ない それでもいい

[Interlude]

[Verse 3]
銀貨より 重い口づけ
罪ならば 共に背負おう
鐘の音が 二人を裂いても
この手はもう 離さない

[Chorus]

[Bridge: stripped, harpsichord and voice]
「永遠は呪い?」
「それとも祈り?」
答えはただ 唇の上に

[Build]

[Final Chorus: key change up]
紅き月よ 永遠を抱いて
堕ちてゆく 二人だけの夜
薔薇のように 紅く咲いて
朝は来ない それでもいい
紅き月の檻の中 永遠に—

[Outro]

### Specifications
- **Tempo:** 172 BPM, double-kick drive; bridge in half-feel
- **Vocal:** dual female — soprano lead + darker second voice; no Suno Voice attached
- **Key Instruments:** harpsichord, pipe organ, strings, tremolo guitar, double-kick drums
- **Production Style:** polished symphonic, cathedral reverb, Baroque minor-key flourishes
- **Inflection Points:** intro texture (sets the fragile→slam dynamic), bridge
  stripped (contrast before climax), build (tension), final chorus key change
  (earned peak) — 4 tags, all technique cues
- **Outro:** music box reprise under a single fading voice — carried by the
  narrative style prompt; `[Outro]` stays bare in the lyrics (a bare tagged
  section typically plays as instrumental — `[Instrumental Break]` forces it)
  to hold the 4-tag budget

### Readings & Casting (craft block — NOT for pasting)
- **Voice map:** Verse 1 = Voice A (the girl, clear soprano); Verse 2 = Voice B
  (the vampire, darker); Pre-Chorus = A/B alternating lines, third line both;
  Chorus = unison → harmony; Verse 3 = A/B/A/both; Bridge = whispered dialogue
  (A then B, third line both); Final Chorus = B descant over A lead.
  (Casting kept OUT of the pasted lyrics to hold the 3-4 tag budget; the style
  prompt's "dual female vocals in dialogue" carries it. The optional ride-along —
  `[Verse 2: second vocalist, darker timbre]` — is available when a user wants
  Suno to attempt explicit assignment.)
- **Reading declarations:** 永遠 → とわ (2 morae) throughout; 紅き → あかき;
  永き → ながき; 月光 → げっこう (4 morae); 銀貨 → ぎんか; 誓約 — not used in
  final lyric; title 紅月 → こうげつ.
- **Mora notes (hooks + flagged lines):** Chorus: あかきつきよ・とわをだいて 6+6 (12);
  おちてゆく・ふたりだけのよる 5+8 (13); ばらのように・あかくさいて 6+6 (12);
  あさはこない・それでもいい 6+6 (12). Final-chorus climax tail (standalone, so
  full-line rule): あかきつきのおりのなか・とわに 11+3 (14). Verse lines 9-13.
- **Script pasted:** Japanese kana/kanji.

---

## Rubric annotations (why this passes)

1. **[S] Voice casting** — the lyric is *written for* the duo: V1/V2 are the two
   characters answering each other; the pre-chorus interleaves quoted speech
   begging in opposite directions (「逃げて」 vs 「行かないで」); the bridge is a
   whispered dialogue; the finale adds a descant. Voice map recorded above.
2. **[M] Prosody** — hook full lines 12-13, parallel-couplet hemistichs 3-8, climax
   tail 14 (standalone → full-line rule), verses 9-13. Held notes land open:
   それでもいい (long い), 永遠に— (open vowel).
3. **[S] Register** — four devices for a gothic subject: archaic negative 届か**ぬ**,
   classical adjectival 永**き**/紅**き**, declared double-reading 永遠→とわ, title
   katakana ノ.
4. **[S] Imagery system** — moon / rose / cage / silver / bell, developed across
   sections in fresh combinations: 銀貨より重い口づけ (a kiss heavier than silver
   coins — Judas pricing), 月光が窓を裂く (moonlight tears the window open).
   Stock-word check (doujin register, strict): 永遠 appears ≤2× per section and
   always under interrogation or modification (永遠の掟, 永遠は呪い?), never as
   default sentiment.
5. **[S] Thesis presence** — 朝は来ない それでもいい ("morning will never come —
   and that's fine"): the whole tragedy stated concretely in 12 morae, closing the
   chorus.
6. **[M] Hook anchor** — 紅き月 opens the chorus; the title phrase 紅き月の檻
   closes the final chorus.
7. **[M] Tags** — exactly 4 inflection tags, all technique cues, every other
   section bare.
8. **[M] Style prompt** — both forms present; one Exclude entry with replacement;
   Lyrics block paste-clean (compare: this file's Readings & Casting block holds
   everything that is NOT sung).

---

## Counter-example: what the rubric prevents

A chorus written by faithfully assembling stock vocabulary (from the calibration
demo's strict-adherence track, same gothic brief):

```
[Chorus]
永遠の夜に          ← stock 永遠, unmodified
二人の夢を誓う       ← stock 夢 + 約束-class sentiment
切ない想いが         ← stock 想い, the most median line in J-pop
月に届くまで         ← generic aspiration; no thesis anywhere
```

Grammatical, singable, on-tempo — and completely interchangeable: no voice
casting, zero register devices for a gothic subject, no image system, no thesis
line, hook anchor absent. Fails rubric items 1, 3, 4, 5, and 6 while satisfying
every *mechanical* count — which is exactly why the structural items exist.
