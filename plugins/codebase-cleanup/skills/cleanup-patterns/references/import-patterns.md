# Import Analysis Patterns

Detailed patterns for detecting import issues in TypeScript/JavaScript.

## Unused Import Detection

### Named Imports

```typescript
// PATTERN: Named import with some unused
import { useState, useEffect, useCallback } from 'react';
//        ^used    ^unused    ^used

// DETECTION:
// 1. Extract identifiers: [useState, useEffect, useCallback]
// 2. Search file for each identifier (excluding import line)
// 3. useEffect has 0 occurrences -> unused
```

### Default Imports

```typescript
// PATTERN: Unused default import
import lodash from 'lodash';
// lodash never used in file

// DETECTION:
// 1. Extract default import name: lodash
// 2. Search for: lodash. or lodash( or lodash[
// 3. Zero matches -> unused
```

### Namespace Imports

```typescript
// PATTERN: Partially used namespace
import * as utils from './utils';
// Only utils.format used, but utils.parse also imported

// DETECTION:
// 1. Find all utils.X references
// 2. Compare to all exports from ./utils
// 3. Report unused exports from that module
```

### Type-Only Imports (TypeScript)

```typescript
// PATTERN: Type import
import type { User } from './types';
import { type Config, formatConfig } from './config';

// HANDLING:
// Type imports are stripped at compile time
// Check for usage in type positions only
// Don't flag type-only imports as unused if used as type annotations
```

### Side-Effect Imports

```typescript
// PATTERN: Side-effect only imports
import './styles.css';
import 'reflect-metadata';
import './polyfills';

// HANDLING:
// These execute code but export nothing
// Cannot be statically determined as "unused"
// Flag for manual review with low confidence
```

## Duplicate Import Detection

### Same Module, Multiple Statements

```typescript
// BAD: Split imports from same module
import { Button } from '@/components';
import { Input } from '@/components';
import { Modal } from '@/components';

// GOOD: Consolidated import
import { Button, Input, Modal } from '@/components';

// DETECTION:
// Build map of module -> import count
// Flag modules with count > 1
```

### Mixed Default and Named

```typescript
// BAD: Separate statements
import React from 'react';
import { useState, useEffect } from 'react';

// GOOD: Combined
import React, { useState, useEffect } from 'react';
```

## Circular Import Detection

### Simple Cycle

```
A.ts imports B.ts
B.ts imports A.ts
```

### Complex Cycle

```
A.ts -> B.ts -> C.ts -> D.ts -> A.ts
```

### Detection Algorithm

```javascript
// Build directed graph
const graph = {
  'A.ts': ['B.ts'],
  'B.ts': ['C.ts'],
  'C.ts': ['A.ts']  // Cycle!
};

// DFS with path tracking
function detectCycle(node, path = [], visited = new Set()) {
  if (path.includes(node)) {
    return path.slice(path.indexOf(node)).concat(node);
  }
  if (visited.has(node)) return null;

  visited.add(node);
  for (const dep of graph[node] || []) {
    const cycle = detectCycle(dep, [...path, node], visited);
    if (cycle) return cycle;
  }
  return null;
}
```

### Resolution Strategies

1. **Extract shared code** - Move common code to third module
2. **Lazy import** - Use dynamic `import()`
3. **Dependency injection** - Pass dependencies as parameters
4. **Interface segregation** - Import only interfaces, not implementations

```typescript
// Before: Circular
// userService.ts
import { AuthService } from './authService';
// authService.ts
import { UserService } from './userService';

// After: Resolved with interfaces
// interfaces.ts
export interface IAuthService { ... }
export interface IUserService { ... }

// userService.ts
import type { IAuthService } from './interfaces';
// authService.ts
import type { IUserService } from './interfaces';
```

## Tool Commands

### TypeScript Compiler

```bash
# Check for unused imports
npx tsc --noEmit --noUnusedLocals 2>&1 | grep "is declared but never used"
```

### ESLint

```bash
# With eslint-plugin-unused-imports
npm install -D eslint-plugin-unused-imports

# .eslintrc.js
module.exports = {
  plugins: ['unused-imports'],
  rules: {
    'unused-imports/no-unused-imports': 'error',
    'unused-imports/no-unused-vars': ['error', {
      vars: 'all',
      varsIgnorePattern: '^_',
      args: 'after-used',
      argsIgnorePattern: '^_'
    }]
  }
};

# Run
npx eslint . --fix
```

### organize-imports-cli

```bash
# Auto-organize and remove unused
npx organize-imports-cli tsconfig.json --remove-unused
```

### madge

```bash
# Circular dependency detection
npx madge --circular --extensions ts,tsx src/

# Generate dependency graph image
npx madge --image graph.svg src/

# List all dependencies for a file
npx madge --depends src/index.ts
```

## Edge Cases

### Re-exports (Barrel Files)

```typescript
// index.ts - barrel file
export { Button } from './Button';
export { Input } from './Input';

// Button not used locally, but re-exported
// Don't mark as unused - it's intentionally re-exported
```

### Dynamic Imports

```typescript
// Cannot statically analyze - flag with low confidence
const Component = await import(`./components/${name}`);
const handler = require(`./handlers/${type}`);
```

### JSX Usage

```typescript
// Import used in JSX, not as function call
import Button from './Button';

// Usage is <Button />, not Button()
// Search for both patterns
```

### Webpack/Vite Magic Comments

```typescript
// Prefetch hint - still a valid import
import(/* webpackPrefetch: true */ './HeavyComponent');
```

## Grep Patterns for Detection

```bash
# Find all imports from a specific module
grep -rn "from ['\"]react['\"]" --include="*.ts" --include="*.tsx"

# Find unused identifier after import
# 1. Get imported name
# 2. Search file excluding import line
grep -c "useEffect" file.tsx  # Count occurrences

# Find potential circular imports
# Look for files that import each other
grep -l "from './a'" b.ts && grep -l "from './b'" a.ts
```

## Auto-Fix Patterns

### Remove Unused Named Import

```diff
- import { useState, useEffect, useCallback } from 'react';
+ import { useState, useCallback } from 'react';
```

### Remove Entire Unused Import

```diff
- import lodash from 'lodash';
```

### Consolidate Duplicate Imports

```diff
- import { Button } from '@/ui';
- import { Input } from '@/ui';
- import { Modal } from '@/ui';
+ import { Button, Input, Modal } from '@/ui';
```
