# Database Models Documentation

## Overview
This document describes the comprehensive database models for Bharat Content AI, designed for production-grade scalability with AWS integration.

## Models

### 1. User Model (`user.py`)
Manages user accounts with role-based access and subscription tiers.

**Key Features:**
- Multiple user roles (Student, YouTuber, Business, Teacher, Startup)
- Subscription tiers (Free, Basic, Pro, Enterprise)
- Usage tracking (content generated, translations, posts)
- AWS Cognito integration support
- Email verification and account status

**AWS Integration:**
- AWS Cognito for authentication
- Cognito user pool for user management

### 2. Content Model (`content.py`)
Stores all generated content with comprehensive metadata.

**Key Features:**
- Multiple content types (social post, blog, article, caption, script, email, ad copy)
- Tone variations (casual, formal, professional, friendly, humorous, inspirational, educational)
- AI model tracking (which model generated the content)
- Quality metrics and sentiment analysis
- Version control for content iterations
- SEO keywords and hashtag suggestions
- Engagement prediction scores

**AWS Integration:**
- AWS Bedrock for content generation
- Stores model ID and request ID for tracking
- CloudWatch for performance monitoring

### 3. Post Model (`post.py`)
Manages social media posts across multiple platforms.

**Key Features:**
- Multi-platform support (Facebook, Instagram, Twitter, LinkedIn, YouTube, WhatsApp, Telegram)
- Post scheduling with status tracking
- Real-time engagement metrics (likes, comments, shares, views, reach, impressions)
- Media attachment support
- Error handling with retry logic
- Engagement rate calculation

**AWS Integration:**
- AWS EventBridge for scheduled posting
- S3 for media storage
- Platform API integration

### 4. Translation Model (`translation.py`)
Tracks all translation operations with quality metrics.

**Key Features:**
- Multiple translation methods (AWS Translate, IndicTrans, Google Translate, Custom)
- Confidence and quality scores
- Tone preservation tracking
- Character count tracking
- Custom terminology support

**AWS Integration:**
- AWS Translate for Indian languages
- Custom terminology in AWS Translate
- Translation job tracking

### 5. Social Account Model (`social_account.py`)
Manages connected social media accounts.

**Key Features:**
- OAuth token management
- Account verification status
- Follower/following counts
- Rate limiting per platform
- Permission tracking

**AWS Integration:**
- AWS Secrets Manager for secure token storage
- Encrypted credentials

### 6. Analytics Model (`analytics.py`)
Comprehensive analytics and performance tracking.

**Key Features:**
- Daily aggregated metrics
- Language and platform usage breakdown
- Content type analysis
- Top performing content tracking
- AI usage metrics (tokens, API calls)
- Cost tracking

**Additional Model: ContentPerformance**
- Time-series performance data
- Audience demographics
- Geographic data
- Device breakdown

**AWS Integration:**
- CloudWatch for metrics
- QuickSight for visualization (optional)

### 7. Voice Input Model (`voice_input.py`)
Manages voice-to-text conversions.

**Key Features:**
- Audio file metadata
- Transcription with confidence scores
- Language detection
- Speaker identification
- Processing status tracking

**AWS Integration:**
- AWS Transcribe for speech-to-text
- S3 for audio file storage
- Support for Indian languages

### 8. AI Model Config Model (`ai_model_config.py`)
Configuration and tracking for AI models.

**Key Features:**
- Model configuration management
- Cost per token tracking
- Performance metrics
- Rate limiting configuration
- Model usage logging

**Additional Model: ModelUsageLog**
- Detailed usage tracking
- Cost calculation
- Performance monitoring
- Error tracking

**AWS Integration:**
- AWS Bedrock model management
- Cost optimization
- Performance monitoring

## AWS Services Used

### Core Services:
1. **AWS Bedrock** - LLM for content generation
   - Claude v2 (best quality)
   - Claude Instant (fast, cost-effective)
   - Llama 2 70B (open-source alternative)
   - Amazon Titan (AWS native)

2. **AWS Translate** - Indian language translation
   - Supports 10+ Indian languages
   - Custom terminology
   - Real-time translation

3. **AWS Transcribe** - Voice-to-text
   - Indian language support
   - Speaker identification
   - High accuracy

4. **AWS S3** - Media storage
   - Audio files
   - Images/videos
   - Generated content backups

5. **AWS RDS** - Database (PostgreSQL recommended)
   - High availability
   - Automated backups
   - Read replicas

6. **AWS Secrets Manager** - Secure credential storage
   - Social media tokens
   - API keys
   - Database credentials

7. **AWS EventBridge** - Scheduled posting
   - Cron-based scheduling
   - Event-driven architecture

8. **AWS CloudWatch** - Monitoring & logging
   - Application logs
   - Performance metrics
   - Alerts

### Optional Services:
- **AWS Cognito** - User authentication
- **AWS QuickSight** - Analytics visualization
- **AWS Lambda** - Serverless functions
- **AWS SQS** - Message queuing
- **AWS SNS** - Notifications

## Database Setup

### Development (SQLite):
```bash
python init_db.py
```

### Production (PostgreSQL on AWS RDS):
1. Create RDS PostgreSQL instance
2. Update DATABASE_URL in .env
3. Run migrations:
```bash
alembic upgrade head
```

## Required Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/dbname

# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# AWS Bedrock
BEDROCK_REGION=us-east-1

# AWS S3
S3_BUCKET_NAME=bharat-content-ai-media
S3_REGION=us-east-1

# AWS Translate
TRANSLATE_REGION=us-east-1

# AWS Transcribe
TRANSCRIBE_REGION=us-east-1
```

## Cost Optimization Tips

1. **Use Claude Instant** for simple content generation (cheaper than Claude v2)
2. **Cache translations** to avoid repeated API calls
3. **Use S3 lifecycle policies** for old media files
4. **Implement rate limiting** to prevent abuse
5. **Monitor usage** with CloudWatch and set billing alerts
6. **Use RDS read replicas** for analytics queries

## Next Steps

1. Get AWS credentials and set up IAM roles
2. Enable AWS Bedrock in your region
3. Create S3 bucket for media storage
4. Set up RDS PostgreSQL instance
5. Configure AWS Secrets Manager
6. Run database initialization
7. Test with sample data

## Estimated AWS Costs (Monthly)

- **AWS Bedrock**: $0.01-0.03 per 1K tokens (~$50-200/month for moderate use)
- **AWS Translate**: $15 per million characters (~$20-50/month)
- **AWS Transcribe**: $0.024 per minute (~$10-30/month)
- **AWS S3**: $0.023 per GB (~$5-20/month)
- **AWS RDS**: $50-200/month (db.t3.small to db.t3.medium)
- **Total**: ~$135-500/month for moderate usage

## Support

For questions about the models or AWS integration, refer to:
- AWS Bedrock Documentation
- AWS Translate Documentation
- SQLAlchemy Documentation
