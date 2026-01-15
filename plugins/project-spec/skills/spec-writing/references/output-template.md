# Project Specification Template

Use this template as the base structure for generating `SPEC.md` (Quick mode). Adapt sections based on project type—not all sections apply to every project.

---

```markdown
# Project Specification: [Project Name]

## Overview

### Problem Statement
[1-2 sentences describing the problem this project solves]

### Solution
[1-2 sentences describing how this project solves the problem]

### Target Users
- **Primary**: [Who is the main user?]
- **Secondary**: [Any other user types?]
- **Technical Level**: [Developer / Technical User / Non-Technical]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: [Feature Name]
**Description**: [What does this feature do?]
**User Story**: As a [user type], I want to [action] so that [benefit].
**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

#### Feature 2: [Feature Name]
**Description**: [What does this feature do?]
**User Story**: As a [user type], I want to [action] so that [benefit].
**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

#### Feature 3: [Feature Name]
**Description**: [What does this feature do?]
**User Story**: As a [user type], I want to [action] so that [benefit].
**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Future Scope (Post-MVP)
1. [Future feature 1]
2. [Future feature 2]
3. [Future feature 3]

### Out of Scope
- [Explicitly not included 1]
- [Explicitly not included 2]

### User Flows

#### [Primary User Flow Name]
1. User [action 1]
2. System [response 1]
3. User [action 2]
4. System [response 2]

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | [Framework] | [Why this choice] |
| Styling | [CSS Solution] | [Why this choice] |
| Backend | [Framework] | [Why this choice] |
| Database | [Database] | [Why this choice] |
| ORM | [ORM/Query Builder] | [Why this choice] |
| Deployment | [Platform] | [Why this choice] |
| Auth | [Solution] | [Why this choice] |

### System Design

```
[ASCII diagram or description of system architecture]

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Server    │────▶│  Database   │
│  (Next.js)  │◀────│   (API)     │◀────│ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
```

### Data Models

#### [Model 1 Name]
```typescript
interface ModelName {
  id: string;           // Primary key
  field1: string;       // Description
  field2: number;       // Description
  createdAt: Date;      // Timestamp
  updatedAt: Date;      // Timestamp
}
```

#### [Model 2 Name]
```typescript
interface ModelName {
  id: string;           // Primary key
  field1: string;       // Description
  foreignId: string;    // Reference to [Other Model]
}
```

### API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /api/resource | List all resources | Required |
| GET | /api/resource/:id | Get single resource | Required |
| POST | /api/resource | Create resource | Required |
| PUT | /api/resource/:id | Update resource | Required |
| DELETE | /api/resource/:id | Delete resource | Required |

### Authentication & Authorization

**Strategy**: [JWT / Session / OAuth / etc.]

**User Roles**:
- **Admin**: [Permissions]
- **User**: [Permissions]
- **Guest**: [Permissions]

### Third-Party Integrations

| Service | Purpose | Notes |
|---------|---------|-------|
| [Service 1] | [What for] | [API key required, etc.] |
| [Service 2] | [What for] | [Notes] |


---

## Design System

*Include this section for web applications and frontend projects.*

### Visual Identity

**Brand Colors**:
| Name | Value | Usage |
|------|-------|-------|
| Primary | `#3B82F6` | CTAs, links, focus states |
| Secondary | `#6366F1` | Accents, highlights |
| Success | `#10B981` | Success states, confirmations |
| Warning | `#F59E0B` | Warnings, cautions |
| Error | `#EF4444` | Errors, destructive actions |
| Neutral | `#6B7280` | Text, borders, backgrounds |

**Typography**:
| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | Inter | 36px | 700 |
| H2 | Inter | 30px | 600 |
| H3 | Inter | 24px | 600 |
| Body | Inter | 16px | 400 |
| Small | Inter | 14px | 400 |
| Code | JetBrains Mono | 14px | 400 |

**Spacing Scale**: 4px base unit (4, 8, 12, 16, 24, 32, 48, 64, 96)

### Responsive Breakpoints

| Name | Width | Target |
|------|-------|--------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablet |
| lg | 1024px | Desktop |
| xl | 1280px | Large desktop |
| 2xl | 1536px | Extra large |

### Component Library

**UI Components Needed**:
- [ ] Button (primary, secondary, ghost, destructive)
- [ ] Input (text, email, password, search)
- [ ] Select / Dropdown
- [ ] Checkbox / Radio
- [ ] Modal / Dialog
- [ ] Toast / Notification
- [ ] Card
- [ ] Table
- [ ] Navigation (header, sidebar, tabs)
- [ ] Form layouts

**Component States**:
- Default, Hover, Focus, Active, Disabled, Loading, Error

### Page Layouts

| Page | Layout Type | Key Components |
|------|-------------|----------------|
| Landing | Marketing | Hero, Features, CTA |
| Dashboard | App shell | Sidebar, Header, Main content |
| Auth | Centered | Form card, Logo |
| Settings | Two-column | Nav, Content panel |

### Accessibility Requirements

- **WCAG Level**: AA (minimum)
- **Color contrast**: 4.5:1 for normal text, 3:1 for large text
- **Focus indicators**: Visible on all interactive elements
- **Screen reader**: ARIA labels on icons and complex components
- **Keyboard navigation**: Full support for tab, enter, escape
- **Reduced motion**: Respect `prefers-reduced-motion`

### Interaction Patterns

**Animations**:
- Transitions: 150ms ease-out (micro), 300ms ease-in-out (page)
- Loading: Skeleton screens preferred over spinners
- Feedback: Immediate visual response on interactions

**Error Handling UX**:
- Inline validation on blur
- Form-level errors at top
- Toast for async operation failures
---

## File Structure

```
project-name/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── (public)/        # Public routes
│   │   ├── (auth)/          # Authenticated routes
│   │   ├── api/             # API routes
│   │   └── layout.tsx       # Root layout
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   └── [feature]/       # Feature-specific components
│   ├── lib/                 # Utilities and helpers
│   ├── hooks/               # Custom React hooks
│   └── types/               # TypeScript types
├── prisma/
│   └── schema.prisma        # Database schema
├── public/                  # Static assets
├── tests/                   # Test files
├── .env.example             # Environment template
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
    "[package]": "^[version]",
    "[package]": "^[version]"
  }
}
```

### Development Dependencies
```json
{
  "devDependencies": {
    "[package]": "^[version]",
    "[package]": "^[version]"
  }
}
```

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | Database connection string | Yes | - |
| NEXT_PUBLIC_API_URL | Public API base URL | Yes | - |
| [OTHER_VAR] | [Description] | [Yes/No] | [Default] |

---

## Development Phases

### Phase 1: Foundation
- [ ] Project setup and configuration
- [ ] Database schema design
- [ ] Authentication implementation
- [ ] Basic UI scaffolding

### Phase 2: Core Features
- [ ] [Core feature 1]
- [ ] [Core feature 2]
- [ ] [Core feature 3]

### Phase 3: Polish & Launch
- [ ] Error handling and validation
- [ ] Loading states and UX polish
- [ ] Testing
- [ ] Deployment setup
- [ ] Documentation

---

## Open Questions

Decisions that need to be made during development:

- [ ] [Question 1 - e.g., "Which email service to use?"]
- [ ] [Question 2 - e.g., "File storage approach?"]
- [ ] [Question 3 - e.g., "Caching strategy?"]

---

## References

### Documentation
- [Tech 1 Docs](url)
- [Tech 2 Docs](url)

### Inspirations
- [Reference project 1](url)
- [Reference project 2](url)

### Design Resources
- [Design system](url)
- [UI kit](url)

---

*Generated with project-spec plugin for Claude Code*
```

---

## Template Variations

### CLI Tool Template

For CLI tools, replace certain sections:

```markdown
## Commands

### Main Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `tool init` | Initialize configuration | `--template <name>` |
| `tool run` | Run the main operation | `--input <file>` |
| `tool help` | Show help | - |

### Configuration

```yaml
# config.yaml
setting1: value
setting2: value
```

### Output Formats
- JSON (default)
- YAML
- Plain text

### Distribution
- npm package: `npm install -g tool-name`
- Binary releases: GitHub Releases
```

### API-Only Template

For pure APIs, simplify frontend sections:

```markdown
## API Design

### Resource: [Resource Name]

**Base URL**: `/api/v1/resource`

#### List Resources
```http
GET /api/v1/resource
Authorization: Bearer <token>

Query Parameters:
- page (number): Page number, default 1
- limit (number): Items per page, default 20
- sort (string): Sort field, default "createdAt"

Response: 200 OK
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

#### Create Resource
```http
POST /api/v1/resource
Authorization: Bearer <token>
Content-Type: application/json

{
  "field1": "value",
  "field2": "value"
}

Response: 201 Created
{
  "data": { ... }
}
```
```

### Library Template

For libraries/packages:

```markdown
## Public API

### Core Functions

#### functionName(params)
**Description**: [What it does]
**Parameters**:
- `param1` (type): Description
- `param2` (type, optional): Description

**Returns**: `ReturnType` - Description

**Example**:
```typescript
import { functionName } from 'library-name';

const result = functionName(param1, param2);
```

### Types

```typescript
export interface ConfigOptions {
  option1: string;
  option2?: number;
}

export type ResultType = {
  success: boolean;
  data: unknown;
};
```

### Publishing

**npm**:
```bash
npm publish
```

**Version Strategy**: Semantic Versioning
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes
```

---

## Writing Guidelines

### Be Specific
❌ "Handle user data"
✅ "Store user profiles with fields: id, email, name, avatar, createdAt"

### Be Actionable
❌ "Implement good error handling"
✅ "Return structured errors with code, message, and details fields"

### Include Examples
❌ "Support multiple output formats"
✅ "Support JSON (default), YAML (--format yaml), and CSV (--format csv)"

### Link to Documentation
❌ "Use Prisma for database"
✅ "Use Prisma for database ([docs](https://prisma.io/docs))"

### Keep MVP Focused
❌ "Implement full social features, notifications, real-time chat..."
✅ "MVP: User profiles, basic messaging. Future: Notifications, real-time."
