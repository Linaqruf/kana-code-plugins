# Table of Contents Component

Fuwari includes an interactive Table of Contents (TOC) component that tracks scroll position and highlights the current section.

## Features

- Automatic heading extraction from markdown
- Active section tracking via IntersectionObserver
- Smooth scrolling to sections
- Visual indicator for current position
- Configurable depth (h2, h3, h4, etc.)
- Web Component implementation

## Astro Implementation

### TOC.astro Component

```astro
---
import type { MarkdownHeading } from "astro";

interface Props {
  class?: string;
  headings: MarkdownHeading[];
}

let { headings = [] } = Astro.props;

// Find minimum heading depth
let minDepth = 10;
for (const heading of headings) {
  minDepth = Math.min(minDepth, heading.depth);
}

const className = Astro.props.class;
const maxLevel = 3; // Configure max depth (h2 + 2 levels = h4)

// Remove trailing hash from heading text
const removeTailingHash = (text: string) => {
  let lastIndexOfHash = text.lastIndexOf("#");
  if (lastIndexOfHash !== text.length - 1) {
    return text;
  }
  return text.substring(0, lastIndexOfHash);
};

let heading1Count = 1;
---

<table-of-contents class:list={[className, "group"]}>
  {headings.filter((heading) => heading.depth < minDepth + maxLevel).map((heading) =>
    <a href={`#${heading.slug}`} class="toc-link">
      <div class:list={["toc-indicator", {
        "toc-h1": heading.depth == minDepth,
        "toc-h2": heading.depth == minDepth + 1,
        "toc-h3": heading.depth == minDepth + 2,
      }]}>
        {heading.depth == minDepth && heading1Count++}
        {heading.depth == minDepth + 1 && <div class="toc-dot-medium"></div>}
        {heading.depth == minDepth + 2 && <div class="toc-dot-small"></div>}
      </div>
      <div class="toc-text">{removeTailingHash(heading.text)}</div>
    </a>
  )}
  <div id="active-indicator" class="toc-active-indicator"></div>
</table-of-contents>

<script>
// Web Component definition below
</script>

<style>
.toc-link {
  display: flex;
  gap: 0.5rem;
  position: relative;
  width: 100%;
  min-height: 2.25rem;
  padding: 0.5rem;
  border-radius: 0.75rem;
  transition: background-color 0.2s;
}

.toc-link:hover {
  background-color: var(--toc-btn-hover);
}

.toc-indicator {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.2s;
}

.toc-h1 {
  background: var(--toc-badge-bg);
  color: var(--btn-content);
}

.toc-h2 {
  margin-left: 1rem;
}

.toc-h3 {
  margin-left: 2rem;
}

.toc-dot-medium {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 0.1875rem;
  background: var(--toc-badge-bg);
  transition: all 0.2s;
}

.toc-dot-small {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 0.125rem;
  background: var(--line-divider);
}

.toc-text {
  font-size: 0.875rem;
  transition: color 0.2s;
}

.toc-active-indicator {
  position: absolute;
  left: 0;
  right: 0;
  border-radius: 0.75rem;
  background: var(--toc-btn-hover);
  border: 2px dashed var(--toc-btn-hover);
  z-index: -1;
  transition: all 0.3s;
  opacity: 0;
}

.group:hover .toc-active-indicator {
  background: transparent;
  border-color: var(--toc-btn-active);
}
</style>
```

### Web Component Script

```javascript
class TableOfContents extends HTMLElement {
  tocEl = null;
  visibleClass = "visible";
  observer;
  headingIdxMap = new Map();
  headings = [];
  sections = [];
  tocEntries = [];
  active = [];
  activeIndicator = null;

  constructor() {
    super();
    this.observer = new IntersectionObserver(
      this.markVisibleSection,
      { threshold: 0 }
    );
  }

  markVisibleSection = (entries) => {
    entries.forEach((entry) => {
      const id = entry.target.children[0]?.getAttribute("id");
      const idx = id ? this.headingIdxMap.get(id) : undefined;
      if (idx !== undefined) {
        this.active[idx] = entry.isIntersecting;
      }
    });

    if (!this.active.includes(true)) {
      this.fallback();
    }
    this.update();
  };

  toggleActiveHeading = () => {
    let i = this.active.length - 1;
    let min = this.active.length - 1;
    let max = -1;

    // Find active range
    while (i >= 0 && !this.active[i]) {
      this.tocEntries[i].classList.remove(this.visibleClass);
      i--;
    }
    while (i >= 0 && this.active[i]) {
      this.tocEntries[i].classList.add(this.visibleClass);
      min = Math.min(min, i);
      max = Math.max(max, i);
      i--;
    }
    while (i >= 0) {
      this.tocEntries[i].classList.remove(this.visibleClass);
      i--;
    }

    // Update active indicator position
    if (min > max) {
      this.activeIndicator?.setAttribute("style", "opacity: 0");
    } else {
      const parentOffset = this.tocEl?.getBoundingClientRect().top || 0;
      const scrollOffset = this.tocEl?.scrollTop || 0;
      const top = this.tocEntries[min].getBoundingClientRect().top - parentOffset + scrollOffset;
      const bottom = this.tocEntries[max].getBoundingClientRect().bottom - parentOffset + scrollOffset;
      this.activeIndicator?.setAttribute("style", `top: ${top}px; height: ${bottom - top}px; opacity: 1`);
    }
  };

  scrollToActiveHeading = () => {
    if (!this.tocEl) return;

    const activeHeading = this.tocEl.querySelectorAll(`.${this.visibleClass}`);
    if (!activeHeading.length) return;

    const topmost = activeHeading[0];
    const bottommost = activeHeading[activeHeading.length - 1];
    const tocHeight = this.tocEl.clientHeight;

    let top;
    if (bottommost.getBoundingClientRect().bottom - topmost.getBoundingClientRect().top < 0.9 * tocHeight) {
      top = topmost.offsetTop - 32;
    } else {
      top = bottommost.offsetTop - tocHeight * 0.8;
    }

    this.tocEl.scrollTo({ top, left: 0, behavior: "smooth" });
  };

  update = () => {
    requestAnimationFrame(() => {
      this.toggleActiveHeading();
      this.scrollToActiveHeading();
    });
  };

  fallback = () => {
    if (!this.sections.length) return;

    for (let i = 0; i < this.sections.length; i++) {
      const offsetTop = this.sections[i].getBoundingClientRect().top;
      const offsetBottom = this.sections[i].getBoundingClientRect().bottom;

      if (
        this.isInRange(offsetTop, 0, window.innerHeight) ||
        this.isInRange(offsetBottom, 0, window.innerHeight) ||
        (offsetTop < 0 && offsetBottom > window.innerHeight)
      ) {
        this.active[i] = true;
      } else if (offsetTop > window.innerHeight) {
        break;
      }
    }
  };

  isInRange(value, min, max) {
    return min < value && value < max;
  }

  connectedCallback() {
    // Initialize after animations complete
    const element = document.querySelector('.prose');
    if (element) {
      element.addEventListener('animationend', () => this.init(), { once: true });
    } else {
      this.init();
    }
  }

  init() {
    this.tocEl = document.getElementById("toc-inner-wrapper");
    if (!this.tocEl) return;

    this.activeIndicator = document.getElementById("active-indicator");
    this.tocEntries = Array.from(this.tocEl.querySelectorAll("a[href^='#']"));

    if (this.tocEntries.length === 0) return;

    // Map headings to sections
    this.sections = new Array(this.tocEntries.length);
    this.headings = new Array(this.tocEntries.length);

    for (let i = 0; i < this.tocEntries.length; i++) {
      const id = decodeURIComponent(this.tocEntries[i].hash?.substring(1));
      const heading = document.getElementById(id);
      const section = heading?.parentElement;

      if (heading && section) {
        this.headings[i] = heading;
        this.sections[i] = section;
        this.headingIdxMap.set(id, i);
      }
    }

    this.active = new Array(this.tocEntries.length).fill(false);

    // Observe sections
    this.sections.forEach((section) => this.observer.observe(section));

    this.fallback();
    this.update();
  }

  disconnectedCallback() {
    this.sections.forEach((section) => this.observer.unobserve(section));
    this.observer.disconnect();
  }
}

if (!customElements.get("table-of-contents")) {
  customElements.define("table-of-contents", TableOfContents);
}
```

## Usage

### In Astro Pages

```astro
---
import TOC from "../components/TOC.astro";
import { getCollection } from "astro:content";

const post = await getEntry("posts", "my-post");
const { Content, headings } = await post.render();
---

<div class="layout">
  <aside>
    <div id="toc-inner-wrapper">
      <TOC headings={headings} />
    </div>
  </aside>
  <article class="prose">
    <Content />
  </article>
</div>
```

## Configuration

### TOC Depth

Control how many heading levels to show:

```javascript
const maxLevel = 3; // Show h2, h3, h4 (minDepth + maxLevel)
```

### CSS Variables

```css
:root {
  /* Badge background for h1 entries */
  --toc-badge-bg: oklch(0.89 0.050 var(--hue));

  /* Hover state background */
  --toc-btn-hover: oklch(0.926 0.015 var(--hue));

  /* Active state background */
  --toc-btn-active: oklch(0.90 0.015 var(--hue));

  /* Button content color */
  --btn-content: oklch(0.55 0.12 var(--hue));
}
```

## Dependencies

Requires `remark-sectionize` to wrap headings in `<section>` elements for proper IntersectionObserver tracking:

```javascript
// astro.config.mjs
import remarkSectionize from 'remark-sectionize';

export default defineConfig({
  markdown: {
    remarkPlugins: [remarkSectionize],
  },
});
```

## Framework Adaptation

### React

```jsx
import { useEffect, useRef, useState } from 'react';

export function TableOfContents({ headings }) {
  const [activeIds, setActiveIds] = useState([]);
  const observer = useRef(null);

  useEffect(() => {
    observer.current = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const id = entry.target.querySelector('[id]')?.id;
          if (id) {
            setActiveIds((prev) =>
              entry.isIntersecting
                ? [...prev, id]
                : prev.filter((i) => i !== id)
            );
          }
        });
      },
      { threshold: 0 }
    );

    document.querySelectorAll('section').forEach((section) => {
      observer.current.observe(section);
    });

    return () => observer.current?.disconnect();
  }, []);

  return (
    <nav>
      {headings.map((heading) => (
        <a
          key={heading.slug}
          href={`#${heading.slug}`}
          className={activeIds.includes(heading.slug) ? 'active' : ''}
        >
          {heading.text}
        </a>
      ))}
    </nav>
  );
}
```

## Troubleshooting

### TOC not tracking sections

Ensure `remark-sectionize` is in your pipeline. The TOC relies on sections wrapping headings:

```html
<!-- Without sectionize -->
<h2 id="heading">Heading</h2>
<p>Content...</p>

<!-- With sectionize -->
<section>
  <h2 id="heading">Heading</h2>
  <p>Content...</p>
</section>
```

### Active indicator not showing

1. Check that `#toc-inner-wrapper` element exists
2. Ensure headings have `id` attributes (from `rehype-slug`)
3. Verify sections are being observed

### Headings not linking

Ensure `rehype-slug` is in your rehype plugins to generate IDs:

```javascript
import rehypeSlug from 'rehype-slug';

rehypePlugins: [rehypeSlug]
```
