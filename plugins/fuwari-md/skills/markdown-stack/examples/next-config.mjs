/**
 * Next.js configuration with Fuwari markdown stack (MDX).
 *
 * Usage:
 * 1. Install @next/mdx and dependencies
 * 2. Create mdx-components.tsx for custom elements
 * 3. Add required CSS imports
 */

import createMDX from '@next/mdx';
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import remarkGfm from 'remark-gfm';
import remarkGithubAdmonitionsToDirectives from 'remark-github-admonitions-to-directives';
import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';

// Custom plugins (copy and adapt from sources/)
// Note: Some plugins need modification for Next.js compatibility
// import { parseDirectiveNode } from './lib/plugins/remark-directive-rehype.js';

const withMDX = createMDX({
  extension: /\.mdx?$/,
  options: {
    remarkPlugins: [
      remarkGfm,
      remarkMath,
      remarkGithubAdmonitionsToDirectives,
      remarkDirective,
      // parseDirectiveNode, // Add after adapting for Next.js
    ],
    rehypePlugins: [
      rehypeKatex,
      rehypeSlug,
      [
        rehypeAutolinkHeadings,
        {
          behavior: 'wrap',
          properties: { className: ['anchor-link'] },
        },
      ],
    ],
  },
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ['js', 'jsx', 'mdx', 'ts', 'tsx'],
};

export default withMDX(nextConfig);

/**
 * Required dependencies:
 *
 * npm install @next/mdx @mdx-js/loader @mdx-js/react
 * npm install remark-math remark-directive remark-gfm
 * npm install remark-github-admonitions-to-directives
 * npm install rehype-katex rehype-slug rehype-autolink-headings
 * npm install hastscript unist-util-visit
 */

/**
 * mdx-components.tsx example:
 *
 * ```tsx
 * import type { MDXComponents } from 'mdx/types';
 *
 * function Admonition({ type, children }: { type: string; children: React.ReactNode }) {
 *   return (
 *     <blockquote className={`admonition bdm-${type}`}>
 *       <span className="bdm-title">{type.toUpperCase()}</span>
 *       {children}
 *     </blockquote>
 *   );
 * }
 *
 * function GithubCard({ repo }: { repo: string }) {
 *   // Implement GitHub card fetching with React hooks
 *   return <a href={`https://github.com/${repo}`}>{repo}</a>;
 * }
 *
 * export function useMDXComponents(components: MDXComponents): MDXComponents {
 *   return {
 *     ...components,
 *     note: (props) => <Admonition type="note" {...props} />,
 *     tip: (props) => <Admonition type="tip" {...props} />,
 *     important: (props) => <Admonition type="important" {...props} />,
 *     warning: (props) => <Admonition type="warning" {...props} />,
 *     caution: (props) => <Admonition type="caution" {...props} />,
 *     github: GithubCard,
 *   };
 * }
 * ```
 */

/**
 * Add to your layout or _app:
 *
 * ```tsx
 * import 'katex/dist/katex.min.css';
 * import './styles/admonitions.css';
 * import './styles/github-card.css';
 * ```
 */
