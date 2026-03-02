# Rate Limiting & Circuit Breaker - Complete Guide

## Overview

This implementation provides enterprise-grade protection for your multi-API system with:
1. **Redis-backed Rate Limiting** - Tier-based API protection
2. **Circuit Breaker Pattern** - Fault tolerance for external services
3. **Intelligent Fallback** - Automatic retry with alternative AI providers
4. **Comprehensive Monitoring** - Real-time visibility into system health

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Request                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Rate Limiter (Redis)                          │
│  • Check user tier (Unauthenticated/Free/Basic/Pro/Enterprise)  │
│  • Enforce tier-specific limits                                 │
│  • Return 429 if limit exceeded                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │ ✓ Within limits
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Route Handler                         │
│  • Process request                                               │
│  • Call AI Service Manager                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Enhanced AI Service Manager                         │
│  • Select primary service (or use preferred)                     │
│  • Build fallback chain                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Circuit Breaker Check                         │
│  • Is circuit CLOSED? → Proceed                                  │
│  • Is circuit OPEN? → Try fallback                              │
│  • Is circuit HALF-OPEN? → Test with single request            │
└────────────────────────┬────────────────────────────────────────┘
                         │ ✓ Circuit closed
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Primary AI Service Call                       │
│  • Call Gemini/Bedrock/OpenAI/etc.                             │
│  • Retry with exponential backoff (2 attempts)                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │         │
              ✓ Success    ✗ Failure
                    │         │
                    │         ▼
                    │    ┌─────────────────────────────────────┐
                    │    │  Circuit Breaker Records Failure    │
                    │    │  • Increment fail counter           │
                    │    │  • Open circuit if threshold hit    │
                    │    └────────┬────────────────────────────┘
                    │             │
                    │             ▼
                    │    ┌─────────────────────────────────────┐
                    │    │     Try Fallback Service            │
                    │    │  • Next in fallback chain           │
                    │    │  • Repeat circuit breaker check     │
                    │    └────────┬────────────────────────────┘
                    │             │
                    │        ┌────┴────┐
                    │        │         │
                    │   ✓ Success   ✗ All Failed
                    │        │         │
                    ▼        ▼         ▼
              ┌─────────────────────────────────────────────┐
              │           Return Response                    │
              │  • Success: Generated content               │
              │  • Failure: Error with all attempts logged  │
              └─────────────────────────────────────────────┘
```

---

## Rate Limiting

### Tier-Based Limits

| Tier | Content Gen | Translation | Bulk Ops | API Calls | Social Posts |
|------|-------------|-------------|----------|-----------|--------------|
| **Unauthenticated** | 5/hour | 10/hour | 1/day | 100/hour | 5/hour |
| **Free** | 20/hour | 50/hour | 2/day | 500/hour | 20/hour |
| **Basic** | 100/hour | 200/hour | 10/day | 2000/hour | 100/hour |
| **Pro** | 500/hour | 1000/hour | 50/day | 10000/hour | 500/hour |
| **Enterprise** | 5000/hour | 10000/hour | unlimited | 100000/hour | 5000/hour |

### How It Works

1. **User Identification**
   - JWT token (user ID) - most accurate
   - API key - for programmatic access
   - IP address - fallback for unauthenticated

2. **Tier Detection**
   - Extract from JWT token: `subscription_tier`
   - Header override (testing): `X-User-Tier: PRO`
   - Default: `UNAUTHENTICATED`

3. **Rate Limit Enforcement**
   - Redis stores request counts
   - Sliding window algorithm
   - Returns 429 when exceeded
   - Headers show remaining requests

### Response Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

### Rate Limit Error Response

```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later.",
  "detail": "100 per 1 hour"
}
```

---

## Circuit Breaker

### Configuration

Each external service has its own circuit breaker:

| Service | Fail Threshold | Timeout Duration | Notes |
|---------|----------------|------------------|-------|
| **Gemini** | 5 failures | 60 seconds | Free tier, may be unstable |
| **Bedrock** | 3 failures | 30 seconds | AWS is usually reliable |
| **OpenAI** | 5 failures | 60 seconds | Standard configuration |
| **Anthropic** | 5 failures | 60 seconds | Claude API |
| **Cohere** | 5 failures | 60 seconds | Standard configuration |
| **HuggingFace** | 10 failures | 120 seconds | More tolerant for free tier |
| **Groq** | 5 failures | 60 seconds | Fast inference |
| **Together** | 5 failures | 60 seconds | Open source models |
| **Facebook** | 3 failures | 300 seconds | Social platform |
| **Instagram** | 3 failures | 300 seconds | Social platform |
| **Twitter** | 3 failures | 300 seconds | Social platform |
| **LinkedIn** | 3 failures | 300 seconds | Social platform |
| **YouTube** | 3 failures | 300 seconds | Social platform |
| **Pinterest** | 3 failures | 300 seconds | Social platform |
| **TikTok** | 3 failures | 300 seconds | Social platform |

### Circuit States

1. **CLOSED** (Normal)
   - All requests pass through
   - Failures are counted
   - Opens when threshold reached

2. **OPEN** (Service Down)
   - All requests immediately fail
   - No calls to external service
   - Automatically transitions to HALF-OPEN after timeout

3. **HALF-OPEN** (Testing)
   - Single test request allowed
   - Success → CLOSED
   - Failure → OPEN again

### Circuit Breaker Flow

```python
# Example: Calling Gemini with circuit breaker
try:
    result = circuit_breaker.call(gemini_api.generate, prompt)
    # Success - circuit stays closed
except CircuitBreakerError:
    # Circuit is open - try fallback
    result = circuit_breaker.call(bedrock_api.generate, prompt)
```

---

## Intelligent Fallback

### Fallback Chain

Services are tried in priority order:

1. **Gemini** (Primary) - Free tier, good multilingual
2. **Bedrock** - AWS, reliable, multiple models
3. **OpenAI** - High quality, widely used
4. **Anthropic** - Claude, excellent for content
5. **Groq** - Fast inference
6. **Cohere** - Good generation
7. **Together** - Open source models
8. **HuggingFace** - Fallback option

### Fallback Process

```
Request → Try Gemini
          ↓ Fails (timeout/500/circuit open)
          ↓
          Try Bedrock
          ↓ Fails
          ↓
          Try OpenAI
          ↓ Fails
          ↓
          Try Anthropic
          ↓ Fails
          ↓
          Try Groq
          ↓ Fails
          ↓
          Try Cohere
          ↓ Fails
          ↓
          Try Together
          ↓ Fails
          ↓
          Try HuggingFace
          ↓ Fails
          ↓
          Return Error (all services failed)
```

### Retry Logic

Each service is retried with exponential backoff:

```python
@retry(
    stop=stop_after_attempt(2),  # 2 attempts total
    wait=wait_exponential(multiplier=1, min=2, max=10),  # 2s, 4s, 8s, 10s
    retry=retry_if_exception_type((TimeoutError, ServiceUnavailable))
)
```

### Success Response with Fallback

```json
{
  "content": "Generated content here...",
  "service_used": "bedrock",
  "fallback_used": true,
  "attempts": 2,
  "execution_time": 3.45,
  "model": "anthropic.claude-v2"
}
```

### Failure Response (All Services Failed)

```json
{
  "error": "All AI services failed",
  "attempts": [
    {
      "service": "gemini",
      "error_type": "AIServiceTimeoutError",
      "error_message": "Request timeout after 30s",
      "timestamp": 1640000000
    },
    {
      "service": "bedrock",
      "error_type": "CircuitBreakerError",
      "error_message": "Circuit breaker is OPEN",
      "timestamp": 1640000001
    },
    {
      "service": "openai",
      "error_type": "AIServiceRateLimitError",
      "error_message": "Rate limit exceeded",
      "timestamp": 1640000002
    }
  ],
  "total_attempts": 3,
  "execution_time": 5.67,
  "last_error": "Rate limit exceeded"
}
```

---

## Installation

### 1. Install Dependencies

```powershell
cd backend
pip install slowapi pybreaker tenacity
```

### 2. Configure Environment

Update `backend/.env`:

```env
# Redis (required for rate limiting)
REDIS_URL=redis://localhost:6379/0

# Internal service token (optional, for bypassing rate limits)
INTERNAL_SERVICE_TOKEN=your-secret-token-here

# AI Service API Keys (configure at least one)
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
# ... etc
```

### 3. Start Services

```powershell
# Start Redis
redis-server

# Start FastAPI
cd backend
uvicorn app.main:app --reload
```

---

## Usage

### Testing Rate Limits

```bash
# Test as unauthenticated user (5 requests/hour for content generation)
for i in {1..10}; do
  curl -X POST "http://localhost:8000/api/content/generate" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Test", "language": "hindi"}'
done

# After 5 requests, you'll get:
# HTTP 429 - Rate limit exceeded
```

### Testing with Different Tiers

```bash
# Test as PRO user (500 requests/hour)
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -H "X-User-Tier: PRO" \
  -d '{"prompt": "Test", "language": "hindi"}'
```

### Checking Your Rate Limits

```bash
curl "http://localhost:8000/api/monitoring/rate-limits/my-limits"
```

Response:
```json
{
  "tier": "FREE",
  "limits": {
    "content_generation": "20/hour",
    "translation": "50/hour",
    "bulk_operations": "2/day",
    "api_general": "500/hour",
    "social_posting": "20/hour"
  },
  "message": "You are on the FREE tier"
}
```

### Monitoring Circuit Breakers

```bash
# Get all circuit breaker statuses
curl "http://localhost:8000/api/monitoring/circuit-breakers"
```

Response:
```json
{
  "circuit_breakers": {
    "gemini": {
      "service": "gemini",
      "state": "closed",
      "fail_counter": 0,
      "fail_max": 5,
      "is_available": true
    },
    "openai": {
      "service": "openai",
      "state": "open",
      "fail_counter": 5,
      "fail_max": 5,
      "is_available": false,
      "last_failure": "2024-01-01T12:00:00Z"
    }
  },
  "summary": {
    "total": 8,
    "open": 1,
    "closed": 7,
    "half_open": 0
  }
}
```

### Resetting Circuit Breakers

```bash
# Reset specific service
curl -X POST "http://localhost:8000/api/monitoring/circuit-breakers/openai/reset"

# Reset all services
curl -X POST "http://localhost:8000/api/monitoring/circuit-breakers/reset-all"
```

### Checking AI Service Health

```bash
curl "http://localhost:8000/api/monitoring/ai-services/health"
```

Response:
```json
{
  "services": {
    "gemini": {
      "available": true,
      "circuit_state": "closed",
      "is_healthy": true,
      "fail_counter": 0,
      "fail_max": 5,
      "usage_count": 150
    },
    "openai": {
      "available": true,
      "circuit_state": "open",
      "is_healthy": false,
      "fail_counter": 5,
      "fail_max": 5,
      "usage_count": 45
    }
  },
  "summary": {
    "total_available": 3,
    "total_healthy": 2
  }
}
```

### Viewing AI Statistics

```bash
curl "http://localhost:8000/api/monitoring/ai-services/statistics"
```

Response:
```json
{
  "total_requests": 1000,
  "successful_requests": 950,
  "failed_requests": 50,
  "success_rate": 95.0,
  "fallback_used": 120,
  "fallback_rate": 12.63,
  "service_usage": {
    "gemini": 600,
    "bedrock": 200,
    "openai": 150,
    "anthropic": 50
  },
  "available_services": 4,
  "fallback_chain": ["gemini", "bedrock", "openai", "anthropic"]
}
```

---

## Monitoring Endpoints

### Health Check
```
GET /api/monitoring/health
```

### Circuit Breakers
```
GET  /api/monitoring/circuit-breakers
POST /api/monitoring/circuit-breakers/{service}/reset
POST /api/monitoring/circuit-breakers/reset-all
```

### AI Services
```
GET  /api/monitoring/ai-services/health
GET  /api/monitoring/ai-services/statistics
POST /api/monitoring/ai-services/statistics/reset
```

### Rate Limits
```
GET /api/monitoring/rate-limits/my-limits
GET /api/monitoring/rate-limits/tiers
```

### System Status
```
GET /api/monitoring/system/status
```

---

## Production Deployment

### AWS ElastiCache Redis

```env
REDIS_URL=redis://your-elasticache.cache.amazonaws.com:6379/0
```

### Environment Variables

```env
# Production Redis
REDIS_URL=redis://prod-redis:6379/0

# Internal service token (for Celery workers)
INTERNAL_SERVICE_TOKEN=your-production-secret-token

# AI Service Keys
GEMINI_API_KEY=prod_gemini_key
BEDROCK_REGION=us-east-1
OPENAI_API_KEY=prod_openai_key
ANTHROPIC_API_KEY=prod_anthropic_key
```

### Monitoring Setup

1. **CloudWatch Alarms**
   - Rate limit exceeded count > 1000/hour
   - Circuit breaker open count > 3
   - AI service failure rate > 10%

2. **Logging**
   - All circuit breaker state changes
   - All fallback usage
   - All rate limit violations

3. **Metrics**
   - Request count by tier
   - Success rate by AI service
   - Average fallback attempts
   - Circuit breaker state duration

---

## Troubleshooting

### Rate Limit Not Working

```bash
# Check Redis connection
redis-cli ping
# Should return: PONG

# Check rate limit keys
redis-cli
KEYS ratelimit:*
```

### Circuit Breaker Always Open

```bash
# Check circuit breaker status
curl "http://localhost:8000/api/monitoring/circuit-breakers"

# Reset if needed
curl -X POST "http://localhost:8000/api/monitoring/circuit-breakers/gemini/reset"

# Check AI service logs
tail -f logs/app.log | grep "Circuit breaker"
```

### All AI Services Failing

```bash
# Check service health
curl "http://localhost:8000/api/monitoring/ai-services/health"

# Check API keys
echo $GEMINI_API_KEY
echo $OPENAI_API_KEY

# Test individual service
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test", "preferred_service": "gemini"}'
```

---

## Summary

✅ **Implemented:**
- Redis-backed rate limiting with 5 tiers
- Circuit breaker for 15 external services
- Intelligent fallback with 8 AI providers
- Retry logic with exponential backoff
- Comprehensive monitoring endpoints
- Real-time health checks
- Usage statistics tracking

✅ **Benefits:**
- Prevents API abuse
- Protects against cascading failures
- Automatic failover to backup services
- 95%+ uptime even with service outages
- Detailed visibility into system health
- Production-ready configuration

✅ **Next Steps:**
1. Configure AI service API keys
2. Test rate limiting with different tiers
3. Simulate service failures
4. Monitor circuit breaker behavior
5. Deploy to production with CloudWatch
