# Project Specification: timeparse

## Overview

### Problem Statement
Parsing and formatting dates/times in JavaScript is inconsistent, with native Date APIs being verbose and error-prone, leading to bugs in timezone handling and format parsing.

### Solution
timeparse is a lightweight, type-safe library for parsing, formatting, and manipulating dates with an intuitive API inspired by day.js but with modern TypeScript design.

### Target Users
- **Primary**: JavaScript/TypeScript developers
- **Secondary**: Library authors needing date utilities
- **Technical Level**: Technical (developers)

### Success Criteria
- [ ] Parse common date string formats reliably
- [ ] Format dates with intuitive template strings
- [ ] Handle timezone conversions correctly
- [ ] Bundle size under 5KB minified+gzipped

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: Date Parsing
**Description**: Parse date strings from various formats into a unified Date object.
**User Story**: As a developer, I want to parse date strings so that I can work with user input reliably.
**Acceptance Criteria**:
- [ ] Parse ISO 8601 strings
- [ ] Parse common formats (MM/DD/YYYY, DD-MM-YYYY, etc.)
- [ ] Return null for invalid dates (no exceptions)
- [ ] Support custom format strings

#### Feature 2: Date Formatting
**Description**: Format Date objects into human-readable strings.
**User Story**: As a developer, I want to format dates so that I can display them to users.
**Acceptance Criteria**:
- [ ] Support format tokens (YYYY, MM, DD, HH, mm, ss)
- [ ] Support relative formatting ("2 hours ago")
- [ ] Localization support (en, es, fr, de, ja)

#### Feature 3: Date Manipulation
**Description**: Add, subtract, and compare dates with a fluent API.
**User Story**: As a developer, I want to manipulate dates so that I can calculate deadlines and intervals.
**Acceptance Criteria**:
- [ ] Add/subtract days, months, years, hours, minutes
- [ ] Compare dates (isBefore, isAfter, isSame)
- [ ] Get start/end of day, week, month, year

#### Feature 4: Timezone Support
**Description**: Convert dates between timezones.
**User Story**: As a developer, I want to handle timezones so that I can display correct times globally.
**Acceptance Criteria**:
- [ ] Convert to/from UTC
- [ ] Support IANA timezone names
- [ ] Detect user's local timezone

### Future Scope (Post-MVP)
1. Calendar utilities (week of year, day of year)
2. Duration parsing ("2h 30m")
3. Recurring date patterns
4. Date range utilities
5. Integration plugins (React hooks, Vue composables)

### Out of Scope
- Full calendar UI components
- Date picker widgets
- Server-side scheduling

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Language | TypeScript | Type safety, excellent DX |
| Build | tsup | Fast, ESM+CJS output |
| Testing | Vitest | Fast, native ESM support |
| Documentation | TypeDoc | Generate from TSDoc comments |
| Linting | Biome | Fast, unified linter/formatter |
| Publishing | npm | Standard JS package registry |

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

### Public API

#### Core Class: TimeDate

```typescript
class TimeDate {
  // Constructors
  constructor(input?: DateInput);
  static parse(input: string, format?: string): TimeDate | null;
  static now(): TimeDate;

  // Formatting
  format(template: string): string;
  toISO(): string;
  toRelative(): string;

  // Manipulation
  add(amount: number, unit: Unit): TimeDate;
  subtract(amount: number, unit: Unit): TimeDate;
  startOf(unit: Unit): TimeDate;
  endOf(unit: Unit): TimeDate;

  // Comparison
  isBefore(other: TimeDate): boolean;
  isAfter(other: TimeDate): boolean;
  isSame(other: TimeDate, unit?: Unit): boolean;
  diff(other: TimeDate, unit: Unit): number;

  // Timezone
  tz(timezone: string): TimeDate;
  utc(): TimeDate;
  local(): TimeDate;

  // Getters
  year(): number;
  month(): number;
  day(): number;
  hour(): number;
  minute(): number;
  second(): number;

  // Conversion
  toDate(): Date;
  valueOf(): number;
  toJSON(): string;
}
```

#### Types

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
  locale?: string;
  timezone?: string;
}
```

#### Format Tokens

| Token | Output | Description |
|-------|--------|-------------|
| YYYY | 2024 | 4-digit year |
| YY | 24 | 2-digit year |
| MM | 01-12 | Month (padded) |
| M | 1-12 | Month |
| DD | 01-31 | Day (padded) |
| D | 1-31 | Day |
| HH | 00-23 | Hour 24h (padded) |
| hh | 01-12 | Hour 12h (padded) |
| mm | 00-59 | Minute (padded) |
| ss | 00-59 | Second (padded) |
| A | AM/PM | Uppercase meridiem |
| a | am/pm | Lowercase meridiem |

---

## File Structure

```
timeparse/
├── src/
│   ├── index.ts           # Main exports
│   ├── timedate.ts        # Core TimeDate class
│   ├── parse.ts           # Parsing logic
│   ├── format.ts          # Formatting logic
│   ├── manipulate.ts      # Add/subtract/compare
│   ├── timezone.ts        # Timezone handling
│   ├── locales/
│   │   ├── index.ts       # Locale registry
│   │   ├── en.ts
│   │   ├── es.ts
│   │   └── ...
│   ├── utils/
│   │   ├── constants.ts   # Time constants
│   │   └── validators.ts  # Input validation
│   └── types.ts           # TypeScript types
├── tests/
│   ├── parse.test.ts
│   ├── format.test.ts
│   ├── manipulate.test.ts
│   ├── timezone.test.ts
│   └── fixtures/
│       └── dates.ts
├── docs/
│   └── api.md             # Generated API docs
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
*Note: Zero runtime dependencies for minimal bundle size*

### Development Dependencies
```json
{
  "devDependencies": {
    "typescript": "^5.3.0",
    "tsup": "^8.0.0",
    "vitest": "^1.0.0",
    "typedoc": "^0.25.0",
    "@biomejs/biome": "^1.4.0"
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
    "prepublishOnly": "npm run build && npm run test"
  }
}
```

### tsup.config.ts

```typescript
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  clean: true,
  minify: true,
  treeshake: true,
});
```

---

## Development Phases

### Phase 1: Foundation
- [ ] Project setup (TypeScript, tsup, Vitest)
- [ ] Core TimeDate class structure
- [ ] Basic parsing (ISO 8601)
- [ ] Basic formatting (common tokens)

### Phase 2: Core Features
- [ ] Extended format parsing
- [ ] All manipulation methods
- [ ] Comparison methods
- [ ] Relative time formatting

### Phase 3: Advanced Features
- [ ] Timezone support
- [ ] Localization system
- [ ] Custom format strings
- [ ] Edge case handling

### Phase 4: Polish & Publish
- [ ] Comprehensive test coverage (>90%)
- [ ] TypeDoc documentation
- [ ] Performance benchmarks
- [ ] README with examples
- [ ] npm publish

---

## Open Questions

- [ ] Should we support legacy browsers (IE11)?
- [ ] Include a plugin system for extensibility?
- [ ] Provide tree-shakeable subpath exports?

---

## References

### Documentation
- [TC39 Temporal Proposal](https://tc39.es/proposal-temporal/docs/)
- [IANA Time Zone Database](https://www.iana.org/time-zones)
- [Unicode CLDR](https://cldr.unicode.org/)

### Similar Libraries
- day.js (inspiration for API)
- date-fns (function-based alternative)
- Luxon (full-featured)

### Design Decisions
- Immutable API (all methods return new instances)
- Chainable methods for fluent API
- Null returns over exceptions for invalid input
- ESM-first with CJS fallback

---

*Generated with project-spec plugin for Claude Code*
