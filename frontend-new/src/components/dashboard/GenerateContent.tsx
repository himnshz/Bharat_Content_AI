'use client'

import { useState } from 'react'
import { API_ENDPOINTS, fetchAPI, handleAPIError, CONTENT_TYPE_MAP, TONE_MAP } from '@/lib/api'

export default function GenerateContent() {
  const [prompt, setPrompt] = useState('')
  const [language, setLanguage] = useState('hindi')
  const [tone, setTone] = useState('professional')
  const [contentType, setContentType] = useState('blog_post')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const languages = ['Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi', 'Gujarati', 'Kannada', 'Malayalam', 'Punjabi', 'Odia', 'Assamese']
  const tones = ['Professional', 'Casual', 'Friendly', 'Formal', 'Humorous', 'Inspirational', 'Persuasive', 'Informative']
  const contentTypes = [
    { value: 'blog_post', label: 'Blog Post' },
    { value: 'social_media', label: 'Social Media' },
    { value: 'article', label: 'Article' },
    { value: 'product_description', label: 'Product Description' },
  ]

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    setLoading(true)
    setError('')
    
    try {
      // Map frontend values to backend enum values
      const mappedContentType = CONTENT_TYPE_MAP[contentType] || 'SOCIAL_POST'
      const mappedTone = TONE_MAP[tone] || 'CASUAL'
      
      const response = await fetchAPI(API_ENDPOINTS.generateContent, {
        method: 'POST',
        body: JSON.stringify({
          prompt: prompt,
          language: language.toLowerCase(),
          tone: mappedTone,
          content_type: mappedContentType,
          max_length: 500
        }),
      })

      if (!response.ok) {
        await handleAPIError(response)
      }

      const data = await response.json()
      setOutput(data.generated_content || data.content || 'Content generated successfully!')
    } catch (err) {
      console.error('Generation error:', err)
      setError(err instanceof Error ? err.message : 'Failed to generate content. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(output)
    alert('Copied to clipboard!')
  }

  return (
    <div className="h-full flex gap-6 p-8">
      {/* Input Section */}
      <div className="flex-1 space-y-6">
        <div className="glass-effect p-6 rounded-2xl border border-periwinkle/30 slide-in-blurred-left">
          <h3 className="text-2xl font-bold text-white mb-4 gradient-text">✨ Content Generation</h3>
          
          {error && (
            <div className="mb-4 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200">
              {error}
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <label className="block text-white/80 mb-2 font-medium">What do you want to create?</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your content idea... (e.g., 'Write a blog post about AI in education')"
                className="w-full h-32 px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none resize-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-white/80 mb-2 font-medium">Language</label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none"
                >
                  {languages.map(lang => (
                    <option key={lang} value={lang.toLowerCase()} className="bg-purple-900">{lang}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-white/80 mb-2 font-medium">Tone</label>
                <select
                  value={tone}
                  onChange={(e) => setTone(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none"
                >
                  {tones.map(t => (
                    <option key={t} value={t.toLowerCase()} className="bg-purple-900">{t}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-white/80 mb-2 font-medium">Content Type</label>
              <select
                value={contentType}
                onChange={(e) => setContentType(e.target.value)}
                className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none"
              >
                {contentTypes.map(type => (
                  <option key={type.value} value={type.value} className="bg-purple-900">{type.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-white/80 mb-2 font-medium">Reference Content (Optional)</label>
              <div className="border-2 border-dashed border-periwinkle/30 rounded-xl p-6 text-center hover:border-lavender transition-all cursor-pointer">
                <input type="file" className="hidden" id="file-upload" />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <div className="text-4xl mb-2">📎</div>
                  <p className="text-white/60">Click to upload reference files</p>
                  <p className="text-white/40 text-sm mt-1">PDF, DOC, TXT supported</p>
                </label>
              </div>
            </div>

            <button
              onClick={handleGenerate}
              disabled={!prompt || loading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '✨ Generating...' : '🚀 Generate Content'}
            </button>
          </div>
        </div>
      </div>

      {/* Output Section */}
      <div className="flex-1 space-y-6">
        <div className="glass-effect p-6 rounded-2xl border border-lavender/30 h-full fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-2xl font-bold text-white gradient-text">📝 Generated Output</h3>
            {output && (
              <button 
                onClick={handleCopy}
                className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-all"
              >
                📋 Copy
              </button>
            )}
          </div>
          
          {output ? (
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 h-[calc(100%-4rem)] overflow-auto">
              <pre className="text-white/90 whitespace-pre-wrap font-sans">{output}</pre>
            </div>
          ) : (
            <div className="flex items-center justify-center h-[calc(100%-4rem)] text-white/40">
              <div className="text-center">
                <div className="text-6xl mb-4 floating">✨</div>
                <p>Your generated content will appear here</p>
                <p className="text-sm mt-2">Powered by AI • Supports 11 Indian Languages</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
