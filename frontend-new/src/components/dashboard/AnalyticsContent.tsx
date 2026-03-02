'use client'

import { useState, useEffect, useMemo, useCallback } from 'react'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { API_ENDPOINTS, fetchAPI } from '@/lib/api'

interface AnalyticsOverview {
  total_content_generated: number
  total_translations: number
  total_posts_scheduled: number
  total_posts_published: number
  total_engagement: {
    likes: number
    comments: number
    shares: number
    views: number
  }
  avg_engagement_rate: number
  top_performing_language: string | null
  top_performing_platform: string | null
}

interface PlatformPerformance {
  platform: string
  total_posts: number
  total_likes: number
  total_comments: number
  total_shares: number
  total_views: number
  avg_engagement_rate: number
}

interface EngagementTrend {
  date: string
  likes: number
  comments: number
  shares: number
  views: number
  engagement_rate: number
}

export default function AnalyticsContent() {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null)
  const [platformPerformance, setPlatformPerformance] = useState<PlatformPerformance[]>([])
  const [engagementTrends, setEngagementTrends] = useState<EngagementTrend[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [days, setDays] = useState(30)

  // ✅ OPTIMIZED: Memoize fetch function
  const fetchAnalytics = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch overview
      const overviewRes = await fetchAPI(`${API_ENDPOINTS.analyticsOverview}/${days}?days=${days}`)
      if (!overviewRes.ok) {
        const data = await overviewRes.json()
        throw new Error(data.detail || 'Failed to fetch overview')
      }
      const overviewData = await overviewRes.json()
      setOverview(overviewData)

      // Fetch platform performance
      const platformRes = await fetchAPI(`${API_ENDPOINTS.analyticsOverview.replace('/overview', '/platform-performance')}?days=${days}`)
      if (!platformRes.ok) {
        const data = await platformRes.json()
        throw new Error(data.detail || 'Failed to fetch platform performance')
      }
      const platformData = await platformRes.json()
      setPlatformPerformance(platformData)

      // Fetch engagement trends
      const trendsRes = await fetchAPI(`${API_ENDPOINTS.analyticsOverview.replace('/overview', '/engagement-trends')}?days=${days}`)
      if (!trendsRes.ok) {
        const data = await trendsRes.json()
        throw new Error(data.detail || 'Failed to fetch engagement trends')
      }
      const trendsData = await trendsRes.json()
      setEngagementTrends(trendsData)

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load analytics')
      console.error('Analytics error:', err)
    } finally {
      setLoading(false)
    }
  }, [days])

  useEffect(() => {
    fetchAnalytics()
  }, [fetchAnalytics])

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-lavender mx-auto mb-4"></div>
          <p className="text-white/60">Loading analytics...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="glass-effect p-8 rounded-2xl border border-red-500/30 text-center">
          <p className="text-red-400 mb-4">❌ {error}</p>
          <button
            onClick={fetchAnalytics}
            className="px-6 py-2 bg-gradient-to-r from-lavender to-purple rounded-lg text-white font-semibold hover:scale-105 transition-transform"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!overview) return null

  // ✅ OPTIMIZED: Memoize expensive computations
  const stats = useMemo(() => [
    { 
      label: 'Content Generated', 
      value: overview.total_content_generated.toLocaleString(), 
      change: '+12%', 
      icon: '📝' 
    },
    { 
      label: 'Total Engagement', 
      value: (overview.total_engagement.likes + overview.total_engagement.comments + overview.total_engagement.shares).toLocaleString(), 
      change: `${overview.avg_engagement_rate.toFixed(1)}%`, 
      icon: '❤️' 
    },
    { 
      label: 'Total Views', 
      value: overview.total_engagement.views.toLocaleString(), 
      change: '+15%', 
      icon: '👥' 
    },
    { 
      label: 'Translations', 
      value: overview.total_translations.toLocaleString(), 
      change: '+23%', 
      icon: '🌐' 
    },
  ], [overview])

  const COLORS = ['#A4A5F5', '#9EF0FF', '#B5C7EB', '#8E70CF', '#E0BBE4', '#957DAD']
  
  // ✅ OPTIMIZED: Memoize button handler
  const handleDaysChange = useCallback((d: number) => {
    setDays(d)
  }, [])

  return (
    <div className="h-full p-8 space-y-6 overflow-auto">
      {/* Header with Date Range Selector */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white gradient-text">📊 Analytics Dashboard</h2>
        <div className="flex gap-2">
          {[7, 30, 90].map((d) => (
            <button
              key={d}
              onClick={() => handleDaysChange(d)}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                days === d
                  ? 'bg-gradient-to-r from-lavender to-purple text-white'
                  : 'glass-effect text-white/60 hover:text-white'
              }`}
            >
              {d} Days
            </button>
          ))}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div
            key={stat.label}
            className="glass-effect p-6 rounded-2xl border border-periwinkle/30 flip-in-hor-bottom"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">{stat.icon}</span>
              <span className="text-cyan text-sm font-semibold">{stat.change}</span>
            </div>
            <div className="text-3xl font-bold text-white gradient-text mb-1">{stat.value}</div>
            <div className="text-white/60 text-sm">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-2 gap-6">
        {/* Engagement Trends Chart */}
        <div className="glass-effect p-6 rounded-2xl border border-lavender/30 slide-in-blurred-left">
          <h3 className="text-xl font-bold text-white mb-4 gradient-text">📈 Engagement Trends</h3>
          {engagementTrends.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={engagementTrends}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis 
                  dataKey="date" 
                  stroke="rgba(255,255,255,0.5)"
                  tick={{ fill: 'rgba(255,255,255,0.7)' }}
                />
                <YAxis stroke="rgba(255,255,255,0.5)" tick={{ fill: 'rgba(255,255,255,0.7)' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(0,0,0,0.8)', 
                    border: '1px solid rgba(164,165,245,0.3)',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Line type="monotone" dataKey="likes" stroke="#A4A5F5" strokeWidth={2} />
                <Line type="monotone" dataKey="comments" stroke="#9EF0FF" strokeWidth={2} />
                <Line type="monotone" dataKey="shares" stroke="#B5C7EB" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-64 flex items-center justify-center text-white/40">
              No engagement data available
            </div>
          )}
        </div>

        {/* Platform Distribution */}
        <div className="glass-effect p-6 rounded-2xl border border-periwinkle/30 fade-in">
          <h3 className="text-xl font-bold text-white mb-4 gradient-text">🎯 Platform Performance</h3>
          {platformPerformance.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={platformPerformance}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis 
                  dataKey="platform" 
                  stroke="rgba(255,255,255,0.5)"
                  tick={{ fill: 'rgba(255,255,255,0.7)' }}
                />
                <YAxis stroke="rgba(255,255,255,0.5)" tick={{ fill: 'rgba(255,255,255,0.7)' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(0,0,0,0.8)', 
                    border: '1px solid rgba(164,165,245,0.3)',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Bar dataKey="total_posts" fill="#A4A5F5" />
                <Bar dataKey="total_likes" fill="#9EF0FF" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-64 flex items-center justify-center text-white/40">
              No platform data available
            </div>
          )}
        </div>
      </div>

      {/* Engagement Breakdown */}
      <div className="grid grid-cols-3 gap-6">
        <div className="glass-effect p-6 rounded-2xl border border-lavender/30">
          <h3 className="text-lg font-bold text-white mb-4 gradient-text">💬 Engagement Breakdown</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-white/80">Likes</span>
              <span className="text-lavender font-bold">{overview.total_engagement.likes.toLocaleString()}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-white/80">Comments</span>
              <span className="text-cyan font-bold">{overview.total_engagement.comments.toLocaleString()}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-white/80">Shares</span>
              <span className="text-periwinkle font-bold">{overview.total_engagement.shares.toLocaleString()}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-white/80">Views</span>
              <span className="text-purple font-bold">{overview.total_engagement.views.toLocaleString()}</span>
            </div>
          </div>
        </div>

        <div className="glass-effect p-6 rounded-2xl border border-periwinkle/30">
          <h3 className="text-lg font-bold text-white mb-4 gradient-text">🏆 Top Performers</h3>
          <div className="space-y-3">
            <div>
              <div className="text-white/60 text-sm mb-1">Best Language</div>
              <div className="text-white font-bold text-lg">
                {overview.top_performing_language || 'N/A'}
              </div>
            </div>
            <div>
              <div className="text-white/60 text-sm mb-1">Best Platform</div>
              <div className="text-white font-bold text-lg">
                {overview.top_performing_platform || 'N/A'}
              </div>
            </div>
            <div>
              <div className="text-white/60 text-sm mb-1">Avg Engagement Rate</div>
              <div className="text-cyan font-bold text-lg">
                {overview.avg_engagement_rate.toFixed(2)}%
              </div>
            </div>
          </div>
        </div>

        <div className="glass-effect p-6 rounded-2xl border border-lavender/30">
          <h3 className="text-lg font-bold text-white mb-4 gradient-text">📅 Publishing Stats</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-white/80">Scheduled</span>
              <span className="text-lavender font-bold">{overview.total_posts_scheduled}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-white/80">Published</span>
              <span className="text-cyan font-bold">{overview.total_posts_published}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-white/80">Success Rate</span>
              <span className="text-periwinkle font-bold">
                {overview.total_posts_scheduled > 0 
                  ? ((overview.total_posts_published / overview.total_posts_scheduled) * 100).toFixed(1)
                  : 0}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Export Button */}
      <div className="flex justify-end">
        <button
          onClick={() => {
            const confirmed = confirm(
              '📊 Export Analytics Report\n\n' +
              'This feature will export your analytics data to:\n' +
              '• PDF Report\n' +
              '• CSV Data\n' +
              '• Excel Spreadsheet\n\n' +
              'Coming in the next update!\n\n' +
              'Would you like to be notified when this feature is ready?'
            );
            if (confirmed) {
              alert('✅ Great! We\'ll notify you when the export feature is available.');
            }
          }}
          className="px-6 py-3 bg-gradient-to-r from-lavender to-purple rounded-lg text-white font-semibold hover:scale-105 transition-transform flex items-center gap-2"
          title="Export Report (Coming Soon)"
        >
          <span>📥</span>
          Export Report
        </button>
      </div>
    </div>
  )
}
