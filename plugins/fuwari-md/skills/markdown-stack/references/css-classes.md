# CSS Classes Reference

Complete reference of CSS classes used by Fuwari's markdown rendering system.

## Container Classes

### `.custom-md`

Main wrapper class for markdown content. Apply to your article container.

```html
<article class="custom-md prose">
  <!-- Rendered markdown here -->
</article>
```

### `.prose`

Tailwind Typography class for base markdown styling. Combine with `.custom-md`:

```html
<article class="custom-md prose dark:prose-invert">
```

---

## Heading Classes

### `.anchor`

Anchor link appended to headings by `rehype-autolink-headings`.

```css
.custom-md .anchor {
  opacity: 0;
  transition: opacity 0.2s;
  margin-left: 0.2ch;
  padding: 0.5rem;
  text-decoration: none;
}

.custom-md h1:hover .anchor,
.custom-md h2:hover .anchor,
.custom-md h3:hover .anchor {
  opacity: 1;
}
```

### `.anchor-icon`

The `#` symbol inside anchor links.

```css
.anchor-icon {
  margin: 0 0.45ch;
}
```

---

## Admonition Classes

### `.admonition`

Base class for all admonition types.

```css
.admonition {
  /* Applied by rehype-component-admonition */
}
```

### `.bdm-{type}`

Type-specific classes:
- `.bdm-note` - Blue, informational
- `.bdm-tip` - Green, helpful hints
- `.bdm-important` - Purple, key information
- `.bdm-warning` - Orange, cautions
- `.bdm-caution` - Red, dangers

```css
.bdm-note {
  /* Uses --admonitions-color-note */
}

.bdm-tip {
  /* Uses --admonitions-color-tip */
}
```

### `.bdm-title`

Title/header element within admonitions.

```css
.bdm-title {
  display: flex;
  align-items: center;
  margin-bottom: -0.9rem;
  font-weight: bold;
}

/* Icon before title */
.bdm-title::before {
  content: ' ';
  display: inline-block;
  height: 1em;
  width: 1em;
  margin-right: 0.6rem;
  mask-size: contain;
  mask-position: center;
  mask-repeat: no-repeat;
}
```

---

## Code Block Classes

### `.expressive-code`

Container for Expressive Code blocks.

```css
.custom-md .expressive-code {
  margin: 1rem 0;
}
```

### `.frame`

Code block frame (includes title bar if present).

```css
.frame:hover .copy-btn {
  opacity: 1;
}
```

### `.copy-btn`

Copy button element.

```css
.copy-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 2rem;
  height: 2rem;
  opacity: 0;
  transition: opacity 0.2s;
  cursor: pointer;
}
```

### `.copy-btn-icon`

Icon wrapper inside copy button.

```css
.copy-btn-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1rem;
  height: 1rem;
}
```

### `.copy-icon` / `.success-icon`

SVG icons for copy states.

```css
.copy-btn .copy-icon {
  opacity: 1;
}
.copy-btn.success .copy-icon {
  opacity: 0;
}
.copy-btn .success-icon {
  opacity: 0;
}
.copy-btn.success .success-icon {
  opacity: 1;
}
```

### `[data-language]`

Attribute for language badge styling.

```css
[data-language]::before {
  content: attr(data-language);
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 0.75rem;
  text-transform: uppercase;
}
```

---

## GitHub Card Classes

### `.card-github`

Main GitHub card container.

```css
a.card-github {
  display: block;
  background: var(--license-block-bg);
  padding: 1.1rem 1.5rem;
  border-radius: var(--radius-large);
  text-decoration: none;
  transition: all 0.15s;
}

a.card-github:hover {
  background-color: var(--btn-regular-bg-hover);
}

a.card-github:active {
  transform: scale(0.98);
}
```

### `.gc-titlebar`

Title bar with owner/repo name.

```css
.gc-titlebar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
}
```

### `.gc-titlebar-left`

Left section of title bar.

```css
.gc-titlebar-left {
  display: flex;
  flex-flow: row nowrap;
  gap: 0.5rem;
}
```

### `.gc-owner`

Repository owner section.

```css
.gc-owner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 300;
}
```

### `.gc-avatar`

Owner avatar circle.

```css
.gc-avatar {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background-color: var(--primary);
  background-size: cover;
}
```

### `.gc-repo`

Repository name.

```css
.gc-repo {
  font-weight: bold;
}
```

### `.gc-description`

Repository description.

```css
.gc-description {
  margin-bottom: 0.7rem;
  font-size: 1rem;
  font-weight: 300;
  line-height: 1.5rem;
}
```

### `.gc-infobar`

Stats bar (stars, forks, license).

```css
.gc-infobar {
  display: flex;
  flex-flow: row nowrap;
  gap: 1.5rem;
  width: fit-content;
}
```

### `.gc-stars` / `.gc-forks` / `.gc-license`

Individual stat items with icons.

```css
.gc-stars,
.gc-forks,
.gc-license {
  font-weight: 500;
  font-size: 0.875rem;
}

.gc-stars::before,
.gc-forks::before,
.gc-license::before {
  content: ' ';
  display: inline-block;
  height: 1.3em;
  width: 1.3em;
  margin-right: 0.4rem;
  vertical-align: -0.24em;
  mask-size: contain;
  /* SVG mask-image for icon */
}
```

### `.gc-language`

Repository language (hidden by default).

```css
.gc-language {
  display: none;
}
```

### `.github-logo`

GitHub logo in title bar.

```css
.github-logo {
  font-size: 1.25rem;
}

.github-logo::before {
  /* GitHub SVG icon */
}
```

### `.fetch-waiting`

Loading state for GitHub cards.

```css
a.card-github.fetch-waiting {
  pointer-events: none;
  opacity: 0.7;
}

.fetch-waiting .gc-description,
.fetch-waiting .gc-infobar,
.fetch-waiting .gc-avatar {
  background-color: var(--tw-prose-body);
  color: transparent;
  animation: pulsate 2s infinite linear;
}

@keyframes pulsate {
  0% { opacity: 0.15; }
  50% { opacity: 0.25; }
  100% { opacity: 0.15; }
}
```

### `.fetch-error`

Error state for failed API calls.

```css
a.card-github.fetch-error {
  pointer-events: all;
  opacity: 1;
}
```

---

## Spoiler Classes

### `spoiler` (element)

Inline spoiler element. Uses a custom HTML element.

```css
.custom-md spoiler {
  background: var(--codeblock-bg);
  padding: 0.125rem 0.25rem;
  border-radius: 0.375rem;
  overflow: hidden;
  transition: all 0.15s;
}

.custom-md spoiler:hover {
  background: transparent;
}

/* Hide content when not hovered */
.custom-md spoiler:not(:hover) {
  color: var(--codeblock-bg);
}

.custom-md spoiler:not(:hover) * {
  color: var(--codeblock-bg);
}
```

---

## Link Classes

### `.no-styling`

Exclude links from markdown styling.

```css
.custom-md a:not(.no-styling) {
  /* Link styles */
  color: var(--primary);
  text-decoration: underline;
  text-decoration-style: dashed;
}

.custom-md a.no-styling {
  /* No special styling */
}
```

---

## Math Classes

### `.katex-display-container`

Container for display math equations.

```css
.katex-display-container {
  max-width: 100%;
  overflow-x: auto;
  margin: 1em 0;
}
```

---

## TOC Classes

### `.visible`

Active/visible state for TOC entries.

```css
.toc-entry.visible {
  /* Highlighted styling */
}
```

### `#active-indicator`

Moving indicator showing current section.

```css
#active-indicator {
  position: absolute;
  left: 0;
  right: 0;
  border-radius: 0.75rem;
  background: var(--toc-btn-hover);
  border: 2px dashed var(--toc-btn-hover);
  z-index: -1;
  transition: all 0.3s;
}
```

---

## Utility Classes

### List Markers

```css
.custom-md ul li::marker,
.custom-md ol li::marker {
  color: var(--primary);
}
```

### Blockquotes

```css
.custom-md blockquote {
  border-left: none;
  font-style: normal;
}

.custom-md blockquote::before {
  content: '';
  position: absolute;
  left: -0.25rem;
  width: 0.25rem;
  height: 100%;
  background: var(--btn-regular-bg);
  border-radius: 9999px;
}
```

### Inline Code

```css
.custom-md code {
  background: var(--inline-code-bg);
  color: var(--inline-code-color);
  padding: 0.125rem 0.25rem;
  border-radius: 0.375rem;
  font-family: 'JetBrains Mono', monospace;
}

/* Remove default quotes */
.custom-md code::before,
.custom-md code::after {
  content: none;
}
```

### Images

```css
.custom-md img {
  border-radius: 0.75rem;
  cursor: zoom-in; /* If using PhotoSwipe */
}
```

### Horizontal Rules

```css
.custom-md hr {
  border-color: var(--line-divider);
  border-style: dashed;
}
```

### iframes

```css
.custom-md iframe {
  border-radius: 0.75rem;
  margin-left: auto;
  margin-right: auto;
  max-width: 100%;
}
```

---

## Complete Stylesheet Template

```css
/* markdown.css - Core styling */

.custom-md {
  /* Headings */
  h1, h2, h3, h4, h5, h6 {
    .anchor {
      opacity: 0;
      transition: opacity 0.2s;
    }
    &:hover .anchor {
      opacity: 1;
    }
  }

  /* Links */
  a:not(.no-styling) {
    color: var(--primary);
    text-decoration: underline dashed;
    text-underline-offset: 4px;
  }

  /* Code */
  code {
    background: var(--inline-code-bg);
    color: var(--inline-code-color);
    padding: 0.125rem 0.25rem;
    border-radius: 0.375rem;
  }

  /* Code blocks */
  .expressive-code {
    margin: 1rem 0;
  }

  .copy-btn {
    opacity: 0;
  }
  .frame:hover .copy-btn {
    opacity: 1;
  }

  /* Lists */
  ul, ol {
    li::marker {
      color: var(--primary);
    }
  }

  /* Blockquotes */
  blockquote {
    position: relative;
    &::before {
      content: '';
      position: absolute;
      left: -0.25rem;
      width: 0.25rem;
      height: 100%;
      background: var(--btn-regular-bg);
      border-radius: 9999px;
    }
  }

  /* Images */
  img {
    border-radius: 0.75rem;
  }

  /* Math */
  .katex-display-container {
    overflow-x: auto;
  }
}
```
