# ✅ System Restart - Complete Guide

## Quick Start (30 Seconds)

```powershell
# 1. Start all services automatically
.\start_all_services.ps1

# 2. Check status
.\check_system_status.ps1

# 3. Open browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/docs
```

---

## 📁 Files Created

### Restart Scripts
1. **`PROJECT_RESTART_GUIDE.md`** - Complete restart documentation
2. **`start_all_services.ps1`** - Automated startup script
3. **`check_system_status.ps1`** - Status verification script

---

## 🚀 Three Ways to Start

### Method 1: Automated (Recommended)
```powershell
.\start_all_services.ps1
```
**Starts:**
- FastAPI (port 8000)
- Celery Worker
- Flower (port 5555)
- Next.js Frontend (port 3000)

### Method 2: Backend Only
```powershell
cd backend
.\start_bulk_services.ps1
```
**Starts:**
- FastAPI
- Celery Worker
- Flower

### Method 3: Manual (Full Control)
```powershell
# Terminal 1: Redis
redis-server

# Terminal 2: FastAPI
cd backend
uvicorn app.main:app --reload

# Terminal 3: Celery
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo

# Terminal 4: Flower
cd backend
celery -A app.config.celery_config.celery_app flower

# Terminal 5: Frontend
cd frontend-new
npm run dev
```

---

## ✅ Verification Checklist

After starting, verify:

### 1. Services Running
```powershell
.\check_system_status.ps1
```

Expected output:
```
✅ Redis: Running
✅ PostgreSQL: Running
✅ Backend API (port 8000): Running
✅ Frontend (port 3000): Running
✅ Flower (port 5555): Running

Running Services: 5 / 5
✅ All services are running!
```

### 2. Health Checks
```bash
# Overall health
curl http://localhost:8000/api/monitoring/health

# Circuit breakers
curl http://localhost:8000/api/monitoring/circuit-breakers

# AI services
curl http://localhost:8000/api/monitoring/ai-services/health

# System status
curl http://localhost:8000/api/monitoring/system/status
```

### 3. Frontend Access
- Open: http://localhost:3000
- Should see landing page with 3D animations
- Can navigate to login/register
- Can access dashboard

### 4. API Documentation
- Open: http://localhost:8000/api/docs
- Should see Swagger UI with all endpoints
- Can test endpoints directly

---

## 🔍 Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | User interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/api/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/api/redoc | Alternative docs |
| **Flower** | http://localhost:5555 | Celery monitoring |
| **Health** | http://localhost:8000/api/monitoring/health | Health check |
| **Status** | http://localhost:8000/api/monitoring/system/status | System status |

---

## 🛠️ Common Issues & Solutions

### Issue 1: Redis Not Running
```
❌ Redis is not running!
```

**Solution:**
```powershell
# Windows (WSL)
wsl
redis-server

# Or install Redis for Windows
# Download from: https://github.com/microsoftarchive/redis/releases
```

### Issue 2: PostgreSQL Not Running
```
❌ PostgreSQL: Not running
```

**Solution:**
```powershell
# Windows
Start-Service postgresql-x64-14

# Or check service name
Get-Service postgresql*
Start-Service <service-name>
```

### Issue 3: Port Already in Use
```
Error: Port 8000 is already in use
```

**Solution:**
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --port 8001
```

### Issue 4: Module Not Found
```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
```powershell
cd backend
pip install -r requirements.txt
```

### Issue 5: Database Connection Failed
```
Error: Could not connect to database
```

**Solution:**
```powershell
# Check .env file
cat backend/.env | grep DATABASE_URL

# Should be:
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bharat_content_ai

# Create database if needed
psql -U postgres
CREATE DATABASE bharat_content_ai;
\q

# Run migrations
cd backend
alembic upgrade head
```

---

## 🔄 Restart Individual Services

### Restart Backend Only
```powershell
# Stop: Ctrl+C in FastAPI terminal
# Restart:
cd backend
uvicorn app.main:app --reload
```

### Restart Celery Only
```powershell
# Stop: Ctrl+C in Celery terminal
# Restart:
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo
```

### Restart Frontend Only
```powershell
# Stop: Ctrl+C in Next.js terminal
# Restart:
cd frontend-new
npm run dev
```

### Restart Redis
```powershell
# Stop: Ctrl+C in Redis terminal
# Restart:
redis-server
```

---

## 📊 Monitoring Commands

### Check All Services
```powershell
.\check_system_status.ps1
```

### Check Backend Health
```bash
curl http://localhost:8000/api/monitoring/health
```

### Check Circuit Breakers
```bash
curl http://localhost:8000/api/monitoring/circuit-breakers
```

### Check AI Services
```bash
curl http://localhost:8000/api/monitoring/ai-services/health
```

### Check Rate Limits
```bash
curl http://localhost:8000/api/monitoring/rate-limits/my-limits
```

### Check Celery Workers
```bash
celery -A app.config.celery_config.celery_app inspect active
```

### Check Redis
```bash
redis-cli ping
redis-cli INFO
```

### Check PostgreSQL
```bash
psql -U postgres -d bharat_content_ai -c "SELECT COUNT(*) FROM users;"
```

---

## 🧪 Test Commands

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

### Test Rate Limiting
```bash
# Make 10 requests (should hit limit at 5 for unauthenticated)
for i in {1..10}; do
  curl -X POST "http://localhost:8000/api/content/generate" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Test"}'
done
```

### Test Bulk Operations
```bash
curl -X POST "http://localhost:8000/api/bulk/upload" \
  -F "file=@backend/sample_csvs/content_generation_sample.csv" \
  -F "operation_type=content_generation"
```

### Test Circuit Breaker
```bash
# Get status
curl http://localhost:8000/api/monitoring/circuit-breakers

# Reset a circuit
curl -X POST "http://localhost:8000/api/monitoring/circuit-breakers/gemini/reset"
```

---

## 📚 Documentation Reference

### Quick Start Guides
- `PROJECT_RESTART_GUIDE.md` - This file
- `backend/QUICK_START.md` - Backend quick start
- `backend/BULK_OPERATIONS_QUICK_START.md` - Bulk operations
- `backend/POSTGRESQL_QUICK_REFERENCE.md` - Database

### Complete Guides
- `backend/API_DOCUMENTATION.md` - All API endpoints
- `backend/BULK_OPERATIONS_GUIDE.md` - Bulk operations
- `backend/RATE_LIMITING_CIRCUIT_BREAKER_GUIDE.md` - Rate limiting
- `backend/POSTGRESQL_MIGRATION_GUIDE.md` - Database migration

### Implementation Details
- `backend/BULK_OPERATIONS_COMPLETE.md` - Bulk ops implementation
- `backend/RATE_LIMITING_CIRCUIT_BREAKER_COMPLETE.md` - Rate limiting implementation
- `backend/POSTGRESQL_MIGRATION_COMPLETE.md` - Database implementation

---

## 🎯 Success Indicators

System is running correctly when:

1. ✅ All 5 services show "Running" in status check
2. ✅ Health check returns `{"status": "healthy"}`
3. ✅ Frontend loads at http://localhost:3000
4. ✅ API docs accessible at http://localhost:8000/api/docs
5. ✅ Can generate content via API
6. ✅ Can upload bulk CSV
7. ✅ Rate limiting is enforced
8. ✅ Circuit breakers show status
9. ✅ Flower shows active workers
10. ✅ No error messages in terminals

---

## 🚨 Emergency Procedures

### Complete System Reset
```powershell
# 1. Stop all services (Ctrl+C in all terminals)

# 2. Clear Redis
redis-cli FLUSHALL

# 3. Reset database (CAUTION: loses data)
psql -U postgres
DROP DATABASE bharat_content_ai;
CREATE DATABASE bharat_content_ai;
\q

# 4. Run migrations
cd backend
alembic upgrade head

# 5. Restart all services
.\start_all_services.ps1
```

### Clear Celery Queue
```bash
celery -A app.config.celery_config.celery_app purge
```

### Reset Circuit Breakers
```bash
curl -X POST "http://localhost:8000/api/monitoring/circuit-breakers/reset-all"
```

### Reset AI Statistics
```bash
curl -X POST "http://localhost:8000/api/monitoring/ai-services/statistics/reset"
```

---

## 📞 Support

### Check Logs
```powershell
# Backend logs (in FastAPI terminal)
# Celery logs (in Celery terminal)
# Frontend logs (in Next.js terminal)

# Or check log files if configured
tail -f logs/app.log
tail -f logs/celery.log
```

### Get System Info
```bash
# System status
curl http://localhost:8000/api/monitoring/system/status

# Circuit breakers
curl http://localhost:8000/api/monitoring/circuit-breakers

# AI services
curl http://localhost:8000/api/monitoring/ai-services/health

# Statistics
curl http://localhost:8000/api/monitoring/ai-services/statistics
```

---

## ✅ Final Checklist

Before considering system "ready":

- [ ] Redis running and responding to PING
- [ ] PostgreSQL running and accessible
- [ ] Backend API responding at port 8000
- [ ] Celery worker active and processing tasks
- [ ] Flower dashboard accessible at port 5555
- [ ] Frontend loading at port 3000
- [ ] Health check returns "healthy"
- [ ] At least one AI service available
- [ ] Circuit breakers showing status
- [ ] Rate limiting working
- [ ] Can generate content
- [ ] Can upload bulk CSV
- [ ] All monitoring endpoints accessible
- [ ] No errors in any terminal
- [ ] Documentation accessible

---

## 🎉 You're All Set!

Your Bharat Content AI system is now running with:

- ✅ **Backend**: FastAPI with 90+ endpoints
- ✅ **Database**: PostgreSQL with 17 models
- ✅ **Cache**: Redis for rate limiting and queues
- ✅ **Workers**: Celery for bulk operations
- ✅ **Frontend**: Next.js with 3D animations
- ✅ **Monitoring**: Real-time health checks
- ✅ **Protection**: Rate limiting + circuit breakers
- ✅ **Resilience**: Intelligent AI fallback

**Happy coding! 🚀**

---

**Last Updated**: March 1, 2026  
**Status**: ✅ PRODUCTION READY  
**Version**: 2.0.0
