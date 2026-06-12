# suno-composer

Compose songs for [Suno AI](https://suno.com) with a craft-reviewed workflow:
dual-form style prompts, mora-accurate Japanese lyrics, duet voice casting, and a
`lyric-critic` agent that enforces a checkable composition rubric before anything
reaches you.

Targets current Suno models (**v5/v5.5**). Where v5.5 behavior is unverified, the
plugin says so and hedges instead of guessing.

## Install

```
/plugin marketplace add Linaqruf/kana-code-plugins
/plugin install suno-composer@kana-code-plugins
```

## Quick start

```
/suno gothic doujin waltz about a vampire covenant, like Ariabl'eyeS
/suno 5-track EP about night drives, city pop, japanese
/suno acoustic version of [paste your song]
/suno                      ← guided wizard
```

Songs are written to `./songs/<timestamp>-<slug>/` as copy-paste-ready files:
one style prompt of each form, optional Exclude-field entries, paste-clean lyrics,
and a Readings & Casting craft block (never pasted) holding voice maps, declared
kana readings, and mora counts.

## What makes it different

- **Dual-form style prompts** — every song ships a modular descriptor list
  ("try first", per 2026 v5.5 guidance) AND a narrative arrangement prose
  ("fallback if the arrangement feels flat", first-party-tested on v5). Pin one
  with the `style-prompt form` preference once you know what works for you.
- **Composition rubric + lyric-critic agent** — eight checkable craft rules
  (voice casting for duets, mora-based Japanese prosody, register devices,
  imagery systems, thesis lines, hook anchors, tag budgets, prompt hygiene). The
  critic checks craft only — never taste — and shows its kana counts so you can
  audit every finding. Skip it any time by saying "quick", or set
  `lyric-critic: album-only | never`.
- **Japanese prosody done right** — lyrics are counted in morae (拍), not
  syllables; held notes land on open vowels; gothic/literary subjects get real
  register devices (届かぬ, 紅き, 永遠 sung とわ). See
  `skills/suno/references/japanese-prosody.md`.
- **Reference-based composition** — 29 artist profiles (tagged by tier, with
  lyric-register notes) and a five-tier J-pop ecosystem map (anisong / surface /
  mainstream / doujin / legacy, plus doujin subgenres). "like YOASOBI",
  "anisong like Aimer", "doujin symphonic" all work.
- **Four modes** — single/batch songs, albums with arc roles and cross-track
  review, variations (acoustic/remix/stripped/extended/cinematic), and
  continuations (sequel/prequel/response/POV/epilogue) with lyrical callbacks.
- **Adaptive preferences** — a 20-second first-run wizard, then session
  reflection that notices your patterns and offers to remember them.

## Suno-side features it tracks

Exclude (Styles) field routing for negatives, parameterized section tags
(`[Bridge: stripped, harpsichord and voice]`), and Voice/Persona awareness —
when you mention an attached Voice, style prompts omit vocal descriptors (they
conflict). Field budgets are listed as verify-in-app (sources conflict).

**Scope note:** this plugin covers the composition side — prompts and lyrics.
Suno's post-generation tools (Studio, stems, section replace, covers) are where
current workflows spend the other half of their time; that editing loop is out of
scope here by design.

## Layout

```
commands/suno.md                     /suno workflow (modes, critic step, previews)
agents/lyric-critic.md               craft reviewer (rubric enforcement)
skills/suno/SKILL.md                 composition knowledge + the rubric
skills/suno/references/              metatags, prosody, profiles, tiers, formats…
skills/suno/references/examples/     annotated quality-bar exemplar
examples/suno-composer.local.md      preference file template
```

## License

MIT
