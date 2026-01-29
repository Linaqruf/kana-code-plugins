---
description: Interactive Suno composition with Chrome browser integration
argument-hint: [theme]
allowed-tools: Read, Glob, AskUserQuestion, Write, Skill, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__find, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__get_page_text
---

# Suno Chrome Integration Workflow

Interactive browser session for composing songs AND filling Suno forms in real-time.

**Requirement:** This command requires Claude Code to be running with Chrome integration (`claude --chrome`).

## Step 1: Verify Chrome Integration

First, call `mcp__claude-in-chrome__tabs_context_mcp` with `createIfEmpty: true` to:
- Verify Chrome integration is available
- Get or create a browser tab for the session

If this fails, inform the user they need to run Claude Code with Chrome integration:
```
This command requires Chrome integration. Please restart Claude Code with:
  claude --chrome
```

## Step 2: Navigate to Suno

Use `mcp__claude-in-chrome__navigate` to go to `https://suno.com/create`.

Take a screenshot with `mcp__claude-in-chrome__computer` (action: screenshot) to verify the page loaded.

**If login required:** Inform the user they need to log in manually, then wait for confirmation before continuing.

## Step 3: Load Skill Knowledge

Use the Skill tool to invoke the `song-composition` skill for comprehensive Suno v5 knowledge.

Also check for user preferences at `.claude/suno-composer.local.md`.

## Step 4: Gather Composition Parameters

Use AskUserQuestion to gather parameters (same as standard `/suno` command):

**If no theme provided in arguments:**
Ask about mood/theme with preset options.

**Always ask:**
1. How many songs to generate (1-5 for interactive mode)
2. Language preference
3. Vocal preference

## Step 5: Compose First Song

Using the skill's knowledge, compose the first song:
- Create title, style prompt, lyrics with metatags, and specifications
- Follow the standard composition process from the skill

## Step 6: Fill Suno Form

After composing, fill the Suno creation form:

1. **Find the Style/Music field:**
   Use `mcp__claude-in-chrome__find` to locate the "Style of Music" or similar input field.

2. **Fill Style Prompt:**
   Use `mcp__claude-in-chrome__form_input` to enter the generated style prompt.

3. **Find the Lyrics field:**
   Use `mcp__claude-in-chrome__find` to locate the "Lyrics" textarea.

4. **Fill Lyrics:**
   Use `mcp__claude-in-chrome__form_input` to enter the complete lyrics with metatags.

5. **Take Screenshot:**
   Use `mcp__claude-in-chrome__computer` (action: screenshot) to show the user the filled form.

## Step 7: User Review

Present the filled form to the user with AskUserQuestion:

**Options:**
- Generate - Click Create to generate this song on Suno
- Modify Style - Let me adjust the style prompt
- Modify Lyrics - Let me adjust the lyrics
- Skip - Move to next song without generating
- Done - End session

**If Modify Style or Modify Lyrics:**
- Ask what changes they want
- Update the composition
- Re-fill the form
- Return to Step 7

**If Generate:**
- Use `mcp__claude-in-chrome__find` to locate the Create/Generate button
- Use `mcp__claude-in-chrome__computer` (action: left_click) to click it
- Wait for generation to start
- Take a screenshot to confirm

## Step 8: Continue or Complete

If more songs to compose (from Step 4 count):
- Clear the form fields if needed
- Return to Step 5 for next song

If all songs done or user chose "Done":
- Present session summary
- Offer to save compositions to files (same as standard `/suno` Step 5)

## Interactive Iteration Tips

Throughout the session, the user can request:

**Style adjustments:**
- "Make it more upbeat"
- "Add more electronic elements"
- "Change to male vocals"

**Lyric adjustments:**
- "Rewrite the chorus"
- "Make the bridge more emotional"
- "Add English to the chorus"

**Form interactions:**
- "Show me what's in the form"
- "Clear and start over"
- "Let me see the current state"

For any adjustment request:
1. Make the requested changes
2. Update the form using `mcp__claude-in-chrome__form_input`
3. Take a screenshot to show the update
4. Return to user review

## Error Handling

**If Suno page doesn't load:**
- Take screenshot to diagnose
- Inform user of the issue
- Offer to retry or compose without browser (fallback to standard `/suno`)

**If form fields not found:**
- Use `mcp__claude-in-chrome__read_page` to analyze page structure
- Try alternative selectors
- If still failing, show the compositions and ask user to copy manually

**If user needs to log in:**
- Pause and wait for user confirmation
- Offer to compose songs in the meantime for later filling

## Session Output

At the end of the session, provide:
- Summary of all composed songs
- Which were generated on Suno
- Option to save all compositions to files

## Notes

- This is a real-time interactive workflow, not just auto-fill
- User maintains control over when to generate
- Compositions can be refined iteratively before generating
- Browser state persists throughout the session
