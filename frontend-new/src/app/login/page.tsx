'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { API_ENDPOINTS, fetchAPI, handleAPIError } from '@/lib/api'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showPassword, setShowPassword] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      setLoading(true)
      setError(null)

      const response = await fetchAPI(API_ENDPOINTS.login, {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })

      if (!response.ok) {
        await handleAPIError(response)
      }

      const data = await response.json()
      
      // Store JWT token and user info
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      // Redirect to dashboard
      router.push('/dashboard')
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-purple-900">
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-20 left-20 w-72 h-72 bg-lavender rounded-full mix-blend-multiply filter blur-xl animate-blob"></div>
          <div className="absolute top-40 right-20 w-72 h-72 bg-cyan rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-2000"></div>
          <div className="absolute bottom-20 left-40 w-72 h-72 bg-periwinkle rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-4000"></div>
        </div>
      </div>

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-md">
        <div className="glass-effect p-8 rounded-2xl border border-periwinkle/30 slide-in-top">
          {/* Logo/Header */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-4 floating">🚀</div>
            <h1 className="text-3xl font-bold text-white gradient-text mb-2">Welcome Back!</h1>
            <p className="text-white/60">Sign in to continue to Bharat AI</p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-300 text-sm fade-in">
              ❌ {error}
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleLogin} className="space-y-4">
            {/* Email Field */}
            <div className="fade-in">
              <label className="block text-white/80 mb-2 font-medium">Email Address</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">📧</span>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full pl-12 pr-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none transition-all"
                  placeholder="you@example.com"
                />
              </div>
            </div>

            {/* Password Field */}
            <div className="fade-in" style={{ animationDelay: '0.1s' }}>
              <label className="block text-white/80 mb-2 font-medium">Password</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">🔒</span>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full pl-12 pr-12 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none transition-all"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-white/40 hover:text-white transition-colors"
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between text-sm fade-in" style={{ animationDelay: '0.2s' }}>
              <label className="flex items-center gap-2 text-white/70 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 rounded border-periwinkle/30 bg-white/10" />
                Remember me
              </label>
              <Link href="/forgot-password" className="text-cyan hover:text-lavender transition-colors">
                Forgot password?
              </Link>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full px-6 py-3 bg-gradient-to-r from-lavender to-purple rounded-xl text-white font-semibold hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 fade-in"
              style={{ animationDelay: '0.3s' }}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                  Signing in...
                </span>
              ) : (
                '🚀 Sign In'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6 fade-in" style={{ animationDelay: '0.4s' }}>
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-white/10"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-transparent text-white/60">Or continue with</span>
            </div>
          </div>

          {/* Social Login */}
          <div className="grid grid-cols-3 gap-3 fade-in" style={{ animationDelay: '0.5s' }}>
            <button className="px-4 py-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all flex items-center justify-center">
              <span className="text-2xl">🔵</span>
            </button>
            <button className="px-4 py-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all flex items-center justify-center">
              <span className="text-2xl">🟢</span>
            </button>
            <button className="px-4 py-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all flex items-center justify-center">
              <span className="text-2xl">⚫</span>
            </button>
          </div>

          {/* Sign Up Link */}
          <p className="text-center text-white/60 mt-6 fade-in" style={{ animationDelay: '0.6s' }}>
            Don't have an account?{' '}
            <Link href="/register" className="text-cyan hover:text-lavender transition-colors font-semibold">
              Sign up
            </Link>
          </p>
        </div>

        {/* Back to Home */}
        <div className="text-center mt-4 fade-in" style={{ animationDelay: '0.7s' }}>
          <Link href="/" className="text-white/60 hover:text-white transition-colors text-sm">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  )
}
