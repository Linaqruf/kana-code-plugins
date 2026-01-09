---
name: syntax
description: Quick reference for Fuwari markdown syntax - admonitions, math, GitHub cards, code blocks
argument-hint: "[feature]"
allowed-tools:
  - Read
version: 1.0.0
---

# Markdown Syntax Reference

Display the syntax reference for Fuwari's markdown extensions.

## Instructions

When the user runs `/fuwari-md:syntax`:

1. If a feature argument is provided (e.g., `/syntax admonitions`), show only that feature's syntax
2. If no argument, show the complete quick reference

## Feature Detection

Match these keywords to features:
- `admonitions`, `callouts`, `note`, `tip`, `warning` → Admonitions section
- `math`, `latex`, `katex`, `equations` → Math section
- `github`, `card`, `repo` → GitHub Cards section
- `code`, `codeblock`, `highlight` → Code Blocks section
- `spoiler`, `hidden` → Spoilers section
- `all` or no argument → Full reference

## Quick Reference Output

### Full Reference (default)

```
# Fuwari Markdown Syntax Reference

## Admonitions (Callouts)

Directive syntax:
:::note[Custom Title]
Content here
:::

Types: note, tip, important, warning, caution

GitHub syntax (auto-converted):
> [!NOTE]
> Content here

Types: NOTE, TIP, IMPORTANT, WARNING, CAUTION


## Math Equations

Inline math:
$E = mc^2$

Display math:
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$


## GitHub Repository Cards

::github{repo="owner/repo"}

Example:
::github{repo="withastro/astro"}


## Code Blocks

Basic:
```javascript
const x = 1;
```

With title:
```js title="config.js"
export default {};
```

With line highlighting:
```js {2,4-6}
const a = 1;
const b = 2;  // highlighted
```

With line numbers disabled:
```bash showLineNumbers=false
npm install
```


## Spoilers (Inline)

:spoiler[This text is hidden until clicked]


## Heading Anchors

Headings automatically get IDs and anchor links.
## My Heading → <h2 id="my-heading">My Heading <a href="#my-heading">#</a></h2>
```

### Admonitions Only

```
# Admonitions Syntax

## Directive Syntax

:::note
Default note without custom title
:::

:::note[Custom Title]
Note with a custom title
:::

:::tip[Pro Tip]
Helpful tip content
:::

:::important
Important information
:::

:::warning
Warning message
:::

:::caution
Caution - be careful!
:::


## GitHub-Style Syntax (Auto-Converted)

> [!NOTE]
> This is a note

> [!TIP]
> This is a tip

> [!IMPORTANT]
> This is important

> [!WARNING]
> This is a warning

> [!CAUTION]
> This requires caution


## Supported Types

| Type      | Use Case                           |
|-----------|-------------------------------------|
| note      | General information                 |
| tip       | Helpful suggestions                 |
| important | Key information to highlight        |
| warning   | Potential issues to be aware of     |
| caution   | Dangerous or critical warnings      |
```

### Math Only

```
# Math Syntax (KaTeX)

## Inline Math

Use single dollar signs for inline math:
The formula $E = mc^2$ changed physics.

## Display Math

Use double dollar signs for block equations:
$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$

## Common Examples

Fractions: $\frac{a}{b}$

Square root: $\sqrt{x}$, $\sqrt[n]{x}$

Subscript/superscript: $x_i^2$

Greek letters: $\alpha, \beta, \gamma, \delta$

Integrals: $\int_a^b f(x) dx$

Limits: $\lim_{x \to \infty} f(x)$

Matrices:
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$

## Tips

- Escape special characters with backslash
- Use \text{} for text within math
- For multiline equations, use aligned environment
```

### GitHub Cards Only

```
# GitHub Card Syntax

## Basic Usage

::github{repo="owner/repo"}

## Examples

::github{repo="withastro/astro"}
::github{repo="facebook/react"}
::github{repo="vuejs/vue"}

## How It Works

1. The card renders with placeholder content
2. JavaScript fetches data from GitHub API
3. Card updates with: description, stars, forks, language, license

## Styling Classes

- .card-github - Main container
- .gc-titlebar - Repository name and owner
- .gc-description - Repository description
- .gc-infobar - Stats (stars, forks, license, language)
- .fetch-waiting - Loading state
- .fetch-error - Error state
```

### Code Blocks Only

```
# Code Block Syntax (Expressive Code)

## Basic

```language
code here
```

## With Title

```js title="filename.js"
const x = 1;
```

## Line Highlighting

Highlight specific lines:
```js {2}
const a = 1;
const b = 2;  // This line highlighted
```

Highlight range:
```js {2-4}
// lines 2-4 highlighted
```

Multiple:
```js {1,3,5-7}
// lines 1, 3, 5, 6, 7 highlighted
```

## Diff Markers

```js
const a = 1;
const b = 2;  // [!code --]
const c = 3;  // [!code ++]
```

## Collapsible Sections

```js collapse={1-5}
// These lines collapsed by default
import { a } from 'a';
import { b } from 'b';
import { c } from 'c';
import { d } from 'd';

function main() {
  // Visible by default
}
```

## Line Numbers

Enabled by default. Disable per block:
```bash showLineNumbers=false
npm install
```

## Word Wrap

Enable word wrap for long lines:
```text wrap
This is a very long line that will wrap instead of scrolling horizontally.
```
```

## Response Format

Output the appropriate reference as formatted markdown. Use code blocks for syntax examples to ensure proper display.

## Error Handling

### Invalid Feature Argument

If the user provides an unrecognized feature argument:

1. List the valid feature keywords:
   - `admonitions`, `callouts`, `note`, `tip`, `warning`
   - `math`, `latex`, `katex`, `equations`
   - `github`, `card`, `repo`
   - `code`, `codeblock`, `highlight`
   - `spoiler`, `hidden`
   - `all` (or no argument for full reference)

2. Suggest the closest matching feature if possible

3. Offer to show the full reference instead

**Example response for invalid feature:**
```
I don't recognize the feature "tables".

Available features:
- admonitions (or: callouts, note, tip, warning)
- math (or: latex, katex, equations)
- github (or: card, repo)
- code (or: codeblock, highlight)
- spoiler (or: hidden)

Did you mean one of these? Or I can show the full reference.
```
