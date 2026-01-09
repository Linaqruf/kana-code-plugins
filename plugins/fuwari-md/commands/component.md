---
name: component
description: Generate custom remark/rehype plugins based on Fuwari patterns
argument-hint: "<type>"
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
version: 1.0.0
---

# Custom Markdown Component Generator

Generate custom remark or rehype plugins following Fuwari's proven patterns.

## Instructions

### Step 1: Determine Component Type

If argument provided (e.g., `/component directive`), use that type.
Otherwise, ask:

```
What type of component do you want to create?
- Container Directive (:::name ... :::)
- Leaf Directive (::name{attrs})
- Text Directive (:name[content])
- Rehype Component (custom HTML rendering)
```

### Step 2: Gather Component Details

Ask relevant questions based on type:

**For Directives:**
```
What is the directive name? (e.g., "youtube", "tweet", "figure")
```

```
What attributes should it accept? (e.g., "id", "url", "caption")
```

```
Should it have children/content? (yes/no)
```

**For Rehype Components:**
```
What HTML element should it render? (e.g., "div", "figure", "iframe")
```

```
What CSS classes should be applied?
```

### Step 3: Generate Plugin Code

Based on Fuwari's patterns, generate:

1. **Remark plugin** (if directive) - for parsing
2. **Rehype component** - for rendering
3. **Integration code** - how to add to config
4. **CSS template** - basic styling

## Templates

### Container Directive Template

```javascript
// rehype-component-{name}.mjs
import { h } from 'hastscript';

/**
 * Creates a {Name} component.
 *
 * Markdown syntax:
 * :::{name}[Optional Title]
 * Content here
 * :::
 *
 * Or with attributes:
 * :::{name}{attr1="value1" attr2="value2"}
 * Content here
 * :::
 */
export function {Name}Component(properties, children) {
  if (!Array.isArray(children) || children.length === 0) {
    return h('div', { class: 'hidden' }, 'Invalid {name} directive');
  }

  let title = null;
  if (properties?.['has-directive-label']) {
    title = children[0];
    children = children.slice(1);
    title.tagName = 'div';
  }

  return h('div', { class: '{name}-container' }, [
    title && h('div', { class: '{name}-title' }, title),
    h('div', { class: '{name}-content' }, children),
  ]);
}
```

### Leaf Directive Template

```javascript
// rehype-component-{name}.mjs
import { h } from 'hastscript';

/**
 * Creates a {Name} component.
 *
 * Markdown syntax:
 * ::{name}{attr="value"}
 */
export function {Name}Component(properties, children) {
  if (Array.isArray(children) && children.length !== 0) {
    return h('div', { class: 'hidden' }, '{name} must be a leaf directive');
  }

  const { attr1, attr2 } = properties;

  if (!attr1) {
    return h('div', { class: 'hidden' }, 'Missing required attribute: attr1');
  }

  return h('div', { class: '{name}-wrapper' }, [
    // Render your component here
    h('span', { class: '{name}-content' }, `Value: ${attr1}`),
  ]);
}
```

### Text Directive Template

```javascript
// rehype-component-{name}.mjs
import { h } from 'hastscript';

/**
 * Creates a {Name} inline component.
 *
 * Markdown syntax:
 * :{name}[inline content]
 */
export function {Name}Component(properties, children) {
  return h('span', { class: '{name}' }, children);
}
```

### Integration Code Template

```javascript
// In your config (astro.config.mjs, etc.):
import { {Name}Component } from './plugins/rehype-component-{name}.mjs';

// Add to rehypePlugins:
[
  rehypeComponents,
  {
    components: {
      // ... existing components
      {name}: {Name}Component,
    },
  },
],
```

### CSS Template

```css
.{name}-container {
  /* Container styling */
  border: 1px solid var(--border-color, #e1e4e8);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
}

.{name}-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.{name}-content {
  /* Content styling */
}
```

## Example Components

### YouTube Embed

```javascript
// rehype-component-youtube.mjs
import { h } from 'hastscript';

export function YoutubeComponent(properties, children) {
  if (Array.isArray(children) && children.length !== 0) {
    return h('div', { class: 'hidden' }, 'youtube must be leaf directive');
  }

  const { id, title = 'YouTube Video' } = properties;

  if (!id) {
    return h('div', { class: 'hidden' }, 'Missing video ID');
  }

  return h('div', { class: 'youtube-embed' }, [
    h('iframe', {
      src: `https://www.youtube.com/embed/${id}`,
      title,
      frameborder: '0',
      allow: 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture',
      allowfullscreen: true,
      loading: 'lazy',
    }),
  ]);
}
```

Usage: `::youtube{id="dQw4w9WgXcQ" title="Rick Astley"}`

### Tweet Embed

```javascript
// rehype-component-tweet.mjs
import { h } from 'hastscript';

export function TweetComponent(properties, children) {
  const { id, user } = properties;

  if (!id || !user) {
    return h('div', { class: 'hidden' }, 'Tweet requires id and user');
  }

  const tweetUrl = `https://twitter.com/${user}/status/${id}`;
  const cardUuid = `TW${Math.random().toString(36).slice(-6)}`;

  return h('div', { class: 'tweet-embed', id: cardUuid }, [
    h('blockquote', { class: 'twitter-tweet' }, [
      h('a', { href: tweetUrl }, 'Loading tweet...'),
    ]),
    h('script', {
      async: true,
      src: 'https://platform.twitter.com/widgets.js',
    }),
  ]);
}
```

Usage: `::tweet{user="astaborsk" id="1234567890"}`

### Figure with Caption

```javascript
// rehype-component-figure.mjs
import { h } from 'hastscript';

export function FigureComponent(properties, children) {
  const { src, alt = '', caption } = properties;

  if (!src) {
    return h('div', { class: 'hidden' }, 'Figure requires src attribute');
  }

  return h('figure', { class: 'md-figure' }, [
    h('img', { src, alt, loading: 'lazy' }),
    caption && h('figcaption', caption),
  ]);
}
```

Usage: `::figure{src="/image.jpg" alt="Description" caption="Figure 1: My image"}`

## Response Format

After gathering requirements:

1. Generate the rehype component file
2. Show the integration code for the user's framework
3. Provide example CSS
4. Show example markdown usage
5. Explain any dependencies needed

## Error Handling

### Invalid Component Type

If the user specifies an unrecognized component type:

1. List valid types:
   - `directive` or `container` - Container directive (:::name ... :::)
   - `leaf` - Leaf directive (::name{attrs})
   - `inline` or `text` - Text directive (:name[content])
   - `rehype` - Custom rehype component

2. Ask which type they meant

### Invalid Directive Name

If the directive name conflicts with existing directives:

1. Warn about the conflict (e.g., `note`, `tip`, `github` are reserved)
2. Suggest an alternative name
3. Ask if they want to override the existing directive

### Missing Required Information

If the user doesn't provide enough details:

1. Explain what's missing (name, attributes, render output)
2. Provide sensible defaults where possible
3. Ask only for the essential missing pieces

### File Already Exists

Before creating a new plugin file:

1. Check if `rehype-component-{name}.mjs` already exists
2. Ask whether to overwrite or use a different name
3. Show diff if overwriting

### Dependencies Not Installed

After generating the component:

1. Check if `hastscript` is installed (required for all components)
2. List any missing dependencies
3. Provide the npm install command
