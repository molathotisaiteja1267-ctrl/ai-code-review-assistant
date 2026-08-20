import React, { useState, useEffect } from 'react';
import { BookOpen, Plus, Search, CheckCircle2, Layers } from 'lucide-react';
import { reviewService } from '../services/reviewService';
import { ProjectRule } from '../types';
import { useToast } from '../context/ToastContext';

export const ProjectRulesPage: React.FC = () => {
  const { showToast } = useToast();
  const [rules, setRules] = useState<ProjectRule[]>([]);
  const [name, setName] = useState('');
  const [ruleType, setRuleType] = useState('architecture');
  const [content, setContent] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchRules();
  }, []);

  const fetchRules = async () => {
    try {
      const data = await reviewService.getRules();
      setRules(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddRule = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !content.trim()) return;
    setLoading(true);
    try {
      await reviewService.createRule({ name, rule_type: ruleType, content });
      showToast('success', 'Rule added', 'Rule tokenized and stored in vector knowledge base.');
      setName('');
      setContent('');
      fetchRules();
    } catch (err) {
      showToast('error', 'Failed to add rule');
    } finally {
      setLoading(false);
    }
  };

  const handleTestSearch = async () => {
    if (!searchQuery.trim()) return;
    try {
      const res = await reviewService.searchRules(searchQuery);
      setSearchResults(res.matches || []);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-surface-border pb-3">
        <h1 className="text-2xl font-bold text-text-primary">Project Rules (RAG Knowledge Base)</h1>
        <p className="text-xs text-text-secondary mt-0.5">
          Store architectural constraints and team coding guidelines. The vector retriever injects matching rules during code review.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Add Rule */}
        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-4 shadow-subtle">
          <div className="flex items-center space-x-2 text-xs font-bold text-brand-600 uppercase tracking-wider">
            <Plus className="w-4 h-4" />
            <span>Add Guideline / Rule</span>
          </div>

          <form onSubmit={handleAddRule} className="space-y-3.5">
            <div className="space-y-1">
              <label className="text-xs font-semibold text-text-primary">Rule Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Repository Pattern Enforcement"
                className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-text-primary">Category</label>
              <select
                value={ruleType}
                onChange={(e) => setRuleType(e.target.value)}
                className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white"
              >
                <option value="architecture">Architecture Pattern</option>
                <option value="security">Security Standard</option>
                <option value="performance">Performance Guideline</option>
                <option value="reliability">Error Handling & Logging</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-text-primary">Guideline Requirement</label>
              <textarea
                rows={4}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="All database access must use repository classes instead of direct cursor queries..."
                className="w-full p-3 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white resize-none leading-relaxed"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-lg text-xs font-semibold bg-brand-500 hover:bg-brand-600 text-white flex items-center justify-center space-x-2 transition-all shadow-sm"
            >
              <span>Add to Vector Store</span>
            </button>
          </form>

          {/* Test Semantic Search Console */}
          <div className="pt-4 border-t border-surface-border space-y-3">
            <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">Test Vector Retrieval</span>
            <div className="flex space-x-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search semantic code, e.g. cursor.execute"
                className="flex-1 px-3 py-1.5 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500"
              />
              <button
                type="button"
                onClick={handleTestSearch}
                className="px-3 py-1.5 rounded-lg bg-white border border-surface-border text-xs font-semibold text-text-primary hover:bg-surface-hover shadow-subtle"
              >
                Search
              </button>
            </div>

            {searchResults.length > 0 && (
              <div className="p-3 bg-surface-subtle rounded-lg border border-surface-border space-y-1.5 text-xs text-text-primary">
                <span className="font-bold text-brand-600">Retrieved Rule Matches:</span>
                {searchResults.map((m, i) => (
                  <p key={i} className="text-[11px] text-text-secondary leading-relaxed">• {m}</p>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right: Active Rules List */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">Active Rules ({rules.length})</span>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-accent-greenLight text-accent-green border border-green-200">
              Indexed successfully
            </span>
          </div>

          <div className="space-y-3">
            {rules.map((r) => (
              <div key={r.id} className="p-4 bg-white border border-surface-border rounded-xl space-y-2 shadow-subtle">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-brand-50 text-brand-700 border border-brand-200 uppercase">
                      {r.rule_type}
                    </span>
                    <h3 className="text-sm font-bold text-text-primary">{r.name}</h3>
                  </div>
                  <span className="text-[11px] text-accent-green font-medium flex items-center space-x-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Active in Pipeline</span>
                  </span>
                </div>
                <p className="text-xs text-text-primary leading-relaxed">{r.content}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
