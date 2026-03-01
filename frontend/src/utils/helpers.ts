/**
 * Utility Helper Functions
 */

import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { format, formatDistanceToNow } from 'date-fns'

// Merge Tailwind classes
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Format date
export function formatDate(date: string | Date, formatStr: string = 'PPP'): string {
  return format(new Date(date), formatStr)
}

// Format relative time
export function formatRelativeTime(date: string | Date): string {
  return formatDistanceToNow(new Date(date), { addSuffix: true })
}

// Truncate text
export function truncateText(text: string, maxLength: number = 100): string {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// Calculate reading time
export function calculateReadingTime(text: string): number {
  const wordsPerMinute = 200
  const wordCount = text.split(/\s+/).length
  return Math.ceil(wordCount / wordsPerMinute)
}

// Count words
export function countWords(text: string): number {
  return text.trim().split(/\s+/).filter(Boolean).length
}

// Count characters
export function countCharacters(text: string): number {
  return text.length
}

// Extract hashtags
export function extractHashtags(text: string): string[] {
  const hashtagRegex = /#[\w]+/g
  return text.match(hashtagRegex) || []
}

// Extract mentions
export function extractMentions(text: string): string[] {
  const mentionRegex = /@[\w]+/g
  return text.match(mentionRegex) || []
}

// Generate random ID
export function generateId(): string {
  return Math.random().toString(36).substring(2, 15)
}

// Debounce function
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// Throttle function
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

// Copy to clipboard
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    // Fallback for older browsers
    const textArea = document.createElement('textarea')
    textArea.value = text
    textArea.style.position = 'fixed'
    textArea.style.left = '-999999px'
    document.body.appendChild(textArea)
    textArea.select()
    try {
      document.execCommand('copy')
      document.body.removeChild(textArea)
      return true
    } catch {
      document.body.removeChild(textArea)
      return false
    }
  }
}

// Download file
export function downloadFile(content: string, filename: string, type: string = 'text/plain') {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

// Format number with commas
export function formatNumber(num: number): string {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// Format percentage
export function formatPercentage(value: number, decimals: number = 1): string {
  return `${value.toFixed(decimals)}%`
}

// Get language name from code
export function getLanguageName(code: string): string {
  const languages: Record<string, string> = {
    en: 'English',
    hi: 'Hindi',
    ta: 'Tamil',
    te: 'Telugu',
    bn: 'Bengali',
    mr: 'Marathi',
    gu: 'Gujarati',
    kn: 'Kannada',
    ml: 'Malayalam',
    pa: 'Punjabi',
    or: 'Odia',
  }
  return languages[code] || code
}

// Get language flag emoji
export function getLanguageFlag(code: string): string {
  const flags: Record<string, string> = {
    en: '🇬🇧',
    hi: '🇮🇳',
    ta: '🇮🇳',
    te: '🇮🇳',
    bn: '🇮🇳',
    mr: '🇮🇳',
    gu: '🇮🇳',
    kn: '🇮🇳',
    ml: '🇮🇳',
    pa: '🇮🇳',
    or: '🇮🇳',
  }
  return flags[code] || '🌐'
}

// Validate email
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Validate URL
export function isValidUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// Get file extension
export function getFileExtension(filename: string): string {
  return filename.slice(((filename.lastIndexOf('.') - 1) >>> 0) + 2)
}

// Format file size
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

// Sleep/delay function
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

// Get initials from name
export function getInitials(name: string): string {
  return name
    .split(' ')
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

// Generate color from string (for avatars)
export function stringToColor(str: string): string {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  const colors = ['#A4A5F5', '#9EF0FF', '#B5C7EB', '#8E70CF']
  return colors[Math.abs(hash) % colors.length]
}

// Check if mobile device
export function isMobile(): boolean {
  if (typeof window === 'undefined') return false
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  )
}

// Get platform icon
export function getPlatformIcon(platform: string): string {
  const icons: Record<string, string> = {
    twitter: '🐦',
    facebook: '📘',
    instagram: '📷',
    linkedin: '💼',
    youtube: '📺',
  }
  return icons[platform.toLowerCase()] || '📱'
}

// Get content type icon
export function getContentTypeIcon(type: string): string {
  const icons: Record<string, string> = {
    social_post: '📱',
    blog_post: '📝',
    article: '📰',
    caption: '💬',
    story: '📖',
    tweet: '🐦',
    linkedin_post: '💼',
    email: '📧',
  }
  return icons[type] || '📄'
}

// Get tone emoji
export function getToneEmoji(tone: string): string {
  const emojis: Record<string, string> = {
    professional: '💼',
    casual: '😊',
    friendly: '🤝',
    formal: '🎩',
    humorous: '😄',
    inspirational: '✨',
    educational: '📚',
    persuasive: '🎯',
  }
  return emojis[tone] || '💬'
}

export default {
  cn,
  formatDate,
  formatRelativeTime,
  truncateText,
  calculateReadingTime,
  countWords,
  countCharacters,
  extractHashtags,
  extractMentions,
  generateId,
  debounce,
  throttle,
  copyToClipboard,
  downloadFile,
  formatNumber,
  formatPercentage,
  getLanguageName,
  getLanguageFlag,
  isValidEmail,
  isValidUrl,
  getFileExtension,
  formatFileSize,
  sleep,
  getInitials,
  stringToColor,
  isMobile,
  getPlatformIcon,
  getContentTypeIcon,
  getToneEmoji,
}
