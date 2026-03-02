'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Hero3D from '@/components/Hero3D'

export default function Home() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  return (
    <main className="min-h-screen bg-gradient-to-br from-periwinkle-50 via-white to-lavender-50">
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-lavender opacity-20" />
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-periwinkle rounded-full opacity-10 blur-3xl animate-floating" />
          <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-lavender rounded-full opacity-10 blur-3xl animate-floating" style={{ animationDelay: '1s' }} />
        </div>

        <div className="container mx-auto px-4 py-20 relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8 slide-in-blurred-left">
              <div className="inline-block bounce-in">
                <span className="px-4 py-2 bg-lavender/20 text-purple rounded-full text-sm font-semibold backdrop-blur-sm border border-lavender/30">
                  🚀 AI for Bharat Hackathon
                </span>
              </div>

              <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                <span className="gradient-text tracking-in-expand">
                  Bharat Content AI
                </span>
              </h1>

              <p className="text-xl lg:text-2xl text-purple-800 fade-in">
                Multilingual Smart Content Assistant for Indian Languages
              </p>

              <p className="text-lg text-purple-600 fade-in" style={{ animationDelay: '0.5s' }}>
                Generate, translate, and schedule content across 11 Indian languages with AI-powered intelligence.
              </p>

              <div className="flex flex-wrap gap-3 fade-in" style={{ animationDelay: '0.7s' }}>
                {['Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi', 'Gujarati'].map((lang, i) => (
                  <span
                    key={lang}
                    className="px-4 py-2 bg-white/80 backdrop-blur-sm border-2 border-periwinkle rounded-full text-sm font-medium text-purple-700 hover:border-lavender hover:bg-lavender/10 transition-all duration-300 hover:scale-105 flip-in-hor-bottom"
                    style={{ animationDelay: `${0.8 + i * 0.1}s` }}
                  >
                    {lang}
                  </span>
                ))}
                <span className="px-4 py-2 bg-white/80 backdrop-blur-sm border-2 border-periwinkle rounded-full text-sm font-medium text-purple-700 flip-in-hor-bottom" style={{ animationDelay: '1.4s' }}>
                  +5 more
                </span>
              </div>

              <div className="flex flex-wrap gap-4 pt-4">
                <Link href="/register">
                  <button className="btn-primary bounce-in" style={{ animationDelay: '1s' }}>
                    Get Started Free 🚀
                  </button>
                </Link>
                <Link href="/login">
                  <button className="px-8 py-4 bg-white/80 backdrop-blur-sm border-2 border-periwinkle rounded-xl font-semibold text-purple-700 hover:border-lavender hover:bg-lavender/10 transition-all duration-300 hover:scale-105 bounce-in" style={{ animationDelay: '1.1s' }}>
                    Sign In
                  </button>
                </Link>
              </div>

              <div className="grid grid-cols-3 gap-6 pt-8 border-t border-periwinkle/30 fade-in" style={{ animationDelay: '1.2s' }}>
                <div className="text-center pulsate">
                  <div className="text-3xl font-bold gradient-text">11</div>
                  <div className="text-sm text-purple-600">Languages</div>
                </div>
                <div className="text-center pulsate" style={{ animationDelay: '0.2s' }}>
                  <div className="text-3xl font-bold gradient-text">8</div>
                  <div className="text-sm text-purple-600">AI Models</div>
                </div>
                <div className="text-center pulsate" style={{ animationDelay: '0.4s' }}>
                  <div className="text-3xl font-bold gradient-text">5</div>
                  <div className="text-sm text-purple-600">Platforms</div>
                </div>
              </div>
            </div>

            <div className="relative rotate-in-center">
              {mounted && <Hero3D />}
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16 slide-in-top">
            <h2 className="text-4xl font-bold mb-4 gradient-text tracking-in-expand">
              Powerful Features
            </h2>
            <p className="text-xl text-purple-600 fade-in">
              Everything you need for multilingual content creation
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="p-8 bg-gradient-to-br from-white/80 to-periwinkle-50/50 backdrop-blur-sm rounded-2xl border-2 border-periwinkle/30 card-hover flip-in-hor-bottom"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="text-5xl mb-4 floating" style={{ animationDelay: `${index * 0.2}s` }}>{feature.icon}</div>
                <h3 className="text-2xl font-bold mb-3 text-purple-800">
                  {feature.title}
                </h3>
                <p className="text-purple-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 bg-gradient-lavender relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-cyan rounded-full blur-3xl animate-floating" />
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-periwinkle rounded-full blur-3xl animate-floating" style={{ animationDelay: '1s' }} />
        </div>
        <div className="container mx-auto px-4 text-center relative z-10">
          <h2 className="text-4xl lg:text-5xl font-bold text-white mb-6 tracking-in-expand">
            Ready to Transform Your Content?
          </h2>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto fade-in">
            Join thousands of creators, businesses, and educators using Bharat Content AI
          </p>
          <Link href="/dashboard">
            <button className="px-12 py-5 bg-white text-purple rounded-xl font-bold text-lg hover:scale-105 transition-all duration-300 glow bounce-in">
              Launch Dashboard
            </button>
          </Link>
        </div>
      </section>

      <footer className="py-12 bg-purple-900 text-white">
        <div className="container mx-auto px-4 text-center">
          <p className="text-purple-200 fade-in">
            © 2024 Bharat Content AI. Built for AI for Bharat Hackathon.
          </p>
          <div className="mt-4 flex justify-center gap-6">
            <a href="#" className="text-purple-200 hover:text-white transition-colors hover:scale-110 inline-block">
              GitHub
            </a>
            <a href="#" className="text-purple-200 hover:text-white transition-colors hover:scale-110 inline-block">
              Documentation
            </a>
            <a href="#" className="text-purple-200 hover:text-white transition-colors hover:scale-110 inline-block">
              API
            </a>
          </div>
        </div>
      </footer>
    </main>
  )
}

const features = [
  {
    icon: '🤖',
    title: 'AI Content Generation',
    description: 'Generate high-quality content in multiple Indian languages using advanced AI models.',
  },
  {
    icon: '🌐',
    title: 'Smart Translation',
    description: 'Translate content across 11 Indian languages with IndicTrans, maintaining tone and cultural context.',
  },
  {
    icon: '📅',
    title: 'Social Scheduling',
    description: 'Schedule and publish content across Twitter, Facebook, Instagram, LinkedIn, and YouTube.',
  },
  {
    icon: '📊',
    title: 'Analytics Dashboard',
    description: 'Track engagement, views, and performance metrics across all platforms and languages.',
  },
  {
    icon: '🎤',
    title: 'Voice Input',
    description: 'Speak your ideas in any Indian language and let AI transcribe and generate content.',
  },
  {
    icon: '✨',
    title: 'Tone Customization',
    description: 'Choose from 8 different tones - professional, casual, friendly, formal, and more.',
  },
]
