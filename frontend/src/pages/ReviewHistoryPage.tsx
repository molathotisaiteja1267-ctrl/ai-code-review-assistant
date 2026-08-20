import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Trash2, ArrowUpRight, CheckCircle2 } from 'lucide-react';
import { reviewService } from '../services/reviewService';
import { Review } from '../types';
import { useToast } from '../context/ToastContext';

export const ReviewHistoryPage: React.FC = () => {
  const { showToast } = useToast();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRisk, setSelectedRisk] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const data = await reviewService.listReviews();
      setReviews(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (window.confirm('Delete this review record?')) {
      await reviewService.deleteReview(id);
      setReviews(reviews.filter((r) => r.id !== id));
      showToast('info', 'Review deleted');
    }
  };

  const filtered = reviews.filter((r) => {
    if (selectedRisk !== 'all' && r.risk_level !== selectedRisk) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const match = r.title.toLowerCase().includes(q) ||
                    r.file_path.toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-2 border-b border-surface-border">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Review History</h1>
          <p className="text-xs text-text-secondary mt-0.5">Archive of automated code reviews, audit trails, and quality metrics.</p>
        </div>

        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 text-text-muted absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search reviews..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 bg-white border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 shadow-subtle"
            />
          </div>

          <select
            value={selectedRisk}
            onChange={(e) => setSelectedRisk(e.target.value)}
            className="px-3 py-1.5 bg-white border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 shadow-subtle"
          >
            <option value="all">All Risk Levels</option>
            <option value="CRITICAL">Critical Only</option>
            <option value="HIGH">High Only</option>
            <option value="MEDIUM">Medium Only</option>
            <option value="LOW">Low Only</option>
          </select>
        </div>
      </div>

      <div className="bg-white border border-surface-border rounded-xl overflow-hidden shadow-subtle">
        <table className="w-full text-left text-xs text-text-primary">
          <thead className="bg-surface-subtle text-text-secondary uppercase font-semibold text-[10px] tracking-wider border-b border-surface-border">
            <tr>
              <th className="px-5 py-3.5">Review ID</th>
              <th className="px-5 py-3.5">Title / File</th>
              <th className="px-5 py-3.5">Type</th>
              <th className="px-5 py-3.5">Quality Score</th>
              <th className="px-5 py-3.5">Risk Tier</th>
              <th className="px-5 py-3.5">Issues</th>
              <th className="px-5 py-3.5">Date</th>
              <th className="px-5 py-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-border">
            {filtered.length > 0 ? (
              filtered.map((r) => (
                <tr key={r.id} className="hover:bg-surface-hover transition-colors">
                  <td className="px-5 py-4 font-mono text-[11px] text-text-muted">#{r.id}</td>
                  <td className="px-5 py-4 font-semibold text-text-primary">
                    <Link to={`/reviews/${r.id}`} className="hover:text-brand-600 transition-colors">
                      {r.title}
                    </Link>
                  </td>
                  <td className="px-5 py-4 uppercase text-[10px] text-text-secondary font-mono">{r.source_type}</td>
                  <td className="px-5 py-4">
                    <span className="font-bold text-text-primary bg-surface-subtle px-2.5 py-0.5 rounded border border-surface-border">
                      {r.letter_grade} ({r.overall_score.toFixed(0)})
                    </span>
                  </td>
                  <td className="px-5 py-4">
                    <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                      r.risk_level === 'CRITICAL' ? 'bg-accent-redLight text-accent-red border border-red-200' :
                      r.risk_level === 'HIGH' ? 'bg-orange-50 text-brand-600 border border-brand-200' :
                      r.risk_level === 'MEDIUM' ? 'bg-accent-yellowLight text-amber-800 border border-amber-200' :
                      'bg-accent-greenLight text-accent-green border border-green-200'
                    }`}>
                      {r.risk_level}
                    </span>
                  </td>
                  <td className="px-5 py-4 text-text-secondary">{r.issues_count} findings</td>
                  <td className="px-5 py-4 text-text-muted">{new Date(r.created_at).toLocaleDateString()}</td>
                  <td className="px-5 py-4 text-right space-x-2">
                    <Link
                      to={`/reviews/${r.id}`}
                      className="text-xs font-semibold text-brand-600 hover:text-brand-700 bg-brand-50 px-2.5 py-1 rounded-md"
                    >
                      Inspect →
                    </Link>
                    <button
                      onClick={(e) => handleDelete(r.id, e)}
                      className="p-1 text-text-muted hover:text-accent-red transition-colors"
                      title="Delete"
                    >
                      <Trash2 className="w-3.5 h-3.5 inline" />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={8} className="px-5 py-10 text-center text-text-muted">
                  No matching review records found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
