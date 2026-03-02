'use client'

import { useState } from 'react'
import Header from '@/components/layout/Header'
import Sidebar from '@/components/layout/Sidebar'
import HomeContent from '@/components/dashboard/HomeContent'
import GenerateContent from '@/components/dashboard/GenerateContent'
import TranslateContent from '@/components/dashboard/TranslateContent'
import ScheduleContent from '@/components/dashboard/ScheduleContent'
import CalendarContent from '@/components/dashboard/CalendarContent'
import AnalyticsContent from '@/components/dashboard/AnalyticsContent'
import VoiceContent from '@/components/dashboard/VoiceContent'
import ProfileContent from '@/components/dashboard/ProfileContent'
import CampaignsContent from '@/components/dashboard/CampaignsContent'
import ModelsContent from '@/components/dashboard/ModelsContent'
import TeamContent from '@/components/dashboard/TeamContent'
import TemplatesContent from '@/components/dashboard/TemplatesContent'
import ErrorBoundary from '@/components/ErrorBoundary'

export default function Dashboard() {
  const [currentScene, setCurrentScene] = useState('home')
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  const renderContent = () => {
    switch (currentScene) {
      case 'generate':
        return <GenerateContent />
      case 'translate':
        return <TranslateContent />
      case 'campaigns':
        return <CampaignsContent />
      case 'schedule':
        return <ScheduleContent />
      case 'calendar':
        return <CalendarContent />
      case 'team':
        return <TeamContent />
      case 'templates':
        return <TemplatesContent />
      case 'analytics':
        return <AnalyticsContent />
      case 'voice':
        return <VoiceContent />
      case 'models':
        return <ModelsContent />
      case 'profile':
        return <ProfileContent />
      default:
        return <HomeContent />
    }
  }

  return (
    <ErrorBoundary>
      <div className="flex h-screen overflow-hidden bg-gradient-to-br from-purple-900 via-lavender-900 to-periwinkle-900">
        {/* Sidebar */}
        <Sidebar 
          currentScene={currentScene} 
          onSceneChange={setCurrentScene}
          isMobileOpen={isMobileMenuOpen}
          onMobileClose={() => setIsMobileMenuOpen(false)}
        />
        
        {/* Main Content Area */}
        <div className="flex-1 flex flex-col lg:ml-64">
          {/* Header */}
          <Header 
            onMenuClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            isMobileMenuOpen={isMobileMenuOpen}
          />
          
          {/* Content */}
          <main className="flex-1 mt-16 relative overflow-auto">
            {/* Gradient Overlays */}
            <div className="absolute inset-0 bg-gradient-to-br from-periwinkle/10 via-transparent to-lavender/10 pointer-events-none" />
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
              <div className="absolute top-0 right-0 w-96 h-96 bg-cyan/20 rounded-full blur-3xl animate-floating" />
              <div className="absolute bottom-0 left-0 w-96 h-96 bg-lavender/20 rounded-full blur-3xl animate-floating" style={{ animationDelay: '1s' }} />
            </div>
            
            {/* Content Layer */}
            <div className="relative z-10 h-full">
              <ErrorBoundary>
                {renderContent()}
              </ErrorBoundary>
            </div>
          </main>
        </div>
      </div>
    </ErrorBoundary>
  )
}
