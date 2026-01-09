---
description: Use this skill when the user asks about "markdown setup", "remark plugins", "rehype configuration", "admonitions", "callouts", "code highlighting", "math equations", "KaTeX", "GitHub cards", "expressive code", "unified ecosystem", "markdown processing pipeline", or wants to set up advanced markdown features for their blog or documentation site.
version: 1.0.0
---

# Fuwari Markdown Stack

Provide comprehensive guidance for implementing Fuwari's production-ready markdown processing pipeline in any framework. This stack includes admonitions, math equations, GitHub repository cards, enhanced code blocks, reading time calculation, and more.

## Processing Pipeline Overview

The markdown processing flows through these stages:

```
Markdown Source
    ↓
[Remark Plugins] - Parse and transform MDAST
├── remark-math          → Parse LaTeX notation
├── remark-reading-time  → Calculate reading time
├── remark-excerpt       → Extract first paragraph
├── remark-github-admonitions-to-directives → Convert GitHub syntax
├── remark-directive     → Parse directive syntax
├── remark-sectionize    → Wrap headings in sections
└── parseDirectiveNode   → Convert directives to HAST
    ↓
[Rehype Plugins] - Transform and render HAST
├── rehype-katex         → Render math equations
├── rehype-slug          → Add IDs to headings
├── rehype-components    → Render custom components
└── rehype-autolink-headings → Add anchor links
    ↓
[Expressive Code] - Enhanced code blocks
├── pluginLineNumbers
├── pluginCollapsibleSections
├── pluginLanguageBadge
└── pluginCustomCopyButton
    ↓
HTML Output
```

## Quick Feature Reference

| Feature | Syntax | Notes |
|---------|--------|-------|
| **Admonitions** | `:::note[Title]` ... `:::` | Types: note, tip, important, warning, caution |
| **GitHub Admonitions** | `> [!NOTE]` | Converted to directive syntax |
| **Math (inline)** | `$E = mc^2$` | KaTeX rendering |
| **Math (display)** | `$$\int_0^\infty$$` | Block-level equations |
| **GitHub Cards** | `::github{repo="owner/repo"}` | Fetches repo info via API |
| **Spoilers** | `:spoiler[hidden text]` | Click to reveal |
| **Code Blocks** | ` ```lang ` | Line numbers, copy button, language badge |

## Core Dependencies

```json
{
  "remark-math": "^6.0.0",
  "remark-directive": "^3.0.0",
  "remark-github-admonitions-to-directives": "^2.0.0",
  "remark-sectionize": "^2.0.0",
  "rehype-katex": "^7.0.0",
  "rehype-slug": "^6.0.0",
  "rehype-autolink-headings": "^7.0.0",
  "rehype-components": "^0.3.0",
  "hastscript": "^9.0.0",
  "unist-util-visit": "^5.0.0",
  "mdast-util-to-string": "^4.0.0",
  "reading-time": "^1.5.0",
  "astro-expressive-code": "^0.35.0",
  "@expressive-code/plugin-collapsible-sections": "^0.35.0",
  "@expressive-code/plugin-line-numbers": "^0.35.0"
}
```

## Implementation by Feature

### Admonitions (Callouts)

Support both directive syntax and GitHub-style admonitions:

**Directive syntax:**
```markdown
:::note[Custom Title]
This is a note with a custom title.
:::

:::warning
This uses the default "WARNING" title.
:::
```

**GitHub syntax (auto-converted):**
```markdown
> [!NOTE]
> This is a GitHub-style note.

> [!TIP]
> Helpful tip here.
```

**Admonition types:** `note`, `tip`, `important`, `warning`, `caution`

See `references/remark-plugins.md` for plugin configuration.
See `sources/rehype-component-admonition.mjs` for component implementation.

### Math Equations

Use KaTeX for rendering LaTeX math:

**Inline math:**
```markdown
The equation $E = mc^2$ is famous.
```

**Display math:**
```markdown
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

Requires `remark-math` and `rehype-katex`. Include KaTeX CSS in your layout.

See `references/rehype-plugins.md` for KaTeX configuration.

### GitHub Repository Cards

Embed interactive GitHub repository cards:

```markdown
::github{repo="withastro/astro"}
```

This creates a card that fetches and displays:
- Repository description
- Star count
- Fork count
- Primary language
- License

See `sources/rehype-component-github-card.mjs` for implementation.

### Enhanced Code Blocks

Expressive Code provides:
- Syntax highlighting with customizable themes
- Line numbers (optional per block)
- Copy button with animated feedback
- Language badge
- Collapsible sections
- Word wrap support

See `references/expressive-code.md` for full configuration.
See `sources/expressive-code-plugins.ts` for custom plugins.

### Reading Time & Excerpt

Automatically calculate reading time and extract excerpt:

```javascript
// In your template (Astro example):
const { minutes, words, excerpt } = Astro.props.frontmatter;
```

See `sources/remark-reading-time.mjs` and `sources/remark-excerpt.js`.

## Framework Integration

For framework-specific configuration:
- **Astro**: See `examples/astro-config.ts`
- **Next.js (MDX)**: See `examples/next-config.mjs`
- **Vite/Generic**: See `examples/vite-config.ts`

See `references/framework-configs.md` for detailed integration guides.

## Custom Directive Development

To create your own directives:

1. Define directive syntax in markdown
2. Use `parseDirectiveNode` to convert to HAST
3. Create a rehype component handler
4. Register with `rehype-components`

See `sources/remark-directive-rehype.js` for the directive parser.

## Styling Requirements

Admonitions and GitHub cards require CSS. Key classes:
- `.admonition`, `.bdm-note`, `.bdm-tip`, etc.
- `.card-github`, `.gc-titlebar`, `.gc-description`, etc.

See `references/troubleshooting.md` for styling guidance.

## References

- `references/remark-plugins.md` - Detailed remark plugin documentation
- `references/rehype-plugins.md` - Detailed rehype plugin documentation
- `references/expressive-code.md` - Code block configuration
- `references/framework-configs.md` - Framework integration guides
- `references/troubleshooting.md` - Common issues and solutions
- `sources/` - Complete plugin source code from Fuwari
