'use client'

import { useState, useEffect } from 'react'
import Head from 'next/head'
import dynamic from 'next/dynamic'
import Sidebar from '@/components/Sidebar'

// Dynamically import SceneManager to avoid SSR issues
const SceneManager = dynamic(() => import('@/components/SceneManager'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-gradient-lavender">
      <div className="text-center">
        <div className="shimmer text-3xl font-bold mb-4">Loading Universe...</div>
        <div className="pulsate-fwd text-6xl">🌌</div>
      </div>
    </div>
  ),
})

export default function Dashboard() {
  const [currentScene, setCurrentScene] = useState('home')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const handleSceneChange = (scene: string) => {
    setCurrentScene(scene)
  }

  return (
    <>
      <Head>
        <title>Dashboard - Bharat Content AI</title>
        <meta name="description" content="AI-powered content creation dashboard" />
      </Head>

      <div className="flex h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        {/* Sidebar Navigation */}
        {mounted && <Sidebar currentScene={currentScene} onSceneChange={handleSceneChange} />}

        {/* Main Content Area - 3D Scene */}
        <main className="flex-1 ml-64 relative">
          {/* Background gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-br from-periwinkle/10 via-transparent to-purple/10 pointer-events-none" />

          {/* 3D Scene Canvas */}
          {mounted && (
            <div className="w-full h-full fade-in">
              <SceneManager currentScene={currentScene} />
            </div>
          )}

          {/* Floating UI Elements */}
          <div className="absolute top-8 right-8 z-10 space-y-4">
            {/* Status Card */}
            <div className="glass-effect px-6 py-4 rounded-2xl slide-in-top">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse" />
                <div>
                  <p className="text-white font-semibold">System Online</p>
                  <p className="text-white/60 text-sm">All services operational</p>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="glass-effect px-6 py-4 rounded-2xl space-y-3 slide-in-top" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center justify-between">
                <span className="text-white/70 text-sm">Content Generated</span>
                <span className="text-white font-bold">247</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-white/70 text-sm">Translations</span>
                <span className="text-white font-bold">1,432</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-white/70 text-sm">Scheduled Posts</span>
                <span className="text-white font-bold">18</span>
              </div>
            </div>
          </div>

          {/* Bottom Action Bar */}
          <div className="absolute bottom-8 right-8 z-10">
            <div className="flex gap-4">
              <button className="glass-effect px-6 py-3 rounded-xl text-white font-medium hover:scale-105 transition-all duration-300 glow">
                Quick Generate
              </button>
              <button className="glass-effect px-6 py-3 rounded-xl text-white font-medium hover:scale-105 transition-all duration-300">
                Settings
              </button>
            </div>
          </div>

          {/* Scene Info Panel */}
          <div className="absolute top-8 left-8 z-10">
            <div className="glass-effect px-6 py-4 rounded-2xl slide-in-top">
              <h2 className="text-white font-bold text-xl mb-2">
                {currentScene === 'home' && '🏠 Home Universe'}
                {currentScene === 'generate' && '✨ Content Generation'}
                {currentScene === 'translate' && '🌐 Translation Hub'}
                {currentScene === 'schedule' && '📅 Scheduler'}
                {currentScene === 'analytics' && '📊 Analytics'}
                {currentScene === 'voice' && '🎤 Voice Input'}
                {currentScene === 'profile' && '👤 Profile'}
              </h2>
              <p className="text-white/60 text-sm">
                {currentScene === 'home' && 'Welcome to your AI-powered content universe'}
                {currentScene === 'generate' && 'Create content with AI across 11 languages'}
                {currentScene === 'translate' && 'Translate content while maintaining tone'}
                {currentScene === 'schedule' && 'Schedule posts across social platforms'}
                {currentScene === 'analytics' && 'Track performance and engagement'}
                {currentScene === 'voice' && 'Speak your ideas, AI does the rest'}
                {currentScene === 'profile' && 'Manage your account and preferences'}
              </p>
            </div>
          </div>
        </main>
      </div>
    </>
  )
}
