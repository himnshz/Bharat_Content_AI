# Complete Security Implementation - Action Plan

## Current Status

✅ **COMPLETED (4/11 routes - 36%)**
- backend/app/routes/users.py
- backend/app/routes/content.py
- backend/app/routes/translation.py
- backend/app/routes/social.py

⚠️ **REMAINING (7/11 routes - 64%)**
- backend/app/routes/analytics.py
- backend/app/routes/voice.py
- backend/app/routes/campaigns.py
- backend/app/routes/models.py
- backend/app/routes/teams.py
- backend/app/routes/templates.py
- backend/app/routes/bulk.py

## Quick Reference: Security Pattern

### Step 1: Add Import
```python
from app.auth.dependencies import get_current_user, enforce_quota
```

### Step 2: Remove user_id from Schemas
```python
# Remove user_id: int fields from all Pydantic models
```

### Step 3: Add Authentication to Endpoints
```python
@router.post("/endpoint")
async def endpoint(
    request: Request,
    current_user: User = Depends(get_current_user),  # Add this
    db: Session = Depends(get_db)
):
    # Use current_user.id instead of request.user_id
```

### Step 4: Add IDOR Protection
```python
# Before
resource = db.query(Resource).filter(Resource.id == resource_id).first()

# After
resource = db.query(Resource).filter(
    Resource.id == resource_id,
    Resource.user_id == current_user.id  # Prevent IDOR
).first()
```

## Detailed Implementation Steps

### Route 1: analytics.py (PRIORITY: HIGH)

**Endpoints to update (7):**
1. `get_analytics_overview(user_id, days)` 
2. `get_platform_performance(user_id, days)`
3. `get_content_type_performance(user_id, days)`
4. `get_engagement_trends(user_id, days)`
5. `get_top_performing_content(user_id, limit, days)`
6. `get_language_distribution(user_id, days)`
7. `sync_post_metrics(post_id)`

**Changes:**
```python
# 1. Add import at top
from app.auth.dependencies import get_current_user

# 2. Update each endpoint signature
# BEFORE:
async def get_analytics_overview(user_id: int, days: int = 30, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

# AFTER:
async def get_analytics_overview(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Use current_user directly, no need to query

# 3. Replace all user_id with current_user.id in queries
# BEFORE:
content_count = db.query(func.count(Content.id)).filter(
    Content.user_id == user_id,
    ...
).scalar()

# AFTER:
content_count = db.query(func.count(Content.id)).filter(
    Content.user_id == current_user.id,
    ...
).scalar()

# 4. For sync_post_metrics, add IDOR check
# BEFORE:
post = db.query(Post).filter(Post.id == post_id).first()

# AFTER:
post = db.query(Post).filter(
    Post.id == post_id,
    Post.user_id == current_user.id  # IDOR protection
).first()
```

**Estimated time:** 20 minutes

---

### Route 2: voice.py (PRIORITY: HIGH)

**Endpoints to update (6):**
1. `upload_voice_input(user_id, audio_file)`
2. `transcribe_audio(request)`
3. `list_voice_inputs(user_id, skip, limit, status)`
4. `get_voice_input(voice_input_id)`
5. `convert_voice_to_content(voice_input_id)`
6. `delete_voice_input(voice_input_id)`

**Changes:**
```python
# 1. Add import
from app.auth.dependencies import get_current_user, enforce_quota

# 2. Update upload_voice_input
# BEFORE:
async def upload_voice_input(
    user_id: int,
    audio_file: UploadFile = File(...),
    ...
):
    user = db.query(User).filter(User.id == user_id).first()

# AFTER:
async def upload_voice_input(
    audio_file: UploadFile = File(...),
    language: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Use current_user.id directly
    voice_input = VoiceInput(
        user_id=current_user.id,
        ...
    )

# 3. Add IDOR protection to get/delete endpoints
# BEFORE:
voice_input = db.query(VoiceInput).filter(VoiceInput.id == voice_input_id).first()

# AFTER:
voice_input = db.query(VoiceInput).filter(
    VoiceInput.id == voice_input_id,
    VoiceInput.user_id == current_user.id  # IDOR protection
).first()

# 4. Update list_voice_inputs
# BEFORE:
async def list_voice_inputs(user_id: int, ...):
    query = db.query(VoiceInput).filter(VoiceInput.user_id == user_id)

# AFTER:
async def list_voice_inputs(
    skip: int = 0,
    limit: int = 20,
    status: Optional[VoiceInputStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(VoiceInput).filter(VoiceInput.user_id == current_user.id)
```

**Estimated time:** 20 minutes

---

### Route 3: campaigns.py (PRIORITY: HIGH)

**Endpoints to update (10):**
1. `create_campaign(campaign_data)`
2. `get_campaigns(user_id, status, campaign_type, skip, limit)`
3. `get_campaign(campaign_id)`
4. `update_campaign(campaign_id, campaign_data)`
5. `update_campaign_metrics(campaign_id, metrics)`
6. `update_campaign_status(campaign_id, new_status)`
7. `approve_campaign(campaign_id, approver_id)`
8. `delete_campaign(campaign_id)`
9. `get_campaign_analytics(campaign_id)`

**Changes:**
```python
# 1. Add import
from app.auth.dependencies import get_current_user, require_role

# 2. Remove user_id from CampaignCreate schema
class CampaignCreate(CampaignBase):
    # Remove: user_id: int
    pass

# 3. Update create_campaign
# BEFORE:
async def create_campaign(campaign_data: CampaignCreate, db: Session = Depends(get_db)):
    campaign = Campaign(**campaign_data.model_dump())

# AFTER:
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    campaign_dict = campaign_data.model_dump()
    campaign_dict['user_id'] = current_user.id
    campaign = Campaign(**campaign_dict)

# 4. Update get_campaigns
# BEFORE:
async def get_campaigns(user_id: Optional[int] = Query(None), ...):
    if user_id:
        query = query.filter(Campaign.user_id == user_id)

# AFTER:
async def get_campaigns(
    status: Optional[CampaignStatus] = Query(None),
    campaign_type: Optional[CampaignType] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Campaign).filter(Campaign.user_id == current_user.id)

# 5. Add IDOR protection to all get/update/delete endpoints
# BEFORE:
campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

# AFTER:
campaign = db.query(Campaign).filter(
    Campaign.id == campaign_id,
    Campaign.user_id == current_user.id  # IDOR protection
).first()

# 6. Update approve_campaign
# BEFORE:
async def approve_campaign(campaign_id: int, approver_id: int, db: Session = Depends(get_db)):

# AFTER:
async def approve_campaign(
    campaign_id: int,
    current_user: User = Depends(require_role([UserRole.BUSINESS, UserRole.STARTUP])),
    db: Session = Depends(get_db)
):
    campaign.approved_by = current_user.id
```

**Estimated time:** 25 minutes

---

### Route 4: models.py (PRIORITY: MEDIUM)

**Endpoints to update (7):**
1. `get_available_models(user_id)`
2. `get_user_models(user_id)`
3. `configure_model(user_id, model_id, config)`
4. `get_model_usage_stats(user_id)`
5. `get_primary_model(user_id)`
6. `increment_model_usage(user_id, model_id)`

**Changes:**
```python
# 1. Add import
from app.auth.dependencies import get_current_user

# 2. Update all endpoints - remove user_id parameter
# BEFORE:
async def get_available_models(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    user_configs = db.query(AIModelConfig).filter(AIModelConfig.user_id == user_id).all()

# AFTER:
async def get_available_models(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_configs = db.query(AIModelConfig).filter(
        AIModelConfig.user_id == current_user.id
    ).all()

# 3. Apply same pattern to all other endpoints
```

**Estimated time:** 15 minutes

---

### Route 5: teams.py (PRIORITY: MEDIUM)

**Endpoints to update (15+):**
- All team management endpoints
- All member management endpoints
- All invite endpoints
- All comment endpoints
- All approval endpoints

**Changes:**
```python
# 1. Add import
from app.auth.dependencies import get_current_user

# 2. Remove user_id from all endpoint parameters
# 3. Add current_user: User = Depends(get_current_user) to all endpoints
# 4. Replace user_id with current_user.id in all queries
# 5. Keep RBAC checks (owner/admin/member) but use current_user

# Example:
# BEFORE:
async def create_team(team: TeamCreate, user_id: int, db: Session = Depends(get_db)):
    new_team = Team(name=team.name, owner_id=user_id)

# AFTER:
async def create_team(
    team: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_team = Team(name=team.name, owner_id=current_user.id)
```

**Estimated time:** 30 minutes

---

### Route 6: templates.py (PRIORITY: MEDIUM)

**Endpoints to update (11):**
1. `create_template(template, user_id)`
2. `get_templates(user_id, category, platform, language)`
3. `get_user_templates(user_id)`
4. `get_favorite_templates(user_id)`
5. `get_templates_by_category(category, user_id)`
6. `get_template(template_id)`
7. `update_template(template_id, template_update, user_id)`
8. `delete_template(template_id, user_id)`
9. `use_template(template_id)`
10. `toggle_favorite(template_id, user_id)`
11. `get_popular_templates(limit)`

**Changes:**
```python
# 1. Add import
from app.auth.dependencies import get_current_user

# 2. Remove user_id parameters, add current_user
# 3. Add IDOR protection to get/update/delete

# Example:
# BEFORE:
async def create_template(template: TemplateCreate, user_id: int, db: Session = Depends(get_db)):
    new_template = Template(user_id=user_id, ...)

# AFTER:
async def create_template(
    template: TemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_template = Template(user_id=current_user.id, ...)
```

**Estimated time:** 20 minutes

---

### Route 7: bulk.py (PRIORITY: LOW)

**Endpoints to update (9):**
1. `validate_csv(file, operation_type)`
2. `upload_bulk_csv(file, operation_type, user_id=1, ...)`  # ❌ Hardcoded!
3. `get_task_progress(task_id)`
4. `stream_task_progress(task_id)`
5. `get_task_result(task_id)`
6. `cancel_task(task_id)`
7-9. Template download endpoints

**Changes:**
```python
# 1. Add import
from app.auth.dependencies import get_current_user

# 2. Fix upload_bulk_csv
# BEFORE:
async def upload_bulk_csv(
    file: UploadFile = File(...),
    operation_type: BulkOperationType = BulkOperationType.CONTENT_GENERATION,
    user_id: int = 1,  # ❌ CRITICAL SECURITY ISSUE!
    ...
):

# AFTER:
async def upload_bulk_csv(
    file: UploadFile = File(...),
    operation_type: BulkOperationType = BulkOperationType.CONTENT_GENERATION,
    batch_size: int = 10,
    priority: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Use current_user.id
    task = process_bulk_content.apply_async(
        args=[csv_data, operation_type.value, current_user.id, batch_size],
        priority=priority
    )

# 3. Add task ownership verification to progress/result/cancel endpoints
# Store task_id -> user_id mapping in Redis
# Verify current_user.id matches task owner before allowing access
```

**Estimated time:** 25 minutes

---

## Additional Security Features

### 1. Add Rate Limiting (15 minutes)

**File:** `backend/app/routes/users.py`

```python
# Install: pip install slowapi

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(...):
    ...

@router.post("/register")
@limiter.limit("3/minute")
async def register(...):
    ...
```

### 2. Add CSRF Protection (10 minutes)

**File:** `backend/app/main.py`

```python
# Install: pip install starlette-csrf

from starlette.middleware.sessions import SessionMiddleware
from starlette_csrf import CSRFMiddleware

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CSRFMiddleware,
    secret=settings.SECRET_KEY,
    cookie_name="csrftoken",
    header_name="X-CSRFToken"
)
```

### 3. Add File Upload Validation (15 minutes)

**File:** `backend/app/routes/voice.py`

```python
# Install: pip install python-magic python-magic-bin

import magic

async def upload_voice_input(...):
    # Read file content
    file_content = await audio_file.read()
    
    # Validate actual file type (not just extension)
    mime = magic.from_buffer(file_content, mime=True)
    allowed_mimes = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/x-m4a']
    
    if mime not in allowed_mimes:
        raise HTTPException(400, f"Invalid file type: {mime}")
    
    # Continue with upload...
```

---

## Frontend Updates

### 1. Update Login Page (10 minutes)

**File:** `frontend-new/src/app/login/page.tsx`

```typescript
// BEFORE
const response = await fetch(`${API_URL}/users/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
const data = await response.json();
localStorage.setItem('token', data.access_token);  // ❌ Remove

// AFTER
const response = await fetch(`${API_URL}/users/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',  // ✅ Add for cookies
  body: JSON.stringify({ email, password })
});
// Token is now in HttpOnly cookie, no localStorage needed
```

### 2. Update All API Calls (30 minutes)

**Pattern to apply everywhere:**

```typescript
// BEFORE
const response = await fetch(`${API_URL}/content/generate`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`  // ❌ Remove
  },
  body: JSON.stringify({
    user_id: userId,  // ❌ Remove
    prompt: prompt
  })
});

// AFTER
const response = await fetch(`${API_URL}/content/generate`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include',  // ✅ Add for cookies
  body: JSON.stringify({
    prompt: prompt  // ✅ No user_id needed
  })
});
```

### 3. Update Header Component (10 minutes)

**File:** `frontend-new/src/components/layout/Header.tsx`

```typescript
// Update logout function
const handleLogout = async () => {
  await fetch(`${API_URL}/users/logout`, {
    method: 'POST',
    credentials: 'include'
  });
  router.push('/login');
};
```

---

## Testing Checklist

After completing all updates:

- [ ] Test login with valid credentials
- [ ] Test login with invalid credentials
- [ ] Test registration with weak password (should fail)
- [ ] Test accessing protected endpoint without auth (should return 401)
- [ ] Test User A accessing User B's content (should return 404)
- [ ] Test quota enforcement (generate content until quota exceeded)
- [ ] Test rate limiting on login (try 6 logins in 1 minute)
- [ ] Test file upload with invalid file type
- [ ] Test CSRF protection
- [ ] Test all CRUD operations for each resource type

---

## Installation Commands

```bash
# Backend dependencies
cd backend
pip install slowapi starlette-csrf python-magic python-magic-bin

# Update requirements.txt
pip freeze > requirements.txt

# Frontend (if needed)
cd ../frontend-new
npm install
```

---

## Time Estimate Summary

| Task | Time |
|------|------|
| analytics.py | 20 min |
| voice.py | 20 min |
| campaigns.py | 25 min |
| models.py | 15 min |
| teams.py | 30 min |
| templates.py | 20 min |
| bulk.py | 25 min |
| Rate limiting | 15 min |
| CSRF protection | 10 min |
| File validation | 15 min |
| Frontend updates | 50 min |
| Testing | 60 min |
| **TOTAL** | **~5 hours** |

---

## Priority Order

1. **CRITICAL** (Do first):
   - analytics.py
   - voice.py
   - campaigns.py

2. **HIGH** (Do second):
   - models.py
   - templates.py
   - Frontend updates

3. **MEDIUM** (Do third):
   - teams.py
   - bulk.py
   - Additional security features

4. **FINAL** (Do last):
   - Comprehensive testing
   - Documentation updates

---

## Success Criteria

✅ All endpoints require authentication
✅ No IDOR vulnerabilities
✅ No user_id in request parameters
✅ HttpOnly cookies for JWT tokens
✅ Rate limiting on auth endpoints
✅ CSRF protection enabled
✅ File upload validation
✅ All tests passing
✅ Frontend using cookies instead of localStorage
✅ API documentation updated

---

## Support Files

- `SECURITY_AUDIT_REPORT.md` - Original vulnerability report
- `SECURITY_FIXES_APPLIED.md` - Detailed fix documentation
- `SECURITY_FIXES_REMAINING.md` - Implementation patterns
- `SECURITY_IMPLEMENTATION_SUMMARY.md` - Progress summary
- `backend/app/routes/content.py` - Reference implementation
- `backend/app/routes/translation.py` - Reference implementation
- `backend/app/routes/social.py` - Reference implementation
