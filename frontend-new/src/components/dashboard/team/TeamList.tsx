'use client';

import { Users, Calendar, Trash2, Edit } from 'lucide-react';

interface Team {
  id: number;
  name: string;
  description: string;
  owner_id: number;
  member_count: number;
  created_at: string;
}

interface TeamListProps {
  teams: Team[];
  selectedTeam: Team | null;
  onSelectTeam: (team: Team) => void;
  onRefresh: () => void;
  getRoleIcon: (role: string) => JSX.Element;
  getRoleBadgeColor: (role: string) => string;
}

export default function TeamList({
  teams,
  selectedTeam,
  onSelectTeam,
  onRefresh,
}: TeamListProps) {
  if (teams.length === 0) {
    return (
      <div className="text-center py-12">
        <Users className="w-16 h-16 text-gray-600 mx-auto mb-4" />
        <p className="text-gray-400 mb-4">No teams yet</p>
        <p className="text-gray-500 text-sm">Create your first team to get started</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {teams.map((team, index) => (
        <div
          key={team.id}
          onClick={() => onSelectTeam(team)}
          className={`bg-white/5 backdrop-blur-sm rounded-xl p-6 border transition-all cursor-pointer hover:scale-105 slide-in-top ${
            selectedTeam?.id === team.id
              ? 'border-[#B5C7EB] bg-[#B5C7EB]/10'
              : 'border-white/10 hover:border-white/20'
          }`}
          style={{ animationDelay: `${index * 0.1}s` }}
        >
          {/* Team Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gradient-to-br from-[#B5C7EB]/20 to-[#A4A5F5]/20 rounded-lg">
                <Users className="w-6 h-6 text-[#B5C7EB]" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">{team.name}</h3>
                <p className="text-gray-400 text-sm">{team.member_count} members</p>
              </div>
            </div>
          </div>

          {/* Description */}
          {team.description && (
            <p className="text-gray-400 text-sm mb-4 line-clamp-2">
              {team.description}
            </p>
          )}

          {/* Footer */}
          <div className="flex items-center justify-between pt-4 border-t border-white/10">
            <div className="flex items-center gap-2 text-gray-500 text-xs">
              <Calendar className="w-3 h-3" />
              {new Date(team.created_at).toLocaleDateString()}
            </div>

            <div className="flex gap-2">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  alert('✨ Team editing feature coming soon!\n\nYou will be able to:\n• Edit team name\n• Update description\n• Change team settings');
                }}
                className="p-2 hover:bg-white/10 rounded-lg transition-all"
                title="Edit team (Coming Soon)"
              >
                <Edit className="w-4 h-4 text-gray-400 hover:text-[#B5C7EB]" />
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  if (confirm('⚠️ Delete team feature coming soon!\n\nThis will allow team owners to:\n• Delete the entire team\n• Remove all members\n• Archive team data\n\nNote: This action will be irreversible.')) {
                    alert('Team deletion will be available in the next update!');
                  }
                }}
                className="p-2 hover:bg-red-500/10 rounded-lg transition-all"
                title="Delete team (Coming Soon)"
              >
                <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-400" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
