/**
 * Global State Management with Zustand
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// User State
interface User {
  id: number
  username: string
  email: string
  full_name?: string
  preferred_language?: string
}

interface UserState {
  user: User | null
  isAuthenticated: boolean
  setUser: (user: User | null) => void
  clearUser: () => void
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      clearUser: () => set({ user: null, isAuthenticated: false }),
    }),
    {
      name: 'user-storage',
    }
  )
)

// Content State
interface ContentState {
  currentContent: any | null
  contentList: any[]
  setCurrentContent: (content: any) => void
  setContentList: (list: any[]) => void
  addContent: (content: any) => void
  updateContent: (id: number, updates: any) => void
  removeContent: (id: number) => void
}

export const useContentStore = create<ContentState>((set) => ({
  currentContent: null,
  contentList: [],
  setCurrentContent: (content) => set({ currentContent: content }),
  setContentList: (list) => set({ contentList: list }),
  addContent: (content) =>
    set((state) => ({ contentList: [content, ...state.contentList] })),
  updateContent: (id, updates) =>
    set((state) => ({
      contentList: state.contentList.map((item) =>
        item.id === id ? { ...item, ...updates } : item
      ),
    })),
  removeContent: (id) =>
    set((state) => ({
      contentList: state.contentList.filter((item) => item.id !== id),
    })),
}))

// UI State
interface UIState {
  sidebarOpen: boolean
  theme: 'light' | 'dark'
  loading: boolean
  notification: {
    show: boolean
    message: string
    type: 'success' | 'error' | 'info' | 'warning'
  } | null
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
  setLoading: (loading: boolean) => void
  showNotification: (message: string, type: 'success' | 'error' | 'info' | 'warning') => void
  hideNotification: () => void
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      theme: 'light',
      loading: false,
      notification: null,
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setTheme: (theme) => set({ theme }),
      setLoading: (loading) => set({ loading }),
      showNotification: (message, type) =>
        set({ notification: { show: true, message, type } }),
      hideNotification: () => set({ notification: null }),
    }),
    {
      name: 'ui-storage',
    }
  )
)

// Translation State
interface TranslationState {
  sourceText: string
  targetLanguage: string
  translations: Record<string, string>
  setSourceText: (text: string) => void
  setTargetLanguage: (lang: string) => void
  addTranslation: (lang: string, text: string) => void
  clearTranslations: () => void
}

export const useTranslationStore = create<TranslationState>((set) => ({
  sourceText: '',
  targetLanguage: 'hi',
  translations: {},
  setSourceText: (text) => set({ sourceText: text }),
  setTargetLanguage: (lang) => set({ targetLanguage: lang }),
  addTranslation: (lang, text) =>
    set((state) => ({
      translations: { ...state.translations, [lang]: text },
    })),
  clearTranslations: () => set({ translations: {} }),
}))

// Social Media State
interface SocialMediaState {
  connectedAccounts: any[]
  scheduledPosts: any[]
  setConnectedAccounts: (accounts: any[]) => void
  addConnectedAccount: (account: any) => void
  removeConnectedAccount: (platform: string) => void
  setScheduledPosts: (posts: any[]) => void
  addScheduledPost: (post: any) => void
  updateScheduledPost: (id: number, updates: any) => void
  removeScheduledPost: (id: number) => void
}

export const useSocialMediaStore = create<SocialMediaState>((set) => ({
  connectedAccounts: [],
  scheduledPosts: [],
  setConnectedAccounts: (accounts) => set({ connectedAccounts: accounts }),
  addConnectedAccount: (account) =>
    set((state) => ({
      connectedAccounts: [...state.connectedAccounts, account],
    })),
  removeConnectedAccount: (platform) =>
    set((state) => ({
      connectedAccounts: state.connectedAccounts.filter(
        (acc) => acc.platform !== platform
      ),
    })),
  setScheduledPosts: (posts) => set({ scheduledPosts: posts }),
  addScheduledPost: (post) =>
    set((state) => ({
      scheduledPosts: [...state.scheduledPosts, post],
    })),
  updateScheduledPost: (id, updates) =>
    set((state) => ({
      scheduledPosts: state.scheduledPosts.map((post) =>
        post.id === id ? { ...post, ...updates } : post
      ),
    })),
  removeScheduledPost: (id) =>
    set((state) => ({
      scheduledPosts: state.scheduledPosts.filter((post) => post.id !== id),
    })),
}))

// Analytics State
interface AnalyticsState {
  overview: any | null
  engagement: any | null
  contentPerformance: any[]
  platformStats: any | null
  setOverview: (data: any) => void
  setEngagement: (data: any) => void
  setContentPerformance: (data: any[]) => void
  setPlatformStats: (data: any) => void
}

export const useAnalyticsStore = create<AnalyticsState>((set) => ({
  overview: null,
  engagement: null,
  contentPerformance: [],
  platformStats: null,
  setOverview: (data) => set({ overview: data }),
  setEngagement: (data) => set({ engagement: data }),
  setContentPerformance: (data) => set({ contentPerformance: data }),
  setPlatformStats: (data) => set({ platformStats: data }),
}))
