'use client'

import { useDroppable } from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'
import CreatorCard from './CreatorCard'

interface Creator {
  id: number
  name: string
  avatar: string
  followers: number
  engagement_rate: number
  platform: string
  status: string
}

interface KanbanColumnProps {
  id: string
  title: string
  color: string
  creators: Creator[]
}

export default function KanbanColumn({ id, title, color, creators }: KanbanColumnProps) {
  const { setNodeRef, isOver } = useDroppable({
    id: id,
  })

  return (
    <div className="flex-shrink-0 w-80 flex flex-col">
      {/* Column Header */}
      <div className={`glass-effect p-4 rounded-t-xl border border-b-0 border-white/20 bg-gradient-to-r ${color} bg-opacity-20`}>
        <div className="flex items-center justify-between">
          <h3 className="text-white font-bold text-lg">{title}</h3>
          <span className="px-3 py-1 bg-white/20 rounded-full text-white text-sm font-semibold">
            {creators.length}
          </span>
        </div>
      </div>

      {/* Column Content */}
      <div
        ref={setNodeRef}
        className={`flex-1 glass-effect p-4 rounded-b-xl border border-t-0 border-white/20 overflow-y-auto transition-all ${
          isOver ? 'bg-lavender/20 border-lavender' : ''
        }`}
        style={{ minHeight: '500px' }}
      >
        <SortableContext
          items={creators.map(c => c.id)}
          strategy={verticalListSortingStrategy}
        >
          <div className="space-y-3">
            {creators.length === 0 ? (
              <div className="text-center py-12 text-white/40">
                <div className="text-4xl mb-2">📋</div>
                <p className="text-sm">Drop creators here</p>
              </div>
            ) : (
              creators.map((creator, index) => (
                <div
                  key={creator.id}
                  className="flip-in-hor-bottom"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <CreatorCard creator={creator} />
                </div>
              ))
            )}
          </div>
        </SortableContext>
      </div>
    </div>
  )
}
