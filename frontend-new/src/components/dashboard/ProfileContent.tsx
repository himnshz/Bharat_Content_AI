'use client'

import { useState, useEffect, useMemo, useCallback } from 'react'

interface UserProfile {
  id: number
  email: string
  username: string
  full_name: string | null
  role: string
  subscription_tier: string
  preferred_language: string
  is_active: boolean
  is_verified: boolean
  email_verified: boolean
  content_generated_count: number
  translations_count: number
  posts_scheduled_count: number
  created_at: string
  last_login: string | null
}

interface APIKey {
  id: number
  service_name: string
  key_preview: string
  is_active: boolean
  created_at: string
}

export default function ProfileContent() {
  const [activeTab, setActiveTab] = useState('account')
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // Form states
  const [fullName, setFullName] = useState('')
  const [preferredLanguage, setPreferredLanguage] = useState('hindi')
  const [phone, setPhone] = useState('')
  
  // API Keys state
  const [apiKeys, setApiKeys] = useState<APIKey[]>([
    { id: 1, service_name: 'Gemini API', key_preview: 'sk-****...****', is_active: true, created_at: '2024-01-01' },
    { id: 2, service_name: 'OpenAI API', key_preview: 'sk-****...****', is_active: true, created_at: '2024-01-01' },
    { id: 3, service_name: 'Anthropic API', key_preview: 'sk-****...****', is_active: false, created_at: '2024-01-01' },
  ])
  
  // Preferences state
  const [preferences, setPreferences] = useState({
    emailNotifications: true,
    autoSaveDrafts: true,
    darkMode: true,
    analyticsTracking: true,
  })

  // For demo, using user_id = 1
  const userId = 1

  useEffect(() => {
    fetchProfile()
  }, [])

  // ✅ OPTIMIZED: Memoize fetch function
  const fetchProfile = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await fetch(`http://127.0.0.1:8000/api/users/profile/${userId}`)
      if (!response.ok) throw new Error('Failed to fetch profile')
      
      const data = await response.json()
      setProfile(data)
      setFullName(data.full_name || '')
      setPreferredLanguage(data.preferred_language || 'hindi')
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load profile')
      console.error('Profile error:', err)
    } finally {
      setLoading(false)
    }
  }, [userId])

  // ✅ OPTIMIZED: Memoize save handler
  const handleSaveProfile = useCallback(async () => {
    try {
      setSaving(true)
      setError(null)
      
      const response = await fetch(`http://127.0.0.1:8000/api/users/profile/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          full_name: fullName,
          preferred_language: preferredLanguage,
        })
      })
      
      if (!response.ok) throw new Error('Failed to update profile')
      
      const data = await response.json()
      setProfile(data)
      alert('✅ Profile updated successfully!')
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save profile')
      alert('❌ Failed to update profile')
    } finally {
      setSaving(false)
    }
  }, [userId, fullName, preferredLanguage])

  // ✅ OPTIMIZED: Memoize subscription color function
  const getSubscriptionColor = useCallback((tier: string) => {
    switch (tier) {
      case 'free': return 'bg-gray-500/20 text-gray-300'
      case 'basic': return 'bg-blue-500/20 text-blue-300'
      case 'pro': return 'bg-purple-500/20 text-purple-300'
      case 'enterprise': return 'bg-gold-500/20 text-gold-300'
      default: return 'bg-gray-500/20 text-gray-300'
    }
  }, [])

  // ✅ OPTIMIZED: Memoize usage percentage calculation
  const getUsagePercentage = useCallback((current: number, limit: number) => {
    return Math.min((current / limit) * 100, 100)
  }, [])

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-lavender mx-auto mb-4"></div>
          <p className="text-white/60">Loading profile...</p>
        </div>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="glass-effect p-8 rounded-2xl border border-red-500/30 text-center">
          <p className="text-red-400 mb-4">❌ {error || 'Failed to load profile'}</p>
          <button
            onClick={fetchProfile}
            className="px-6 py-2 bg-gradient-to-r from-lavender to-purple rounded-lg text-white font-semibold hover:scale-105 transition-transform"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full p-8 overflow-auto">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Profile Header */}
        <div className="glass-effect p-8 rounded-2xl border border-periwinkle/30 slide-in-top">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-lavender to-purple flex items-center justify-center text-4xl border-4 border-white/20">
              {profile.full_name ? profile.full_name[0].toUpperCase() : '👤'}
            </div>
            <div className="flex-1">
              <h2 className="text-3xl font-bold text-white gradient-text mb-2">
                {profile.full_name || profile.username}
              </h2>
              <p className="text-white/60 mb-2">{profile.email}</p>
              <div className="flex gap-2">
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getSubscriptionColor(profile.subscription_tier)}`}>
                  {profile.subscription_tier.toUpperCase()} Plan
                </span>
                {profile.is_verified && (
                  <span className="px-3 py-1 bg-cyan/20 text-cyan rounded-full text-sm font-semibold">
                    ✓ Verified
                  </span>
                )}
                {profile.email_verified && (
                  <span className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-sm font-semibold">
                    ✉️ Email Verified
                  </span>
                )}
              </div>
            </div>
            <div className="text-right">
              <div className="text-white/60 text-sm mb-1">Member since</div>
              <div className="text-white font-semibold">
                {new Date(profile.created_at).toLocaleDateString()}
              </div>
            </div>
          </div>
        </div>

        {/* Usage Stats */}
        <div className="grid grid-cols-3 gap-4">
          <div className="glass-effect p-4 rounded-xl border border-lavender/30 flip-in-hor-bottom">
            <div className="text-white/60 text-sm mb-1">Content Generated</div>
            <div className="text-2xl font-bold text-white gradient-text">
              {profile.content_generated_count}
            </div>
          </div>
          <div className="glass-effect p-4 rounded-xl border border-cyan/30 flip-in-hor-bottom" style={{ animationDelay: '0.1s' }}>
            <div className="text-white/60 text-sm mb-1">Translations</div>
            <div className="text-2xl font-bold text-white gradient-text">
              {profile.translations_count}
            </div>
          </div>
          <div className="glass-effect p-4 rounded-xl border border-periwinkle/30 flip-in-hor-bottom" style={{ animationDelay: '0.2s' }}>
            <div className="text-white/60 text-sm mb-1">Posts Scheduled</div>
            <div className="text-2xl font-bold text-white gradient-text">
              {profile.posts_scheduled_count}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="glass-effect p-2 rounded-2xl border border-periwinkle/30 flex gap-2 fade-in">
          {['Account', 'Subscription', 'API Keys', 'Preferences'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab.toLowerCase())}
              className={`flex-1 px-6 py-3 rounded-xl transition-all font-semibold ${
                activeTab === tab.toLowerCase()
                  ? 'bg-gradient-to-r from-lavender to-purple text-white'
                  : 'text-white/70 hover:bg-white/10'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Account Tab */}
        {activeTab === 'account' && (
          <div className="glass-effect p-6 rounded-2xl border border-lavender/30 space-y-4 slide-in-blurred-left">
            <h3 className="text-xl font-bold text-white gradient-text mb-4">👤 Account Settings</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-white/80 mb-2 font-medium">Full Name</label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none transition-all"
                  placeholder="Enter your full name"
                />
              </div>
              <div>
                <label className="block text-white/80 mb-2 font-medium">Email</label>
                <input
                  type="email"
                  value={profile.email}
                  disabled
                  className="w-full px-4 py-3 bg-white/5 backdrop-blur-sm border-2 border-white/10 rounded-xl text-white/50 cursor-not-allowed"
                />
              </div>
              <div>
                <label className="block text-white/80 mb-2 font-medium">Username</label>
                <input
                  type="text"
                  value={profile.username}
                  disabled
                  className="w-full px-4 py-3 bg-white/5 backdrop-blur-sm border-2 border-white/10 rounded-xl text-white/50 cursor-not-allowed"
                />
              </div>
              <div>
                <label className="block text-white/80 mb-2 font-medium">Preferred Language</label>
                <select 
                  value={preferredLanguage}
                  onChange={(e) => setPreferredLanguage(e.target.value)}
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
              <div>
                <label className="block text-white/80 mb-2 font-medium">Role</label>
                <input
                  type="text"
                  value={profile.role}
                  disabled
                  className="w-full px-4 py-3 bg-white/5 backdrop-blur-sm border-2 border-white/10 rounded-xl text-white/50 cursor-not-allowed capitalize"
                />
              </div>
              <div>
                <label className="block text-white/80 mb-2 font-medium">Phone (Optional)</label>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+91 XXXXX XXXXX"
                  className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none transition-all"
                />
              </div>
            </div>

            {error && (
              <div className="p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-300">
                ❌ {error}
              </div>
            )}

            <button 
              onClick={handleSaveProfile}
              disabled={saving}
              className="w-full px-6 py-3 bg-gradient-to-r from-lavender to-purple rounded-xl text-white font-semibold hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {saving ? '💾 Saving...' : '💾 Save Changes'}
            </button>
          </div>
        )}

        {/* Subscription Tab */}
        {activeTab === 'subscription' && (
          <div className="space-y-4">
            {/* Current Plan */}
            <div className="glass-effect p-6 rounded-2xl border border-lavender/30 slide-in-blurred-left">
              <h3 className="text-xl font-bold text-white gradient-text mb-4">💎 Current Plan</h3>
              
              <div className="bg-gradient-to-br from-lavender/20 to-purple/20 p-6 rounded-xl border border-lavender/30">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h4 className="text-2xl font-bold text-white mb-1">
                      {profile.subscription_tier.toUpperCase()} Plan
                    </h4>
                    <p className="text-white/60">
                      {profile.subscription_tier === 'free' ? 'Free forever' : '$29/month • Renews on March 15, 2024'}
                    </p>
                  </div>
                  {profile.subscription_tier !== 'enterprise' && (
                    <button className="px-6 py-3 bg-white text-purple rounded-xl font-semibold hover:scale-105 transition-all">
                      ⬆️ Upgrade Plan
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Usage Limits */}
            <div className="glass-effect p-6 rounded-2xl border border-periwinkle/30 fade-in">
              <h3 className="text-xl font-bold text-white gradient-text mb-4">📊 Usage & Limits</h3>
              
              <div className="space-y-4">
                {[
                  { label: 'Content Generated', current: profile.content_generated_count, limit: profile.subscription_tier === 'free' ? 100 : 1000, icon: '📝' },
                  { label: 'Translations', current: profile.translations_count, limit: profile.subscription_tier === 'free' ? 50 : 500, icon: '🌐' },
                  { label: 'Posts Scheduled', current: profile.posts_scheduled_count, limit: profile.subscription_tier === 'free' ? 20 : 200, icon: '📅' },
                ].map((item, i) => {
                  const percentage = getUsagePercentage(item.current, item.limit)
                  return (
                    <div key={item.label} className="bounce-in" style={{ animationDelay: `${i * 0.1}s` }}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-white/80 flex items-center gap-2">
                          <span>{item.icon}</span>
                          {item.label}
                        </span>
                        <span className="text-white font-semibold">
                          {item.current} / {item.limit}
                        </span>
                      </div>
                      <div className="h-3 bg-white/10 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-1000 ${
                            percentage > 80 ? 'bg-red-500' : percentage > 50 ? 'bg-yellow-500' : 'bg-gradient-to-r from-lavender to-cyan'
                          }`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Plan Comparison */}
            <div className="glass-effect p-6 rounded-2xl border border-lavender/30 slide-in-top">
              <h3 className="text-xl font-bold text-white gradient-text mb-4">💰 Available Plans</h3>
              
              <div className="grid grid-cols-3 gap-4">
                {[
                  { name: 'Basic', price: '$9', features: ['500 Content', '250 Translations', '100 Posts'] },
                  { name: 'Pro', price: '$29', features: ['2000 Content', '1000 Translations', '500 Posts'] },
                  { name: 'Enterprise', price: '$99', features: ['Unlimited', 'Priority Support', 'Custom AI'] },
                ].map((plan, i) => (
                  <div key={plan.name} className="bg-white/5 p-4 rounded-xl border border-white/10 hover:border-lavender/50 transition-all flip-in-hor-bottom" style={{ animationDelay: `${i * 0.1}s` }}>
                    <h4 className="text-white font-bold text-lg mb-2">{plan.name}</h4>
                    <div className="text-3xl font-bold text-white gradient-text mb-4">{plan.price}<span className="text-sm text-white/60">/mo</span></div>
                    <ul className="space-y-2 mb-4">
                      {plan.features.map((feature) => (
                        <li key={feature} className="text-white/70 text-sm flex items-center gap-2">
                          <span className="text-cyan">✓</span>
                          {feature}
                        </li>
                      ))}
                    </ul>
                    <button className="w-full px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-all">
                      Select Plan
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* API Keys Tab */}
        {activeTab === 'api keys' && (
          <div className="glass-effect p-6 rounded-2xl border border-lavender/30 space-y-4 fade-in">
            <h3 className="text-xl font-bold text-white gradient-text mb-4">🔑 API Keys</h3>
            
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4 mb-4">
              <p className="text-blue-300 text-sm">
                ℹ️ API keys are used to authenticate with AI services. Keep them secure and never share them publicly.
              </p>
            </div>
            
            <div className="space-y-3">
              {apiKeys.map((api, i) => (
                <div key={api.id} className="bg-white/5 backdrop-blur-sm p-4 rounded-xl border border-white/10 flip-in-hor-bottom" style={{ animationDelay: `${i * 0.1}s` }}>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-white font-semibold">{api.service_name}</span>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      api.is_active ? 'bg-green-500/20 text-green-300' : 'bg-gray-500/20 text-gray-300'
                    }`}>
                      {api.is_active ? '✓ Active' : '○ Inactive'}
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <input
                      type="password"
                      value={api.key_preview}
                      disabled
                      className="flex-1 px-4 py-2 bg-white/10 backdrop-blur-sm border border-periwinkle/30 rounded-lg text-white text-sm"
                    />
                    <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-all" title="Show/Hide">
                      👁️
                    </button>
                    <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-all" title="Copy">
                      📋
                    </button>
                    <button className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-red-300 text-sm transition-all" title="Delete">
                      🗑️
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <button className="w-full px-6 py-3 bg-gradient-to-r from-lavender to-purple rounded-xl text-white font-semibold hover:scale-105 transition-transform">
              ➕ Add New API Key
            </button>
          </div>
        )}

        {/* Preferences Tab */}
        {activeTab === 'preferences' && (
          <div className="glass-effect p-6 rounded-2xl border border-lavender/30 space-y-4 slide-in-blurred-left">
            <h3 className="text-xl font-bold text-white gradient-text mb-4">⚙️ Preferences</h3>
            
            <div className="space-y-4">
              {[
                { key: 'emailNotifications', label: 'Email Notifications', description: 'Receive updates via email' },
                { key: 'autoSaveDrafts', label: 'Auto-save Drafts', description: 'Automatically save your work' },
                { key: 'darkMode', label: 'Dark Mode', description: 'Use dark theme (currently enabled)' },
                { key: 'analyticsTracking', label: 'Analytics Tracking', description: 'Help us improve with usage data' },
              ].map((pref, i) => (
                <div key={pref.key} className="flex items-center justify-between p-4 bg-white/5 rounded-xl bounce-in" style={{ animationDelay: `${i * 0.1}s` }}>
                  <div>
                    <div className="text-white font-semibold mb-1">{pref.label}</div>
                    <div className="text-white/60 text-sm">{pref.description}</div>
                  </div>
                  <label className="relative inline-block w-12 h-6">
                    <input 
                      type="checkbox" 
                      checked={preferences[pref.key as keyof typeof preferences]}
                      onChange={(e) => setPreferences({ ...preferences, [pref.key]: e.target.checked })}
                      className="sr-only peer" 
                    />
                    <div className="w-12 h-6 bg-white/20 rounded-full peer peer-checked:bg-lavender transition-all cursor-pointer" />
                    <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full transition-all peer-checked:translate-x-6" />
                  </label>
                </div>
              ))}
            </div>

            <button className="w-full px-6 py-3 bg-gradient-to-r from-lavender to-purple rounded-xl text-white font-semibold hover:scale-105 transition-transform">
              💾 Save Preferences
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
