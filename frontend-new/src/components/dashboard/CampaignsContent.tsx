'use client'

import { useState, useEffect, useMemo, useCallback } from 'react'
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
} from '@dnd-kit/core'
import { Plus, TrendingUp, Users, DollarSign, Calendar } from 'lucide-react'
import KanbanColumn from './kanban/KanbanColumn'
import CreatorCard from './kanban/CreatorCard'
import { API_ENDPOINTS, fetchAPI, handleAPIError, getAuthUser } from '@/lib/api'

interface Creator {
  id: number
  name: string
  avatar: string
  followers: number
  engagement_rate: number
  platform: string
  status: string
  campaign_id?: number
}

interface Campaign {
  id: number
  name: string
  status: string
  budget: number
  actual_reach: number
  roi: number
  start_date: string
  end_date: string
}

const PIPELINE_STAGES = [
  { id: 'outreach', title: 'Outreach', color: 'from-periwinkle to-cyan' },
  { id: 'negotiating', title: 'Negotiating', color: 'from-cyan to-lavender' },
  { id: 'contracted', title: 'Contracted', color: 'from-lavender to-purple' },
  { id: 'content_creation', title: 'Content Creation', color: 'from-purple to-periwinkle' },
  { id: 'completed', title: 'Completed', color: 'from-cyan to-periwinkle' },
]

export default function CampaignsContent() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [selectedCampaign, setSelectedCampaign] = useState<number | null>(null)
  const [creators, setCreators] = useState<Creator[]>([])
  const [activeCreator, setActiveCreator] = useState<Creator | null>(null)
  const [loading, setLoading] = useState(true)
  const [showNewCampaign, setShowNewCampaign] = useState(false)

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  )

  // Fetch campaigns from API
  const fetchCampaigns = useCallback(async () => {
    try {
      const response = await fetchAPI(API_ENDPOINTS.campaigns)
      if (response.ok) {
        const data = await response.json()
        setCampaigns(data)
        if (data.length > 0 && !selectedCampaign) {
          setSelectedCampaign(data[0].id)
        }
      } else {
        await handleAPIError(response)
      }
    } catch (error) {
      console.error('Failed to fetch campaigns:', error)
    } finally {
      setLoading(false)
    }
  }, [selectedCampaign])

  useEffect(() => {
    fetchCampaigns()
  }, [fetchCampaigns])

  // Mock creators data - in production, this would come from an API
  useEffect(() => {
    const mockCreators: Creator[] = [
      { id: 1, name: 'Sarah Johnson', avatar: '👩‍💼', followers: 125000, engagement_rate: 4.2, platform: 'Instagram', status: 'outreach' },
      { id: 2, name: 'Mike Chen', avatar: '👨‍💻', followers: 89000, engagement_rate: 3.8, platform: 'YouTube', status: 'outreach' },
      { id: 3, name: 'Emma Davis', avatar: '👩‍🎨', followers: 210000, engagement_rate: 5.1, platform: 'TikTok', status: 'negotiating' },
      { id: 4, name: 'Alex Kumar', avatar: '👨‍🎤', followers: 156000, engagement_rate: 4.5, platform: 'Instagram', status: 'negotiating' },
      { id: 5, name: 'Lisa Wang', avatar: '👩‍🔬', followers: 98000, engagement_rate: 3.9, platform: 'Twitter', status: 'contracted' },
      { id: 6, name: 'James Brown', avatar: '👨‍🚀', followers: 175000, engagement_rate: 4.8, platform: 'YouTube', status: 'content_creation' },
      { id: 7, name: 'Nina Patel', avatar: '👩‍🎓', followers: 142000, engagement_rate: 4.3, platform: 'Instagram', status: 'content_creation' },
      { id: 8, name: 'Tom Wilson', avatar: '👨‍🏫', followers: 203000, engagement_rate: 5.2, platform: 'TikTok', status: 'completed' },
    ]
    setCreators(mockCreators)
  }, [])

  // ✅ OPTIMIZED: Memoize drag handlers
  const handleDragStart = useCallback((event: DragStartEvent) => {
    const { active } = event
    const creator = creators.find(c => c.id === active.id)
    setActiveCreator(creator || null)
  }, [creators])

  const handleDragEnd = useCallback((event: DragEndEvent) => {
    const { active, over } = event
    
    if (!over) {
      setActiveCreator(null)
      return
    }

    const creatorId = active.id as number
    const newStatus = over.id as string

    // Update creator status
    setCreators(prev =>
      prev.map(creator =>
        creator.id === creatorId
          ? { ...creator, status: newStatus }
          : creator
      )
    )

    setActiveCreator(null)
  }, [])

  // ✅ OPTIMIZED: Memoize filtered creators
  const getCreatorsByStatus = useCallback((status: string) => {
    return creators.filter(c => c.status === status)
  }, [creators])

  // ✅ OPTIMIZED: Memoize current campaign
  const currentCampaign = useMemo(() => 
    campaigns.find(c => c.id === selectedCampaign),
    [campaigns, selectedCampaign]
  )

  return (
    <div className="h-full flex flex-col p-6 overflow-hidden">
      {/* Header */}
      <div className="mb-6 slide-in-top">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold text-white gradient-text">Campaign Pipeline</h2>
            <p className="text-white/60 mt-1">Manage your creator collaborations</p>
          </div>
          <button
            onClick={() => setShowNewCampaign(true)}
            className="btn-primary flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            New Campaign
          </button>
        </div>

        {/* Campaign Selector */}
        <div className="glass-effect p-4 rounded-xl border border-periwinkle/30">
          <div className="flex items-center gap-4 overflow-x-auto">
            {loading ? (
              <div className="text-white/60">Loading campaigns...</div>
            ) : campaigns.length === 0 ? (
              <div className="text-white/60">No campaigns yet. Create your first campaign!</div>
            ) : (
              campaigns.map(campaign => (
                <button
                  key={campaign.id}
                  onClick={() => setSelectedCampaign(campaign.id)}
                  className={`px-6 py-3 rounded-lg transition-all whitespace-nowrap ${
                    selectedCampaign === campaign.id
                      ? 'bg-gradient-to-r from-lavender to-purple text-white scale-105'
                      : 'bg-white/10 text-white/70 hover:bg-white/20'
                  }`}
                >
                  <div className="font-semibold">{campaign.name}</div>
                  <div className="text-xs mt-1 opacity-80">{campaign.status}</div>
                </button>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Campaign Stats */}
      {currentCampaign && (
        <div className="grid grid-cols-4 gap-4 mb-6 fade-in">
          <div className="glass-effect p-4 rounded-xl border border-periwinkle/30">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-cyan/20 flex items-center justify-center">
                <DollarSign className="w-5 h-5 text-cyan" />
              </div>
              <div>
                <div className="text-white/60 text-sm">Budget</div>
                <div className="text-white font-bold">${currentCampaign.budget?.toLocaleString() || 0}</div>
              </div>
            </div>
          </div>

          <div className="glass-effect p-4 rounded-xl border border-lavender/30">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-lavender/20 flex items-center justify-center">
                <Users className="w-5 h-5 text-lavender" />
              </div>
              <div>
                <div className="text-white/60 text-sm">Reach</div>
                <div className="text-white font-bold">{(currentCampaign.actual_reach || 0).toLocaleString()}</div>
              </div>
            </div>
          </div>

          <div className="glass-effect p-4 rounded-xl border border-purple/30">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-purple/20 flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-purple" />
              </div>
              <div>
                <div className="text-white/60 text-sm">ROI</div>
                <div className="text-white font-bold">{currentCampaign.roi?.toFixed(1) || 0}%</div>
              </div>
            </div>
          </div>

          <div className="glass-effect p-4 rounded-xl border border-periwinkle/30">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-periwinkle/20 flex items-center justify-center">
                <Calendar className="w-5 h-5 text-periwinkle" />
              </div>
              <div>
                <div className="text-white/60 text-sm">Creators</div>
                <div className="text-white font-bold">{creators.length}</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Kanban Board */}
      <div className="flex-1 overflow-hidden">
        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          <div className="flex gap-4 h-full overflow-x-auto pb-4">
            {PIPELINE_STAGES.map(stage => (
              <KanbanColumn
                key={stage.id}
                id={stage.id}
                title={stage.title}
                color={stage.color}
                creators={getCreatorsByStatus(stage.id)}
              />
            ))}
          </div>

          <DragOverlay>
            {activeCreator ? (
              <div className="rotate-3 scale-105">
                <CreatorCard creator={activeCreator} isDragging />
              </div>
            ) : null}
          </DragOverlay>
        </DndContext>
      </div>

      {/* New Campaign Modal */}
      {showNewCampaign && (
        <div className="fixed inset-0 bg-purple-900/50 backdrop-blur-sm z-50 flex items-center justify-center fade-in">
          <div className="glass-effect p-8 rounded-2xl border border-periwinkle/30 max-w-2xl w-full mx-4 scale-in-center">
            <h3 className="text-2xl font-bold text-white mb-6 gradient-text">Create New Campaign</h3>
            <form className="space-y-4">
              <input
                type="text"
                name="name"
                placeholder="Campaign Name"
                required
                className="w-full px-4 py-3 bg-white/10 border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none"
              />
              <textarea
                name="description"
                placeholder="Campaign Description"
                className="w-full px-4 py-3 bg-white/10 border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none resize-none h-24"
              />
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="number"
                  name="budget"
                  placeholder="Budget"
                  className="px-4 py-3 bg-white/10 border-2 border-periwinkle/30 rounded-xl text-white placeholder-white/40 focus:border-lavender focus:outline-none"
                />
                <select name="campaign_type" className="px-4 py-3 bg-white/10 border-2 border-periwinkle/30 rounded-xl text-white focus:border-lavender focus:outline-none">
                  <option value="awareness" className="bg-purple-900">Awareness</option>
                  <option value="engagement" className="bg-purple-900">Engagement</option>
                  <option value="conversion" className="bg-purple-900">Conversion</option>
                </select>
              </div>
              <div className="flex gap-3 mt-6">
                <button
                  onClick={() => setShowNewCampaign(false)}
                  className="flex-1 px-6 py-3 bg-white/10 hover:bg-white/20 rounded-xl text-white transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={async () => {
                    try {
                      const user = getAuthUser();
                      if (!user) {
                        alert('❌ Please log in to create a campaign');
                        return;
                      }
                      
                      const formData = new FormData(document.querySelector('form') as HTMLFormElement);
                      
                      const response = await fetchAPI(API_ENDPOINTS.campaigns, {
                        method: 'POST',
                        body: JSON.stringify({
                          name: formData.get('name'),
                          description: formData.get('description'),
                          campaign_type: 'influencer',
                          status: 'draft',
                          budget: 0,
                          start_date: new Date().toISOString(),
                          end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
                        }),
                      });

                      if (response.ok) {
                        fetchCampaigns();
                        setShowNewCampaign(false);
                        alert('✅ Campaign created successfully!');
                      } else {
                        await handleAPIError(response);
                      }
                    } catch (error) {
                      console.error('Error creating campaign:', error);
                      alert('❌ Error creating campaign: ' + (error instanceof Error ? error.message : 'Unknown error'));
                    }
                  }}
                  className="flex-1 btn-primary"
                >
                  Create Campaign
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
