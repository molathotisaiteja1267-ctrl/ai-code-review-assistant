import React from 'react';
import { Search } from 'lucide-react';

interface IssueFilterBarProps {
  searchQuery: string;
  onSearchChange: (q: string) => void;
  selectedSeverity: string;
  onSeverityChange: (s: string) => void;
  selectedCategory: string;
  onCategoryChange: (c: string) => void;
  minConfidence: number;
  onConfidenceChange: (c: number) => void;
  totalCount: number;
}

export const IssueFilterBar: React.FC<IssueFilterBarProps> = ({
  searchQuery,
  onSearchChange,
  selectedSeverity,
  onSeverityChange,
  selectedCategory,
  onCategoryChange,
  minConfidence,
  onConfidenceChange,
  totalCount
}) => {
  return (
    <div className="p-3 bg-white border border-surface-border rounded-xl space-y-3 shadow-subtle">
      <div className="flex flex-col sm:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-text-muted absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search findings, rules, or code..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary placeholder-text-muted focus:outline-none focus:border-brand-500 focus:bg-white transition-colors"
          />
        </div>

        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <select
            value={selectedSeverity}
            onChange={(e) => onSeverityChange(e.target.value)}
            className="px-2.5 py-1.5 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500"
          >
            <option value="all">All Severities</option>
            <option value="critical">Critical Only</option>
            <option value="high">High Only</option>
            <option value="medium">Medium Only</option>
            <option value="low">Low Only</option>
          </select>

          <select
            value={selectedCategory}
            onChange={(e) => onCategoryChange(e.target.value)}
            className="px-2.5 py-1.5 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500"
          >
            <option value="all">All Categories</option>
            <option value="security">Security</option>
            <option value="bug">Bugs</option>
            <option value="performance">Performance</option>
            <option value="code_quality">Code Quality</option>
            <option value="complexity">Complexity</option>
          </select>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs text-text-secondary pt-1 border-t border-surface-border">
        <div className="flex items-center space-x-3">
          <span>Min Confidence: {Math.round(minConfidence * 100)}%</span>
          <input
            type="range"
            min="0.5"
            max="0.95"
            step="0.05"
            value={minConfidence}
            onChange={(e) => onConfidenceChange(parseFloat(e.target.value))}
            className="w-24 accent-brand-500 cursor-pointer"
          />
        </div>

        <div className="font-semibold text-text-primary">
          Showing {totalCount} issue{totalCount === 1 ? '' : 's'}
        </div>
      </div>
    </div>
  );
};
