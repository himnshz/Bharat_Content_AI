'use client';

import { useState } from 'react';
import { X, Mail, UserPlus, Eye, Edit, Shield } from 'lucide-react';
import { API_ENDPOINTS, fetchAPI, isValidEmail } from '@/lib/api';

interface InviteModalProps {
  teamId: number;
  onClose: () => void;
  onSuccess: () => void;
}

export default function InviteModal({ teamId, onClose, onSuccess }: InviteModalProps) {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState<'viewer' | 'editor' | 'admin'>('viewer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!isValidEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }
    
    setLoading(true);
    setError('');

    try {
      const response = await fetchAPI(
        `${API_ENDPOINTS.teams}/${teamId}/invites`,
        {
          method: 'POST',
          body: JSON.stringify({ email, role }),
        }
      );

      if (response.ok) {
        onSuccess();
      } else {
        const data = await response.json();
        setError(data.detail || 'Failed to send invite');
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to send invite';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const roles = [
    {
      value: 'viewer',
      label: 'Viewer',
      icon: <Eye className="w-4 h-4" />,
      description: 'Can view content and analytics',
      color: 'text-gray-400',
    },
    {
      value: 'editor',
      label: 'Editor',
      icon: <Edit className="w-4 h-4" />,
      description: 'Can create and edit content',
      color: 'text-blue-400',
    },
    {
      value: 'admin',
      label: 'Admin',
      icon: <Shield className="w-4 h-4" />,
      description: 'Can manage team and members',
      color: 'text-purple-400',
    },
  ];

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 fade-in">
      <div className="bg-[#1a1a2e] rounded-xl p-6 max-w-md w-full mx-4 border border-white/10 slide-in-top">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-[#B5C7EB]/20 to-[#A4A5F5]/20 rounded-lg">
              <UserPlus className="w-5 h-5 text-[#B5C7EB]" />
            </div>
            <h3 className="text-xl font-bold text-white">Invite Team Member</h3>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-all"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleInvite} className="space-y-6">
          {/* Email Input */}
          <div>
            <label className="block text-gray-400 text-sm mb-2">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB] transition-all"
                placeholder="colleague@example.com"
              />
            </div>
          </div>

          {/* Role Selection */}
          <div>
            <label className="block text-gray-400 text-sm mb-3">Select Role</label>
            <div className="space-y-2">
              {roles.map((r) => (
                <button
                  key={r.value}
                  type="button"
                  onClick={() => setRole(r.value as any)}
                  className={`w-full p-4 rounded-lg border transition-all text-left ${
                    role === r.value
                      ? 'border-[#B5C7EB] bg-[#B5C7EB]/10'
                      : 'border-white/10 bg-white/5 hover:border-white/20'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`mt-0.5 ${r.color}`}>{r.icon}</div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-white font-medium">{r.label}</span>
                        {role === r.value && (
                          <div className="w-2 h-2 bg-[#B5C7EB] rounded-full" />
                        )}
                      </div>
                      <p className="text-gray-400 text-sm">{r.description}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-3 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-3 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                  Sending...
                </>
              ) : (
                <>
                  <UserPlus className="w-4 h-4" />
                  Send Invite
                </>
              )}
            </button>
          </div>
        </form>

        {/* Info */}
        <div className="mt-6 p-4 bg-[#B5C7EB]/10 border border-[#B5C7EB]/20 rounded-lg">
          <p className="text-[#B5C7EB] text-sm">
            💡 The invite will be sent to the email address and expire in 7 days.
          </p>
        </div>
      </div>
    </div>
  );
}
