'use client'

import { useState } from 'react'
import { API_ENDPOINTS, fetchAPI } from '@/lib/api'

export default function ScheduleContent() {
  const [content, setContent] = useState('')
  const [platform, setPlatform] = useState('twitter')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const platforms = [
    { id: 'twitter', name: 'Twitter', icon: '🐦' },
    { id: 'facebook', name: 'Facebook', icon: '📘' },
    { id: 'instagram', name: 'Instagram', icon: '📸' },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼' },
    { id: 'youtube', name: 'YouTube', icon: '📺' },
  ]

  const scheduledPosts = [
    { id: 1, platform: 'Twitter', content: 'Check out our new AI features!', date: '2024-03-15', time: '10:00 AM', status: 'scheduled' },
    { id: 2, platform: 'Facebook', content: 'Join our webinar on AI...', date: '2024-03-16', time: '2:00 PM', status: 'scheduled' },
    { id: 3, platform: 'LinkedIn', content: 'We are hiring!', date: '2024-03-14', time: '9:00 AM', status: 'published' },
  ]

  const handleSchedule = async () => {
    // Validation
    if (!content.trim()) {
      setError('Please enter content')
      return
    }
    
    // Platform-specific validation
    if (platform === 'twitter' && content.length > 280) {
      setError('Twitter posts must be 280 characters or less')
      return
    }
    
    if (!date || !time) {
      setError('Please select date and time')
      return
    }
    
    const scheduledTime = new Date(`${date}T${time}`)
    if (scheduledTime <= new Date()) {
      setError('Scheduled time must be in the future')
      return
    }
    
    setLoading(true)
    setError('')
    
    try {
      const scheduledTimeISO = `${date}T${time}:00`
      
      const response = await fetchAPI(API_ENDPOINTS.schedulePost, {
        method: 'POST',
        body: JSON.stringify({
          text_content: content,  // Fixed: was 'content', now 'text_content'
          platform: platform,
          scheduled_time: scheduledTimeISO,
        }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || `HTTP error! status: ${response.status}`)
      }

      alert('Post scheduled successfully!')
      setContent('')
      setDate('')
      setTime('')
    } catch (err) {
      console.error('Scheduling error:', err)
      const message = err instanceof Error ? err.message : 'Failed to schedule post. Please try again.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-full flex gap-6 p-8">
      {/* Schedule Form */}
      <div className="w-2/5 space-y-6">
        <div className="glass-effect p-6 rounded-2xl border border-periwinkle/30 slide-in-blurred-left">
          <h3 className="text-2xl font-bold text-white mb-4 gradient-text">📅 Schedule Post</h3>
          
          <div className="space-y-4">
            {error && (
              <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm">
                {error}
              </div>
            )}
            
            <div>
              <label className="block text-white/80 mb-2 font-medium">Content</label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="What do you want to post?"
                className="w-full h-32 px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none resize-none"
              />
            </div>

            <div>
              <label className="block text-white/80 mb-2 font-medium">Platform</label>
              <div className="grid grid-cols-3 gap-2">
                {platforms.map(p => (
                  <button
                    key={p.id}
                    onClick={() => setPlatform(p.id)}
                    className={`px-4 py-3 rounded-xl transition-all ${
                      platform === p.id
                        ? 'bg-lavender text-white scale-105'
                        : 'bg-white/10 text-white/70 hover:bg-white/20'
                    }`}
                  >
                    <div className="text-2xl mb-1">{p.icon}</div>
                    <div className="text-xs">{p.name}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-white/80 mb-2 font-medium">Date</label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-white/80 mb-2 font-medium">Time</label>
                <input
                  type="time"
                  value={time}
                  onChange={(e) => setTime(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none"
                />
              </div>
            </div>

            <button
              onClick={handleSchedule}
              disabled={!content || !date || !time || loading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '⏳ Scheduling...' : '📅 Schedule Post'}
            </button>
          </div>
        </div>
      </div>

      {/* Scheduled Posts */}
      <div className="flex-1">
        <div className="glass-effect p-6 rounded-2xl border border-lavender/30 h-full fade-in">
          <h3 className="text-2xl font-bold text-white mb-4 gradient-text">📋 Scheduled Posts</h3>
          
          <div className="space-y-3 overflow-auto h-[calc(100%-4rem)]">
            {scheduledPosts.map((post, index) => (
              <div
                key={post.id}
                className="bg-white/5 backdrop-blur-sm p-4 rounded-xl border border-white/10 hover:border-lavender/50 transition-all flip-in-hor-bottom"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">{platforms.find(p => p.name === post.platform)?.icon}</span>
                    <span className="text-white font-semibold">{post.platform}</span>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs ${
                    post.status === 'published' 
                      ? 'bg-cyan/20 text-cyan' 
                      : 'bg-lavender/20 text-lavender'
                  }`}>
                    {post.status}
                  </span>
                </div>
                
                <p className="text-white/80 text-sm mb-3">{post.content}</p>
                
                <div className="flex items-center justify-between text-xs text-white/60">
                  <span>📅 {post.date}</span>
                  <span>🕐 {post.time}</span>
                  <div className="flex gap-2">
                    <button className="hover:text-white transition-colors">✏️</button>
                    <button className="hover:text-white transition-colors">🗑️</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
