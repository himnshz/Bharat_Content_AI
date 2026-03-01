'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import Head from 'next/head'

// Dynamically import Hero3D to avoid SSR issues with Three.js
const Hero3D = dynamic(() => import('@/components/Hero3D'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[600px] flex items-center justify-center">
      <div className="shimmer text-2xl font-bold">Loading 3D Scene...</div>
    </div>
  ),
})

export default function Home() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  return (
    <>
      <Head>
        <title>Bharat Content AI - Multilingual Smart Content Assistant</title>
        <meta name="description" content="AI-powered multilingual content creation for Indian languages" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          {/* Background gradient */}
          <div className="absolute inset-0 bg-gradient-lavender opacity-10"></div>
          
          <div className="container mx-auto px-4 py-20">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Left: Text Content */}
              <div className="space-y-8 slide-in-top">
                <div className="inline-block">
                  <span className="px-4 py-2 bg-lavender-100 text-lavender-700 rounded-full text-sm font-semibold">
                    🚀 AI for Bharat Hackathon
                  </span>
                </div>

                <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                  <span className="gradient-text text-focus-in">
                    Bharat Content AI
                  </span>
                </h1>

                <p className="text-xl lg:text-2xl text-gray-600 fade-in">
                  Multilingual Smart Content Assistant for Indian Languages
                </p>

                <p className="text-lg text-gray-500">
                  Generate, translate, and schedule content across 11 Indian languages with AI-powered intelligence.
                </p>

                {/* Feature Pills */}
                <div className="flex flex-wrap gap-3">
                  {['Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi', 'Gujarati'].map((lang, i) => (
                    <span
                      key={lang}
                      className="px-4 py-2 bg-white border-2 border-lavender-200 rounded-full text-sm font-medium text-gray-700 hover:border-lavender-400 transition-all duration-300 hover:scale-105"
                      style={{ animationDelay: `${i * 0.1}s` }}
                    >
                      {lang}
                    </span>
                  ))}
                  <span className="px-4 py-2 bg-white border-2 border-lavender-200 rounded-full text-sm font-medium text-gray-700">
                    +5 more
                  </span>
                </div>

                {/* CTA Buttons */}
                <div className="flex flex-wrap gap-4 pt-4">
                  <a href="/dashboard">
                    <button className="btn-primary scale-in-center">
                      Enter Universe 🚀
                    </button>
                  </a>
                  <button className="px-8 py-4 bg-white border-2 border-gray-300 rounded-xl font-semibold text-gray-700 hover:border-lavender-500 hover:text-lavender-600 transition-all duration-300 hover:scale-105">
                    View Demo
                  </button>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-6 pt-8 border-t border-gray-200">
                  <div className="text-center">
                    <div className="text-3xl font-bold gradient-text">11</div>
                    <div className="text-sm text-gray-500">Languages</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold gradient-text">8</div>
                    <div className="text-sm text-gray-500">AI Models</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold gradient-text">5</div>
                    <div className="text-sm text-gray-500">Platforms</div>
                  </div>
                </div>
              </div>

              {/* Right: 3D Animation */}
              <div className="relative">
                {mounted && <Hero3D />}
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4 gradient-text">
                Powerful Features
              </h2>
              <p className="text-xl text-gray-600">
                Everything you need for multilingual content creation
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <div
                  key={feature.title}
                  className="p-8 bg-gradient-to-br from-white to-gray-50 rounded-2xl border-2 border-gray-100 card-hover"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="text-5xl mb-4">{feature.icon}</div>
                  <h3 className="text-2xl font-bold mb-3 text-gray-800">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gradient-lavender">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl lg:text-5xl font-bold text-white mb-6">
              Ready to Transform Your Content?
            </h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Join thousands of creators, businesses, and educators using Bharat Content AI
            </p>
            <button className="px-12 py-5 bg-white text-lavender-600 rounded-xl font-bold text-lg hover:scale-105 transition-all duration-300 glow">
              <a href="/dashboard">Launch Dashboard</a>
            </button>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-12 bg-gray-900 text-white">
          <div className="container mx-auto px-4 text-center">
            <p className="text-gray-400">
              © 2024 Bharat Content AI. Built for AI for Bharat Hackathon.
            </p>
            <div className="mt-4 flex justify-center gap-6">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                GitHub
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                Documentation
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                API
              </a>
            </div>
          </div>
        </footer>
      </main>
    </>
  )
}

const features = [
  {
    icon: '🤖',
    title: 'AI Content Generation',
    description: 'Generate high-quality content in multiple Indian languages using advanced AI models including Gemini, GPT, and Claude.',
  },
  {
    icon: '🌐',
    title: 'Smart Translation',
    description: 'Translate content across 11 Indian languages with IndicTrans, maintaining tone and cultural context.',
  },
  {
    icon: '📅',
    title: 'Social Scheduling',
    description: 'Schedule and publish content across Twitter, Facebook, Instagram, LinkedIn, and YouTube automatically.',
  },
  {
    icon: '📊',
    title: 'Analytics Dashboard',
    description: 'Track engagement, views, and performance metrics across all platforms and languages in real-time.',
  },
  {
    icon: '🎤',
    title: 'Voice Input',
    description: 'Speak your ideas in any Indian language and let AI transcribe and generate content automatically.',
  },
  {
    icon: '✨',
    title: 'Tone Customization',
    description: 'Choose from 8 different tones - professional, casual, friendly, formal, humorous, and more.',
  },
]
