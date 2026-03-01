# Backend Routes Documentation

This directory contains all API route handlers for the Bharat Content AI application.

## Route Files

### 1. content.py - Content Generation Routes
Handles AI-powered content generation using Google Gemini or AWS Bedrock.

**Key Features:**
- Generate content from prompts
- Support for multiple content types (social posts, blogs, articles, etc.)
- Multiple tone options (casual, formal, professional, etc.)
- Content editing and versioning
- Automatic keyword and hashtag extraction
- Content summarization
- Quality scoring

**Endpoints:**
- `POST /generate` - Generate new content
- `GET /list` - List user's content with filters
- `GET /{content_id}` - Get specific content
- `PUT /{content_id}/edit` - Edit generated content
- `POST /summarize` - Summarize existing content
- `DELETE /{content_id}` - Delete content

**Database Integration:**
- Creates `Content` records with full metadata
- Updates user statistics
- Tracks generation metrics

---

### 2. translation.py - Translation Routes
Handles translation between Indian languages using IndicTrans.

**Key Features:**
- Translate existing content to 11+ Indian languages
- Direct text translation without content creation
- Batch translation to multiple languages
- Tone preservation
- Cultural adaptation options
- Quality scoring

**Supported Languages:**
- Hindi, Tamil, Telugu, Bengali, Marathi
- Gujarati, Kannada, Malayalam, Punjabi, Odia, English

**Endpoints:**
- `POST /translate` - Translate existing content
- `POST /translate/direct` - Direct text translation
- `POST /batch` - Batch translate to multiple languages
- `GET /list/{content_id}` - List all translations for content
- `GET /{translation_id}` - Get specific translation
- `GET /supported-languages` - Get list of supported languages
- `DELETE /{translation_id}` - Delete translation

**Database Integration:**
- Creates `Translation` records
- Links to original content
- Updates user translation count

---

### 3. social.py - Social Media Routes
Handles scheduling and publishing to social media platforms.

**Key Features:**
- Schedule posts to 7+ platforms
- Bulk scheduling to multiple platforms
- Calendar view for scheduled posts
- Immediate publishing option
- Post cancellation
- Platform-specific customization
- Engagement metrics tracking

**Supported Platforms:**
- Facebook, Instagram, Twitter, LinkedIn
- YouTube, WhatsApp, Telegram

**Endpoints:**
- `POST /schedule` - Schedule a single post
- `POST /schedule/bulk` - Schedule to multiple platforms
- `GET /list` - List posts with filters
- `GET /{post_id}` - Get specific post
- `PUT /{post_id}` - Update scheduled post
- `POST /{post_id}/publish` - Publish immediately
- `POST /{post_id}/cancel` - Cancel scheduled post
- `GET /calendar/{user_id}` - Get calendar view
- `DELETE /{post_id}` - Delete post

**Database Integration:**
- Creates `Post` records
- Tracks scheduling and publishing status
- Stores engagement metrics
- Updates user post count

---

### 4. analytics.py - Analytics Routes
Provides comprehensive analytics and performance metrics.

**Key Features:**
- Overall analytics dashboard
- Platform-specific performance
- Content type analysis
- Engagement trends over time
- Top performing content
- Language distribution
- Metric synchronization

**Endpoints:**
- `GET /overview/{user_id}` - Comprehensive overview
- `GET /platform-performance/{user_id}` - Platform breakdown
- `GET /content-type-performance/{user_id}` - Content type analysis
- `GET /engagement-trends/{user_id}` - Daily trends
- `GET /top-content/{user_id}` - Top performing content
- `GET /language-distribution/{user_id}` - Language usage stats
- `POST /sync-metrics/{post_id}` - Sync engagement metrics

**Metrics Tracked:**
- Likes, comments, shares, views
- Reach and impressions
- Engagement rate
- Content generation stats
- Translation usage
- Platform distribution

**Database Integration:**
- Queries `Analytics` and `ContentPerformance` tables
- Aggregates data from `Post` and `Content` tables
- Provides time-series data

---

### 5. voice.py - Voice Input Routes
Handles voice-to-text transcription and processing.

**Key Features:**
- Audio file upload (MP3, WAV, M4A)
- AWS Transcribe integration
- Language detection
- Confidence scoring
- Direct conversion to content
- Speaker identification support

**Endpoints:**
- `POST /upload` - Upload audio file
- `POST /transcribe` - Trigger transcription
- `GET /list` - List voice inputs
- `GET /{voice_input_id}` - Get specific voice input
- `POST /{voice_input_id}/to-content` - Convert to content
- `DELETE /{voice_input_id}` - Delete voice input

**Database Integration:**
- Creates `VoiceInput` records
- Stores audio metadata
- Tracks transcription status
- Links to S3 storage

---

### 6. users.py - User Management Routes
Handles user registration, profiles, and account management.

**Key Features:**
- User registration with password hashing
- Profile management
- Subscription tier management
- Usage statistics
- Email verification
- Login tracking

**User Roles:**
- Student, YouTuber, Business, Teacher, Startup

**Subscription Tiers:**
- Free, Basic, Pro, Enterprise

**Endpoints:**
- `POST /register` - Register new user
- `GET /{user_id}` - Get user profile
- `GET /username/{username}` - Get user by username
- `PUT /{user_id}` - Update user profile
- `GET /{user_id}/stats` - Get user statistics
- `POST /{user_id}/upgrade-subscription` - Upgrade tier
- `POST /{user_id}/verify-email` - Verify email
- `POST /{user_id}/login` - Record login
- `DELETE /{user_id}` - Deactivate account

**Security:**
- Bcrypt password hashing
- Soft delete (deactivation)
- Email verification support

**Database Integration:**
- Creates and manages `User` records
- Tracks usage statistics
- Manages subscription tiers

---

## Common Patterns

### Request/Response Models
All routes use Pydantic models for:
- Request validation
- Response serialization
- Type safety
- Automatic API documentation

### Database Sessions
All routes use FastAPI's dependency injection:
```python
async def endpoint(db: Session = Depends(get_db)):
    # Database operations
```

### Error Handling
Consistent error responses:
- `400` - Bad Request (validation errors)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error (unexpected errors)

### Pagination
List endpoints support pagination:
- `skip` - Number of records to skip
- `limit` - Maximum records to return

### Filtering
List endpoints support filtering by:
- Status
- Type
- Language
- Platform
- Date range

---

## Integration Points

### AI Services
- **Content Generation:** Gemini or Bedrock
- **Translation:** IndicTrans (to be integrated)
- **Voice:** AWS Transcribe (to be integrated)

### Storage
- **Audio Files:** AWS S3 (to be integrated)
- **Database:** SQLite (dev) / PostgreSQL (prod)

### Background Jobs
- **Post Scheduling:** AWS EventBridge (to be integrated)
- **Metric Sync:** Periodic background tasks

### Social Media APIs
- **Publishing:** Platform-specific APIs (to be integrated)
- **Metrics:** Platform analytics APIs (to be integrated)

---

## Testing

Each route can be tested using:

1. **Swagger UI:** http://localhost:8000/api/docs
2. **Test Script:** `python test_api.py`
3. **Manual Testing:** Using curl or Postman

Example curl command:
```bash
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write about AI",
    "language": "hindi",
    "tone": "casual",
    "content_type": "social_post",
    "user_id": 1
  }'
```

---

## Future Enhancements

### Authentication
- [ ] JWT token-based authentication
- [ ] OAuth2 integration
- [ ] API key management
- [ ] Role-based access control

### Rate Limiting
- [ ] Per-user rate limits
- [ ] Tier-based quotas
- [ ] API throttling

### Caching
- [ ] Redis caching for analytics
- [ ] Content caching
- [ ] Translation caching

### Webhooks
- [ ] Post publication webhooks
- [ ] Metric update webhooks
- [ ] Error notification webhooks

### Advanced Features
- [ ] Content scheduling recommendations
- [ ] A/B testing support
- [ ] Sentiment analysis
- [ ] Trend detection
- [ ] Competitor analysis

---

## Maintenance

### Adding New Endpoints

1. Define Pydantic models for request/response
2. Implement route handler with proper error handling
3. Add database operations using SQLAlchemy
4. Update `main.py` to include the router
5. Add tests to `test_api.py`
6. Update API documentation

### Modifying Existing Endpoints

1. Update Pydantic models if needed
2. Modify route handler logic
3. Update database queries
4. Test thoroughly
5. Update documentation

### Database Schema Changes

1. Modify model in `app/models/`
2. Create Alembic migration
3. Test migration on dev database
4. Update route handlers if needed
5. Deploy migration to production

---

## Best Practices

1. **Always validate input** using Pydantic models
2. **Use database transactions** for multi-step operations
3. **Handle errors gracefully** with appropriate HTTP status codes
4. **Log important operations** for debugging
5. **Keep routes thin** - move business logic to services
6. **Document complex logic** with comments
7. **Test edge cases** thoroughly
8. **Use type hints** for better IDE support
9. **Follow REST conventions** for endpoint naming
10. **Version your API** when making breaking changes
