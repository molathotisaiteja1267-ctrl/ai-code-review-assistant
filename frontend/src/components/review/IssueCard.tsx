import React from 'react';
import { 
  ShieldAlert, 
  Wrench, 
  CheckCircle2, 
  Layers
} from 'lucide-react';
import { ReviewIssue } from '../../types';

interface IssueCardProps {
  issue: ReviewIssue;
  isSelected?: boolean;
  onSelect?: () => void;
  onGenerateFix?: (issue: ReviewIssue) => void;
}

export const IssueCard: React.FC<IssueCardProps> = ({
  issue,
  isSelected = false,
  onSelect,
  onGenerateFix
}) => {
  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'critical':
        return { bg: 'bg-accent-redLight text-accent-red border-red-200', label: 'CRITICAL' };
      case 'high':
        return { bg: 'bg-orange-50 text-brand-600 border-brand-200', label: 'HIGH' };
      case 'medium':
        return { bg: 'bg-accent-yellowLight text-amber-800 border-amber-200', label: 'MEDIUM' };
      default:
        return { bg: 'bg-accent-blueLight text-accent-blue border-blue-200', label: 'LOW' };
    }
  };

  const badge = getSeverityBadge(issue.severity);

  return (
    <div
      onClick={onSelect}
      className={`p-4 rounded-xl border transition-all cursor-pointer space-y-2.5 shadow-subtle ${
        isSelected
          ? 'bg-brand-50/40 border-brand-500 ring-1 ring-brand-500/30'
          : 'bg-white border-surface-border hover:border-brand-300 hover:bg-surface-hover'
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-0.5 text-[10px] font-bold tracking-wider rounded border ${badge.bg}`}>
              {badge.label}
            </span>
            <span className="text-xs font-semibold text-text-secondary uppercase tracking-wide">
              {issue.category}
            </span>
            <span className="text-xs text-text-muted">• Line {issue.line_start}{issue.line_end !== issue.line_start ? `-${issue.line_end}` : ''}</span>
          </div>
          <h4 className="text-sm font-bold text-text-primary leading-snug">{issue.title}</h4>
        </div>

        <div className="flex items-center space-x-1 shrink-0">
          <span className="text-[11px] font-medium text-text-secondary bg-surface-subtle px-2 py-0.5 rounded border border-surface-border">
            {Math.round(issue.confidence * 100)}% conf
          </span>
        </div>
      </div>

      <p className="text-xs text-text-primary leading-relaxed">{issue.explanation}</p>

      {issue.impact && (
        <div className="p-2.5 rounded-lg bg-accent-redLight/60 border border-red-100 text-xs text-red-900 space-y-0.5">
          <span className="font-bold text-[11px] uppercase tracking-wider text-accent-red">Impact: </span>
          <span>{issue.impact}</span>
        </div>
      )}

      {issue.recommendation && (
        <div className="p-2.5 rounded-lg bg-brand-50/60 border border-brand-100 text-xs text-brand-900 space-y-0.5">
          <span className="font-bold text-[11px] uppercase tracking-wider text-brand-600">Recommendation: </span>
          <span>{issue.recommendation}</span>
        </div>
      )}

      {issue.evidence_sources && issue.evidence_sources.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5 pt-1">
          <Layers className="w-3 h-3 text-text-muted shrink-0" />
          {issue.evidence_sources.map((ev, idx) => (
            <span key={idx} className="text-[10px] font-medium px-2 py-0.5 bg-surface-subtle border border-surface-border text-text-secondary rounded-md">
              {ev}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between pt-2 border-t border-surface-border">
        <div className="text-[11px] text-text-muted">
          {issue.is_resolved ? (
            <span className="flex items-center space-x-1 text-accent-green font-medium">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Resolved</span>
            </span>
          ) : (
            <span>Rule: {issue.rule_id || 'GENERAL-RULE'}</span>
          )}
        </div>

        <button
          onClick={(e) => {
            e.stopPropagation();
            onGenerateFix && onGenerateFix(issue);
          }}
          className="flex items-center space-x-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg bg-brand-500 hover:bg-brand-600 text-white transition-colors shadow-sm"
        >
          <Wrench className="w-3.5 h-3.5" />
          <span>Generate & Validate Fix</span>
        </button>
      </div>
    </div>
  );
};
