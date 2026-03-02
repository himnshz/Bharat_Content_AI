# Bharat Content AI - API Documentation

## Overview
This document provides comprehensive documentation for all API endpoints in the Bharat Content AI backend.

**Base URL:** `http://localhost:8000/api`

**API Documentation:** `http://localhost:8000/api/docs` (Swagger UI)

---

## Table of Contents
1. [Content Generation](#content-generation)
2. [Translation](#translation)
3. [Social Media](#social-media)
4. [Analytics](#analytics)
5. [Voice Input](#voice-input)
6. [User Management](#user-management)

---

## Content Generation

### Generate Content
**POST** `/api/content/generate`

Generate AI-powered content using Google Gemini or AWS Bedrock.

**Request Body:**
```json
{
  "prompt": "Create a social media post about Indian festivals",
  "language": "hindi",
  "tone": "casual",
  "content_type": "social_post",
  "user_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "original_prompt": "Create a social media post about Indian festivals",
  "generated_content": "भारतीय त्योहार हमारी संस्कृति का अभिन्न हिस्सा हैं...",
  "content_type": "social_post",
  "status": "generated",
  "language": "hindi",
  "tone": "casual",
  "model_used": "gemini-pro",
  "generation_time_ms": 1250,
  "word_count": 45,
  "quality_score": 85.0,
  "keywords": ["festivals", "culture", "celebration"],
  "hashtags": ["#IndianFestivals", "#Culture"],
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Content
**GET** `/api/content/list?user_id=1&skip=0&limit=20`

List all content for a user with pagination and filters.

**Query Parameters:**
- `user_id` (required): User ID
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 20)
- `content_type` (optional): Filter by content type
- `language` (optional): Filter by language
- `status` (optional): Filter by status

### Get Content by ID
**GET** `/api/content/{content_id}`

### Edit Content
**PUT** `/api/content/{content_id}/edit`

**Request Body:**
```json
{
  "edited_content": "Updated content text..."
}
```

### Summarize Content
**POST** `/api/content/summarize`

**Request Body:**
```json
{
  "content_id": 1,
  "target_length": 100
}
```

### Delete Content
**DELETE** `/api/content/{content_id}`

---

## Translation

### Translate Content
**POST** `/api/translation/translate`

Translate existing content to Indian languages using IndicTrans.

**Request Body:**
```json
{
  "content_id": 1,
  "target_language": "tamil",
  "source_language": "hindi",
  "maintain_tone": true,
  "cultural_adaptation": false
}
```

**Response:**
```json
{
  "id": 1,
  "content_id": 1,
  "source_language": "hindi",
  "target_language": "tamil",
  "original_text": "भारतीय त्योहार...",
  "translated_text": "இந்திய திருவிழாக்கள்...",
  "method": "indictrans",
  "quality_score": 92.5,
  "translation_time_ms": 850,
  "created_at": "2024-01-15T10:35:00Z"
}
```

### Direct Translation
**POST** `/api/translation/translate/direct`

Translate text directly without creating content first.

**Request Body:**
```json
{
  "text": "Hello, how are you?",
  "source_language": "english",
  "target_language": "hindi",
  "tone": "neutral",
  "user_id": 1
}
```

### Batch Translation
**POST** `/api/translation/batch?content_id=1`

**Request Body:**
```json
{
  "target_languages": ["tamil", "telugu", "bengali"]
}
```

### List Translations
**GET** `/api/translation/list/{content_id}`

### Get Supported Languages
**GET** `/api/translation/supported-languages`

**Response:**
```json
{
  "languages": [
    {"name": "hindi", "code": "hi"},
    {"name": "tamil", "code": "ta"},
    {"name": "telugu", "code": "te"},
    {"name": "bengali", "code": "bn"}
  ],
  "total": 11
}
```

---

## Social Media

### Schedule Post
**POST** `/api/social/schedule`

Schedule a post to a social media platform.

**Request Body:**
```json
{
  "user_id": 1,
  "content_id": 1,
  "text_content": "Check out our latest blog post!",
  "platform": "instagram",
  "scheduled_time": "2024-01-20T15:00:00Z",
  "media_urls": ["https://example.com/image.jpg"],
  "title": "New Blog Post"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "content_id": 1,
  "title": "New Blog Post",
  "text_content": "Check out our latest blog post!",
  "platform": "instagram",
  "status": "scheduled",
  "scheduled_time": "2024-01-20T15:00:00Z",
  "published_time": null,
  "media_urls": ["https://example.com/image.jpg"],
  "likes_count": 0,
  "comments_count": 0,
  "shares_count": 0,
  "views_count": 0,
  "engagement_rate": 0,
  "created_at": "2024-01-15T10:40:00Z"
}
```

### Bulk Schedule
**POST** `/api/social/schedule/bulk`

Schedule the same content to multiple platforms.

**Request Body:**
```json
{
  "user_id": 1,
  "content_id": 1,
  "platforms": ["facebook", "instagram", "twitter"],
  "scheduled_time": "2024-01-20T15:00:00Z",
  "customize_per_platform": true
}
```

### List Posts
**GET** `/api/social/list?user_id=1&platform=instagram&status=scheduled`

### Get Post by ID
**GET** `/api/social/{post_id}`

### Update Post
**PUT** `/api/social/{post_id}`

### Publish Post Now
**POST** `/api/social/{post_id}/publish`

Bypass scheduling and publish immediately.

### Cancel Scheduled Post
**POST** `/api/social/{post_id}/cancel`

### Get Post Calendar
**GET** `/api/social/calendar/{user_id}?start_date=2024-01-01&end_date=2024-01-31`

Get all scheduled posts for calendar view.

### Delete Post
**DELETE** `/api/social/{post_id}`

---

## Analytics

### Get Analytics Overview
**GET** `/api/analytics/overview/{user_id}?days=30`

Get comprehensive analytics for a user.

**Response:**
```json
{
  "total_content_generated": 45,
  "total_translations": 23,
  "total_posts_scheduled": 30,
  "total_posts_published": 25,
  "total_engagement": {
    "likes": 1250,
    "comments": 340,
    "shares": 180,
    "views": 15000
  },
  "avg_engagement_rate": 4.5,
  "top_performing_language": "hindi",
  "top_performing_platform": "instagram",
  "period_start": "2023-12-15",
  "period_end": "2024-01-15"
}
```

### Get Platform Performance
**GET** `/api/analytics/platform-performance/{user_id}?days=30`

**Response:**
```json
[
  {
    "platform": "instagram",
    "total_posts": 15,
    "total_likes": 850,
    "total_comments": 200,
    "total_shares": 120,
    "total_views": 8500,
    "avg_engagement_rate": 5.2
  }
]
```

### Get Content Type Performance
**GET** `/api/analytics/content-type-performance/{user_id}?days=30`

### Get Engagement Trends
**GET** `/api/analytics/engagement-trends/{user_id}?days=30`

Returns daily engagement metrics for trend visualization.

### Get Top Content
**GET** `/api/analytics/top-content/{user_id}?limit=10&days=30`

### Get Language Distribution
**GET** `/api/analytics/language-distribution/{user_id}?days=30`

### Sync Post Metrics
**POST** `/api/analytics/sync-metrics/{post_id}`

Manually trigger sync of engagement metrics from social platforms.

---

## Voice Input

### Upload Voice Input
**POST** `/api/voice/upload`

Upload an audio file for transcription.

**Form Data:**
- `user_id`: User ID
- `audio_file`: Audio file (MP3, WAV, M4A)
- `language` (optional): Expected language

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "audio_file_url": "https://s3.amazonaws.com/...",
  "audio_duration_seconds": null,
  "audio_format": "mp3",
  "transcribed_text": null,
  "language_detected": null,
  "language_specified": "hindi",
  "status": "processing",
  "created_at": "2024-01-15T10:45:00Z"
}
```

### Transcribe Audio
**POST** `/api/voice/transcribe`

**Request Body:**
```json
{
  "voice_input_id": 1,
  "language": "hindi"
}
```

### List Voice Inputs
**GET** `/api/voice/list?user_id=1&status=completed`

### Get Voice Input by ID
**GET** `/api/voice/{voice_input_id}`

### Convert Voice to Content
**POST** `/api/voice/{voice_input_id}/to-content`

Convert transcribed voice input directly to generated content.

### Delete Voice Input
**DELETE** `/api/voice/{voice_input_id}`

---

## User Management

### Register User
**POST** `/api/users/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "role": "student",
  "preferred_language": "hindi"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "student",
  "subscription_tier": "free",
  "preferred_language": "hindi",
  "is_active": true,
  "is_verified": false,
  "email_verified": false,
  "content_generated_count": 0,
  "translations_count": 0,
  "posts_scheduled_count": 0,
  "created_at": "2024-01-15T10:50:00Z",
  "last_login": null
}
```

### Get User by ID
**GET** `/api/users/{user_id}`

### Get User by Username
**GET** `/api/users/username/{username}`

### Update User
**PUT** `/api/users/{user_id}`

**Request Body:**
```json
{
  "full_name": "John Smith",
  "preferred_language": "tamil",
  "role": "business"
}
```

### Get User Stats
**GET** `/api/users/{user_id}/stats`

**Response:**
```json
{
  "user_id": 1,
  "username": "johndoe",
  "total_content": 45,
  "total_translations": 23,
  "total_posts": 30,
  "total_published": 25,
  "account_age_days": 90,
  "subscription_tier": "free"
}
```

### Upgrade Subscription
**POST** `/api/users/{user_id}/upgrade-subscription?tier=pro`

### Verify Email
**POST** `/api/users/{user_id}/verify-email`

### Record Login
**POST** `/api/users/{user_id}/login`

### Delete User
**DELETE** `/api/users/{user_id}`

Soft delete (deactivates account).

---

## Enums and Constants

### ContentType
- `social_post`
- `blog`
- `article`
- `caption`
- `script`
- `email`
- `ad_copy`

### ContentStatus
- `draft`
- `generated`
- `edited`
- `published`
- `archived`

### ToneType
- `casual`
- `formal`
- `professional`
- `friendly`
- `humorous`
- `inspirational`
- `educational`

### Platform
- `facebook`
- `instagram`
- `twitter`
- `linkedin`
- `youtube`
- `whatsapp`
- `telegram`

### PostStatus
- `draft`
- `scheduled`
- `publishing`
- `published`
- `failed`
- `cancelled`

### UserRole
- `student`
- `youtuber`
- `business`
- `teacher`
- `startup`

### SubscriptionTier
- `free`
- `basic`
- `pro`
- `enterprise`

---

## Error Responses

All endpoints return standard error responses:

**400 Bad Request:**
```json
{
  "detail": "Validation error message"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Authentication

Currently, the API uses simple user_id based authentication. In production, implement:
- JWT token-based authentication
- OAuth2 with AWS Cognito
- API key authentication for external integrations

---

## Rate Limiting

Recommended rate limits by subscription tier:
- **Free:** 100 requests/hour
- **Basic:** 500 requests/hour
- **Pro:** 2000 requests/hour
- **Enterprise:** Unlimited

---

## Testing

Use the test script to verify API functionality:

```bash
python test_api.py
```

Or use the interactive Swagger UI at `/api/docs`.
