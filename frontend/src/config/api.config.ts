/**
 * API Configuration
 * Maps to backend FastAPI endpoints
 */

export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  TIMEOUT: 30000,
  
  // API Endpoints
  ENDPOINTS: {
    // Content Generation
    CONTENT: {
      GENERATE: '/api/content/generate',
      LIST: '/api/content/list',
      GET: (id: number) => `/api/content/${id}`,
      EDIT: (id: number) => `/api/content/${id}/edit`,
      SUMMARIZE: '/api/content/summarize',
      DELETE: (id: number) => `/api/content/${id}`,
      AI_SERVICES_STATUS: '/api/content/ai-services/status',
    },
    
    // Translation
    TRANSLATION: {
      TRANSLATE: '/api/translation/translate',
      BATCH_TRANSLATE: '/api/translation/batch',
      SUPPORTED_LANGUAGES: '/api/translation/languages/supported',
      DETECT_LANGUAGE: '/api/translation/detect',
      HISTORY: '/api/translation/history',
      GET: (id: number) => `/api/translation/${id}`,
      DELETE: (id: number) => `/api/translation/${id}`,
    },
    
    // Social Media
    SOCIAL: {
      CONNECT: '/api/social/connect',
      DISCONNECT: (platform: string) => `/api/social/disconnect/${platform}`,
      ACCOUNTS: '/api/social/accounts',
      SCHEDULE: '/api/social/schedule',
      SCHEDULED_POSTS: '/api/social/scheduled',
      PUBLISH: '/api/social/publish',
      UPDATE_POST: (id: number) => `/api/social/scheduled/${id}`,
      DELETE_POST: (id: number) => `/api/social/scheduled/${id}`,
      PLATFORMS: '/api/social/platforms',
      CALENDAR: '/api/social/calendar',
    },
    
    // Analytics
    ANALYTICS: {
      OVERVIEW: '/api/analytics/overview',
      ENGAGEMENT: '/api/analytics/engagement',
      CONTENT_PERFORMANCE: '/api/analytics/content-performance',
      PLATFORM_STATS: '/api/analytics/platform-stats',
      LANGUAGE_DISTRIBUTION: '/api/analytics/language-distribution',
      TRENDS: '/api/analytics/trends',
      EXPORT: '/api/analytics/export',
    },
    
    // Voice Input
    VOICE: {
      TRANSCRIBE: '/api/voice/transcribe',
      PROCESS: '/api/voice/process',
      HISTORY: '/api/voice/history',
      GET: (id: number) => `/api/voice/${id}`,
      DELETE: (id: number) => `/api/voice/${id}`,
      SUPPORTED_LANGUAGES: '/api/voice/languages',
    },
    
    // User Management
    USERS: {
      REGISTER: '/api/users/register',
      LOGIN: '/api/users/login',
      PROFILE: '/api/users/profile',
      UPDATE_PROFILE: '/api/users/profile',
      CHANGE_PASSWORD: '/api/users/change-password',
      PREFERENCES: '/api/users/preferences',
      STATS: '/api/users/stats',
      DELETE: '/api/users/delete',
      REFRESH_TOKEN: '/api/users/refresh',
    },
    
    // Health Check
    HEALTH: '/api/health',
  },
}

// Supported Languages (from backend)
export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
  { code: 'ta', name: 'Tamil', flag: '🇮🇳' },
  { code: 'te', name: 'Telugu', flag: '🇮🇳' },
  { code: 'bn', name: 'Bengali', flag: '🇮🇳' },
  { code: 'mr', name: 'Marathi', flag: '🇮🇳' },
  { code: 'gu', name: 'Gujarati', flag: '🇮🇳' },
  { code: 'kn', name: 'Kannada', flag: '🇮🇳' },
  { code: 'ml', name: 'Malayalam', flag: '🇮🇳' },
  { code: 'pa', name: 'Punjabi', flag: '🇮🇳' },
  { code: 'or', name: 'Odia', flag: '🇮🇳' },
]

// Content Types
export const CONTENT_TYPES = [
  { value: 'social_post', label: 'Social Media Post', icon: '📱' },
  { value: 'blog_post', label: 'Blog Post', icon: '📝' },
  { value: 'article', label: 'Article', icon: '📰' },
  { value: 'caption', label: 'Caption', icon: '💬' },
  { value: 'story', label: 'Story', icon: '📖' },
  { value: 'tweet', label: 'Tweet', icon: '🐦' },
  { value: 'linkedin_post', label: 'LinkedIn Post', icon: '💼' },
  { value: 'email', label: 'Email', icon: '📧' },
]

// Tone Types
export const TONE_TYPES = [
  { value: 'professional', label: 'Professional', emoji: '💼' },
  { value: 'casual', label: 'Casual', emoji: '😊' },
  { value: 'friendly', label: 'Friendly', emoji: '🤝' },
  { value: 'formal', label: 'Formal', emoji: '🎩' },
  { value: 'humorous', label: 'Humorous', emoji: '😄' },
  { value: 'inspirational', label: 'Inspirational', emoji: '✨' },
  { value: 'educational', label: 'Educational', emoji: '📚' },
  { value: 'persuasive', label: 'Persuasive', emoji: '🎯' },
]

// Social Media Platforms
export const SOCIAL_PLATFORMS = [
  { id: 'twitter', name: 'Twitter', icon: '🐦', color: '#1DA1F2' },
  { id: 'facebook', name: 'Facebook', icon: '📘', color: '#4267B2' },
  { id: 'instagram', name: 'Instagram', icon: '📷', color: '#E4405F' },
  { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: '#0077B5' },
  { id: 'youtube', name: 'YouTube', icon: '📺', color: '#FF0000' },
]

// Translation Methods
export const TRANSLATION_METHODS = [
  { value: 'INDIC_TRANS', label: 'IndicTrans (Indian Languages)', recommended: true },
  { value: 'AWS_TRANSLATE', label: 'AWS Translate' },
  { value: 'AI_MODEL', label: 'AI Model Translation' },
]

export default API_CONFIG
