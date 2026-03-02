# Remaining Security Fixes - Implementation Guide

## Summary
Translation routes have been secured. The following routes still need security updates.

## Pattern to Apply

All routes need these changes:

### 1. Add Authentication Import
```python
from app.auth.dependencies import get_current_user, enforce_quota
```

### 2. Remove user_id from Request Schemas
```python
# BEFORE
class SomeRequest(BaseModel):
    user_id: int  # ❌ REMOVE THIS
    other_field: str

# AFTER  
class SomeRequest(BaseModel):
    other_field: str  # ✅ No user_id
```

### 3. Add Authentication to Endpoints
```python
# BEFORE
@router.post("/endpoint")
async def some_endpoint(request: SomeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()

# AFTER
@router.post("/endpoint")
async def some_endpoint(
    request: SomeRequest,
    current_user: User = Depends(get_current_user),  # ✅ Add this
    db: Session = Depends(get_db)
):
    # Use current_user.id instead of request.user_id
```

### 4. Add IDOR Protection
```python
# BEFORE
content = db.query(Content).filter(Content.id == content_id).first()

# AFTER
content = db.query(Content).filter(
    Content.id == content_id,
    Content.user_id == current_user.id  # ✅ Prevent IDOR
).first()
```

### 5. Use Quota Enforcement for Resource-Intensive Operations
```python
@router.post("/generate")
async def generate(
    request: GenerateRequest,
    current_user: User = Depends(enforce_quota("content_generation")),  # ✅
    db: Session = Depends(get_db)
):
```

## Routes to Update

### 1. backend/app/routes/social.py ✅ DONE
- Created social_secured.py with all fixes
- Replace original file with secured version

### 2. backend/app/routes/analytics.py
**Changes needed:**
- Remove `user_id` parameter from all endpoints
- Add `current_user: User = Depends(get_current_user)` to all endpoints
- Replace `user_id` with `current_user.id` in queries
- Add IDOR protection to all resource queries

**Endpoints to update:**
- `get_analytics_overview(user_id)` → `get_analytics_overview(current_user)`
- `get_platform_performance(user_id)` → `get_platform_performance(current_user)`
- `get_content_type_performance(user_id)` → `get_content_type_performance(current_user)`
- `get_engagement_trends(user_id)` → `get_engagement_trends(current_user)`
- `get_top_performing_content(user_id)` → `get_top_performing_content(current_user)`
- `get_language_distribution(user_id)` → `get_language_distribution(current_user)`
- `sync_post_metrics(post_id)` → Add IDOR check

### 3. backend/app/routes/voice.py
**Changes needed:**
- Remove `user_id` parameter from `upload_voice_input`
- Add authentication to all endpoints
- Add IDOR protection
- Add file validation (check actual file content, not just Content-Type)

**Endpoints to update:**
- `upload_voice_input(user_id, audio_file)` → `upload_voice_input(audio_file, current_user)`
- `list_voice_inputs(user_id)` → `list_voice_inputs(current_user)`
- `get_voice_input(voice_input_id)` → Add IDOR check
- `convert_voice_to_content(voice_input_id)` → Add IDOR check
- `delete_voice_input(voice_input_id)` → Add IDOR check

### 4. backend/app/routes/campaigns.py
**Changes needed:**
- Remove `user_id` from `CampaignCreate` schema
- Add authentication to all endpoints
- Add IDOR protection
- Add RBAC for approval operations

**Endpoints to update:**
- `create_campaign(campaign_data)` → Add `current_user`
- `get_campaigns(user_id)` → `get_campaigns(current_user)`
- `get_campaign(campaign_id)` → Add IDOR check
- `update_campaign(campaign_id)` → Add IDOR check
- `update_campaign_metrics(campaign_id)` → Add IDOR check
- `update_campaign_status(campaign_id)` → Add IDOR check
- `approve_campaign(campaign_id, approver_id)` → Use `current_user.id` for approver
- `delete_campaign(campaign_id)` → Add IDOR check
- `get_campaign_analytics(campaign_id)` → Add IDOR check

### 5. backend/app/routes/models.py
**Changes needed:**
- Remove `user_id` parameters from all endpoints
- Add authentication
- Add IDOR protection

**Endpoints to update:**
- `get_available_models(user_id)` → `get_available_models(current_user)`
- `get_user_models(user_id)` → `get_user_models(current_user)`
- `configure_model(user_id, model_id)` → `configure_model(model_id, current_user)`
- `get_model_usage_stats(user_id)` → `get_model_usage_stats(current_user)`
- `get_primary_model(user_id)` → `get_primary_model(current_user)`
- `increment_model_usage(user_id, model_id)` → `increment_model_usage(model_id, current_user)`

### 6. backend/app/routes/teams.py
**Changes needed:**
- Remove `user_id` parameters
- Add authentication
- Add RBAC checks (owner/admin/member)
- Add IDOR protection

**Endpoints to update:**
- `create_team(team, user_id)` → `create_team(team, current_user)`
- `get_user_teams(user_id)` → `get_user_teams(current_user)`
- `update_team(team_id, team_update, user_id)` → `update_team(team_id, team_update, current_user)`
- `delete_team(team_id, user_id)` → `delete_team(team_id, current_user)`
- `update_member_role(team_id, member_id, new_role, user_id)` → Use `current_user`
- `remove_team_member(team_id, member_id, user_id)` → Use `current_user`
- `invite_member(team_id, invite, user_id)` → Use `current_user`
- `accept_invite(invite_id, user_id)` → Use `current_user`
- `add_comment(team_id, comment, user_id)` → Use `current_user`
- `request_approval(team_id, approval, user_id)` → Use `current_user`
- `review_approval(approval_id, status, notes, user_id)` → Use `current_user`
- `get_pending_approvals(team_id, user_id)` → Use `current_user`

### 7. backend/app/routes/templates.py
**Changes needed:**
- Remove `user_id` parameters
- Add authentication
- Add IDOR protection

**Endpoints to update:**
- `create_template(template, user_id)` → `create_template(template, current_user)`
- `get_templates(user_id)` → `get_templates(current_user)`
- `get_user_templates(user_id)` → `get_user_templates(current_user)`
- `get_favorite_templates(user_id)` → `get_favorite_templates(current_user)`
- `get_templates_by_category(category, user_id)` → `get_templates_by_category(category, current_user)`
- `update_template(template_id, template_update, user_id)` → Use `current_user`
- `delete_template(template_id, user_id)` → Use `current_user`
- `toggle_favorite(template_id, user_id)` → Use `current_user`

### 8. backend/app/routes/bulk.py
**Changes needed:**
- Remove hardcoded `user_id = 1`
- Add authentication to all endpoints
- Add file validation

**Endpoints to update:**
- `upload_bulk_csv(file, operation_type, user_id=1)` → `upload_bulk_csv(file, operation_type, current_user)`
- All other endpoints should verify task ownership

## Additional Security Enhancements

### 1. Add Rate Limiting to Auth Endpoints
```python
# In backend/app/routes/users.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")  # ✅ Add rate limiting
async def login(...):
```

### 2. Add CSRF Protection
```python
# In backend/app/main.py
from starlette.middleware.sessions import SessionMiddleware
from starlette_csrf import CSRFMiddleware

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(CSRFMiddleware, secret=settings.SECRET_KEY)
```

### 3. Add File Upload Validation
```python
# Install python-magic
# pip install python-magic python-magic-bin

import magic

def validate_file_type(file_content: bytes, expected_types: list):
    """Validate actual file content, not just extension"""
    mime = magic.from_buffer(file_content, mime=True)
    if mime not in expected_types:
        raise HTTPException(400, f"Invalid file type: {mime}")
```

## Testing Checklist

After implementing fixes:

- [ ] Test all endpoints require authentication
- [ ] Test IDOR protection (user A cannot access user B's resources)
- [ ] Test quota enforcement
- [ ] Test rate limiting on auth endpoints
- [ ] Test file upload validation
- [ ] Test RBAC for team operations
- [ ] Update API documentation
- [ ] Update frontend to remove user_id parameters
- [ ] Update frontend to use HttpOnly cookies

## Priority Order

1. **HIGH**: social.py, analytics.py, voice.py (most used features)
2. **MEDIUM**: campaigns.py, models.py, templates.py
3. **LOW**: teams.py, bulk.py (less critical features)

## Estimated Time

- Each route: 15-20 minutes
- Total: ~2-3 hours for all routes
- Frontend updates: 1-2 hours
- Testing: 1-2 hours

**Total estimated time: 4-7 hours**
