# Project Structure

Clean, organized structure after comprehensive cleanup.

---

## 📁 Directory Tree

```
AI-Content_Creator-1/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── config/            # Configuration files
│   │   │   ├── aws_config.py
│   │   │   ├── celery_config.py
│   │   │   ├── circuit_breaker_config.py
│   │   │   ├── database.py
│   │   │   ├── rate_limit_config.py
│   │   │   ├── redis_config.py
│   │   │   └── settings.py
│   │   ├── models/            # SQLAlchemy Models
│   │   │   ├── ai_model_config.py
│   │   │   ├── analytics.py
│   │   │   ├── campaign.py
│   │   │   ├── content.py
│   │   │   ├── post.py
│   │   │   ├── social_account.py
│   │   │   ├── team.py
│   │   │   ├── template.py
│   │   │   ├── translation.py
│   │   │   ├── user.py
│   │   │   └── voice_input.py
│   │   ├── routes/            # API Endpoints
│   │   │   ├── analytics.py
│   │   │   ├── bulk.py
│   │   │   ├── campaigns.py
│   │   │   ├── content.py
│   │   │   ├── models.py
│   │   │   ├── monitoring.py
│   │   │   ├── social.py
│   │   │   ├── teams.py
│   │   │   ├── templates.py
│   │   │   ├── translation.py
│   │   │   ├── users.py
│   │   │   └── voice.py
│   │   ├── schemas/           # Pydantic Schemas
│   │   │   └── bulk_schemas.py
│   │   ├── services/          # Business Logic
│   │   │   ├── analytics/
│   │   │   │   └── tracker.py
│   │   │   ├── content_generation/
│   │   │   │   ├── ai_service_manager.py
│   │   │   │   ├── ai_service_manager_v2.py
│   │   │   │   ├── bedrock_service.py
│   │   │   │   ├── gemini_service.py
│   │   │   │   └── generator.py
│   │   │   ├── social_media/
│   │   │   │   └── scheduler.py
│   │   │   ├── translation/
│   │   │   │   └── translator.py
│   │   │   └── voice/
│   │   │       └── processor.py
│   │   ├── tasks/             # Celery Tasks
│   │   │   ├── bulk_operations.py
│   │   │   ├── content_tasks.py
│   │   │   └── translation_tasks.py
│   │   └── main.py            # FastAPI App Entry
│   ├── alembic/               # Database Migrations
│   │   └── env.py
│   ├── sample_csvs/           # Sample CSV Files
│   │   ├── content_generation_sample.csv
│   │   └── translation_sample.csv
│   ├── temp_uploads/          # Temporary Upload Storage
│   ├── tests/                 # Backend Tests
│   │   ├── check_api_key.py
│   │   ├── quick_test.py
│   │   ├── test_api.py
│   │   └── test_campaign_api.py
│   ├── venv/                  # Python Virtual Environment
│   ├── .env                   # Environment Variables
│   ├── .env.example           # Environment Template
│   ├── alembic.ini            # Alembic Configuration
│   ├── celery_worker.py       # Celery Worker Entry
│   ├── migrate_sqlite_to_postgres.py  # Migration Script
│   ├── requirements.txt       # Python Dependencies
│   └── start_bulk_services.ps1  # Bulk Services Starter
│
├── frontend-new/              # Next.js 15 Frontend
│   ├── public/                # Static Assets
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/       # React Components
│   │   │   ├── dashboard/
│   │   │   │   ├── kanban/
│   │   │   │   │   ├── CreatorCard.tsx
│   │   │   │   │   └── KanbanColumn.tsx
│   │   │   │   ├── team/
│   │   │   │   │   ├── ActivityFeed.tsx
│   │   │   │   │   ├── ApprovalCard.tsx
│   │   │   │   │   ├── InviteModal.tsx
│   │   │   │   │   └── MemberList.tsx
│   │   │   │   ├── AnalyticsContent.tsx
│   │   │   │   ├── CalendarContent.tsx
│   │   │   │   ├── CampaignsContent.tsx
│   │   │   │   ├── GenerateContent.tsx
│   │   │   │   ├── HomeContent.tsx
│   │   │   │   ├── ModelsContent.tsx
│   │   │   │   ├── ProfileContent.tsx
│   │   │   │   ├── ScheduleContent.tsx
│   │   │   │   ├── TeamContent.tsx
│   │   │   │   ├── TemplatesContent.tsx
│   │   │   │   ├── TranslateContent.tsx
│   │   │   │   └── VoiceContent.tsx
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── index.ts
│   │   │   └── Hero3D.tsx
│   │   ├── store/            # Zustand State Management
│   │   │   └── useStore.ts
│   │   └── utils/            # Utility Functions
│   │       └── helpers.ts
│   ├── .eslintrc.json        # ESLint Config
│   ├── next.config.ts        # Next.js Config
│   ├── package.json          # Node Dependencies
│   ├── postcss.config.mjs    # PostCSS Config
│   ├── tailwind.config.ts    # Tailwind Config
│   └── tsconfig.json         # TypeScript Config
│
├── docs/                      # Documentation (64 files)
│   ├── INDEX.md              # Documentation Index
│   ├── AI_SERVICES_GUIDE.md
│   ├── API_DOCUMENTATION.md
│   ├── BULK_OPERATIONS_GUIDE.md
│   ├── CAMPAIGN_API_DOCUMENTATION.md
│   ├── POSTGRESQL_MIGRATION_GUIDE.md
│   ├── RATE_LIMITING_CIRCUIT_BREAKER_GUIDE.md
│   ├── SETUP_GUIDE.md
│   ├── STATIC_ANALYSIS_REPORT.md
│   └── ... (60 more documentation files)
│
├── scripts/                   # Utility Scripts
│   ├── check_system_status.ps1
│   └── start_all_services.ps1
│
├── .gitignore                # Git Ignore Rules
├── .vscode/                  # VS Code Settings
├── CLEANUP_SUMMARY.md        # Cleanup Report
├── QUICK_START.md            # Quick Start Guide
├── PROJECT_STRUCTURE.md      # This File
└── README.md                 # Project Overview
```

---

## 📊 Statistics

### File Counts
- **Backend Python Files:** 45
- **Frontend TypeScript Files:** 35
- **Documentation Files:** 64
- **Test Files:** 4
- **Configuration Files:** 12
- **Total Files:** ~160

### Lines of Code (Estimated)
- **Backend:** ~8,000 lines
- **Frontend:** ~6,000 lines
- **Total:** ~14,000 lines

### Directory Sizes
- **Backend:** ~50 MB (excluding venv)
- **Frontend:** ~150 MB (excluding node_modules)
- **Documentation:** ~2 MB
- **Total Project:** ~200 MB (excluding dependencies)

---

## 🎯 Key Directories Explained

### Backend Structure

#### `/app/config`
Configuration files for all services:
- Database connections
- AWS/AI service credentials
- Redis & Celery setup
- Rate limiting rules
- Circuit breaker patterns

#### `/app/models`
SQLAlchemy ORM models (11 models):
- User management
- Content & campaigns
- Social media accounts
- Analytics tracking
- Team collaboration
- AI model configurations

#### `/app/routes`
FastAPI route handlers (12 modules):
- RESTful API endpoints
- Request validation
- Response formatting
- Error handling

#### `/app/services`
Business logic layer:
- AI content generation (Gemini, Bedrock)
- Translation services
- Social media scheduling
- Analytics tracking
- Voice processing

#### `/app/tasks`
Celery background tasks:
- Bulk content generation
- Batch translations
- CSV processing
- Scheduled posts

### Frontend Structure

#### `/src/app`
Next.js 15 app router:
- Server-side rendering
- Client components
- Route handlers
- Layouts

#### `/src/components/dashboard`
Dashboard UI components:
- 12 main content sections
- Kanban board system
- Team collaboration UI
- Analytics visualizations

#### `/src/store`
Zustand state management:
- User authentication state
- Content management
- UI state (theme, notifications)
- Translation cache
- Social media data
- Analytics data

#### `/src/utils`
Utility functions:
- Date formatting
- Text processing
- Validation helpers
- File operations
- Platform-specific helpers

---

## 🔧 Configuration Files

### Backend
- `.env` - Environment variables (API keys, database URL)
- `requirements.txt` - Python dependencies
- `alembic.ini` - Database migration config
- `celery_worker.py` - Celery worker entry point

### Frontend
- `package.json` - Node dependencies
- `next.config.ts` - Next.js configuration
- `tailwind.config.ts` - Tailwind CSS config
- `tsconfig.json` - TypeScript configuration

### Root
- `.gitignore` - Git exclusion rules
- `README.md` - Project overview
- `QUICK_START.md` - Quick setup guide

---

## 📦 Dependencies

### Backend (Python)
- **Core:** FastAPI, Uvicorn, Pydantic, SQLAlchemy
- **AI:** Google Gemini, AWS Boto3 (Bedrock)
- **Tasks:** Celery, Redis
- **Security:** Python-JOSE, Passlib
- **Utilities:** Pandas, HTTPX, Tenacity

### Frontend (Node.js)
- **Core:** Next.js 15, React 19, TypeScript
- **UI:** Tailwind CSS, Framer Motion, Lucide Icons
- **State:** Zustand
- **3D:** Three.js, React Three Fiber
- **Charts:** Recharts
- **Calendar:** FullCalendar
- **DnD:** DND Kit

---

## 🚀 Entry Points

### Development
- **Backend:** `uvicorn app.main:app --reload`
- **Frontend:** `npm run dev`
- **Celery:** `celery -A app.config.celery_config.celery_app worker`

### Production
- **Backend:** `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker`
- **Frontend:** `npm run build && npm start`

### Scripts
- **Start All:** `.\scripts\start_all_services.ps1`
- **Check Status:** `.\scripts\check_system_status.ps1`

---

## 📝 Important Files

### Must Read
1. `README.md` - Project overview
2. `QUICK_START.md` - Setup in 5 minutes
3. `docs/INDEX.md` - Documentation index
4. `CLEANUP_SUMMARY.md` - Recent changes

### Configuration
1. `backend/.env` - Backend environment variables
2. `frontend-new/.env.local` - Frontend environment variables
3. `backend/requirements.txt` - Python dependencies
4. `frontend-new/package.json` - Node dependencies

### Documentation
1. `docs/API_DOCUMENTATION.md` - API reference
2. `docs/SETUP_GUIDE.md` - Detailed setup
3. `docs/AI_SERVICES_GUIDE.md` - AI configuration
4. `docs/BULK_OPERATIONS_GUIDE.md` - Bulk operations

---

## 🎨 Design Patterns

### Backend
- **Repository Pattern** - Data access layer
- **Service Layer** - Business logic separation
- **Circuit Breaker** - Fault tolerance
- **Rate Limiting** - API protection
- **Task Queue** - Async processing

### Frontend
- **Component Composition** - Reusable UI
- **State Management** - Zustand stores
- **Server Components** - Next.js 15
- **Client Components** - Interactive UI
- **Utility-First CSS** - Tailwind

---

## 🔒 Security

### Backend
- JWT authentication
- Password hashing (bcrypt)
- Rate limiting (5 tiers)
- CORS configuration
- Environment variable protection

### Frontend
- Client-side validation
- Secure API calls
- Token storage
- XSS protection
- CSRF protection

---

**Last Updated:** March 1, 2026  
**Version:** 2.0.0  
**Status:** Production Ready
