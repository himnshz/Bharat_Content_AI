'use client';

import { useState, useEffect } from 'react';
import { FileText, Plus, Search, Star, Copy, Edit, Trash2, Eye, Filter, Sparkles } from 'lucide-react';
import { API_ENDPOINTS, fetchAPI } from '@/lib/api';

interface Template {
  id: number;
  user_id: number | null;
  name: string;
  description: string | null;
  category: string;
  content: string;
  language: string;
  tone: string;
  platform: string | null;
  is_public: boolean;
  is_system: boolean;
  is_favorite: boolean;
  usage_count: number;
  created_at: string;
}

const categories = [
  { value: 'all', label: 'All Templates', icon: '📁' },
  { value: 'social_media', label: 'Social Media', icon: '📱' },
  { value: 'blog', label: 'Blog', icon: '📝' },
  { value: 'email', label: 'Email', icon: '📧' },
  { value: 'marketing', label: 'Marketing', icon: '📢' },
  { value: 'announcement', label: 'Announcement', icon: '📣' },
  { value: 'product', label: 'Product', icon: '🛍️' },
  { value: 'event', label: 'Event', icon: '🎉' },
  { value: 'educational', label: 'Educational', icon: '📚' },
  { value: 'entertainment', label: 'Entertainment', icon: '🎬' },
  { value: 'news', label: 'News', icon: '📰' },
];

export default function TemplatesContent() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [filteredTemplates, setFilteredTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showPreviewModal, setShowPreviewModal] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [activeTab, setActiveTab] = useState<'all' | 'my' | 'favorites' | 'system'>('all');

  useEffect(() => {
    fetchTemplates();
  }, [activeTab]);

  useEffect(() => {
    filterTemplates();
  }, [templates, selectedCategory, searchQuery]);

  const fetchTemplates = async () => {
    try {
      setError('');
      let url = `${API_ENDPOINTS.templates}/`;
      
      if (activeTab === 'my') {
        url = `${API_ENDPOINTS.templates}/user`;
      } else if (activeTab === 'favorites') {
        url = `${API_ENDPOINTS.templates}/favorites`;
      } else if (activeTab === 'system') {
        url = `${API_ENDPOINTS.templates}/system`;
      }
      
      const response = await fetchAPI(url);
      
      if (response.ok) {
        const data = await response.json();
        setTemplates(data);
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to fetch templates');
      }
    } catch (err) {
      console.error('Error fetching templates:', err);
      const message = err instanceof Error ? err.message : 'Failed to load templates';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const filterTemplates = () => {
    let filtered = templates;
    
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(t => t.category === selectedCategory);
    }
    
    if (searchQuery) {
      filtered = filtered.filter(t =>
        t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.description?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    setFilteredTemplates(filtered);
  };

  const handleUseTemplate = async (template: Template) => {
    try {
      setError('');
      const response = await fetchAPI(`${API_ENDPOINTS.templates}/${template.id}/use`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error('Failed to use template');
      }
      
      // Copy to clipboard
      navigator.clipboard.writeText(template.content);
      
      // Show success message
      alert('Template copied to clipboard!');
      
      fetchTemplates();
    } catch (err) {
      console.error('Error using template:', err);
      const message = err instanceof Error ? err.message : 'Failed to use template';
      setError(message);
    }
  };

  const handleToggleFavorite = async (template: Template) => {
    try {
      setError('');
      const response = await fetchAPI(`${API_ENDPOINTS.templates}/${template.id}/favorite`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error('Failed to toggle favorite');
      }
      
      fetchTemplates();
    } catch (err) {
      console.error('Error toggling favorite:', err);
      const message = err instanceof Error ? err.message : 'Failed to update favorite';
      setError(message);
    }
  };

  const handleDeleteTemplate = async (templateId: number) => {
    if (!confirm('Are you sure you want to delete this template?')) return;
    
    try {
      setError('');
      const response = await fetchAPI(`${API_ENDPOINTS.templates}/${templateId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        fetchTemplates();
      } else {
        throw new Error('Failed to delete template');
      }
    } catch (err) {
      console.error('Error deleting template:', err);
      const message = err instanceof Error ? err.message : 'Failed to delete template';
      setError(message);
    }
  };

  const getCategoryIcon = (category: string) => {
    const cat = categories.find(c => c.value === category);
    return cat?.icon || '📁';
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
            <FileText className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Content Templates</h2>
            <p className="text-gray-400">Speed up content creation with templates</p>
          </div>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Create Template
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-white/10">
        {[
          { id: 'all', label: 'All Templates', count: templates.length },
          { id: 'my', label: 'My Templates', count: templates.filter(t => t.user_id).length },
          { id: 'favorites', label: 'Favorites', count: templates.filter(t => t.is_favorite).length },
          { id: 'system', label: 'System', count: templates.filter(t => t.is_system).length },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-3 font-medium transition-all relative ${
              activeTab === tab.id
                ? 'text-[#B5C7EB]'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            <div className="flex items-center gap-2">
              {tab.label}
              {tab.count > 0 && (
                <span className="px-2 py-0.5 bg-[#B5C7EB]/20 text-[#B5C7EB] rounded-full text-xs">
                  {tab.count}
                </span>
              )}
            </div>
            {activeTab === tab.id && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5]" />
            )}
          </button>
        ))}
      </div>

      {/* Search and Filter */}
      <div className="flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search templates..."
            className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
          />
        </div>

        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
        >
          {categories.map(cat => (
            <option key={cat.value} value={cat.value}>
              {cat.icon} {cat.label}
            </option>
          ))}
        </select>
      </div>

      {/* Templates Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredTemplates.map((template, index) => (
          <div
            key={template.id}
            className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-white/20 transition-all slide-in-top"
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="text-3xl">{getCategoryIcon(template.category)}</div>
                <div>
                  <h3 className="text-white font-bold">{template.name}</h3>
                  <p className="text-gray-400 text-sm">{template.category.replace('_', ' ')}</p>
                </div>
              </div>

              <button
                onClick={() => handleToggleFavorite(template)}
                className="p-2 hover:bg-white/10 rounded-lg transition-all"
              >
                <Star
                  className={`w-5 h-5 ${
                    template.is_favorite
                      ? 'fill-yellow-400 text-yellow-400'
                      : 'text-gray-400'
                  }`}
                />
              </button>
            </div>

            {/* Description */}
            {template.description && (
              <p className="text-gray-400 text-sm mb-4 line-clamp-2">
                {template.description}
              </p>
            )}

            {/* Tags */}
            <div className="flex flex-wrap gap-2 mb-4">
              {template.is_system && (
                <span className="px-2 py-1 bg-purple-500/20 text-purple-400 rounded text-xs">
                  System
                </span>
              )}
              {template.platform && (
                <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">
                  {template.platform}
                </span>
              )}
              <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">
                {template.language}
              </span>
              <span className="px-2 py-1 bg-cyan-500/20 text-cyan-400 rounded text-xs">
                {template.tone}
              </span>
            </div>

            {/* Stats */}
            <div className="flex items-center gap-4 mb-4 text-gray-500 text-sm">
              <div className="flex items-center gap-1">
                <Sparkles className="w-4 h-4" />
                {template.usage_count} uses
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2">
              <button
                onClick={() => handleUseTemplate(template)}
                className="flex-1 px-3 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all flex items-center justify-center gap-2"
              >
                <Copy className="w-4 h-4" />
                Use
              </button>
              <button
                onClick={() => {
                  setSelectedTemplate(template);
                  setShowPreviewModal(true);
                }}
                className="px-3 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
              >
                <Eye className="w-4 h-4" />
              </button>
              {template.user_id && !template.is_system && (
                <>
                  <button
                    onClick={() => {
                      setSelectedTemplate(template);
                      setShowCreateModal(true);
                    }}
                    className="px-3 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteTemplate(template.id)}
                    className="px-3 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg transition-all"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </>
              )}
            </div>
          </div>
        ))}
      </div>

      {filteredTemplates.length === 0 && (
        <div className="text-center py-12">
          <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400 mb-4">No templates found</p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all"
          >
            Create Your First Template
          </button>
        </div>
      )}

      {/* Preview Modal */}
      {showPreviewModal && selectedTemplate && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-[#1a1a2e] rounded-xl p-6 max-w-2xl w-full mx-4 border border-white/10 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-white">{selectedTemplate.name}</h3>
              <button
                onClick={() => setShowPreviewModal(false)}
                className="p-2 hover:bg-white/10 rounded-lg transition-all"
              >
                <span className="text-gray-400 text-2xl">×</span>
              </button>
            </div>

            {selectedTemplate.description && (
              <p className="text-gray-400 mb-4">{selectedTemplate.description}</p>
            )}

            <div className="bg-white/5 rounded-lg p-4 border border-white/10 mb-4">
              <pre className="text-white whitespace-pre-wrap font-mono text-sm">
                {selectedTemplate.content}
              </pre>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => {
                  handleUseTemplate(selectedTemplate);
                  setShowPreviewModal(false);
                }}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all"
              >
                Use Template
              </button>
              <button
                onClick={() => setShowPreviewModal(false)}
                className="px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create Template Modal */}
      {showCreateModal && !selectedTemplate && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-[#1a1a2e] rounded-xl p-6 max-w-2xl w-full mx-4 border border-white/10 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-white">Create New Template</h3>
              <button
                onClick={() => setShowCreateModal(false)}
                className="p-2 hover:bg-white/10 rounded-lg transition-all"
              >
                <span className="text-gray-400 text-2xl">×</span>
              </button>
            </div>

            <form
              onSubmit={async (e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                
                try {
                  setError('');
                  const response = await fetchAPI(`${API_ENDPOINTS.templates}/`, {
                    method: 'POST',
                    body: JSON.stringify({
                      name: formData.get('name'),
                      description: formData.get('description'),
                      category: formData.get('category'),
                      content: formData.get('content'),
                      language: formData.get('language'),
                      tone: formData.get('tone'),
                      platform: formData.get('platform') || null,
                      is_public: false,
                    }),
                  });

                  if (response.ok) {
                    fetchTemplates();
                    setShowCreateModal(false);
                    alert('✅ Template created successfully!');
                  } else {
                    const data = await response.json();
                    throw new Error(data.detail || 'Failed to create template');
                  }
                } catch (err) {
                  console.error('Error creating template:', err);
                  const message = err instanceof Error ? err.message : 'Failed to create template';
                  alert(`❌ ${message}`);
                }
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-gray-400 text-sm mb-2">Template Name</label>
                <input
                  type="text"
                  name="name"
                  required
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                  placeholder="My Awesome Template"
                />
              </div>

              <div>
                <label className="block text-gray-400 text-sm mb-2">Description</label>
                <input
                  type="text"
                  name="description"
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                  placeholder="Brief description of the template"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-gray-400 text-sm mb-2">Category</label>
                  <select
                    name="category"
                    required
                    className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                  >
                    {categories.filter(c => c.value !== 'all').map(cat => (
                      <option key={cat.value} value={cat.value}>
                        {cat.icon} {cat.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-gray-400 text-sm mb-2">Language</label>
                  <select
                    name="language"
                    className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                  >
                    <option value="english">English</option>
                    <option value="hindi">Hindi</option>
                    <option value="bengali">Bengali</option>
                    <option value="tamil">Tamil</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-gray-400 text-sm mb-2">Tone</label>
                  <select
                    name="tone"
                    className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                  >
                    <option value="professional">Professional</option>
                    <option value="friendly">Friendly</option>
                    <option value="exciting">Exciting</option>
                    <option value="informative">Informative</option>
                  </select>
                </div>

                <div>
                  <label className="block text-gray-400 text-sm mb-2">Platform (Optional)</label>
                  <select
                    name="platform"
                    className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB]"
                  >
                    <option value="">Any Platform</option>
                    <option value="facebook">Facebook</option>
                    <option value="instagram">Instagram</option>
                    <option value="twitter">Twitter</option>
                    <option value="linkedin">LinkedIn</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-gray-400 text-sm mb-2">Template Content</label>
                <textarea
                  name="content"
                  required
                  rows={8}
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-[#B5C7EB] font-mono text-sm"
                  placeholder="Enter your template content here...&#10;&#10;Use [placeholders] for dynamic content.&#10;Example: Hello [Name], welcome to [Company]!"
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-[#B5C7EB] to-[#A4A5F5] hover:from-[#A4A5F5] to-[#8E70CF] text-white rounded-lg transition-all"
                >
                  Create Template
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
