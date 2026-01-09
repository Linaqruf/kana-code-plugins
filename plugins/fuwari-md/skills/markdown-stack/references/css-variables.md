# CSS Variables Reference

Fuwari uses CSS custom properties (variables) for theming. All colors use the oklch() color space with a configurable `--hue` value.

## Theme Configuration

Set the base hue in your CSS:

```css
:root {
  --hue: 250;  /* 0-360, changes entire color scheme */
}
```

## Core Variables

### Primary Colors

```css
:root {
  /* Primary accent color - used for links, highlights */
  --primary: oklch(0.70 0.14 var(--hue));

  /* Page background */
  --page-bg: oklch(0.95 0.01 var(--hue));

  /* Card/panel backgrounds */
  --card-bg: white;

  /* Deep text color */
  --deep-text: oklch(0.25 0.02 var(--hue));

  /* Active title color */
  --title-active: oklch(0.6 0.1 var(--hue));
}

/* Dark mode overrides */
:root.dark {
  --primary: oklch(0.75 0.14 var(--hue));
  --page-bg: oklch(0.16 0.014 var(--hue));
  --card-bg: oklch(0.23 0.015 var(--hue));
}
```

### Button Colors

```css
:root {
  /* Button text/icon color */
  --btn-content: oklch(0.55 0.12 var(--hue));

  /* Regular button states */
  --btn-regular-bg: oklch(0.95 0.025 var(--hue));
  --btn-regular-bg-hover: oklch(0.9 0.05 var(--hue));
  --btn-regular-bg-active: oklch(0.85 0.08 var(--hue));

  /* Plain/ghost button states */
  --btn-plain-bg-hover: oklch(0.95 0.025 var(--hue));
  --btn-plain-bg-active: oklch(0.98 0.01 var(--hue));

  /* Card button states */
  --btn-card-bg-hover: oklch(0.98 0.005 var(--hue));
  --btn-card-bg-active: oklch(0.9 0.03 var(--hue));
}

:root.dark {
  --btn-content: oklch(0.75 0.1 var(--hue));
  --btn-regular-bg: oklch(0.33 0.035 var(--hue));
  --btn-regular-bg-hover: oklch(0.38 0.04 var(--hue));
  --btn-regular-bg-active: oklch(0.43 0.045 var(--hue));
  --btn-plain-bg-hover: oklch(0.30 0.035 var(--hue));
  --btn-plain-bg-active: oklch(0.27 0.025 var(--hue));
  --btn-card-bg-hover: oklch(0.3 0.03 var(--hue));
  --btn-card-bg-active: oklch(0.35 0.035 var(--hue));
}
```

### Code Block Colors

```css
:root {
  /* Inline code */
  --inline-code-bg: var(--btn-regular-bg);
  --inline-code-color: var(--btn-content);

  /* Code block backgrounds */
  --codeblock-bg: oklch(0.17 0.015 var(--hue));
  --codeblock-topbar-bg: oklch(0.3 0.02 var(--hue));

  /* Selection in code blocks */
  --codeblock-selection: oklch(0.40 0.08 var(--hue));
}

:root.dark {
  --codeblock-bg: oklch(0.17 0.015 var(--hue));
  --codeblock-topbar-bg: oklch(0.12 0.015 var(--hue));
}
```

### Link Colors

```css
:root {
  /* Link underline (dashed) */
  --link-underline: oklch(0.93 0.04 var(--hue));

  /* Link hover underline */
  --link-hover: oklch(0.95 0.025 var(--hue));

  /* Link active state */
  --link-active: oklch(0.90 0.05 var(--hue));
}

:root.dark {
  --link-underline: oklch(0.40 0.08 var(--hue));
  --link-hover: oklch(0.40 0.08 var(--hue));
  --link-active: oklch(0.35 0.07 var(--hue));
}
```

### Admonition Colors

```css
:root {
  /* Tip - green/cyan (hue 180) */
  --admonitions-color-tip: oklch(0.7 0.14 180);

  /* Note - blue (hue 250) */
  --admonitions-color-note: oklch(0.7 0.14 250);

  /* Important - purple (hue 310) */
  --admonitions-color-important: oklch(0.7 0.14 310);

  /* Warning - orange (hue 60) */
  --admonitions-color-warning: oklch(0.7 0.14 60);

  /* Caution - red (hue 25) */
  --admonitions-color-caution: oklch(0.6 0.2 25);
}

:root.dark {
  --admonitions-color-tip: oklch(0.75 0.14 180);
  --admonitions-color-note: oklch(0.75 0.14 250);
  --admonitions-color-important: oklch(0.75 0.14 310);
  --admonitions-color-warning: oklch(0.75 0.14 60);
  --admonitions-color-caution: oklch(0.65 0.2 25);
}
```

### Table of Contents Colors

```css
:root {
  /* Badge background for numbered headings */
  --toc-badge-bg: oklch(0.89 0.050 var(--hue));

  /* Hover state */
  --toc-btn-hover: oklch(0.926 0.015 var(--hue));

  /* Active state */
  --toc-btn-active: oklch(0.90 0.015 var(--hue));

  /* Active item highlight */
  --toc-item-active: oklch(0.70 0.13 var(--hue));

  /* TOC width calculation */
  --toc-width: calc((100vw - var(--page-width)) / 2 - 1rem);
}

:root.dark {
  --toc-badge-bg: var(--btn-regular-bg);
  --toc-btn-hover: oklch(0.22 0.02 var(--hue));
  --toc-btn-active: oklch(0.25 0.02 var(--hue));
  --toc-item-active: oklch(0.35 0.07 var(--hue));
}
```

### Divider & Line Colors

```css
:root {
  /* Light divider lines */
  --line-divider: rgba(0, 0, 0, 0.08);

  /* General line color */
  --line-color: rgba(0, 0, 0, 0.1);

  /* Meta/separator dividers */
  --meta-divider: rgba(0, 0, 0, 0.2);
}

:root.dark {
  --line-divider: rgba(255, 255, 255, 0.08);
  --line-color: rgba(255, 255, 255, 0.1);
  --meta-divider: rgba(255, 255, 255, 0.2);
}
```

### Selection Colors

```css
:root {
  --selection-bg: oklch(0.90 0.05 var(--hue));
}

:root.dark {
  --selection-bg: oklch(0.40 0.08 var(--hue));
}
```

### Scrollbar Colors

```css
:root {
  --scrollbar-bg: rgba(0, 0, 0, 0.4);
  --scrollbar-bg-hover: rgba(0, 0, 0, 0.5);
  --scrollbar-bg-active: rgba(0, 0, 0, 0.6);
}

:root.dark {
  --scrollbar-bg: rgba(255, 255, 255, 0.4);
  --scrollbar-bg-hover: rgba(255, 255, 255, 0.5);
  --scrollbar-bg-active: rgba(255, 255, 255, 0.6);
}
```

### Miscellaneous

```css
:root {
  /* Border radius for large elements */
  --radius-large: 1rem;

  /* Content animation delay */
  --content-delay: 150ms;

  /* License/quote block background */
  --license-block-bg: rgba(0, 0, 0, 0.03);

  /* Float panel background */
  --float-panel-bg: white;
}

:root.dark {
  --license-block-bg: var(--codeblock-bg);
  --float-panel-bg: oklch(0.19 0.015 var(--hue));
}
```

## Using Variables

### In CSS

```css
.my-element {
  background: var(--card-bg);
  color: var(--primary);
  border: 1px solid var(--line-color);
}
```

### In Tailwind

```html
<div class="bg-[var(--card-bg)] text-[var(--primary)]">
  Content
</div>
```

### Dynamic Theming

Change the entire color scheme by updating `--hue`:

```javascript
// Set theme hue dynamically
document.documentElement.style.setProperty('--hue', '180'); // Cyan theme
document.documentElement.style.setProperty('--hue', '250'); // Blue theme
document.documentElement.style.setProperty('--hue', '330'); // Pink theme
```

## OKLCH Color Space

Fuwari uses oklch() for perceptually uniform colors:

```
oklch(lightness chroma hue)

- lightness: 0-1 (0 = black, 1 = white)
- chroma: 0-0.4 (0 = gray, higher = more saturated)
- hue: 0-360 (color wheel angle)
```

### Why OKLCH?

1. **Perceptual uniformity**: Same lightness values look equally bright
2. **Predictable saturation**: Chroma behaves consistently across hues
3. **Easy theming**: Change hue while maintaining contrast ratios
4. **Wide gamut**: Supports modern displays

## Complete Variables File

```css
/* Utility functions */
:root {
  --radius-large: 1rem;
  --content-delay: 150ms;
}

/* Light mode */
:root {
  --primary: oklch(0.70 0.14 var(--hue));
  --page-bg: oklch(0.95 0.01 var(--hue));
  --card-bg: white;
  --btn-content: oklch(0.55 0.12 var(--hue));
  --btn-regular-bg: oklch(0.95 0.025 var(--hue));
  --btn-regular-bg-hover: oklch(0.9 0.05 var(--hue));
  --btn-regular-bg-active: oklch(0.85 0.08 var(--hue));
  --deep-text: oklch(0.25 0.02 var(--hue));
  --inline-code-bg: var(--btn-regular-bg);
  --inline-code-color: var(--btn-content);
  --codeblock-bg: oklch(0.17 0.015 var(--hue));
  --codeblock-topbar-bg: oklch(0.3 0.02 var(--hue));
  --link-underline: oklch(0.93 0.04 var(--hue));
  --link-hover: oklch(0.95 0.025 var(--hue));
  --line-divider: rgba(0, 0, 0, 0.08);
  --line-color: rgba(0, 0, 0, 0.1);
  --admonitions-color-tip: oklch(0.7 0.14 180);
  --admonitions-color-note: oklch(0.7 0.14 250);
  --admonitions-color-important: oklch(0.7 0.14 310);
  --admonitions-color-warning: oklch(0.7 0.14 60);
  --admonitions-color-caution: oklch(0.6 0.2 25);
}

/* Dark mode */
:root.dark {
  --primary: oklch(0.75 0.14 var(--hue));
  --page-bg: oklch(0.16 0.014 var(--hue));
  --card-bg: oklch(0.23 0.015 var(--hue));
  --btn-content: oklch(0.75 0.1 var(--hue));
  --btn-regular-bg: oklch(0.33 0.035 var(--hue));
  --codeblock-topbar-bg: oklch(0.12 0.015 var(--hue));
  --line-divider: rgba(255, 255, 255, 0.08);
  --line-color: rgba(255, 255, 255, 0.1);
  --admonitions-color-tip: oklch(0.75 0.14 180);
  --admonitions-color-note: oklch(0.75 0.14 250);
  --admonitions-color-important: oklch(0.75 0.14 310);
  --admonitions-color-warning: oklch(0.75 0.14 60);
  --admonitions-color-caution: oklch(0.65 0.2 25);
}
```
