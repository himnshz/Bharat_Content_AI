# Backend Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./bharat_content_ai.db

# For PostgreSQL (Production)
# DATABASE_URL=postgresql://username:password@localhost:5432/bharat_content_ai

# Google Gemini API (Free tier available)
GEMINI_API_KEY=your_gemini_api_key_here

# AWS Configuration (Optional - for Bedrock)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# AWS Bedrock Model IDs
BEDROCK_MODEL_ID=anthropic.claude-v2

# Application Settings
APP_ENV=development
DEBUG=True
```

### 3. Initialize Database

```bash
python -c "from app.config.database import init_db; init_db()"
```

This will create all necessary tables in your database.

### 4. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base:** http://localhost:8000/api
- **Swagger Docs:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

### 5. Test the API

Run the comprehensive test suite:

```bash
python ../test_api.py
```

Or test individual endpoints using the Swagger UI at http://localhost:8000/api/docs

---

## Project Structure

```
backend/
├── app/
│   ├── config/
│   │   ├── database.py          # Database configuration
│   │   ├── settings.py          # App settings
│   │   └── aws_config.py        # AWS configuration
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── content.py           # Content model
│   │   ├── post.py              # Post model
│   │   ├── translation.py       # Translation model
│   │   ├── analytics.py         # Analytics models
│   │   └── voice_input.py       # Voice input model
│   ├── routes/
│   │   ├── content.py           # Content generation endpoints
│   │   ├── translation.py       # Translation endpoints
│   │   ├── social.py            # Social media endpoints
│   │   ├── analytics.py         # Analytics endpoints
│   │   ├── voice.py             # Voice input endpoints
│   │   └── users.py             # User management endpoints
│   ├── services/
│   │   ├── content_generation/  # AI content generation
│   │   ├── translation/         # Translation services
│   │   ├── social_media/        # Social media integration
│   │   ├── analytics/           # Analytics tracking
│   │   └── voice/               # Voice processing
│   └── main.py                  # FastAPI application
├── requirements.txt
├── .env.example
├── API_DOCUMENTATION.md
└── SETUP_GUIDE.md
```

---

## API Endpoints Overview

### Content Generation
- `POST /api/content/generate` - Generate AI content
- `GET /api/content/list` - List all content
- `GET /api/content/{id}` - Get specific content
- `PUT /api/content/{id}/edit` - Edit content
- `POST /api/content/summarize` - Summarize content
- `DELETE /api/content/{id}` - Delete content

### Translation
- `POST /api/translation/translate` - Translate content
- `POST /api/translation/translate/direct` - Direct text translation
- `POST /api/translation/batch` - Batch translate to multiple languages
- `GET /api/translation/list/{content_id}` - List translations
- `GET /api/translation/supported-languages` - Get supported languages

### Social Media
- `POST /api/social/schedule` - Schedule a post
- `POST /api/social/schedule/bulk` - Bulk schedule to multiple platforms
- `GET /api/social/list` - List posts
- `PUT /api/social/{id}` - Update post
- `POST /api/social/{id}/publish` - Publish immediately
- `POST /api/social/{id}/cancel` - Cancel scheduled post
- `GET /api/social/calendar/{user_id}` - Get calendar view

### Analytics
- `GET /api/analytics/overview/{user_id}` - Analytics overview
- `GET /api/analytics/platform-performance/{user_id}` - Platform metrics
- `GET /api/analytics/content-type-performance/{user_id}` - Content type metrics
- `GET /api/analytics/engagement-trends/{user_id}` - Engagement trends
- `GET /api/analytics/top-content/{user_id}` - Top performing content
- `POST /api/analytics/sync-metrics/{post_id}` - Sync metrics

### Voice Input
- `POST /api/voice/upload` - Upload audio file
- `POST /api/voice/transcribe` - Transcribe audio
- `GET /api/voice/list` - List voice inputs
- `POST /api/voice/{id}/to-content` - Convert to content

### User Management
- `POST /api/users/register` - Register new user
- `GET /api/users/{id}` - Get user profile
- `PUT /api/users/{id}` - Update user
- `GET /api/users/{id}/stats` - Get user statistics
- `POST /api/users/{id}/upgrade-subscription` - Upgrade subscription

---

## Database Models

### User
- Email, username, password (hashed)
- Role (student, youtuber, business, teacher, startup)
- Subscription tier (free, basic, pro, enterprise)
- Usage statistics

### Content
- Original prompt and generated content
- Content type, language, tone
- AI model metadata
- Quality metrics and keywords

### Post
- Platform (Facebook, Instagram, Twitter, etc.)
- Scheduling and publishing info
- Engagement metrics (likes, comments, shares, views)

### Translation
- Source and target languages
- Translation method (IndicTrans)
- Quality score

### Analytics
- Daily aggregated metrics
- Platform and language breakdowns
- Engagement tracking

### VoiceInput
- Audio file metadata
- Transcription results
- Language detection

---

## Development Tips

### Database Migrations

When you modify models, create a migration:

```bash
# Generate migration
alembic revision --autogenerate -m "Description of changes"

# Apply migration
alembic upgrade head
```

### Reset Database

To start fresh:

```bash
python -c "from app.config.database import drop_db, init_db; drop_db(); init_db()"
```

### Environment-Specific Settings

- **Development:** Use SQLite for quick setup
- **Production:** Use PostgreSQL with AWS RDS
- **Testing:** Use separate test database

### API Testing

1. **Swagger UI:** http://localhost:8000/api/docs
   - Interactive API documentation
   - Try endpoints directly in browser

2. **Test Script:** `python test_api.py`
   - Automated testing of all endpoints
   - Creates test data automatically

3. **Postman/Insomnia:** Import OpenAPI spec from `/api/docs`

---

## Troubleshooting

### Database Connection Issues

```bash
# Check if database file exists
ls -la bharat_content_ai.db

# Reinitialize database
python -c "from app.config.database import init_db; init_db()"
```

### Import Errors

```bash
# Make sure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### CORS Issues

The API allows all origins by default. In production, update `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Production Deployment

### AWS Deployment

1. **Database:** AWS RDS (PostgreSQL)
2. **API:** AWS Elastic Beanstalk or ECS
3. **File Storage:** AWS S3 for audio files
4. **AI Services:** AWS Bedrock for content generation
5. **Transcription:** AWS Transcribe for voice-to-text

### Environment Variables for Production

```env
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/dbname
AWS_ACCESS_KEY_ID=your_production_key
AWS_SECRET_ACCESS_KEY=your_production_secret
AWS_REGION=ap-south-1
APP_ENV=production
DEBUG=False
```

### Security Checklist

- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Implement JWT authentication
- [ ] Set up rate limiting
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable database backups
- [ ] Set up monitoring and logging

---

## Next Steps

1. **Implement Authentication:** Add JWT token-based auth
2. **Integrate Real AI Services:** Connect Gemini/Bedrock APIs
3. **Add Social Media APIs:** Integrate Facebook, Instagram, Twitter APIs
4. **Implement Background Jobs:** Use Celery for scheduled posts
5. **Add Caching:** Use Redis for performance
6. **Set Up Monitoring:** CloudWatch, Sentry, or similar
7. **Write Unit Tests:** Add pytest test suite
8. **API Versioning:** Implement /api/v1/ versioning

---

## Support

For issues or questions:
- Check API documentation: `/api/docs`
- Review error logs in console
- Refer to `API_DOCUMENTATION.md` for endpoint details
