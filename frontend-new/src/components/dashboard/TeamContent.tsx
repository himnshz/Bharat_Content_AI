'use client';

import { useState, useEffect } from 'react';
import { Users, Plus, UserPlus, CheckCircle, Activity, Crown, Shield, Edit, Eye } from 'lucide-react';
import { API_ENDPOINTS, fetchAPI } from '@/lib/api';
import TeamList from './team/TeamList';
import MemberList from './team/MemberList';
import InviteModal from './team/InviteModal';
import ActivityFeed from './team/ActivityFeed';
import ApprovalCard from './team/ApprovalCard';

interface Team {
  id: number;
  name: string;
  description: string;
  owner_id: number;
  member_count: number;
  created_at: string;
}

interface Member {
  id: number;
  user_id: number;
  username: string;
  email: string;
  role: string;
  joined_at: string;
}

interface Approval {
  id: number;
  status: string;
  requested_by: number;
  approver_id: number;
  requested_at: string;
  reviewed_at: string | null;
  notes: string | null;
}

export default function TeamContent() {
  const [activeTab, setActiveTab] = useState<'teams' | 'members' | 'approvals' | 'activity'>('teams');
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);
  const [members, setMembers] = useState<Member[]>([]);
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [showCreateTeam, setShowCreateTeam] = useState(false);

  useEffect(() => {
    fetchTeams();
  }, []);

  useEffect(() => {
    if (selectedTeam) {
      fetchMembers(selectedTeam.id);
      fetchApprovals(selectedTeam.id);
    }
  }, [selectedTeam]);

  const fetchTeams = async () => {
    try {
      setError('');
      const response = await fetchAPI(`${API_ENDPOINTS.teams}/user`);
      
      if (response.ok) {
        const data = await response.json();
        setTeams(data);
        if (data.length > 0 && !selectedTeam) {
          setSelectedTeam(data[0]);
        }
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to fetch teams');
      }
    } catch (err) {
      console.error('Error fetching teams:', err);
      const message = err instanceof Error ? err.message : 'Failed to load teams';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const fetchMembers = async (teamId: number) => {
    try {
      setError('');
      const response = await fetchAPI(`${API_ENDPOINTS.teams}/${teamId}/members`);
      
      if (response.ok) {
        const data = await response.json();
        setMembers(data);
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to fetch members');
      }
    } catch (err) {
      console.error('Error fetching members:', err);
      const message = err instanceof Error ? err.message : 'Failed to load members';
      setError(message);
    }
  };

  const fetchApprovals = async (teamId: number) => {
    try {
      setError('');
      const response = await fetchAPI(`${API_ENDPOINTS.teams}/${teamId}/approvals/pending`);
      
      if (response.ok) {
        const data = await response.json();
        setApprovals(data);
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to fetch approvals');
      }
    } catch (err) {
      console.error('Error fetching approvals:', err);
      const message = err instanceof Error ? err.message : 'Failed to load approvals';
      setError(message);
    }
  };

  const handleCreateTeam = async (name: string, description: string) => {
    try {
      setError('');
      const response = await fetchAPI(`${API_ENDPOINTS.teams}/`, {
        method: 'POST',
        body: JSON.stringify({ name, description }),
      });

      if (response.ok) {
        fetchTeams();
        setShowCreateTeam(false);
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to create team');
      }
    } catch (err) {
      console.error('Error creating team:', err);
      const message = err instanceof Error ? err.message : 'Failed to create team';
      setError(message);
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'owner':
        return <Crown className="w-4 h-4 text-yellow-400" />;
      case 'admin':
        return <Shield className="w-4 h-4 text-purple-400" />;
      case 'editor':
        return <Edit className="w-4 h-4 text-blue-400" />;
      default:
        return <Eye className="w-4 h-4 text-gray-400" />;
    }
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'owner':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'admin':
        return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
      case 'editor':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

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
            <Users className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Team Collaboration</h2>
            <p className="text-gray-400">Manage teams, members, and workflows</p>
          </div>
        </div>

        <button
          onClick={() => setShowCreateTeam(true)}
          className="px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Create Team
        </button>
      </div>

      {/* Team Selector */}
      {teams.length > 0 && (
        <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
          <div className="flex items-center gap-3 mb-3">
            <Users className="w-5 h-5 text-[#B5C7EB]" />
            <span className="text-white font-medium">Select Team</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {teams.map(team => (
              <button
                key={team.id}
                onClick={() => setSelectedTeam(team)}
                className={`px-4 py-2 rounded-lg transition-all ${
                  selectedTeam?.id === team.id
                    ? 'bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] text-white'
                    : 'bg-white/5 text-gray-400 hover:bg-white/10'
                }`}
              >
                {team.name}
                <span className="ml-2 text-xs opacity-70">({team.member_count})</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-2 border-b border-white/10">
        <button
          onClick={() => setActiveTab('teams')}
          className={`px-4 py-3 font-medium transition-all relative ${
            activeTab === 'teams'
              ? 'text-[#B5C7EB]'
              : 'text-gray-400 hover:text-gray-300'
          }`}
        >
          <div className="flex items-center gap-2">
            <Users className="w-4 h-4" />
            Teams
          </div>
          {activeTab === 'teams' && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5]" />
          )}
        </button>

        <button
          onClick={() => setActiveTab('members')}
          className={`px-4 py-3 font-medium transition-all relative ${
            activeTab === 'members'
              ? 'text-[#B5C7EB]'
              : 'text-gray-400 hover:text-gray-300'
          }`}
        >
          <div className="flex items-center gap-2">
            <UserPlus className="w-4 h-4" />
            Members
            {members.length > 0 && (
              <span className="px-2 py-0.5 bg-[#B5C7EB]/20 text-[#B5C7EB] rounded-full text-xs">
                {members.length}
              </span>
            )}
          </div>
          {activeTab === 'members' && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5]" />
          )}
        </button>

        <button
          onClick={() => setActiveTab('approvals')}
          className={`px-4 py-3 font-medium transition-all relative ${
            activeTab === 'approvals'
              ? 'text-[#B5C7EB]'
              : 'text-gray-400 hover:text-gray-300'
          }`}
        >
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Approvals
            {approvals.length > 0 && (
              <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 rounded-full text-xs">
                {approvals.length}
              </span>
            )}
          </div>
          {activeTab === 'approvals' && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5]" />
          )}
        </button>

        <button
          onClick={() => setActiveTab('activity')}
          className={`px-4 py-3 font-medium transition-all relative ${
            activeTab === 'activity'
              ? 'text-[#B5C7EB]'
              : 'text-gray-400 hover:text-gray-300'
          }`}
        >
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4" />
            Activity
          </div>
          {activeTab === 'activity' && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5]" />
          )}
        </button>
      </div>

      {/* Tab Content */}
      <div className="min-h-[500px]">
        {activeTab === 'teams' && (
          <TeamList
            teams={teams}
            selectedTeam={selectedTeam}
            onSelectTeam={setSelectedTeam}
            onRefresh={fetchTeams}
            getRoleIcon={getRoleIcon}
            getRoleBadgeColor={getRoleBadgeColor}
          />
        )}

        {activeTab === 'members' && selectedTeam && (
          <MemberList
            teamId={selectedTeam.id}
            members={members}
            onInvite={() => setShowInviteModal(true)}
            onRefresh={() => fetchMembers(selectedTeam.id)}
            getRoleIcon={getRoleIcon}
            getRoleBadgeColor={getRoleBadgeColor}
          />
        )}

        {activeTab === 'approvals' && selectedTeam && (
          <div className="space-y-4">
            {approvals.length === 0 ? (
              <div className="text-center py-12">
                <CheckCircle className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                <p className="text-gray-400">No pending approvals</p>
              </div>
            ) : (
              approvals.map(approval => (
                <ApprovalCard
                  key={approval.id}
                  approval={approval}
                  onRefresh={() => fetchApprovals(selectedTeam.id)}
                />
              ))
            )}
          </div>
        )}

        {activeTab === 'activity' && selectedTeam && (
          <ActivityFeed teamId={selectedTeam.id} />
        )}
      </div>

      {/* Invite Modal */}
      {showInviteModal && selectedTeam && (
        <InviteModal
          teamId={selectedTeam.id}
          onClose={() => setShowInviteModal(false)}
          onSuccess={() => {
            setShowInviteModal(false);
            fetchMembers(selectedTeam.id);
          }}
        />
      )}

      {/* Create Team Modal */}
      {showCreateTeam && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-[#1a1a2e] rounded-xl p-6 max-w-md w-full mx-4 border border-white/10">
            <h3 className="text-xl font-bold text-white mb-4">Create New Team</h3>
            
            <form
              onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                handleCreateTeam(
                  formData.get('name') as string,
                  formData.get('description') as string
                );
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-gray-400 text-sm mb-2">Team Name</label>
                <input
                  type="text"
                  name="name"
                  required
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                  placeholder="Marketing Team"
                />
              </div>

              <div>
                <label className="block text-gray-400 text-sm mb-2">Description</label>
                <textarea
                  name="description"
                  rows={3}
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                  placeholder="Team description..."
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setShowCreateTeam(false)}
                  className="flex-1 px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all"
                >
                  Create Team
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
