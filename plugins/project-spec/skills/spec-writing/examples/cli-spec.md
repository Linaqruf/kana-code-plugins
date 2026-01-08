# Project Specification: envcheck

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
- [ ] Validate .env files against a schema definition
- [ ] Clear error messages with fix suggestions
- [ ] Exit codes suitable for CI/CD integration

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: Schema Definition
**Description**: Define expected environment variables with types and constraints.
**User Story**: As a developer, I want to define what env vars my app needs so that I can validate them.
**Acceptance Criteria**:
- [ ] Support YAML schema format
- [ ] Define variable name, type, required/optional
- [ ] Support types: string, number, boolean, url, email
- [ ] Custom regex patterns

#### Feature 2: Validation Command
**Description**: Validate environment against schema.
**User Story**: As a developer, I want to check my .env file so that I catch misconfigurations early.
**Acceptance Criteria**:
- [ ] `envcheck validate` command
- [ ] Read from .env file or system environment
- [ ] Report all errors, not just first
- [ ] Exit code 0 on success, 1 on failure

#### Feature 3: Init Command
**Description**: Generate schema from existing .env file.
**User Story**: As a developer, I want to generate a schema from my current .env so that I can start validating quickly.
**Acceptance Criteria**:
- [ ] `envcheck init` command
- [ ] Infer types from values
- [ ] Generate .envcheck.yaml file

#### Feature 4: CI/CD Integration
**Description**: Output formats suitable for automated pipelines.
**User Story**: As a DevOps engineer, I want to run envcheck in CI so that deployments fail fast on misconfigurations.
**Acceptance Criteria**:
- [ ] JSON output format option
- [ ] GitHub Actions compatible exit codes
- [ ] Quiet mode for minimal output

### Future Scope (Post-MVP)
1. `.env.example` generation from schema
2. Secret detection and warnings
3. Environment comparison (dev vs prod)
4. VS Code extension integration
5. Auto-fix suggestions that write to .env

### Out of Scope
- Secret management or storage
- Remote environment fetching
- GUI interface

---

## Commands

### Main Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `envcheck validate` | Validate env against schema | `--schema <file>`, `--env <file>`, `--format <json\|text>` |
| `envcheck init` | Generate schema from .env | `--env <file>`, `--output <file>` |
| `envcheck check <var>` | Check single variable | Variable name |
| `envcheck help` | Show help | - |
| `envcheck version` | Show version | - |

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--schema, -s` | Path to schema file | `.envcheck.yaml` |
| `--env, -e` | Path to .env file | `.env` |
| `--format, -f` | Output format (text, json) | `text` |
| `--quiet, -q` | Minimal output | `false` |
| `--strict` | Fail on warnings too | `false` |

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Language | Node.js (TypeScript) | Wide ecosystem, easy npm distribution |
| CLI Framework | Commander.js | Mature, well-documented |
| Schema Parser | js-yaml | Standard YAML parsing |
| Validation | Zod | Type-safe validation |
| Output | Chalk | Colored terminal output |
| Testing | Vitest | Fast, ESM-native |

### System Design

```
┌─────────────────┐
│   CLI Entry     │
│   (index.ts)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   Commands      │────▶│   Validators    │
│  validate.ts    │     │  (per type)     │
│  init.ts        │     └─────────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   Schema        │     │   Reporters     │
│   Parser        │     │  text, json     │
└─────────────────┘     └─────────────────┘
```

### Data Models

#### Schema Definition
```typescript
interface EnvSchema {
  version: '1.0';
  variables: Record<string, VariableSchema>;
}

interface VariableSchema {
  type: 'string' | 'number' | 'boolean' | 'url' | 'email';
  required?: boolean;
  default?: string;
  pattern?: string;        // Regex pattern
  description?: string;
  examples?: string[];
}
```

#### Validation Result
```typescript
interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

interface ValidationError {
  variable: string;
  message: string;
  expected?: string;
  received?: string;
  suggestion?: string;
}
```

### Configuration

#### .envcheck.yaml Schema Format
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
```

---

## File Structure

```
envcheck/
├── src/
│   ├── index.ts           # CLI entry point
│   ├── commands/
│   │   ├── validate.ts    # validate command
│   │   ├── init.ts        # init command
│   │   └── check.ts       # check command
│   ├── lib/
│   │   ├── schema.ts      # Schema parser
│   │   ├── validator.ts   # Validation logic
│   │   ├── env.ts         # Env file parser
│   │   └── types.ts       # TypeScript types
│   ├── validators/
│   │   ├── string.ts
│   │   ├── number.ts
│   │   ├── boolean.ts
│   │   ├── url.ts
│   │   └── email.ts
│   └── reporters/
│       ├── text.ts        # Terminal output
│       └── json.ts        # JSON output
├── tests/
│   ├── validate.test.ts
│   ├── init.test.ts
│   └── fixtures/
│       ├── valid.env
│       └── invalid.env
├── package.json
├── tsconfig.json
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

Result: 2 errors, 0 warnings
```

### JSON Output
```json
{
  "valid": false,
  "errors": [
    {
      "variable": "DATABASE_URL",
      "message": "Required variable is missing",
      "suggestion": "Add DATABASE_URL to your .env file"
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
    "total": 4,
    "valid": 2,
    "errors": 2,
    "warnings": 0
  }
}
```

---

## Distribution

### npm Package
```bash
# Install globally
npm install -g envcheck

# Or use npx
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

## Development Phases

### Phase 1: Foundation
- [ ] Project setup with TypeScript
- [ ] Commander.js CLI scaffolding
- [ ] Basic validate command structure
- [ ] Schema parsing

### Phase 2: Core Validation
- [ ] Type validators (string, number, boolean)
- [ ] URL and email validators
- [ ] Pattern matching support
- [ ] Error reporting with suggestions

### Phase 3: Additional Features
- [ ] Init command for schema generation
- [ ] JSON output format
- [ ] Check single variable command
- [ ] Quiet mode

### Phase 4: Polish & Publish
- [ ] Comprehensive tests
- [ ] Error handling edge cases
- [ ] README documentation
- [ ] npm publish

---

## Open Questions

- [ ] Support for .env.local, .env.development patterns?
- [ ] Should we warn about unused variables in .env?
- [ ] Integration with monorepo tools (turborepo, nx)?

---

## References

### Documentation
- [Commander.js](https://github.com/tj/commander.js)
- [Chalk](https://github.com/chalk/chalk)
- [Zod](https://zod.dev)

### Similar Tools
- dotenv-linter (Rust)
- env-cmd (Node.js)
- direnv (Shell)

---

*Generated with project-spec plugin for Claude Code*
