# 🎨 Frontend Requirements - Bharat Content AI

## 📋 Overview

Modern, responsive web application for multilingual content creation targeting Indian audiences (students, YouTubers, businesses, teachers, startups).

**Tech Stack Recommendation:**
- **Framework:** Next.js 14+ (React) with App Router
- **Styling:** Tailwind CSS + shadcn/ui components
- **Animations:** Framer Motion
- **State Management:** Zustand or React Context
- **API Client:** Axios or TanStack Query
- **Icons:** Lucide React or Heroicons
- **Charts:** Recharts or Chart.js

---

## 🎯 Core Pages & Features

### 1. Landing Page / Home
**Purpose:** Welcome users, showcase features, drive sign-ups

**Components:**
- Hero section with animated gradient background
- Feature cards with hover effects
- Language selector showcase
- Testimonials carousel
- CTA buttons with pulse animations
- Footer with links

**Animations:**
- Fade-in on scroll (stagger effect)
- Floating elements (subtle)
- Gradient background animation
- Button hover scale + glow
- Card lift on hover

---

### 2. Authentication Pages

#### Login Page
**Components:**
- Email/password form
- Social login buttons (Google, Facebook)
- "Remember me" checkbox
- Forgot password link
- Sign up redirect

**Animations:**
- Form slide-in from right
- Input focus glow effect
- Button ripple on click
- Error shake animation
- Success checkmark animation

#### Registration Page
**Components:**
- Multi-step form (3 steps)
  - Step 1: Basic info (email, username, password)
  - Step 2: Profile (name, role, language preference)
  - Step 3: Confirmation
- Progress indicator
- Role selection cards
- Language dropdown with flags

**Animations:**
- Step transition slide
- Progress bar fill animation
- Card selection scale + border glow
- Success confetti animation

---

### 3. Dashboard (Main Hub)

**Layout:**
- Sidebar navigation (collapsible)
- Top bar (user menu, notifications, search)
- Main content area
- Quick action floating button

**Widgets:**
1. **Stats Cards** (animated counters)
   - Total content generated
   - Posts scheduled
   - Translations made
   - Engagement rate

2. **Recent Activity Feed**
   - Timeline with icons
   - Slide-in animation

3. **Quick Actions**
   - Generate Content (primary button)
   - Schedule Post
   - Translate Content
   - View Analytics

4. **Upcoming Posts Calendar**
   - Mini calendar view
   - Hover tooltips

**Animations:**
- Sidebar slide-in/out
- Stats counter animation (count-up)
- Card stagger fade-in
- Skeleton loading states
- Notification badge pulse

---

### 4. Content Generator Page

**Layout:**
- Split view: Input (left) | Preview (right)
- Floating toolbar

**Components:**

#### Input Section
- **Prompt Textarea**
  - Auto-resize
  - Character counter
  - Voice input button (mic icon)
  - AI suggestions dropdown

- **Configuration Panel**
  - Language selector (dropdown with flags)
  - Tone selector (pills/chips)
  - Content type selector (cards)
  - Advanced options (collapsible)

- **Generate Button**
  - Large, prominent
  - Loading spinner animation
  - Success pulse

#### Preview Section
- **Generated Content Display**
  - Typewriter animation (optional)
  - Editable text area
  - Word count
  - Reading time estimate

- **Action Buttons**
  - Copy to clipboard (with toast)
  - Regenerate
  - Save draft
  - Translate
  - Schedule post

**Animations:**
- Prompt input focus expand
- Configuration panel slide-down
- Generate button: loading dots → success checkmark
- Content typewriter effect (optional)
- Preview fade-in
- Button hover glow
- Toast notifications slide-in

**Loading States:**
- Skeleton loader for preview
- Animated dots "Generating content..."
- Progress bar (if long generation)

---

### 5. Translation Page

**Layout:**
- Two-column layout: Source | Target
- Language swap button in center

**Components:**

#### Source Panel
- Text input/paste area
- Language detector badge
- Character count

#### Target Panel
- Translated text display
- Multiple language tabs
- Download options

#### Controls
- **Language Selectors**
  - Dropdown with search
  - Flag icons
  - Popular languages pinned

- **Batch Translation**
  - Multi-select languages
  - Progress indicators

- **Options**
  - Maintain tone toggle
  - Cultural adaptation toggle

**Animations:**
- Language swap flip animation
- Translation progress bar
- Text fade-in on translation
- Tab switch slide
- Success checkmark

---

### 6. Social Media Scheduler

**Layout:**
- Calendar view (default)
- List view (alternative)
- Post composer modal

**Components:**

#### Calendar View
- Month/week/day views
- Drag-and-drop posts
- Color-coded by platform
- Hover preview cards

#### Post Composer
- **Platform Selector**
  - Icon buttons (multi-select)
  - Platform-specific previews

- **Content Input**
  - Rich text editor
  - Media upload (drag-drop)
  - Emoji picker
  - Hashtag suggestions

- **Scheduling**
  - Date/time picker
  - Timezone selector
  - Best time suggestions

- **Preview Cards**
  - Platform-specific mockups
  - Character limits
  - Image previews

**Animations:**
- Calendar events fade-in
- Drag-and-drop ghost element
- Modal slide-up
- Platform icon bounce on select
- Media upload progress
- Schedule success animation

---

### 7. Analytics Dashboard

**Layout:**
- Grid of charts and metrics
- Date range selector
- Export button

**Components:**

#### Metrics Cards
- Total views (with trend arrow)
- Engagement rate (circular progress)
- Top performing content
- Language distribution

#### Charts
1. **Engagement Trends** (Line chart)
   - Animated line draw
   - Hover tooltips
   - Zoom/pan

2. **Platform Performance** (Bar chart)
   - Animated bars grow
   - Color-coded

3. **Content Type Distribution** (Pie/Donut chart)
   - Animated segments
   - Interactive legend

4. **Language Usage** (Horizontal bar)
   - Animated fill
   - Percentage labels

#### Top Content List
- Thumbnail previews
- Engagement metrics
- Platform badges
- Click to view details

**Animations:**
- Chart draw-in animations
- Counter animations
- Card hover lift
- Tooltip fade-in
- Data refresh pulse

---

### 8. Voice Input Page

**Layout:**
- Centered recording interface
- Waveform visualization
- Transcription display

**Components:**

#### Recording Interface
- **Microphone Button**
  - Large circular button
  - Pulse animation when recording
  - Color change (idle → recording → processing)

- **Waveform Visualizer**
  - Real-time audio bars
  - Animated waves

- **Controls**
  - Start/stop recording
  - Pause/resume
  - Cancel
  - Language selector

#### Transcription Display
- **Text Output**
  - Appears word-by-word
  - Editable
  - Confidence indicators

- **Actions**
  - Use for content generation
  - Save transcription
  - Download audio

**Animations:**
- Mic button pulse (recording)
- Waveform bars animation
- Text appear word-by-word
- Processing spinner
- Success checkmark

---

### 9. User Profile & Settings

**Layout:**
- Tabbed interface
- Sidebar menu

**Tabs:**

#### Profile
- Avatar upload (with crop)
- Name, email, username
- Role badge
- Subscription tier

#### Preferences
- Default language
- Default tone
- Timezone
- Notification settings

#### Subscription
- Current plan card
- Usage statistics
- Upgrade options
- Billing history

#### API Keys
- Service status indicators
- Add/remove keys
- Test connection buttons

**Animations:**
- Tab switch slide
- Avatar upload preview
- Toggle switch animations
- Plan card hover scale
- Success/error toasts

---

## 🎨 Design System

### Color Palette

#### Primary Colors
```css
--primary-50: #eff6ff;
--primary-100: #dbeafe;
--primary-500: #3b82f6;  /* Main brand color */
--primary-600: #2563eb;
--primary-700: #1d4ed8;
```

#### Secondary Colors
```css
--secondary-500: #8b5cf6;  /* Purple accent */
--accent-500: #f59e0b;     /* Orange for CTAs */
```

#### Semantic Colors
```css
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;
```

#### Neutral Colors
```css
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-500: #6b7280;
--gray-900: #111827;
```

#### Dark Mode
```css
--dark-bg: #0f172a;
--dark-surface: #1e293b;
--dark-border: #334155;
```

### Typography

#### Font Families
```css
--font-sans: 'Inter', system-ui, sans-serif;
--font-display: 'Poppins', sans-serif;  /* For headings */
--font-mono: 'JetBrains Mono', monospace;
```

#### Font Sizes
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

### Spacing
```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
```

### Border Radius
```css
--radius-sm: 0.25rem;   /* 4px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 0.75rem;   /* 12px */
--radius-xl: 1rem;      /* 16px */
--radius-full: 9999px;  /* Circular */
```

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
```

---

## 🎭 Animation Guidelines

### Timing Functions
```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Duration
```css
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
```

### Common Animations

#### Button Hover
```css
.button {
  transition: all 200ms ease-out;
}
.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
```

#### Card Hover
```css
.card {
  transition: transform 300ms ease-out;
}
.card:hover {
  transform: scale(1.02);
}
```

#### Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

#### Slide In
```css
@keyframes slideIn {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}
```

#### Pulse
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

#### Spin
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

---

## 🧩 Component Library

### Buttons

#### Primary Button
```jsx
<button className="
  px-6 py-3 
  bg-primary-500 hover:bg-primary-600 
  text-white font-medium rounded-lg
  transition-all duration-200
  hover:scale-105 hover:shadow-lg
  active:scale-95
">
  Generate Content
</button>
```

#### Secondary Button
```jsx
<button className="
  px-6 py-3 
  bg-white border-2 border-gray-300
  hover:border-primary-500 hover:text-primary-500
  text-gray-700 font-medium rounded-lg
  transition-all duration-200
">
  Cancel
</button>
```

#### Icon Button
```jsx
<button className="
  p-3 rounded-full
  bg-gray-100 hover:bg-gray-200
  transition-all duration-200
  hover:scale-110
">
  <Icon className="w-5 h-5" />
</button>
```

### Input Fields

#### Text Input
```jsx
<input className="
  w-full px-4 py-3
  border-2 border-gray-300 rounded-lg
  focus:border-primary-500 focus:ring-4 focus:ring-primary-100
  transition-all duration-200
  outline-none
" />
```

#### Textarea
```jsx
<textarea className="
  w-full px-4 py-3
  border-2 border-gray-300 rounded-lg
  focus:border-primary-500 focus:ring-4 focus:ring-primary-100
  transition-all duration-200
  outline-none resize-none
  min-h-[200px]
" />
```

### Cards

#### Basic Card
```jsx
<div className="
  p-6 bg-white rounded-xl shadow-md
  hover:shadow-xl transition-shadow duration-300
  border border-gray-100
">
  {/* Content */}
</div>
```

#### Interactive Card
```jsx
<div className="
  p-6 bg-white rounded-xl shadow-md
  hover:shadow-xl hover:scale-102
  transition-all duration-300
  cursor-pointer border border-gray-100
  hover:border-primary-500
">
  {/* Content */}
</div>
```

### Modals

```jsx
<div className="
  fixed inset-0 z-50
  flex items-center justify-center
  bg-black/50 backdrop-blur-sm
  animate-fadeIn
">
  <div className="
    bg-white rounded-2xl shadow-2xl
    max-w-2xl w-full mx-4
    animate-slideUp
  ">
    {/* Modal content */}
  </div>
</div>
```

### Toasts/Notifications

```jsx
<div className="
  fixed top-4 right-4 z-50
  px-6 py-4 bg-white rounded-lg shadow-lg
  border-l-4 border-success
  animate-slideInRight
">
  <div className="flex items-center gap-3">
    <CheckIcon className="w-5 h-5 text-success" />
    <p className="font-medium">Content generated successfully!</p>
  </div>
</div>
```

### Loading States

#### Spinner
```jsx
<div className="
  w-8 h-8 border-4 border-gray-200
  border-t-primary-500 rounded-full
  animate-spin
" />
```

#### Skeleton
```jsx
<div className="
  h-4 bg-gray-200 rounded
  animate-pulse
" />
```

#### Progress Bar
```jsx
<div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
  <div className="
    h-full bg-primary-500
    transition-all duration-300
    animate-shimmer
  " style={{width: `${progress}%`}} />
</div>
```

---

## 📱 Responsive Design

### Breakpoints
```css
--screen-sm: 640px;   /* Mobile landscape */
--screen-md: 768px;   /* Tablet */
--screen-lg: 1024px;  /* Desktop */
--screen-xl: 1280px;  /* Large desktop */
--screen-2xl: 1536px; /* Extra large */
```

### Mobile-First Approach
- Design for mobile first
- Progressive enhancement for larger screens
- Touch-friendly targets (min 44x44px)
- Collapsible navigation
- Bottom navigation bar on mobile

---

## ♿ Accessibility

### Requirements
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader friendly
- Focus indicators
- Alt text for images
- ARIA labels
- Color contrast ratios (4.5:1 minimum)

### Implementation
```jsx
// Example: Accessible button
<button
  aria-label="Generate content"
  aria-pressed={isGenerating}
  disabled={isGenerating}
  className="..."
>
  {isGenerating ? 'Generating...' : 'Generate'}
</button>
```

---

## 🌐 Internationalization (i18n)

### Supported Languages
- English (default)
- Hindi
- Tamil
- Telugu
- Bengali
- Marathi
- Gujarati
- Kannada
- Malayalam
- Punjabi
- Odia

### Implementation
- Use next-i18next or react-i18next
- RTL support for applicable languages
- Date/time localization
- Number formatting
- Currency formatting

---

## 🚀 Performance Optimization

### Best Practices
1. **Code Splitting**
   - Route-based splitting
   - Component lazy loading
   - Dynamic imports

2. **Image Optimization**
   - Next.js Image component
   - WebP format
   - Lazy loading
   - Responsive images

3. **Caching**
   - API response caching
   - Static asset caching
   - Service worker (PWA)

4. **Bundle Size**
   - Tree shaking
   - Minimize dependencies
   - Code minification

---

## 📦 Recommended Libraries

### UI Components
```json
{
  "shadcn/ui": "Latest",
  "radix-ui": "Latest",
  "headlessui": "Latest"
}
```

### Animations
```json
{
  "framer-motion": "^10.0.0",
  "react-spring": "^9.7.0",
  "lottie-react": "^2.4.0"
}
```

### Forms
```json
{
  "react-hook-form": "^7.48.0",
  "zod": "^3.22.0",
  "@hookform/resolvers": "^3.3.0"
}
```

### Data Fetching
```json
{
  "@tanstack/react-query": "^5.0.0",
  "axios": "^1.6.0"
}
```

### Charts
```json
{
  "recharts": "^2.10.0",
  "chart.js": "^4.4.0",
  "react-chartjs-2": "^5.2.0"
}
```

### Utilities
```json
{
  "date-fns": "^2.30.0",
  "clsx": "^2.0.0",
  "tailwind-merge": "^2.0.0"
}
```

---

## 🎯 User Flows

### Content Generation Flow
```
1. User clicks "Generate Content"
2. Modal/page opens with form
3. User enters prompt
4. User selects language, tone, type
5. User clicks "Generate"
6. Loading animation shows
7. Content appears with typewriter effect
8. User can edit, save, or schedule
```

### Post Scheduling Flow
```
1. User navigates to scheduler
2. Clicks on calendar date/time
3. Composer modal opens
4. User selects platforms
5. User enters/pastes content
6. User uploads media (optional)
7. User sets schedule time
8. Preview shows for each platform
9. User clicks "Schedule"
10. Success animation + confirmation
```

---

## 📊 Key Metrics to Track

### User Engagement
- Time on page
- Click-through rates
- Feature usage
- Conversion rates

### Performance
- Page load time
- Time to interactive
- First contentful paint
- Largest contentful paint

---

## 🎨 Design Inspiration

### Reference Sites
- Linear.app (clean, modern UI)
- Notion (intuitive interface)
- Vercel (smooth animations)
- Stripe (excellent UX)
- Figma (collaborative features)

### Design Resources
- **Icons:** Lucide, Heroicons, Phosphor
- **Illustrations:** unDraw, Storyset
- **Animations:** LottieFiles
- **Gradients:** Mesh Gradients, CSS Gradient

---

## ✅ Implementation Checklist

### Phase 1: Core Pages
- [ ] Landing page
- [ ] Authentication (login/register)
- [ ] Dashboard
- [ ] Content generator
- [ ] Basic navigation

### Phase 2: Features
- [ ] Translation page
- [ ] Social media scheduler
- [ ] Analytics dashboard
- [ ] Voice input
- [ ] User profile

### Phase 3: Polish
- [ ] Animations
- [ ] Dark mode
- [ ] Mobile optimization
- [ ] Accessibility
- [ ] Performance optimization

### Phase 4: Advanced
- [ ] PWA features
- [ ] Offline support
- [ ] Real-time updates
- [ ] Advanced analytics
- [ ] A/B testing

---

**This frontend will provide a modern, engaging, and accessible experience for your users!** 🚀
