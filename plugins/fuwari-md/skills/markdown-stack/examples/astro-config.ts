/**
 * Complete Astro configuration with Fuwari markdown stack.
 *
 * Usage:
 * 1. Copy this file to your project root as `astro.config.mjs`
 * 2. Copy plugin files from `sources/` to `src/plugins/`
 * 3. Install dependencies (see package.json below)
 * 4. Add required CSS imports
 */

import { defineConfig } from 'astro/config';
import expressiveCode from 'astro-expressive-code';
import { pluginCollapsibleSections } from '@expressive-code/plugin-collapsible-sections';
import { pluginLineNumbers } from '@expressive-code/plugin-line-numbers';

// Remark plugins
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import remarkGithubAdmonitionsToDirectives from 'remark-github-admonitions-to-directives';
import remarkSectionize from 'remark-sectionize';

// Rehype plugins
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
  site: 'https://your-site.com',

  integrations: [
    // Expressive Code MUST come before other integrations that process markdown
    expressiveCode({
      themes: ['github-dark'],
      plugins: [
        pluginCollapsibleSections(),
        pluginLineNumbers(),
        pluginLanguageBadge(),
        pluginCustomCopyButton(),
      ],
      defaultProps: {
        wrap: true,
        overridesByLang: {
          'shellsession': { showLineNumbers: false },
          'bash': { showLineNumbers: false },
        },
      },
      styleOverrides: {
        codeBackground: 'var(--codeblock-bg, #1e1e1e)',
        borderRadius: '0.75rem',
        codeFontSize: '0.875rem',
        codeFontFamily: "'JetBrains Mono', monospace",
      },
      frames: {
        showCopyToClipboardButton: false, // Using custom copy button
      },
    }),
  ],

  markdown: {
    remarkPlugins: [
      // Order matters!
      remarkMath,                           // 1. Parse LaTeX math
      remarkReadingTime,                    // 2. Calculate reading time
      remarkExcerpt,                        // 3. Extract first paragraph
      remarkGithubAdmonitionsToDirectives,  // 4. Convert GitHub admonition syntax
      remarkDirective,                      // 5. Parse directive syntax
      remarkSectionize,                     // 6. Wrap headings in sections
      parseDirectiveNode,                   // 7. Convert directives to HAST
    ],
    rehypePlugins: [
      rehypeKatex,
      rehypeSlug,
      [
        rehypeComponents,
        {
          components: {
            github: GithubCardComponent,
            note: (props, children) => AdmonitionComponent(props, children, 'note'),
            tip: (props, children) => AdmonitionComponent(props, children, 'tip'),
            important: (props, children) => AdmonitionComponent(props, children, 'important'),
            caution: (props, children) => AdmonitionComponent(props, children, 'caution'),
            warning: (props, children) => AdmonitionComponent(props, children, 'warning'),
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
            properties: {
              className: ['anchor-icon'],
              'data-pagefind-ignore': true,
            },
            children: [{ type: 'text', value: '#' }],
          },
        },
      ],
    ],
  },
});

/**
 * Required dependencies (add to package.json):
 *
 * {
 *   "dependencies": {
 *     "astro": "^5.0.0",
 *     "astro-expressive-code": "^0.35.0",
 *     "@expressive-code/plugin-collapsible-sections": "^0.35.0",
 *     "@expressive-code/plugin-line-numbers": "^0.35.0",
 *     "remark-math": "^6.0.0",
 *     "remark-directive": "^3.0.0",
 *     "remark-github-admonitions-to-directives": "^2.0.0",
 *     "remark-sectionize": "^2.0.0",
 *     "rehype-katex": "^7.0.0",
 *     "rehype-slug": "^6.0.0",
 *     "rehype-autolink-headings": "^7.0.0",
 *     "rehype-components": "^0.3.0",
 *     "hastscript": "^9.0.0",
 *     "unist-util-visit": "^5.0.0",
 *     "mdast-util-to-string": "^4.0.0",
 *     "reading-time": "^1.5.0"
 *   }
 * }
 */
