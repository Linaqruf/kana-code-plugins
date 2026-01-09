# Framework Configuration Guide

This guide shows how to integrate the Fuwari markdown stack into different frameworks.

## Astro

Astro has first-class markdown support with remark/rehype plugins.

### Full Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import expressiveCode from 'astro-expressive-code';
import { pluginCollapsibleSections } from '@expressive-code/plugin-collapsible-sections';
import { pluginLineNumbers } from '@expressive-code/plugin-line-numbers';
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import remarkGithubAdmonitionsToDirectives from 'remark-github-admonitions-to-directives';
import remarkSectionize from 'remark-sectionize';
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeComponents from 'rehype-components';

// Custom plugins (copy from sources/)
import { remarkReadingTime } from './src/plugins/remark-reading-time.mjs';
import { remarkExcerpt } from './src/plugins/remark-excerpt.js';
import { parseDirectiveNode } from './src/plugins/remark-directive-rehype.js';
import { AdmonitionComponent } from './src/plugins/rehype-component-admonition.mjs';
import { GithubCardComponent } from './src/plugins/rehype-component-github-card.mjs';
import { pluginLanguageBadge, pluginCustomCopyButton } from './src/plugins/expressive-code-plugins';

export default defineConfig({
  integrations: [
    expressiveCode({
      themes: ['github-dark'],
      plugins: [
        pluginCollapsibleSections(),
        pluginLineNumbers(),
        pluginLanguageBadge(),
        pluginCustomCopyButton(),
      ],
    }),
  ],
  markdown: {
    remarkPlugins: [
      remarkMath,
      remarkReadingTime,
      remarkExcerpt,
      remarkGithubAdmonitionsToDirectives,
      remarkDirective,
      remarkSectionize,
      parseDirectiveNode,
    ],
    rehypePlugins: [
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
    ],
  },
});
```

### Accessing Frontmatter Data

```astro
---
// In your .astro component
const { frontmatter } = Astro.props;
const { minutes, words, excerpt } = frontmatter;
---

<article>
  <p>{minutes} min read ({words} words)</p>
  <meta name="description" content={excerpt} />
</article>
```

---

## Next.js (with MDX)

### Installation

```bash
npm install @next/mdx @mdx-js/loader @mdx-js/react
npm install remark-math remark-directive remark-gfm
npm install rehype-katex rehype-slug rehype-autolink-headings
```

### Configuration

```javascript
// next.config.mjs
import createMDX from '@next/mdx';
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';

const withMDX = createMDX({
  extension: /\.mdx?$/,
  options: {
    remarkPlugins: [
      remarkGfm,
      remarkMath,
      remarkDirective,
      // Add custom remark plugins here
    ],
    rehypePlugins: [
      rehypeKatex,
      rehypeSlug,
      [rehypeAutolinkHeadings, { behavior: 'wrap' }],
      // Add custom rehype plugins here
    ],
  },
});

export default withMDX({
  pageExtensions: ['js', 'jsx', 'mdx', 'ts', 'tsx'],
});
```

### MDX Components

```jsx
// components/MDXComponents.jsx
import { Admonition } from './Admonition';
import { GithubCard } from './GithubCard';

export const mdxComponents = {
  // Map custom elements to React components
  note: (props) => <Admonition type="note" {...props} />,
  tip: (props) => <Admonition type="tip" {...props} />,
  warning: (props) => <Admonition type="warning" {...props} />,
  github: GithubCard,
};
```

### KaTeX CSS

```jsx
// app/layout.jsx or _app.jsx
import 'katex/dist/katex.min.css';
```

---

## Vite (Generic Unified)

For vanilla Vite projects or custom setups.

### Installation

```bash
npm install unified remark-parse remark-rehype rehype-stringify
npm install remark-math remark-directive
npm install rehype-katex rehype-slug
```

### Processor Setup

```javascript
// lib/markdown.js
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import remarkRehype from 'remark-rehype';
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';
import rehypeStringify from 'rehype-stringify';

// Custom plugins
import { parseDirectiveNode } from './plugins/remark-directive-rehype.js';
import { remarkReadingTime } from './plugins/remark-reading-time.mjs';

export async function processMarkdown(content) {
  const file = await unified()
    .use(remarkParse)
    .use(remarkMath)
    .use(remarkDirective)
    .use(parseDirectiveNode)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeKatex)
    .use(rehypeSlug)
    .use(rehypeStringify, { allowDangerousHtml: true })
    .process(content);

  return String(file);
}
```

### Vite Plugin

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import { processMarkdown } from './lib/markdown.js';

export default defineConfig({
  plugins: [
    {
      name: 'markdown-transform',
      async transform(code, id) {
        if (id.endsWith('.md')) {
          const html = await processMarkdown(code);
          return `export default ${JSON.stringify(html)}`;
        }
      },
    },
  ],
});
```

---

## SvelteKit

### Configuration

```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-auto';
import { mdsvex } from 'mdsvex';
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';

export default {
  extensions: ['.svelte', '.md', '.svx'],
  preprocess: [
    mdsvex({
      extensions: ['.md', '.svx'],
      remarkPlugins: [
        remarkMath,
        remarkDirective,
      ],
      rehypePlugins: [
        rehypeKatex,
        rehypeSlug,
      ],
    }),
  ],
  kit: {
    adapter: adapter(),
  },
};
```

---

## Docusaurus

Docusaurus has built-in MDX support with some features already included.

```javascript
// docusaurus.config.js
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default {
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: {
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
      },
    ],
  ],
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
    },
  ],
};
```

Note: Docusaurus has built-in admonition support with different syntax.

---

## Common Setup Steps

### 1. Install Dependencies

```bash
# Core
npm install remark-math remark-directive rehype-katex rehype-slug

# For admonitions
npm install remark-github-admonitions-to-directives rehype-components hastscript

# For reading time
npm install reading-time mdast-util-to-string

# For expressive code (Astro)
npm install astro-expressive-code @expressive-code/plugin-line-numbers
```

### 2. Copy Custom Plugins

Copy from `sources/` directory:
- `remark-directive-rehype.js`
- `remark-reading-time.mjs`
- `remark-excerpt.js`
- `rehype-component-admonition.mjs`
- `rehype-component-github-card.mjs`
- `expressive-code-plugins.ts` (if using Expressive Code)

### 3. Add Required CSS

```css
/* KaTeX */
@import 'katex/dist/katex.min.css';

/* Admonitions */
.admonition {
  border-left: 4px solid;
  padding: 1rem;
  margin: 1rem 0;
}
.bdm-note { border-color: #448aff; background: #448aff10; }
.bdm-tip { border-color: #00c853; background: #00c85310; }
.bdm-important { border-color: #7c4dff; background: #7c4dff10; }
.bdm-warning { border-color: #ff9100; background: #ff910010; }
.bdm-caution { border-color: #ff5252; background: #ff525210; }

/* GitHub cards */
.card-github {
  display: block;
  border: 1px solid #30363d;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  text-decoration: none;
  color: inherit;
}
```

### 4. Test Your Setup

Create a test markdown file:

```markdown
# Test Page

## Math

Inline: $E = mc^2$

Display:
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

## Admonitions

:::note[Custom Title]
This is a note.
:::

> [!TIP]
> GitHub-style tip.

## GitHub Card

::github{repo="withastro/astro"}

## Code

```javascript title="example.js"
const hello = 'world';
```
```
