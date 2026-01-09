# Troubleshooting Guide

Common issues and solutions when implementing the Fuwari markdown stack.

## Plugin Order Issues

### Problem: Directives not rendering

**Symptom:** `:::note` or `::github` appears as plain text.

**Cause:** Plugin order is wrong.

**Solution:** Ensure this order:
```javascript
remarkPlugins: [
  // ... other plugins
  remarkGithubAdmonitionsToDirectives, // BEFORE remarkDirective
  remarkDirective,                      // Parse directives
  remarkSectionize,
  parseDirectiveNode,                   // AFTER remarkDirective, converts to HAST
],
rehypePlugins: [
  // ... other plugins
  [rehypeComponents, { components: {...} }], // Renders the HAST nodes
]
```

### Problem: Math not rendering

**Symptom:** `$...$` appears as plain text with dollar signs.

**Cause:** `remark-math` not running first, or `rehype-katex` missing.

**Solution:**
```javascript
remarkPlugins: [
  remarkMath, // FIRST - before any plugin that might modify text
  // ... other plugins
],
rehypePlugins: [
  rehypeKatex, // Renders the math nodes
  // ... other plugins
]
```

---

## Styling Issues

### Problem: Admonitions have no styling

**Symptom:** Admonitions render but look like plain blockquotes.

**Solution:** Add CSS for admonition classes:

```css
.admonition {
  border-left: 4px solid var(--admonition-color, #448aff);
  padding: 1rem;
  margin: 1rem 0;
  background: var(--admonition-bg, rgba(68, 138, 255, 0.1));
  border-radius: 0 0.5rem 0.5rem 0;
}

.bdm-title {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  font-size: 0.875rem;
}

.bdm-note { --admonition-color: #448aff; --admonition-bg: rgba(68, 138, 255, 0.1); }
.bdm-tip { --admonition-color: #00c853; --admonition-bg: rgba(0, 200, 83, 0.1); }
.bdm-important { --admonition-color: #7c4dff; --admonition-bg: rgba(124, 77, 255, 0.1); }
.bdm-warning { --admonition-color: #ff9100; --admonition-bg: rgba(255, 145, 0, 0.1); }
.bdm-caution { --admonition-color: #ff5252; --admonition-bg: rgba(255, 82, 82, 0.1); }
```

### Problem: KaTeX equations overflow

**Symptom:** Long equations extend beyond container.

**Solution:**
```css
.katex-display {
  overflow-x: auto;
  overflow-y: hidden;
  padding: 0.5rem 0;
}

.katex-display > .katex {
  white-space: nowrap;
}
```

### Problem: GitHub cards not styled

**Solution:** Add GitHub card CSS:

```css
.card-github {
  display: block;
  border: 1px solid #30363d;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s;
}

.card-github:hover {
  border-color: #58a6ff;
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

.gc-description {
  margin: 0.5rem 0;
  color: #8b949e;
  font-size: 0.875rem;
}

.gc-infobar {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #8b949e;
}

.fetch-waiting {
  opacity: 0.7;
}

.fetch-error .gc-description {
  color: #f85149;
}
```

---

## Build Errors

### Problem: "Cannot find module 'hastscript'"

**Solution:**
```bash
npm install hastscript
```

### Problem: "Cannot find module 'unist-util-visit'"

**Solution:**
```bash
npm install unist-util-visit
```

### Problem: "Cannot find module 'mdast-util-to-string'"

**Solution:**
```bash
npm install mdast-util-to-string
```

### Problem: TypeScript errors with custom plugins

**Symptom:** Type errors when importing `.mjs` or `.js` plugins.

**Solutions:**

**Option 1: Use `// @ts-ignore` (quick fix)**
```typescript
// @ts-ignore
import { remarkReadingTime } from './plugins/remark-reading-time.mjs';
```

**Option 2: Create type declarations (recommended)**

Create `plugins/types.d.ts`:
```typescript
// plugins/types.d.ts
import type { Root as MdastRoot } from 'mdast';
import type { Root as HastRoot } from 'hast';
import type { VFile } from 'vfile';
import type { Plugin } from 'unified';

// Remark plugins (MDAST)
declare module './remark-reading-time.mjs' {
  const remarkReadingTime: Plugin<[], MdastRoot>;
  export { remarkReadingTime };
}

declare module './remark-excerpt.js' {
  const remarkExcerpt: Plugin<[], MdastRoot>;
  export { remarkExcerpt };
}

declare module './remark-directive-rehype.js' {
  const parseDirectiveNode: Plugin<[], MdastRoot>;
  export { parseDirectiveNode };
}

// Rehype components (HAST)
declare module './rehype-component-admonition.mjs' {
  import type { Element } from 'hast';
  export function AdmonitionComponent(
    properties: Record<string, unknown>,
    children: Element[]
  ): Element;
}

declare module './rehype-component-github-card.mjs' {
  import type { Element } from 'hast';
  export function GithubCardComponent(
    properties: { repo?: string },
    children: Element[]
  ): Element;
}
```

**Option 3: Configure tsconfig.json**
```json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true
  }
}
```

**Option 4: Convert plugins to TypeScript**

See `sources/expressive-code-plugins.ts` as an example of a TypeScript plugin.

---

## Runtime Errors

### Problem: GitHub cards show "Waiting for api.github.com..."

**Cause:** GitHub API request failed or was blocked.

**Possible causes:**
1. Rate limiting (60 requests/hour for unauthenticated)
2. CORS issues in development
3. Network blocking
4. Invalid repository name

**Solutions:**

1. **Check browser console for errors**

2. **Add retry logic with exponential backoff:**
```javascript
async function fetchWithRetry(url, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url);
      if (res.status === 403) {
        // Rate limited - wait longer
        await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      if (i === retries - 1) throw err;
      await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
    }
  }
}
```

3. **Cache API responses in localStorage:**
```javascript
const CACHE_KEY = 'github-card-cache';
const CACHE_TTL = 1000 * 60 * 60; // 1 hour

function getCached(repo) {
  const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}');
  const entry = cache[repo];
  if (entry && Date.now() - entry.timestamp < CACHE_TTL) {
    return entry.data;
  }
  return null;
}

function setCache(repo, data) {
  const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}');
  cache[repo] = { data, timestamp: Date.now() };
  localStorage.setItem(CACHE_KEY, JSON.stringify(cache));
}
```

4. **Use a GitHub token for higher rate limits (5000/hour):**
```javascript
// Server-side only - never expose token in client code
const headers = process.env.GITHUB_TOKEN
  ? { Authorization: `token ${process.env.GITHUB_TOKEN}` }
  : {};

fetch(`https://api.github.com/repos/${repo}`, { headers });
```

5. **Add graceful fallback UI:**
```css
.card-github.fetch-error {
  border-color: var(--caution-color, #f85149);
}

.card-github.fetch-error .gc-description::before {
  content: "⚠️ ";
}
```

### Problem: Copy button doesn't work

**Cause:** Missing JavaScript for copy functionality.

**Solution:** Add this script:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const pre = btn.closest('pre');
      const code = pre.querySelector('code');

      try {
        await navigator.clipboard.writeText(code.textContent);
        btn.classList.add('copied');
        setTimeout(() => btn.classList.remove('copied'), 2000);
      } catch (err) {
        console.error('Failed to copy:', err);
      }
    });
  });
});
```

---

## Framework-Specific Issues

### Astro: remarkReadingTime not injecting data

**Cause:** The plugin expects Astro's file data structure.

**Solution:** Ensure you're using Content Collections:

```javascript
// In remarkReadingTime
data.astro.frontmatter.minutes = ...
```

For non-Astro frameworks, modify the plugin:
```javascript
export function remarkReadingTime() {
  return (tree, file) => {
    const textOnPage = toString(tree);
    const readingTime = getReadingTime(textOnPage);

    // Generic approach
    file.data.readingTime = {
      minutes: Math.max(1, Math.round(readingTime.minutes)),
      words: readingTime.words,
    };
  };
}
```

### Next.js: Admonitions not rendering

**Cause:** Need to map directive elements to React components.

**Solution:** Use MDX components:

```jsx
// components/MDXComponents.jsx
const Admonition = ({ type, children }) => (
  <blockquote className={`admonition bdm-${type}`}>
    <span className="bdm-title">{type.toUpperCase()}</span>
    {children}
  </blockquote>
);

export const mdxComponents = {
  note: (props) => <Admonition type="note" {...props} />,
  tip: (props) => <Admonition type="tip" {...props} />,
  // ... etc
};
```

---

## Performance Issues

### Problem: Slow build with many markdown files

**Solutions:**

1. **Cache KaTeX rendering:**
```javascript
import rehypeKatex from 'rehype-katex';

.use(rehypeKatex, {
  trust: true,        // Skip validation for trusted content
  strict: false,      // Don't throw on warnings
})
```

2. **Lazy load GitHub cards:**
```javascript
// Use Intersection Observer to fetch only visible cards
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      fetchGithubData(entry.target);
      observer.unobserve(entry.target);
    }
  });
});

document.querySelectorAll('.card-github').forEach(card => {
  observer.observe(card);
});
```

3. **Preload common KaTeX fonts:**
```html
<link rel="preload" href="/fonts/KaTeX_Main-Regular.woff2" as="font" type="font/woff2" crossorigin>
```

---

## Debugging Tips

### Enable verbose logging

```javascript
// Add to any custom plugin
export function myPlugin() {
  return (tree, file) => {
    console.log('Processing:', file.path);
    console.log('Tree:', JSON.stringify(tree, null, 2));
  };
}
```

### Inspect AST

Use `unist-util-inspect`:

```javascript
import { inspect } from 'unist-util-inspect';

export function debugPlugin() {
  return (tree) => {
    console.log(inspect(tree));
  };
}
```

### Check plugin execution order

```javascript
const plugins = [
  [() => (tree) => console.log('1. Start'), {}],
  remarkMath,
  [() => (tree) => console.log('2. After remarkMath'), {}],
  remarkDirective,
  [() => (tree) => console.log('3. After remarkDirective'), {}],
];
```
