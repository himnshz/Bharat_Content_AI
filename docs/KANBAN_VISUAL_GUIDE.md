# Kanban Board Visual Guide

## Layout Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  Campaign Pipeline                              [+ New Campaign]     │
├─────────────────────────────────────────────────────────────────────┤
│  [Summer Launch 2024] [Holiday Campaign] [Q1 Awareness]             │
├─────────────────────────────────────────────────────────────────────┤
│  💰 Budget    👥 Reach      📈 ROI       📅 Creators                │
│  $50,000      850K          257%         8                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Outreach  │ │Negotiat..│ │Contract..│ │Content...│ │Completed │ │
│  │    2     │ │    2     │ │    1     │ │    2     │ │    1     │ │
│  ├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤ │
│  │          │ │          │ │          │ │          │ │          │ │
│  │ 👩‍💼 Sarah │ │ 👩‍🎨 Emma  │ │ 👩‍🔬 Lisa  │ │ 👨‍🚀 James │ │ 👨‍🏫 Tom   │ │
│  │ Johnson  │ │ Davis    │ │ Wang     │ │ Brown    │ │ Wilson   │ │
│  │ 📸 Insta │ │ 🎵 TikTok│ │ 🐦 Twitt │ │ 📺 YouTu │ │ 🎵 TikTok│ │
│  │ 125K     │ │ 210K     │ │ 98K      │ │ 175K     │ │ 203K     │ │
│  │ 4.2%     │ │ 5.1%     │ │ 3.9%     │ │ 4.8%     │ │ 5.2%     │ │
│  │ ████░░   │ │ █████░   │ │ ███░░░   │ │ ████░░   │ │ █████░   │ │
│  │          │ │          │ │          │ │          │ │          │ │
│  │ 👨‍💻 Mike  │ │ 👨‍🎤 Alex  │ │          │ │ 👩‍🎓 Nina  │ │          │ │
│  │ Chen     │ │ Kumar    │ │          │ │ Patel    │ │          │ │
│  │ 📺 YouTu │ │ 📸 Insta │ │          │ │ 📸 Insta │ │          │ │
│  │ 89K      │ │ 156K     │ │          │ │ 142K     │ │          │ │
│  │ 3.8%     │ │ 4.5%     │ │          │ │ 4.3%     │ │          │ │
│  │ ███░░░   │ │ ████░░   │ │          │ │ ████░░   │ │          │ │
│  │          │ │          │ │          │ │          │ │          │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Drag-and-Drop Flow

### Step 1: Initial State
```
Outreach          Negotiating
┌──────────┐     ┌──────────┐
│ 👩‍💼 Sarah │     │ 👩‍🎨 Emma  │
│ Johnson  │     │ Davis    │
└──────────┘     └──────────┘
```

### Step 2: User Clicks and Drags Sarah
```
Outreach          Negotiating
┌──────────┐     ┌──────────┐
│          │     │ 👩‍🎨 Emma  │
│  [drag]  │ →   │ Davis    │
└──────────┘     └──────────┘
     ↓
  👩‍💼 Sarah (dragging, rotated 3°, scaled 105%)
```

### Step 3: Hover Over Negotiating Column
```
Outreach          Negotiating (highlighted)
┌──────────┐     ┌──────────┐
│          │     │ 👩‍🎨 Emma  │
│          │     │ Davis    │
└──────────┘     │ [drop    │
                 │  zone]   │
                 └──────────┘
                      ↑
                  👩‍💼 Sarah
```

### Step 4: Drop Complete
```
Outreach          Negotiating
┌──────────┐     ┌──────────┐
│          │     │ 👩‍🎨 Emma  │
│          │     │ Davis    │
│          │     │          │
│          │     │ 👩‍💼 Sarah │
│          │     │ Johnson  │
└──────────┘     └──────────┘
```

## Creator Card Anatomy

```
┌─────────────────────────────────┐
│ 👩‍💼  Sarah Johnson              │  ← Avatar + Name
│     📸 Instagram                │  ← Platform Badge
├─────────────────────────────────┤
│ 👥 Followers        125K        │  ← Follower Count
│ 📈 Engagement       4.2%        │  ← Engagement Rate
├─────────────────────────────────┤
│ ████████░░░░░░░░░░░░░░░░░░░░   │  ← Visual Engagement Bar
└─────────────────────────────────┘
```

## Platform Badges

```
Instagram:  📸  [Pink → Purple gradient]
YouTube:    📺  [Red gradient]
TikTok:     🎵  [Cyan → Blue gradient]
Twitter:    🐦  [Blue gradient]
```

## Campaign Stats Cards

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ 💰 Budget   │  │ 👥 Reach    │  │ 📈 ROI      │  │ 📅 Creators │
│             │  │             │  │             │  │             │
│   $50,000   │  │    850K     │  │   257.1%    │  │      8      │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

## Color Scheme (Lavender Lullaby)

```
Pipeline Stage Colors:
┌──────────────────────────────────────┐
│ Outreach:         Periwinkle → Cyan  │
│ Negotiating:      Cyan → Lavender    │
│ Contracted:       Lavender → Purple  │
│ Content Creation: Purple → Periwinkle│
│ Completed:        Cyan → Periwinkle  │
└──────────────────────────────────────┘

Base Colors:
• Periwinkle: #B5C7EB
• Cyan:       #9EF0FF
• Lavender:   #A4A5F5
• Purple:     #8E70CF
```

## Interaction States

### Normal State
```
┌─────────────────┐
│ 👩‍💼 Sarah       │  opacity: 1
│ Johnson         │  scale: 1
│ 📸 Instagram    │  border: white/20
└─────────────────┘
```

### Hover State
```
┌─────────────────┐
│ 👩‍💼 Sarah       │  scale: 1.02
│ Johnson         │  translateY: -8px
│ 📸 Instagram    │  border: lavender/50
└─────────────────┘  shadow: enhanced
```

### Dragging State
```
  👩‍💼 Sarah          opacity: 0.5 (original)
  Johnson           rotate: 3deg
  📸 Instagram      scale: 1.05
                    shadow: 2xl
                    border: lavender
```

### Drop Zone Active
```
┌─────────────────┐
│                 │  bg: lavender/20
│   Drop Here     │  border: lavender
│                 │  (pulsing)
└─────────────────┘
```

## Mobile View

```
┌─────────────────────┐
│ ☰  Campaign Pipeline│
├─────────────────────┤
│ [Summer Launch]     │
├─────────────────────┤
│ Stats (2x2 grid)    │
├─────────────────────┤
│                     │
│ ← Swipe to scroll → │
│                     │
│ [Outreach]          │
│ [Negotiating]       │
│ [Contracted]        │
│ ...                 │
│                     │
└─────────────────────┘
```

## Animations

### Card Entrance
```
Frame 1:  opacity: 0, rotateX: 80deg
Frame 2:  opacity: 0.5, rotateX: 40deg
Frame 3:  opacity: 1, rotateX: 0deg
Duration: 0.5s
Delay:    index * 0.05s (staggered)
```

### Drag Start
```
Scale:    1 → 1.05
Rotate:   0deg → 3deg
Shadow:   normal → 2xl
Duration: 0.2s
```

### Drop Animation
```
Scale:    1.05 → 1
Rotate:   3deg → 0deg
Opacity:  0.5 → 1
Duration: 0.3s
Easing:   cubic-bezier(0.4, 0, 0.2, 1)
```

## API Integration Points

```
┌─────────────────────────────────────┐
│ Component Lifecycle                 │
├─────────────────────────────────────┤
│                                     │
│ 1. Mount                            │
│    ↓                                │
│ 2. fetchCampaigns()                 │
│    GET /api/campaigns/              │
│    ↓                                │
│ 3. Display campaigns                │
│    ↓                                │
│ 4. User selects campaign            │
│    ↓                                │
│ 5. Display creators (mock data)     │
│    ↓                                │
│ 6. User drags creator               │
│    ↓                                │
│ 7. Update local state               │
│    ↓                                │
│ 8. [Future] PATCH /api/creators/    │
│                                     │
└─────────────────────────────────────┘
```

## Keyboard Shortcuts (Future)

```
Space:     Pick up / Drop creator
Arrow Keys: Move between columns
Enter:     Open creator details
Esc:       Cancel drag
Tab:       Navigate between creators
```

## Accessibility Features

```
✓ Keyboard navigation
✓ Screen reader support
✓ Focus indicators
✓ ARIA labels
✓ Touch-friendly targets (min 44x44px)
✓ High contrast mode support
```

This visual guide shows the complete Kanban board layout and interactions!
