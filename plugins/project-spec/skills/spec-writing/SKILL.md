---
name: spec-writing
description: This skill should be used when the user asks to "create a project spec", "write a specification document", "plan a new project", "generate project_spec.md", "define project requirements", "create a design document", "update the project spec", "revise the specification", "add requirements to the spec", or mentions wanting to "plan before building", "document requirements", "structure a project", or "what should be in a project spec". Provides comprehensive guidance for interviewing users and generating project specification documents.
version: 1.0.0
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
Adapt questions for library consumers vs end users

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
