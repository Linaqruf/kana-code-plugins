# Changelog

All notable changes to the codebase-cleanup plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-09

### Fixed

- Skill description now uses third-person format per plugin-dev best practices

### Added

- Initial release of codebase-cleanup plugin
- **5 Specialized Agents:**
  - `import-analyzer` - Detects unused, duplicate, and circular imports
  - `dead-code-detector` - Finds unreachable code, unused functions/variables/exports
  - `asset-tracker` - Identifies unused images, CSS, fonts, and static files
  - `dependency-auditor` - Audits npm packages for unused deps, security issues, duplicates
  - `config-cleaner` - Finds unused env vars, obsolete configs, stale feature flags

- **Command:**
  - `/cleanup [scope]` - Main command with interactive scope selection
  - Supported scopes: `all`, `imports`, `deadcode`, `assets`, `deps`, `configs`
  - Multiple scope support via comma-separated values

- **Skill:**
  - `cleanup-patterns` - Comprehensive reference documentation
  - Reference files for import, dead-code, asset, and dependency patterns
  - Before/after cleanup examples

- **Hooks:**
  - Proactive suggestions on cleanup-related user prompts
  - Triggers on keywords: refactor, cleanup, remove unused, technical debt, dead code

- **Features:**
  - Interactive review with confirmation before changes
  - Confidence levels (High/Medium/Low) for all findings
  - Structured markdown reports with actionable recommendations
  - Framework support: React, Next.js, Vue, Vite, Svelte
  - Optional tool integration: depcheck, madge, ts-prune, npm audit
  - Windows path handling support
  - Invalid argument validation with helpful error messages
