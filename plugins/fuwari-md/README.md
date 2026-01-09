# fuwari-md

Fuwari's production-ready markdown processing stack for any framework. Includes admonitions, math equations, GitHub repository cards, enhanced code blocks, reading time, and more.

## Features

- **Admonitions/Callouts** - `:::note`, `:::tip`, `:::warning`, etc. + GitHub-style `> [!NOTE]`
- **Math Equations** - KaTeX rendering with `$inline$` and `$$display$$` syntax
- **GitHub Repository Cards** - `::github{repo="owner/repo"}` with live API data
- **Enhanced Code Blocks** - Line numbers, copy button, language badges, collapsible sections
- **Reading Time** - Automatic calculation injected into frontmatter
- **Excerpt Extraction** - First paragraph as excerpt for SEO
- **Auto-linking Headings** - Anchor links for easy navigation

## Installation

```bash
# Add to your Claude Code plugins
/plugin marketplace add Linaqruf/cc-plugins
```

## Commands

### `/fuwari-md:syntax [feature]`

Quick reference for markdown syntax.

```bash
/fuwari-md:syntax              # Full reference
/fuwari-md:syntax admonitions  # Admonitions only
/fuwari-md:syntax math         # Math equations only
/fuwari-md:syntax code         # Code blocks only
```

### `/fuwari-md:setup [framework]`

Interactive setup generator for your project.

```bash
/fuwari-md:setup         # Auto-detect framework
/fuwari-md:setup astro   # Astro configuration
/fuwari-md:setup nextjs  # Next.js MDX configuration
/fuwari-md:setup vite    # Generic Vite/unified
```

Generates:
- Framework config file
- Custom plugin files
- Base CSS styles
- Example markdown file

### `/fuwari-md:component <type>`

Generate custom remark/rehype plugins.

```bash
/fuwari-md:component directive  # Container directive (:::name)
/fuwari-md:component leaf       # Leaf directive (::name{})
/fuwari-md:component inline     # Text directive (:name[])
```

## Agent

### markdown-architect

Proactively helps with:
- Designing markdown processing pipelines
- Debugging rendering issues
- Optimizing plugin configurations
- Creating custom directives

Triggers when you discuss remark, rehype, unified, or markdown processing problems.

## Skill

The `markdown-stack` skill provides comprehensive documentation and source code references. It activates when you ask about:

- "How do I set up admonitions?"
- "Configure remark plugins"
- "Add math equations to my blog"
- "GitHub cards in markdown"

## Quick Syntax Reference

| Feature | Syntax |
|---------|--------|
| Note | `:::note[Title]` ... `:::` |
| Tip | `:::tip` ... `:::` |
| Warning | `:::warning` ... `:::` |
| GitHub Note | `> [!NOTE]` |
| Inline Math | `$E = mc^2$` |
| Display Math | `$$\int_0^\infty$$` |
| GitHub Card | `::github{repo="owner/repo"}` |
| Spoiler | `:spoiler[hidden text]` |

## Source Files

The plugin includes Fuwari's actual source code in `skills/markdown-stack/sources/`:

- `remark-directive-rehype.js` - Directive to HAST conversion
- `remark-reading-time.mjs` - Reading time calculation
- `remark-excerpt.js` - Excerpt extraction
- `rehype-component-admonition.mjs` - Admonition rendering
- `rehype-component-github-card.mjs` - GitHub card rendering
- `expressive-code-plugins.ts` - Custom copy button & language badge

## Framework Support

| Framework | Support Level |
|-----------|---------------|
| Astro | Full (native) |
| Next.js | Full (MDX) |
| Vite | Full (unified) |
| SvelteKit | Partial (mdsvex) |
| Docusaurus | Partial (built-in admonitions) |

## Dependencies

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
  "reading-time": "^1.5.0",
  "astro-expressive-code": "^0.35.0"
}
```

## Credits

Based on the markdown processing stack from [Fuwari](https://github.com/saicaca/fuwari), an Astro blog theme.

## License

MIT
