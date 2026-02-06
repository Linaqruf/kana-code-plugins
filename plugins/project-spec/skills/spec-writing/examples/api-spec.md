# Project Specification: BookmarkAPI

> Self-hosted REST API for saving, organizing, and searching bookmarks with automatic metadata extraction.

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
- [ ] CRUD operations on bookmarks complete in under 100ms at p95
- [ ] Metadata extraction succeeds for 90%+ of valid URLs
- [ ] Full-text search returns results in under 200ms for 10,000+ bookmarks

---

## Product Requirements

### Core Features (MVP)

#### Feature 1: Bookmark CRUD
**Description**: Create, read, update, delete bookmarks with metadata.
**User Story**: As a developer, I want to save bookmarks via API so that I can build integrations.
**Acceptance Criteria**:
- [ ] POST creates bookmark, returns 201 with created resource
- [ ] GET lists bookmarks with pagination (default 20, max 100 per page)
- [ ] PUT updates bookmark fields, returns 200
- [ ] DELETE removes bookmark, returns 204

#### Feature 2: Automatic Metadata
**Description**: Extract title, description, and favicon from URLs automatically.
**User Story**: As a user, I want bookmarks to have titles automatically so that I don't have to enter them manually.
**Acceptance Criteria**:
- [ ] Fetch page title from `<title>` tag or `og:title` meta
- [ ] Extract description from `<meta name="description">` or `og:description`
- [ ] Store favicon URL from `<link rel="icon">` or `/favicon.ico` fallback
- [ ] If fetch fails (timeout after 10s, non-2xx response, invalid HTML): save bookmark with URL as title, empty description, null favicon

#### Feature 3: Tags & Organization
**Description**: Tag bookmarks for organization and filtering.
**User Story**: As a user, I want to tag bookmarks so that I can organize them by topic.
**Acceptance Criteria**:
- [ ] Add up to 20 tags per bookmark (tag name: 1-50 chars, lowercase alphanumeric + hyphens)
- [ ] Filter bookmarks by one or more tags (AND logic)
- [ ] GET /tags returns all tags with bookmark counts, sorted by count descending

#### Feature 4: Search
**Description**: Full-text search across bookmark titles and descriptions.
**User Story**: As a user, I want to search my bookmarks so that I can find saved links.
**Acceptance Criteria**:
- [ ] Search by title, description, and URL using PostgreSQL full-text search
- [ ] Filter search results by tag
- [ ] Results ranked by relevance (ts_rank), paginated

### Future Scope (Post-MVP)
1. Collections/folders for grouping bookmarks
2. Import/export (Netscape HTML format, JSON)
3. Browser extension API integration
4. Archive/snapshot of pages via Wayback Machine
5. Public sharing links with optional expiry

### Out of Scope
- User interface (API only)
- Social features (sharing, likes)
- Full-page archiving/crawling

---

## Technical Architecture

### Tech Stack

| Layer | Technology | Rationale | Alternatives Considered |
|-------|------------|-----------|------------------------|
| Language | Python 3.11+ | Async ecosystem, fast prototyping, rich HTTP libraries | Node.js (good but team prefers Python), Go (faster but slower dev) |
| Framework | FastAPI | Async-native, auto-generates OpenAPI docs, Pydantic validation built-in | Flask (no async), Django REST (heavier, more opinionated) |
| Database | PostgreSQL | Full-text search built-in (no extra service), ACID compliance, relational integrity | SQLite (no concurrent writes), MongoDB (weak for relational tag queries) |
| ORM | SQLAlchemy 2.0 | Async support, mature ecosystem, flexible query builder | Tortoise ORM (smaller community), raw SQL (no migration tooling) |
| Validation | Pydantic v2 | FastAPI integration, 5-50x faster than v1, JSON Schema generation | Marshmallow (older, no FastAPI integration) |
| Metadata | httpx + BeautifulSoup | httpx for async HTTP, BeautifulSoup for HTML parsing | requests (sync-only), lxml (faster but harder install) |
| Search | PostgreSQL FTS | Built-in tsvector/tsquery, no extra service, good enough for <100k docs | Elasticsearch (overkill for MVP), Meilisearch (extra service) |
| Deployment | Docker | Portable, self-hosted, reproducible environments | Direct install (not portable), Kubernetes (overkill) |

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
                        │   (async httpx) │
                        └─────────────────┘
```

### Data Model Relations

```
User (1) ──────< (N) Bookmark
User (1) ──────< (N) Tag
Bookmark (N) >─< (N) Tag  (via BookmarkTag)
```

---

## Data Models

#### User
```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    api_key_hash: Mapped[str] = mapped_column(String(64))  # SHA-256 hash
    api_key_prefix: Mapped[str] = mapped_column(String(12))  # "bk_live_..." for display
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

#### Bookmark
```python
class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    url: Mapped[str] = mapped_column(String(2048), index=True)
    title: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    favicon: Mapped[str | None] = mapped_column(String(2048))
    is_read: Mapped[bool] = mapped_column(default=False)
    is_favorite: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow)

    # Full-text search vector (auto-updated via trigger)
    search_vector: Mapped[str] = mapped_column(TSVECTOR)

    __table_args__ = (
        UniqueConstraint("user_id", "url"),  # One bookmark per URL per user
        Index("ix_bookmarks_search", "search_vector", postgresql_using="gin"),
    )
```

#### Tag
```python
class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(50))

    __table_args__ = (UniqueConstraint("user_id", "name"),)
```

#### BookmarkTag
```python
class BookmarkTag(Base):
    __tablename__ = "bookmark_tags"

    bookmark_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookmarks.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
```

#### Validation Schemas (Pydantic)
```python
class BookmarkCreate(BaseModel):
    url: HttpUrl                          # Validated URL format
    title: str | None = None              # Auto-fetched if omitted
    description: str | None = None        # Auto-fetched if omitted
    tags: list[str] = Field(default=[], max_length=20)
    is_favorite: bool = False

    @field_validator("tags")
    def validate_tags(cls, v):
        for tag in v:
            if not re.match(r"^[a-z0-9][a-z0-9-]{0,49}$", tag):
                raise ValueError(f"Tag '{tag}' must be lowercase alphanumeric with hyphens, 1-50 chars")
        return v
```

---

## API Endpoints

### Authentication
All endpoints require `X-API-Key` header. Keys are prefixed with `bk_live_` for identification.

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| GET | /api/v1/bookmarks | List bookmarks (paginated, filterable) | 100/min |
| POST | /api/v1/bookmarks | Create bookmark | 30/min |
| GET | /api/v1/bookmarks/:id | Get single bookmark | 100/min |
| PUT | /api/v1/bookmarks/:id | Update bookmark | 30/min |
| DELETE | /api/v1/bookmarks/:id | Delete bookmark | 10/min |
| GET | /api/v1/tags | List all tags with counts | 100/min |
| GET | /api/v1/search | Search bookmarks (full-text) | 60/min |
| POST | /api/v1/auth/register | Register and get API key | 5/min |

→ *For full request/response schemas, see SPEC/api-reference.md*

---

## Security

### API Key Management
- Keys generated as `bk_live_` + 32 random bytes (base64url encoded)
- Stored as SHA-256 hash in database (original key shown only once at registration)
- Key prefix (`bk_live_...xxxx`, last 4 chars) stored separately for display
- Key rotation: POST /api/v1/auth/rotate generates new key, old key valid for 24 hours

### Rate Limiting
- Implemented via sliding window counter in PostgreSQL (no Redis dependency for MVP)
- Limits per API key, not per IP
- Returns `429 Too Many Requests` with `Retry-After` header (seconds until reset)

### Input Validation
- All request bodies validated by Pydantic schemas (type coercion + constraints)
- URL validation: must be valid HTTP/HTTPS URL (no file://, javascript://, data:// schemes)
- SQL injection: SQLAlchemy parameterized queries only
- Tag names sanitized: lowercase, alphanumeric + hyphens only

### Metadata Fetcher Security
- Timeout: 10 seconds per URL fetch
- Block private IP ranges (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) — prevent SSRF
- Max response body: 1MB (prevent memory exhaustion)
- User-Agent: `BookmarkAPI/1.0` (identify the bot)

---

## Error Handling Strategy

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid URL format",
    "details": {
      "field": "url",
      "value": "not-a-url",
      "constraint": "Must be a valid HTTP or HTTPS URL"
    }
  }
}
```

### Error Codes
| Code | HTTP Status | When |
|------|-------------|------|
| UNAUTHORIZED | 401 | Missing or invalid API key |
| NOT_FOUND | 404 | Bookmark or tag not found (or belongs to different user) |
| VALIDATION_ERROR | 422 | Request body fails Pydantic validation |
| DUPLICATE_URL | 409 | Bookmark with same URL already exists for this user |
| RATE_LIMITED | 429 | Too many requests (includes Retry-After header) |
| METADATA_FETCH_FAILED | 200 | URL metadata could not be fetched (non-blocking, bookmark still created) |
| SERVER_ERROR | 500 | Unexpected internal error (logged to Sentry) |

---

## Algorithm: Metadata Extraction

**Purpose**: Extract title, description, and favicon from a URL when creating a bookmark.

**Steps**:
1. Send GET request to URL with 10s timeout, max 1MB response body
2. Parse HTML with BeautifulSoup
3. Extract title: `og:title` meta → `<title>` tag → URL hostname as fallback
4. Extract description: `og:description` → `<meta name="description">` → first 200 chars of `<p>` → null
5. Extract favicon: `<link rel="icon">` href → `<link rel="shortcut icon">` → `/favicon.ico` → null
6. Store extracted metadata on bookmark

**Edge cases**:
- URL returns non-HTML content type (PDF, image) → use URL as title, null description
- URL redirects more than 5 times → abort, save with URL as title
- URL returns 403/451 → save bookmark without metadata, log warning
- URL is behind authentication (returns login page) → extract whatever is on login page
- Connection refused / DNS failure → save bookmark with URL as title

### Algorithm: Search Ranking

**Purpose**: Rank search results by relevance using PostgreSQL full-text search.

**Implementation**:
- Search vector: `setweight(to_tsvector(title), 'A') || setweight(to_tsvector(description), 'B')`
- Title matches weighted 2x over description matches
- Results sorted by `ts_rank(search_vector, query)` descending
- Tie-breaker: `created_at` descending (newest first)

---

## File Structure

```
bookmark-api/
├── src/
│   ├── main.py              # FastAPI application + lifespan
│   ├── config.py            # Pydantic Settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── bookmark.py
│   │   └── tag.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── bookmark.py      # Pydantic request/response schemas
│   │   ├── tag.py
│   │   └── error.py         # Error response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── bookmarks.py
│   │   ├── tags.py
│   │   ├── search.py
│   │   └── auth.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bookmark.py      # Business logic
│   │   ├── metadata.py      # URL metadata fetcher
│   │   └── search.py        # Full-text search service
│   ├── core/
│   │   ├── database.py      # Async engine + session factory
│   │   ├── security.py      # API key hashing, validation
│   │   ├── rate_limit.py    # Sliding window rate limiter
│   │   └── exceptions.py    # Custom exception handlers
│   └── middleware/
│       ├── auth.py           # API key authentication
│       └── rate_limit.py     # Rate limiting middleware
├── tests/
│   ├── conftest.py           # Fixtures: test client, test DB
│   ├── test_bookmarks.py
│   ├── test_tags.py
│   ├── test_search.py
│   └── test_metadata.py
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

## Monitoring & Observability

| Aspect | Tool | Purpose |
|--------|------|---------|
| Error tracking | Sentry | Capture unhandled exceptions with request context |
| Logging | Python `logging` + structlog | Structured JSON logs with request ID |
| Health check | `GET /health` | Return `{ status, version, db_connected, uptime_seconds }` |
| API docs | Swagger UI (`/docs`) | Auto-generated from FastAPI/Pydantic schemas |

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL async connection string | Yes | - |
| API_KEY_SALT | Salt for API key hashing | Yes | - |
| RATE_LIMIT_PER_MINUTE | Default requests per minute | No | 60 |
| METADATA_TIMEOUT_SECONDS | URL fetch timeout | No | 10 |
| METADATA_MAX_BODY_BYTES | Max response body for metadata fetch | No | 1048576 |
| LOG_LEVEL | Logging level | No | INFO |
| SENTRY_DSN | Sentry error tracking DSN | No | - |
| CORS_ORIGINS | Allowed CORS origins (comma-separated) | No | * |

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
    "structlog>=23.2.0",
    "sentry-sdk[fastapi]>=1.39.0",
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
    "coverage>=7.3.0",
]
```

---

## Development Phases

### Phase 1: Foundation
**Depends on**: Nothing
- [ ] FastAPI project setup with async SQLAlchemy
- [ ] Database models (User, Bookmark, Tag, BookmarkTag)
- [ ] Alembic migrations with full-text search index
- [ ] Basic CRUD endpoints for bookmarks

### Phase 2: Core Features
**Depends on**: Phase 1 (models + CRUD must exist)
- [ ] Metadata extraction service (httpx + BeautifulSoup)
- [ ] Tag management (create-on-write, filter, counts)
- [ ] Pagination and filtering (by tag, favorite, read status)
- [ ] API key authentication middleware

### Phase 3: Search & Security
**Depends on**: Phase 2 (bookmarks with metadata must exist for meaningful search)
- [ ] PostgreSQL full-text search with weighted ranking
- [ ] Rate limiting (sliding window)
- [ ] SSRF protection in metadata fetcher
- [ ] Input validation hardening

### Phase 4: Deployment & Docs
**Depends on**: Phase 3 (API must be complete and secure)
- [ ] Docker configuration (multi-stage build)
- [ ] docker-compose with PostgreSQL
- [ ] Health check endpoint
- [ ] Sentry integration
- [ ] README with API examples

---

## Open Questions

| # | Question | Options | Impact | Status |
|---|----------|---------|--------|--------|
| 1 | Support batch operations? | A) Yes (POST /bookmarks/batch, max 50), B) No (single create only) | Batch import is common use case but adds complexity | Open |
| 2 | Archive integration? | A) Wayback Machine API check, B) Local snapshot, C) Skip for MVP | Dead link detection is valuable but scope risk | Open |
| 3 | Webhook support? | A) Yes (POST to user URL on bookmark events), B) No | Enables integrations but adds delivery guarantee complexity | Open |

---

## References

→ *For full endpoint request/response schemas: `SPEC/api-reference.md`*

### Documentation
- [FastAPI](https://fastapi.tiangolo.com)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [PostgreSQL Full-Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- [Pydantic v2](https://docs.pydantic.dev/latest/)

### Similar APIs
- [Pocket API](https://getpocket.com/developer/)
- [Raindrop.io API](https://developer.raindrop.io)
- [Pinboard API](https://pinboard.in/api/)

---

*Generated with project-spec plugin for Claude Code*
