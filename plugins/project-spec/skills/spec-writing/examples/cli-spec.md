# Project Specification: envcheck

> CLI tool that validates environment variables against a schema and provides actionable fix suggestions.

## Overview

### Problem Statement
Developers frequently encounter environment configuration issues that are difficult to diagnose, leading to wasted debugging time and inconsistent behavior across environments.

### Solution
envcheck is a CLI tool that validates environment variables against a schema, identifies missing or invalid values, and provides actionable suggestions for fixing issues.

### Target Users
- **Primary**: Developers working on Node.js/Python projects
- **Secondary**: DevOps engineers, CI/CD pipelines
- **Technical Level**: Technical (developers)

### Success Criteria
- [ ] Validate a 20-variable schema in under 500ms
- [ ] Exit codes compatible with GitHub Actions and CI/CD pipelines
- [ ] Error messages include specific fix suggestions (not just "invalid value")

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: Schema Definition
**Description**: Define expected environment variables with types and constraints.
**User Story**: As a developer, I want to define what env vars my app needs so that I can validate them.
**Acceptance Criteria**:
- [ ] YAML schema format (`.envcheck.yaml`)
- [ ] Fields: name, type, required (default: true), default, pattern, description, examples
- [ ] Supported types: string, number, boolean, url, email
- [ ] Custom regex patterns via `pattern` field

#### Feature 2: Validation Command
**Description**: Validate environment against schema.
**User Story**: As a developer, I want to check my .env file so that I catch misconfigurations early.
**Acceptance Criteria**:
- [ ] `envcheck validate` reads schema + env file, reports all errors (not just first)
- [ ] Sources: `.env` file (default), `--env <path>` flag, or system environment (`--system`)
- [ ] Exit code 0 on success, 1 on validation errors, 2 on config errors
- [ ] Shows per-variable status: checkmark for valid, X for invalid, with fix suggestion

#### Feature 3: Init Command
**Description**: Generate schema from existing .env file.
**User Story**: As a developer, I want to generate a schema from my current .env so that I can start validating quickly.
**Acceptance Criteria**:
- [ ] `envcheck init` reads `.env` and generates `.envcheck.yaml`
- [ ] Infers types from values using type inference algorithm
- [ ] Marks all variables as required (user can edit to optional)
- [ ] Preserves comments from .env as `description` fields

#### Feature 4: CI/CD Integration
**Description**: Output formats suitable for automated pipelines.
**User Story**: As a DevOps engineer, I want to run envcheck in CI so that deployments fail fast on misconfigurations.
**Acceptance Criteria**:
- [ ] `--format json` outputs machine-readable validation results
- [ ] `--quiet` suppresses all output except error count (for scripts)
- [ ] `--strict` treats warnings as errors (exit code 1)
- [ ] Exit codes: 0 (pass), 1 (validation errors), 2 (config error), 3 (runtime error)

### Future Scope (Post-MVP)
1. `.env.example` generation from schema
2. Secret detection and warnings (AWS keys, passwords, tokens)
3. Environment comparison (diff between .env.development and .env.production)
4. VS Code extension integration
5. Auto-fix mode that writes missing defaults to .env

### Out of Scope
- Secret management or encrypted storage
- Remote environment fetching (Vault, AWS SSM)
- GUI interface

---

## Commands

### Main Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `envcheck validate` | Validate env against schema | `--schema <file>`, `--env <file>`, `--format <json\|text>`, `--quiet`, `--strict`, `--system` |
| `envcheck init` | Generate schema from .env | `--env <file>`, `--output <file>` |
| `envcheck check <var>` | Check single variable | Variable name |
| `envcheck help` | Show help | - |
| `envcheck version` | Show version | - |

### Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--schema, -s` | Path to schema file | `.envcheck.yaml` |
| `--env, -e` | Path to .env file | `.env` |
| `--format, -f` | Output format (text, json) | `text` |
| `--quiet, -q` | Minimal output (error count only) | `false` |
| `--strict` | Treat warnings as errors | `false` |
| `--system` | Read from system environment instead of .env file | `false` |
| `--no-color` | Disable colored output | `false` |

### Exit Codes

| Code | Meaning | CI/CD Interpretation |
|------|---------|---------------------|
| 0 | All variables valid | Pipeline continues |
| 1 | Validation errors found | Pipeline fails |
| 2 | Configuration error (missing schema, invalid YAML) | Pipeline fails (setup issue) |
| 3 | Runtime error (file not found, permission denied) | Pipeline fails (infrastructure) |

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale | Alternatives Considered |
|-------|------------|-----------|------------------------|
| Language | TypeScript (Node.js) | Wide ecosystem, easy npm distribution, type safety | Go (faster binary but less ecosystem), Rust (complex for string-heavy CLI) |
| CLI Framework | Commander.js | Mature, well-documented, declarative subcommands | yargs (verbose), oclif (too heavy for simple CLI) |
| Schema Parser | js-yaml | Standard YAML parsing, lightweight | yaml (newer but less tested), TOML (less familiar to users) |
| Validation | Zod | Type-safe schema validation, great error messages | Joi (no TypeScript inference), Ajv (JSON Schema — more complex) |
| Output | Chalk | Colored terminal output, auto-detects color support | kleur (lighter but fewer features), picocolors (minimal) |
| Testing | Vitest | Fast, ESM-native, snapshot testing | Jest (slower, CJS-first) |
| Bundling | tsup | Fast, zero-config, ESM+CJS output | esbuild (manual config), rollup (more complex) |

### System Design

```
┌─────────────────┐
│   CLI Entry     │
│   (index.ts)    │
└────────┬────────┘
         │ parse args
         ▼
┌─────────────────┐
│   Commands      │
│  validate.ts    │
│  init.ts        │
│  check.ts       │
└────────┬────────┘
         │ load + validate
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────────┐
│ Schema │ │    Env     │
│ Parser │ │   Parser   │
└────┬───┘ └─────┬──────┘
     │           │
     ▼           ▼
┌─────────────────────┐
│     Validators      │
│  (per type: string, │
│  number, boolean,   │
│  url, email)        │
└────────┬────────────┘
         │ results
         ▼
┌─────────────────┐
│   Reporters     │
│  text.ts (tty)  │
│  json.ts (CI)   │
└─────────────────┘
```

---

## Data Models

#### Schema Definition
```typescript
interface EnvSchema {
  version: '1.0';
  variables: Record<string, VariableSchema>;
}

interface VariableSchema {
  type: 'string' | 'number' | 'boolean' | 'url' | 'email';
  required?: boolean;      // default: true
  default?: string;
  pattern?: string;        // Regex pattern for string type
  description?: string;
  examples?: string[];
}
```

#### Schema Validation (Zod)
```typescript
const variableSchemaValidator = z.object({
  type: z.enum(['string', 'number', 'boolean', 'url', 'email']),
  required: z.boolean().default(true),
  default: z.string().optional(),
  pattern: z.string().optional(),
  description: z.string().optional(),
  examples: z.array(z.string()).optional(),
});

const envSchemaValidator = z.object({
  version: z.literal('1.0'),
  variables: z.record(variableSchemaValidator),
});
```

#### Validation Result
```typescript
interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  summary: {
    total: number;
    valid: number;
    errors: number;
    warnings: number;
  };
}

interface ValidationError {
  variable: string;
  message: string;
  expected?: string;
  received?: string;
  suggestion?: string;    // Actionable fix
}

interface ValidationWarning {
  variable: string;
  message: string;
}
```

---

## Algorithm: Type Inference

**Purpose**: Infer the type of an environment variable value for `envcheck init`.

**Input**: String value from .env file
**Output**: One of `string | number | boolean | url | email`

**Rules** (evaluated in order, first match wins):
1. If value matches `^(true|false|yes|no|1|0)$` (case-insensitive) → `boolean`
2. If value matches `^https?://` → `url`
3. If value matches `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` → `email`
4. If value matches `^-?\d+(\.\d+)?$` → `number`
5. Otherwise → `string`

**Examples**:
| Value | Inferred Type | Rule Applied |
|-------|--------------|-------------|
| `"3000"` | `number` | Rule 4: numeric string |
| `"true"` | `boolean` | Rule 1: boolean literal |
| `"https://api.example.com"` | `url` | Rule 2: URL pattern |
| `"user@example.com"` | `email` | Rule 3: email pattern |
| `"production"` | `string` | Rule 5: default |
| `"yes"` | `boolean` | Rule 1: boolean alias |
| `"0"` | `boolean` | Rule 1: boolean numeric (0/1 preferred as boolean for env vars) |
| `"postgresql://..."` | `string` | Rule 5: non-HTTP URL (use `url` type only for HTTP) |

**Ambiguity handling**: When `"0"` or `"1"` could be number or boolean, prefer `boolean` because env vars use these as flags more often than as numeric values. Users can override in schema.

---

## Algorithm: Validation Pipeline

**Purpose**: Validate all environment variables against schema.

**Steps**:
1. Load schema from `.envcheck.yaml` (exit 2 if file missing or invalid YAML)
2. Load environment values from `.env` file or system environment
3. For each variable defined in schema:
   a. If value is missing and `required: true` → error: "Required variable is missing"
   b. If value is missing and `required: false` → skip (or use `default` if defined)
   c. If value is present → run type-specific validator
4. Check for variables in .env that are NOT in schema → warning: "Variable not defined in schema"
5. Aggregate results and return `ValidationResult`

**Type validators**:
| Type | Validation | Example Error |
|------|-----------|---------------|
| `string` | Non-empty (unless optional). If `pattern` set, match regex | "Value does not match pattern ^(dev\|prod)$" |
| `number` | Parseable as integer or float via `Number()`, not NaN | "Expected number, got 'abc'" |
| `boolean` | One of: true, false, yes, no, 1, 0 (case-insensitive) | "Expected boolean, got 'maybe'" |
| `url` | Valid HTTP or HTTPS URL (URL constructor doesn't throw) | "Expected URL, got 'not-a-url'" |
| `email` | Matches standard email regex | "Expected email, got 'user@'" |

---

## Configuration

#### .envcheck.yaml Example
```yaml
version: "1.0"
variables:
  DATABASE_URL:
    type: url
    required: true
    description: PostgreSQL connection string
    examples:
      - postgresql://user:pass@localhost:5432/db

  PORT:
    type: number
    required: false
    default: "3000"
    description: Server port

  NODE_ENV:
    type: string
    required: true
    pattern: "^(development|production|test)$"
    description: Environment mode

  DEBUG:
    type: boolean
    required: false
    default: "false"
    description: Enable debug logging

  ADMIN_EMAIL:
    type: email
    required: false
    description: Admin notification email
```

---

## Security

### Secret Detection (Future)
- Warn on common secret patterns: AWS keys (`AKIA...`), private keys (`-----BEGIN`), high-entropy strings (>4.5 bits/char for values >20 chars)
- Never print secret values in output (mask with `****` after first 4 chars)

### Schema Validation Safety
- Schema file is YAML: validate structure before processing to prevent YAML deserialization attacks
- Regex patterns from schema: wrap in try/catch to handle invalid regex gracefully (exit 2)
- File paths: resolve relative to CWD, reject absolute paths outside project root

---

## Output Formats

### Text Output (Default)
```
envcheck v1.0.0

Validating .env against .envcheck.yaml...

✗ DATABASE_URL
  Error: Required variable is missing
  Hint: Add DATABASE_URL to your .env file
  Example: postgresql://user:pass@localhost:5432/db

✗ NODE_ENV
  Error: Value "staging" does not match pattern
  Expected: development | production | test
  Received: staging

✓ PORT (using default: 3000)
✓ DEBUG
✓ ADMIN_EMAIL

Result: 2 errors, 0 warnings (3/5 valid)
```

### JSON Output (`--format json`)
```json
{
  "valid": false,
  "errors": [
    {
      "variable": "DATABASE_URL",
      "message": "Required variable is missing",
      "suggestion": "Add DATABASE_URL to your .env file",
      "examples": ["postgresql://user:pass@localhost:5432/db"]
    },
    {
      "variable": "NODE_ENV",
      "message": "Value does not match pattern",
      "expected": "^(development|production|test)$",
      "received": "staging"
    }
  ],
  "warnings": [],
  "summary": {
    "total": 5,
    "valid": 3,
    "errors": 2,
    "warnings": 0
  }
}
```

### Quiet Output (`--quiet`)
```
2 errors
```

---

## File Structure

```
envcheck/
├── src/
│   ├── index.ts           # CLI entry point (Commander setup)
│   ├── commands/
│   │   ├── validate.ts    # validate command handler
│   │   ├── init.ts        # init command handler
│   │   └── check.ts       # check single variable handler
│   ├── lib/
│   │   ├── schema.ts      # Schema loader + validator
│   │   ├── env-parser.ts  # .env file parser
│   │   ├── validator.ts   # Validation pipeline orchestrator
│   │   └── types.ts       # TypeScript interfaces
│   ├── validators/
│   │   ├── index.ts       # Validator registry (type → validator)
│   │   ├── string.ts
│   │   ├── number.ts
│   │   ├── boolean.ts
│   │   ├── url.ts
│   │   └── email.ts
│   ├── reporters/
│   │   ├── text.ts        # Colored terminal output
│   │   └── json.ts        # JSON output for CI/CD
│   └── utils/
│       └── type-inference.ts  # Type inference for init command
├── tests/
│   ├── validate.test.ts
│   ├── init.test.ts
│   ├── type-inference.test.ts
│   ├── validators/
│   │   ├── string.test.ts
│   │   ├── number.test.ts
│   │   ├── boolean.test.ts
│   │   ├── url.test.ts
│   │   └── email.test.ts
│   └── fixtures/
│       ├── valid.env
│       ├── invalid.env
│       ├── valid-schema.yaml
│       └── invalid-schema.yaml
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
  "dependencies": {
    "commander": "^11.1.0",
    "chalk": "^5.3.0",
    "js-yaml": "^4.1.0",
    "zod": "^3.22.0",
    "dotenv": "^16.3.0"
  }
}
```

### Development Dependencies
```json
{
  "devDependencies": {
    "typescript": "^5.3.0",
    "vitest": "^1.0.0",
    "@types/node": "^20.0.0",
    "@types/js-yaml": "^4.0.0",
    "tsup": "^8.0.0"
  }
}
```

---

## Distribution

### npm Package
```bash
# Install globally
npm install -g envcheck

# Or use npx (no install)
npx envcheck validate
```

### Package Configuration
```json
{
  "name": "envcheck",
  "version": "1.0.0",
  "bin": {
    "envcheck": "./dist/index.js"
  },
  "files": ["dist"],
  "engines": {
    "node": ">=18"
  }
}
```

---

## Error Handling Strategy

### Error Response Format (JSON mode)
```json
{
  "error": {
    "code": "CONFIG_ERROR",
    "message": "Schema file not found: .envcheck.yaml",
    "suggestion": "Run 'envcheck init' to generate a schema from your .env file"
  }
}
```

### Error Scenarios

| Scenario | Exit Code | Message |
|----------|-----------|---------|
| Schema file not found | 2 | "Schema file not found: [path]. Run 'envcheck init' to generate one." |
| Invalid YAML in schema | 2 | "Invalid YAML in schema: [parse error at line N]" |
| Invalid schema structure | 2 | "Schema validation failed: [Zod error details]" |
| .env file not found | 3 | "Environment file not found: [path]. Use --env to specify path or --system for system env." |
| Permission denied on file | 3 | "Permission denied: [path]" |
| Invalid regex in pattern | 2 | "Invalid regex pattern for [var]: [pattern]" |
| Validation errors found | 1 | Per-variable error details + summary |

---

## Development Phases

### Phase 1: Foundation
**Depends on**: Nothing
- [ ] Project setup: TypeScript, Commander.js, tsup, Vitest
- [ ] Schema parser: load `.envcheck.yaml`, validate structure with Zod
- [ ] Env parser: read `.env` file, parse key=value pairs
- [ ] CLI scaffolding: `validate`, `init`, `check`, `help`, `version` subcommands

### Phase 2: Core Validation
**Depends on**: Phase 1 (schema + env parser must work)
- [ ] Type validators: string, number, boolean, url, email
- [ ] Pattern matching (regex) for string type
- [ ] Validation pipeline: iterate schema, run validators, collect results
- [ ] Text reporter: colored output with checkmarks, X marks, suggestions

### Phase 3: Init & Output
**Depends on**: Phase 2 (validators must exist for init to infer types)
- [ ] Init command: read .env, infer types, generate `.envcheck.yaml`
- [ ] Type inference algorithm
- [ ] JSON reporter for CI/CD
- [ ] Quiet mode, strict mode
- [ ] `--system` flag (read from process.env instead of file)

### Phase 4: Polish & Publish
**Depends on**: Phase 3 (all features must work)
- [ ] Comprehensive tests (validators, init, edge cases)
- [ ] Error handling for all file I/O edge cases
- [ ] `--no-color` flag
- [ ] README with usage examples and CI/CD recipes
- [ ] npm publish with `prepublishOnly` hook

---

## Open Questions

| # | Question | Options | Impact | Status |
|---|----------|---------|--------|--------|
| 1 | Support .env.local, .env.development? | A) Yes (merge in priority order), B) No (single file) | Multi-file adds complexity but matches Next.js/Vite conventions | Open |
| 2 | Warn about unused variables? | A) Yes (warn for vars in .env not in schema), B) No | Catches typos but noisy for shared .env files | Open |
| 3 | Monorepo support? | A) Yes (--root flag, recursive schema search), B) No | Common use case but significant scope | Open |

---

## References

### Documentation
- [Commander.js](https://github.com/tj/commander.js)
- [Chalk v5](https://github.com/chalk/chalk)
- [Zod](https://zod.dev)
- [dotenv](https://github.com/motdotla/dotenv)

### Similar Tools
- dotenv-linter (Rust) — linting only, no schema validation
- env-cmd (Node.js) — env management, no validation
- direnv (Shell) — per-directory env, no type checking

---

*Generated with project-spec plugin for Claude Code*
