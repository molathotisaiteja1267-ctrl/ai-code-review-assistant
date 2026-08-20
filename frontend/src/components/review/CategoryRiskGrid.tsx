import React from 'react';
import { Shield, Bug, Gauge, Cpu } from 'lucide-react';
import { Review } from '../../types';

interface CategoryRiskGridProps {
  review: Review;
}

export const CategoryRiskGrid: React.FC<CategoryRiskGridProps> = ({ review }) => {
  const categories = [
    { label: 'Security Posture', score: review.security_score, icon: Shield, color: 'text-accent-red', barColor: 'bg-accent-red' },
    { label: 'System Reliability', score: review.reliability_score, icon: Bug, color: 'text-brand-600', barColor: 'bg-brand-500' },
    { label: 'Performance & Algo', score: review.performance_score, icon: Gauge, color: 'text-amber-600', barColor: 'bg-accent-yellow' },
    { label: 'Maintainability', score: review.maintainability_score, icon: Cpu, color: 'text-accent-blue', barColor: 'bg-accent-blue' },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {categories.map((cat) => {
        const Icon = cat.icon;
        const percentage = Math.min(100, Math.max(0, cat.score * 10));
        return (
          <div key={cat.label} className="bg-white border border-surface-border rounded-xl p-4 space-y-3 shadow-subtle">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Icon className={`w-4 h-4 ${cat.color}`} />
                <span className="text-xs font-semibold text-text-primary">{cat.label}</span>
              </div>
              <span className="text-sm font-bold text-text-primary">{cat.score.toFixed(1)}<span className="text-[11px] text-text-muted font-normal">/10</span></span>
            </div>

            <div className="w-full bg-surface-subtle border border-surface-border/60 rounded-full h-1.5 overflow-hidden">
              <div className={`h-full rounded-full ${cat.barColor}`} style={{ width: `${percentage}%` }} />
            </div>
          </div>
        );
      })}
    </div>
  );
};
