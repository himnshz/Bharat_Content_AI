# Security Implementation - Quick Reference Card

## 🎯 Current Status
- ✅ **DONE:** 4/11 routes (36%)
- ⚠️ **TODO:** 7/11 routes (64%)
- ⏱️ **Time Remaining:** ~5 hours

## 📚 Key Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `COMPLETE_SECURITY_IMPLEMENTATION.md` | Step-by-step action plan | **START HERE** |
| `SECURITY_FIXES_REMAINING.md` | Implementation patterns | When coding |
| `WORK_COMPLETED_SUMMARY.md` | What's done, what's left | For overview |
| `backend/app/routes/content.py` | Reference implementation | As template |

## 🔧 The Security Pattern (Copy-Paste This)

### Step 1: Add Import
```python
from app.auth.dependencies import get_current_user, enforce_quota
```

### Step 2: Remove user_id from Schemas
```python
# DELETE THIS:
class SomeRequest(BaseModel):
    user_id: int  # ❌ DELETE
```

### Step 3: Update Endpoint Signature
```python
# BEFORE:
async def endpoint(request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()

# AFTER:
async def endpoint(
    request: Request,
    current_user: User = Depends(get_current_user),  # ✅ ADD THIS
    db: Session = Depends(get_db)
):
    # Use current_user directly, no query needed
```

### Step 4: Add IDOR Protection
```python
# BEFORE:
resource = db.query(Resource).filter(Resource.id == id).first()

# AFTER:
resource = db.query(Resource).filter(
    Resource.id == id,
    Resource.user_id == current_user.id  # ✅ ADD THIS
).first()
```

### Step 5: Use Quota Enforcement (Optional)
```python
# For resource-intensive operations:
async def generate(
    request: Request,
    current_user: User = Depends(enforce_quota("content_generation")),  # ✅
    db: Session = Depends(get_db)
):
```

## 📋 Routes to Update (Priority Order)

### 🔴 HIGH PRIORITY (Do First - ~1 hour)
1. ✅ ~~content.py~~ (DONE)
2. ✅ ~~translation.py~~ (DONE)
3. ✅ ~~social.py~~ (DONE)
4. ⚠️ **analytics.py** (20 min) - 7 endpoints
5. ⚠️ **voice.py** (20 min) - 6 endpoints
6. ⚠️ **campaigns.py** (25 min) - 10 endpoints

### 🟡 MEDIUM PRIORITY (Do Second - ~1 hour)
7. ⚠️ **models.py** (15 min) - 7 endpoints
8. ⚠️ **templates.py** (20 min) - 11 endpoints

### 🟢 LOW PRIORITY (Do Third - ~1 hour)
9. ⚠️ **teams.py** (30 min) - 15+ endpoints
10. ⚠️ **bulk.py** (25 min) - 9 endpoints

## 🎨 Frontend Updates (~1 hour)

### Remove localStorage
```typescript
// DELETE THIS:
localStorage.setItem('token', data.access_token);  // ❌
localStorage.getItem('token');  // ❌
```

### Add credentials: 'include'
```typescript
// ADD THIS TO ALL FETCH CALLS:
const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',  // ✅ ADD THIS
  body: JSON.stringify(data)
});
```

### Remove user_id from requests
```typescript
// BEFORE:
body: JSON.stringify({ user_id: userId, prompt: prompt })  // ❌

// AFTER:
body: JSON.stringify({ prompt: prompt })  // ✅
```

## 🔒 Additional Security (~40 min)

### 1. Rate Limiting (15 min)
```bash
pip install slowapi
```
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(...):
```

### 2. CSRF Protection (10 min)
```bash
pip install starlette-csrf
```
```python
from starlette_csrf import CSRFMiddleware
app.add_middleware(CSRFMiddleware, secret=settings.SECRET_KEY)
```

### 3. File Validation (15 min)
```bash
pip install python-magic python-magic-bin
```
```python
import magic
mime = magic.from_buffer(file_content, mime=True)
if mime not in allowed_types:
    raise HTTPException(400, "Invalid file type")
```

## ✅ Testing Checklist

- [ ] Login works
- [ ] Protected endpoints require auth (401 without token)
- [ ] User A cannot access User B's data (404 or 403)
- [ ] Quota enforcement works
- [ ] Rate limiting works (try 6 logins in 1 minute)
- [ ] File upload rejects invalid types
- [ ] Frontend uses cookies (no localStorage)
- [ ] All CRUD operations work

## 🚀 Quick Start

1. Open `COMPLETE_SECURITY_IMPLEMENTATION.md`
2. Pick a route from HIGH PRIORITY section
3. Follow the code examples
4. Copy-paste the pattern
5. Test the endpoint
6. Move to next route

## 📞 Need Help?

- **For detailed instructions:** `COMPLETE_SECURITY_IMPLEMENTATION.md`
- **For code examples:** `backend/app/routes/content.py`
- **For patterns:** `SECURITY_FIXES_REMAINING.md`
- **For overview:** `WORK_COMPLETED_SUMMARY.md`

## 💡 Pro Tips

1. **Use completed routes as templates** - Copy from content.py, translation.py, or social.py
2. **Test as you go** - Don't wait until all routes are done
3. **Follow the priority order** - High priority routes are most used
4. **Use find-and-replace** - Replace `user_id` with `current_user.id` in bulk
5. **Check diagnostics** - Use getDiagnostics tool to catch errors early

## ⏱️ Time Budget

| Task | Time |
|------|------|
| High priority routes | 1 hour |
| Medium priority routes | 1 hour |
| Low priority routes | 1 hour |
| Frontend updates | 1 hour |
| Additional security | 40 min |
| Testing | 1 hour |
| **TOTAL** | **~5.5 hours** |

## 🎯 Success Criteria

When you're done:
- ✅ All endpoints require authentication
- ✅ No IDOR vulnerabilities
- ✅ No user_id in request parameters
- ✅ HttpOnly cookies for JWT
- ✅ Rate limiting on auth
- ✅ CSRF protection enabled
- ✅ File validation working
- ✅ All tests passing

---

**Remember:** The pattern is the same for all routes. Once you do one, the rest are easy!
