# Bulk Operations Module - Complete Guide

## Overview

The Bulk Operations module enables processing of large batches of content generation, translation, and scheduling tasks without blocking the FastAPI event loop. It uses Celery for distributed task processing and Redis for caching and real-time progress tracking.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Frontend)                         │
│  • Upload CSV                                                │
│  • Monitor Progress (SSE)                                    │
│  • Download Results                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                FastAPI Application                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Bulk Operations Routes                        │  │
│  │  • POST /api/bulk/upload                             │  │
│  │  • GET  /api/bulk/progress/{task_id}                 │  │
│  │  • GET  /api/bulk/progress-stream/{task_id} (SSE)    │  │
│  │  • GET  /api/bulk/result/{task_id}                   │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Redis (Message Broker)                    │
│  • Task Queue                                                │
│  • Progress Tracking                                         │
│  • Pub/Sub for SSE                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Celery Workers                              │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Worker 1: Bulk Queue                                │  │
│  │  • Process CSV data                                   │  │
│  │  • Validate rows                                      │  │
│  │  • Batch processing                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Worker 2: Content Queue                             │  │
│  │  • AI content generation                             │  │
│  │  • Save to database                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Worker 3: Translation Queue                         │  │
│  │  • Batch translations                                 │  │
│  │  • Save to database                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

### ✅ Implemented Features

1. **CSV Upload & Validation**
   - Upload CSV files up to 10,000 rows
   - Pre-validation before processing
   - Detailed error reporting

2. **Async Task Processing**
   - Non-blocking task execution
   - Celery distributed task queue
   - Multiple worker queues (bulk, content, translation)

3. **Real-time Progress Tracking**
   - Server-Sent Events (SSE) for live updates
   - Polling endpoint for progress checks
   - Redis pub/sub for instant notifications

4. **Batch Processing**
   - Configurable batch sizes (1-100 items)
   - Optimized for AI API rate limits
   - Automatic retry on failures

5. **Three Operation Types**
   - Content Generation (bulk AI content)
   - Translation (bulk language translation)
   - Scheduling (bulk social media posts)

6. **CSV Templates**
   - Download pre-formatted templates
   - Example data included
   - Validation rules documented

---

## Installation

### 1. Install Redis

**Windows:**
```powershell
# Download from: https://github.com/microsoftarchive/redis/releases
# Or use WSL:
wsl --install
wsl
sudo apt-get update
sudo apt-get install redis-server
redis-server
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

### 2. Install Python Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `celery==5.3.4` - Distributed task queue
- `redis==5.0.1` - Redis client
- `flower==2.0.1` - Celery monitoring
- `pandas==2.1.4` - CSV processing
- `aiofiles==23.2.1` - Async file operations

### 3. Configure Environment

Update `backend/.env`:

```env
# Redis Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## Usage

### Starting the Services

You need to run **3 separate processes**:

#### 1. Start Redis
```powershell
# Windows (WSL)
wsl
redis-server

# macOS/Linux
redis-server
```

#### 2. Start FastAPI Server
```powershell
cd backend
uvicorn app.main:app --reload
```

#### 3. Start Celery Worker
```powershell
cd backend

# Start worker with all queues
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo

# Or start multiple workers for different queues
celery -A app.config.celery_config.celery_app worker -Q bulk --loglevel=info --pool=solo
celery -A app.config.celery_config.celery_app worker -Q content --loglevel=info --pool=solo
celery -A app.config.celery_config.celery_app worker -Q translation --loglevel=info --pool=solo
```

#### 4. Start Flower (Optional - Monitoring)
```powershell
cd backend
celery -A app.config.celery_config.celery_app flower
# Access at: http://localhost:5555
```

---

## API Endpoints

### 1. Validate CSV
```http
POST /api/bulk/validate-csv
Content-Type: multipart/form-data

file: <csv_file>
operation_type: content_generation | translation | scheduling
```

**Response:**
```json
{
  "valid": true,
  "total_rows": 100,
  "valid_rows": 98,
  "invalid_rows": 2,
  "errors": [
    {
      "row_number": 5,
      "field": "prompt",
      "error": "Field is required",
      "value": null
    }
  ],
  "sample_data": [...]
}
```

### 2. Upload CSV & Start Processing
```http
POST /api/bulk/upload
Content-Type: multipart/form-data

file: <csv_file>
operation_type: content_generation
user_id: 1
batch_size: 10
priority: 5
```

**Response:**
```json
{
  "task_id": "abc123-def456-ghi789",
  "operation_type": "content_generation",
  "total_rows": 100,
  "status": "queued",
  "message": "Bulk operation queued successfully",
  "progress_url": "/api/bulk/progress/abc123-def456-ghi789",
  "estimated_time_seconds": 200
}
```

### 3. Get Progress (Polling)
```http
GET /api/bulk/progress/{task_id}
```

**Response:**
```json
{
  "task_id": "abc123-def456-ghi789",
  "current": 45,
  "total": 100,
  "percentage": 45.0,
  "status": "processing",
  "message": "Processed 45/100 items"
}
```

### 4. Stream Progress (SSE)
```http
GET /api/bulk/progress-stream/{task_id}
Accept: text/event-stream
```

**SSE Stream:**
```
data: {"task_id":"abc123","current":10,"total":100,"percentage":10.0,"status":"processing"}

data: {"task_id":"abc123","current":20,"total":100,"percentage":20.0,"status":"processing"}

data: {"task_id":"abc123","current":100,"total":100,"percentage":100.0,"status":"completed"}
```

### 5. Get Final Result
```http
GET /api/bulk/result/{task_id}
```

**Response:**
```json
{
  "task_id": "abc123-def456-ghi789",
  "operation_type": "content_generation",
  "total_rows": 100,
  "successful": 98,
  "failed": 2,
  "errors": [
    {
      "row_number": 5,
      "error": "AI service timeout",
      "prompt": "..."
    }
  ],
  "results": [
    {
      "success": true,
      "content_id": 123,
      "prompt": "...",
      "language": "hindi"
    }
  ],
  "execution_time_seconds": 185.5,
  "completed_at": "2024-01-01T12:00:00Z"
}
```

### 6. Cancel Task
```http
DELETE /api/bulk/cancel/{task_id}
```

### 7. Download CSV Templates
```http
GET /api/bulk/templates/content-generation
GET /api/bulk/templates/translation
GET /api/bulk/templates/scheduling
```

---

## CSV Formats

### Content Generation CSV

```csv
prompt,language,content_type,tone,platform,keywords
"Write a post about AI",hindi,social_post,casual,instagram,"AI,technology"
"Create blog intro",english,blog,professional,linkedin,"business,tech"
```

**Required Fields:**
- `prompt` (10-5000 chars)
- `language` (hindi, english, tamil, etc.)
- `content_type` (social_post, blog, article, etc.)
- `tone` (casual, formal, professional, etc.)

**Optional Fields:**
- `platform` (instagram, facebook, etc.)
- `keywords` (comma-separated)

### Translation CSV

```csv
text,source_language,target_language,preserve_formatting
"Hello World",english,hindi,true
"Welcome",english,tamil,true
```

**Required Fields:**
- `text` (1-10000 chars)
- `source_language`
- `target_language`

**Optional Fields:**
- `preserve_formatting` (true/false)

### Scheduling CSV

```csv
content_id,platform,scheduled_time,caption,hashtags
123,facebook,2024-12-01T10:00:00Z,"Check this out!","#content,#social"
124,instagram,2024-12-01T14:00:00Z,"New post!","#instagram"
```

**Required Fields:**
- `content_id` (integer)
- `platform` (facebook, instagram, etc.)
- `scheduled_time` (ISO format)

**Optional Fields:**
- `caption` (max 2000 chars)
- `hashtags` (comma-separated)

---

## Frontend Integration

### React/Next.js Example

```typescript
// Upload CSV and start processing
async function uploadBulkCSV(file: File, operationType: string) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('operation_type', operationType);
  formData.append('batch_size', '10');
  
  const response = await fetch('/api/bulk/upload', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  return data.task_id;
}

// Monitor progress with SSE
function monitorProgress(taskId: string, onProgress: (data: any) => void) {
  const eventSource = new EventSource(`/api/bulk/progress-stream/${taskId}`);
  
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onProgress(data);
    
    if (data.status === 'completed' || data.status === 'failed') {
      eventSource.close();
    }
  };
  
  eventSource.onerror = () => {
    eventSource.close();
  };
  
  return eventSource;
}

// Usage
const taskId = await uploadBulkCSV(file, 'content_generation');

monitorProgress(taskId, (progress) => {
  console.log(`Progress: ${progress.percentage}%`);
  setProgress(progress.percentage);
  setStatus(progress.message);
});
```

### Progress Bar Component

```typescript
import { useState, useEffect } from 'react';

export function BulkOperationProgress({ taskId }: { taskId: string }) {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');
  const [message, setMessage] = useState('');
  
  useEffect(() => {
    const eventSource = new EventSource(`/api/bulk/progress-stream/${taskId}`);
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setProgress(data.percentage || 0);
      setStatus(data.status);
      setMessage(data.message);
      
      if (data.status === 'completed' || data.status === 'failed') {
        eventSource.close();
      }
    };
    
    return () => eventSource.close();
  }, [taskId]);
  
  return (
    <div className="bulk-progress">
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${progress}%` }}
        />
      </div>
      <p>{message} ({progress.toFixed(1)}%)</p>
      <p>Status: {status}</p>
    </div>
  );
}
```

---

## Performance Optimization

### Batch Size Tuning

```python
# Small batches (1-5): Better for rate-limited APIs
batch_size = 5

# Medium batches (10-20): Balanced performance
batch_size = 10

# Large batches (50-100): Maximum throughput
batch_size = 50
```

### Worker Scaling

```powershell
# Single worker (development)
celery -A app.config.celery_config.celery_app worker --loglevel=info

# Multiple workers (production)
celery -A app.config.celery_config.celery_app worker --concurrency=4 --loglevel=info

# Autoscaling workers
celery -A app.config.celery_config.celery_app worker --autoscale=10,3 --loglevel=info
```

### Queue Priorities

```python
# High priority (7-10): Real-time operations
priority = 10

# Medium priority (4-6): Bulk operations
priority = 5

# Low priority (1-3): Background tasks
priority = 1
```

---

## Monitoring

### Flower Dashboard

Access Celery monitoring at: http://localhost:5555

Features:
- Active tasks
- Worker status
- Task history
- Success/failure rates
- Execution times

### Redis Monitoring

```bash
# Connect to Redis CLI
redis-cli

# Monitor commands
MONITOR

# Check queue lengths
LLEN celery

# Check active tasks
KEYS task_progress:*
```

### Logs

```powershell
# Celery worker logs
celery -A app.config.celery_config.celery_app worker --loglevel=debug

# FastAPI logs
uvicorn app.main:app --log-level debug
```

---

## Troubleshooting

### Redis Connection Error
```
Error: Redis connection refused
```

**Solution:**
```powershell
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Start Redis if not running
redis-server
```

### Celery Worker Not Starting
```
Error: No module named 'app'
```

**Solution:**
```powershell
# Ensure you're in the backend directory
cd backend

# Use correct module path
celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo
```

### Task Stuck in Queue
```
Task status: PENDING (forever)
```

**Solution:**
```powershell
# Check if worker is running
celery -A app.config.celery_config.celery_app inspect active

# Restart worker
# Ctrl+C to stop, then restart
```

### SSE Connection Timeout
```
EventSource connection closed
```

**Solution:**
```typescript
// Add reconnection logic
const eventSource = new EventSource(url);

eventSource.onerror = () => {
  setTimeout(() => {
    // Reconnect after 5 seconds
    monitorProgress(taskId, onProgress);
  }, 5000);
};
```

---

## Production Deployment

### AWS ElastiCache Redis

```env
# Update .env for production
REDIS_URL=redis://your-elasticache-endpoint.cache.amazonaws.com:6379/0
CELERY_BROKER_URL=redis://your-elasticache-endpoint.cache.amazonaws.com:6379/0
CELERY_RESULT_BACKEND=redis://your-elasticache-endpoint.cache.amazonaws.com:6379/0
```

### Docker Deployment

```dockerfile
# Dockerfile for Celery Worker
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["celery", "-A", "app.config.celery_config.celery_app", "worker", "--loglevel=info"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  fastapi:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      - redis
  
  celery_worker:
    build: .
    command: celery -A app.config.celery_config.celery_app worker --loglevel=info
    depends_on:
      - redis
  
  flower:
    build: .
    command: celery -A app.config.celery_config.celery_app flower
    ports:
      - "5555:5555"
    depends_on:
      - redis
```

---

## Summary

✅ **Implemented:**
- Async task queue with Celery
- Redis for caching and pub/sub
- CSV upload and validation
- Batch processing (configurable)
- Real-time progress tracking (SSE)
- Three operation types (content, translation, scheduling)
- Error handling and retry logic
- Monitoring with Flower
- Production-ready configuration

✅ **Benefits:**
- Non-blocking operations
- Scalable to thousands of concurrent tasks
- Real-time progress updates
- Fault-tolerant with retries
- Easy to monitor and debug

✅ **Next Steps:**
1. Install Redis
2. Start Celery worker
3. Test with sample CSV
4. Integrate with frontend
5. Deploy to production
