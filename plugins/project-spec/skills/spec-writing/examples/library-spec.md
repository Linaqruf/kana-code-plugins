# Project Specification: timeparse

> Lightweight, type-safe library for parsing, formatting, and manipulating dates with an intuitive API.

## Overview

### Problem Statement
Parsing and formatting dates/times in JavaScript is inconsistent, with native Date APIs being verbose and error-prone, leading to bugs in timezone handling and format parsing.

### Solution
timeparse is a lightweight, type-safe library for parsing, formatting, and manipulating dates with an intuitive API inspired by day.js but with modern TypeScript design and zero runtime dependencies.

### Target Users
- **Primary**: JavaScript/TypeScript developers
- **Secondary**: Library authors needing date utilities
- **Technical Level**: Technical (developers)

### Success Criteria
- [ ] Parse ISO 8601 and common date formats (MM/DD/YYYY, DD-MM-YYYY) with 100% accuracy
- [ ] Format dates with template strings in under 0.1ms per call
- [ ] Handle timezone conversions using IANA timezone names
- [ ] Bundle size under 5KB minified + gzipped (measured via `size-limit`)

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: Date Parsing
**Description**: Parse date strings from various formats into a unified TimeDate object.
**User Story**: As a developer, I want to parse date strings so that I can work with user input reliably.
**Acceptance Criteria**:
- [ ] Parse ISO 8601 strings (full and partial: `2024-01-15`, `2024-01-15T10:30:00Z`)
- [ ] Parse common formats: MM/DD/YYYY, DD-MM-YYYY, YYYY/MM/DD, MMM DD YYYY
- [ ] Return `null` for invalid dates (never throw)
- [ ] Support custom format strings via `TimeDate.parse(input, 'DD/MM/YYYY')`

#### Feature 2: Date Formatting
**Description**: Format TimeDate objects into human-readable strings.
**User Story**: As a developer, I want to format dates so that I can display them to users.
**Acceptance Criteria**:
- [ ] Format tokens: YYYY, YY, MM, M, DD, D, HH, hh, mm, ss, A, a
- [ ] Relative formatting: "2 hours ago", "in 3 days", "just now" (threshold: <60s)
- [ ] Localization: en, es, fr, de, ja (locale affects month names and relative text)

#### Feature 3: Date Manipulation
**Description**: Add, subtract, and compare dates with a fluent API.
**User Story**: As a developer, I want to manipulate dates so that I can calculate deadlines and intervals.
**Acceptance Criteria**:
- [ ] Add/subtract: days, months, years, hours, minutes, seconds
- [ ] Compare: `isBefore`, `isAfter`, `isSame` (with optional unit granularity)
- [ ] Boundary: `startOf('month')`, `endOf('year')` for all units
- [ ] Diff: `diff(other, 'days')` returns signed integer

#### Feature 4: Timezone Support
**Description**: Convert dates between timezones.
**User Story**: As a developer, I want to handle timezones so that I can display correct times globally.
**Acceptance Criteria**:
- [ ] Convert to/from UTC: `.utc()`, `.local()`
- [ ] Convert to IANA timezone: `.tz('America/New_York')`
- [ ] Detect user's local timezone via `Intl.DateTimeFormat`

### Future Scope (Post-MVP)
1. Calendar utilities (week of year, day of year, ISO week number)
2. Duration parsing ("2h 30m" → milliseconds)
3. Recurring date patterns (every Monday, first of month)
4. Date range utilities (overlap detection, iteration)
5. Framework plugins (React hook `useTimeDate`, Vue composable)

### Out of Scope
- Full calendar UI components
- Date picker widgets
- Server-side scheduling / cron

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale | Alternatives Considered |
|-------|------------|-----------|------------------------|
| Language | TypeScript | Type safety, excellent IDE support, source of truth for docs | JavaScript (no types), Rust+WASM (overkill for date lib) |
| Build | tsup | Fast builds, ESM+CJS dual output, tree-shaking, dts generation | Rollup (more config), esbuild (no dts), tsc (slow, no bundling) |
| Testing | Vitest | Fast, native ESM, snapshot testing, good for library testing | Jest (slower, CJS-first), node:test (minimal assertion library) |
| Docs | TypeDoc | Generates from TSDoc comments, zero manual maintenance | Docusaurus (heavier, manual), hand-written (maintenance burden) |
| Linting | Biome | Single tool for lint + format, 10-100x faster than ESLint + Prettier | ESLint+Prettier (slower, two configs) |
| Size check | size-limit | Enforce bundle size budget in CI | bundlesize (less maintained) |

### System Design

```
+-----------------------------------------------------+
|                    timeparse                         |
+-----------------------------------------------------+
|  +---------+  +---------+  +---------+  +--------+  |
|  |  parse  |  | format  |  |  manip  |  |   tz   |  |
|  +----+----+  +----+----+  +----+----+  +---+----+  |
|       |            |            |           |       |
|       +------------+-----+------+-----------+       |
|                          |                          |
|                    +-----+-----+                    |
|                    |   core    |                    |
|                    | (TimeDate)|                    |
|                    +-----------+                    |
+-----------------------------------------------------+
```

All modules are pure functions operating on the immutable TimeDate class. No side effects, no global state.

---

## Public API

### Core Class: TimeDate

```typescript
class TimeDate {
  // Constructors
  constructor(input?: DateInput);
  static parse(input: string, format?: string): TimeDate | null;
  static now(): TimeDate;

  // Formatting
  format(template: string): string;      // format('YYYY-MM-DD') → "2024-01-15"
  toISO(): string;                        // "2024-01-15T10:30:00.000Z"
  toRelative(): string;                   // "2 hours ago"

  // Manipulation (returns new instance — immutable)
  add(amount: number, unit: Unit): TimeDate;
  subtract(amount: number, unit: Unit): TimeDate;
  startOf(unit: Unit): TimeDate;
  endOf(unit: Unit): TimeDate;

  // Comparison
  isBefore(other: TimeDate): boolean;
  isAfter(other: TimeDate): boolean;
  isSame(other: TimeDate, unit?: Unit): boolean;
  diff(other: TimeDate, unit: Unit): number;  // signed integer

  // Timezone
  tz(timezone: string): TimeDate;         // .tz('America/New_York')
  utc(): TimeDate;
  local(): TimeDate;

  // Getters (read-only)
  year(): number;
  month(): number;    // 1-12 (not 0-11 like native Date)
  day(): number;      // 1-31
  hour(): number;     // 0-23
  minute(): number;   // 0-59
  second(): number;   // 0-59

  // Conversion
  toDate(): Date;      // native Date object
  valueOf(): number;   // Unix timestamp (ms)
  toJSON(): string;    // ISO string (for JSON.stringify)
}
```

### Types

```typescript
type DateInput = Date | string | number | TimeDate;

type Unit =
  | 'year' | 'years' | 'y'
  | 'month' | 'months' | 'M'
  | 'week' | 'weeks' | 'w'
  | 'day' | 'days' | 'd'
  | 'hour' | 'hours' | 'h'
  | 'minute' | 'minutes' | 'm'
  | 'second' | 'seconds' | 's';

interface FormatOptions {
  locale?: string;     // 'en' | 'es' | 'fr' | 'de' | 'ja'
  timezone?: string;   // IANA timezone name
}
```

### Format Tokens

| Token | Output | Description |
|-------|--------|-------------|
| YYYY | 2024 | 4-digit year |
| YY | 24 | 2-digit year |
| MM | 01-12 | Month (zero-padded) |
| M | 1-12 | Month |
| DD | 01-31 | Day (zero-padded) |
| D | 1-31 | Day |
| HH | 00-23 | Hour 24h (zero-padded) |
| hh | 01-12 | Hour 12h (zero-padded) |
| mm | 00-59 | Minute (zero-padded) |
| ss | 00-59 | Second (zero-padded) |
| A | AM/PM | Uppercase meridiem |
| a | am/pm | Lowercase meridiem |

---

## Bundle Size Strategy

- **Target**: < 5KB minified + gzipped
- **Zero runtime dependencies**: All functionality self-contained
- **Tree-shakeable exports**: Named exports only, no default export with class methods
- **Locale splitting**: Locales loaded on-demand via subpath exports (`timeparse/locales/ja`)
- **Intl.DateTimeFormat**: Leverage browser/Node built-in for timezone conversion (no bundled tz data)
- **CI enforcement**: `size-limit` check in GitHub Actions, PR blocked if budget exceeded

### Size Budget

| Export | Max Size |
|--------|----------|
| `timeparse` (core) | 3KB gzip |
| `timeparse/locales/[lang]` | 0.5KB gzip each |
| Total (core + 5 locales) | 5.5KB gzip |

---

## Algorithm: Timezone Conversion

**Purpose**: Convert a TimeDate from one timezone to another without bundling timezone data.

**Approach**: Use `Intl.DateTimeFormat` with `timeZone` option (available in all modern runtimes).

**Steps**:
1. Store internal time as UTC milliseconds (single source of truth)
2. To display in timezone: create `Intl.DateTimeFormat` with target `timeZone`
3. Format parts via `formatToParts()` to extract year, month, day, hour, minute, second
4. Cache `Intl.DateTimeFormat` instances per timezone string (avoid re-creation)

**Edge cases**:
- Invalid timezone name → throw `Error("Unknown timezone: [name]")` (only place library throws)
- DST transitions → `Intl.DateTimeFormat` handles automatically
- Ambiguous times during fall-back → defer to runtime behavior (matches native Date)

**Why this approach**: Avoids bundling 30KB+ of timezone data. Relies on runtime Intl support which is universal in Node 18+ and all modern browsers.

---

## Algorithm: Format Token Parsing

**Purpose**: Convert a template string like `'YYYY-MM-DD HH:mm'` into formatted output.

**Steps**:
1. Tokenize template: scan left-to-right, greedily match longest token first
2. Token priority: `YYYY` before `YY`, `MM` before `M`, `DD` before `D`
3. Non-token characters pass through as-is
4. Apply token → value mapping using TimeDate getters

**Example**: `format('DD/MM/YYYY')` on Jan 5, 2024
- Tokens found: `DD`, `/`, `MM`, `/`, `YYYY`
- Values: `05`, `/`, `01`, `/`, `2024`
- Result: `"05/01/2024"`

---

## Data Models

#### TimeDate Internal State
```typescript
// Internal representation (not exposed)
interface TimeDateInternal {
  _ms: number;          // UTC milliseconds (source of truth)
  _tz: string | null;   // Target timezone for display (null = local)
}
```

#### Locale Definition
```typescript
interface Locale {
  code: string;                              // 'en', 'ja'
  months: [string, ...string[]] & { length: 12 };
  monthsShort: [string, ...string[]] & { length: 12 };
  weekdays: [string, ...string[]] & { length: 7 };
  weekdaysShort: [string, ...string[]] & { length: 7 };
  relativeTime: {
    past: string;       // '%s ago'
    future: string;     // 'in %s'
    s: string;          // 'just now'
    m: string;          // '1 minute'
    mm: string;         // '%d minutes'
    h: string;          // '1 hour'
    hh: string;         // '%d hours'
    d: string;          // '1 day'
    dd: string;         // '%d days'
    M: string;          // '1 month'
    MM: string;         // '%d months'
    y: string;          // '1 year'
    yy: string;         // '%d years'
  };
}
```

---

## File Structure

```
timeparse/
├── src/
│   ├── index.ts           # Main exports (TimeDate, types)
│   ├── timedate.ts        # Core TimeDate class
│   ├── parse.ts           # Parsing logic (ISO, custom formats)
│   ├── format.ts          # Format token engine
│   ├── manipulate.ts      # Add/subtract/startOf/endOf
│   ├── compare.ts         # isBefore/isAfter/isSame/diff
│   ├── timezone.ts        # Timezone conversion via Intl
│   ├── relative.ts        # Relative time formatting
│   ├── locales/
│   │   ├── index.ts       # Locale registry + default (en)
│   │   ├── en.ts
│   │   ├── es.ts
│   │   ├── fr.ts
│   │   ├── de.ts
│   │   └── ja.ts
│   ├── utils/
│   │   ├── constants.ts   # MS_PER_DAY, MONTHS_PER_YEAR, etc.
│   │   └── tokens.ts      # Token definitions and priority
│   └── types.ts           # Public TypeScript types
├── tests/
│   ├── parse.test.ts
│   ├── format.test.ts
│   ├── manipulate.test.ts
│   ├── compare.test.ts
│   ├── timezone.test.ts
│   ├── relative.test.ts
│   └── fixtures/
│       └── dates.ts       # Known date/format pairs for testing
├── package.json
├── tsconfig.json
├── tsup.config.ts
├── vitest.config.ts
└── README.md
```

---

## Dependencies

### Production Dependencies
```json
{
  "dependencies": {}
}
```
*Zero runtime dependencies — all functionality is self-contained.*

### Development Dependencies
```json
{
  "devDependencies": {
    "typescript": "^5.3.0",
    "tsup": "^8.0.0",
    "vitest": "^1.0.0",
    "@biomejs/biome": "^1.4.0",
    "typedoc": "^0.25.0",
    "size-limit": "^11.0.0",
    "@size-limit/preset-small-lib": "^11.0.0"
  }
}
```

---

## Package Configuration

### package.json
```json
{
  "name": "timeparse",
  "version": "1.0.0",
  "description": "Lightweight, type-safe date parsing and formatting",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    },
    "./locales/*": {
      "import": "./dist/locales/*.js",
      "require": "./dist/locales/*.cjs"
    }
  },
  "files": ["dist"],
  "sideEffects": false,
  "keywords": ["date", "time", "parse", "format", "timezone"],
  "license": "MIT",
  "engines": {
    "node": ">=18"
  },
  "scripts": {
    "build": "tsup",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "lint": "biome check .",
    "docs": "typedoc src/index.ts",
    "size": "size-limit",
    "prepublishOnly": "npm run build && npm run test && npm run size"
  },
  "size-limit": [
    { "path": "dist/index.js", "limit": "3 KB" }
  ]
}
```

### tsup.config.ts
```typescript
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts', 'src/locales/*.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  clean: true,
  minify: true,
  treeshake: true,
  splitting: true,
});
```

---

## Development Phases

### Phase 1: Foundation
**Depends on**: Nothing
- [ ] Project setup: TypeScript, tsup, Vitest, Biome
- [ ] Core TimeDate class with internal UTC storage
- [ ] Basic parsing: ISO 8601 (full and partial)
- [ ] Basic formatting: YYYY, MM, DD, HH, mm, ss tokens
- [ ] `toDate()`, `valueOf()`, `toJSON()` conversions

### Phase 2: Core Features
**Depends on**: Phase 1 (TimeDate class must exist)
- [ ] Extended format parsing (MM/DD/YYYY, DD-MM-YYYY, custom format strings)
- [ ] All manipulation methods (add, subtract, startOf, endOf)
- [ ] Comparison methods (isBefore, isAfter, isSame, diff)
- [ ] Relative time formatting ("2 hours ago")

### Phase 3: Advanced Features
**Depends on**: Phase 2 (manipulation and formatting must work)
- [ ] Timezone support via Intl.DateTimeFormat
- [ ] Intl formatter caching
- [ ] Localization system (en, es, fr, de, ja)
- [ ] Subpath exports for locales
- [ ] Edge case handling (DST, leap years, month overflow)

### Phase 4: Polish & Publish
**Depends on**: Phase 3 (all features must work)
- [ ] Test coverage > 95% (focus on edge cases: DST, leap years, format ambiguities)
- [ ] TypeDoc API documentation
- [ ] size-limit CI check (fail build if > 5KB)
- [ ] Performance benchmarks vs day.js and date-fns
- [ ] README with quick start, API reference, and migration guide
- [ ] npm publish

---

## Open Questions

| # | Question | Options | Impact | Status |
|---|----------|---------|--------|--------|
| 1 | Support legacy browsers (< ES2020)? | A) No (Intl required), B) Yes (polyfill guide) | Affects timezone implementation and bundle size | Open |
| 2 | Plugin system for extensibility? | A) Yes (register custom formats/locales), B) No (subpath exports only) | Adds API surface but enables community extensions | Open |
| 3 | Subpath exports per feature? | A) Yes (`timeparse/parse`, `timeparse/format`), B) No (single entry) | Enables smaller bundles but more complex package.json | Open |

---

## References

### Documentation
- [TC39 Temporal Proposal](https://tc39.es/proposal-temporal/docs/) — future standard, inform API design
- [IANA Time Zone Database](https://www.iana.org/time-zones)
- [Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)

### Similar Libraries
- day.js — API inspiration (similar fluent interface)
- date-fns — function-based alternative (tree-shakeable but larger)
- Luxon — full-featured (but 20KB+ gzipped)

### Design Decisions
- **Immutable API**: All methods return new instances (prevents mutation bugs)
- **Null over exceptions**: `parse()` returns null for invalid input (never throws, except invalid timezone)
- **Month 1-indexed**: `.month()` returns 1-12 (not 0-11 like native Date, which causes bugs)
- **ESM-first**: Primary export is ESM with CJS fallback for legacy bundlers
- **Intl-based timezones**: No bundled tz data — keeps bundle small, relies on runtime support

---

*Generated with project-spec plugin for Claude Code*
