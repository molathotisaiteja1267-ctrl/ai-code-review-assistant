import React, { useState, useEffect } from 'react';
import { X, CheckCircle2, AlertTriangle, ShieldCheck, Wrench, Sparkles, Copy, Check } from 'lucide-react';
import { ReviewIssue, ReviewFix } from '../../types';
import { MonacoDiffViewer } from '../editor/MonacoDiffViewer';
import { reviewService } from '../../services/reviewService';
import { useToast } from '../../context/ToastContext';

interface FixModalProps {
  issue: ReviewIssue;
  sourceCode: string;
  onClose: () => void;
  onFixApplied: (updatedCode: string) => void;
}

export const FixModal: React.FC<FixModalProps> = ({
  issue,
  sourceCode,
  onClose,
  onFixApplied
}) => {
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [fix, setFix] = useState<ReviewFix | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetchFix();
  }, [issue]);

  const fetchFix = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await reviewService.generateFix(issue.id);
      setFix(res);
    } catch (err: any) {
      setError('Failed to generate fix patch. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async () => {
    if (!fix) return;
    try {
      const res = await reviewService.applyFix(fix.id);
      onFixApplied(res.updated_source_code);
      showToast('success', 'Fix applied successfully', 'The patch has been written to the active buffer.');
      onClose();
    } catch (err) {
      setError('Failed to apply fix.');
      showToast('error', 'Failed to apply fix');
    }
  };

  const handleCopy = () => {
    if (!fix) return;
    navigator.clipboard.writeText(fix.patched_snippet);
    setCopied(true);
    showToast('info', 'Copied to clipboard');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/40 backdrop-blur-xs">
      <div className="bg-white border border-surface-border rounded-2xl w-full max-w-5xl max-h-[90vh] flex flex-col shadow-elevated overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b border-surface-border flex items-center justify-between bg-surface-subtle">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-brand-500 text-white flex items-center justify-center shadow-sm">
              <Wrench className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-text-primary">AI Fix & Automated Safety Validation</h3>
              <p className="text-xs text-text-secondary">Target: {issue.title} (Line {issue.line_start})</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-surface-border text-text-secondary hover:text-text-primary transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          {loading ? (
            <div className="py-16 text-center space-y-3">
              <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
              <p className="text-sm font-semibold text-text-primary">Generating fix patch & re-running safety validation loop...</p>
              <p className="text-xs text-text-secondary">Executing AST syntax parser, Bandit security checks, and regression tests.</p>
            </div>
          ) : error ? (
            <div className="p-4 bg-accent-redLight border border-red-200 rounded-xl text-accent-red text-xs">
              {error}
            </div>
          ) : fix ? (
            <>
              {/* Validation Checklist Banner */}
              <div className="p-4 rounded-xl bg-surface-subtle border border-surface-border space-y-3">
                <div className="flex items-center space-x-2 text-xs font-bold text-text-primary uppercase tracking-wider">
                  <ShieldCheck className="w-4 h-4 text-accent-green" />
                  <span>Automated Safety Validation Results</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className={`p-3 rounded-lg border flex items-center space-x-2 text-xs font-medium ${fix.validation_results.syntax_valid ? 'bg-accent-greenLight border-green-200 text-green-900' : 'bg-accent-redLight border-red-200 text-red-900'}`}>
                    <CheckCircle2 className="w-4 h-4 text-accent-green shrink-0" />
                    <span>AST Syntax Valid</span>
                  </div>

                  <div className={`p-3 rounded-lg border flex items-center space-x-2 text-xs font-medium ${fix.validation_results.vulnerability_resolved ? 'bg-accent-greenLight border-green-200 text-green-900' : 'bg-accent-yellowLight border-amber-200 text-amber-900'}`}>
                    <CheckCircle2 className="w-4 h-4 text-accent-green shrink-0" />
                    <span>Vulnerability Resolved</span>
                  </div>

                  <div className={`p-3 rounded-lg border flex items-center space-x-2 text-xs font-medium ${!fix.validation_results.regression_detected ? 'bg-accent-greenLight border-green-200 text-green-900' : 'bg-accent-redLight border-red-200 text-red-900'}`}>
                    <CheckCircle2 className="w-4 h-4 text-accent-green shrink-0" />
                    <span>Zero Regressions</span>
                  </div>
                </div>

                {fix.validation_results.details && (
                  <ul className="text-xs text-text-secondary space-y-1 pl-1">
                    {fix.validation_results.details.map((d, i) => (
                      <li key={i}>• {d}</li>
                    ))}
                  </ul>
                )}
              </div>

              {/* Explanations */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-white border border-surface-border space-y-1.5">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-text-secondary">What Changed?</h4>
                  <p className="text-xs text-text-primary leading-relaxed">{fix.what_changed}</p>
                </div>

                <div className="p-4 rounded-xl bg-brand-50/60 border border-brand-200 space-y-1.5">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-brand-700">Why is this safer?</h4>
                  <p className="text-xs text-brand-900 leading-relaxed">{fix.why_safer}</p>
                </div>
              </div>

              {/* Diff Viewer */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs text-text-secondary">
                  <span className="font-semibold text-text-primary">Side-by-Side Patch Diff</span>
                  <span>Original vs Patched</span>
                </div>
                <MonacoDiffViewer
                  original={sourceCode}
                  modified={fix.full_patched_code || sourceCode}
                  language="python"
                />
              </div>
            </>
          ) : null}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-surface-border bg-surface-subtle flex items-center justify-between">
          <button
            onClick={handleCopy}
            disabled={!fix}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold text-text-secondary bg-white border border-surface-border hover:bg-surface-hover flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-accent-green" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy Snippet'}</span>
          </button>

          <div className="flex items-center space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg text-xs font-medium text-text-secondary hover:bg-surface-border transition-colors"
            >
              Cancel
            </button>

            {fix && (
              <button
                onClick={handleApply}
                className="px-4 py-2 rounded-lg text-xs font-semibold bg-accent-green hover:bg-green-700 text-white flex items-center space-x-1.5 shadow-sm transition-all"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>Apply Fix to Buffer</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
