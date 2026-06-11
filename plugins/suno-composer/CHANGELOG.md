# Changelog

## 6.0.0 (2026-06-12)

Craft-layer and currency overhaul. (For pre-6.0.0 history, see git history —
this changelog starts fresh at 6.0.0.)

- **Suno v5.5 currency**: retargeted from "Suno v5" to current models (v5/v5.5);
  negatives routed to the Exclude (Styles) field; parameterized section tags
  (`[Verse: whispered, acoustic only]`) as the arrangement-precision tool;
  Voice/Persona awareness (vocal descriptors omitted when a Voice is attached);
  field budgets documented as verify-in-app.
- **Dual-form style prompts**: modular descriptor list ("try first", per 2026
  guidance) + narrative prose ("fallback", v5-tested) in every song output;
  `style-prompt form` preference key to pin one.
- **Craft layer**: new `japanese-prosody.md` (mora-based counting — the old file
  counted syllables; register devices; assonance; stock-word anti-default list)
  replacing `japanese-lyric-patterns.md`; an 8-item tiered Composition Rubric in
  SKILL.md; paste-clean Lyrics contract with a new Readings & Casting craft block
  in the output format; annotated quality-bar exemplar
  (`references/examples/gothic-doujin-song.md`).
- **New `lyric-critic` agent**: enforces the rubric (craft only, never taste),
  counts against declared readings and shows its kana expansions, adds
  cross-track checks in album mode; default-on with "quick" skip and a
  `lyric-critic` preference key.
- **Structural**: deleted `workflow-modes.md`, `user-preferences.md`,
  `walkthroughs.md` (duplication/training wheels; unique bits folded into the
  command); trimmed Western/EDM catalogs from `genre-deep-dive.md` and filler
  from `pro-techniques.md`; tier presets relabeled as ingredient lists;
  `Register:` lines added to all 29 artist profiles; vision-first mode now
  presents 2-3 concept directions via AskUserQuestion previews.
- Rebuilt README; plugin/marketplace descriptions re-synced.
