'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { API_ENDPOINTS, fetchAPI, handleAPIError } from '@/lib/api'

export default function RegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    fullName: '',
    role: 'student',
    preferredLanguage: 'hindi'
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await fetchAPI(API_ENDPOINTS.register, {
        method: 'POST',
        body: JSON.stringify({
          email: formData.email,
          username: formData.username,
          password: formData.password,
          full_name: formData.fullName || null,
          role: formData.role,
          preferred_language: formData.preferredLanguage
        })
      })

      if (!response.ok) {
        await handleAPIError(response)
      }

      const data = await response.json()
      
      // Auto-login after registration
      const loginResponse = await fetchAPI(API_ENDPOINTS.login, {
        method: 'POST',
        body: JSON.stringify({ 
          email: formData.email, 
          password: formData.password 
        })
      })

      if (loginResponse.ok) {
        const loginData = await loginResponse.json()
        localStorage.setItem('token', loginData.access_token)
        localStorage.setItem('user', JSON.stringify(loginData.user))
        router.push('/dashboard')
      } else {
        // Registration successful but auto-login failed, redirect to login
        router.push('/login')
      }
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed')
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

      {/* Register Card */}
      <div className="relative z-10 w-full max-w-2xl">
        <div className="glass-effect p-8 rounded-2xl border border-periwinkle/30 slide-in-top">
          {/* Logo/Header */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-4 floating">✨</div>
            <h1 className="text-3xl font-bold text-white gradient-text mb-2">Create Account</h1>
            <p className="text-white/60">Join Bharat AI and start creating amazing content</p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-300 text-sm fade-in">
              ❌ {error}
            </div>
          )}

          {/* Register Form */}
          <form onSubmit={handleRegister} className="space-y-4">
            {/* Email & Username */}
            <div className="grid grid-cols-2 gap-4">
              <div className="fade-in">
                <label className="block text-white/80 mb-2 font-medium">Email Address</label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">📧</span>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full pl-12 pr-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none transition-all"
                    placeholder="you@example.com"
                  />
                </div>
              </div>

              <div className="fade-in" style={{ animationDelay: '0.05s' }}>
                <label className="block text-white/80 mb-2 font-medium">Username</label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">👤</span>
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    minLength={3}
                    className="w-full pl-12 pr-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none transition-all"
                    placeholder="johndoe"
                  />
                </div>
              </div>
            </div>

            {/* Full Name */}
            <div className="fade-in" style={{ animationDelay: '0.1s' }}>
              <label className="block text-white/80 mb-2 font-medium">Full Name (Optional)</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">✍️</span>
                <input
                  type="text"
                  name="fullName"
                  value={formData.fullName}
                  onChange={handleChange}
                  className="w-full pl-12 pr-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none transition-all"
                  placeholder="John Doe"
                />
              </div>
            </div>

            {/* Password & Confirm Password */}
            <div className="grid grid-cols-2 gap-4">
              <div className="fade-in" style={{ animationDelay: '0.15s' }}>
                <label className="block text-white/80 mb-2 font-medium">Password</label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">🔒</span>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    minLength={8}
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

              <div className="fade-in" style={{ animationDelay: '0.2s' }}>
                <label className="block text-white/80 mb-2 font-medium">Confirm Password</label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">🔒</span>
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                    className="w-full pl-12 pr-12 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none transition-all"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-white/40 hover:text-white transition-colors"
                  >
                    {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                  </button>
                </div>
              </div>
            </div>

            {/* Role & Language */}
            <div className="grid grid-cols-2 gap-4">
              <div className="fade-in" style={{ animationDelay: '0.25s' }}>
                <label className="block text-white/80 mb-2 font-medium">I am a...</label>
                <select
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none transition-all"
                >
                  <option value="student" className="bg-purple-900">Student</option>
                  <option value="youtuber" className="bg-purple-900">YouTuber</option>
                  <option value="business" className="bg-purple-900">Business</option>
                  <option value="teacher" className="bg-purple-900">Teacher</option>
                  <option value="startup" className="bg-purple-900">Startup</option>
                </select>
              </div>

              <div className="fade-in" style={{ animationDelay: '0.3s' }}>
                <label className="block text-white/80 mb-2 font-medium">Preferred Language</label>
                <select
                  name="preferredLanguage"
                  value={formData.preferredLanguage}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none transition-all"
                >
                  <option value="english" className="bg-purple-900">English</option>
                  <option value="hindi" className="bg-purple-900">Hindi</option>
                  <option value="tamil" className="bg-purple-900">Tamil</option>
                  <option value="telugu" className="bg-purple-900">Telugu</option>
                  <option value="bengali" className="bg-purple-900">Bengali</option>
                  <option value="marathi" className="bg-purple-900">Marathi</option>
                  <option value="gujarati" className="bg-purple-900">Gujarati</option>
                  <option value="kannada" className="bg-purple-900">Kannada</option>
                  <option value="malayalam" className="bg-purple-900">Malayalam</option>
                  <option value="punjabi" className="bg-purple-900">Punjabi</option>
                  <option value="odia" className="bg-purple-900">Odia</option>
                  <option value="assamese" className="bg-purple-900">Assamese</option>
                </select>
              </div>
            </div>

            {/* Terms & Conditions */}
            <div className="flex items-start gap-2 text-sm fade-in" style={{ animationDelay: '0.35s' }}>
              <input type="checkbox" required className="w-4 h-4 mt-1 rounded border-periwinkle/30 bg-white/10" />
              <label className="text-white/70">
                I agree to the{' '}
                <Link href="/terms" className="text-cyan hover:text-lavender transition-colors">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link href="/privacy" className="text-cyan hover:text-lavender transition-colors">
                  Privacy Policy
                </Link>
              </label>
            </div>

            {/* Register Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full px-6 py-3 bg-gradient-to-r from-lavender to-purple rounded-xl text-white font-semibold hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 fade-in"
              style={{ animationDelay: '0.4s' }}>
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                  Creating account...
                </span>
              ) : (
                '✨ Create Account'
              )}
            </button>
          </form>

          {/* Sign In Link */}
          <p className="text-center text-white/60 mt-6 fade-in" style={{ animationDelay: '0.45s' }}>
            Already have an account?{' '}
            <Link href="/login" className="text-cyan hover:text-lavender transition-colors font-semibold">
              Sign in
            </Link>
          </p>
        </div>

        {/* Back to Home */}
        <div className="text-center mt-4 fade-in" style={{ animationDelay: '0.5s' }}>
          <Link href="/" className="text-white/60 hover:text-white transition-colors text-sm">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  )
}
