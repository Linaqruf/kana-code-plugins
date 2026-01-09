---
name: spec-writing
description: Use when the user wants to create project specs, design systems, or feature plans. Triggers on "create spec", "plan project", "design system", "plan feature", or "write specification".
version: 1.0.2
---

# Spec Writing

Generate comprehensive project specification documents through structured interviews. This skill transforms vague project ideas into actionable specifications that serve as development guidelines.

## Purpose

Project specifications front-load critical decisions, reducing ambiguity and scope creep during development. A well-structured spec enables Claude Code to understand project context throughout the development lifecycle.

## Interview Workflow

### Phase 1: Product Requirements

Conduct interviews using AskUserQuestion with 2-4 questions per interaction. Avoid overwhelming with too many questions at once.

**Essential Questions:**

1. **Problem & Purpose**
   - What problem does this project solve?
   - What is the core value proposition?

2. **Target Users**
   - Who will use this? (developers, end-users, businesses)
   - What is their technical level?

3. **Core Features (MVP)**
   - What are the must-have features for launch?
   - What is the minimum viable product?

4. **Future Scope**
   - What features can wait for later versions?
   - What is out of scope?

5. **Inspirations**
   - Any existing products or examples to reference?
   - Design or UX inspirations?

### Phase 2: Technical Design

**Essential Questions:**

1. **Tech Stack**
   - Frontend framework preference? (React, Vue, Svelte, vanilla)
   - Backend preference? (Node, Python, Go, serverless)
   - Database needs? (SQL, NoSQL, none)

2. **Deployment**
   - Where will this run? (local, cloud, serverless, edge)
   - Any hosting preferences? (Vercel, AWS, self-hosted)

3. **Integrations**
   - Third-party APIs or services needed?
   - Authentication requirements?

4. **Performance**
   - Expected scale? (users, requests, data volume)
   - Real-time requirements?

5. **Security**
   - Sensitive data handling?
   - Compliance requirements? (GDPR, HIPAA)

### Phase 3: Constraints

**Essential Questions:**

1. **Team & Timeline**
   - Solo developer or team?
   - Any deadline expectations?

2. **Existing Code**
   - Integrating with existing codebase?
   - Any legacy constraints?

3. **Budget**
   - Constraints on paid services/tools?

## Context Gathering

After gathering requirements, fetch relevant documentation using Context7 MCP:

1. **Resolve library IDs** for chosen technologies
2. **Query documentation** for setup guides and best practices
3. **Validate compatibility** between chosen technologies

Example workflow:
```
1. User chooses Next.js + Prisma + PostgreSQL
2. Resolve: "next.js", "prisma", "postgresql"
3. Query: Setup guides, common patterns, integration tips
4. Include relevant insights in spec
```

## Output Generation

Generate `project_spec.md` in the project root with all sections. Use the template in `references/output-template.md` as the base structure.

### Section Guidelines

**Overview Section:**
- Problem statement in 1-2 sentences
- Clear success criteria
- Target user definition

**Product Requirements:**
- Prioritized feature list (MVP vs future)
- User stories in standard format
- Acceptance criteria where helpful

**Technical Architecture:**
- Tech stack with version recommendations
- System design overview
- Data models with field types
- API endpoints if applicable

**File Structure:**
- Proposed directory layout
- Key file purposes
- Naming conventions

**Development Phases:**
- Logical groupings of work
- Dependencies between phases
- No time estimates (per Claude Code guidelines)

**Open Questions:**
- Unresolved decisions as checkboxes
- Areas needing user input
- Technical uncertainties

## Project Type Templates

Adapt the interview and output based on project type:

### Web Application
Focus on: UI/UX, state management, routing, authentication, database schema
See: `examples/web-app-spec.md`

### CLI Tool
Focus on: Commands/subcommands, argument parsing, output formats, configuration
See: `examples/cli-spec.md`

### REST API
Focus on: Endpoints, authentication, rate limiting, documentation, versioning
See: `examples/api-spec.md`

### Library/Package
Focus on: Public API, documentation, testing, publishing, versioning
See: `examples/library-spec.md`

## Best Practices

### Interview Conduct
- Ask 2-4 questions maximum per interaction
- Provide sensible defaults when user is uncertain
- Skip irrelevant questions based on project type
- Summarize understanding before proceeding

### Specification Quality
- Be specific and actionable
- Include code examples where helpful
- Link to external documentation
- Keep scope realistic for MVP

### Iteration Support
- Specs can be updated as project evolves
- Mark changed sections clearly
- Maintain decision history in Open Questions

## Additional Resources

### Reference Files

For detailed question banks and templates:
- **`references/interview-questions.md`** - Complete question bank by category
- **`references/output-template.md`** - Full project_spec.md template

### Example Files

Working specification examples:
- **`examples/web-app-spec.md`** - Web application specification
- **`examples/cli-spec.md`** - CLI tool specification
- **`examples/api-spec.md`** - REST API specification
- **`examples/library-spec.md`** - Library/package specification
- **`examples/design-spec.md`** - Design system specification
- **`examples/feature-spec.md`** - Feature specification

## Design System Coverage

For frontend projects, include a Design System section in the specification. Use the `/design` command for dedicated design interviews.

### Phase 4: Design & UX (Frontend Projects)

**Essential Questions:**

1. **Visual Identity**
   - Existing brand guidelines or colors?
   - Aesthetic preference (modern, minimal, bold)?
   - Light mode, dark mode, or both?

2. **Component Library**
   - UI library preference (shadcn, Radix, Material)?
   - Icon library?
   - Custom component needs?

3. **Layout & Responsiveness**
   - Primary device target?
   - Navigation style?
   - Key page layouts?

4. **Accessibility**
   - WCAG compliance level?
   - Specific accessibility needs?

5. **Interaction Patterns**
   - Animation preferences?
   - Loading state style?
   - Error handling UX?

### Design System Section

For web applications, include in project_spec.md:

- **Visual Identity**: Colors, typography, spacing
- **Responsive Breakpoints**: Mobile, tablet, desktop
- **Component Library**: Selected library, core components
- **Accessibility**: WCAG level, focus states, screen reader support
- **Interaction Patterns**: Animations, loading states, error handling

See: `references/output-template.md` for the full Design System template.

### Dedicated Design Specification

For detailed design documentation, use the `/design` command to generate a separate `design_spec.md` with:

- Complete color palette with hex values
- Typography scale with weights and sizes
- Component specifications with states
- Page layout diagrams
- Accessibility checklist
- Animation timing guidelines

See: `examples/design-spec.md` for a complete example.

## Integration with frontend-design

The `frontend-design` skill can implement components based on the design specification:

1. Generate `project_spec.md` with `/spec` command
2. Generate `design_spec.md` with `/design` command (optional)
3. Use `frontend-design` skill to implement components following the spec

The design specification provides:
- Color values for Tailwind configuration
- Typography settings for CSS
- Component requirements for implementation
- Accessibility requirements for testing

## Feature Planning

For adding new functionality to existing projects, use the `/feature` command to generate a focused `feature_spec.md`.

### When to Use /feature

- Adding new functionality to an existing codebase
- Planning a feature before implementation
- Breaking down complex features into steps
- Documenting feature requirements for team alignment

### Feature Interview Flow

**Phase 1: Feature Definition**
- What does this feature do?
- What problem does it solve?
- How will users interact with it?

**Phase 2: Scope & Requirements**
- Must-have requirements (MVP)
- Explicitly out of scope
- Dependencies on other features

**Phase 3: Technical Approach**
- Existing patterns to follow
- API changes needed
- Database changes needed
- Third-party integrations

**Phase 4: Edge Cases & Testing**
- Key edge cases to handle
- Error states to design
- Testing strategy

### Feature Specification Sections

The generated `feature_spec.md` includes:

- **Overview**: Description, problem statement, user story
- **Requirements**: Must have, nice to have, out of scope
- **Technical Design**: Affected components, new components, API/DB changes
- **Implementation Plan**: Step-by-step tasks with dependencies
- **UI/UX**: User flows, component designs, states
- **Edge Cases**: Error handling, boundary conditions
- **Testing Strategy**: Unit, integration, E2E tests
- **Open Questions**: Unresolved decisions

See: `examples/feature-spec.md` for a complete example.

## Integration with feature-dev Skill

The `feature-dev` skill provides specialized agents for feature implementation:

### Workflow

1. **Plan**: Run `/feature` to create feature_spec.md
2. **Explore**: Use `code-explorer` agent to analyze relevant codebase patterns
3. **Design**: Use `code-architect` agent for detailed implementation blueprint
4. **Implement**: Build the feature following the spec and blueprint
5. **Review**: Use `code-reviewer` agent to verify implementation

### feature-dev Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `code-explorer` | Analyze existing patterns | Before implementation, understand codebase |
| `code-architect` | Design implementation | After spec, before coding |
| `code-reviewer` | Review implementation | After coding, before PR |

### Suggested Prompts

After creating a feature spec, suggest:

```
Feature spec created! Next steps:
1. Use feature-dev:code-explorer to analyze existing patterns
2. Use feature-dev:code-architect to design implementation
3. Implement following the plan
4. Use feature-dev:code-reviewer to verify
```
