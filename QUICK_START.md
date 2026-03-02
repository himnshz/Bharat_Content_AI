# Quick Start Guide

Get Bharat Content AI running in 5 minutes!

---

## 1. Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn app.main:app --reload --port 8000
```

**Backend running at:** http://localhost:8000  
**API Docs:** http://localhost:8000/api/docs

---

## 2. Frontend Setup (2 minutes)

```bash
# Open new terminal
cd frontend-new

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend running at:** http://localhost:3000

---

## 3. Configure AI Services (1 minute)

Create `backend/.env`:

```env
# Required: Choose at least one AI provider

# Option 1: Google Gemini (Recommended - Free tier available)
GEMINI_API_KEY=your_gemini_api_key_here

# Option 2: AWS Bedrock
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1

# Database (SQLite by default)
DATABASE_URL=sqlite:///./bharat_content_ai.db

# JWT Secret
SECRET_KEY=your-secret-key-change-this-in-production
```

---

## 4. Test the Application

### Generate Content
1. Open http://localhost:3000
2. Click "Generate Content"
3. Enter a prompt: "Write a social media post about Diwali"
4. Select language: Hindi
5. Click "Generate"

### Translate Content
1. Click "Translate"
2. Enter text in English
3. Select target language
4. Click "Translate"

---

## 🎉 You're Ready!

### What's Working
- ✅ Content generation with AI
- ✅ Translation to 11+ Indian languages
- ✅ Social media scheduling
- ✅ Analytics dashboard
- ✅ Campaign management
- ✅ Team collaboration
- ✅ Template library

### Optional Setup

#### Redis (for bulk operations)
```bash
# Install Redis
# Windows: Download from https://github.com/microsoftarchive/redis/releases
# Mac: brew install redis
# Linux: sudo apt-get install redis-server

# Start Redis
redis-server

# Add to backend/.env
REDIS_URL=redis://localhost:6379/0
```

#### Celery Worker (for bulk operations)
```bash
cd backend
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo
```

---

## 🆘 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.10+)
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Delete node_modules: `rm -rf node_modules`
- Reinstall: `npm install`

### AI generation fails
- Check `.env` file exists in `backend/`
- Verify API keys are correct
- Check API docs: http://localhost:8000/api/docs

### Port already in use
```bash
# Backend (change port)
uvicorn app.main:app --reload --port 8001

# Frontend (change port)
npm run dev -- -p 3001
```

---

## 📚 Next Steps

1. **Read Documentation:** Check `/docs` folder
2. **Explore API:** http://localhost:8000/api/docs
3. **Configure Features:** See `docs/` for detailed guides
4. **Deploy:** See deployment guides in `docs/`

---

## 🚀 Scripts Available

Located in `/scripts`:
- `start_all_services.ps1` - Start backend + frontend + Redis + Celery
- `check_system_status.ps1` - Check if all services are running

---

**Happy content creating! 🎨**
