---
name: chrome
version: 5.5.0
description: Interactive Suno composition with Chrome browser integration
argument-hint: [theme]
allowed-tools: Read, Glob, AskUserQuestion, Write, Skill, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__find, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__get_page_text
---

# Suno Chrome Integration Workflow

Interactive browser session for composing songs AND filling Suno forms in real-time.

**Requirement:** This command requires Chrome integration (`claude --chrome`).

## Step 1: Verify & Navigate

1. Call `mcp__claude-in-chrome__tabs_context_mcp` with `createIfEmpty: true` to verify Chrome integration
   - If fails: inform user to restart with `claude --chrome` and exit
2. Navigate to `https://suno.com/create` via `mcp__claude-in-chrome__navigate`
3. Screenshot to verify page loaded
   - If login required: pause for user to log in manually

## Step 2: Load Context

1. Invoke `song-composition` skill via Skill tool
2. Check for preferences at `.claude/suno-composer.local.md`
3. Gather composition parameters using the same flow as `/suno` (mood, count, language, vocals)

## Step 3: Compose & Fill

For each song:

1. **Compose** using the skill's knowledge (title, style prompt, lyrics, specifications)
2. **Fill form** — find and fill "Style of Music" and "Lyrics" fields via `mcp__claude-in-chrome__find` + `mcp__claude-in-chrome__form_input`
3. **Screenshot** the filled form for user review
4. **User decides** via AskUserQuestion:
   - Generate — click Create button
   - Modify — adjust style/lyrics, re-fill, re-screenshot
   - Skip — move to next song
   - Done — end session

Repeat for remaining songs, then present session summary and offer to save compositions to files.

## Error Recovery

| Issue | Action |
|-------|--------|
| Page won't load | Screenshot, diagnose, offer fallback to standard `/suno` |
| Form fields not found | Read page structure, try alternatives, offer manual copy |
| Login required | Pause for user, offer to compose in the meantime |
