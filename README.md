# cc-plugins

A collection of Claude Code plugins by Linaqruf.

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add Linaqruf/cc-plugins
```

Then install any plugin:

```bash
/plugin install <plugin-name>@cc-plugins
```

## Available Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [project-spec](./plugins/project-spec) | Generate comprehensive project specifications through interactive interviews | 1.0.1 |

## Plugins

### project-spec

Generate comprehensive project specification documents through interactive interviews before you start building.

**Features:**
- `/spec` command for guided project planning
- `spec-writer` agent for autonomous planning assistance
- Auto-suggestion hook when starting new projects
- Context7 integration for tech stack documentation

**Install:**
```bash
/plugin install project-spec@cc-plugins
```

**Usage:**
```bash
/spec              # Full interview
/spec web-app      # Quick-start for web apps
/spec cli          # Quick-start for CLI tools
/spec api          # Quick-start for APIs
```

See [plugin documentation](./plugins/project-spec/README.md) for details.

## License

MIT
