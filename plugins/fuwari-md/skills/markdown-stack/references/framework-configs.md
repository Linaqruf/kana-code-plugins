# Framework Configuration Guide

This guide shows how to adapt the markdown processing stack to different frameworks. The stack is portable - adapt these patterns to your project's conventions.

## Framework Compatibility & Limitations

Before choosing your framework, review the compatibility matrix:

| Framework | MDX/Markdown Support | Known Limitations | Recommendation |
|-----------|---------------------|-------------------|----------------|
| **Astro** | Native remark/rehype | None | Best support - recommended for blogs |
| **Next.js** | Via @next/mdx | **Turbopack incompatible** - must use webpack mode | Use `next dev` not `next dev --turbopack` |
| **Vite** | Via plugins | Requires manual unified setup | Good for custom builds |
| **SvelteKit** | Via mdsvex | Different component syntax | Good with mdsvex knowledge |
| **Docusaurus** | Built-in MDX | Has own admonition syntax (:::note) | Use built-in features when possible |
| **Remix** | Via MDX | Limited plugin support | Simpler setups only |

### Critical: Next.js Turbopack Warning

MDX is **NOT compatible with Turbopack**. If your `package.json` has:

```json
{
  "scripts": {
    "dev": "next dev --turbopack"  // MDX WILL NOT WORK
  }
}
```

**Fix:** Remove the `--turbopack` flag:

```json
{
  "scripts": {
    "dev": "next dev"  // MDX works with webpack
  }
}
```

Turbopack support for MDX is tracked in [vercel/next.js#64525](https://github.com/vercel/next.js/issues/64525).

---

## Astro

Astro has first-class markdown support with remark/rehype plugins. This is the reference implementation - adapt the plugin order and options to your project's needs.

**Adapt for your project:**
- Remove plugins you don't need (e.g., skip `remarkExcerpt` if not using SEO excerpts)
- Adjust file paths for custom plugins based on your project structure
- Customize Expressive Code themes to match your design

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

Next.js uses MDX for markdown processing. The remark/rehype pipeline works the same, but component registration differs.

**Adapt for your project:**
- Use your existing component library for admonitions instead of creating new ones
- Consider using `next-mdx-remote` for dynamic MDX loading
- Adjust paths based on your `src/` vs root structure

**Critical:** MDX does NOT work with Turbopack. See the [Turbopack warning](#critical-nextjs-turbopack-warning) above.

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

For vanilla Vite projects or custom setups where you need full control over the markdown pipeline.

**Adapt for your project:**
- This is a standalone processor - integrate it into your build pipeline as needed
- Use as a library function, CLI tool, or build plugin
- Works with any bundler (Vite, Webpack, esbuild, Rollup)

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

SvelteKit uses mdsvex for markdown processing, which supports remark/rehype plugins with some syntax differences.

**Adapt for your project:**
- Use Svelte components for custom elements instead of hastscript
- mdsvex uses `.svx` extension for markdown files with Svelte components
- Layout files work differently than Astro/Next.js

### Configuration

```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-auto';
import { mdsvex } from 'mdsvex';
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import remarkGithubAdmonitionsToDirectives from 'remark-github-admonitions-to-directives';
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';

export default {
  extensions: ['.svelte', '.md', '.svx'],
  preprocess: [
    mdsvex({
      extensions: ['.md', '.svx'],
      remarkPlugins: [
        remarkMath,
        remarkGithubAdmonitionsToDirectives,
        remarkDirective,
      ],
      rehypePlugins: [
        rehypeKatex,
        rehypeSlug,
        [rehypeAutolinkHeadings, { behavior: 'append' }],
      ],
    }),
  ],
  kit: {
    adapter: adapter(),
  },
};
```

### Custom Components in mdsvex

mdsvex allows custom Svelte components for directives:

```svelte
<!-- src/lib/components/Admonition.svelte -->
<script>
  export let type = 'note';
  export let title = '';
</script>

<aside class="admonition admonition-{type}">
  {#if title}
    <div class="admonition-title">{title}</div>
  {/if}
  <slot />
</aside>

<style>
  .admonition {
    padding: 1rem;
    border-left: 4px solid var(--admonition-color, #448aff);
    margin: 1rem 0;
  }
  .admonition-note { --admonition-color: #448aff; }
  .admonition-warning { --admonition-color: #ff9100; }
  .admonition-tip { --admonition-color: #00c853; }
</style>
```

### Layout with KaTeX CSS

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  import 'katex/dist/katex.min.css';
</script>

<slot />
```

### Reading Time in SvelteKit

```javascript
// src/lib/utils/reading-time.js
import readingTime from 'reading-time';

export function getReadingTime(content) {
  const stats = readingTime(content);
  return Math.ceil(stats.minutes);
}

// Use in +page.server.js
export async function load({ params }) {
  const post = await getPost(params.slug);
  return {
    post,
    readingTime: getReadingTime(post.content),
  };
}
```

---

## Docusaurus

Docusaurus has built-in MDX support with many features already included. Don't reinvent the wheel - use Docusaurus's built-in features when they exist.

**Adapt for your project:**
- Use built-in admonitions (:::note, :::tip) instead of adding remark-directive
- Use built-in code highlighting instead of Expressive Code
- Only add plugins for features Docusaurus doesn't have (like GitHub cards)

### Configuration

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
          readingTime: ({ content }) => content.split(/\s+/).length / 200,
        },
      },
    ],
  ],
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css',
      type: 'text/css',
    },
  ],
};
```

### Built-in Admonitions

Docusaurus uses different syntax for admonitions:

```markdown
:::note
This is a note.
:::

:::tip
This is a tip.
:::

:::info
This is info.
:::

:::caution
This is a caution.
:::

:::danger
This is a danger warning.
:::
```

### GitHub-style Admonitions

To use `> [!NOTE]` syntax, add the conversion plugin:

```javascript
// docusaurus.config.js
import remarkGithubAdmonitionsToDirectives from 'remark-github-admonitions-to-directives';

export default {
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          remarkPlugins: [
            remarkGithubAdmonitionsToDirectives,
            // Note: Docusaurus will map these to its built-in admonitions
          ],
        },
      },
    ],
  ],
};
```

### Custom Code Block Features

Docusaurus supports code block features via comments:

```javascript
// highlight-next-line
const highlighted = true;

// highlight-start
const block = 'of';
const highlighted = 'lines';
// highlight-end
```

### Adding GitHub Cards

For GitHub cards in Docusaurus, use MDX components:

```jsx
// src/components/GitHubCard.jsx
import React, { useState, useEffect } from 'react';

export default function GitHubCard({ repo }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`https://api.github.com/repos/${repo}`)
      .then(res => res.json())
      .then(setData);
  }, [repo]);

  if (!data) return <div>Loading...</div>;

  return (
    <a href={data.html_url} className="github-card">
      <h3>{data.full_name}</h3>
      <p>{data.description}</p>
      <span>⭐ {data.stargazers_count}</span>
    </a>
  );
}
```

Usage in MDX:

```mdx
import GitHubCard from '@site/src/components/GitHubCard';

<GitHubCard repo="facebook/docusaurus" />
```

---

## Remix

Remix has MDX support but with more limited plugin options than other frameworks.

**Adapt for your project:**
- Keep it simple - Remix MDX works best with fewer plugins
- Use React components for custom elements
- Consider if you really need all features or just the basics (math + code highlighting)

### Configuration with MDX

```javascript
// remix.config.js
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';

export default {
  mdx: {
    remarkPlugins: [remarkMath, remarkDirective],
    rehypePlugins: [rehypeKatex, rehypeSlug],
  },
};
```

### MDX Route with Frontmatter

```mdx
---
title: My Post
description: A blog post with math
---

# {frontmatter.title}

The equation $E = mc^2$ changed physics.
```

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
