# 🎨 Frontend Implementation Guide - Bharat Content AI

## 📋 Overview

Professional, techy frontend with **Lavender Lullaby** color theme and stunning 3D animations using Three.js and Animista.

---

## 🎨 Color Theme: Lavender Lullaby

```css
Periwinkle: #B5C7EB (Soft blue)
Cyan:       #9EF0FF (Bright cyan)
Lavender:   #A4A5F5 (Main lavender)
Purple:     #8E70CF (Deep purple)

Gradient: linear-gradient(135deg, #B5C7EB 0%, #9EF0FF 25%, #A4A5F5 50%, #8E70CF 100%)
```

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Hero3D.tsx      # 3D animated hero with Three.js
│   │   ├── Header.js
│   │   ├── Sidebar.js
│   │   ├── ContentEditor.js
│   │   ├── LanguageSelector.js
│   │   └── VoiceInput.js
│   │
│   ├── pages/              # Next.js pages
│   │   ├── index.js        # Landing page
│   │   ├── content-generator.js
│   │   ├── translator.js
│   │   ├── scheduler.js
│   │   ├── analytics.js
│   │   └── _app.js
│   │
│   ├── services/           # API services
│   │   ├── api.service.ts  # Complete API client
│   │   └── auth.service.ts # Authentication service
│   │
│   ├── config/             # Configuration
│   │   └── api.config.ts   # API endpoints & constants
│   │
│   ├── store/              # State management
│   │   └── useStore.ts     # Zustand stores
│   │
│   ├── utils/              # Utilities
│   │   └── helpers.ts      # Helper functions
│   │
│   └── styles/             # Styles
│       └── globals.css     # Global styles + Animista animations
│
├── package.json            # Dependencies
├── tailwind.config.js      # Tailwind configuration
├── tsconfig.json           # TypeScript configuration
├── next.config.js          # Next.js configuration
└── postcss.config.js       # PostCSS configuration
```

---

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Visit: http://localhost:3000

---

## 🎭 Features Implemented

### ✅ Configuration & Services

1. **API Configuration** (`src/config/api.config.ts`)
   - All 53 backend endpoints mapped
   - Supported languages (11 Indian languages)
   - Content types, tones, platforms
   - Translation methods

2. **API Service** (`src/services/api.service.ts`)
   - Complete HTTP client with Axios
   - Token management & refresh
   - Request/response interceptors
   - All backend API methods:
     - Content generation
     - Translation
     - Social media scheduling
     - Analytics
     - Voice input
     - User management

3. **Auth Service** (`src/services/auth.service.ts`)
   - User authentication
   - Session management
   - Profile management
   - Token handling

4. **State Management** (`src/store/useStore.ts`)
   - User state (Zustand + persist)
   - Content state
   - UI state (sidebar, theme, notifications)
   - Translation state
   - Social media state
   - Analytics state

5. **Utilities** (`src/utils/helpers.ts`)
   - 30+ helper functions
   - Date formatting
   - Text manipulation
   - Clipboard operations
   - File operations
   - Validation functions

### ✅ Styling & Animations

1. **Tailwind Configuration**
   - Lavender Lullaby color palette
   - Custom animations
   - Responsive breakpoints
   - Custom utilities

2. **Global Styles** (`src/styles/globals.css`)
   - 15+ Animista animations:
     - slide-in-top/bottom
     - scale-in-center
     - bounce-in-top
     - pulsate-fwd
     - rotate-in-center
     - flip-in-hor-bottom
     - swing-in-top-fwd
     - fade-in
     - text-focus-in
     - tracking-in-expand
     - glow
     - shimmer
   - Custom utility classes
   - Gradient text effects
   - Glass morphism effects
   - Custom scrollbar

3. **3D Hero Component** (`src/components/Hero3D.tsx`)
   - Three.js integration
   - Animated distorted sphere
   - Particle system (500 particles)
   - Floating rings
   - Auto-rotating camera
   - Dynamic lighting

---

## 🎨 Animation Classes (Animista)

### Usage Examples

```jsx
// Slide in from top
<div className="slide-in-top">Content</div>

// Bounce in
<div className="bounce-in-top">Content</div>

// Scale in
<div className="scale-in-center">Content</div>

// Pulsate
<button className="pulsate-fwd">Click me</button>

// Glow effect
<div className="glow">Glowing content</div>

// Shimmer effect
<div className="shimmer">Loading...</div>

// Text focus
<h1 className="text-focus-in">Title</h1>

// Gradient text
<h1 className="gradient-text">Gradient Title</h1>

// Glass effect
<div className="glass-effect">Glass card</div>

// Card hover
<div className="card-hover">Hover me</div>
```

---

## 🎯 API Integration Examples

### Content Generation

```typescript
import { apiService } from '@/services/api.service'

// Generate content
const result = await apiService.generateContent({
  prompt: "Create a social media post about AI",
  language: "hindi",
  tone: "casual",
  content_type: "social_post",
  user_id: 1
})

// List content
const content = await apiService.listContent({
  user_id: 1,
  skip: 0,
  limit: 20
})

// Summarize content
const summary = await apiService.summarizeContent(contentId, 100)
```

### Translation

```typescript
// Translate text
const translation = await apiService.translateContent({
  text: "Hello, how are you?",
  source_language: "en",
  target_language: "hi",
  maintain_tone: true
})

// Batch translate
const translations = await apiService.batchTranslate({
  text: "Hello world",
  source_language: "en",
  target_languages: ["hi", "ta", "te"]
})

// Get supported languages
const languages = await apiService.getSupportedLanguages()
```

### Social Media

```typescript
// Schedule post
const scheduled = await apiService.schedulePost({
  content_id: 1,
  platforms: ["twitter", "facebook"],
  scheduled_time: "2024-03-15T10:00:00Z",
  user_id: 1
})

// Get scheduled posts
const posts = await apiService.getScheduledPosts(userId)

// Publish immediately
const published = await apiService.publishPost({
  content_id: 1,
  platforms: ["twitter"],
  user_id: 1
})
```

### Analytics

```typescript
// Get overview
const overview = await apiService.getAnalyticsOverview(userId, 30)

// Get engagement metrics
const engagement = await apiService.getEngagementMetrics(
  userId,
  "2024-01-01",
  "2024-03-01"
)

// Get content performance
const performance = await apiService.getContentPerformance(userId, 10)
```

### Voice Input

```typescript
// Process voice input
const formData = new FormData()
formData.append('audio_file', audioFile)

const result = await apiService.processVoiceInput({
  audio_file: audioFile,
  language: "hi",
  user_id: 1,
  generate_content: true
})
```

### Authentication

```typescript
import { authService } from '@/services/auth.service'

// Register
const user = await authService.register({
  username: "john_doe",
  email: "john@example.com",
  password: "securepass123",
  full_name: "John Doe"
})

// Login
const response = await authService.login("john_doe", "securepass123")

// Get current user
const currentUser = authService.getCurrentUser()

// Update profile
const updated = await authService.updateProfile({
  full_name: "John Smith",
  preferred_language: "hi"
})

// Logout
await authService.logout()
```

---

## 🎨 State Management Examples

### User Store

```typescript
import { useUserStore } from '@/store/useStore'

function Component() {
  const { user, isAuthenticated, setUser, clearUser } = useUserStore()
  
  // Use user data
  if (isAuthenticated) {
    console.log(user.username)
  }
}
```

### Content Store

```typescript
import { useContentStore } from '@/store/useStore'

function Component() {
  const { contentList, addContent, updateContent } = useContentStore()
  
  // Add new content
  addContent(newContent)
  
  // Update content
  updateContent(contentId, { status: 'published' })
}
```

### UI Store

```typescript
import { useUIStore } from '@/store/useStore'

function Component() {
  const { showNotification, setLoading } = useUIStore()
  
  // Show notification
  showNotification('Content generated successfully!', 'success')
  
  // Set loading state
  setLoading(true)
}
```

---

## 🛠️ Utility Functions Examples

```typescript
import { 
  formatDate, 
  countWords, 
  copyToClipboard,
  formatNumber,
  getLanguageName 
} from '@/utils/helpers'

// Format date
const formatted = formatDate(new Date(), 'PPP')

// Count words
const wordCount = countWords(text)

// Copy to clipboard
await copyToClipboard(text)

// Format number
const formatted = formatNumber(1234567) // "1,234,567"

// Get language name
const name = getLanguageName('hi') // "Hindi"
```

---

## 🎯 Next Steps

### Phase 1: Core Pages (Priority)

1. **Landing Page** (`pages/index.tsx`)
   - Hero section with 3D animation
   - Feature showcase
   - CTA buttons
   - Language selector

2. **Authentication Pages**
   - Login page
   - Registration page
   - Password reset

3. **Dashboard** (`pages/dashboard.tsx`)
   - Stats cards
   - Recent activity
   - Quick actions
   - Upcoming posts

4. **Content Generator** (`pages/content-generator.tsx`)
   - Prompt input
   - Configuration panel
   - Preview section
   - Action buttons

### Phase 2: Features

5. **Translation Page** (`pages/translator.tsx`)
6. **Social Media Scheduler** (`pages/scheduler.tsx`)
7. **Analytics Dashboard** (`pages/analytics.tsx`)
8. **Voice Input Page** (`pages/voice-input.tsx`)
9. **User Profile** (`pages/profile.tsx`)

### Phase 3: Components

10. Create reusable components:
    - Button
    - Input
    - Card
    - Modal
    - Toast
    - Dropdown
    - Tabs
    - Loading states

---

## 📦 Dependencies Installed

```json
{
  "next": "^14.2.0",
  "react": "^18.2.0",
  "@react-three/fiber": "^8.15.0",
  "@react-three/drei": "^9.96.0",
  "three": "^0.161.0",
  "framer-motion": "^11.0.0",
  "axios": "^1.6.0",
  "@tanstack/react-query": "^5.17.0",
  "zustand": "^4.5.0",
  "lucide-react": "^0.323.0",
  "tailwindcss": "^3.4.0",
  "typescript": "^5.3.0"
}
```

---

## 🎨 Design System

### Colors
- Primary: #A4A5F5 (Lavender)
- Secondary: #8E70CF (Purple)
- Accent: #9EF0FF (Cyan)
- Background: #B5C7EB (Periwinkle)

### Typography
- Font: Inter (body), Poppins (headings)
- Sizes: xs, sm, base, lg, xl, 2xl, 3xl, 4xl

### Spacing
- Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px

### Animations
- Duration: 150ms (fast), 300ms (normal), 500ms (slow)
- Easing: ease-out, ease-in-out, bounce

---

## ✅ What's Complete

- ✅ Project configuration (Next.js, TypeScript, Tailwind)
- ✅ API configuration with all 53 endpoints
- ✅ Complete API service with authentication
- ✅ Auth service with session management
- ✅ State management (6 stores)
- ✅ 30+ utility functions
- ✅ Lavender Lullaby theme
- ✅ 15+ Animista animations
- ✅ 3D Hero component with Three.js
- ✅ Responsive design system
- ✅ Custom Tailwind configuration

---

## 🚀 Ready to Build!

All configuration, services, and utilities are ready. Now you can:

1. Run `npm install` in the frontend directory
2. Create the page components
3. Build the UI with the provided animations
4. Connect to the backend API using the services

The foundation is solid and professional! 🎉

