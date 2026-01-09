/**
 * Remark plugin to parse directive nodes and convert them to HAST.
 * Works with remark-directive to handle container, leaf, and text directives.
 *
 * @example
 * ```js
 * import { parseDirectiveNode } from './remark-directive-rehype.js';
 *
 * // In your unified pipeline:
 * .use(remarkDirective)
 * .use(parseDirectiveNode)
 * ```
 *
 * @see https://github.com/remarkjs/remark-directive
 */
import { h } from "hastscript";
import { visit } from "unist-util-visit";

export function parseDirectiveNode() {
	return (tree, { _data }) => {
		visit(tree, (node) => {
			if (
				node.type === "containerDirective" ||
				node.type === "leafDirective" ||
				node.type === "textDirective"
			) {
				// biome-ignore lint/suspicious/noAssignInExpressions: <check later>
				const data = node.data || (node.data = {});
				node.attributes = node.attributes || {};
				if (
					node.children.length > 0 &&
					node.children[0].data &&
					node.children[0].data.directiveLabel
				) {
					// Add a flag to the node to indicate that it has a directive label
					node.attributes["has-directive-label"] = true;
				}
				const hast = h(node.name, node.attributes);

				data.hName = hast.tagName;
				data.hProperties = hast.properties;
			}
		});
	};
}
