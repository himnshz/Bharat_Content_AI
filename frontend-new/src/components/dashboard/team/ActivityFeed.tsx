'use client';

import { useState, useEffect } from 'react';
import { Activity, User, FileText, MessageSquare, CheckCircle, UserPlus, Trash2, Edit } from 'lucide-react';

interface ActivityItem {
  id: number;
  user_id: number;
  username: string;
  action: string;
  resource_type: string;
  resource_id: number;
  details: string | null;
  created_at: string;
}

interface ActivityFeedProps {
  teamId: number;
}

export default function ActivityFeed({ teamId }: ActivityFeedProps) {
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchActivities();
  }, [teamId]);

  const fetchActivities = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/teams/${teamId}/activity?limit=50`);
      
      if (response.ok) {
        const data = await response.json();
        setActivities(data);
      }
    } catch (error) {
      console.error('Error fetching activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'created':
        return <FileText className="w-4 h-4 text-green-400" />;
      case 'updated':
        return <Edit className="w-4 h-4 text-blue-400" />;
      case 'deleted':
        return <Trash2 className="w-4 h-4 text-red-400" />;
      case 'commented':
        return <MessageSquare className="w-4 h-4 text-purple-400" />;
      case 'approved':
      case 'requested_approval':
        return <CheckCircle className="w-4 h-4 text-yellow-400" />;
      case 'invited':
      case 'joined':
        return <UserPlus className="w-4 h-4 text-cyan-400" />;
      default:
        return <Activity className="w-4 h-4 text-gray-400" />;
    }
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'created':
        return 'bg-green-500/10 border-green-500/20';
      case 'updated':
        return 'bg-blue-500/10 border-blue-500/20';
      case 'deleted':
        return 'bg-red-500/10 border-red-500/20';
      case 'commented':
        return 'bg-purple-500/10 border-purple-500/20';
      case 'approved':
      case 'requested_approval':
        return 'bg-yellow-500/10 border-yellow-500/20';
      case 'invited':
      case 'joined':
        return 'bg-cyan-500/10 border-cyan-500/20';
      default:
        return 'bg-gray-500/10 border-gray-500/20';
    }
  };

  const getActionText = (activity: ActivityItem) => {
    const action = activity.action;
    const resource = activity.resource_type;
    
    switch (action) {
      case 'created':
        return `created a ${resource}`;
      case 'updated':
        return `updated a ${resource}`;
      case 'deleted':
        return `deleted a ${resource}`;
      case 'commented':
        return `commented on a ${resource}`;
      case 'approved':
        return `approved a ${resource}`;
      case 'requested_approval':
        return `requested approval for a ${resource}`;
      case 'invited':
        return `invited a new member`;
      case 'joined':
        return `joined the team`;
      case 'removed':
        return `removed a ${resource}`;
      default:
        return `performed an action on ${resource}`;
    }
  };

  const getTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
    return date.toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#B5C7EB]"></div>
      </div>
    );
  }

  if (activities.length === 0) {
    return (
      <div className="text-center py-12">
        <Activity className="w-16 h-16 text-gray-600 mx-auto mb-4" />
        <p className="text-gray-400">No activity yet</p>
        <p className="text-gray-500 text-sm mt-2">Team activity will appear here</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white">Recent Activity</h3>
          <p className="text-gray-400 text-sm">{activities.length} activities</p>
        </div>
        <button
          onClick={fetchActivities}
          className="px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
        >
          Refresh
        </button>
      </div>

      {/* Activity Timeline */}
      <div className="space-y-3">
        {activities.map((activity, index) => (
          <div
            key={activity.id}
            className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10 hover:border-white/20 transition-all slide-in-top"
            style={{ animationDelay: `${index * 0.03}s` }}
          >
            <div className="flex items-start gap-4">
              {/* Icon */}
              <div className={`p-2 rounded-lg border ${getActionColor(activity.action)}`}>
                {getActionIcon(activity.action)}
              </div>

              {/* Content */}
              <div className="flex-1">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-white">
                      <span className="font-medium text-[#B5C7EB]">{activity.username}</span>
                      {' '}
                      <span className="text-gray-400">{getActionText(activity)}</span>
                    </p>
                    {activity.details && (
                      <p className="text-gray-500 text-sm mt-1 line-clamp-2">
                        {activity.details}
                      </p>
                    )}
                  </div>
                  <span className="text-gray-500 text-xs whitespace-nowrap">
                    {getTimeAgo(activity.created_at)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Load More */}
      {activities.length >= 50 && (
        <div className="text-center">
          <button className="px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all">
            Load More
          </button>
        </div>
      )}
    </div>
  );
}
