# Expressive Code Configuration

Expressive Code provides enhanced code block rendering with syntax highlighting, line numbers, copy buttons, and more.

## Installation

```bash
npm install astro-expressive-code @expressive-code/plugin-collapsible-sections @expressive-code/plugin-line-numbers
```

## Basic Configuration (Astro)

```javascript
import expressiveCode from 'astro-expressive-code';
import { pluginCollapsibleSections } from '@expressive-code/plugin-collapsible-sections';
import { pluginLineNumbers } from '@expressive-code/plugin-line-numbers';

export default defineConfig({
  integrations: [
    expressiveCode({
      themes: ['github-dark'],
      plugins: [
        pluginCollapsibleSections(),
        pluginLineNumbers(),
      ],
    }),
    // ... other integrations
  ],
});
```

---

## Full Fuwari Configuration

```javascript
import expressiveCode from 'astro-expressive-code';
import { pluginCollapsibleSections } from '@expressive-code/plugin-collapsible-sections';
import { pluginLineNumbers } from '@expressive-code/plugin-line-numbers';
import { pluginLanguageBadge } from './plugins/expressive-code-plugins';
import { pluginCustomCopyButton } from './plugins/expressive-code-plugins';

expressiveCode({
  themes: ['github-dark', 'github-dark'],  // Light/dark themes
  plugins: [
    pluginCollapsibleSections(),
    pluginLineNumbers(),
    pluginLanguageBadge(),        // Custom: shows language in corner
    pluginCustomCopyButton(),     // Custom: animated copy button
  ],
  defaultProps: {
    wrap: true,                   // Enable word wrap
    overridesByLang: {
      'shellsession': {
        showLineNumbers: false,   // No line numbers for shell sessions
      },
    },
  },
  styleOverrides: {
    codeBackground: 'var(--codeblock-bg)',
    borderRadius: '0.75rem',
    borderColor: 'none',
    codeFontSize: '0.875rem',
    codeFontFamily: "'JetBrains Mono Variable', ui-monospace, monospace",
    codeLineHeight: '1.5rem',
    frames: {
      editorBackground: 'var(--codeblock-bg)',
      terminalBackground: 'var(--codeblock-bg)',
      terminalTitlebarBackground: 'var(--codeblock-topbar-bg)',
      editorTabBarBackground: 'var(--codeblock-topbar-bg)',
      editorActiveTabBackground: 'none',
      editorActiveTabIndicatorBottomColor: 'var(--primary)',
      editorActiveTabIndicatorTopColor: 'none',
      editorTabBarBorderBottomColor: 'var(--codeblock-topbar-bg)',
      terminalTitlebarBorderBottomColor: 'none',
    },
    textMarkers: {
      delHue: 0,      // Red for deletions
      insHue: 180,    // Cyan for insertions
      markHue: 250,   // Purple for marks
    },
  },
  frames: {
    showCopyToClipboardButton: false,  // We use custom copy button
  },
})
```

---

## Built-in Plugins

### pluginLineNumbers

Shows line numbers in code blocks.

```javascript
import { pluginLineNumbers } from '@expressive-code/plugin-line-numbers';

plugins: [pluginLineNumbers()]

// Per-block control via meta:
// ```js showLineNumbers=false
// ```
```

### pluginCollapsibleSections

Allows collapsing sections of code.

```javascript
import { pluginCollapsibleSections } from '@expressive-code/plugin-collapsible-sections';

plugins: [pluginCollapsibleSections()]
```

**Usage in markdown:**
````markdown
```js collapse={1-5}
// These lines will be collapsed
import { a } from 'a';
import { b } from 'b';
import { c } from 'c';
import { d } from 'd';
// End of collapsed section

function main() {
  // This is visible
}
```
````

---

## Custom Plugins

### pluginLanguageBadge

Shows the code language as a badge in the corner.

**Source:** `sources/expressive-code-plugins.ts`

**Features:**
- Positioned in top-right corner
- Fades on hover (to not obstruct copy button)
- Respects theme colors via CSS variables

**CSS variables used:**
- `--hue` - Theme hue for color calculation

### pluginCustomCopyButton

Adds a custom copy button with animated feedback.

**Source:** `sources/expressive-code-plugins.ts`

**Features:**
- Copy and success icons (SVG)
- Animated transition between states
- Positioned in code block

**Required CSS:**
```css
.copy-btn {
  position: absolute;
  right: 0.5rem;
  top: 0.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s;
}

pre:hover .copy-btn {
  opacity: 1;
}

.copy-icon { display: block; }
.success-icon { display: none; }

.copy-btn.copied .copy-icon { display: none; }
.copy-btn.copied .success-icon { display: block; }
```

**JavaScript for copy functionality:**
```javascript
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const pre = btn.closest('pre');
    const code = pre.querySelector('code');
    await navigator.clipboard.writeText(code.textContent);
    btn.classList.add('copied');
    setTimeout(() => btn.classList.remove('copied'), 2000);
  });
});
```

---

## Code Block Features

### Syntax Highlighting

Automatic based on language:
````markdown
```javascript
const x = 1;
```

```python
x = 1
```

```rust
let x = 1;
```
````

### Line Highlighting

Mark specific lines:
````markdown
```js {2,4-6}
const a = 1;
const b = 2;  // highlighted
const c = 3;
const d = 4;  // highlighted
const e = 5;  // highlighted
const f = 6;  // highlighted
```
````

### Diff Highlighting

Show additions and deletions:
````markdown
```js
const a = 1;
const b = 2;  // [!code --]
const c = 3;  // [!code ++]
```
````

### Title/Filename

Add a title to code blocks:
````markdown
```js title="config.js"
export default {};
```
````

### Word Wrap

Enable word wrap for long lines:
````markdown
```js wrap
const veryLongLine = "This line is very long and will wrap to the next line instead of scrolling horizontally";
```
````

---

## Theming

### Available Themes

Common themes:
- `github-dark`, `github-light`
- `dracula`
- `nord`
- `one-dark-pro`
- `vitesse-dark`, `vitesse-light`

### CSS Variables

Define these for custom styling:
```css
:root {
  --codeblock-bg: #1e1e1e;
  --codeblock-topbar-bg: #2d2d2d;
  --primary: #007acc;
  --hue: 250;
}
```

---

## Next.js / MDX Integration

For Next.js with MDX:

```javascript
// next.config.mjs
import createMDX from '@next/mdx';
import { pluginCollapsibleSections } from '@expressive-code/plugin-collapsible-sections';
import { pluginLineNumbers } from '@expressive-code/plugin-line-numbers';

const withMDX = createMDX({
  options: {
    rehypePlugins: [
      // ... your rehype plugins
    ],
  },
});

export default withMDX({
  pageExtensions: ['js', 'jsx', 'mdx', 'ts', 'tsx'],
});
```

Note: Expressive Code integration with Next.js may require additional setup. See the expressive-code documentation for framework-specific guides.
