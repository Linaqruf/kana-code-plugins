/**
 * Rehype component for rendering admonitions (callouts).
 * Supports: note, tip, important, caution, warning
 *
 * @example
 * ```js
 * import { AdmonitionComponent } from './rehype-component-admonition.mjs';
 * import rehypeComponents from 'rehype-components';
 *
 * // In your unified pipeline:
 * .use(rehypeComponents, {
 *   components: {
 *     note: (x, y) => AdmonitionComponent(x, y, "note"),
 *     tip: (x, y) => AdmonitionComponent(x, y, "tip"),
 *     important: (x, y) => AdmonitionComponent(x, y, "important"),
 *     caution: (x, y) => AdmonitionComponent(x, y, "caution"),
 *     warning: (x, y) => AdmonitionComponent(x, y, "warning"),
 *   }
 * })
 * ```
 *
 * Markdown syntax:
 * ```md
 * :::note[Custom Title]
 * Your content here
 * :::
 *
 * Or GitHub-style:
 * > [!NOTE]
 * > Your content here
 * ```
 */
/// <reference types="mdast" />
import { h } from "hastscript";

/**
 * Creates an admonition component.
 *
 * @param {Object} properties - The properties of the component.
 * @param {string} [properties.title] - An optional title.
 * @param {('tip'|'note'|'important'|'caution'|'warning')} type - The admonition type.
 * @param {import('mdast').RootContent[]} children - The children elements of the component.
 * @returns {import('mdast').Parent} The created admonition component.
 */
export function AdmonitionComponent(properties, children, type) {
	if (!Array.isArray(children) || children.length === 0)
		return h(
			"div",
			{ class: "hidden" },
			'Invalid admonition directive. (Admonition directives must be of block type ":::note{name="name"} <content> :::")',
		);

	let label = null;
	if (properties?.["has-directive-label"]) {
		label = children[0]; // The first child is the label
		// biome-ignore lint/style/noParameterAssign: <check later>
		children = children.slice(1);
		label.tagName = "div"; // Change the tag <p> to <div>
	}

	return h("blockquote", { class: `admonition bdm-${type}` }, [
		h("span", { class: "bdm-title" }, label ? label : type.toUpperCase()),
		...children,
	]);
}
