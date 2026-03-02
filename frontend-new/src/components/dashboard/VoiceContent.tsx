'use client'

import { useState } from 'react'

export default function VoiceContent() {
  const [isRecording, setIsRecording] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [language, setLanguage] = useState('hindi')
  const [audioFile, setAudioFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)

  const languages = ['Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi', 'Gujarati', 'Kannada', 'Malayalam', 'Punjabi', 'English']

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    
    setAudioFile(file)
    setLoading(true)
    
    try {
      const formData = new FormData()
      formData.append('audio_file', file)
      formData.append('language', language)
      
      const response = await fetch('http://127.0.0.1:8000/api/voice/transcribe', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setTranscript(data.transcript || data.text || 'Transcription completed!')
    } catch (err) {
      console.error('Transcription error:', err)
      setTranscript('Failed to transcribe audio. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const toggleRecording = () => {
    setIsRecording(!isRecording)
    if (!isRecording) {
      // Simulate recording
      setTimeout(() => {
        setTranscript('This is a sample transcription of your voice input. The AI will convert your speech to text in the selected language.')
        setIsRecording(false)
      }, 3000)
    }
  }

  return (
    <div className="h-full flex gap-6 p-8">
      {/* Recording Section */}
      <div className="flex-1 flex items-center justify-center">
        <div className="glass-effect p-12 rounded-3xl border border-periwinkle/30 text-center slide-in-blurred-left max-w-md w-full">
          <h3 className="text-2xl font-bold text-white mb-6 gradient-text">🎤 Voice Input</h3>
          
          <div className="mb-8">
            <label className="block text-white/80 mb-3 font-medium">Select Language</label>
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

          <div className="relative mb-8">
            <button
              onClick={toggleRecording}
              className={`w-32 h-32 rounded-full flex items-center justify-center text-6xl transition-all duration-300 ${
                isRecording
                  ? 'bg-red-500 animate-pulse scale-110'
                  : 'bg-gradient-to-br from-lavender to-purple hover:scale-110'
              }`}
            >
              {isRecording ? '⏸️' : '🎤'}
            </button>
            
            {isRecording && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-40 h-40 border-4 border-cyan rounded-full animate-ping opacity-20" />
                <div className="w-48 h-48 border-4 border-lavender rounded-full animate-ping opacity-10 absolute" style={{ animationDelay: '0.5s' }} />
              </div>
            )}
          </div>

          <p className="text-white/80 mb-4">
            {loading ? '⏳ Processing audio...' : isRecording ? '🔴 Recording... Speak now' : 'Click the microphone to start recording'}
          </p>

          <div className="mb-6">
            <label className="block text-white/80 mb-2 text-sm">Or upload an audio file:</label>
            <input
              type="file"
              accept="audio/*"
              onChange={handleFileUpload}
              className="w-full text-sm text-white/70 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-lavender/20 file:text-white hover:file:bg-lavender/30 file:cursor-pointer"
            />
          </div>

          <div className="flex gap-2 justify-center">
            <div className={`w-2 h-8 bg-cyan rounded-full ${isRecording ? 'animate-pulse' : 'opacity-30'}`} />
            <div className={`w-2 h-12 bg-lavender rounded-full ${isRecording ? 'animate-pulse' : 'opacity-30'}`} style={{ animationDelay: '0.1s' }} />
            <div className={`w-2 h-10 bg-periwinkle rounded-full ${isRecording ? 'animate-pulse' : 'opacity-30'}`} style={{ animationDelay: '0.2s' }} />
            <div className={`w-2 h-14 bg-purple rounded-full ${isRecording ? 'animate-pulse' : 'opacity-30'}`} style={{ animationDelay: '0.3s' }} />
            <div className={`w-2 h-10 bg-cyan rounded-full ${isRecording ? 'animate-pulse' : 'opacity-30'}`} style={{ animationDelay: '0.4s' }} />
            <div className={`w-2 h-12 bg-lavender rounded-full ${isRecording ? 'animate-pulse' : 'opacity-30'}`} style={{ animationDelay: '0.5s' }} />
            <div className={`w-2 h-8 bg-periwinkle rounded-full ${isRecording ? 'animate-pulse' : 'opacity-30'}`} style={{ animationDelay: '0.6s' }} />
          </div>
        </div>
      </div>

      {/* Transcript Section */}
      <div className="flex-1">
        <div className="glass-effect p-6 rounded-2xl border border-lavender/30 h-full fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-2xl font-bold text-white gradient-text">📝 Transcript</h3>
            {transcript && (
              <div className="flex gap-2">
                <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-all">
                  📋 Copy
                </button>
                <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-all">
                  ✨ Generate Content
                </button>
              </div>
            )}
          </div>
          
          {transcript ? (
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 h-[calc(100%-5rem)] overflow-auto">
              <p className="text-white/90 text-lg leading-relaxed">{transcript}</p>
            </div>
          ) : (
            <div className="flex items-center justify-center h-[calc(100%-5rem)] text-white/40 border-2 border-dashed border-white/10 rounded-xl">
              <div className="text-center">
                <div className="text-6xl mb-4 floating">🎙️</div>
                <p>Your voice transcript will appear here</p>
                <p className="text-sm mt-2">Start recording to see the magic!</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
