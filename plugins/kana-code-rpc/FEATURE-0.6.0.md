# kana-code-rpc v0.6.0 Feature Spec

> **Status: Planned — not yet implemented.** (Originally targeted for v0.5.0, which was consumed by audit fixes.)

> Button links, richer activity states, and statusline enhancements.

## Overview

### Problem Statement
Discord presence currently shows flat tool activity with no clickable actions, no distinction between thinking vs active tool use, and the terminal statusline lacks session cost, elapsed time, and tool indicators.

### Solution
Three feature groups in a single v0.5.0 release:
1. **Button links** — Clickable "View on GitHub" button (auto-detected) with optional custom override
2. **Richer activity states** — Thinking detection (tool gap + statusline growth), compacting state (PreCompact hook), reading vs editing distinction
3. **Statusline enhancements** — Running cost tracker, current tool indicator, elapsed session time

### Success Criteria
- [ ] Discord presence shows "View on GitHub" button linking to correct repo
- [ ] Discord shows "Thinking..." when no tool fires but context is growing
- [ ] Discord shows "Compacting..." during context compaction
- [ ] Terminal statusline shows session cost, tool activity, and elapsed time

---

## Feature 1: Button Links

### Description
Add a clickable button to Discord Rich Presence that links to the project's GitHub repo or a user-configured URL.

### Technical Design

**Auto-detection**: Parse `git remote get-url origin` output to extract GitHub/GitLab URL.

```python
# In presence.py daemon loop, when building RPC update:
buttons = []
if github_url:
    buttons.append({"label": "View on GitHub", "url": github_url})
if custom_button_url:
    buttons.append({"label": custom_button_label, "url": custom_button_url})
# pypresence: rpc.update(..., buttons=buttons)
```

**Config additions** (`config.yaml`):
```yaml
display:
  # ... existing toggles ...
  show_button: true        # Show "View on GitHub" button
  custom_button_label: ""  # Custom button label (max 31 chars)
  custom_button_url: ""    # Custom button URL (overrides auto-detect)
```

**Data flow**:
- `cmd_start()` runs `git remote get-url origin` and writes `github_url` to state.json
- Daemon reads `github_url` from state and passes to `rpc.update(buttons=...)`
- If `custom_button_url` is set in config, it overrides `github_url`

**Constraints**:
- Discord allows max 2 buttons, each max 31 chars label and 512 chars URL
- Button URLs must be `https://` (Discord rejects `http://`)
- pypresence `buttons` parameter: `[{"label": str, "url": str}]`

### Acceptance Criteria
- [ ] Auto-detects GitHub URL from `git remote -v`
- [ ] Falls back gracefully if no git remote (no button shown)
- [ ] Custom URL from config overrides auto-detected URL
- [ ] Button label respects 31 char Discord limit
- [ ] Config toggle `show_button` disables button entirely

---

## Feature 2: Richer Activity States

### Description
Add three new activity states to Discord presence beyond tool-based activity.

### State Priority (highest to lowest)
1. **Compacting** — PreCompact hook fired, context compaction in progress
2. **Tool activity** — PreToolUse hook fired recently (existing behavior)
3. **Thinking** — No tool fired for >5s but statusline context % still growing
4. **Idling** — No activity for > idle_timeout (existing behavior)

### 2a. Thinking State

**Detection logic** (in daemon loop):
```python
now = time.time()
last_tool_time = state.get("last_update", 0)
tool_gap = now - last_tool_time
context_growing = state.get("context_pct", 0) > prev_context_pct

if tool_gap > 5 and context_growing:
    activity = "Thinking..."
```

**How it works**:
- Statusline updates context_pct every ~300ms
- Daemon tracks previous context_pct each loop iteration
- If 5+ seconds since last tool AND context_pct increased → "Thinking..."
- Once a tool fires again, immediately switches back to tool activity

### 2b. Compacting State

**Implementation**: Add a `PreCompact` hook to `hooks.json`:
```json
"PreCompact": [{
  "type": "command",
  "command": "python \"${CLAUDE_PLUGIN_ROOT}/scripts/presence.py\" compact",
  "timeout": 5000,
  "alwaysApprove": true
}]
```

**New `cmd_compact()` function** in presence.py:
```python
def cmd_compact():
    update_state({"tool": "__compact__", "last_update": int(time.time())})
```

**Daemon recognizes** `tool == "__compact__"` → activity = "Compacting context..."

**Duration**: Compacting state persists until next tool fires or statusline updates tool state.

### 2c. Reading vs Editing Distinction

Already partially implemented — the tool mapping distinguishes:
- `Read` / `NotebookRead` → "Reading"
- `Edit` / `NotebookEdit` → "Editing"
- `Write` → "Writing"

**Enhancement**: When multiple consecutive Read tools fire without Edit/Write, show "Reviewing code..." instead of "Reading {file}". Threshold: 3+ consecutive reads.

**Implementation**:
```python
# In state.json, add:
"consecutive_reads": 0  # Reset on non-Read tool

# In cmd_update():
if tool_name in ("Read", "NotebookRead"):
    state["consecutive_reads"] = state.get("consecutive_reads", 0) + 1
else:
    state["consecutive_reads"] = 0

# In daemon:
if tool == "Read" and state.get("consecutive_reads", 0) >= 3:
    activity = "Reviewing"
```

### Acceptance Criteria
- [ ] "Thinking..." shown when no tool fires for >5s but context growing
- [ ] Returns to tool activity immediately when tool fires
- [ ] "Compacting context..." shown during PreCompact hook
- [ ] "Reviewing" shown after 3+ consecutive Read tools
- [ ] States don't flicker (debounce transitions)

---

## Feature 3: Statusline Enhancements

### Description
Enhance the terminal statusline with session cost, tool activity indicator, and elapsed time.

### 3a. Session Cost Tracker

Add running cost total to statusline breadcrumb:

```
Opus 4.6  ›  ████░░░░░░ 42%  ›  29.4k tokens  ›  $0.18  ›  3m 12s  ›  main
                                                     ↑         ↑
                                                  cost      elapsed
```

**Already implemented**: Cost is shown in the statusline. This is confirmed done.

### 3b. Tool Activity Indicator

Show current tool name or a spinner character in the statusline:

```
Opus 4.6  ›  ████░░░░░░ 42%  ›  ⚡ Editing  ›  29.4k tokens  ›  $0.18  ›  main
                                  ↑
                              tool indicator
```

**Implementation** in `statusline.py`:
```python
# Read current tool from state.json
state = read_state_unlocked() if has_lock else None
current_tool = state.get("tool", "") if state else ""
tool_display = TOOL_DISPLAY_MAP.get(current_tool, current_tool)

# Add to breadcrumb
if tool_display:
    parts.append(f"{C.YELLOW}⚡ {tool_display}{C.RESET}")
```

**TOOL_DISPLAY_MAP**: Reuse the same mapping from presence.py (Edit→"Editing", Bash→"Running", etc.)

### 3c. Elapsed Time

Show session duration in the statusline:

```
Opus 4.6  ›  ████░░░░░░ 42%  ›  29.4k tokens  ›  $0.18  ›  3m 12s  ›  main
                                                             ↑
                                                         elapsed time
```

**Implementation**: Use `duration_ms` from the statusline API (already extracted):
```python
duration_sec = duration_ms // 1000
if duration_sec >= 3600:
    elapsed = f"{duration_sec // 3600}h {(duration_sec % 3600) // 60}m"
elif duration_sec >= 60:
    elapsed = f"{duration_sec // 60}m {duration_sec % 60}s"
else:
    elapsed = f"{duration_sec}s"
parts.append(f"{C.DIM}{elapsed}{C.RESET}")
```

### Config Additions

```yaml
display:
  # ... existing toggles ...
  show_elapsed: true       # Show elapsed time in statusline
  show_tool_indicator: true  # Show current tool in statusline
```

### Acceptance Criteria
- [ ] Cost displayed in statusline (already done — verify)
- [ ] Current tool shown with ⚡ indicator
- [ ] Elapsed time formatted as Xs / Xm Xs / Xh Xm
- [ ] Both new elements togglable via config
- [ ] Statusline doesn't exceed terminal width (truncation strategy)

---

## Implementation Plan

### Phase 1: Activity States
- [ ] Add `cmd_compact()` and PreCompact hook to hooks.json
- [ ] Add thinking detection to daemon loop (tool gap + context growth)
- [ ] Add consecutive_reads tracking for "Reviewing" state
- [ ] Add state transition debouncing (min 2s between changes)

### Phase 2: Button Links
- [ ] Add `github_url` extraction in `cmd_start()` (parse git remote)
- [ ] Add buttons to `rpc.update()` in daemon loop
- [ ] Add config toggles: `show_button`, `custom_button_label`, `custom_button_url`
- [ ] Validate URL format (https:// only) and label length (≤31 chars)

### Phase 3: Statusline Enhancements
- [ ] Add tool indicator to statusline breadcrumb
- [ ] Add elapsed time to statusline breadcrumb
- [ ] Add config toggles: `show_elapsed`, `show_tool_indicator`
- [ ] Handle terminal width overflow (drop rightmost elements first)

### Phase 4: Polish & Version
- [ ] Update config.yaml with new defaults
- [ ] Update README.md with new features
- [ ] Bump version to 0.5.0 across plugin.json, marketplace.json, root README, SPEC.md, CLAUDE.md
- [ ] Update CLAUDE.md (plugin) with new architecture notes

---

## Files to Modify

| File | Changes |
|------|---------|
| `scripts/presence.py` | Add cmd_compact(), thinking detection, consecutive_reads, buttons, debouncing |
| `scripts/statusline.py` | Add tool indicator, elapsed time display |
| `scripts/state.py` | No changes expected |
| `hooks/hooks.json` | Add PreCompact hook |
| `.claude-plugin/config.yaml` | Add show_button, custom_button_*, show_elapsed, show_tool_indicator |
| `.claude-plugin/plugin.json` | Version bump to 0.5.0 |
| `README.md` | Document new features |

---

## Open Questions

| # | Question | Options | Status |
|---|----------|---------|--------|
| 1 | Should "Thinking..." have a spinner animation? | A) Static text, B) Rotating ⠋⠙⠹⠸ chars | Open |
| 2 | Terminal width detection — use shutil.get_terminal_size? | A) Yes, B) Fixed 120 char assumption | Open |
| 3 | Should buttons show on idle state too? | A) Always show, B) Only during activity | Open |

---

*Generated with project-spec plugin for Claude Code*
