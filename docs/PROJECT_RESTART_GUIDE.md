# 🚀 Project Restart Guide

## Complete System Startup Instructions

This guide will help you restart the entire Bharat Content AI system with all its components.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Python 3.11+** installed
- [ ] **Node.js 18+** and npm installed
- [ ] **PostgreSQL** installed and running
- [ ] **Redis** installed and running
- [ ] **Git** installed
- [ ] All API keys configured in `.env` files

---

## 🔧 Step 1: Install Dependencies

### Backend Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

**Key Dependencies:**
- FastAPI, Uvicorn
- SQLAlchemy, Alembic, asyncpg
- Celery, Redis, Flower
- SlowAPI, PyBreaker, Tenacity
- Pandas, aiofiles
- Google Gemini, AWS Boto3

### Frontend Dependencies

```powershell
cd frontend-new
npm install
```

**Key Dependencies:**
- Next.js 15.1.0
- React 18.3.1
- Three.js, @react-three/fiber
- FullCalendar
- Framer Motion

---

## 🗄️ Step 2: Start Database Services

### Start PostgreSQL

**Windows:**
```powershell
# Check if running
Get-Service postgresql*

# Start if not running
Start-Service postgresql-x64-14
```

**macOS/Linux:**
```bash
# Check status
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql
```

**Verify Connection:**
```bash
psql -U postgres -d bharat_content_ai
# Should connect successfully
\q
```

### Start Redis

**Windows (WSL):**
```powershell
wsl
redis-server
```

**macOS:**
```bash
brew services start redis
```

**Linux:**
```bash
sudo systemctl start redis
```

**Verify Connection:**
```bash
redis-cli ping
# Should return: PONG
```

---

## 🚀 Step 3: Start Backend Services

### Option A: Automated Startup (Recommended)

```powershell
cd backend
.\start_bulk_services.ps1
```

This will automatically start:
- FastAPI server (port 8000)
- Celery worker
- Flower monitoring (port 5555)

### Option B: Manual Startup

Open **4 separate terminal windows**:

#### Terminal 1: FastAPI Server
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2: Celery Worker
```powershell
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo
```

#### Terminal 3: Flower Monitoring (Optional)
```powershell
cd backend
celery -A app.config.celery_config.celery_app flower --port=5555
```

#### Terminal 4: Celery Beat (Optional - for scheduled tasks)
```powershell
cd backend
celery -A app.config.celery_config.celery_app beat --loglevel=info
```

---

## 🎨 Step 4: Start Frontend

```powershell
cd frontend-new
npm run dev
```

The frontend will start on: http://localhost:3000

---

## ✅ Step 5: Verify All Services

### Check Backend Health

```bash
# Health check
curl http://localhost:8000/api/monitoring/health

# API documentation
# Open in browser: http://localhost:8000/api/docs
```

**Expected Response:**
```json
{
  "status": "healthy",
  "components": {
    "redis": {"status": "healthy"},
    "ai_services": {"status": "healthy"}
  }
}
```

### Check Circuit Breakers

```bash
curl http://localhost:8000/api/monitoring/circuit-breakers
```

### Check Rate Limits

```bash
curl http://localhost:8000/api/monitoring/rate-limits/tiers
```

### Check Celery Worker

```bash
# Check active workers
celery -A app.config.celery_config.celery_app inspect active

# Or visit Flower dashboard
# http://localhost:5555
```

### Check Frontend

Open browser: http://localhost:3000

You should see:
- Landing page with 3D animations
- Login/Register pages
- Dashboard (after login)

---

## 🔍 Step 6: Run Database Migrations (If Needed)

### Check Current Migration Status

```powershell
cd backend
alembic current
```

### Apply Pending Migrations

```powershell
alembic upgrade head
```

### Create New Migration (If Schema Changed)

```powershell
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

---

## 🧪 Step 7: Test the System

### Test Content Generation

```bash
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -H "X-User-Tier: FREE" \
  -d '{
    "prompt": "Write a social media post about AI",
    "language": "hindi",
    "content_type": "social_post",
    "tone": "casual"
  }'
```

### Test Bulk Operations

```bash
# Upload sample CSV
curl -X POST "http://localhost:8000/api/bulk/upload" \
  -F "file=@sample_csvs/content_generation_sample.csv" \
  -F "operation_type=content_generation"
```

### Test Rate Limiting

```bash
# Make 10 requests quickly (should hit rate limit)
for i in {1..10}; do
  curl -X POST "http://localhost:8000/api/content/generate" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Test"}'
done
```

---

## 📊 Service URLs Reference

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Next.js application |
| **Backend API** | http://localhost:8000 | FastAPI server |
| **API Docs** | http://localhost:8000/api/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/api/redoc | Alternative API docs |
| **Flower** | http://localhost:5555 | Celery monitoring |
| **PostgreSQL** | localhost:5432 | Database |
| **Redis** | localhost:6379 | Cache & queue |

---

## 🛠️ Troubleshooting

### Backend Won't Start

**Error: "Redis connection refused"**
```powershell
# Check if Redis is running
redis-cli ping

# Start Redis if not running
redis-server
```

**Error: "PostgreSQL connection failed"**
```powershell
# Check if PostgreSQL is running
psql -U postgres -l

# Check DATABASE_URL in .env
# Should be: postgresql+asyncpg://postgres:postgres@localhost:5432/bharat_content_ai
```

**Error: "No module named 'app'"**
```powershell
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Celery Worker Won't Start

**Error: "No module named 'celery'"**
```powershell
pip install celery redis flower
```

**Error: "Task not found"**
```powershell
# Restart worker
# Ctrl+C to stop, then restart
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo
```

### Frontend Won't Start

**Error: "Cannot find module"**
```powershell
cd frontend-new
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 3000 already in use"**
```powershell
# Kill process on port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill -9
```

### Database Issues

**Error: "Database does not exist"**
```bash
# Create database
psql -U postgres
CREATE DATABASE bharat_content_ai;
\q

# Run migrations
cd backend
alembic upgrade head
```

**Error: "Migration conflict"**
```powershell
# Reset migrations (CAUTION: loses data)
alembic downgrade base
alembic upgrade head
```

---

## 🔄 Quick Restart Commands

### Restart Everything

```powershell
# Stop all services (Ctrl+C in each terminal)

# Restart Redis
redis-server

# Restart PostgreSQL (if needed)
# Windows: Restart-Service postgresql-x64-14
# Linux: sudo systemctl restart postgresql

# Restart Backend
cd backend
uvicorn app.main:app --reload

# Restart Celery (new terminal)
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo

# Restart Frontend (new terminal)
cd frontend-new
npm run dev
```

### Restart Only Backend

```powershell
# Stop FastAPI (Ctrl+C)
# Restart
cd backend
uvicorn app.main:app --reload
```

### Restart Only Celery

```powershell
# Stop Celery (Ctrl+C)
# Restart
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo
```

### Restart Only Frontend

```powershell
# Stop Next.js (Ctrl+C)
# Restart
cd frontend-new
npm run dev
```

---

## 📝 Environment Variables Checklist

### Backend `.env`

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bharat_content_ai

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# AI Services (configure at least one)
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# AWS (optional)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1

# Security
SECRET_KEY=your-secret-key-for-jwt
INTERNAL_SERVICE_TOKEN=your-internal-token
```

### Frontend `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🎯 Post-Restart Checklist

After restarting, verify:

- [ ] Backend API responds at http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/api/docs
- [ ] Health check returns "healthy"
- [ ] Circuit breakers show status
- [ ] Celery worker is active
- [ ] Flower dashboard accessible
- [ ] Frontend loads at http://localhost:3000
- [ ] Can navigate to login/register
- [ ] Can access dashboard
- [ ] Redis is connected
- [ ] PostgreSQL is connected
- [ ] Rate limiting is working
- [ ] AI services are available

---

## 📚 Additional Resources

### Documentation
- **Backend API**: `backend/API_DOCUMENTATION.md`
- **Bulk Operations**: `backend/BULK_OPERATIONS_GUIDE.md`
- **Rate Limiting**: `backend/RATE_LIMITING_CIRCUIT_BREAKER_GUIDE.md`
- **PostgreSQL Migration**: `backend/POSTGRESQL_MIGRATION_GUIDE.md`
- **Frontend**: `FRONTEND_IMPLEMENTATION_GUIDE.md`

### Quick References
- **Backend Quick Start**: `backend/QUICK_START.md`
- **Bulk Operations Quick Start**: `backend/BULK_OPERATIONS_QUICK_START.md`
- **PostgreSQL Quick Reference**: `backend/POSTGRESQL_QUICK_REFERENCE.md`

### Monitoring
- **Health Check**: http://localhost:8000/api/monitoring/health
- **Circuit Breakers**: http://localhost:8000/api/monitoring/circuit-breakers
- **AI Services**: http://localhost:8000/api/monitoring/ai-services/health
- **System Status**: http://localhost:8000/api/monitoring/system/status

---

## 🚨 Emergency Procedures

### Complete System Reset

```powershell
# 1. Stop all services (Ctrl+C in all terminals)

# 2. Clear Redis cache
redis-cli FLUSHALL

# 3. Reset database (CAUTION: loses all data)
psql -U postgres
DROP DATABASE bharat_content_ai;
CREATE DATABASE bharat_content_ai;
\q

# 4. Run migrations
cd backend
alembic upgrade head

# 5. Restart all services
# Follow "Step 3: Start Backend Services" above
```

### Clear Celery Queue

```bash
# Clear all tasks
celery -A app.config.celery_config.celery_app purge

# Or clear Redis queues
redis-cli
DEL celery
DEL celery-task-meta-*
```

---

## ✅ Success Indicators

You'll know the system is running correctly when:

1. ✅ All 4 backend services are running without errors
2. ✅ Frontend loads and shows 3D animations
3. ✅ Health check returns "healthy"
4. ✅ Can generate content via API
5. ✅ Can upload bulk CSV
6. ✅ Rate limiting is enforced
7. ✅ Circuit breakers show status
8. ✅ Flower shows active workers
9. ✅ No error messages in any terminal
10. ✅ Can access all monitoring endpoints

---

## 🎉 You're Ready!

Once all services are running and verified, your Bharat Content AI system is fully operational with:

- ✅ FastAPI backend with 90+ endpoints
- ✅ PostgreSQL database with 17 models
- ✅ Redis caching and task queue
- ✅ Celery workers for bulk operations
- ✅ Rate limiting (5 tiers)
- ✅ Circuit breakers (15 services)
- ✅ Intelligent AI fallback (8 providers)
- ✅ Next.js frontend with 3D animations
- ✅ Real-time monitoring
- ✅ Production-ready configuration

**Happy coding! 🚀**
