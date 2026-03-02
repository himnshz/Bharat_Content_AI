# Static Code Analysis Report
**Generated:** March 1, 2026  
**Scope:** Full codebase scan for unused code, dependencies, state leaks, and orphaned files

---

## Executive Summary

This report identifies dead code, unused dependencies, state management leaks, and orphaned files across the entire codebase. All findings require manual review and cleanup.

---

## 1. DEAD CODE - Unused Components & Files

### Frontend (frontend-new/)

#### ❌ Completely Unused Components
- [ ] `frontend-new/src/components/SceneCanvas.tsx` - Not imported anywhere
- [ ] `frontend-new/src/components/Sidebar.tsx` - Not imported anywhere (layout/Sidebar.tsx is used instead)
- [ ] `frontend-new/src/components/dashboard/ProfileContent_Old.tsx` - Old version, not imported
- [ ] `frontend-new/src/components/scenes/ProfileScene.tsx` - Not used (SceneCanvas not used)
- [ ] `frontend-new/src/components/scenes/AnalyticsScene.tsx` - Not used (SceneCanvas not used)
- [ ] `frontend-new/src/components/scenes/GenerateScene.tsx` - Not used (SceneCanvas not used)
- [ ] `frontend-new/src/components/scenes/HomeScene.tsx` - Not used (SceneCanvas not used)
- [ ] `frontend-new/src/components/scenes/ScheduleScene.tsx` - Not used (SceneCanvas not used)
- [ ] `frontend-new/src/components/scenes/TranslateScene.tsx` - Not used (SceneCanvas not used)
- [ ] `frontend-new/src/components/scenes/VoiceScene.tsx` - Not used (SceneCanvas not used)

#### ❌ Unused Services & Utilities
- [ ] `frontend-new/src/services/api.service.ts` - Not imported anywhere
- [ ] `frontend-new/src/services/auth.service.ts` - Not imported anywhere
- [ ] `frontend-new/src/config/api.config.ts` - Not imported anywhere
- [ ] `frontend-new/src/utils/helpers.ts` - Not imported anywhere
- [ ] `frontend-new/src/store/useStore.ts` - Not imported anywhere (Zustand store defined but never used)
- [ ] `frontend-new/src/contexts/AuthContext.tsx` - Defined but never used in app

#### ❌ Unused Middleware
- [ ] `frontend-new/src/middleware.ts` - Defined but Next.js middleware requires specific export config to work

### Backend (backend/)

#### ❌ Unused AI Service Files
- [ ] `backend/app/services/content_generation/openai_service.py` - Service class defined but OpenAI not installed
- [ ] `backend/app/services/content_generation/anthropic_service.py` - Service class defined but Anthropic not installed
- [ ] `backend/app/services/content_generation/cohere_service.py` - Service class defined but Cohere not installed

**Note:** These services are referenced in `ai_service_manager_v2.py` but will fail at runtime since packages aren't installed.

---

## 2. UNUSED DEPENDENCIES

### Frontend (frontend-new/package.json)

#### ❌ Never Imported
- [ ] `@auth/prisma-adapter` - Not used anywhere in codebase
- [ ] `@prisma/client` - Not used anywhere in codebase
- [ ] `prisma` - Not used anywhere in codebase
- [ ] `next-auth` - Not used anywhere in codebase

**Impact:** ~4 packages can be removed  
**Estimated Size Savings:** ~50-100 MB in node_modules

#### ✅ Actually Used
- `@dnd-kit/*` - Used in CampaignsContent.tsx, KanbanColumn.tsx, CreatorCard.tsx
- `@fullcalendar/*` - Used in CalendarContent.tsx
- `recharts` - Used in AnalyticsContent.tsx
- `@react-three/fiber`, `@react-three/drei`, `three` - Used in Hero3D.tsx
- `zustand` - Installed but store not used (see State Management section)
- `framer-motion` - Used for animations
- `lucide-react` - Used for icons throughout
- `date-fns` - Used in helpers.ts (but helpers.ts not used)

### Backend (backend/requirements.txt)

#### ❌ Installed But Never Imported
- [ ] `asyncpg==0.29.0` - PostgreSQL async driver, only mentioned in comments
- [ ] `psycopg2-binary==2.9.9` - PostgreSQL sync driver, never imported
- [ ] `pymysql==1.1.0` - MySQL driver, never imported
- [ ] `alembic==1.12.1` - Database migrations, config exists but never used in code

**Note:** Backend currently uses SQLite, not PostgreSQL/MySQL

#### ❌ Installed But Packages Not Available
- [ ] `flower==2.0.1` - Celery monitoring UI, installed but not used in code
  - **Action:** Can be removed or kept for manual Celery monitoring

#### ❌ Commented Out But Listed
The following are commented in requirements.txt but still worth noting:
- `openai` - Service file exists but package not installed
- `anthropic` - Service file exists but package not installed
- `cohere` - Service file exists but package not installed
- `huggingface-hub` - Referenced in ai_service_manager but not installed
- `groq` - Referenced in ai_service_manager but not installed

#### ✅ Actually Used
- `fastapi`, `uvicorn`, `pydantic` - Core framework
- `sqlalchemy` - Database ORM (using SQLite)
- `boto3`, `botocore` - AWS Bedrock integration
- `google-generativeai` - Gemini AI service
- `celery`, `redis` - Task queue (configured but Redis not running)
- `slowapi`, `pybreaker`, `tenacity` - Rate limiting & circuit breaker
- `pandas`, `aiofiles` - CSV bulk operations
- `python-jose`, `passlib` - Authentication
- `httpx`, `requests` - HTTP clients

---

## 3. STATE MANAGEMENT LEAKS

### Frontend State Issues

#### ❌ Zustand Store Defined But Never Used
- [ ] `frontend-new/src/store/useStore.ts` - Lines 1-80
  - Defines `UserState`, `ThemeState`, `NotificationState`
  - Exports `useUserStore`, `useThemeStore`, `useNotificationStore`
  - **Never imported or used anywhere in the application**
  - **Action:** Either integrate or remove entirely

#### ❌ AuthContext Defined But Never Used
- [ ] `frontend-new/src/contexts/AuthContext.tsx` - Lines 1-94
  - Defines `AuthContext`, `AuthProvider`, `useAuth` hook
  - **Never imported or used in app layout or pages**
  - **Action:** Either wrap app with AuthProvider or remove

#### ⚠️ Potential State Leak
- [ ] `frontend-new/src/app/dashboard/page.tsx` - Line 21
  - Uses `useState` for `activeTab` but no cleanup
  - Multiple content components loaded simultaneously (all rendered conditionally)
  - **Recommendation:** Consider lazy loading or proper unmounting

### Backend State Issues

#### ✅ No Major State Leaks Detected
- Redis connections properly managed with lifecycle hooks
- Database sessions use context managers
- Circuit breakers properly initialized

---

## 4. ORPHANED FILES & FOLDERS

### ❌ Entire Orphaned Directories

#### Old Frontend (frontend/)
- [ ] **ENTIRE `frontend/` DIRECTORY** - Old Next.js implementation
  - `frontend/src/` - Complete old source code
  - `frontend/package.json` - Different dependencies than frontend-new
  - `frontend/public/` - Old assets
  - **Status:** Superseded by `frontend-new/`
  - **Action:** Archive or delete entire directory
  - **Estimated Size:** ~200+ MB with node_modules

#### Duplicate Project (bharat-ai-v2/)
- [ ] **ENTIRE `bharat-ai-v2/` DIRECTORY** - Duplicate project structure
  - `bharat-ai-v2/backend/` - Duplicate backend code
  - `bharat-ai-v2/frontend/` - Duplicate frontend code
  - Contains 12 documentation files (INDEX.md, QUICK_START.md, etc.)
  - **Status:** Appears to be a copy/backup of main project
  - **Action:** Archive or delete if not needed
  - **Estimated Size:** ~300+ MB

### ❌ Orphaned Documentation Files

#### Root Level Documentation Bloat
- [ ] `AI_MODELS_IMPLEMENTATION_COMPLETE.md` - Feature completion doc
- [ ] `ANALYTICS_IMPLEMENTATION_COMPLETE.md` - Feature completion doc
- [ ] `ANIMISTA_INTEGRATION_GUIDE.md` - Animation guide
- [ ] `AUTHENTICATION_IMPLEMENTATION_COMPLETE.md` - Feature completion doc
- [ ] `BACKEND_FRONTEND_FEATURE_MAPPING.md` - Mapping doc
- [ ] `BUTTON_IMPLEMENTATION_COMPLETE.md` - Feature completion doc
- [ ] `CAMPAIGN_API_SUMMARY.md` - API summary
- [ ] `CINEMATIC_3D_GUIDE.md` - 3D guide
- [ ] `COMPLETE_PROJECT_SUMMARY.md` - Summary doc
- [ ] `CONTENT_CALENDAR_IMPLEMENTATION_COMPLETE.md` - Feature completion doc
- [ ] `DASHBOARD_INTEGRATION_COMPLETE.md` - Feature completion doc
- [ ] `DEPLOYMENT_STATUS.md` - Deployment doc
- [ ] `FINAL_PROJECT_SUMMARY.md` - Summary doc
- [ ] `FINAL_SESSION_SUMMARY.md` - Summary doc
- [ ] `FINAL_STATUS.md` - Status doc
- [ ] `FRONTEND_IMPLEMENTATION_GUIDE.md` - Implementation guide
- [ ] `FRONTEND_REQUIREMENTS.md` - Requirements doc
- [ ] `KANBAN_BOARD_DOCUMENTATION.md` - Kanban doc
- [ ] `KANBAN_VISUAL_GUIDE.md` - Kanban guide
- [ ] `MASTER_FEATURE_LIST.md` - Feature list
- [ ] `NAVIGATION_SYSTEM_GUIDE.md` - Navigation guide
- [ ] `POSTGRESQL_MIGRATION_SUMMARY.md` - Migration summary
- [ ] `PROFILE_ENHANCEMENT_COMPLETE.md` - Feature completion doc
- [ ] `PROGRESS_UPDATE.md` - Progress doc
- [ ] `PROJECT_COPY_CHECKLIST.md` - Checklist
- [ ] `PROJECT_RESTART_GUIDE.md` - Restart guide
- [ ] `READ_THIS_FIRST.md` - Intro doc
- [ ] `SESSION_COMPLETE_SUMMARY.md` - Summary doc
- [ ] `SESSION_PROGRESS_SUMMARY.md` - Summary doc
- [ ] `SITE_READY.md` - Status doc
- [ ] `SUCCESS_REPORT.md` - Report doc
- [ ] `SYSTEM_ARCHITECTURE_SUMMARY.md` - Architecture doc
- [ ] `SYSTEM_RESTART_COMPLETE.md` - Restart doc
- [ ] `TEAM_COLLABORATION_IMPLEMENTATION_COMPLETE.md` - Feature completion doc

**Total:** 35+ markdown files in root directory  
**Action:** Consolidate into a single `docs/` folder or keep only essential README.md

### ❌ Orphaned Test Files
- [ ] `test_api.py` - Root level test file
- [ ] `test_campaign_api.py` - Root level test file
- [ ] `quick_test.py` - Root level test file
- [ ] `check_api_key.py` - Root level utility script

**Action:** Move to `backend/tests/` directory or delete if obsolete

### ❌ Orphaned Scripts
- [ ] `start_all_services.ps1` - PowerShell startup script (root level)
- [ ] `check_system_status.ps1` - PowerShell status script (root level)

**Action:** Move to `scripts/` directory for better organization

### ❌ Backend Orphaned Files
- [ ] `backend/bharat_content_ai.db` - SQLite database file (should be in .gitignore)
- [ ] `backend/main.py` - Duplicate of `backend/app/main.py`? (needs verification)
- [ ] `backend/celery_worker.py` - Celery worker entry point (used but could be in scripts/)

---

## 5. API ENDPOINTS ANALYSIS

### ✅ All Routes Registered in main.py
All route files in `backend/app/routes/` are properly registered:
- `content.py` → `/api/content`
- `translation.py` → `/api/translation`
- `social.py` → `/api/social`
- `analytics.py` → `/api/analytics`
- `voice.py` → `/api/voice`
- `users.py` → `/api/users`
- `campaigns.py` → `/api/campaigns`
- `models.py` → `/api/models`
- `teams.py` → `/api/teams`
- `templates.py` → `/api/templates`
- `bulk.py` → `/api/bulk`
- `monitoring.py` → `/api/monitoring`

**No orphaned route files detected.**

---

## 6. IMPORT ANALYSIS SUMMARY

### Frontend Import Issues
- **axios** - Installed in old frontend, not in frontend-new (uses fetch instead)
- **@tanstack/react-query** - Only in old frontend
- **react-hook-form** - Only in old frontend
- **zod** - Only in old frontend

### Backend Import Issues
- **No critical import errors** - All imported packages are installed
- **Optional AI packages** - Services exist but packages commented out (expected behavior)

---

## 7. CLEANUP RECOMMENDATIONS

### Priority 1: High Impact (Remove Immediately)
1. [ ] Delete `frontend/` directory (old frontend) - ~200 MB
2. [ ] Delete or archive `bharat-ai-v2/` directory - ~300 MB
3. [ ] Remove unused npm packages from frontend-new:
   ```bash
   npm uninstall @auth/prisma-adapter @prisma/client prisma next-auth
   ```
4. [ ] Remove unused Python packages from backend:
   ```bash
   pip uninstall asyncpg psycopg2-binary pymysql alembic
   ```

### Priority 2: Medium Impact (Clean Up Code)
5. [ ] Delete unused frontend components:
   - `SceneCanvas.tsx`, `Sidebar.tsx` (root level)
   - All files in `components/scenes/`
   - `ProfileContent_Old.tsx`
6. [ ] Delete unused frontend services:
   - `services/api.service.ts`
   - `services/auth.service.ts`
   - `config/api.config.ts`
   - `utils/helpers.ts`
   - `store/useStore.ts`
   - `contexts/AuthContext.tsx`
7. [ ] Remove or fix `middleware.ts` (not properly configured)

### Priority 3: Low Impact (Organization)
8. [ ] Consolidate root-level markdown files into `docs/` folder
9. [ ] Move test files to `backend/tests/`
10. [ ] Move PowerShell scripts to `scripts/`
11. [ ] Add `bharat_content_ai.db` to `.gitignore`
12. [ ] Consider removing unused AI service files or install packages

---

## 8. ESTIMATED CLEANUP IMPACT

### Disk Space Savings
- Delete `frontend/` directory: ~200 MB
- Delete `bharat-ai-v2/` directory: ~300 MB
- Remove unused npm packages: ~50-100 MB
- Remove unused Python packages: ~20-30 MB
- **Total Estimated Savings:** ~570-630 MB

### Code Reduction
- Frontend: ~15 unused files (~2,000+ lines of code)
- Backend: ~3 unused service files (~500+ lines of code)
- Documentation: ~35 markdown files (consolidate to ~5-10)
- **Total Files to Remove/Consolidate:** ~50+ files

### Maintenance Benefits
- Reduced confusion about which frontend to use
- Clearer dependency tree
- Faster npm/pip install times
- Easier onboarding for new developers
- Reduced CI/CD build times

---

## 9. VERIFICATION CHECKLIST

Before deleting any files, verify:
- [ ] Run full test suite to ensure nothing breaks
- [ ] Check git history to see if files have recent commits
- [ ] Verify no environment-specific references (production configs)
- [ ] Create backup/archive of deleted directories
- [ ] Update README.md with correct project structure
- [ ] Update .gitignore to prevent future bloat

---

## 10. NEXT STEPS

1. **Review this report** with the team
2. **Create a backup** of the entire project
3. **Execute Priority 1 cleanup** (high impact, low risk)
4. **Test thoroughly** after each cleanup phase
5. **Update documentation** to reflect new structure
6. **Set up linting rules** to prevent future unused imports
7. **Configure dependency analysis** in CI/CD pipeline

---

**Report End**
