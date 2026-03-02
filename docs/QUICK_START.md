# Quick Start Guide - Bharat Content AI Backend

## 🚀 Get Running in 5 Minutes

### 1. Setup (2 minutes)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure (1 minute)
Create `backend/.env`:
```env
DATABASE_URL=sqlite:///./bharat_content_ai.db
GEMINI_API_KEY=your_key_here
```

### 3. Initialize Database (30 seconds)
```bash
python -c "from app.config.database import init_db; init_db()"
```

### 4. Run Server (30 seconds)
```bash
uvicorn app.main:app --reload
```

### 5. Test (1 minute)
Open browser: http://localhost:8000/api/docs

---

## 📋 Common Commands

### Start Server
```bash
uvicorn app.main:app --reload --port 8000
```

### Run Tests
```bash
python ../test_api.py
```

### Reset Database
```bash
python -c "from app.config.database import drop_db, init_db; drop_db(); init_db()"
```

### Check Database
```bash
sqlite3 bharat_content_ai.db ".tables"
```

---

## 🎯 Quick API Examples

### Register User
```bash
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "role": "student"
  }'
```

### Generate Content
```bash
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write about Indian festivals",
    "language": "hindi",
    "tone": "casual",
    "content_type": "social_post",
    "user_id": 1
  }'
```

### Translate Content
```bash
curl -X POST "http://localhost:8000/api/translation/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": 1,
    "target_language": "tamil",
    "maintain_tone": true
  }'
```

### Schedule Post
```bash
curl -X POST "http://localhost:8000/api/social/schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "content_id": 1,
    "text_content": "Check this out!",
    "platform": "instagram",
    "scheduled_time": "2024-12-31T15:00:00Z"
  }'
```

### Get Analytics
```bash
curl "http://localhost:8000/api/analytics/overview/1?days=30"
```

---

## 📚 API Endpoints Cheat Sheet

### Content
- `POST /api/content/generate` - Generate content
- `GET /api/content/list?user_id=1` - List content
- `GET /api/content/{id}` - Get content
- `PUT /api/content/{id}/edit` - Edit content
- `POST /api/content/summarize` - Summarize

### Translation
- `POST /api/translation/translate` - Translate content
- `POST /api/translation/translate/direct` - Direct translation
- `POST /api/translation/batch` - Batch translate
- `GET /api/translation/supported-languages` - Languages

### Social Media
- `POST /api/social/schedule` - Schedule post
- `POST /api/social/schedule/bulk` - Bulk schedule
- `GET /api/social/list?user_id=1` - List posts
- `POST /api/social/{id}/publish` - Publish now
- `GET /api/social/calendar/{user_id}` - Calendar

### Analytics
- `GET /api/analytics/overview/{user_id}` - Overview
- `GET /api/analytics/platform-performance/{user_id}` - Platforms
- `GET /api/analytics/engagement-trends/{user_id}` - Trends
- `GET /api/analytics/top-content/{user_id}` - Top content

### Voice
- `POST /api/voice/upload` - Upload audio
- `POST /api/voice/transcribe` - Transcribe
- `POST /api/voice/{id}/to-content` - Convert to content

### Users
- `POST /api/users/register` - Register
- `GET /api/users/{id}` - Get profile
- `GET /api/users/{id}/stats` - Get stats
- `PUT /api/users/{id}` - Update profile

---

## 🔧 Troubleshooting

### Port in use?
```bash
uvicorn app.main:app --reload --port 8001
```

### Database locked?
```bash
rm bharat_content_ai.db
python -c "from app.config.database import init_db; init_db()"
```

### Import errors?
```bash
pip install -r requirements.txt --force-reinstall
```

### Can't connect?
Check if server is running:
```bash
curl http://localhost:8000/
```

---

## 📖 Documentation Links

- **Full API Docs:** http://localhost:8000/api/docs
- **API Reference:** `API_DOCUMENTATION.md`
- **Setup Guide:** `SETUP_GUIDE.md`
- **Implementation Details:** `IMPLEMENTATION_SUMMARY.md`
- **Route Details:** `app/routes/README.md`

---

## 🎓 Learning Path

1. **Start Here:** Read `SETUP_GUIDE.md`
2. **Understand Routes:** Read `app/routes/README.md`
3. **API Reference:** Check `API_DOCUMENTATION.md`
4. **Try Examples:** Use Swagger UI at `/api/docs`
5. **Run Tests:** Execute `test_api.py`
6. **Build Features:** Start coding!

---

## 💡 Pro Tips

1. **Use Swagger UI** for interactive testing
2. **Check logs** in terminal for debugging
3. **Use `--reload`** for auto-restart during development
4. **Test with curl** before frontend integration
5. **Read error messages** - they're descriptive
6. **Check database** with SQLite browser
7. **Use Postman** for complex requests
8. **Enable DEBUG** in .env for detailed logs

---

## 🎯 Common Workflows

### Create User → Generate Content → Translate → Schedule
```bash
# 1. Register user
USER_ID=$(curl -s -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"Pass123!"}' \
  | jq -r '.id')

# 2. Generate content
CONTENT_ID=$(curl -s -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Write about AI\",\"language\":\"hindi\",\"tone\":\"casual\",\"content_type\":\"social_post\",\"user_id\":$USER_ID}" \
  | jq -r '.id')

# 3. Translate
curl -X POST "http://localhost:8000/api/translation/translate" \
  -H "Content-Type: application/json" \
  -d "{\"content_id\":$CONTENT_ID,\"target_language\":\"tamil\"}"

# 4. Schedule
curl -X POST "http://localhost:8000/api/social/schedule" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":$USER_ID,\"content_id\":$CONTENT_ID,\"text_content\":\"Check this!\",\"platform\":\"instagram\",\"scheduled_time\":\"2024-12-31T15:00:00Z\"}"
```

---

## 🚨 Important Notes

- **User ID Required:** Most endpoints need a valid user_id
- **Timestamps:** Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- **Enums:** Check API docs for valid values
- **Pagination:** Use skip/limit for large lists
- **Errors:** Check response.detail for error messages

---

## 📞 Need Help?

1. Check **Swagger UI** at `/api/docs`
2. Read **error messages** carefully
3. Review **API_DOCUMENTATION.md**
4. Check **terminal logs**
5. Verify **database state**

---

## ✅ Quick Checklist

Before starting development:
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Database initialized
- [ ] Server running
- [ ] Swagger UI accessible
- [ ] Test script passes

You're ready to build! 🎉
