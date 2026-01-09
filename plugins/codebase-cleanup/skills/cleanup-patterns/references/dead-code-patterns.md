# Dead Code Detection Patterns

Strategies for finding unreachable and unused code in TypeScript/JavaScript.

## Unreachable Code

### After Return Statement

```typescript
// PATTERN: Code after return
function getValue() {
  return 42;
  console.log('Never runs'); // DEAD
  const x = 10;              // DEAD
}

// DETECTION: Parse function body, find code after unconditional return
```

### After Throw Statement

```typescript
// PATTERN: Code after throw
function validate(input) {
  if (!input) {
    throw new Error('Invalid');
    cleanup(); // DEAD
  }
  return process(input);
}
```

### After Control Flow Exit

```typescript
// After break
for (const item of items) {
  if (condition) {
    break;
    processItem(item); // DEAD
  }
}

// After continue
for (const item of items) {
  if (shouldSkip(item)) {
    continue;
    log(item); // DEAD
  }
}

// After process.exit
process.exit(1);
cleanup(); // DEAD
```

### Constant Conditions

```typescript
// Always false
if (false) {
  neverExecuted(); // DEAD
}

// Compile-time constant
const DEBUG = false;
if (DEBUG) {
  debugLog(); // DEAD (intentional, but flaggable)
}

// Type-based impossible
function process(x: string) {
  if (typeof x === 'number') {
    handleNumber(x); // DEAD - x is never number
  }
}
```

## Unused Functions

### Private/Local Functions

```typescript
// Never called in file
function helperFunction() { ... } // DEAD if no calls found

// Method never called
class Service {
  private unusedMethod() { ... } // DEAD

  public usedMethod() {
    // unusedMethod not called here
  }
}
```

### Exported But Never Imported

```typescript
// utils.ts
export function usedUtil() { ... }
export function unusedUtil() { ... } // DEAD if never imported

// DETECTION:
// 1. Find all exports
// 2. Search codebase for imports of each export
// 3. Flag exports with zero importers
```

### Detection Strategy

```javascript
// Step 1: Collect all function declarations
const functions = collectFunctions(codebase);

// Step 2: Collect all function calls
const calls = collectCalls(codebase);

// Step 3: Find functions never called
const unused = functions.filter(fn =>
  !calls.some(call => call.name === fn.name)
);
```

## Unused Variables

### Simple Unused

```typescript
// Declared, never read
const UNUSED_CONSTANT = 42; // DEAD
let unusedVariable = 'hello'; // DEAD
```

### Assigned But Never Read

```typescript
let result;
result = calculate(); // Assigned
// result never accessed after this -> DEAD assignment
return otherValue;
```

### Unused Destructured

```typescript
// Destructured but not used
const { used, unused } = getData();
console.log(used);
// unused never referenced -> DEAD

// FIX: Use rest pattern
const { used, ...rest } = getData();
// or omit entirely
const { used } = getData();
```

### Unused Function Parameters

```typescript
// Parameter never used
function process(data, options, callback) {
  //              ^used  ^unused  ^used
  return callback(transform(data));
}

// FIX: Prefix with underscore or remove
function process(data, _options, callback) { ... }
```

### Caught Error Not Used

```typescript
// Error binding unused
try {
  riskyOperation();
} catch (error) {  // error never used
  console.log('Failed');
}

// FIX (ES2019+): Omit binding
try {
  riskyOperation();
} catch {
  console.log('Failed');
}
```

## Unused Class Members

### Private Methods

```typescript
class Service {
  private helper() {    // Never called internally
    return 'unused';
  }

  public main() {
    // helper() not invoked anywhere
  }
}
```

### Private Properties

```typescript
class Config {
  private readonly oldSetting = true;  // Never read
  private cache: Map<string, any>;      // Never used

  constructor() {
    this.cache = new Map(); // Assigned but never accessed
  }
}
```

### Unused Getters/Setters

```typescript
class User {
  private _name: string;

  get name() { return this._name; }        // Used
  set name(v) { this._name = v; }          // Never called -> DEAD

  get fullName() { return this._name; }    // Never accessed -> DEAD
}
```

## Unused Exports

### Finding Unused Exports

```bash
# Using ts-prune
npx ts-prune

# Output format:
# src/utils.ts:25 - unusedFunction
# src/types.ts:10 - UnusedType
```

### Entry Point Consideration

Not all exports need internal callers:

```typescript
// index.ts - public API, exports are intentional
export { createApp } from './app';
export { Config } from './config';

// pages/about.tsx - Next.js page, default export is entry point
export default function AboutPage() { ... }

// api/users.ts - API route entry point
export async function GET() { ... }
```

### Detection with Exclusions

```javascript
const entryPoints = [
  'src/index.ts',
  'src/pages/**/*.tsx',
  'src/api/**/*.ts',
];

const unusedExports = findExports()
  .filter(exp => !isInEntryPoint(exp, entryPoints))
  .filter(exp => !hasImporters(exp));
```

## Tool Integration

### TypeScript Compiler

```json
// tsconfig.json
{
  "compilerOptions": {
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

```bash
npx tsc --noEmit
# Reports: 'x' is declared but its value is never read.
```

### ESLint Rules

```json
{
  "rules": {
    "no-unused-vars": ["error", {
      "vars": "all",
      "args": "after-used",
      "ignoreRestSiblings": true,
      "varsIgnorePattern": "^_",
      "argsIgnorePattern": "^_"
    }],
    "no-unreachable": "error",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

### ts-prune for Exports

```bash
# Install
npm install -g ts-prune

# Run
ts-prune

# With ignore patterns
ts-prune --ignore "index.ts"
```

## Confidence Scoring

| Confidence | Criteria | Recommendation |
|------------|----------|----------------|
| **High** | Zero references, private scope, no dynamic patterns | Safe to remove |
| **Medium** | Only test file references, behind feature flag | Verify before removing |
| **Low** | Dynamic invocation possible, public export | Manual review required |

### Dynamic Usage Patterns (Low Confidence)

```typescript
// Object bracket notation
handlers[eventName](); // Can't know which handlers are used

// Reflection/decorators
@Injectable()
class Service { } // Framework may use reflection

// String-based method calls
obj[methodName](); // Runtime determined

// eval/Function constructor
eval('functionName()'); // Cannot statically analyze
```

## Grep Patterns for Detection

```bash
# Find function definitions
grep -rn "function \w\+\s*(" --include="*.ts"
grep -rn "const \w\+ = (" --include="*.ts"  # Arrow functions
grep -rn "^\s*\w\+\s*(" --include="*.ts"    # Method definitions

# Count references to a function name
grep -c "functionName" src/**/*.ts

# Find unused exports (basic)
# 1. List all exports
grep -rhn "^export " src/ --include="*.ts"
# 2. For each export, search for imports
grep -r "import.*exportName" src/
```

## Auto-Fix Patterns

### Remove Unused Variable

```diff
- const unused = 42;
  const used = computeValue();
```

### Remove Unused Import After Removing Variable

```diff
- import { helperA, helperB } from './helpers';
+ import { helperA } from './helpers';

- const result = helperB(); // Removed usage
```

### Remove Unreachable Code

```diff
  function getValue() {
    return 42;
-   console.log('cleanup');
-   performCleanup();
  }
```

### Prefix Unused Parameters

```diff
- function handler(req, res, next) {
+ function handler(req, _res, next) {
    // res not used but required by signature
    next();
  }
```
