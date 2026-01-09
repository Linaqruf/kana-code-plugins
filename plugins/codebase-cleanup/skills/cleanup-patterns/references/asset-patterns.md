# Asset Tracking Patterns

Strategies for detecting unused static assets in web projects.

## Asset Types and Locations

### Images

| Extension | Type | Common Locations |
|-----------|------|------------------|
| .png | Raster | public/images/, src/assets/ |
| .jpg, .jpeg | Raster | public/images/, src/assets/ |
| .svg | Vector | public/icons/, src/components/ |
| .webp | Modern raster | public/images/ |
| .gif | Animated | public/images/ |
| .ico | Favicon | public/, public/favicon/ |
| .avif | Modern raster | public/images/ |

### Stylesheets

| Extension | Type | Common Locations |
|-----------|------|------------------|
| .css | Plain CSS | src/styles/, public/ |
| .scss, .sass | Sass | src/styles/, src/components/ |
| .less | Less | src/styles/ |
| .module.css | CSS Modules | alongside components |

### Fonts

| Extension | Type | Common Locations |
|-----------|------|------------------|
| .woff2 | Modern web | public/fonts/ |
| .woff | Web font | public/fonts/ |
| .ttf | TrueType | public/fonts/ |
| .otf | OpenType | public/fonts/ |
| .eot | IE legacy | public/fonts/ |

### Other Static Files

| Type | Extensions | Locations |
|------|------------|-----------|
| Data | .json, .yaml | src/data/, public/ |
| Documents | .pdf | public/docs/ |
| Video | .mp4, .webm | public/videos/ |
| Audio | .mp3, .wav | public/audio/ |

## Reference Patterns

### Direct Imports (Bundler Processed)

```typescript
// Webpack/Vite/Parcel handle these
import logo from './logo.png';
import heroImage from '../assets/hero.jpg';
import Icon from './icon.svg';

// Usage
<img src={logo} alt="Logo" />
<Icon className="icon" />  // SVG as component
```

### Public Directory References

```typescript
// Path from public/ folder root
<img src="/images/hero.png" />
<link rel="stylesheet" href="/styles/main.css" />

// Next.js Image component
import Image from 'next/image';
<Image src="/logo.png" width={100} height={50} />
```

### CSS References

```css
/* Background images */
.hero {
  background-image: url('/images/hero.jpg');
  background-image: url('../assets/pattern.png');
}

/* Font files */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2'),
       url('/fonts/custom.woff') format('woff');
}

/* Cursor */
.custom-cursor {
  cursor: url('/images/cursor.png'), auto;
}
```

### HTML References

```html
<!-- Link tags -->
<link rel="icon" href="/favicon.ico" />
<link rel="stylesheet" href="/styles/global.css" />
<link rel="preload" href="/fonts/main.woff2" as="font" />

<!-- Image tags -->
<img src="/images/logo.png" alt="Logo" />

<!-- Video/Audio -->
<video src="/videos/intro.mp4" />
<audio src="/audio/notification.mp3" />
```

## Detection Algorithm

### Step 1: Collect All Assets

```bash
# Find all potential assets
find public src/assets -type f \( \
  -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o \
  -name "*.svg" -o -name "*.webp" -o -name "*.gif" -o \
  -name "*.woff" -o -name "*.woff2" -o -name "*.ttf" -o \
  -name "*.css" -o -name "*.json" \
\) -not -path "./node_modules/*"
```

### Step 2: Search for References

```javascript
for (const asset of assets) {
  const filename = path.basename(asset);
  const relativePath = asset.replace('public/', '/');

  // Search patterns
  const patterns = [
    filename,                    // hero.png
    relativePath,                // /images/hero.png
    asset,                       // public/images/hero.png
    `./${path.relative(cwd, asset)}`, // ./public/images/hero.png
  ];

  const references = searchCodebase(patterns, [
    '**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx',
    '**/*.css', '**/*.scss', '**/*.html'
  ]);

  if (references.length === 0) {
    report('Unused asset', asset);
  }
}
```

### Step 3: Handle Path Variations

```javascript
// Normalize paths for comparison
function normalizePath(p) {
  return p
    .replace(/^\.\//, '')           // Remove leading ./
    .replace(/^public\//, '/')      // public/x -> /x
    .replace(/\\/g, '/');           // Windows paths
}

// Match variations
function pathsMatch(ref, asset) {
  return normalizePath(ref) === normalizePath(asset) ||
         path.basename(ref) === path.basename(asset);
}
```

## Dynamic Asset Loading (Low Confidence)

### Template Literals

```typescript
// Cannot determine which images are used
const imagePath = `/images/${category}/${id}.png`;
<img src={imagePath} />

// Flag entire directory for manual review
```

### Import Meta Glob (Vite)

```typescript
// All images in directory are potentially used
const images = import.meta.glob('./gallery/*.jpg');

// Cannot determine which are actually rendered
```

### Require Context (Webpack)

```typescript
// Dynamic require
const images = require.context('./icons', false, /\.svg$/);
const icon = images(`./${iconName}.svg`);
```

### Handling Strategy

```markdown
## Potentially Unused (Manual Review Required)

The following directories contain dynamically loaded assets:
- `public/images/gallery/` - 50 images, loaded via import.meta.glob
- `src/icons/` - 30 SVGs, loaded via require.context

These cannot be statically analyzed. Please manually verify usage.
```

## CSS-Specific Detection

### Unused CSS Files

```bash
# Find CSS imports in JS/TS
grep -rn "import.*\.css" --include="*.ts" --include="*.tsx"
grep -rn "require.*\.css" --include="*.js"

# Find link tags in HTML
grep -rn "<link.*stylesheet" --include="*.html"
```

### Unused CSS Classes (Advanced)

```javascript
// 1. Extract all class selectors from CSS
const cssClasses = extractSelectors('styles.css');
// ['.container', '.header', '.btn-primary', ...]

// 2. Search for usage in templates
for (const cls of cssClasses) {
  const className = cls.slice(1); // Remove leading dot
  const patterns = [
    `className="${className}"`,
    `className={\`.*${className}.*\`}`,
    `classList.add('${className}')`,
  ];

  if (!foundInCodebase(patterns)) {
    report('Unused CSS class', cls);
  }
}
```

## Font Detection

### Find Font Files

```bash
find . -type f \( -name "*.woff" -o -name "*.woff2" -o -name "*.ttf" -o -name "*.otf" \) \
  -not -path "./node_modules/*"
```

### Check @font-face References

```javascript
// 1. Find all font files
const fonts = glob(['**/*.woff', '**/*.woff2', '**/*.ttf']);

// 2. Search CSS for @font-face rules
for (const font of fonts) {
  const filename = path.basename(font);
  const refs = searchCSS(`url.*${filename}`);

  if (refs.length === 0) {
    report('Font not in @font-face', font);
  }
}

// 3. Check if font-family is used
for (const fontFace of fontFaces) {
  const family = fontFace.fontFamily;
  const usage = searchCSS(`font-family.*${family}`);

  if (usage.length === 0) {
    report('Font-family never used', family);
  }
}
```

## Framework-Specific Patterns

### Next.js

```typescript
// Image component
import Image from 'next/image';
<Image src="/logo.png" ... />  // public/logo.png

// Static imports (optimized)
import heroImg from '../public/hero.jpg';
<Image src={heroImg} ... />
```

### Astro

```astro
---
// Optimized imports
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<Image src={heroImage} alt="Hero" />
```

### Vite

```typescript
// URL imports
import logoUrl from './logo.png?url';

// Raw imports
import iconSvg from './icon.svg?raw';

// Asset imports
const imageUrl = new URL('./image.png', import.meta.url).href;
```

## Size Analysis

```bash
# Total size by directory
du -sh public/images/
du -sh public/fonts/
du -sh src/assets/

# Largest files
find public -type f -exec ls -lh {} \; | sort -k5 -h -r | head -20

# By extension
find public -name "*.png" -exec du -ch {} + | tail -1
find public -name "*.jpg" -exec du -ch {} + | tail -1
```

## Report Format

```markdown
## Unused Assets Report

### Summary
| Type | Count | Size |
|------|-------|------|
| Images | 12 | 2.3 MB |
| CSS | 3 | 45 KB |
| Fonts | 2 | 180 KB |
| **Total** | **17** | **2.5 MB** |

### High Confidence (Safe to Remove)
| File | Size | Last Modified |
|------|------|---------------|
| public/images/old-logo.png | 45 KB | 2023-01-15 |
| public/icons/deprecated.svg | 2 KB | 2022-11-20 |

### Low Confidence (Manual Review)
| Directory | Files | Reason |
|-----------|-------|--------|
| public/gallery/ | 50 | Dynamic loading detected |
| src/icons/ | 30 | require.context usage |
```

## Exclusions

### Always Skip

- `node_modules/`
- `.next/`, `dist/`, `build/`
- `.git/`
- `*.map` (source maps)

### Framework Generated

- `_next/static/` (Next.js build output)
- `.astro/` (Astro build cache)
- `public/_astro/` (Astro optimized assets)

### Build Artifacts

```javascript
// Skip files with hashes (generated by bundler)
const isGenerated = /\.[a-f0-9]{8,}\.(js|css|png|jpg)$/.test(filename);
```
