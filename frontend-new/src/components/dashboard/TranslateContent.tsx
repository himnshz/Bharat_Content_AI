'use client'

import { useState } from 'react'
import { API_ENDPOINTS, fetchAPI } from '@/lib/api'

export default function TranslateContent() {
  const [sourceText, setSourceText] = useState('')
  const [translatedText, setTranslatedText] = useState('')
  const [sourceLang, setSourceLang] = useState('english')
  const [targetLang, setTargetLang] = useState('hindi')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi', 'Gujarati', 'Kannada', 'Malayalam', 'Punjabi', 'Odia', 'Assamese']

  const handleTranslate = async () => {
    // Validation
    if (!sourceText.trim()) {
      setError('Please enter text to translate')
      return
    }
    
    if (sourceText.length > 10000) {
      setError('Text too long. Maximum 10,000 characters.')
      return
    }
    
    if (sourceLang === targetLang) {
      setError('Source and target languages must be different')
      return
    }
    
    setLoading(true)
    setError('')
    
    try {
      const response = await fetchAPI(`${API_ENDPOINTS.translateDirect}`, {
        method: 'POST',
        body: JSON.stringify({
          text: sourceText,
          source_language: sourceLang,
          target_language: targetLang,
        }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setTranslatedText(data.translated_text || 'Translation completed!')
    } catch (err) {
      console.error('Translation error:', err)
      const message = err instanceof Error ? err.message : 'Failed to translate. Please try again.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const swapLanguages = () => {
    setSourceLang(targetLang)
    setTargetLang(sourceLang)
    setSourceText(translatedText)
    setTranslatedText(sourceText)
  }

  return (
    <div className="h-full flex gap-6 p-8">
      {/* Source Section */}
      <div className="flex-1 space-y-4">
        <div className="glass-effect p-6 rounded-2xl border border-periwinkle/30 h-full slide-in-blurred-left">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-white gradient-text">🌐 Source</h3>
            <select
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
              className="px-4 py-2 bg-white/10 backdrop-blur-sm border-2 border-periwinkle/30 rounded-lg text-white focus:border-lavender focus:outline-none"
            >
              {languages.map(lang => (
                <option key={lang} value={lang.toLowerCase()} className="bg-purple-900">{lang}</option>
              ))}
            </select>
          </div>
          
          {error && (
            <div className="mb-4 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm">
              <div className="flex items-center gap-2">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            </div>
          )}
          
          <textarea
            value={sourceText}
            onChange={(e) => setSourceText(e.target.value)}
            placeholder="Enter text to translate..."
            className="w-full h-[calc(100%-8rem)] px-4 py-3 bg-white/5 backdrop-blur-sm border-2 border-periwinkle/20 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none resize-none"
          />

          <div className="mt-4 flex gap-2">
            <button
              onClick={handleTranslate}
              disabled={!sourceText || loading}
              className="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '🔄 Translating...' : '→ Translate'}
            </button>
            <button
              onClick={swapLanguages}
              className="px-4 py-3 bg-white/10 hover:bg-white/20 rounded-xl text-white transition-all"
              title="Swap languages"
            >
              ⇄
            </button>
          </div>
        </div>
      </div>

      {/* Target Section */}
      <div className="flex-1 space-y-4">
        <div className="glass-effect p-6 rounded-2xl border border-lavender/30 h-full fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-white gradient-text">🎯 Translation</h3>
            <select
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
              className="px-4 py-2 bg-white/10 backdrop-blur-sm border-2 border-lavender/30 rounded-lg text-white focus:border-cyan focus:outline-none"
            >
              {languages.map(lang => (
                <option key={lang} value={lang.toLowerCase()} className="bg-purple-900">{lang}</option>
              ))}
            </select>
          </div>
          
          {translatedText ? (
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 h-[calc(100%-8rem)] overflow-auto">
              <pre className="text-white/90 whitespace-pre-wrap font-sans">{translatedText}</pre>
            </div>
          ) : (
            <div className="flex items-center justify-center h-[calc(100%-8rem)] text-white/40 border-2 border-dashed border-white/10 rounded-xl">
              <div className="text-center">
                <div className="text-6xl mb-4 floating">🌍</div>
                <p>Translation will appear here</p>
              </div>
            </div>
          )}

          {translatedText && (
            <div className="mt-4">
              <button className="w-full px-4 py-3 bg-white/10 hover:bg-white/20 rounded-xl text-white transition-all">
                📋 Copy Translation
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
