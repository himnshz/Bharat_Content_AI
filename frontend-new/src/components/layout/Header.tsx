'use client'

import { useState } from 'react'
import { Bell, Search, Settings, User, Menu, X, LogOut } from 'lucide-react'
import { useRouter } from 'next/navigation'

interface HeaderProps {
  onMenuClick: () => void
  isMobileMenuOpen: boolean
}

export default function Header({ onMenuClick, isMobileMenuOpen }: HeaderProps) {
  const router = useRouter()
  const [showNotifications, setShowNotifications] = useState(false)
  const [showProfile, setShowProfile] = useState(false)

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  const notifications = [
    { id: 1, text: 'Content generated successfully', time: '2 min ago', unread: true },
    { id: 2, text: 'Translation completed', time: '1 hour ago', unread: true },
    { id: 3, text: 'Post scheduled for tomorrow', time: '3 hours ago', unread: false },
  ]

  return (
    <header className="fixed top-0 right-0 left-0 lg:left-64 h-16 bg-white/80 backdrop-blur-xl border-b border-periwinkle/20 z-40 slide-in-top">
      <div className="h-full px-4 lg:px-6 flex items-center justify-between">
        {/* Left Section - Mobile Menu + Search */}
        <div className="flex items-center gap-4 flex-1">
          {/* Mobile Menu Button */}
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 hover:bg-periwinkle/10 rounded-lg transition-colors"
          >
            {isMobileMenuOpen ? (
              <X className="w-6 h-6 text-purple" />
            ) : (
              <Menu className="w-6 h-6 text-purple" />
            )}
          </button>

          {/* Search Bar */}
          <div className="hidden md:flex items-center flex-1 max-w-md">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-purple/40" />
              <input
                type="text"
                placeholder="Search content, translations..."
                className="w-full pl-10 pr-4 py-2 bg-periwinkle/10 border border-periwinkle/20 rounded-xl text-purple-900 placeholder-purple/40 focus:outline-none focus:border-lavender focus:ring-2 focus:ring-lavender/20 transition-all"
              />
            </div>
          </div>
        </div>

        {/* Right Section - Actions */}
        <div className="flex items-center gap-2">
          {/* Search Icon (Mobile) */}
          <button className="md:hidden p-2 hover:bg-periwinkle/10 rounded-lg transition-colors">
            <Search className="w-5 h-5 text-purple" />
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 hover:bg-periwinkle/10 rounded-lg transition-colors"
            >
              <Bell className="w-5 h-5 text-purple" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-cyan rounded-full animate-pulse" />
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-2xl border border-periwinkle/20 overflow-hidden fade-in">
                <div className="p-4 border-b border-periwinkle/20">
                  <h3 className="font-semibold text-purple-900">Notifications</h3>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  {notifications.map((notif) => (
                    <div
                      key={notif.id}
                      className={`p-4 border-b border-periwinkle/10 hover:bg-periwinkle/5 transition-colors cursor-pointer ${notif.unread ? 'bg-lavender/5' : ''
                        }`}
                    >
                      <div className="flex items-start gap-3">
                        {notif.unread && (
                          <div className="w-2 h-2 bg-cyan rounded-full mt-2" />
                        )}
                        <div className="flex-1">
                          <p className="text-sm text-purple-900">{notif.text}</p>
                          <p className="text-xs text-purple/60 mt-1">{notif.time}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="p-3 text-center border-t border-periwinkle/20">
                  <button className="text-sm text-lavender hover:text-purple font-medium">
                    View all notifications
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Settings */}
          <button className="hidden sm:block p-2 hover:bg-periwinkle/10 rounded-lg transition-colors">
            <Settings className="w-5 h-5 text-purple" />
          </button>

          {/* Profile */}
          <div className="relative">
            <button
              onClick={() => setShowProfile(!showProfile)}
              className="flex items-center gap-2 p-1 pr-3 hover:bg-periwinkle/10 rounded-xl transition-colors"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-lavender to-purple flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <span className="hidden sm:block text-sm font-medium text-purple-900">User</span>
            </button>

            {showProfile && (
              <div className="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-2xl border border-periwinkle/20 overflow-hidden fade-in">
                <div className="p-4 border-b border-periwinkle/20">
                  <p className="font-semibold text-purple-900">User Name</p>
                  <p className="text-xs text-purple/60">user@example.com</p>
                </div>
                <div className="p-2">
                  <button className="w-full text-left px-4 py-2 text-sm text-purple-900 hover:bg-periwinkle/10 rounded-lg transition-colors">
                    Profile Settings
                  </button>
                  <button className="w-full text-left px-4 py-2 text-sm text-purple-900 hover:bg-periwinkle/10 rounded-lg transition-colors">
                    API Keys
                  </button>
                  <button className="w-full text-left px-4 py-2 text-sm text-purple-900 hover:bg-periwinkle/10 rounded-lg transition-colors">
                    Billing
                  </button>
                </div>
                <div className="p-2 border-t border-periwinkle/20">
                  <button 
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors flex items-center gap-2"
                  >
                    <LogOut className="w-4 h-4" />
                    Sign Out
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
