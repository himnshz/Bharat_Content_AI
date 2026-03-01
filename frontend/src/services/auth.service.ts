/**
 * Authentication Service
 * Handles user authentication and session management
 */

import { apiService } from './api.service'

export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  role?: string
  preferred_language?: string
  is_active: boolean
  created_at: string
}

export interface LoginResponse {
  access_token: string
  refresh_token?: string
  token_type: string
  user: User
}

export interface RegisterData {
  username: string
  email: string
  password: string
  full_name?: string
}

class AuthService {
  private currentUser: User | null = null

  // Check if user is authenticated
  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false
    const token = localStorage.getItem('access_token')
    return !!token
  }

  // Get current user
  getCurrentUser(): User | null {
    if (this.currentUser) return this.currentUser

    if (typeof window !== 'undefined') {
      const userStr = localStorage.getItem('current_user')
      if (userStr) {
        try {
          this.currentUser = JSON.parse(userStr)
          return this.currentUser
        } catch {
          return null
        }
      }
    }
    return null
  }

  // Set current user
  private setCurrentUser(user: User): void {
    this.currentUser = user
    if (typeof window !== 'undefined') {
      localStorage.setItem('current_user', JSON.stringify(user))
    }
  }

  // Clear current user
  private clearCurrentUser(): void {
    this.currentUser = null
    if (typeof window !== 'undefined') {
      localStorage.removeItem('current_user')
    }
  }

  // Register new user
  async register(data: RegisterData): Promise<User> {
    try {
      const response = await apiService.register(data)
      return response as User
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed')
    }
  }

  // Login user
  async login(username: string, password: string): Promise<LoginResponse> {
    try {
      const response = await apiService.login(username, password)
      
      // Fetch user profile after login
      const user = await apiService.getProfile()
      this.setCurrentUser(user as User)
      
      return {
        access_token: response.access_token,
        refresh_token: response.refresh_token,
        token_type: response.token_type || 'bearer',
        user: user as User,
      }
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed')
    }
  }

  // Logout user
  async logout(): Promise<void> {
    await apiService.logout()
    this.clearCurrentUser()
    
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  // Refresh user profile
  async refreshProfile(): Promise<User> {
    try {
      const user = await apiService.getProfile()
      this.setCurrentUser(user as User)
      return user as User
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to refresh profile')
    }
  }

  // Update user profile
  async updateProfile(data: {
    full_name?: string
    email?: string
    bio?: string
    preferred_language?: string
    timezone?: string
  }): Promise<User> {
    try {
      const user = await apiService.updateProfile(data)
      this.setCurrentUser(user as User)
      return user as User
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to update profile')
    }
  }

  // Change password
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      await apiService.changePassword(currentPassword, newPassword)
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to change password')
    }
  }

  // Get user stats
  async getUserStats(): Promise<any> {
    try {
      return await apiService.getUserStats()
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get user stats')
    }
  }

  // Check if token is expired (basic check)
  isTokenExpired(): boolean {
    if (typeof window === 'undefined') return true
    
    const token = localStorage.getItem('access_token')
    if (!token) return true

    try {
      // Decode JWT token (basic implementation)
      const payload = JSON.parse(atob(token.split('.')[1]))
      const exp = payload.exp * 1000 // Convert to milliseconds
      return Date.now() >= exp
    } catch {
      return true
    }
  }
}

// Export singleton instance
export const authService = new AuthService()
export default authService
