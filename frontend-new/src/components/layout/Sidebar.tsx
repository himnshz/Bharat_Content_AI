'use client'

import { useState } from 'react'
import { Home, Sparkles, Languages, Calendar, BarChart3, Mic, User, ChevronLeft, ChevronRight, X, Settings, Target, Users, FileText } from 'lucide-react'

interface SidebarProps {
  currentScene: string
  onSceneChange: (scene: string) => void
  isMobileOpen: boolean
  onMobileClose: () => void
}

export default function Sidebar({ currentScene, onSceneChange, isMobileOpen, onMobileClose }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false)

  const navItems = [
    { id: 'home', label: 'Home', icon: Home, description: 'Dashboard overview' },
    { id: 'generate', label: 'Generate', icon: Sparkles, description: 'AI content creation' },
    { id: 'translate', label: 'Translate', icon: Languages, description: '11 Indian languages' },
    { id: 'schedule', label: 'Schedule', icon: Calendar, description: 'Plan your posts' },
    { id: 'calendar', label: 'Calendar', icon: Calendar, description: 'Visual scheduling' },
    { id: 'campaigns', label: 'Campaigns', icon: Target, description: 'Manage campaigns' },
    { id: 'team', label: 'Team', icon: Users, description: 'Collaboration' },
    { id: 'templates', label: 'Templates', icon: FileText, description: 'Content templates' },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, description: 'Track performance' },
    { id: 'voice', label: 'Voice', icon: Mic, description: 'Speech to text' },
    { id: 'models', label: 'AI Models', icon: Settings, description: 'Configure AI' },
    { id: 'profile', label: 'Profile', icon: User, description: 'Account settings' },
  ]

  const handleNavClick = (id: string) => {
    onSceneChange(id)
    if (isMobileOpen) {
      onMobileClose()
    }
  }

  return (
    <>
      {/* Mobile Overlay */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-purple-900/50 backdrop-blur-sm z-40 lg:hidden fade-in"
          onClick={onMobileClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-screen bg-gradient-to-b from-lavender/95 to-purple/95 backdrop-blur-xl border-r border-white/10 transition-all duration-300 z-50 ${collapsed ? 'w-20' : 'w-64'
          } ${isMobileOpen ? 'translate-x-0' : '-translate-x-full'
          } lg:translate-x-0`}
      >
        {/* Header */}
        <div className="h-16 px-6 flex items-center justify-between border-b border-white/10">
          {!collapsed && (
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan to-periwinkle flex items-center justify-center">
                <span className="text-white font-bold text-lg">B</span>
              </div>
              <h1 className="text-xl font-bold text-white shimmer">Bharat AI</h1>
            </div>
          )}

          {/* Desktop Collapse Button */}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="hidden lg:block p-2 rounded-lg hover:bg-white/10 transition-all text-white hover:scale-110"
          >
            {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
          </button>

          {/* Mobile Close Button */}
          <button
            onClick={onMobileClose}
            className="lg:hidden p-2 rounded-lg hover:bg-white/10 transition-all text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2 overflow-y-auto h-[calc(100vh-8rem)]">
          {navItems.map((item, index) => {
            const Icon = item.icon
            const isActive = currentScene === item.id

            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group flip-in-hor-bottom ${isActive
                    ? 'bg-white/20 text-white shadow-lg scale-105 border border-cyan/30'
                    : 'text-white/70 hover:bg-white/10 hover:text-white hover:scale-105'
                  } ${collapsed ? 'justify-center' : ''}`}
                style={{ animationDelay: `${index * 0.05}s` }}
                title={collapsed ? item.label : ''}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-cyan' : ''} transition-colors`} />
                {!collapsed && (
                  <div className="flex-1 text-left">
                    <div className="font-medium">{item.label}</div>
                    <div className="text-xs text-white/50 group-hover:text-white/70 transition-colors">
                      {item.description}
                    </div>
                  </div>
                )}
              </button>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-white/10 bg-purple/20">
          {!collapsed ? (
            <div className="space-y-2 fade-in">
              <div className="flex items-center gap-2 text-xs text-white/50">
                <div className="w-2 h-2 bg-cyan rounded-full animate-pulse" />
                <span>All systems operational</span>
              </div>
              <div className="text-xs text-white/50">
                <span className="gradient-text font-semibold">v1.0.0</span> • Powered by AI
              </div>
            </div>
          ) : (
            <div className="flex justify-center">
              <div className="w-2 h-2 bg-cyan rounded-full animate-pulse" />
            </div>
          )}
        </div>
      </aside>
    </>
  )
}
