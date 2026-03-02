# Bulk Operations - Quick Start (5 Minutes)

## 🚀 Setup

### 1. Install Redis (One-time)
```powershell
# Windows (WSL)
wsl --install
wsl
sudo apt-get install redis-server

# macOS
brew install redis
```

### 2. Install Dependencies
```powershell
cd backend
pip install celery redis flower pandas aiofiles
```

### 3. Configure Environment
Add to `backend/.env`:
```env
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## ▶️ Start Services

### Option A: Automated (Recommended)
```powershell
cd backend
.\start_bulk_services.ps1
```

### Option B: Manual
```powershell
# Terminal 1: Redis
redis-server

# Terminal 2: FastAPI
cd backend
uvicorn app.main:app --reload

# Terminal 3: Celery Worker
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo

# Terminal 4: Flower (Optional)
cd backend
celery -A app.config.celery_config.celery_app flower
```

## 📊 Service URLs

- **FastAPI**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Flower**: http://localhost:5555

## 🧪 Test It

### 1. Download Template
```bash
curl http://localhost:8000/api/bulk/templates/content-generation -o template.csv
```

### 2. Upload CSV
```bash
curl -X POST "http://localhost:8000/api/bulk/upload" \
  -F "file=@template.csv" \
  -F "operation_type=content_generation" \
  -F "batch_size=10"
```

Response:
```json
{
  "task_id": "abc123-def456",
  "total_rows": 10,
  "status": "queued",
  "progress_url": "/api/bulk/progress/abc123-def456"
}
```

### 3. Monitor Progress
```bash
# Polling
curl http://localhost:8000/api/bulk/progress/abc123-def456

# SSE Stream
curl -N http://localhost:8000/api/bulk/progress-stream/abc123-def456
```

### 4. Get Results
```bash
curl http://localhost:8000/api/bulk/result/abc123-def456
```

## 📝 CSV Formats

### Content Generation
```csv
prompt,language,content_type,tone,platform,keywords
"Write about AI",hindi,social_post,casual,instagram,"AI,tech"
```

### Translation
```csv
text,source_language,target_language,preserve_formatting
"Hello",english,hindi,true
```

### Scheduling
```csv
content_id,platform,scheduled_time,caption,hashtags
123,facebook,2024-12-01T10:00:00Z,"Post!","#social"
```

## 🔧 Common Commands

### Check Redis
```bash
redis-cli ping  # Should return: PONG
```

### Check Celery Workers
```bash
celery -A app.config.celery_config.celery_app inspect active
```

### Monitor Redis Queue
```bash
redis-cli
LLEN celery
KEYS task_progress:*
```

### View Logs
```bash
# Celery debug logs
celery -A app.config.celery_config.celery_app worker --loglevel=debug

# FastAPI debug logs
uvicorn app.main:app --log-level debug
```

## 🐛 Troubleshooting

### Redis Not Running
```bash
redis-cli ping
# If fails: redis-server
```

### Celery Worker Not Starting
```bash
# Ensure you're in backend directory
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo
```

### Task Stuck
```bash
# Check worker status
celery -A app.config.celery_config.celery_app inspect active

# Restart worker (Ctrl+C, then restart)
```

## 📱 Frontend Integration

### Upload
```typescript
const formData = new FormData();
formData.append('file', csvFile);
formData.append('operation_type', 'content_generation');

const res = await fetch('/api/bulk/upload', {
  method: 'POST',
  body: formData
});

const { task_id } = await res.json();
```

### Monitor with SSE
```typescript
const eventSource = new EventSource(`/api/bulk/progress-stream/${taskId}`);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`Progress: ${data.percentage}%`);
  
  if (data.status === 'completed') {
    eventSource.close();
  }
};
```

## 📚 Documentation

- **Complete Guide**: `BULK_OPERATIONS_GUIDE.md`
- **Implementation Details**: `BULK_OPERATIONS_COMPLETE.md`
- **API Docs**: http://localhost:8000/api/docs

## ✅ Checklist

- [ ] Redis installed and running
- [ ] Dependencies installed
- [ ] .env configured
- [ ] FastAPI server started
- [ ] Celery worker started
- [ ] Tested with sample CSV
- [ ] Flower dashboard accessible
- [ ] Frontend integration complete

## 🎯 Next Steps

1. ✅ Test locally with sample CSVs
2. ✅ Integrate with frontend
3. ✅ Monitor with Flower
4. ✅ Deploy to production
5. ✅ Setup AWS ElastiCache Redis

---

**Status**: ✅ READY TO USE  
**Time to Setup**: 5 minutes  
**Time to First Bulk Operation**: 10 minutes
