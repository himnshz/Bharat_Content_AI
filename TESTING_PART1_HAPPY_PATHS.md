# 🎯 PART 1: Critical User Flows - Happy Path Testing

## Flow 1: AI Content Generation with Intelligent Fallback

**Business Context:** Users generate AI content with automatic failover across 8 AI providers

**Prerequisites:**
- User registered and logged in (user_id: 1, email: test@example.com)
- At least one AI service API key configured (Gemini preferred)
- User has remaining quota: content_generated_count < tier limit
- Free tier: 100/month, Basic: 1000/month, Pro: 10000/month

**Test Data:**
```json
{
  "prompt": "Create a social media post about AI benefits in Hindi",
  "language": "hindi",
  "tone": "casual",
  "content_type": "social_post"
}
```

**Detailed Test Steps:**

| Step | Action | API Endpoint | Expected Result | Verification Point |
|------|--------|--------------|----------------|-------------------|
| 1 | Login as test user | POST /api/auth/login | 200 OK, JWT token returned | Token in response.access_token |
| 2 | Navigate to Generate Content | GET /api/content/list | 200 OK, existing content list | Response.total >= 0 |
| 3 | Submit generation request | POST /api/content/generate | 201 Created, content object | Response.id exists |
| 4 | Verify content in database | GET /api/content/{id} | 200 OK, content details | content.user_id == 1 |
| 5 | Check user quota updated | GET /api/users/profile/1 | 200 OK, quota incremented | user.content_generated_count += 1 |

**Expected Response Structure:**
```json
{
  "id": 123,
  "original_prompt": "Create a social media post...",
  "generated_content": "एआई के फायदे...",
  "content_type": "social_post",
  "status": "generated",
  "language": "hindi",
  "tone": "casual",
  "model_used": "gemini-pro",
  "generation_time_ms": 3500,
  "word_count": 45,
  "quality_score": 85.0,
  "created_at": "2026-03-02T10:30:00Z"
}
```

**Success Criteria:**
✅ HTTP 201 Created status
✅ Content generated in Hindi language
✅ Casual tone maintained
✅ Generation time < 15000ms
✅ Word count between 20-200
✅ Quality score >= 70
✅ User quota decremented
✅ Content saved with correct user_id

---

## Flow 2: Campaign Management Lifecycle

**Business Context:** Users create, manage, and track influencer marketing campaigns

**Prerequisites:**
- User authenticated with valid JWT
- User has campaign creation permissions
- Database has campaigns table

**Test Data:**
```json
{
  "name": "Summer Product Launch 2026",
  "description": "Launch new AI-powered product",
  "campaign_type": "product_launch",
  "status": "draft",
  "budget": 50000.00,
  "currency": "USD",
  "start_date": "2026-06-01T00:00:00Z",
  "end_date": "2026-08-31T23:59:59Z",
  "platforms": ["instagram", "youtube", "twitter"],
  "target_reach": 1000000,
  "target_engagement_rate": 4.5
}
```

**Detailed Test Steps:**

| Step | Action | API Endpoint | Expected Result | Verification |
|------|--------|--------------|----------------|--------------|
| 1 | Create new campaign | POST /api/campaigns/ | 201 Created | campaign.id exists |
| 2 | Verify campaign in list | GET /api/campaigns/ | 200 OK | campaign in response.items |
| 3 | Get campaign details | GET /api/campaigns/{id} | 200 OK | All fields match input |
| 4 | Update campaign status | PATCH /api/campaigns/{id}/status | 200 OK | status changed to "active" |
| 5 | Update metrics | PATCH /api/campaigns/{id}/metrics | 200 OK | actual_reach updated |
| 6 | Get analytics | GET /api/campaigns/{id}/analytics | 200 OK | ROI calculated |
| 7 | Approve campaign | PATCH /api/campaigns/{id}/approve | 200 OK | approved_by set |

**Success Criteria:**
✅ Campaign created with user_id
✅ Status transitions: draft → active → completed
✅ Budget tracking accurate
✅ ROI calculated correctly: ((revenue - spent) / spent) * 100
✅ Days remaining calculated from end_date
✅ Only owner can update/delete campaign

---

## Flow 3: Team Collaboration & Role-Based Access

**Business Context:** Team owners invite members with specific roles (Owner/Admin/Editor/Viewer)

**Prerequisites:**
- User A (Owner): user_id=1, email=owner@example.com
- User B (to be invited): email=editor@example.com
- No existing team for User A

**Test Data:**
```json
{
  "team": {
    "name": "Marketing Team",
    "description": "Content marketing team"
  },
  "invite": {
    "email": "editor@example.com",
    "role": "editor"
  }
}
```

**Detailed Test Steps:**

| Step | Action | API Endpoint | Expected Result | Verification |
|------|--------|--------------|----------------|--------------|
| 1 | User A creates team | POST /api/teams/ | 201 Created | team.owner_id == 1 |
| 2 | User A auto-added as owner | GET /api/teams/{id}/members | 200 OK | User A has role "owner" |
| 3 | User A invites User B | POST /api/teams/{id}/invites | 201 Created | invite.status == "pending" |
| 4 | Verify invite in list | GET /api/teams/{id}/invites | 200 OK | Invite visible |
| 5 | User B accepts invite | POST /api/teams/invites/{id}/accept | 200 OK | User B added to team |
| 6 | Verify User B in members | GET /api/teams/{id}/members | 200 OK | User B has role "editor" |
| 7 | User B tries to invite (should fail) | POST /api/teams/{id}/invites | 403 Forbidden | Only owner/admin can invite |
| 8 | User A updates User B role | PUT /api/teams/{id}/members/{member_id}/role | 200 OK | Role changed to "admin" |
| 9 | User B can now invite | POST /api/teams/{id}/invites | 201 Created | Admin can invite |
| 10 | User A removes User B | DELETE /api/teams/{id}/members/{member_id} | 200 OK | User B removed |

**Role Permission Matrix:**

| Action | Owner | Admin | Editor | Viewer |
|--------|-------|-------|--------|--------|
| Create Team | ✅ | ❌ | ❌ | ❌ |
| Invite Members | ✅ | ✅ | ❌ | ❌ |
| Remove Members | ✅ | ✅ | ❌ | ❌ |
| Update Roles | ✅ | ✅ | ❌ | ❌ |
| Edit Content | ✅ | ✅ | ✅ | ❌ |
| View Content | ✅ | ✅ | ✅ | ✅ |
| Delete Team | ✅ | ❌ | ❌ | ❌ |

**Success Criteria:**
✅ Team created with owner as first member
✅ Invites expire after 7 days
✅ Role-based permissions enforced
✅ Activity log tracks all actions
✅ Cannot remove team owner
✅ Cannot change owner role

---

## Flow 4: Post Scheduling & Publishing

**Business Context:** Users schedule social media posts to multiple platforms

**Prerequisites:**
- User authenticated
- Content generated (content_id: 123)
- User has posts_scheduled quota remaining
- Scheduled time is in the future

**Test Data:**
```json
{
  "content_id": 123,
  "text_content": "Check out our new AI features!",
  "platform": "instagram",
  "scheduled_time": "2026-03-05T14:00:00Z",
  "media_urls": ["https://example.com/image1.jpg"]
}
```

**Detailed Test Steps:**

| Step | Action | API Endpoint | Expected Result | Verification |
|------|--------|--------------|----------------|--------------|
| 1 | Schedule single post | POST /api/social/schedule | 201 Created | post.status == "scheduled" |
| 2 | Verify in post list | GET /api/social/list | 200 OK | Post appears in list |
| 3 | Get post details | GET /api/social/{post_id} | 200 OK | All fields correct |
| 4 | Reschedule post | PUT /api/social/reschedule/{post_id} | 200 OK | scheduled_time updated |
| 5 | Bulk schedule to 3 platforms | POST /api/social/schedule/bulk | 201 Created | 3 posts created |
| 6 | View calendar | GET /api/social/calendar | 200 OK | Posts grouped by date |
| 7 | Publish immediately | POST /api/social/{post_id}/publish | 200 OK | status == "published" |
| 8 | Cancel scheduled post | POST /api/social/{post_id}/cancel | 200 OK | status == "cancelled" |

**Platform-Specific Validation:**

| Platform | Max Length | Required Fields | Media Support |
|----------|-----------|----------------|---------------|
| Twitter | 280 chars | text_content | Images, Videos |
| Instagram | 2200 chars | text_content, media_urls | Images required |
| LinkedIn | 3000 chars | text_content | Images, Videos |
| Facebook | 63206 chars | text_content | Images, Videos |

**Success Criteria:**
✅ Cannot schedule in the past
✅ Platform character limits enforced
✅ User can only access own posts (IDOR prevented)
✅ Bulk scheduling creates multiple posts
✅ Calendar groups posts by date
✅ Published posts cannot be edited
✅ User quota incremented correctly

---

## Flow 5: User Authentication & Quota Management

**Business Context:** Users register, login, and have quota limits based on subscription tier

**Prerequisites:**
- Clean database (no existing user with test email)
- Valid email format
- Strong password requirements

**Test Data:**
```json
{
  "register": {
    "email": "newuser@example.com",
    "username": "newuser123",
    "password": "SecurePass123!",
    "full_name": "New User"
  },
  "login": {
    "email": "newuser@example.com",
    "password": "SecurePass123!"
  }
}
```

**Detailed Test Steps:**

| Step | Action | API Endpoint | Expected Result | Verification |
|------|--------|--------------|----------------|--------------|
| 1 | Register new user | POST /api/auth/register | 201 Created | user.id exists |
| 2 | Verify default tier | GET /api/users/profile/{id} | 200 OK | subscription_tier == "free" |
| 3 | Login with credentials | POST /api/auth/login | 200 OK | JWT token returned |
| 4 | Access protected route | GET /api/content/list | 200 OK | Authorization header accepted |
| 5 | Check initial quota | GET /api/users/profile/{id} | 200 OK | content_generated_count == 0 |
| 6 | Generate content 100 times | POST /api/content/generate (loop) | 201 Created | Quota increments |
| 7 | Attempt 101st generation | POST /api/content/generate | 429 Too Many Requests | Quota exceeded error |
| 8 | Upgrade to Basic tier | PUT /api/users/profile/{id} | 200 OK | subscription_tier == "basic" |
| 9 | Generate content again | POST /api/content/generate | 201 Created | New quota limit (1000) |

**Quota Limits by Tier:**

| Tier | Content Generation | Translations | Posts Scheduled | Price |
|------|-------------------|--------------|----------------|-------|
| Free | 100/month | 50/month | 20/month | $0 |
| Basic | 1,000/month | 500/month | 200/month | $9/month |
| Pro | 10,000/month | 5,000/month | 2,000/month | $29/month |
| Enterprise | Unlimited | Unlimited | Unlimited | $99/month |

**Success Criteria:**
✅ Password hashed (not stored in plaintext)
✅ JWT token expires after 60 minutes
✅ Refresh token valid for 7 days
✅ Quota enforced per operation type
✅ 429 error when quota exceeded
✅ Inactive users cannot access API
✅ Email must be unique

