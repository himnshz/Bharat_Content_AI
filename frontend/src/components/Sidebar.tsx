'use client'

import { useState } from 'react'
import { 
  Home, 
  Sparkles, 
  Languages, 
  Calendar, 
  BarChart3, 
  Mic, 
  User,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

interface SidebarProps {
  currentScene?: string
  onSceneChange?: (scene: string) => void
}

export default function Sidebar({ currentScene, onSceneChange }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false)

  const navItems = [
    { id: 'home', label: 'Home', icon: Home, scene: 'home' },
    { id: 'generate', label: 'Generate', icon: Sparkles, scene: 'generate' },
    { id: 'translate', label: 'Translate', icon: Languages, scene: 'translate' },
    { id: 'schedule', label: 'Schedule', icon: Calendar, scene: 'schedule' },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, scene: 'analytics' },
    { id: 'voice', label: 'Voice', icon: Mic, scene: 'voice' },
    { id: 'profile', label: 'Profile', icon: User, scene: 'profile' },
  ]

  const handleNavClick = (item: typeof navItems[0]) => {
    if (onSceneChange) {
      onSceneChange(item.scene)
    }
  }

  return (
    <div 
      className={`
        fixed left-0 top-0 h-screen
        bg-gradient-to-b from-purple/90 to-lavender-600/90
        backdrop-blur-xl border-r border-white/10
        transition-all duration-500 ease-in-out
        z-50 slide-in-left
        ${collapsed ? 'w-20' : 'w-64'}
      `}
    >
      {/* Logo */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <h1 className="text-2xl font-bold text-white tracking-in-expand">
              Bharat AI
            </h1>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-2 rounded-lg hover:bg-white/10 transition-all duration-300 text-white"
          >
            {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-2">
        {navItems.map((item, index) => {
          const Icon = item.icon
          const isActive = currentScene === item.scene
          
          return (
            <button
              key={item.id}
              onClick={() => handleNavClick(item)}
              className={`
                w-full flex items-center gap-4 px-4 py-3 rounded-xl
                transition-all duration-300
                ${isActive 
                  ? 'bg-white/20 text-white shadow-lg scale-105' 
                  : 'text-white/70 hover:bg-white/10 hover:text-white hover:scale-102'
                }
                ${collapsed ? 'justify-center' : ''}
              `}
              style={{ 
                animationDelay: `${index * 0.1}s`,
              }}
            >
              <Icon size={20} className={isActive ? 'pulsate-fwd' : ''} />
              {!collapsed && (
                <span className="font-medium">{item.label}</span>
              )}
            </button>
          )
        })}
      </nav>

      {/* Bottom Section */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-white/10">
        {!collapsed && (
          <div className="text-xs text-white/50 text-center">
            <p>Powered by AI</p>
            <p className="mt-1">v1.0.0</p>
          </div>
        )}
      </div>

      {/* Glow Effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-cyan-light/10 to-transparent pointer-events-none"></div>
    </div>
  )
}
