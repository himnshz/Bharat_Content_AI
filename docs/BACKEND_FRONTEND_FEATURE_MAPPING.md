# Backend & Frontend Feature Mapping

## Complete System Overview

This document maps all backend API features to their recommended frontend implementations.

---

## 1. CONTENT GENERATION 🎨

### Backend API
**Endpoint**: `POST /api/content/generate`

**Features**:
- AI-powered content generation using 8 AI services (Gemini, Bedrock, OpenAI, Anthropic, Cohere, HuggingFace, Groq, Together AI)
- Automatic service fallback (primary → secondary → tertiary)
- Support for 11 Indian languages
- Multiple content types (blog_post, social_media, article, product_description)
- Tone customization (professional, casual, friendly, formal, humorous, inspirational, persuasive, informative)
- Word count and character count tracking
- Quality scoring and sentiment analysis

**Request**:
```json
{
  "prompt": "Write about AI in education",
  "language": "hindi",
  "tone": "professional",
  "content_type": "blog_post",
  "max_length": 500
}
```

**Response**:
```json
{
  "content": "Generated content...",
  "word_count": 450,
  "character_count": 2800,
  "model_used": "gemini-pro",
  "generation_time_ms": 1200
}
```

### Frontend Display ✅ IMPLEMENTED

**Component**: `GenerateContent.tsx`

**UI Elements**:
- Large textarea for prompt input
- Language dropdown (11 Indian languages)
- Tone selector
- Content type selector
- Reference file upload area
- Generate button with loading state
- Split-screen output panel
- Copy to clipboard button
- Word/character count display
- Generation time indicator

**Visual Design**:
- Left panel: Input form with glass effect
- Right panel: Output display with syntax highlighting
- Gradient borders (periwinkle/lavender)
- Floating animation for empty state
- Success animations on generation

---

## 2. TRANSLATION 🌐

### Backend API
**Endpoint**: `POST /api/translation/translate`

**Features**:
- Translation between 11 Indian languages + English
- Multiple translation methods (google, aws, azure, custom)
- Confidence scoring
- Translation history tracking
- Batch translation support

**Request**:
```json
{
  "text": "Hello, how are you?",
  "source_language": "english",
  "target_language": "hindi"
}
```

**Response**:
```json
{
  "translated_text": "नमस्ते, आप कैसे हैं?",
  "source_language": "english",
  "target_language": "hindi",
  "confidence_score": 0.95,
  "translation_method": "google"
}
```

### Frontend Display ✅ IMPLEMENTED

**Component**: `TranslateContent.tsx`

**UI Elements**:
- Dual-panel layout (source | target)
- Language selectors for both sides
- Swap languages button (⇄)
- Large text areas for input/output
- Translate button
- Copy translation button
- Character count for both sides
- Translation confidence indicator

**Visual Design**:
- Side-by-side panels with glass effect
- Source panel: periwinkle border
- Target panel: lavender border
- Floating globe icon for empty state
- Smooth fade-in for translations

---

## 3. SOCIAL MEDIA SCHEDULING 📅

### Backend API
**Endpoint**: `POST /api/social/schedule`

**Features**:
- Multi-platform support (Facebook, Instagram, Twitter, LinkedIn, YouTube, WhatsApp, Telegram)
- Scheduled posting with date/time
- Media attachment support
- Post status tracking (draft, scheduled, publishing, published, failed, cancelled)
- Engagement metrics (likes, comments, shares, views, reach, impressions)
- Retry mechanism for failed posts
- AWS EventBridge integration

**Request**:
```json
{
  "content": "Check out our new product!",
  "platform": "instagram",
  "scheduled_time": "2024-06-01T10:00:00",
  "media_urls": ["https://example.com/image.jpg"]
}
```

**Response**:
```json
{
  "id": 1,
  "status": "scheduled",
  "scheduled_time": "2024-06-01T10:00:00",
  "platform": "instagram"
}
```

### Frontend Display ✅ IMPLEMENTED

**Component**: `ScheduleContent.tsx`

**UI Elements**:
- Content textarea
- Platform selector (grid of icons)
- Date picker
- Time picker
- Media upload area
- Schedule button
- Scheduled posts list with:
  - Platform icon
  - Content preview
  - Date/time
  - Status badge
  - Edit/Delete buttons

**Visual Design**:
- Left panel: Scheduling form (40% width)
- Right panel: Scheduled posts list (60% width)
- Platform buttons with emoji icons
- Color-coded status badges
- Card-based post list with hover effects

---

## 4. ANALYTICS 📊

### Backend API
**Endpoint**: `GET /api/analytics/overview`

**Features**:
- User-specific analytics
- Content performance metrics
- Engagement tracking
- Platform-wise breakdown
- Time-series data
- ROI calculations
- Trend analysis

**Response**:
```json
{
  "total_content": 150,
  "total_posts": 89,
  "total_reach": 1250000,
  "total_engagement": 45000,
  "engagement_rate": 3.6,
  "top_platforms": ["instagram", "facebook"],
  "performance_by_language": {...},
  "recent_activity": [...]
}
```

### Frontend Display ⏳ NEEDS CONNECTION

**Component**: `AnalyticsContent.tsx`

**Recommended UI Elements**:
- KPI cards at top (4 columns):
  - Total Content Generated
  - Total Posts Scheduled
  - Total Reach
  - Average Engagement Rate
- Line chart: Engagement over time
- Bar chart: Performance by platform
- Pie chart: Content by language
- Table: Top performing posts
- Heatmap: Best posting times
- Export to PDF/CSV button

**Visual Design**:
- Grid layout with glass-effect cards
- Interactive charts (Chart.js or Recharts)
- Gradient backgrounds for charts
- Animated number counters
- Responsive grid (4 cols → 2 cols → 1 col)

---

## 5. VOICE INPUT 🎤

### Backend API
**Endpoint**: `POST /api/voice/transcribe`

**Features**:
- Audio file transcription
- Multi-language support
- Real-time processing
- Confidence scoring
- Speaker identification (future)
- Timestamp generation

**Request**:
```
FormData:
- audio_file: <file>
- language: "hindi"
```

**Response**:
```json
{
  "transcript": "Transcribed text...",
  "language": "hindi",
  "confidence": 0.92,
  "duration_seconds": 45
}
```

### Frontend Display ✅ IMPLEMENTED

**Component**: `VoiceContent.tsx`

**UI Elements**:
- Large microphone button (record/stop)
- Language selector
- Audio file upload input
- Recording indicator with animation
- Waveform visualization (7 bars)
- Transcript output panel
- Copy transcript button
- Generate content from transcript button

**Visual Design**:
- Left panel: Recording interface (centered)
- Right panel: Transcript display
- Pulsing animation during recording
- Concentric circles for recording state
- Floating microphone icon for empty state

---

## 6. USER MANAGEMENT 👤

### Backend API
**Endpoints**:
- `POST /api/users/register` - Create account
- `POST /api/users/login` - Authenticate
- `GET /api/users/profile` - Get user info
- `PUT /api/users/profile` - Update profile
- `GET /api/users/usage` - Usage statistics

**Features**:
- User roles (student, youtuber, business, teacher, startup)
- Subscription tiers (free, basic, pro, enterprise)
- Usage tracking (content generated, translations, posts scheduled)
- Preferred language setting
- Email verification
- AWS Cognito integration

**User Model**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "business",
  "subscription_tier": "pro",
  "preferred_language": "hindi",
  "content_generated_count": 150,
  "translations_count": 89,
  "posts_scheduled_count": 45
}
```

### Frontend Display ⏳ NEEDS FULL IMPLEMENTATION

**Component**: `ProfileContent.tsx`

**Recommended UI Elements**:

**Tab 1: Profile**
- Avatar upload
- Full name input
- Email (read-only)
- Username input
- Role selector
- Preferred language dropdown
- Save changes button

**Tab 2: Subscription**
- Current plan card
- Usage statistics:
  - Content generated (progress bar)
  - Translations (progress bar)
  - Posts scheduled (progress bar)
- Upgrade plan button
- Billing history table

**Tab 3: API Keys**
- List of API keys with:
  - Service name (Gemini, OpenAI, etc.)
  - Masked key display
  - Status indicator
  - Edit/Delete buttons
- Add new API key button

**Tab 4: Settings**
- Email notifications toggle
- Language preferences
- Theme selector
- Timezone selector
- Export data button
- Delete account button

**Visual Design**:
- Tabbed interface with glass effect
- Profile picture with gradient border
- Progress bars for usage limits
- Color-coded subscription tiers
- Confirmation modals for destructive actions

---

## 7. CAMPAIGN MANAGEMENT 🎯

### Backend API
**Endpoints**:
- `POST /api/campaigns/` - Create campaign
- `GET /api/campaigns/` - List campaigns
- `GET /api/campaigns/{id}` - Get campaign
- `PUT /api/campaigns/{id}` - Update campaign
- `PATCH /api/campaigns/{id}/metrics` - Update metrics
- `PATCH /api/campaigns/{id}/status` - Update status
- `PATCH /api/campaigns/{id}/approve` - Approve campaign
- `DELETE /api/campaigns/{id}` - Delete campaign
- `GET /api/campaigns/{id}/analytics` - Get analytics

**Features**:
- Campaign types (influencer, brand, product_launch, awareness, engagement, conversion)
- Status tracking (draft, active, paused, completed, cancelled)
- Budget management
- ROI calculation
- Target vs actual metrics
- Team collaboration
- Approval workflow
- Creator management

**Campaign Model**:
```json
{
  "id": 1,
  "name": "Summer Product Launch 2024",
  "campaign_type": "product_launch",
  "status": "active",
  "budget": 50000,
  "actual_reach": 850000,
  "target_reach": 1000000,
  "roi": 257.14,
  "start_date": "2024-06-01",
  "end_date": "2024-08-31",
  "creator_ids": [101, 102, 103],
  "platforms": ["instagram", "facebook", "twitter"]
}
```

### Frontend Display ✅ IMPLEMENTED

**Component**: `CampaignsContent.tsx`

**UI Elements**:

**Header Section**:
- Campaign selector (horizontal tabs)
- New Campaign button
- Stats cards (4 columns):
  - Budget (with spent %)
  - Reach (actual vs target)
  - ROI percentage
  - Creator count

**Kanban Board**:
- 5 columns (Outreach → Negotiating → Contracted → Content Creation → Completed)
- Draggable creator cards with:
  - Avatar
  - Name
  - Platform badge
  - Follower count
  - Engagement rate
  - Visual engagement bar
- Drag-and-drop between columns
- Column headers with count badges

**New Campaign Modal**:
- Campaign name input
- Description textarea
- Budget input
- Campaign type selector
- Date range picker
- Platform multi-select
- Create/Cancel buttons

**Visual Design**:
- Full-height layout with horizontal scrolling
- Glass-effect columns with gradient headers
- Platform-specific colors for creator cards
- Smooth drag animations
- Drop zone highlighting
- Staggered card entrance animations

---

## 8. AI MODEL CONFIGURATION ⚙️

### Backend API
**Endpoint**: `GET /api/models/config`

**Features**:
- List available AI models
- Model capabilities
- Pricing information
- Usage limits
- Performance metrics
- Model selection preferences

**Response**:
```json
{
  "models": [
    {
      "id": "gemini-pro",
      "name": "Google Gemini Pro",
      "provider": "google",
      "capabilities": ["text", "multimodal"],
      "cost_per_1k_tokens": 0.0005,
      "max_tokens": 32000,
      "is_available": true
    }
  ]
}
```

### Frontend Display ⏳ NOT YET IMPLEMENTED

**Recommended Component**: `ModelsContent.tsx`

**UI Elements**:
- Model cards grid (3 columns)
- Each card shows:
  - Provider logo
  - Model name
  - Capabilities badges
  - Pricing info
  - Performance rating
  - Enable/Disable toggle
  - Set as primary button
- Filter by provider
- Sort by price/performance
- Model comparison table

**Visual Design**:
- Card-based layout
- Provider-specific brand colors
- Toggle switches with animations
- Comparison mode with side-by-side view
- Performance charts (speed, quality, cost)

---

## SUMMARY TABLE

| Feature | Backend Status | Frontend Status | Priority |
|---------|---------------|-----------------|----------|
| Content Generation | ✅ Complete | ✅ Connected | High |
| Translation | ✅ Complete | ✅ Connected | High |
| Social Scheduling | ✅ Complete | ✅ Connected | High |
| Voice Input | ✅ Complete | ✅ Connected | Medium |
| Analytics | ✅ Complete | ⏳ UI Only | High |
| User Management | ✅ Complete | ⏳ Partial | High |
| Campaign Management | ✅ Complete | ✅ Connected | High |
| AI Model Config | ✅ Complete | ❌ Not Started | Low |

---

## RECOMMENDED IMPLEMENTATION ORDER

### Phase 1: Core Features (DONE ✅)
1. ✅ Content Generation
2. ✅ Translation
3. ✅ Social Scheduling
4. ✅ Voice Input
5. ✅ Campaign Kanban

### Phase 2: Analytics & Insights (NEXT)
1. ⏳ Connect Analytics to backend
2. ⏳ Add charts and visualizations
3. ⏳ Implement export functionality

### Phase 3: User Experience (NEXT)
1. ⏳ Complete Profile management
2. ⏳ Add authentication flow
3. ⏳ Implement subscription management
4. ⏳ Add API key management

### Phase 4: Advanced Features
1. ❌ AI Model configuration UI
2. ❌ Bulk operations
3. ❌ Advanced filtering
4. ❌ Collaboration features

---

## DESIGN SYSTEM

### Color Palette (Lavender Lullaby)
```css
--periwinkle: #B5C7EB
--cyan: #9EF0FF
--lavender: #A4A5F5
--purple: #8E70CF
```

### Component Patterns

**Glass Effect**:
```css
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.2);
```

**Gradient Buttons**:
```css
background: linear-gradient(135deg, #A4A5F5, #8E70CF);
box-shadow: 0 4px 15px rgba(164, 165, 245, 0.4);
```

**Card Hover**:
```css
transform: translateY(-8px) scale(1.02);
box-shadow: 0 20px 40px rgba(164, 165, 245, 0.3);
```

### Animation Library
- `slide-in-top` - Header entrance
- `fade-in` - Content appearance
- `flip-in-hor-bottom` - Card entrance
- `scale-in-center` - Modal entrance
- `floating` - Background elements
- `shimmer` - Text effects
- `pulsate` - Loading states

---

## API BASE URL

**Development**: `http://127.0.0.1:8000`
**Production**: `https://api.bharatcontentai.com` (to be configured)

All endpoints are prefixed with `/api/`

---

## AUTHENTICATION FLOW (TO BE IMPLEMENTED)

```
1. User visits site
   ↓
2. Redirected to /login
   ↓
3. POST /api/users/login
   ↓
4. Receive JWT token
   ↓
5. Store in localStorage
   ↓
6. Add to all API requests:
   Authorization: Bearer <token>
   ↓
7. Token expires → Refresh or re-login
```

---

## ERROR HANDLING PATTERN

All components should follow this pattern:

```typescript
try {
  setLoading(true)
  const response = await fetch(API_URL, options)
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  
  const data = await response.json()
  setData(data)
  
} catch (error) {
  console.error('Error:', error)
  setError('Failed to load data. Please try again.')
  
} finally {
  setLoading(false)
}
```

---

## RESPONSIVE BREAKPOINTS

```css
/* Mobile */
@media (max-width: 640px) { }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }
```

---

## PERFORMANCE OPTIMIZATION

1. **Lazy Loading**: Load components on demand
2. **Memoization**: Use React.memo for expensive components
3. **Debouncing**: Debounce API calls (300ms)
4. **Pagination**: Limit results to 20-50 per page
5. **Caching**: Cache API responses (5 minutes)
6. **Image Optimization**: Use Next.js Image component
7. **Code Splitting**: Split by route

---

## ACCESSIBILITY CHECKLIST

- [ ] Keyboard navigation for all interactive elements
- [ ] ARIA labels for icons and buttons
- [ ] Focus indicators visible
- [ ] Color contrast ratio ≥ 4.5:1
- [ ] Screen reader tested
- [ ] Form validation messages
- [ ] Error messages descriptive
- [ ] Loading states announced

---

This mapping provides a complete overview of all backend features and their frontend implementations!
