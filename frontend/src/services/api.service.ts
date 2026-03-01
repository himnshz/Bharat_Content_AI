/**
 * API Service
 * Handles all HTTP requests to the backend
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { API_CONFIG } from '@/config/api.config'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        const token = this.getToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expired, try to refresh
          const refreshed = await this.refreshToken()
          if (refreshed) {
            // Retry the original request
            return this.api.request(error.config)
          } else {
            // Redirect to login
            this.clearToken()
            if (typeof window !== 'undefined') {
              window.location.href = '/login'
            }
          }
        }
        return Promise.reject(error)
      }
    )
  }

  // Token management
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token')
    }
    return null
  }

  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token)
    }
  }

  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  private async refreshToken(): Promise<boolean> {
    try {
      const refreshToken = typeof window !== 'undefined' 
        ? localStorage.getItem('refresh_token') 
        : null
      
      if (!refreshToken) return false

      const response = await axios.post(
        `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USERS.REFRESH_TOKEN}`,
        { refresh_token: refreshToken }
      )

      if (response.data.access_token) {
        this.setToken(response.data.access_token)
        return true
      }
      return false
    } catch {
      return false
    }
  }

  // Generic HTTP methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.api.get(url, config)
    return response.data
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.api.post(url, data, config)
    return response.data
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.api.put(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.api.delete(url, config)
    return response.data
  }

  // Content Generation APIs
  async generateContent(data: {
    prompt: string
    language: string
    tone: string
    content_type: string
    user_id: number
  }) {
    return this.post(API_CONFIG.ENDPOINTS.CONTENT.GENERATE, data)
  }

  async listContent(params: {
    user_id: number
    skip?: number
    limit?: number
    content_type?: string
    language?: string
    status?: string
  }) {
    return this.get(API_CONFIG.ENDPOINTS.CONTENT.LIST, { params })
  }

  async getContent(id: number) {
    return this.get(API_CONFIG.ENDPOINTS.CONTENT.GET(id))
  }

  async editContent(id: number, edited_content: string) {
    return this.put(API_CONFIG.ENDPOINTS.CONTENT.EDIT(id), { edited_content })
  }

  async summarizeContent(content_id: number, target_length?: number) {
    return this.post(API_CONFIG.ENDPOINTS.CONTENT.SUMMARIZE, {
      content_id,
      target_length,
    })
  }

  async deleteContent(id: number) {
    return this.delete(API_CONFIG.ENDPOINTS.CONTENT.DELETE(id))
  }

  async getAIServicesStatus() {
    return this.get(API_CONFIG.ENDPOINTS.CONTENT.AI_SERVICES_STATUS)
  }

  // Translation APIs
  async translateContent(data: {
    text: string
    source_language: string
    target_language: string
    maintain_tone?: boolean
    method?: string
  }) {
    return this.post(API_CONFIG.ENDPOINTS.TRANSLATION.TRANSLATE, data)
  }

  async batchTranslate(data: {
    text: string
    source_language: string
    target_languages: string[]
    maintain_tone?: boolean
  }) {
    return this.post(API_CONFIG.ENDPOINTS.TRANSLATION.BATCH_TRANSLATE, data)
  }

  async getSupportedLanguages() {
    return this.get(API_CONFIG.ENDPOINTS.TRANSLATION.SUPPORTED_LANGUAGES)
  }

  async detectLanguage(text: string) {
    return this.post(API_CONFIG.ENDPOINTS.TRANSLATION.DETECT_LANGUAGE, { text })
  }

  // Social Media APIs
  async connectSocialAccount(data: {
    platform: string
    access_token: string
    user_id: number
  }) {
    return this.post(API_CONFIG.ENDPOINTS.SOCIAL.CONNECT, data)
  }

  async disconnectSocialAccount(platform: string) {
    return this.delete(API_CONFIG.ENDPOINTS.SOCIAL.DISCONNECT(platform))
  }

  async getSocialAccounts(user_id: number) {
    return this.get(API_CONFIG.ENDPOINTS.SOCIAL.ACCOUNTS, {
      params: { user_id },
    })
  }

  async schedulePost(data: {
    content_id: number
    platforms: string[]
    scheduled_time: string
    user_id: number
  }) {
    return this.post(API_CONFIG.ENDPOINTS.SOCIAL.SCHEDULE, data)
  }

  async getScheduledPosts(user_id: number) {
    return this.get(API_CONFIG.ENDPOINTS.SOCIAL.SCHEDULED_POSTS, {
      params: { user_id },
    })
  }

  async publishPost(data: {
    content_id: number
    platforms: string[]
    user_id: number
  }) {
    return this.post(API_CONFIG.ENDPOINTS.SOCIAL.PUBLISH, data)
  }

  // Analytics APIs
  async getAnalyticsOverview(user_id: number, days?: number) {
    return this.get(API_CONFIG.ENDPOINTS.ANALYTICS.OVERVIEW, {
      params: { user_id, days },
    })
  }

  async getEngagementMetrics(user_id: number, start_date?: string, end_date?: string) {
    return this.get(API_CONFIG.ENDPOINTS.ANALYTICS.ENGAGEMENT, {
      params: { user_id, start_date, end_date },
    })
  }

  async getContentPerformance(user_id: number, limit?: number) {
    return this.get(API_CONFIG.ENDPOINTS.ANALYTICS.CONTENT_PERFORMANCE, {
      params: { user_id, limit },
    })
  }

  async getPlatformStats(user_id: number) {
    return this.get(API_CONFIG.ENDPOINTS.ANALYTICS.PLATFORM_STATS, {
      params: { user_id },
    })
  }

  async getLanguageDistribution(user_id: number) {
    return this.get(API_CONFIG.ENDPOINTS.ANALYTICS.LANGUAGE_DISTRIBUTION, {
      params: { user_id },
    })
  }

  // Voice Input APIs
  async transcribeAudio(data: FormData) {
    return this.post(API_CONFIG.ENDPOINTS.VOICE.TRANSCRIBE, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  }

  async processVoiceInput(data: {
    audio_file: File
    language: string
    user_id: number
    generate_content?: boolean
  }) {
    const formData = new FormData()
    formData.append('audio_file', data.audio_file)
    formData.append('language', data.language)
    formData.append('user_id', data.user_id.toString())
    if (data.generate_content !== undefined) {
      formData.append('generate_content', data.generate_content.toString())
    }

    return this.post(API_CONFIG.ENDPOINTS.VOICE.PROCESS, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  }

  // User Management APIs
  async register(data: {
    username: string
    email: string
    password: string
    full_name?: string
  }) {
    return this.post(API_CONFIG.ENDPOINTS.USERS.REGISTER, data)
  }

  async login(username: string, password: string) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await this.post<any>(
      API_CONFIG.ENDPOINTS.USERS.LOGIN,
      formData,
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      }
    )

    if (response.access_token) {
      this.setToken(response.access_token)
      if (response.refresh_token && typeof window !== 'undefined') {
        localStorage.setItem('refresh_token', response.refresh_token)
      }
    }

    return response
  }

  async logout() {
    this.clearToken()
  }

  async getProfile() {
    return this.get(API_CONFIG.ENDPOINTS.USERS.PROFILE)
  }

  async updateProfile(data: {
    full_name?: string
    email?: string
    bio?: string
    preferred_language?: string
    timezone?: string
  }) {
    return this.put(API_CONFIG.ENDPOINTS.USERS.UPDATE_PROFILE, data)
  }

  async changePassword(current_password: string, new_password: string) {
    return this.post(API_CONFIG.ENDPOINTS.USERS.CHANGE_PASSWORD, {
      current_password,
      new_password,
    })
  }

  async getUserStats() {
    return this.get(API_CONFIG.ENDPOINTS.USERS.STATS)
  }

  // Health Check
  async healthCheck() {
    return this.get(API_CONFIG.ENDPOINTS.HEALTH)
  }
}

// Export singleton instance
export const apiService = new ApiService()
export default apiService
