'use client'

import { useState, useEffect } from 'react'
import { API_ENDPOINTS, fetchAPI } from '@/lib/api'

interface ModelInfo {
  id: string
  name: string
  provider: string
  description: string
  capabilities: string[]
  cost_per_1k_tokens: number
  max_tokens: number
  is_available: boolean
  is_enabled: boolean
  performance_rating: number
  speed_rating: number
  quality_rating: number
}

interface ModelUsageStats {
  model_id: string
  model_name: string
  total_requests: number
  total_tokens: number
  total_cost: number
  success_rate: number
  avg_response_time_ms: number
  last_used: string | null
}

export default function ModelsContent() {
  const [models, setModels] = useState<ModelInfo[]>([])
  const [usageStats, setUsageStats] = useState<ModelUsageStats[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'models' | 'usage' | 'comparison'>('models')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch available models
      const modelsRes = await fetchAPI(`${API_ENDPOINTS.models}/available`)
      if (!modelsRes.ok) {
        const data = await modelsRes.json()
        throw new Error(data.detail || 'Failed to fetch models')
      }
      const modelsData = await modelsRes.json()
      setModels(modelsData)

      // Fetch usage stats
      const usageRes = await fetchAPI(`${API_ENDPOINTS.models}/usage`)
      if (!usageRes.ok) {
        const data = await usageRes.json()
        throw new Error(data.detail || 'Failed to fetch usage')
      }
      const usageData = await usageRes.json()
      setUsageStats(usageData)

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load models')
    } finally {
      setLoading(false)
    }
  }

  const toggleModel = async (modelId: string, currentState: boolean) => {
    try {
      const response = await fetchAPI(
        `${API_ENDPOINTS.models}/configure/${modelId}`,
        {
          method: 'POST',
          body: JSON.stringify({ is_enabled: !currentState })
        }
      )

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Failed to update model')
      }

      // Update local state
      setModels(models.map(m => 
        m.id === modelId ? { ...m, is_enabled: !currentState } : m
      ))

    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error'
      alert('Failed to update model: ' + message)
    }
  }

  const setPrimaryModel = async (modelId: string) => {
    try {
      const response = await fetchAPI(
        `${API_ENDPOINTS.models}/configure/${modelId}`,
        {
          method: 'POST',
          body: JSON.stringify({ is_enabled: true, is_primary: true })
        }
      )

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Failed to set primary model')
      }

      alert('✅ Primary model updated!')
      fetchData()

    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error'
      alert('Failed to set primary: ' + message)
    }
  }

  const getProviderColor = (provider: string) => {
    const colors: Record<string, string> = {
      'Google': 'bg-blue-500/20 text-blue-300',
      'OpenAI': 'bg-green-500/20 text-green-300',
      'Anthropic': 'bg-purple-500/20 text-purple-300',
      'Cohere': 'bg-orange-500/20 text-orange-300',
      'AWS Bedrock': 'bg-yellow-500/20 text-yellow-300',
      'Meta (via Together AI)': 'bg-pink-500/20 text-pink-300'
    }
    return colors[provider] || 'bg-gray-500/20 text-gray-300'
  }

  const getRatingColor = (rating: number) => {
    if (rating >= 9) return 'text-green-400'
    if (rating >= 7.5) return 'text-cyan'
    return 'text-yellow-400'
  }

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-lavender mx-auto mb-4"></div>
          <p className="text-white/60">Loading AI models...</p>
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
            onClick={fetchData}
            className="px-6 py-2 bg-gradient-to-r from-lavender to-purple rounded-lg text-white font-semibold hover:scale-105 transition-transform"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full p-8 space-y-6 overflow-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white gradient-text">⚙️ AI Model Configuration</h2>
          <p className="text-white/60 mt-1">Manage and configure your AI models</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="glass-effect p-2 rounded-2xl border border-periwinkle/30 flex gap-2">
        {[
          { id: 'models', label: 'Models', icon: '🤖' },
          { id: 'usage', label: 'Usage Stats', icon: '📊' },
          { id: 'comparison', label: 'Comparison', icon: '⚖️' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex-1 px-6 py-3 rounded-xl transition-all font-semibold flex items-center justify-center gap-2 ${
              activeTab === tab.id
                ? 'bg-gradient-to-r from-lavender to-purple text-white'
                : 'text-white/70 hover:bg-white/10'
            }`}
          >
            <span>{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {/* Models Tab */}
      {activeTab === 'models' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {models.map((model, index) => (
            <div
              key={model.id}
              className="glass-effect p-6 rounded-2xl border border-periwinkle/30 hover:border-lavender/50 transition-all flip-in-hor-bottom"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-white mb-1">{model.name}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getProviderColor(model.provider)}`}>
                    {model.provider}
                  </span>
                </div>
                <label className="relative inline-block w-12 h-6">
                  <input
                    type="checkbox"
                    checked={model.is_enabled}
                    onChange={() => toggleModel(model.id, model.is_enabled)}
                    className="sr-only peer"
                  />
                  <div className="w-12 h-6 bg-white/20 rounded-full peer peer-checked:bg-lavender transition-all cursor-pointer" />
                  <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full transition-all peer-checked:translate-x-6" />
                </label>
              </div>

              {/* Description */}
              <p className="text-white/70 text-sm mb-4">{model.description}</p>

              {/* Capabilities */}
              <div className="flex flex-wrap gap-1 mb-4">
                {model.capabilities.map((cap) => (
                  <span key={cap} className="px-2 py-1 bg-cyan/20 text-cyan rounded text-xs">
                    {cap}
                  </span>
                ))}
              </div>

              {/* Ratings */}
              <div className="space-y-2 mb-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-white/60">Performance</span>
                  <span className={`font-bold ${getRatingColor(model.performance_rating)}`}>
                    {model.performance_rating}/10
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-white/60">Speed</span>
                  <span className={`font-bold ${getRatingColor(model.speed_rating)}`}>
                    {model.speed_rating}/10
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-white/60">Quality</span>
                  <span className={`font-bold ${getRatingColor(model.quality_rating)}`}>
                    {model.quality_rating}/10
                  </span>
                </div>
              </div>

              {/* Pricing */}
              <div className="p-3 bg-white/5 rounded-xl mb-4">
                <div className="text-white/60 text-xs mb-1">Cost per 1K tokens</div>
                <div className="text-white font-bold">${model.cost_per_1k_tokens.toFixed(4)}</div>
              </div>

              {/* Actions */}
              <button
                onClick={() => setPrimaryModel(model.id)}
                disabled={!model.is_enabled}
                className="w-full px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ⭐ Set as Primary
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Usage Stats Tab */}
      {activeTab === 'usage' && (
        <div className="space-y-4">
          {usageStats.length === 0 ? (
            <div className="glass-effect p-12 rounded-2xl border border-periwinkle/30 text-center">
              <div className="text-6xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-white mb-2">No Usage Data Yet</h3>
              <p className="text-white/60">Start using AI models to see statistics here</p>
            </div>
          ) : (
            usageStats.map((stat, index) => (
              <div
                key={stat.model_id}
                className="glass-effect p-6 rounded-2xl border border-lavender/30 slide-in-blurred-left"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-white gradient-text">{stat.model_name}</h3>
                  <span className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-sm font-semibold">
                    {stat.success_rate.toFixed(1)}% Success
                  </span>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-white/5 p-4 rounded-xl">
                    <div className="text-white/60 text-sm mb-1">Total Requests</div>
                    <div className="text-2xl font-bold text-white">{stat.total_requests.toLocaleString()}</div>
                  </div>
                  <div className="bg-white/5 p-4 rounded-xl">
                    <div className="text-white/60 text-sm mb-1">Total Tokens</div>
                    <div className="text-2xl font-bold text-cyan">{stat.total_tokens.toLocaleString()}</div>
                  </div>
                  <div className="bg-white/5 p-4 rounded-xl">
                    <div className="text-white/60 text-sm mb-1">Total Cost</div>
                    <div className="text-2xl font-bold text-lavender">${stat.total_cost.toFixed(2)}</div>
                  </div>
                  <div className="bg-white/5 p-4 rounded-xl">
                    <div className="text-white/60 text-sm mb-1">Avg Response</div>
                    <div className="text-2xl font-bold text-periwinkle">{stat.avg_response_time_ms.toFixed(0)}ms</div>
                  </div>
                </div>

                {stat.last_used && (
                  <div className="mt-4 text-white/60 text-sm">
                    Last used: {new Date(stat.last_used).toLocaleString()}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* Comparison Tab */}
      {activeTab === 'comparison' && (
        <div className="glass-effect p-6 rounded-2xl border border-periwinkle/30">
          <h3 className="text-xl font-bold text-white gradient-text mb-6">Model Comparison</h3>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left text-white/80 font-semibold p-3">Model</th>
                  <th className="text-left text-white/80 font-semibold p-3">Provider</th>
                  <th className="text-center text-white/80 font-semibold p-3">Performance</th>
                  <th className="text-center text-white/80 font-semibold p-3">Speed</th>
                  <th className="text-center text-white/80 font-semibold p-3">Quality</th>
                  <th className="text-right text-white/80 font-semibold p-3">Cost/1K</th>
                  <th className="text-right text-white/80 font-semibold p-3">Max Tokens</th>
                </tr>
              </thead>
              <tbody>
                {models.sort((a, b) => b.performance_rating - a.performance_rating).map((model, index) => (
                  <tr
                    key={model.id}
                    className="border-b border-white/5 hover:bg-white/5 transition-colors fade-in"
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <td className="p-3">
                      <div className="font-semibold text-white">{model.name}</div>
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getProviderColor(model.provider)}`}>
                        {model.provider}
                      </span>
                    </td>
                    <td className="p-3 text-center">
                      <span className={`font-bold ${getRatingColor(model.performance_rating)}`}>
                        {model.performance_rating}
                      </span>
                    </td>
                    <td className="p-3 text-center">
                      <span className={`font-bold ${getRatingColor(model.speed_rating)}`}>
                        {model.speed_rating}
                      </span>
                    </td>
                    <td className="p-3 text-center">
                      <span className={`font-bold ${getRatingColor(model.quality_rating)}`}>
                        {model.quality_rating}
                      </span>
                    </td>
                    <td className="p-3 text-right text-white font-mono">
                      ${model.cost_per_1k_tokens.toFixed(4)}
                    </td>
                    <td className="p-3 text-right text-white/70">
                      {model.max_tokens.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
