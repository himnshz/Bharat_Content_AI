# QA Fix Checklist: Frontend-Backend Integration

**Project:** Bharat Content AI Platform  
**Date:** March 2, 2026  
**Status:** Ready for Implementation

---

## PHASE 1: CRITICAL FIXES (Day 1 - 8 hours)

### 1.1 Replace Hardcoded fetch() with fetchAPI() ⚠️ CRITICAL

**Files to Update:**

- [ ] `frontend-new/src/components/dashboard/TranslateContent.tsx`
  - [ ] Line 18: Replace hardcoded fetch with `fetchAPI(API_ENDPOINTS.translate, ...)`
  - [ ] Import: `import { API_ENDPOINTS, fetchAPI } from '@/lib/api'`

- [ ] `frontend-new/src/components/dashboard/ScheduleContent.tsx`
  - [ ] Line 38: Replace with `fetchAPI(API_ENDPOINTS.schedulePost, ...)`
  - [ ] Fix field name: `content` → `text_content`

- [ ] `frontend-new/src/components/dashboard/TemplatesContent.tsx`
  - [ ] Lines 60, 63, 66, 69: Replace with `fetchAPI(API_ENDPOINTS.templates + '/...', ...)`
  - [ ] Lines 103, 118, 133, 148: Update all template API calls
  - [ ] Line 380: Update create template call

- [ ] `frontend-new/src/components/dashboard/ModelsContent.tsx`
  - [ ] Lines 44, 47: Replace with `fetchAPI(API_ENDPOINTS.models + '/available', ...)`
  - [ ] Line 62: Update configure model call

- [ ] `frontend-new/src/components/dashboard/AnalyticsContent.tsx`
  - [ ] Lines 56, 69, 82: Replace with `fetchAPI(API_ENDPOINTS.analyticsOverview + '...', ...)`

- [ ] `frontend-new/src/components/dashboard/TeamContent.tsx`
  - [ ] Lines 48, 68, 78, 88: Replace with `fetchAPI(API_ENDPOINTS.teams + '/...', ...)`

- [ ] `frontend-new/src/components/dashboard/CalendarContent.tsx`
  - [ ] Line 42: Replace with `fetchAPI(API_ENDPOINTS.listPosts + '...', ...)`
  - [ ] Line 95: Fix endpoint to use `/reschedule/` instead of base URL

- [ ] `frontend-new/src/components/dashboard/team/MemberList.tsx`
  - [ ] Lines 28, 38: Replace with `fetchAPI(API_ENDPOINTS.teams + '/...', ...)`

- [ ] `frontend-new/src/components/dashboard/team/InviteModal.tsx`
  - [ ] Line 26: Replace with `fetchAPI(API_ENDPOINTS.teams + '/...', ...)`

- [ ] `frontend-new/src/components/dashboard/team/ApprovalCard.tsx`
  - [ ] Line 24: Replace with `fetchAPI(API_ENDPOINTS.teams + '/...', ...)`

**Verification:**
```bash
# Search for remaining hardcoded URLs
grep -r "http://127.0.0.1:8000" frontend-new/src/components/
# Should return 0 results after fixes
```

---

### 1.2 Remove localStorage userId Usage ⚠️ CRITICAL

**Pattern to Remove:**
```typescript
// ✗ REMOVE THIS:
const userId = localStorage.getItem('userId') || '1';
fetch(`http://127.0.0.1:8000/api/endpoint?user_id=${userId}`)

// ✓ REPLACE WITH:
import { fetchAPI, API_ENDPOINTS } from '@/lib/api'
fetchAPI(API_ENDPOINTS.endpoint)  // Backend gets user from JWT token
```

**Files to Update:**

- [ ] `TemplatesContent.tsx`
  - [ ] Line 60: Remove `?user_id=${userId}` from URL
  - [ ] Line 63: Remove `user/${userId}` - use `/user` endpoint
  - [ ] Line 66: Remove `favorites/${userId}` - use `/favorites` endpoint
  - [ ] Line 103: Remove `?user_id=${userId}` from use template
  - [ ] Line 118: Remove `?user_id=${userId}` from favorite toggle
  - [ ] Line 133: Remove `?user_id=${userId}` from delete
  - [ ] Line 148: Remove `?user_id=${userId}` from delete
  - [ ] Line 380: Remove `?user_id=${userId}` from create

- [ ] `TeamContent.tsx`
  - [ ] Line 48: Remove `user/${userId}` - backend uses authenticated user
  - [ ] Line 78: Remove `?user_id=${userId}` from pending approvals
  - [ ] Line 88: Remove `?user_id=${userId}` from create team
  - [ ] Line 98: Remove userId variable declaration

- [ ] `MemberList.tsx`
  - [ ] Line 28: Remove `?user_id=${userId}` from remove member
  - [ ] Line 38: Remove `?user_id=${userId}` from change role

- [ ] `InviteModal.tsx`
  - [ ] Line 26: Remove `?user_id=${userId}` from invite

- [ ] `ApprovalCard.tsx`
  - [ ] Line 24: Remove `?user_id=${userId}` from review

- [ ] `CalendarContent.tsx`
  - [ ] Line 42: Remove `scheduled/${userId}` - use authenticated endpoint

- [ ] `ModelsContent.tsx`
  - [ ] Line 36: Remove userId variable - not needed

**Verification:**
```bash
# Search for remaining localStorage userId usage
grep -r "localStorage.getItem('userId')" frontend-new/src/components/dashboard/
# Should return 0 results after fixes
```

---

### 1.3 Fix Field Name Mismatches ⚠️ CRITICAL

- [ ] **ScheduleContent.tsx** (Line 42)
  ```typescript
  // ✗ WRONG:
  body: JSON.stringify({
    content: content,  // Wrong field name
    platform: platform,
    scheduled_time: scheduledTime,
  })
  
  // ✓ CORRECT:
  body: JSON.stringify({
    text_content: content,  // Correct field name
    platform: platform,
    scheduled_time: scheduledTime,
  })
  ```

- [ ] **CalendarContent.tsx** (Line 95)
  ```typescript
  // ✗ WRONG:
  const response = await fetch(`http://127.0.0.1:8000/api/social/${postId}`, {
    method: 'PUT',
    body: JSON.stringify({ scheduled_time: newTime })
  });
  
  // ✓ CORRECT:
  const response = await fetchAPI(`${API_ENDPOINTS.listPosts}/reschedule/${postId}`, {
    method: 'PUT',
    body: JSON.stringify({ scheduled_time: newTime })
  });
  ```

---

### 1.4 Fix Enum Value Mappings ⚠️ CRITICAL

- [ ] **lib/api.ts** - Update PLATFORM_MAP
  ```typescript
  // ✗ WRONG:
  export const PLATFORM_MAP: Record<string, string> = {
    'facebook': 'FACEBOOK',  // Backend expects lowercase
    'twitter': 'TWITTER',
    'instagram': 'INSTAGRAM',
  };
  
  // ✓ CORRECT:
  export const PLATFORM_MAP: Record<string, string> = {
    'facebook': 'facebook',  // Match backend enum
    'twitter': 'twitter',
    'instagram': 'instagram',
    'linkedin': 'linkedin',
    'youtube': 'youtube',
  };
  ```

- [ ] **lib/api.ts** - Update CONTENT_TYPE_MAP
  ```typescript
  // ✗ WRONG:
  export const CONTENT_TYPE_MAP: Record<string, string> = {
    'blog_post': 'BLOG',
    'social_media': 'SOCIAL_POST',
  };
  
  // ✓ CORRECT:
  export const CONTENT_TYPE_MAP: Record<string, string> = {
    'blog_post': 'blog',
    'social_media': 'social_post',
    'article': 'article',
    'email': 'email',
  };
  ```

- [ ] **lib/api.ts** - Update TONE_MAP
  ```typescript
  // ✗ WRONG:
  export const TONE_MAP: Record<string, string> = {
    'professional': 'PROFESSIONAL',
    'casual': 'CASUAL',
  };
  
  // ✓ CORRECT:
  export const TONE_MAP: Record<string, string> = {
    'professional': 'professional',
    'casual': 'casual',
    'friendly': 'friendly',
    'formal': 'formal',
  };
  ```

---

## PHASE 2: HIGH PRIORITY FIXES (Day 2 - 8 hours)

### 2.1 Add Comprehensive Error Handling

**Pattern to Implement:**
```typescript
const [error, setError] = useState<string | null>(null);

try {
  setError(null);
  const response = await fetchAPI(endpoint, options);
  
  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.detail || `Error: ${response.status}`);
  }
  
  const data = await response.json();
  // Process data...
  
} catch (err) {
  const message = err instanceof Error ? err.message : 'An error occurred';
  setError(message);
  console.error('API Error:', err);
}
```

**Files to Update:**

- [ ] `TranslateContent.tsx` - Add error state display
- [ ] `TemplatesContent.tsx` - Add error handling to all API calls
- [ ] `ModelsContent.tsx` - Add error handling to configure/usage calls
- [ ] `AnalyticsContent.tsx` - Add error handling to analytics fetches
- [ ] `TeamContent.tsx` - Add error handling to team operations
- [ ] `MemberList.tsx` - Add error handling to member operations
- [ ] `CalendarContent.tsx` - Add error handling to calendar operations

**Error Display Component:**
```typescript
{error && (
  <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm mb-4">
    <div className="flex items-center gap-2">
      <span>⚠️</span>
      <span>{error}</span>
    </div>
  </div>
)}
```

---

### 2.2 Implement Token Expiration Handling

- [ ] **lib/api.ts** - Add token validation
  ```typescript
  export function isTokenExpired(): boolean {
    const token = getAuthToken();
    if (!token) return true;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  }
  
  export async function fetchAPI(
    endpoint: string,
    options: RequestInit = {},
    timeout?: number
  ): Promise<Response> {
    // Check token before request
    if (isTokenExpired()) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
      throw new Error('Session expired');
    }
    
    const response = await fetchWithTimeout(endpoint, options, timeout);
    
    // Handle 401 responses
    if (response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
      throw new Error('Authentication required');
    }
    
    return response;
  }
  ```

---

### 2.3 Add Client-Side Validation

- [ ] **TranslateContent.tsx**
  ```typescript
  const handleTranslate = async () => {
    // Validation
    if (!sourceText.trim()) {
      setError('Please enter text to translate');
      return;
    }
    
    if (sourceText.length > 10000) {
      setError('Text too long. Maximum 10,000 characters.');
      return;
    }
    
    if (sourceLang === targetLang) {
      setError('Source and target languages must be different');
      return;
    }
    
    // Proceed with API call...
  }
  ```

- [ ] **ScheduleContent.tsx**
  ```typescript
  const handleSchedule = async () => {
    // Validation
    if (!content.trim()) {
      setError('Please enter content');
      return;
    }
    
    // Platform-specific validation
    if (platform === 'twitter' && content.length > 280) {
      setError('Twitter posts must be 280 characters or less');
      return;
    }
    
    if (!date || !time) {
      setError('Please select date and time');
      return;
    }
    
    const scheduledTime = new Date(`${date}T${time}`);
    if (scheduledTime <= new Date()) {
      setError('Scheduled time must be in the future');
      return;
    }
    
    // Proceed with API call...
  }
  ```

- [ ] **TemplatesContent.tsx** - Add template name validation
- [ ] **InviteModal.tsx** - Add email format validation

---

## PHASE 3: MEDIUM PRIORITY (Days 3-4 - 16 hours)

### 3.1 Implement Cache Invalidation

- [ ] Create custom hook `useInvalidateCache`
- [ ] Invalidate templates cache after create/update/delete
- [ ] Invalidate team cache after member changes
- [ ] Invalidate posts cache after scheduling/rescheduling

### 3.2 Add Optimistic Updates

- [ ] Templates: Update UI immediately on delete
- [ ] Posts: Update UI immediately on reschedule
- [ ] Team members: Update UI immediately on role change

### 3.3 Implement Pagination

- [ ] TemplatesContent: Add pagination controls
- [ ] CalendarContent: Paginate scheduled posts
- [ ] AnalyticsContent: Paginate performance data

### 3.4 Add Loading Skeletons

- [ ] Replace spinners with skeleton screens
- [ ] Add shimmer effect for better UX

### 3.5 Add Abort Controllers

- [ ] Implement cleanup on component unmount
- [ ] Cancel pending requests when navigating away

---

## PHASE 4: TESTING & VALIDATION (Day 5 - 8 hours)

### 4.1 Integration Tests

- [ ] Test authentication flow
- [ ] Test API error handling
- [ ] Test field name mappings
- [ ] Test enum value compatibility

### 4.2 Security Audit

- [ ] Verify no IDOR vulnerabilities
- [ ] Verify all API calls use authentication
- [ ] Verify XSS prevention in inputs
- [ ] Verify CSRF protection

### 4.3 Performance Testing

- [ ] Test with large datasets
- [ ] Test network throttling
- [ ] Test concurrent requests
- [ ] Measure page load times

---

## VERIFICATION COMMANDS

```bash
# 1. Check for hardcoded URLs
grep -r "http://127.0.0.1:8000" frontend-new/src/components/

# 2. Check for localStorage userId
grep -r "localStorage.getItem('userId')" frontend-new/src/components/

# 3. Check for direct fetch() calls (should use fetchAPI)
grep -r "fetch(" frontend-new/src/components/dashboard/ | grep -v "fetchAPI"

# 4. Run TypeScript compiler
cd frontend-new && npm run build

# 5. Run linter
cd frontend-new && npm run lint

# 6. Test authentication
# - Try accessing dashboard without login
# - Try with expired token
# - Try with invalid token

# 7. Test API calls
# - Check browser network tab for Authorization headers
# - Verify no user_id query parameters
# - Verify correct field names in request bodies
```

---

## SUCCESS CRITERIA

### Phase 1 Complete When:
- ✅ Zero hardcoded API URLs remain
- ✅ Zero localStorage userId usage
- ✅ All API calls use fetchAPI() with auth headers
- ✅ Field names match backend expectations
- ✅ Enum values match backend enums
- ✅ Post scheduling works
- ✅ Calendar rescheduling works

### Phase 2 Complete When:
- ✅ All API errors display to users
- ✅ Expired tokens redirect to login
- ✅ Client-side validation prevents invalid requests
- ✅ No console errors on normal usage

### Phase 3 Complete When:
- ✅ Cache invalidates after mutations
- ✅ UI updates optimistically
- ✅ Pagination implemented for large lists
- ✅ Loading states use skeletons

### Phase 4 Complete When:
- ✅ Integration tests pass
- ✅ Security audit complete
- ✅ Performance benchmarks met
- ✅ Production deployment approved

---

## NOTES

- **Backup before starting:** Create git branch for fixes
- **Test incrementally:** Test after each file update
- **Document changes:** Update CHANGELOG.md
- **Code review:** Have another developer review changes
- **Staging deployment:** Test in staging before production

---

**Checklist Owner:** Development Team  
**Review Date:** March 2, 2026  
**Target Completion:** March 9, 2026
