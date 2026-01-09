# Rehype Plugins Reference

## Plugin Order

The order of rehype plugins matters. Use this sequence:

```javascript
rehypePlugins: [
  rehypeKatex,           // 1. Render math (needs math nodes from remark-math)
  rehypeSlug,            // 2. Add IDs to headings (needed for autolink)
  [rehypeComponents, {}], // 3. Render custom components (admonitions, cards)
  [rehypeAutolinkHeadings, {}], // 4. Add anchor links (needs slug IDs)
]
```

---

## rehype-katex

Renders LaTeX math nodes to HTML using KaTeX.

**Installation:**
```bash
npm install rehype-katex katex
```

**Usage:**
```javascript
import rehypeKatex from 'rehype-katex';

// In unified pipeline:
.use(rehypeKatex)
```

**Required CSS:**
```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css"
  integrity="sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEaqSD1odI+WdtXRGWt2kTvGFasHpSy3SV"
  crossorigin="anonymous"
/>
```

**Or import in CSS:**
```css
@import 'katex/dist/katex.min.css';
```

**Options:**
```javascript
.use(rehypeKatex, {
  strict: false,           // Don't throw on unknown commands
  throwOnError: false,     // Render error instead of throwing
  output: 'htmlAndMathml', // Accessibility support
})
```

**Styling for overflow:**
```css
.katex-display {
  overflow-x: auto;
  overflow-y: hidden;
}
```

---

## rehype-slug

Adds `id` attributes to headings based on their text content.

**Installation:**
```bash
npm install rehype-slug
```

**Usage:**
```javascript
import rehypeSlug from 'rehype-slug';

// In unified pipeline:
.use(rehypeSlug)
```

**Before:**
```html
<h2>My Heading</h2>
```

**After:**
```html
<h2 id="my-heading">My Heading</h2>
```

**Notes:**
- Required before `rehype-autolink-headings`
- Handles duplicate headings by appending numbers

---

## rehype-autolink-headings

Adds anchor links to headings for easy navigation.

**Installation:**
```bash
npm install rehype-autolink-headings
```

**Usage:**
```javascript
import rehypeAutolinkHeadings from 'rehype-autolink-headings';

// In unified pipeline - AFTER rehypeSlug:
.use(rehypeSlug)
.use(rehypeAutolinkHeadings, {
  behavior: 'append',  // Add link after heading text
  properties: {
    className: ['anchor'],
  },
  content: {
    type: 'element',
    tagName: 'span',
    properties: {
      className: ['anchor-icon'],
      'data-pagefind-ignore': true,  // Exclude from search
    },
    children: [{ type: 'text', value: '#' }],
  },
})
```

**Behavior options:**
- `'prepend'` - Add link before heading text
- `'append'` - Add link after heading text
- `'wrap'` - Wrap entire heading in link
- `'before'` - Add link as sibling before heading
- `'after'` - Add link as sibling after heading

**Styling:**
```css
.anchor {
  opacity: 0;
  transition: opacity 0.2s;
  margin-left: 0.5rem;
  text-decoration: none;
}

h2:hover .anchor,
h3:hover .anchor {
  opacity: 1;
}
```

---

## rehype-components

Renders custom directive components to HTML.

**Installation:**
```bash
npm install rehype-components hastscript
```

**Usage:**
```javascript
import rehypeComponents from 'rehype-components';
import { AdmonitionComponent } from './rehype-component-admonition.mjs';
import { GithubCardComponent } from './rehype-component-github-card.mjs';

// In unified pipeline:
.use(rehypeComponents, {
  components: {
    // GitHub card directive
    github: GithubCardComponent,

    // Admonition directives (with type parameter)
    note: (props, children) => AdmonitionComponent(props, children, 'note'),
    tip: (props, children) => AdmonitionComponent(props, children, 'tip'),
    important: (props, children) => AdmonitionComponent(props, children, 'important'),
    caution: (props, children) => AdmonitionComponent(props, children, 'caution'),
    warning: (props, children) => AdmonitionComponent(props, children, 'warning'),
  },
})
```

**Component function signature:**
```javascript
function MyComponent(properties, children) {
  // properties: Object with directive attributes
  // children: Array of child HAST nodes
  // Return: HAST node (use hastscript)

  return h('div', { class: 'my-component' }, children);
}
```

---

## AdmonitionComponent (Custom)

Renders admonition/callout blocks.

**Source:** `sources/rehype-component-admonition.mjs`

**Rendered HTML:**
```html
<blockquote class="admonition bdm-note">
  <span class="bdm-title">NOTE</span>
  <!-- content -->
</blockquote>
```

**With custom title:**
```html
<blockquote class="admonition bdm-tip">
  <span class="bdm-title">
    <div>Custom Title</div>
  </span>
  <!-- content -->
</blockquote>
```

**Required CSS (basic):**
```css
.admonition {
  border-left: 4px solid var(--admonition-color);
  padding: 1rem;
  margin: 1rem 0;
  background: var(--admonition-bg);
}

.bdm-note { --admonition-color: #448aff; }
.bdm-tip { --admonition-color: #00c853; }
.bdm-important { --admonition-color: #7c4dff; }
.bdm-warning { --admonition-color: #ff9100; }
.bdm-caution { --admonition-color: #ff5252; }
```

---

## GithubCardComponent (Custom)

Renders GitHub repository cards with API data.

**Source:** `sources/rehype-component-github-card.mjs`

**Features:**
- Fetches repo data from GitHub API
- Displays: description, stars, forks, language, license
- Owner avatar
- Loading and error states

**Rendered HTML structure:**
```html
<a class="card-github fetch-waiting" href="https://github.com/owner/repo">
  <div class="gc-titlebar">...</div>
  <div class="gc-description">...</div>
  <div class="gc-infobar">
    <div class="gc-stars">...</div>
    <div class="gc-forks">...</div>
    <div class="gc-license">...</div>
    <span class="gc-language">...</span>
  </div>
  <script>/* fetch logic */</script>
</a>
```

**Required CSS (basic):**
```css
.card-github {
  display: block;
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  padding: 1rem;
  text-decoration: none;
}

.card-github.fetch-waiting {
  opacity: 0.7;
}

.gc-titlebar {
  display: flex;
  justify-content: space-between;
}

.gc-infobar {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}
```

---

## Complete Rehype Configuration

```javascript
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeComponents from 'rehype-components';
import { AdmonitionComponent } from './plugins/rehype-component-admonition.mjs';
import { GithubCardComponent } from './plugins/rehype-component-github-card.mjs';

export const rehypePlugins = [
  rehypeKatex,
  rehypeSlug,
  [
    rehypeComponents,
    {
      components: {
        github: GithubCardComponent,
        note: (x, y) => AdmonitionComponent(x, y, 'note'),
        tip: (x, y) => AdmonitionComponent(x, y, 'tip'),
        important: (x, y) => AdmonitionComponent(x, y, 'important'),
        caution: (x, y) => AdmonitionComponent(x, y, 'caution'),
        warning: (x, y) => AdmonitionComponent(x, y, 'warning'),
      },
    },
  ],
  [
    rehypeAutolinkHeadings,
    {
      behavior: 'append',
      properties: { className: ['anchor'] },
      content: {
        type: 'element',
        tagName: 'span',
        properties: { className: ['anchor-icon'] },
        children: [{ type: 'text', value: '#' }],
      },
    },
  ],
];
```
