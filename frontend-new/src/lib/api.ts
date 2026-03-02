/**
 * API Configuration and Helper Functions
 * Centralized API URL management and fetch utilities
 */

// Get API URL from environment variable with fallback
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// Default request timeout (30 seconds)
const DEFAULT_TIMEOUT = 30000;

// API endpoints
export const API_ENDPOINTS = {
  // Auth
  login: `${API_URL}/api/users/login`,
  register: `${API_URL}/api/users/register`,
  
  // Content
  generateContent: `${API_URL}/api/content/generate`,
  listContent: `${API_URL}/api/content/list`,
  
  // Campaigns
  campaigns: `${API_URL}/api/campaigns`,
  
  // Translation
  translate: `${API_URL}/api/translation/translate`,
  translateDirect: `${API_URL}/api/translation/translate/direct`,
  
  // Social
  schedulePost: `${API_URL}/api/social/schedule`,
  listPosts: `${API_URL}/api/social/list`,
  
  // Analytics
  analyticsOverview: `${API_URL}/api/analytics/overview`,
  
  // Teams
  teams: `${API_URL}/api/teams`,
  
  // Models
  models: `${API_URL}/api/models`,
  
  // Templates
  templates: `${API_URL}/api/templates`,
  
  // Bulk Operations
  bulkUpload: `${API_URL}/api/bulk/upload`,
  bulkValidate: `${API_URL}/api/bulk/validate-csv`,
};

/**
 * Get authentication token from localStorage
 */
export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

/**
 * Get authenticated user from localStorage
 */
export function getAuthUser(): any | null {
  if (typeof window === 'undefined') return null;
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
}

/**
 * Check if JWT token is expired
 */
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

/**
 * Clear authentication data and redirect to login
 */
export function clearAuthAndRedirect(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/login';
}

/**
 * Create a fetch request with timeout
 */
function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeout: number = DEFAULT_TIMEOUT
): Promise<Response> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      reject(new Error('Request timeout'));
    }, timeout);

    fetch(url, options)
      .then(response => {
        clearTimeout(timer);
        resolve(response);
      })
      .catch(err => {
        clearTimeout(timer);
        reject(err);
      });
  });
}

/**
 * Make authenticated API request with timeout
 */
export async function fetchAPI(
  endpoint: string,
  options: RequestInit = {},
  timeout?: number
): Promise<Response> {
  // Check token expiration before request
  if (isTokenExpired()) {
    clearAuthAndRedirect();
    throw new Error('Session expired. Please login again.');
  }
  
  const token = getAuthToken();
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetchWithTimeout(endpoint, {
    ...options,
    headers,
  }, timeout);
  
  // Handle 401 Unauthorized
  if (response.status === 401) {
    clearAuthAndRedirect();
    throw new Error('Authentication required. Please login again.');
  }
  
  return response;
}

/**
 * Handle API errors consistently
 */
export async function handleAPIError(response: Response): Promise<never> {
  let errorMessage = `HTTP error! status: ${response.status}`;
  
  try {
    const data = await response.json();
    errorMessage = data.detail || data.message || errorMessage;
  } catch {
    // If response is not JSON, use default error message
  }
  
  throw new Error(errorMessage);
}

/**
 * Sanitize user input to prevent XSS
 */
export function sanitizeInput(input: string): string {
  if (!input) return '';
  
  // Remove HTML tags
  let sanitized = input.replace(/<[^>]*>/g, '');
  
  // Escape special characters
  sanitized = sanitized
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
  
  return sanitized;
}

/**
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate password strength
 */
export function validatePassword(password: string): { valid: boolean; message: string } {
  if (password.length < 8) {
    return { valid: false, message: 'Password must be at least 8 characters long' };
  }
  
  if (!/[A-Z]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one uppercase letter' };
  }
  
  if (!/[a-z]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one lowercase letter' };
  }
  
  if (!/[0-9]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one number' };
  }
  
  return { valid: true, message: 'Password is strong' };
}

/**
 * Type mapping for content types (frontend to backend)
 * Backend uses lowercase with underscores
 */
export const CONTENT_TYPE_MAP: Record<string, string> = {
  'blog_post': 'blog',
  'social_media': 'social_post',
  'article': 'article',
  'caption': 'caption',
  'script': 'script',
  'email': 'email',
  'ad_copy': 'ad_copy',
};

/**
 * Type mapping for tones (frontend to backend)
 * Backend uses lowercase
 */
export const TONE_MAP: Record<string, string> = {
  'professional': 'professional',
  'casual': 'casual',
  'friendly': 'friendly',
  'formal': 'formal',
  'humorous': 'humorous',
  'inspirational': 'inspirational',
  'educational': 'educational',
};

/**
 * Type mapping for platforms (frontend to backend)
 * Backend uses lowercase
 */
export const PLATFORM_MAP: Record<string, string> = {
  'facebook': 'facebook',
  'instagram': 'instagram',
  'twitter': 'twitter',
  'linkedin': 'linkedin',
  'youtube': 'youtube',
  'tiktok': 'tiktok',
};
