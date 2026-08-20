import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Download, 
  Trash2, 
  ArrowLeft, 
  Code2,
  CheckCircle2,
  FileText
} from 'lucide-react';
import { reviewService } from '../services/reviewService';
import { Review, ReviewIssue } from '../types';
import { Scorecard } from '../components/review/Scorecard';
import { CategoryRiskGrid } from '../components/review/CategoryRiskGrid';
import { IssueFilterBar } from '../components/review/IssueFilterBar';
import { IssueCard } from '../components/review/IssueCard';
import { FixModal } from '../components/review/FixModal';
import { MonacoCodeEditor } from '../components/editor/MonacoCodeEditor';
import { useToast } from '../context/ToastContext';

export const ReviewDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [review, setReview] = useState<Review | null>(null);
  const [selectedIssue, setSelectedIssue] = useState<ReviewIssue | null>(null);
  const [activeFixIssue, setActiveFixIssue] = useState<ReviewIssue | null>(null);
  const [loading, setLoading] = useState(true);

  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [minConfidence, setMinConfidence] = useState(0.60);

  useEffect(() => {
    if (id) {
      fetchReview(parseInt(id));
    }
  }, [id]);

  const fetchReview = async (reviewId: number) => {
    try {
      const data = await reviewService.getReview(reviewId);
      setReview(data);
      if (data.issues && data.issues.length > 0) {
        setSelectedIssue(data.issues[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!review) return;
    if (window.confirm('Are you sure you want to delete this review?')) {
      await reviewService.deleteReview(review.id);
      showToast('info', 'Review deleted');
      navigate('/history');
    }
  };

  const handleExportMarkdown = async () => {
    if (!review) return;
    const url = await reviewService.exportMarkdownUrl(review.id);
    window.open(url, '_blank');
    showToast('success', 'Exporting Report', 'Markdown report opened in new tab.');
  };

  const handleFixApplied = (updatedCode: string) => {
    if (review) {
      setReview({ ...review, source_code: updatedCode });
    }
  };

  if (loading) {
    return (
      <div className="py-24 text-center space-y-3">
        <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs font-semibold text-text-secondary">Loading review results...</p>
      </div>
    );
  }

  if (!review) {
    return (
      <div className="p-8 text-center space-y-3 bg-white border border-surface-border rounded-xl">
        <p className="text-sm text-text-secondary">Review record not found.</p>
        <button onClick={() => navigate('/history')} className="text-xs font-semibold text-brand-600 underline">
          Back to Review History
        </button>
      </div>
    );
  }

  const filteredIssues = (review.issues || []).filter((issue) => {
    if (selectedSeverity !== 'all' && issue.severity !== selectedSeverity) return false;
    if (selectedCategory !== 'all' && issue.category !== selectedCategory) return false;
    if (issue.confidence < minConfidence) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const match = issue.title.toLowerCase().includes(q) ||
                    issue.explanation.toLowerCase().includes(q) ||
                    (issue.rule_id && issue.rule_id.toLowerCase().includes(q));
      if (!match) return false;
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Top Bar Navigation */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/history')}
          className="flex items-center space-x-2 text-xs font-semibold text-text-secondary hover:text-text-primary transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to History</span>
        </button>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleExportMarkdown}
            className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-white border border-surface-border hover:bg-surface-hover text-text-primary flex items-center space-x-2 transition-all shadow-subtle"
          >
            <Download className="w-3.5 h-3.5 text-brand-500" />
            <span>Export Markdown Report</span>
          </button>

          <button
            onClick={handleDelete}
            className="p-2 rounded-lg text-text-muted hover:text-accent-red hover:bg-accent-redLight transition-colors"
            title="Delete Review"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Scorecard */}
      <Scorecard review={review} />

      {/* Category Risk Grid */}
      <CategoryRiskGrid review={review} />

      {/* Main Review Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left 7 Columns: Monaco Code Editor */}
        <div className="lg:col-span-7 bg-white border border-surface-border rounded-xl p-4 space-y-3 shadow-subtle">
          <div className="flex items-center justify-between text-xs text-text-secondary">
            <div className="flex items-center space-x-2 font-mono font-bold text-text-primary">
              <Code2 className="w-4 h-4 text-brand-500" />
              <span>{review.file_path}</span>
            </div>
            <span className="text-[11px] text-text-muted font-mono">
              {review.metrics_json?.sloc || 0} SLOC • CC={review.metrics_json?.cyclomatic_complexity || 1}
            </span>
          </div>

          <div className="h-[580px] w-full">
            <MonacoCodeEditor
              code={review.source_code}
              language={review.language}
              issues={filteredIssues}
              selectedIssue={selectedIssue}
              onSelectIssue={setSelectedIssue}
              readOnly={false}
            />
          </div>
        </div>

        {/* Right 5 Columns: Issue List & Filters */}
        <div className="lg:col-span-5 space-y-3">
          <IssueFilterBar
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
            selectedSeverity={selectedSeverity}
            onSeverityChange={setSelectedSeverity}
            selectedCategory={selectedCategory}
            onCategoryChange={setSelectedCategory}
            minConfidence={minConfidence}
            onConfidenceChange={setMinConfidence}
            totalCount={filteredIssues.length}
          />

          <div className="space-y-2.5 max-h-[520px] overflow-y-auto pr-1">
            {filteredIssues.length > 0 ? (
              filteredIssues.map((issue) => (
                <IssueCard
                  key={issue.id}
                  issue={issue}
                  isSelected={selectedIssue?.id === issue.id}
                  onSelect={() => setSelectedIssue(issue)}
                  onGenerateFix={(iss) => setActiveFixIssue(iss)}
                />
              ))
            ) : (
              <div className="p-8 text-center bg-white border border-surface-border rounded-xl text-text-muted text-xs">
                No issues match your active filters.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Fix Generation & Validation Modal */}
      {activeFixIssue && (
        <FixModal
          issue={activeFixIssue}
          sourceCode={review.source_code}
          onClose={() => setActiveFixIssue(null)}
          onFixApplied={handleFixApplied}
        />
      )}
    </div>
  );
};
