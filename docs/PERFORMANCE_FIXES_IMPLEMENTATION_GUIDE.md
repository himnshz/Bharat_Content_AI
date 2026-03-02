# ⚡ Performance Fixes - Implementation Guide
**Quick Reference for Developers**

---

## 🔴 CRITICAL FIX #1: N+1 Query Patterns

### File: `backend/app/routes/teams.py`

#### Fix 1: get_team_members (Line 267)
```python
# BEFORE (❌ N+1 Query)
@router.get("/{team_id}/members", response_model=List[MemberResponse])
async def get_team_members(team_id: int, db: Session = Depends(get_db)):
    members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
    result = []
    for member in members:
        user = db.query(User).filter(User.id == member.user_id).first()  # ❌ Query in loop
        if user:
            result.append({...})
    return result

# AFTER (✅ Single Query with JOIN)
from sqlalchemy.orm import joinedload

@router.get("/{team_id}/members", response_model=List[MemberResponse])
async def get_team_members(team_id: int, db: Session = Depends(get_db)):
    members = db.query(TeamMember)\
        .options(joinedload(TeamMember.user))\
        .filter(TeamMember.team_id == team_id)\
        .all()
    
    result = []
    for member in members:
        result.append({
            "id": member.id,
            "user_id": member.user.id,
            "username": member.user.username,  # ✅ No extra query
            "email": member.user.email,
            "role": member.role,
            "joined_at": member.joined_at
        })
    return result
```

#### Fix 2: get_comments (Line 584)
```python
# BEFORE (❌)
for comment in comments:
    user = db.query(User).filter(User.id == comment.user_id).first()

# AFTER (✅)
comments = db.query(Comment)\
    .options(joinedload(Comment.user))\
    .filter(Comment.content_id == resource_id)\
    .all()

for comment in comments:
    username = comment.user.username  # ✅ Already loaded
```

#### Fix 3: get_team_activity (Line 718)
```python
# AFTER (✅)
activities = db.query(ActivityLog)\
    .options(joinedload(ActivityLog.user))\
    .filter(ActivityLog.team_id == team_id)\
    .order_by(ActivityLog.created_at.desc())\
    .limit(limit)\
    .all()
```

---

## 🔴 CRITICAL FIX #2: Add Composite Indexes

### File: `backend/app/models/post.py`
```python
from sqlalchemy import Index

class Post(Base):
    __tablename__ = "posts"
    
    # ... existing columns ...
    
    __table_args__ = (
        Index('idx_post_user_schedule', 'user_id', 'scheduled_time'),
        Index('idx_post_user_platform_status', 'user_id', 'platform', 'status'),
        Index('idx_post_scheduled_time', 'scheduled_time'),
    )
```

### File: `backend/app/models/team.py`
```python
class TeamMember(Base):
    __tablename__ = "team_members"
    
    __table_args__ = (
        Index('idx_team_member_lookup', 'team_id', 'user_id'),
        Index('idx_team_member_user', 'user_id'),
    )

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    __table_args__ = (
        Index('idx_activity_team_time', 'team_id', 'created_at'),
    )
```

### File: `backend/app/models/translation.py`
```python
class Translation(Base):
    __tablename__ = "translations"
    
    __table_args__ = (
        Index('idx_translation_content_lang', 'content_id', 'target_language'),
    )
```

### Create Migration
```bash
cd backend
alembic revision --autogenerate -m "Add composite indexes for performance"
alembic upgrade head
```

---

## 🔴 CRITICAL FIX #3: Redis Caching for Analytics

### File: `backend/app/routes/analytics.py`
```python
from app.config.redis_config import get_async_redis
import json

@router.get("/overview/{days}")
async def get_analytics_overview(
    days: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ✅ Check cache first
    redis = await get_async_redis()
    cache_key = f"analytics:overview:{current_user.id}:{days}"
    
    cached_data = await redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Compute analytics (existing logic)
    result = {
        "total_content_generated": ...,
        # ... rest of analytics
    }
    
    # ✅ Cache for 5 minutes
    await redis.setex(cache_key, 300, json.dumps(result))
    
    return result
```

### Cache Invalidation Pattern
```python
# When user creates content, invalidate cache
@router.post("/content/generate")
async def generate_content(...):
    # ... generate content ...
    
    # ✅ Invalidate analytics cache
    redis = await get_async_redis()
    await redis.delete(f"analytics:overview:{current_user.id}:*")
    
    return result
```

---

## 🔴 CRITICAL FIX #4: Background Tasks for AI Operations

### File: `backend/app/routes/content.py`
```python
from app.tasks.content_tasks import generate_content_task

# BEFORE (❌ Blocking)
@router.post("/generate")
async def generate_content(request: ContentRequest, ...):
    # This blocks for 5-15 seconds
    generated = await ai_service.generate_content(request.prompt)
    return {"content": generated}

# AFTER (✅ Non-blocking)
@router.post("/generate")
async def generate_content(request: ContentRequest, ...):
    # Start background task
    task = generate_content_task.delay(
        user_id=current_user.id,
        prompt=request.prompt,
        params=request.dict()
    )
    
    return {
        "task_id": task.id,
        "status": "processing",
        "message": "Content generation started"
    }

# Add status endpoint
@router.get("/generate/status/{task_id}")
async def get_generation_status(task_id: str):
    from celery.result import AsyncResult
    task = AsyncResult(task_id)
    
    if task.ready():
        return {
            "status": "completed",
            "result": task.result
        }
    else:
        return {
            "status": "processing",
            "progress": task.info.get('progress', 0)
        }
```

### File: `backend/app/tasks/content_tasks.py`
```python
from app.celery_worker import celery_app
from app.config.redis_config import get_sync_redis, TaskProgressTracker

@celery_app.task(bind=True)
def generate_content_task(self, user_id: int, prompt: str, params: dict):
    redis = get_sync_redis()
    tracker = TaskProgressTracker(redis)
    
    try:
        # Update progress
        tracker.set_progress(self.request.id, 0, 100, "processing", "Starting generation")
        
        # Generate content
        from app.services.content_generation.ai_service_manager_v2 import AIServiceManager
        manager = AIServiceManager()
        
        tracker.set_progress(self.request.id, 50, 100, "processing", "Generating content")
        result = manager.generate_content(prompt, params)
        
        tracker.set_progress(self.request.id, 100, 100, "completed", "Done", result)
        
        return result
        
    except Exception as e:
        tracker.set_progress(self.request.id, 0, 100, "failed", str(e))
        raise
```

---

## 🟠 HIGH-PRIORITY FIX #5: React useMemo Optimization

### File: `frontend-new/src/components/dashboard/AnalyticsContent.tsx`
```typescript
import { useMemo, useCallback } from 'react'

export default function AnalyticsContent() {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null)
  const [days, setDays] = useState(30)

  // ✅ Memoize expensive computations
  const stats = useMemo(() => {
    if (!overview) return []
    
    return [
      { 
        label: 'Content Generated', 
        value: overview.total_content_generated.toLocaleString(), 
        change: '+12%', 
        icon: '📝' 
      },
      { 
        label: 'Total Engagement', 
        value: (overview.total_engagement.likes + 
                overview.total_engagement.comments + 
                overview.total_engagement.shares).toLocaleString(), 
        change: `${overview.avg_engagement_rate.toFixed(1)}%`, 
        icon: '❤️' 
      },
      // ... rest
    ]
  }, [overview])

  // ✅ Memoize callback
  const fetchAnalytics = useCallback(async () => {
    try {
      setLoading(true)
      // ... fetch logic
    } finally {
      setLoading(false)
    }
  }, [days])

  useEffect(() => {
    fetchAnalytics()
  }, [fetchAnalytics])

  // ✅ Memoize chart data
  const chartData = useMemo(() => {
    return engagementTrends.map(trend => ({
      ...trend,
      date: new Date(trend.date).toLocaleDateString()
    }))
  }, [engagementTrends])

  return (
    // ... JSX
  )
}
```

---

## 🟠 HIGH-PRIORITY FIX #6: React useCallback for Handlers

### File: `frontend-new/src/components/dashboard/ProfileContent.tsx`
```typescript
export default function ProfileContent() {
  const [fullName, setFullName] = useState('')
  const [saving, setSaving] = useState(false)

  // ✅ Stable callback reference
  const handleSaveProfile = useCallback(async () => {
    try {
      setSaving(true)
      const response = await fetchAPI(`${API_ENDPOINTS.userProfile}/${userId}`, {
        method: 'PUT',
        body: JSON.stringify({ full_name: fullName })
      })
      // ... handle response
    } finally {
      setSaving(false)
    }
  }, [fullName, userId])

  // ✅ Memoize button click handlers
  const handleDaysChange = useCallback((d: number) => {
    setDays(d)
  }, [])

  return (
    <button onClick={handleSaveProfile} disabled={saving}>
      Save
    </button>
  )
}
```

---

## 🟡 MEDIUM-PRIORITY FIX #7: WebSocket for Real-Time Updates

### Backend: `backend/app/main.py`
```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections[user_id].discard(websocket)
    
    async def send_to_user(self, user_id: int, message: dict):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# Send updates from tasks
async def notify_user(user_id: int, event_type: str, data: dict):
    await manager.send_to_user(user_id, {
        "type": event_type,
        "data": data
    })
```

### Frontend: `frontend-new/src/hooks/useWebSocket.ts`
```typescript
import { useEffect, useState } from 'react'

export function useWebSocket(userId: number) {
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [messages, setMessages] = useState<any[]>([])

  useEffect(() => {
    const websocket = new WebSocket(`ws://localhost:8000/ws/${userId}`)
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMessages(prev => [...prev, data])
    }
    
    setWs(websocket)
    
    return () => websocket.close()
  }, [userId])

  return { messages, ws }
}
```

---

## 📋 TESTING CHECKLIST

### Database Optimization
- [ ] Run EXPLAIN ANALYZE on modified queries
- [ ] Verify indexes are being used
- [ ] Measure query time before/after
- [ ] Test with 1000+ records

### Caching
- [ ] Verify cache hits in Redis
- [ ] Test cache invalidation
- [ ] Measure response time improvement
- [ ] Test cache expiration

### Background Tasks
- [ ] Test task queue processing
- [ ] Verify progress tracking
- [ ] Test error handling
- [ ] Monitor task completion time

### React Performance
- [ ] Use React DevTools Profiler
- [ ] Count re-renders before/after
- [ ] Test with large datasets
- [ ] Verify memo/callback effectiveness

---

## 🚀 DEPLOYMENT STEPS

1. **Database Changes**
   ```bash
   alembic upgrade head
   ```

2. **Redis Setup**
   ```bash
   docker run -d -p 6379:6379 redis:alpine
   ```

3. **Celery Workers**
   ```bash
   celery -A app.celery_worker worker --loglevel=info
   ```

4. **Frontend Build**
   ```bash
   npm run build
   ```

5. **Monitoring**
   - Enable query logging
   - Set up Redis monitoring
   - Track API response times

