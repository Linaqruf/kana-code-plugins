---
name: setup
description: Generate portable markdown stack configuration for your project
argument-hint: "[framework]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
version: 1.0.2
---

# Markdown Stack Setup Generator

Generate configuration files to add a portable markdown processing stack to your project. This stack is framework-agnostic and can be adapted to your project's conventions.

## Instructions

### Step 1: Detect or Ask Framework

Check for framework indicators in the current directory:

1. **Astro**: Look for `astro.config.mjs` or `astro.config.ts`
2. **Next.js**: Look for `next.config.js` or `next.config.mjs`
3. **Vite**: Look for `vite.config.js` or `vite.config.ts`
4. **SvelteKit**: Look for `svelte.config.js`

If no framework detected or argument provided, ask the user:

```
Which framework are you using?
- Astro (Recommended for blogs)
- Next.js (with MDX)
- Vite/Generic (standalone unified)
- SvelteKit (with mdsvex)
```

**Framework-Specific Notes:**
- **Next.js**: MDX is NOT compatible with Turbopack. Use `next dev` (webpack mode), not `next dev --turbopack`
- **SvelteKit**: Uses mdsvex which has slightly different directive syntax
- **Docusaurus**: Has built-in admonitions with different syntax (:::note vs > [!NOTE])

### Step 2: Implementation Scope

Ask the user how comprehensive they want the setup:

```
How much do you want to install?
- Full Stack (Recommended) - Everything: admonitions, math, code blocks, GitHub cards, reading time, excerpts, auto-linking
- Selective - Choose individual features
```

**If "Full Stack" selected:**
- Skip Steps 3-4 (feature selection)
- Auto-select ALL features
- Generate complete config with everything enabled
- Continue to Step 5

**If "Selective" selected:**
- Continue to Step 3 for feature selection

### Step 3: Select Core Features (Selective mode only)

Ask the user which core features to include (multi-select, max 4 options):

```
Which core markdown features do you want?
- Admonitions/Callouts (:::note, :::tip, etc.)
- Math Equations (KaTeX)
- Enhanced Code Blocks (Expressive Code)
- GitHub Repository Cards
```

Default: All selected.

### Step 4: Select Supplementary Features (Selective mode only)

Ask about supplementary features (multi-select, max 3 options):

```
Which supplementary features do you want?
- Reading Time Calculation
- Excerpt Extraction (for SEO)
- Auto-linking Headings (anchor links)
```

Default: All selected. User can also select "None" to skip these.

### Step 5: TypeScript or JavaScript

Ask the user:

```
Which language for config files?
- TypeScript
- JavaScript
```

### Step 6: Generate Files

Based on selections, generate:

1. **Framework config file** (astro.config.mjs, next.config.mjs, etc.)
2. **Plugin files** in `src/plugins/` or `lib/plugins/`:
   - `remark-directive-rehype.js` (if admonitions or GitHub cards)
   - `remark-reading-time.mjs` (if reading time)
   - `remark-excerpt.js` (if excerpt)
   - `rehype-component-admonition.mjs` (if admonitions)
   - `rehype-component-github-card.mjs` (if GitHub cards)
   - `expressive-code-plugins.ts` (if enhanced code blocks, Astro only)
3. **CSS file** with base styles for admonitions and GitHub cards
4. **Example markdown file** demonstrating all enabled features

### Step 7: Show Dependencies

Output the npm install command for required packages:

```bash
npm install remark-math remark-directive rehype-katex rehype-slug ...
```

### Step 8: Post-Setup Instructions

Provide framework-specific instructions:

- **Astro**: "Add KaTeX CSS import to your layout"
- **Next.js**:
  - "Create mdx-components.tsx for custom elements"
  - "**Important**: MDX is NOT compatible with Turbopack. Use `next dev` instead of `next dev --turbopack`"
- **Vite**: "Import the markdown processor in your build"
- **SvelteKit**: "Import KaTeX CSS in your root +layout.svelte"

## File Templates

### Plugin Directory Structure

```
src/plugins/        # or lib/plugins/ for Next.js
├── remark-directive-rehype.js
├── remark-reading-time.mjs
├── remark-excerpt.js
├── rehype-component-admonition.mjs
├── rehype-component-github-card.mjs
└── expressive-code-plugins.ts
```

### Base CSS Template

```css
/* Admonitions */
.admonition {
  border-left: 4px solid var(--admonition-color, #448aff);
  padding: 1rem;
  margin: 1rem 0;
  background: var(--admonition-bg, rgba(68, 138, 255, 0.1));
  border-radius: 0 0.5rem 0.5rem 0;
}

.bdm-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.bdm-note { --admonition-color: #448aff; --admonition-bg: rgba(68, 138, 255, 0.1); }
.bdm-tip { --admonition-color: #00c853; --admonition-bg: rgba(0, 200, 83, 0.1); }
.bdm-important { --admonition-color: #7c4dff; --admonition-bg: rgba(124, 77, 255, 0.1); }
.bdm-warning { --admonition-color: #ff9100; --admonition-bg: rgba(255, 145, 0, 0.1); }
.bdm-caution { --admonition-color: #ff5252; --admonition-bg: rgba(255, 82, 82, 0.1); }

/* GitHub Cards */
.card-github {
  display: block;
  border: 1px solid #30363d;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.card-github:hover {
  border-color: #58a6ff;
  box-shadow: 0 0 0 1px #58a6ff;
}

.gc-titlebar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.gc-titlebar-left {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.gc-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #30363d;
  background-size: cover;
}

.gc-user, .gc-repo {
  font-size: 0.875rem;
}

.gc-repo {
  font-weight: 600;
  color: #58a6ff;
}

.gc-description {
  margin: 0.5rem 0;
  color: #8b949e;
  font-size: 0.875rem;
  line-height: 1.5;
}

.gc-infobar {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #8b949e;
}

.gc-stars::before { content: "⭐ "; }
.gc-forks::before { content: "🍴 "; }

.fetch-waiting {
  opacity: 0.7;
}

.fetch-error .gc-description {
  color: #f85149;
}

/* KaTeX overflow */
.katex-display {
  overflow-x: auto;
  overflow-y: hidden;
}

/* Anchor links */
.anchor {
  opacity: 0;
  margin-left: 0.5rem;
  text-decoration: none;
  color: inherit;
  transition: opacity 0.2s;
}

h1:hover .anchor,
h2:hover .anchor,
h3:hover .anchor,
h4:hover .anchor {
  opacity: 0.7;
}
```

### Example Markdown Template

```markdown
---
title: Markdown Features Demo
---

# Markdown Features Demo

This page demonstrates all the markdown features.

## Admonitions

:::note[Information]
This is a note with useful information.
:::

:::tip
A helpful tip for the reader.
:::

:::warning
Be careful with this operation.
:::

> [!IMPORTANT]
> GitHub-style admonition syntax also works!

## Math Equations

Inline math: $E = mc^2$

Display math:
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

## GitHub Cards

::github{repo="withastro/astro"}

## Code Blocks

```javascript title="example.js"
function greet(name) {
  console.log("Hello, " + name + "!");
}
```

```python {2}
def greet(name):
    print(f"Hello, {name}!")  # highlighted
```

## Spoilers

This sentence has a :spoiler[hidden secret] in it.
```

## Response Format

After generating files:

1. List all files created with their paths
2. Show the npm install command
3. Provide any framework-specific post-setup instructions
4. Suggest testing by creating the example markdown file

## Error Handling

### Unsupported Framework

If the user specifies an unsupported framework:

1. List supported frameworks: Astro, Next.js, Vite, SvelteKit
2. Offer to use the generic Vite/unified configuration
3. Explain that the generic config works with any unified-based setup

### No package.json Found

If no `package.json` exists in the current directory:

1. Warn the user that dependencies cannot be automatically detected
2. Ask if they want to proceed anyway
3. Recommend running `npm init` first

### Existing Files Would Be Overwritten

Before writing any file that already exists:

1. Inform the user which files would be overwritten
2. Ask for confirmation before proceeding
3. Offer to create backup files (e.g., `astro.config.mjs.backup`)

### User Cancels Setup

If the user abandons the interview:

1. Summarize what was configured so far
2. Offer to save partial configuration
3. Explain how to resume with specific arguments

**Example:**
```
Setup cancelled. You had selected:
- Framework: Astro
- Features: Admonitions, Math

To resume, run:
/fuwari-md:setup astro --features admonitions,math
```
