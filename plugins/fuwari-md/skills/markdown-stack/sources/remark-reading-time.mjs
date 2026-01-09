/**
 * Remark plugin to calculate reading time from markdown content.
 * Injects `minutes` and `words` into frontmatter.
 *
 * @example
 * ```js
 * import { remarkReadingTime } from './remark-reading-time.mjs';
 *
 * // In your Astro config:
 * markdown: {
 *   remarkPlugins: [remarkReadingTime]
 * }
 *
 * // Access in your template:
 * const { minutes, words } = Astro.props.frontmatter;
 * ```
 *
 * @requires reading-time
 */
// biome-ignore lint/suspicious/noShadowRestrictedNames: <toString from mdast-util-to-string>
import { toString } from "mdast-util-to-string";
import getReadingTime from "reading-time";

export function remarkReadingTime() {
	return (tree, { data }) => {
		const textOnPage = toString(tree);
		const readingTime = getReadingTime(textOnPage);
		data.astro.frontmatter.minutes = Math.max(
			1,
			Math.round(readingTime.minutes),
		);
		data.astro.frontmatter.words = readingTime.words;
	};
}
