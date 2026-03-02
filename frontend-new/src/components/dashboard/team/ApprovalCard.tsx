'use client';

import { useState } from 'react';
import { CheckCircle, XCircle, Clock, FileText, MessageSquare } from 'lucide-react';
import { API_ENDPOINTS, fetchAPI } from '@/lib/api';

interface Approval {
  id: number;
  status: string;
  requested_by: number;
  approver_id: number;
  requested_at: string;
  reviewed_at: string | null;
  notes: string | null;
}

interface ApprovalCardProps {
  approval: Approval;
  onRefresh: () => void;
}

export default function ApprovalCard({ approval, onRefresh }: ApprovalCardProps) {
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);

  const handleReview = async (status: 'approved' | 'rejected') => {
    setLoading(true);

    try {
      const notesParam = notes ? `&notes=${encodeURIComponent(notes)}` : '';
      const response = await fetchAPI(
        `${API_ENDPOINTS.teams.replace('/teams', '')}/teams/approvals/${approval.id}/review?status=${status}${notesParam}`,
        { method: 'PUT' }
      );

      if (response.ok) {
        onRefresh();
        setShowReviewModal(false);
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to review approval');
      }
    } catch (err) {
      console.error('Error reviewing approval:', err);
      const message = err instanceof Error ? err.message : 'Failed to review approval';
      alert(message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = () => {
    switch (approval.status) {
      case 'pending':
        return (
          <span className="px-3 py-1 bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 rounded-full text-sm font-medium flex items-center gap-1">
            <Clock className="w-3 h-3" />
            Pending Review
          </span>
        );
      case 'approved':
        return (
          <span className="px-3 py-1 bg-green-500/20 text-green-400 border border-green-500/30 rounded-full text-sm font-medium flex items-center gap-1">
            <CheckCircle className="w-3 h-3" />
            Approved
          </span>
        );
      case 'rejected':
        return (
          <span className="px-3 py-1 bg-red-500/20 text-red-400 border border-red-500/30 rounded-full text-sm font-medium flex items-center gap-1">
            <XCircle className="w-3 h-3" />
            Rejected
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <>
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-white/20 transition-all">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-yellow-500/10 rounded-lg">
              <FileText className="w-5 h-5 text-yellow-400" />
            </div>
            <div>
              <h4 className="text-white font-medium">Approval Request #{approval.id}</h4>
              <p className="text-gray-400 text-sm">
                Requested {new Date(approval.requested_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          {getStatusBadge()}
        </div>

        {approval.notes && (
          <div className="mb-4 p-3 bg-white/5 rounded-lg border border-white/10">
            <div className="flex items-center gap-2 mb-2">
              <MessageSquare className="w-4 h-4 text-[#B5C7EB]" />
              <span className="text-gray-400 text-sm">Review Notes</span>
            </div>
            <p className="text-white text-sm">{approval.notes}</p>
          </div>
        )}

        {approval.status === 'pending' && (
          <div className="flex gap-3">
            <button
              onClick={() => handleReview('approved')}
              disabled={loading}
              className="flex-1 px-4 py-2 bg-green-500/20 hover:bg-green-500/30 text-green-400 border border-green-500/30 rounded-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <CheckCircle className="w-4 h-4" />
              Approve
            </button>
            <button
              onClick={() => setShowReviewModal(true)}
              disabled={loading}
              className="flex-1 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500/30 rounded-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <XCircle className="w-4 h-4" />
              Reject
            </button>
          </div>
        )}

        {approval.reviewed_at && (
          <p className="text-gray-500 text-sm mt-4">
            Reviewed on {new Date(approval.reviewed_at).toLocaleDateString()}
          </p>
        )}
      </div>

      {/* Review Modal */}
      {showReviewModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-[#1a1a2e] rounded-xl p-6 max-w-md w-full mx-4 border border-white/10">
            <h3 className="text-xl font-bold text-white mb-4">Reject Approval</h3>
            
            <div className="mb-4">
              <label className="block text-gray-400 text-sm mb-2">
                Reason for rejection (optional)
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={4}
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                placeholder="Explain why this is being rejected..."
              />
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setShowReviewModal(false)}
                className="flex-1 px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
              >
                Cancel
              </button>
              <button
                onClick={() => handleReview('rejected')}
                disabled={loading}
                className="flex-1 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500/30 rounded-lg transition-all disabled:opacity-50"
              >
                {loading ? 'Rejecting...' : 'Reject'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
