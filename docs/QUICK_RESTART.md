# ⚡ Quick Restart Reference

## 🚀 Start Everything (One Command)

```powershell
.\start_all_services.ps1
```

## ✅ Check Status

```powershell
.\check_system_status.ps1
```

## 🌐 Service URLs

```
Frontend:    http://localhost:3000
Backend:     http://localhost:8000
API Docs:    http://localhost:8000/api/docs
Flower:      http://localhost:5555
Health:      http://localhost:8000/api/monitoring/health
```

## 🔧 Manual Start (If Needed)

```powershell
# Terminal 1: Redis
redis-server

# Terminal 2: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 3: Celery
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo

# Terminal 4: Frontend
cd frontend-new
npm run dev
```

## 🐛 Quick Fixes

### Redis Not Running
```powershell
redis-server
```

### PostgreSQL Not Running
```powershell
Start-Service postgresql-x64-14
```

### Port Already in Use
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Not Found
```powershell
cd backend
pip install -r requirements.txt
```

## 📊 Quick Health Checks

```bash
# Overall health
curl http://localhost:8000/api/monitoring/health

# Circuit breakers
curl http://localhost:8000/api/monitoring/circuit-breakers

# AI services
curl http://localhost:8000/api/monitoring/ai-services/health
```

## 🧪 Quick Test

```bash
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test", "language": "hindi"}'
```

## 📚 Full Documentation

- `PROJECT_RESTART_GUIDE.md` - Complete guide
- `SYSTEM_RESTART_COMPLETE.md` - Detailed reference
- `backend/QUICK_START.md` - Backend quick start

---

**That's it! You're ready to go! 🎉**
