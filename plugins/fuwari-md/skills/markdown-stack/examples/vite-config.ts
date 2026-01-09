/**
 * Generic Vite/Unified configuration for Fuwari markdown stack.
 *
 * This shows how to set up a unified processor that can be used
 * in any framework or as a standalone markdown processor.
 */

import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import remarkGithubAdmonitionsToDirectives from 'remark-github-admonitions-to-directives';
import remarkRehype from 'remark-rehype';
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeStringify from 'rehype-stringify';

// Custom plugins (copy from sources/)
import { parseDirectiveNode } from './plugins/remark-directive-rehype.js';
import { AdmonitionComponent } from './plugins/rehype-component-admonition.mjs';
import { GithubCardComponent } from './plugins/rehype-component-github-card.mjs';

// For reading time (optional - modify for non-Astro use)
import { toString } from 'mdast-util-to-string';
import getReadingTime from 'reading-time';

/**
 * Custom reading time plugin (framework-agnostic version)
 */
function remarkReadingTime() {
  return (tree: any, file: any) => {
    const text = toString(tree);
    const time = getReadingTime(text);

    // Store in file data (access via file.data.readingTime)
    file.data.readingTime = {
      minutes: Math.max(1, Math.round(time.minutes)),
      words: time.words,
    };
  };
}

/**
 * Custom excerpt plugin (framework-agnostic version)
 */
function remarkExcerpt() {
  return (tree: any, file: any) => {
    let excerpt = '';
    for (const node of tree.children) {
      if (node.type === 'paragraph') {
        excerpt = toString(node);
        break;
      }
    }
    file.data.excerpt = excerpt;
  };
}

/**
 * Create a configured unified processor
 */
export function createMarkdownProcessor() {
  return unified()
    // Parse markdown to MDAST
    .use(remarkParse)

    // Remark plugins (MDAST transformations)
    .use(remarkMath)
    .use(remarkReadingTime)
    .use(remarkExcerpt)
    .use(remarkGithubAdmonitionsToDirectives)
    .use(remarkDirective)
    .use(parseDirectiveNode)

    // Convert MDAST to HAST
    .use(remarkRehype, {
      allowDangerousHtml: true,
      handlers: {
        // Custom handlers for directives
        note: (h: any, node: any) => AdmonitionComponent(node.attributes, node.children, 'note'),
        tip: (h: any, node: any) => AdmonitionComponent(node.attributes, node.children, 'tip'),
        important: (h: any, node: any) => AdmonitionComponent(node.attributes, node.children, 'important'),
        warning: (h: any, node: any) => AdmonitionComponent(node.attributes, node.children, 'warning'),
        caution: (h: any, node: any) => AdmonitionComponent(node.attributes, node.children, 'caution'),
        github: (h: any, node: any) => GithubCardComponent(node.attributes, node.children),
      },
    })

    // Rehype plugins (HAST transformations)
    .use(rehypeKatex)
    .use(rehypeSlug)
    .use(rehypeAutolinkHeadings, {
      behavior: 'append',
      properties: { className: ['anchor'] },
      content: {
        type: 'element',
        tagName: 'span',
        properties: { className: ['anchor-icon'] },
        children: [{ type: 'text', value: '#' }],
      },
    })

    // Stringify to HTML
    .use(rehypeStringify, { allowDangerousHtml: true });
}

/**
 * Process markdown content to HTML
 */
export async function processMarkdown(content: string) {
  const processor = createMarkdownProcessor();
  const file = await processor.process(content);

  return {
    html: String(file),
    readingTime: file.data.readingTime as { minutes: number; words: number },
    excerpt: file.data.excerpt as string,
  };
}

/**
 * Vite plugin for markdown transformation
 */
export function viteMarkdownPlugin() {
  return {
    name: 'vite-plugin-fuwari-md',
    async transform(code: string, id: string) {
      if (!id.endsWith('.md')) return;

      const { html, readingTime, excerpt } = await processMarkdown(code);

      return {
        code: `
          export const html = ${JSON.stringify(html)};
          export const readingTime = ${JSON.stringify(readingTime)};
          export const excerpt = ${JSON.stringify(excerpt)};
          export default html;
        `,
        map: null,
      };
    },
  };
}

/**
 * Vite configuration
 */
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [viteMarkdownPlugin()],
});

/**
 * Usage in your app:
 *
 * ```ts
 * import content, { readingTime, excerpt } from './post.md';
 *
 * document.getElementById('article').innerHTML = content;
 * document.getElementById('reading-time').textContent = `${readingTime.minutes} min read`;
 * ```
 */

/**
 * Required dependencies:
 *
 * npm install unified remark-parse remark-math remark-directive
 * npm install remark-github-admonitions-to-directives remark-rehype
 * npm install rehype-katex rehype-slug rehype-autolink-headings rehype-stringify
 * npm install hastscript unist-util-visit mdast-util-to-string reading-time
 */
