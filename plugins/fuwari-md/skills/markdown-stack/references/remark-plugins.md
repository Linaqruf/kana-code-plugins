# Remark Plugins Reference

## Plugin Order

The order of remark plugins matters. Use this sequence:

```javascript
remarkPlugins: [
  remarkMath,                              // 1. Parse LaTeX math notation
  remarkReadingTime,                       // 2. Calculate reading time (needs raw text)
  remarkExcerpt,                           // 3. Extract first paragraph
  remarkGithubAdmonitionsToDirectives,     // 4. Convert GitHub syntax BEFORE directive parsing
  remarkDirective,                         // 5. Parse directive syntax
  remarkSectionize,                        // 6. Wrap headings in sections
  parseDirectiveNode,                      // 7. Convert directives to HAST (LAST)
]
```

---

## remark-math

Parses LaTeX math notation into special AST nodes.

**Installation:**
```bash
npm install remark-math
```

**Usage:**
```javascript
import remarkMath from 'remark-math';

// In unified pipeline:
.use(remarkMath)
```

**Syntax:**
```markdown
Inline math: $E = mc^2$

Display math:
$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$
```

**Notes:**
- Pairs with `rehype-katex` for rendering
- Must come before other plugins that might interfere with `$` parsing

---

## remark-directive

Enables custom directive syntax for extending markdown.

**Installation:**
```bash
npm install remark-directive
```

**Usage:**
```javascript
import remarkDirective from 'remark-directive';

// In unified pipeline:
.use(remarkDirective)
```

**Directive Types:**

1. **Container Directive** (block-level):
```markdown
:::note[Title]
Content here
:::
```

2. **Leaf Directive** (self-closing block):
```markdown
::github{repo="owner/repo"}
```

3. **Text Directive** (inline):
```markdown
This has a :spoiler[hidden text] inline.
```

**Notes:**
- Directives need handlers to become HTML (use `parseDirectiveNode` + `rehype-components`)
- Attributes use `{key="value"}` syntax

---

## remark-github-admonitions-to-directives

Converts GitHub-style admonitions to directive syntax.

**Installation:**
```bash
npm install remark-github-admonitions-to-directives
```

**Usage:**
```javascript
import remarkGithubAdmonitionsToDirectives from 'remark-github-admonitions-to-directives';

// In unified pipeline - BEFORE remarkDirective:
.use(remarkGithubAdmonitionsToDirectives)
.use(remarkDirective)
```

**Converts:**
```markdown
> [!NOTE]
> This is a note

> [!WARNING]
> This is a warning
```

**To:**
```markdown
:::note
This is a note
:::

:::warning
This is a warning
:::
```

**Supported types:** NOTE, TIP, IMPORTANT, WARNING, CAUTION

---

## remark-sectionize

Wraps heading blocks in semantic `<section>` elements.

**Installation:**
```bash
npm install remark-sectionize
```

**Usage:**
```javascript
import remarkSectionize from 'remark-sectionize';

// In unified pipeline:
.use(remarkSectionize)
```

**Before:**
```html
<h2>Section Title</h2>
<p>Content...</p>
<h2>Next Section</h2>
```

**After:**
```html
<section>
  <h2>Section Title</h2>
  <p>Content...</p>
</section>
<section>
  <h2>Next Section</h2>
</section>
```

---

## parseDirectiveNode (Custom)

Converts directive AST nodes to HAST for rendering.

**Source:** `sources/remark-directive-rehype.js`

**Usage:**
```javascript
import { parseDirectiveNode } from './remark-directive-rehype.js';

// In unified pipeline - AFTER remarkDirective:
.use(remarkDirective)
.use(parseDirectiveNode)
```

**How it works:**
1. Visits all directive nodes (container, leaf, text)
2. Extracts directive labels (custom titles)
3. Converts to HAST using `hastscript`
4. Sets `hName` and `hProperties` for rehype to process

**Important:** This plugin must run AFTER `remarkDirective` and prepares nodes for `rehype-components`.

---

## remarkReadingTime (Custom)

Calculates reading time and injects into frontmatter.

**Source:** `sources/remark-reading-time.mjs`

**Dependencies:**
```bash
npm install reading-time mdast-util-to-string
```

**Usage:**
```javascript
import { remarkReadingTime } from './remark-reading-time.mjs';

// In unified pipeline:
.use(remarkReadingTime)
```

**Injects:**
```javascript
frontmatter.minutes  // Reading time in minutes (minimum 1)
frontmatter.words    // Word count
```

**Access in Astro:**
```astro
---
const { minutes, words } = Astro.props.frontmatter;
---
<span>{minutes} min read</span>
```

---

## remarkExcerpt (Custom)

Extracts the first paragraph as an excerpt.

**Source:** `sources/remark-excerpt.js`

**Dependencies:**
```bash
npm install mdast-util-to-string
```

**Usage:**
```javascript
import { remarkExcerpt } from './remark-excerpt.js';

// In unified pipeline:
.use(remarkExcerpt)
```

**Injects:**
```javascript
frontmatter.excerpt  // Text content of first paragraph
```

**Access in Astro:**
```astro
---
const { excerpt } = Astro.props.frontmatter;
---
<meta name="description" content={excerpt} />
```

---

## Complete Remark Configuration

```javascript
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import remarkGithubAdmonitionsToDirectives from 'remark-github-admonitions-to-directives';
import remarkSectionize from 'remark-sectionize';
import { remarkReadingTime } from './plugins/remark-reading-time.mjs';
import { remarkExcerpt } from './plugins/remark-excerpt.js';
import { parseDirectiveNode } from './plugins/remark-directive-rehype.js';

export const remarkPlugins = [
  remarkMath,
  remarkReadingTime,
  remarkExcerpt,
  remarkGithubAdmonitionsToDirectives,
  remarkDirective,
  remarkSectionize,
  parseDirectiveNode,
];
```
