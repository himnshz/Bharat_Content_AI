# Routes Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
│                   (app/main.py)                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─── CORS Middleware
                              ├─── API Documentation (/api/docs)
                              └─── Route Registration
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   Content     │          │  Translation  │          │  Social Media │
│   Routes      │          │   Routes      │          │    Routes     │
│               │          │               │          │               │
│ 14 endpoints  │          │  7 endpoints  │          │ 10 endpoints  │
└───────────────┘          └───────────────┘          └───────────────┘
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│  Analytics    │          │  Voice Input  │          │     Users     │
│   Routes      │          │    Routes     │          │    Routes     │
│               │          │               │          │               │
│  7 endpoints  │          │  6 endpoints  │          │  9 endpoints  │
└───────────────┘          └───────────────┘          └───────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │   Database Layer      │
                        │   (SQLAlchemy ORM)    │
                        └───────────────────────┘
                                    │
                        ┌───────────┴───────────┐
                        │                       │
                        ▼                       ▼
                ┌──────────────┐        ┌──────────────┐
                │   SQLite     │        │  PostgreSQL  │
                │   (Dev)      │        │  (Production)│
                └──────────────┘        └──────────────┘
```

---

## Route Hierarchy

```
/api
├── /content                    [Content Generation]
│   ├── POST   /generate        → Generate AI content
│   ├── GET    /list            → List all content
│   ├── GET    /{id}            → Get specific content
│   ├── PUT    /{id}/edit       → Edit content
│   ├── POST   /summarize       → Summarize content
│   └── DELETE /{id}            → Delete content
│
├── /translation                [Translation Services]
│   ├── POST   /translate       → Translate content
│   ├── POST   /translate/direct → Direct text translation
│   ├── POST   /batch           → Batch translate
│   ├── GET    /list/{id}       → List translations
│   ├── GET    /{id}            → Get translation
│   ├── GET    /supported-languages → Get languages
│   └── DELETE /{id}            → Delete translation
│
├── /social                     [Social Media Management]
│   ├── POST   /schedule        → Schedule single post
│   ├── POST   /schedule/bulk   → Bulk schedule
│   ├── GET    /list            → List posts
│   ├── GET    /{id}            → Get post
│   ├── PUT    /{id}            → Update post
│   ├── POST   /{id}/publish    → Publish immediately
│   ├── POST   /{id}/cancel     → Cancel scheduled post
│   ├── GET    /calendar/{user_id} → Calendar view
│   └── DELETE /{id}            → Delete post
│
├── /analytics                  [Analytics & Metrics]
│   ├── GET    /overview/{user_id} → Analytics overview
│   ├── GET    /platform-performance/{user_id} → Platform stats
│   ├── GET    /content-type-performance/{user_id} → Content stats
│   ├── GET    /engagement-trends/{user_id} → Trends
│   ├── GET    /top-content/{user_id} → Top content
│   ├── GET    /language-distribution/{user_id} → Language stats
│   └── POST   /sync-metrics/{post_id} → Sync metrics
│
├── /voice                      [Voice Input Processing]
│   ├── POST   /upload          → Upload audio file
│   ├── POST   /transcribe      → Transcribe audio
│   ├── GET    /list            → List voice inputs
│   ├── GET    /{id}            → Get voice input
│   ├── POST   /{id}/to-content → Convert to content
│   └── DELETE /{id}            → Delete voice input
│
└── /users                      [User Management]
    ├── POST   /register        → Register new user
    ├── GET    /{id}            → Get user profile
    ├── GET    /username/{username} → Get by username
    ├── PUT    /{id}            → Update user
    ├── GET    /{id}/stats      → Get user stats
    ├── POST   /{id}/upgrade-subscription → Upgrade tier
    ├── POST   /{id}/verify-email → Verify email
    ├── POST   /{id}/login      → Record login
    └── DELETE /{id}            → Delete user
```

---

## Data Flow Diagram

```
┌──────────────┐
│   Client     │
│  (Frontend)  │
└──────┬───────┘
       │ HTTP Request
       ▼
┌──────────────────────────────────────┐
│         FastAPI Router               │
│  - Route matching                    │
│  - Request validation (Pydantic)     │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│      Route Handler Function          │
│  - Business logic                    │
│  - Error handling                    │
└──────┬───────────────────────────────┘
       │
       ├─────────────────┬──────────────┐
       ▼                 ▼              ▼
┌─────────────┐   ┌─────────────┐  ┌─────────────┐
│  Database   │   │  AI Service │  │  External   │
│  Operations │   │  (Gemini/   │  │  APIs       │
│  (SQLAlchemy)│   │  Bedrock)   │  │  (Social)   │
└─────────────┘   └─────────────┘  └─────────────┘
       │                 │              │
       └─────────────────┴──────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  Response   │
                  │  Serializer │
                  └─────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Client    │
                  │  (Frontend) │
                  └─────────────┘
```

---

## Database Relationships

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     ├─────────────┐
     │             │
     ▼             ▼
┌─────────┐   ┌──────────┐
│ Content │   │   Post   │
└────┬────┘   └────┬─────┘
     │             │
     ├─────────┐   ├──────────────┐
     │         │   │              │
     ▼         ▼   ▼              ▼
┌────────────┐ ┌──────────┐ ┌──────────┐
│Translation │ │Analytics │ │ContentPerf│
└────────────┘ └──────────┘ └──────────┘

┌──────────┐
│   User   │
└────┬─────┘
     │
     ├──────────────┬──────────────┐
     │              │              │
     ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│VoiceInput│  │SocialAcc │  │Analytics │
└──────────┘  └──────────┘  └──────────┘
```

---

## Request/Response Flow by Feature

### Content Generation Flow
```
1. Client → POST /api/content/generate
2. Validate request (Pydantic)
3. Check user exists (Database)
4. Call AI service (Gemini/Bedrock)
5. Extract keywords/hashtags
6. Create Content record (Database)
7. Update user stats (Database)
8. Return ContentResponse
```

### Translation Flow
```
1. Client → POST /api/translation/translate
2. Validate request
3. Fetch content (Database)
4. Check if translation exists
5. Call IndicTrans service
6. Create Translation record (Database)
7. Update user translation count
8. Return TranslationResponse
```

### Social Media Scheduling Flow
```
1. Client → POST /api/social/schedule
2. Validate request
3. Verify user and content exist
4. Validate scheduled time
5. Create Post record (Database)
6. Schedule with EventBridge (Future)
7. Update user post count
8. Return PostResponse
```

### Analytics Flow
```
1. Client → GET /api/analytics/overview/{user_id}
2. Validate user exists
3. Query aggregated metrics (Database)
4. Calculate engagement rates
5. Identify top performers
6. Return AnalyticsOverviewResponse
```

---

## Service Integration Points

```
┌─────────────────────────────────────────────────────────┐
│                    Backend Routes                        │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  AI Services │  │Cloud Services│  │Social Media  │
│              │  │              │  │     APIs     │
│ • Gemini     │  │ • S3 Storage │  │ • Facebook   │
│ • Bedrock    │  │ • Transcribe │  │ • Instagram  │
│ • IndicTrans │  │ • EventBridge│  │ • Twitter    │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## Error Handling Flow

```
Request → Route Handler
              │
              ├─ Try Block
              │   ├─ Validation (Pydantic)
              │   ├─ Database Operations
              │   ├─ External API Calls
              │   └─ Response Generation
              │
              └─ Except Block
                  ├─ HTTPException → Return error response
                  ├─ Database Rollback
                  └─ Log error
```

---

## Authentication Flow (Future)

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ 1. Login Request
     ▼
┌──────────────┐
│ /users/login │
└────┬─────────┘
     │ 2. Verify credentials
     ▼
┌──────────────┐
│  Database    │
└────┬─────────┘
     │ 3. Generate JWT
     ▼
┌──────────────┐
│  JWT Token   │
└────┬─────────┘
     │ 4. Return token
     ▼
┌──────────────┐
│   Client     │
│ (Store token)│
└────┬─────────┘
     │ 5. Subsequent requests
     │    (Include token in header)
     ▼
┌──────────────┐
│  Middleware  │
│ (Verify JWT) │
└────┬─────────┘
     │ 6. Allow/Deny
     ▼
┌──────────────┐
│Route Handler │
└──────────────┘
```

---

## Performance Optimization Points

```
┌─────────────────────────────────────────┐
│           Request Pipeline              │
└─────────────────────────────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Cache  │ │Database│ │External│
│ Layer  │ │ Query  │ │  API   │
│(Redis) │ │Optimize│ │ Cache  │
└────────┘ └────────┘ └────────┘
    │           │           │
    └───────────┼───────────┘
                │
                ▼
         ┌─────────────┐
         │  Response   │
         └─────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────┐
│              Load Balancer (AWS ALB)            │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  FastAPI     │ │  FastAPI     │ │  FastAPI     │
│  Instance 1  │ │  Instance 2  │ │  Instance 3  │
└──────────────┘ └──────────────┘ └──────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  PostgreSQL  │ │    Redis     │ │     S3       │
│   (RDS)      │ │   (Cache)    │ │  (Storage)   │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## Summary Statistics

- **Total Routes:** 6 route files
- **Total Endpoints:** 53 API endpoints
- **Database Models:** 10 models
- **Supported Languages:** 11 Indian languages
- **Social Platforms:** 7 platforms
- **Content Types:** 7 types
- **User Roles:** 5 roles
- **Subscription Tiers:** 4 tiers

---

## Quick Navigation

- **Implementation Details:** `IMPLEMENTATION_SUMMARY.md`
- **Setup Instructions:** `SETUP_GUIDE.md`
- **API Reference:** `API_DOCUMENTATION.md`
- **Quick Start:** `QUICK_START.md`
- **Route Details:** `app/routes/README.md`
