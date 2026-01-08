# Project Specification: BookmarkAPI

## Overview

### Problem Statement
Developers need a simple, self-hosted bookmarking service with a clean API for saving, organizing, and retrieving links across devices and applications.

### Solution
BookmarkAPI is a REST API service for managing bookmarks with tagging, search, and metadata extraction capabilities.

### Target Users
- **Primary**: Developers building bookmark integrations
- **Secondary**: Power users wanting self-hosted bookmarks
- **Technical Level**: Technical (API consumers)

### Success Criteria
- [ ] RESTful API for CRUD operations on bookmarks
- [ ] Automatic metadata extraction from URLs
- [ ] Tag-based organization and search
- [ ] API key authentication

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: Bookmark CRUD
**Description**: Create, read, update, delete bookmarks with metadata.
**User Story**: As a developer, I want to save bookmarks via API so that I can build integrations.
**Acceptance Criteria**:
- [ ] POST endpoint to create bookmarks
- [ ] GET endpoint to list/retrieve bookmarks
- [ ] PUT endpoint to update bookmarks
- [ ] DELETE endpoint to remove bookmarks

#### Feature 2: Automatic Metadata
**Description**: Extract title, description, and favicon from URLs automatically.
**User Story**: As a user, I want bookmarks to have titles automatically so that I don't have to enter them manually.
**Acceptance Criteria**:
- [ ] Fetch page title from URL
- [ ] Extract meta description
- [ ] Store favicon URL
- [ ] Graceful fallback if fetch fails

#### Feature 3: Tags & Organization
**Description**: Tag bookmarks for organization and filtering.
**User Story**: As a user, I want to tag bookmarks so that I can organize them by topic.
**Acceptance Criteria**:
- [ ] Add/remove tags on bookmarks
- [ ] Filter bookmarks by tag
- [ ] List all tags with counts

#### Feature 4: Search
**Description**: Full-text search across bookmark titles and descriptions.
**User Story**: As a user, I want to search my bookmarks so that I can find saved links.
**Acceptance Criteria**:
- [ ] Search by title, description, URL
- [ ] Search by tag
- [ ] Paginated results

### Future Scope (Post-MVP)
1. Collections/folders for grouping
2. Import/export (Netscape format, JSON)
3. Browser extension API
4. Archive/snapshot of pages
5. Public sharing links

### Out of Scope
- User interface (API only)
- Social features (sharing, likes)
- Full-page archiving

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Language | Python 3.11+ | Fast development, good libraries |
| Framework | FastAPI | Modern, async, auto-docs |
| Database | PostgreSQL | Full-text search, reliability |
| ORM | SQLAlchemy 2.0 | Async support, mature |
| Validation | Pydantic v2 | FastAPI integration, performance |
| Metadata | BeautifulSoup | HTML parsing for extraction |
| Search | PostgreSQL FTS | Built-in, no extra service |
| Deployment | Docker | Portable, self-hosted |

### System Design

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   API Client    │────▶│   FastAPI       │────▶│   PostgreSQL    │
│   (any)         │◀────│   Application   │◀────│   Database      │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Metadata      │
                        │   Fetcher       │
                        │   (async)       │
                        └─────────────────┘
```

### Data Models

#### User (for multi-tenancy)
```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    api_key: Mapped[str] = mapped_column(unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

#### Bookmark
```python
class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    url: Mapped[str] = mapped_column(index=True)
    title: Mapped[str | None]
    description: Mapped[str | None]
    favicon: Mapped[str | None]
    is_read: Mapped[bool] = mapped_column(default=False)
    is_favorite: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow)

    # Full-text search vector
    search_vector: Mapped[str] = mapped_column(TSVECTOR)
```

#### Tag
```python
class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]

    __table_args__ = (UniqueConstraint("user_id", "name"),)
```

#### BookmarkTag (Association)
```python
class BookmarkTag(Base):
    __tablename__ = "bookmark_tags"

    bookmark_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookmarks.id"))
    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tags.id"))
```

---

## API Endpoints

### Authentication
All endpoints require `X-API-Key` header.

### Bookmarks

#### List Bookmarks
```http
GET /api/v1/bookmarks
X-API-Key: <key>

Query Parameters:
- page (int): Page number, default 1
- limit (int): Items per page, default 20, max 100
- tag (string): Filter by tag name
- q (string): Search query
- is_favorite (bool): Filter favorites
- is_read (bool): Filter read status
- sort (string): created_at | updated_at, default -created_at

Response: 200 OK
{
  "data": [
    {
      "id": "uuid",
      "url": "https://example.com",
      "title": "Example",
      "description": "An example website",
      "favicon": "https://example.com/favicon.ico",
      "tags": ["tech", "reference"],
      "is_read": false,
      "is_favorite": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

#### Create Bookmark
```http
POST /api/v1/bookmarks
X-API-Key: <key>
Content-Type: application/json

{
  "url": "https://example.com",
  "title": "Optional title",      // Auto-fetched if omitted
  "description": "Optional desc", // Auto-fetched if omitted
  "tags": ["tech", "reference"],
  "is_favorite": false
}

Response: 201 Created
{
  "data": { ... }
}
```

#### Get Bookmark
```http
GET /api/v1/bookmarks/:id
X-API-Key: <key>

Response: 200 OK
{
  "data": { ... }
}
```

#### Update Bookmark
```http
PUT /api/v1/bookmarks/:id
X-API-Key: <key>
Content-Type: application/json

{
  "title": "Updated title",
  "tags": ["new-tag"],
  "is_read": true
}

Response: 200 OK
{
  "data": { ... }
}
```

#### Delete Bookmark
```http
DELETE /api/v1/bookmarks/:id
X-API-Key: <key>

Response: 204 No Content
```

### Tags

#### List Tags
```http
GET /api/v1/tags
X-API-Key: <key>

Response: 200 OK
{
  "data": [
    { "name": "tech", "count": 25 },
    { "name": "reference", "count": 12 }
  ]
}
```

### Search

#### Search Bookmarks
```http
GET /api/v1/search?q=python+tutorial
X-API-Key: <key>

Response: 200 OK
{
  "data": [...],
  "pagination": {...}
}
```

---

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid URL format",
    "details": {
      "field": "url",
      "value": "not-a-url"
    }
  }
}
```

### Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| UNAUTHORIZED | 401 | Invalid or missing API key |
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 422 | Invalid request data |
| DUPLICATE_URL | 409 | Bookmark already exists |
| RATE_LIMITED | 429 | Too many requests |
| SERVER_ERROR | 500 | Internal error |

---

## File Structure

```
bookmark-api/
├── src/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── bookmark.py
│   │   └── tag.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── bookmark.py      # Pydantic schemas
│   │   └── tag.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── bookmarks.py
│   │   ├── tags.py
│   │   └── search.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bookmark.py      # Business logic
│   │   ├── metadata.py      # URL metadata fetcher
│   │   └── search.py        # Search service
│   ├── core/
│   │   ├── database.py      # DB connection
│   │   ├── security.py      # Auth utilities
│   │   └── exceptions.py    # Custom exceptions
│   └── utils/
│       └── pagination.py
├── tests/
│   ├── conftest.py
│   ├── test_bookmarks.py
│   └── test_search.py
├── migrations/
│   └── versions/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── alembic.ini
├── pyproject.toml
└── README.md
```

---

## Dependencies

### Production Dependencies
```toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "asyncpg>=0.29.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "httpx>=0.25.0",
    "beautifulsoup4>=4.12.0",
    "alembic>=1.12.0",
]
```

### Development Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.25.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]
```

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection | Yes | - |
| API_KEY_SALT | Salt for API key hashing | Yes | - |
| RATE_LIMIT | Requests per minute | No | 60 |
| METADATA_TIMEOUT | URL fetch timeout (s) | No | 10 |
| LOG_LEVEL | Logging level | No | INFO |

---

## Development Phases

### Phase 1: Foundation
- [ ] FastAPI project setup
- [ ] Database models with SQLAlchemy
- [ ] Alembic migrations
- [ ] Basic CRUD endpoints

### Phase 2: Core Features
- [ ] Metadata extraction service
- [ ] Tag management
- [ ] Pagination and filtering
- [ ] API key authentication

### Phase 3: Search & Polish
- [ ] PostgreSQL full-text search
- [ ] Rate limiting
- [ ] Error handling
- [ ] Input validation

### Phase 4: Deployment
- [ ] Docker configuration
- [ ] API documentation (OpenAPI)
- [ ] README and usage docs
- [ ] CI/CD setup

---

## Open Questions

- [ ] Should we support batch operations (create multiple)?
- [ ] Archive/wayback integration for dead links?
- [ ] Webhook support for integrations?

---

## References

### Documentation
- [FastAPI](https://fastapi.tiangolo.com)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org)
- [PostgreSQL Full-Text Search](https://www.postgresql.org/docs/current/textsearch.html)

### Similar APIs
- Pocket API
- Raindrop.io API
- Pinboard API

---

*Generated with project-spec plugin for Claude Code*
