'use client';

import { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { Calendar, Clock, Filter, X } from 'lucide-react';
import { API_ENDPOINTS, fetchAPI } from '@/lib/api';

interface Post {
  id: number;
  content: string;
  platform: string;
  scheduled_time: string;
  status: string;
}

interface CalendarEvent {
  id: string;
  title: string;
  start: string;
  end?: string;
  backgroundColor: string;
  borderColor: string;
  extendedProps: {
    platform: string;
    content: string;
    status: string;
  };
}

const platformColors: Record<string, { bg: string; border: string }> = {
  facebook: { bg: '#1877F2', border: '#0C63D4' },
  instagram: { bg: '#E4405F', border: '#C13584' },
  twitter: { bg: '#1DA1F2', border: '#0C85D0' },
  linkedin: { bg: '#0A66C2', border: '#004182' },
  youtube: { bg: '#FF0000', border: '#CC0000' },
  whatsapp: { bg: '#25D366', border: '#128C7E' },
  telegram: { bg: '#0088CC', border: '#006699' },
};

export default function CalendarContent() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null);
  const [view, setView] = useState<'month' | 'week' | 'day'>('month');

  useEffect(() => {
    fetchScheduledPosts();
  }, []);

  useEffect(() => {
    convertPostsToEvents();
  }, [posts, selectedPlatforms]);

  const fetchScheduledPosts = async () => {
    try {
      setError('');
      const response = await fetchAPI(`${API_ENDPOINTS.listPosts}?status=scheduled`);
      
      if (response.ok) {
        const data = await response.json();
        setPosts(data.items || data);
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to fetch posts');
      }
    } catch (err) {
      console.error('Error fetching posts:', err);
      const message = err instanceof Error ? err.message : 'Failed to load scheduled posts';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const convertPostsToEvents = () => {
    const filtered = selectedPlatforms.length > 0
      ? posts.filter(post => selectedPlatforms.includes(post.platform))
      : posts;

    const calendarEvents: CalendarEvent[] = filtered.map(post => {
      const colors = platformColors[post.platform] || { bg: '#9EF0FF', border: '#8E70CF' };
      
      return {
        id: post.id.toString(),
        title: `${post.platform.charAt(0).toUpperCase() + post.platform.slice(1)}`,
        start: post.scheduled_time,
        backgroundColor: colors.bg,
        borderColor: colors.border,
        extendedProps: {
          platform: post.platform,
          content: post.content,
          status: post.status,
        },
      };
    });

    setEvents(calendarEvents);
  };

  const handleEventClick = (info: any) => {
    setSelectedEvent(info.event);
    setShowModal(true);
  };

  const handleEventDrop = async (info: any) => {
    const postId = info.event.id;
    const newTime = info.event.start.toISOString();

    try {
      setError('');
      // Fixed: Use correct reschedule endpoint
      const response = await fetchAPI(`${API_ENDPOINTS.schedulePost.replace('/schedule', '')}/reschedule/${postId}?scheduled_time=${encodeURIComponent(newTime)}`, {
        method: 'PUT',
      });

      if (response.ok) {
        fetchScheduledPosts();
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to reschedule');
        info.revert();
      }
    } catch (err) {
      console.error('Error rescheduling:', err);
      const message = err instanceof Error ? err.message : 'Failed to reschedule post';
      setError(message);
      info.revert();
    }
  };

  const togglePlatform = (platform: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(platform)
        ? prev.filter(p => p !== platform)
        : [...prev, platform]
    );
  };

  const platforms = ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'whatsapp', 'telegram'];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#B5C7EB]"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Error Display */}
      {error && (
        <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm">
          <div className="flex items-center gap-2">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        </div>
      )}
      
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-gradient-to-br from-[#B5C7EB] to-[#A4A5F5] rounded-xl">
            <Calendar className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Content Calendar</h2>
            <p className="text-gray-400">Visual scheduling and planning</p>
          </div>
        </div>

        {/* View Selector */}
        <div className="flex gap-2">
          <button
            onClick={() => setView('month')}
            className={`px-4 py-2 rounded-lg transition-all ${
              view === 'month'
                ? 'bg-[#B5C7EB] text-white'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            Month
          </button>
          <button
            onClick={() => setView('week')}
            className={`px-4 py-2 rounded-lg transition-all ${
              view === 'week'
                ? 'bg-[#B5C7EB] text-white'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            Week
          </button>
          <button
            onClick={() => setView('day')}
            className={`px-4 py-2 rounded-lg transition-all ${
              view === 'day'
                ? 'bg-[#B5C7EB] text-white'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            Day
          </button>
        </div>
      </div>

      {/* Platform Filters */}
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
        <div className="flex items-center gap-3 mb-3">
          <Filter className="w-5 h-5 text-[#B5C7EB]" />
          <span className="text-white font-medium">Filter by Platform</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {platforms.map(platform => (
            <button
              key={platform}
              onClick={() => togglePlatform(platform)}
              className={`px-4 py-2 rounded-lg transition-all ${
                selectedPlatforms.includes(platform)
                  ? 'text-white'
                  : 'bg-white/5 text-gray-400 hover:bg-white/10'
              }`}
              style={{
                backgroundColor: selectedPlatforms.includes(platform)
                  ? platformColors[platform]?.bg
                  : undefined,
              }}
            >
              {platform.charAt(0).toUpperCase() + platform.slice(1)}
            </button>
          ))}
          {selectedPlatforms.length > 0 && (
            <button
              onClick={() => setSelectedPlatforms([])}
              className="px-4 py-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-all"
            >
              Clear All
            </button>
          )}
        </div>
      </div>

      {/* Calendar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
        <FullCalendar
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          initialView={view === 'month' ? 'dayGridMonth' : view === 'week' ? 'timeGridWeek' : 'timeGridDay'}
          headerToolbar={{
            left: 'prev,next today',
            center: 'title',
            right: '',
          }}
          events={events}
          editable={true}
          droppable={true}
          eventClick={handleEventClick}
          eventDrop={handleEventDrop}
          height="auto"
          eventTimeFormat={{
            hour: '2-digit',
            minute: '2-digit',
            meridiem: 'short',
          }}
          slotLabelFormat={{
            hour: '2-digit',
            minute: '2-digit',
            meridiem: 'short',
          }}
        />
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-[#B5C7EB]/20 to-[#9EF0FF]/20 rounded-xl p-4 border border-[#B5C7EB]/30">
          <div className="text-gray-400 text-sm mb-1">Total Scheduled</div>
          <div className="text-3xl font-bold text-white">{posts.length}</div>
        </div>
        <div className="bg-gradient-to-br from-[#A4A5F5]/20 to-[#8E70CF]/20 rounded-xl p-4 border border-[#A4A5F5]/30">
          <div className="text-gray-400 text-sm mb-1">This Week</div>
          <div className="text-3xl font-bold text-white">
            {posts.filter(p => {
              const postDate = new Date(p.scheduled_time);
              const now = new Date();
              const weekFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
              return postDate >= now && postDate <= weekFromNow;
            }).length}
          </div>
        </div>
        <div className="bg-gradient-to-br from-[#9EF0FF]/20 to-[#B5C7EB]/20 rounded-xl p-4 border border-[#9EF0FF]/30">
          <div className="text-gray-400 text-sm mb-1">Platforms</div>
          <div className="text-3xl font-bold text-white">
            {new Set(posts.map(p => p.platform)).size}
          </div>
        </div>
        <div className="bg-gradient-to-br from-[#8E70CF]/20 to-[#A4A5F5]/20 rounded-xl p-4 border border-[#8E70CF]/30">
          <div className="text-gray-400 text-sm mb-1">Pending</div>
          <div className="text-3xl font-bold text-white">
            {posts.filter(p => p.status === 'scheduled').length}
          </div>
        </div>
      </div>

      {/* Event Details Modal */}
      {showModal && selectedEvent && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-[#1a1a2e] rounded-xl p-6 max-w-md w-full mx-4 border border-white/10">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-white">Post Details</h3>
              <button
                onClick={() => setShowModal(false)}
                className="p-2 hover:bg-white/10 rounded-lg transition-all"
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <div className="text-gray-400 text-sm mb-1">Platform</div>
                <div
                  className="px-4 py-2 rounded-lg text-white font-medium inline-block"
                  style={{
                    backgroundColor: platformColors[selectedEvent.extendedProps.platform]?.bg,
                  }}
                >
                  {selectedEvent.extendedProps.platform.charAt(0).toUpperCase() +
                    selectedEvent.extendedProps.platform.slice(1)}
                </div>
              </div>

              <div>
                <div className="text-gray-400 text-sm mb-1">Scheduled Time</div>
                <div className="flex items-center gap-2 text-white">
                  <Clock className="w-4 h-4 text-[#B5C7EB]" />
                  {new Date(selectedEvent.start).toLocaleString()}
                </div>
              </div>

              <div>
                <div className="text-gray-400 text-sm mb-1">Content</div>
                <div className="bg-white/5 rounded-lg p-3 text-white">
                  {selectedEvent.extendedProps.content}
                </div>
              </div>

              <div>
                <div className="text-gray-400 text-sm mb-1">Status</div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    selectedEvent.extendedProps.status === 'scheduled'
                      ? 'bg-blue-500/20 text-blue-400'
                      : selectedEvent.extendedProps.status === 'published'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-gray-500/20 text-gray-400'
                  }`}
                >
                  {selectedEvent.extendedProps.status}
                </span>
              </div>
            </div>

            <div className="mt-6 flex gap-3">
              <button
                onClick={() => setShowModal(false)}
                className="flex-1 px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
              >
                Close
              </button>
              <button className="flex-1 px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all">
                Edit Post
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
