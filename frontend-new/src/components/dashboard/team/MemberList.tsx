'use client';

import { UserPlus, Mail, MoreVertical, Trash2, Shield } from 'lucide-react';
import { useState } from 'react';
import { API_ENDPOINTS, fetchAPI } from '@/lib/api';

interface Member {
  id: number;
  user_id: number;
  username: string;
  email: string;
  role: string;
  joined_at: string;
}

interface MemberListProps {
  teamId: number;
  members: Member[];
  onInvite: () => void;
  onRefresh: () => void;
  getRoleIcon: (role: string) => JSX.Element;
  getRoleBadgeColor: (role: string) => string;
}

export default function MemberList({
  teamId,
  members,
  onInvite,
  onRefresh,
  getRoleIcon,
  getRoleBadgeColor,
}: MemberListProps) {
  const [showMenu, setShowMenu] = useState<number | null>(null);

  const handleRemoveMember = async (memberId: number) => {
    try {
      const response = await fetchAPI(
        `${API_ENDPOINTS.teams}/${teamId}/members/${memberId}`,
        { method: 'DELETE' }
      );

      if (response.ok) {
        onRefresh();
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to remove member');
      }
    } catch (err) {
      console.error('Error removing member:', err);
      const message = err instanceof Error ? err.message : 'Failed to remove member';
      alert(message);
    }
  };

  const handleChangeRole = async (memberId: number, newRole: string) => {
    try {
      const response = await fetchAPI(
        `${API_ENDPOINTS.teams}/${teamId}/members/${memberId}/role?new_role=${newRole}`,
        { method: 'PUT' }
      );

      if (response.ok) {
        onRefresh();
        setShowMenu(null);
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to change role');
      }
    } catch (err) {
      console.error('Error changing role:', err);
      const message = err instanceof Error ? err.message : 'Failed to change role';
      alert(message);
    }
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white">Team Members</h3>
          <p className="text-gray-400 text-sm">{members.length} members</p>
        </div>
        <button
          onClick={onInvite}
          className="px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all flex items-center gap-2"
        >
          <UserPlus className="w-4 h-4" />
          Invite Member
        </button>
      </div>

      {/* Members Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {members.map((member, index) => (
          <div
            key={member.id}
            className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10 hover:border-white/20 transition-all slide-in-top"
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            <div className="flex items-start justify-between">
              {/* Member Info */}
              <div className="flex items-center gap-3 flex-1">
                <div className="w-12 h-12 bg-gradient-to-br from-[#B5C7EB] to-[#A4A5F5] rounded-full flex items-center justify-center text-white font-bold text-lg">
                  {member.username.charAt(0).toUpperCase()}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h4 className="text-white font-medium">{member.username}</h4>
                    <div className={`px-2 py-0.5 rounded-full text-xs font-medium border flex items-center gap-1 ${getRoleBadgeColor(member.role)}`}>
                      {getRoleIcon(member.role)}
                      {member.role}
                    </div>
                  </div>
                  <div className="flex items-center gap-1 text-gray-400 text-sm mt-1">
                    <Mail className="w-3 h-3" />
                    {member.email}
                  </div>
                  <p className="text-gray-500 text-xs mt-1">
                    Joined {new Date(member.joined_at).toLocaleDateString()}
                  </p>
                </div>
              </div>

              {/* Actions Menu */}
              {member.role !== 'owner' && (
                <div className="relative">
                  <button
                    onClick={() => setShowMenu(showMenu === member.id ? null : member.id)}
                    className="p-2 hover:bg-white/10 rounded-lg transition-all"
                  >
                    <MoreVertical className="w-4 h-4 text-gray-400" />
                  </button>

                  {showMenu === member.id && (
                    <div className="absolute right-0 mt-2 w-48 bg-[#1a1a2e] border border-white/10 rounded-lg shadow-xl z-10">
                      <div className="p-2">
                        <button
                          onClick={() => handleChangeRole(member.id, 'admin')}
                          className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-white/10 rounded-lg transition-all flex items-center gap-2"
                        >
                          <Shield className="w-4 h-4" />
                          Make Admin
                        </button>
                        <button
                          onClick={() => handleChangeRole(member.id, 'editor')}
                          className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-white/10 rounded-lg transition-all flex items-center gap-2"
                        >
                          <Shield className="w-4 h-4" />
                          Make Editor
                        </button>
                        <button
                          onClick={() => handleChangeRole(member.id, 'viewer')}
                          className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-white/10 rounded-lg transition-all flex items-center gap-2"
                        >
                          <Shield className="w-4 h-4" />
                          Make Viewer
                        </button>
                        <div className="border-t border-white/10 my-2" />
                        <button
                          onClick={() => handleRemoveMember(member.id)}
                          className="w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-red-500/10 rounded-lg transition-all flex items-center gap-2"
                        >
                          <Trash2 className="w-4 h-4" />
                          Remove Member
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {members.length === 0 && (
        <div className="text-center py-12">
          <UserPlus className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400 mb-4">No members yet</p>
          <button
            onClick={onInvite}
            className="px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all"
          >
            Invite First Member
          </button>
        </div>
      )}
    </div>
  );
}
