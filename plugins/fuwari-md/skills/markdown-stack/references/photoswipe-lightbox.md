# PhotoSwipe Image Lightbox

Fuwari uses PhotoSwipe v5 for image lightbox/gallery functionality, allowing users to click on images to view them in a full-screen overlay with zoom capabilities.

## Installation

```bash
npm install photoswipe
```

## Basic Setup

### 1. Import in Layout

```javascript
// In your layout file (e.g., Layout.astro)
import PhotoSwipeLightbox from "photoswipe/lightbox"
import "photoswipe/style.css"

let lightbox: PhotoSwipeLightbox
let pswp = import("photoswipe")

function createPhotoSwipe() {
  lightbox = new PhotoSwipeLightbox({
    gallery: ".custom-md img, #post-cover img",  // Target images
    pswpModule: () => pswp,
    closeSVG: '<svg>...</svg>',  // Custom close icon
    zoomSVG: '<svg>...</svg>',   // Custom zoom icon
    padding: { top: 20, bottom: 20, left: 20, right: 20 },
    wheelToZoom: true,
    arrowPrev: false,
    arrowNext: false,
    imageClickAction: 'close',
    tapAction: 'close',
    doubleTapAction: 'zoom',
  })

  // Filter to get image dimensions
  lightbox.addFilter("domItemData", (itemData, element) => {
    if (element instanceof HTMLImageElement) {
      itemData.src = element.src
      itemData.w = Number(element.naturalWidth || window.innerWidth)
      itemData.h = Number(element.naturalHeight || window.innerHeight)
      itemData.msrc = element.src
    }
    return itemData
  })

  lightbox.init()
}
```

### 2. Initialize on Page Load

```javascript
// For single page apps with page transitions (Swup)
const setup = () => {
  if (!lightbox) {
    createPhotoSwipe()
  }

  // Re-initialize on page navigation
  window.swup.hooks.on("page:view", () => {
    createPhotoSwipe()
  })

  // Destroy before content replacement
  window.swup.hooks.on(
    "content:replace",
    () => {
      lightbox?.destroy?.()
    },
    { before: true },
  )
}

if (window.swup) {
  setup()
} else {
  document.addEventListener("swup:enable", setup)
}

// For static sites without Swup
document.addEventListener("DOMContentLoaded", createPhotoSwipe)
```

## Configuration Options

```javascript
{
  // Target selector for images
  gallery: ".custom-md img",

  // Dynamic import for code splitting
  pswpModule: () => import("photoswipe"),

  // Padding around lightbox content
  padding: { top: 20, bottom: 20, left: 20, right: 20 },

  // Enable mouse wheel zoom
  wheelToZoom: true,

  // Hide navigation arrows (for single images)
  arrowPrev: false,
  arrowNext: false,

  // Click behaviors
  imageClickAction: 'close',    // Click image to close
  tapAction: 'close',           // Tap to close (mobile)
  doubleTapAction: 'zoom',      // Double tap to zoom

  // Custom SVG icons (optional)
  closeSVG: '<svg>...</svg>',
  zoomSVG: '<svg>...</svg>',
}
```

## Custom Styling

Create a CSS file for PhotoSwipe customization:

```css
/* photoswipe.css */

/* Button styling */
.pswp__button {
  transition: all 0.2s;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0;
  width: 3rem;
  height: 3rem;
}

.pswp__button:hover {
  background: rgba(0, 0, 0, 0.5);
}

.pswp__button:active {
  background: rgba(0, 0, 0, 0.6);
}

/* Zoom and close buttons */
.pswp__button--zoom,
.pswp__button--close {
  margin-top: 1rem;
  border-radius: 0.75rem;
}

.pswp__button--zoom:active,
.pswp__button--close:active {
  transform: scale(0.9);
}

.pswp__button--zoom {
  margin-right: 0.625rem;
}

.pswp__button--close {
  margin-right: 1rem;
}
```

## Astro Integration

### Layout.astro

```astro
---
import "photoswipe/style.css"
import "../styles/photoswipe.css"
---

<html>
  <body>
    <slot />
  </body>
</html>

<script>
import PhotoSwipeLightbox from "photoswipe/lightbox"

let lightbox: PhotoSwipeLightbox

function createPhotoSwipe() {
  lightbox = new PhotoSwipeLightbox({
    gallery: ".prose img",
    pswpModule: () => import("photoswipe"),
    wheelToZoom: true,
  })

  lightbox.addFilter("domItemData", (itemData, element) => {
    if (element instanceof HTMLImageElement) {
      itemData.src = element.src
      itemData.w = element.naturalWidth || 1200
      itemData.h = element.naturalHeight || 800
      itemData.msrc = element.src
    }
    return itemData
  })

  lightbox.init()
}

document.addEventListener("astro:page-load", createPhotoSwipe)
</script>
```

## Next.js Integration

```jsx
// components/PhotoSwipeProvider.jsx
'use client'

import { useEffect } from 'react'
import PhotoSwipeLightbox from 'photoswipe/lightbox'
import 'photoswipe/style.css'

export default function PhotoSwipeProvider({ children }) {
  useEffect(() => {
    const lightbox = new PhotoSwipeLightbox({
      gallery: '.prose img',
      pswpModule: () => import('photoswipe'),
      wheelToZoom: true,
    })

    lightbox.addFilter('domItemData', (itemData, element) => {
      if (element instanceof HTMLImageElement) {
        itemData.src = element.src
        itemData.w = element.naturalWidth || 1200
        itemData.h = element.naturalHeight || 800
      }
      return itemData
    })

    lightbox.init()

    return () => {
      lightbox.destroy()
    }
  }, [])

  return children
}
```

## Image Styling

Add cursor styling to indicate images are clickable:

```css
/* Indicate images are zoomable */
.prose img,
.custom-md img {
  cursor: zoom-in;
  border-radius: 0.75rem;
}
```

## Troubleshooting

### Images not opening in lightbox

1. Check selector matches your images:
   ```javascript
   gallery: ".custom-md img"  // Adjust to match your container
   ```

2. Ensure PhotoSwipe CSS is imported:
   ```javascript
   import "photoswipe/style.css"
   ```

3. Verify images have `src` attribute (not just `srcset`)

### Wrong image dimensions

The `domItemData` filter should extract dimensions:

```javascript
lightbox.addFilter("domItemData", (itemData, element) => {
  if (element instanceof HTMLImageElement) {
    // Wait for image to load for accurate dimensions
    itemData.w = element.naturalWidth || 1200
    itemData.h = element.naturalHeight || 800
  }
  return itemData
})
```

### Conflicts with page transitions

Destroy and recreate lightbox on navigation:

```javascript
// Destroy before page change
lightbox?.destroy?.()

// Recreate after new page loads
createPhotoSwipe()
```

## Dependencies

```json
{
  "photoswipe": "^5.4.4"
}
```

**Version notes:**
- Tested with PhotoSwipe v5.4.4
- For production stability, consider pinning: `"photoswipe": "5.4.4"`
- v5.x has breaking changes from v4.x - don't use older tutorials
- Check [PhotoSwipe changelog](https://github.com/dimsemenov/PhotoSwipe/releases) before updating
