# CLI Reference Template

> Command-line interface documentation. Create if project is CLI tool.

```markdown
## CLI Reference

> Command-line interface for [Project Name]

## Installation

```bash
# npm
npm install -g [package]

# cargo
cargo install [package]

# homebrew
brew install [package]
```

## Usage

```bash
[command] [subcommand] [options]
```

## Global Options

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Show help |
| `--version` | `-V` | Show version |
| `--verbose` | `-v` | Verbose output |
| `--quiet` | `-q` | Quiet mode |

## Commands

### `[command] init`

Initialize [something].

```bash
[command] init [options]
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--template` | `default` | Template to use |
| `--force` | `false` | Overwrite existing |

---

### `[command] [action]`

[Description]

```bash
[command] [action] <required> [optional]
```

**Arguments:**

| Arg | Required | Description |
|-----|----------|-------------|
| `<required>` | Yes | [Description] |
| `[optional]` | No | [Description] |

---

## Configuration

### Config File

| Platform | Path |
|----------|------|
| Linux | `~/.config/[app]/config.toml` |
| macOS | `~/Library/Application Support/[app]/config.toml` |
| Windows | `%APPDATA%\[app]\config.toml` |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `[APP]_CONFIG` | Config path |
| `[APP]_LOG_LEVEL` | Log level |

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Error |
| 2 | Invalid args |

---

*Related: Architecture*
```

## When to Create

- Project is CLI tool
- Project has CLI component
