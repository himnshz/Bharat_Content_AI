'use client'

import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { TrendingUp, Users } from 'lucide-react'

interface Creator {
  id: number
  name: string
  avatar: string
  followers: number
  engagement_rate: number
  platform: string
  status: string
}

interface CreatorCardProps {
  creator: Creator
  isDragging?: boolean
}

const platformColors: Record<string, string> = {
  Instagram: 'from-pink-500 to-purple-500',
  YouTube: 'from-red-500 to-red-600',
  TikTok: 'from-cyan-400 to-blue-500',
  Twitter: 'from-blue-400 to-blue-500',
}

const platformEmojis: Record<string, string> = {
  Instagram: '📸',
  YouTube: '📺',
  TikTok: '🎵',
  Twitter: '🐦',
}

export default function CreatorCard({ creator, isDragging = false }: CreatorCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({ id: creator.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isSortableDragging ? 0.5 : 1,
  }

  const platformColor = platformColors[creator.platform] || 'from-gray-400 to-gray-500'

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`glass-effect p-4 rounded-xl border border-white/20 cursor-grab active:cursor-grabbing hover:border-lavender/50 transition-all card-hover ${
        isDragging ? 'shadow-2xl border-lavender' : ''
      }`}
    >
      {/* Creator Header */}
      <div className="flex items-start gap-3 mb-3">
        <div className="text-4xl">{creator.avatar}</div>
        <div className="flex-1 min-w-0">
          <h4 className="text-white font-semibold truncate">{creator.name}</h4>
          <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-semibold bg-gradient-to-r ${platformColor} text-white mt-1`}>
            <span>{platformEmojis[creator.platform]}</span>
            <span>{creator.platform}</span>
          </div>
        </div>
      </div>

      {/* Creator Stats */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2 text-white/70">
            <Users className="w-4 h-4" />
            <span>Followers</span>
          </div>
          <span className="text-white font-semibold">
            {creator.followers >= 1000
              ? `${(creator.followers / 1000).toFixed(0)}K`
              : creator.followers}
          </span>
        </div>

        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2 text-white/70">
            <TrendingUp className="w-4 h-4" />
            <span>Engagement</span>
          </div>
          <span className="text-cyan font-semibold">{creator.engagement_rate}%</span>
        </div>
      </div>

      {/* Engagement Bar */}
      <div className="mt-3">
        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-cyan to-lavender rounded-full transition-all"
            style={{ width: `${Math.min(creator.engagement_rate * 20, 100)}%` }}
          />
        </div>
      </div>
    </div>
  )
}
