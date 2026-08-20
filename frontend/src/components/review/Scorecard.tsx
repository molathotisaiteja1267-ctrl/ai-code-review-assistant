import React from 'react';
import { ShieldCheck, AlertTriangle, Clock, Zap } from 'lucide-react';
import { Review } from '../../types';

interface ScorecardProps {
  review: Review;
}

export const Scorecard: React.FC<ScorecardProps> = ({ review }) => {
  const getGradeColor = (grade: string) => {
    if (grade.startsWith('A')) return 'text-accent-green bg-accent-greenLight border-green-200';
    if (grade.startsWith('B')) return 'text-accent-blue bg-accent-blueLight border-blue-200';
    if (grade.startsWith('C')) return 'text-amber-700 bg-accent-yellowLight border-amber-300';
    return 'text-accent-red bg-accent-redLight border-red-200';
  };

  const getRiskBadge = (risk: string) => {
    if (risk === 'CRITICAL') return 'bg-accent-redLight text-accent-red border-red-300 font-bold';
    if (risk === 'HIGH') return 'bg-orange-50 text-brand-600 border-brand-200 font-bold';
    if (risk === 'MEDIUM') return 'bg-accent-yellowLight text-amber-800 border-amber-300 font-semibold';
    return 'bg-accent-greenLight text-accent-green border-green-300 font-semibold';
  };

  return (
    <div className="bg-white border border-surface-border rounded-xl p-5 shadow-subtle flex flex-col md:flex-row items-center justify-between gap-6">
      <div className="flex items-center space-x-5">
        <div className={`w-18 h-18 rounded-xl border flex flex-col items-center justify-center font-bold px-4 py-2 ${getGradeColor(review.letter_grade)}`}>
          <span className="text-3xl tracking-tight leading-none">{review.letter_grade}</span>
          <span className="text-[10px] tracking-wider uppercase font-semibold mt-1 opacity-80">Grade</span>
        </div>

        <div className="space-y-1">
          <div className="flex items-center space-x-3">
            <h2 className="text-lg font-bold text-text-primary">{review.title}</h2>
            <span className={`px-2.5 py-0.5 text-xs uppercase rounded-full border ${getRiskBadge(review.risk_level)}`}>
              {review.risk_level} Risk
            </span>
          </div>
          <p className="text-xs text-text-secondary max-w-2xl leading-relaxed">
            {review.summary || 'Multi-tier static analysis and AI verification completed.'}
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-6 border-t md:border-t-0 md:border-l border-surface-border pt-4 md:pt-0 md:pl-6 shrink-0">
        <div className="text-center">
          <div className="text-2xl font-bold text-brand-600">{review.overall_score.toFixed(1)}<span className="text-xs font-normal text-text-muted">/100</span></div>
          <div className="text-[11px] text-text-secondary font-medium uppercase">Quality Score</div>
        </div>

        <div className="text-center">
          <div className="text-2xl font-bold text-text-primary">{review.issues?.length || 0}</div>
          <div className="text-[11px] text-text-secondary font-medium uppercase">Issues Found</div>
        </div>

        <div className="text-center">
          <div className="text-2xl font-bold text-text-primary">{review.execution_time_ms.toFixed(0)}<span className="text-xs font-normal text-text-muted">ms</span></div>
          <div className="text-[11px] text-text-secondary font-medium uppercase">Latency</div>
        </div>
      </div>
    </div>
  );
};
