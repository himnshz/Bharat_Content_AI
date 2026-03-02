'use client'

export default function HomeContent() {
  const quickActions = [
    { icon: '✨', title: 'Generate Content', desc: 'Create AI-powered content', color: 'from-lavender to-purple' },
    { icon: '🌐', title: 'Translate', desc: 'Translate to 11 languages', color: 'from-cyan to-periwinkle' },
    { icon: '📅', title: 'Schedule Post', desc: 'Plan your content calendar', color: 'from-periwinkle to-lavender' },
    { icon: '🎤', title: 'Voice Input', desc: 'Speak your ideas', color: 'from-purple to-cyan' },
  ]

  const recentProjects = [
    { title: 'Blog Post: AI in Education', lang: 'Hindi', date: '2 hours ago', status: 'completed' },
    { title: 'Social Media Campaign', lang: 'Tamil', date: '5 hours ago', status: 'in-progress' },
    { title: 'Product Description', lang: 'Bengali', date: '1 day ago', status: 'completed' },
  ]

  return (
    <div className="h-full p-8 space-y-6 overflow-auto">
      {/* Welcome Section */}
      <div className="glass-effect p-8 rounded-2xl border border-periwinkle/30 slide-in-top">
        <h2 className="text-4xl font-bold text-white gradient-text mb-2 tracking-in-expand">
          Welcome to Bharat Content AI 🚀
        </h2>
        <p className="text-white/70 text-lg">
          Your AI-powered multilingual content creation platform
        </p>
      </div>

      {/* Quick Actions */}
      <div>
        <h3 className="text-xl font-bold text-white mb-4 fade-in">⚡ Quick Actions</h3>
        <div className="grid grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <button
              key={action.title}
              className={`glass-effect p-6 rounded-2xl border border-white/20 hover:border-lavender/50 transition-all hover:scale-105 text-left flip-in-hor-bottom`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${action.color} flex items-center justify-center text-2xl mb-3`}>
                {action.icon}
              </div>
              <h4 className="text-white font-semibold mb-1">{action.title}</h4>
              <p className="text-white/60 text-sm">{action.desc}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-3 gap-6">
        {[
          { label: 'Content Generated', value: '1,234', icon: '📝', color: 'text-cyan' },
          { label: 'Languages Used', value: '11', icon: '🌐', color: 'text-lavender' },
          { label: 'Total Reach', value: '128K', icon: '👥', color: 'text-periwinkle' },
        ].map((stat, index) => (
          <div
            key={stat.label}
            className="glass-effect p-6 rounded-2xl border border-lavender/30 bounce-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">{stat.icon}</span>
              <span className={`text-3xl font-bold ${stat.color}`}>{stat.value}</span>
            </div>
            <p className="text-white/70">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Recent Projects */}
      <div className="glass-effect p-6 rounded-2xl border border-periwinkle/30 slide-in-blurred-left">
        <h3 className="text-xl font-bold text-white mb-4 gradient-text">📂 Recent Projects</h3>
        <div className="space-y-3">
          {recentProjects.map((project, index) => (
            <div
              key={index}
              className="bg-white/5 backdrop-blur-sm p-4 rounded-xl border border-white/10 hover:border-lavender/50 transition-all cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h4 className="text-white font-semibold mb-1">{project.title}</h4>
                  <div className="flex items-center gap-3 text-sm text-white/60">
                    <span>🌐 {project.lang}</span>
                    <span>•</span>
                    <span>🕐 {project.date}</span>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs ${
                  project.status === 'completed' 
                    ? 'bg-cyan/20 text-cyan' 
                    : 'bg-lavender/20 text-lavender'
                }`}>
                  {project.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
