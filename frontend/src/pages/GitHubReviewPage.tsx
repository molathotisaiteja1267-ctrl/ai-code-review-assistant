import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { GitPullRequest, FolderGit2, Play, CheckCircle2, FileText, ArrowRight, User } from 'lucide-react';
import { githubService } from '../services/githubService';
import { GitHubRepo, GitHubPR } from '../types';
import { useToast } from '../context/ToastContext';

export const GitHubReviewPage: React.FC = () => {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [repos, setRepos] = useState<GitHubRepo[]>([]);
  const [selectedRepo, setSelectedRepo] = useState<string>('acme-corp/ecommerce-api');
  const [prs, setPrs] = useState<GitHubPR[]>([]);
  const [selectedPr, setSelectedPr] = useState<GitHubPR | null>(null);
  const [loading, setLoading] = useState(false);
  const [reviewing, setReviewing] = useState(false);

  useEffect(() => {
    fetchRepos();
  }, []);

  useEffect(() => {
    if (selectedRepo) {
      fetchPrs(selectedRepo);
    }
  }, [selectedRepo]);

  const fetchRepos = async () => {
    try {
      const data = await githubService.getRepositories();
      setRepos(data);
      if (data.length > 0) {
        setSelectedRepo(data[0].full_name);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchPrs = async (repoName: string) => {
    setLoading(true);
    try {
      const data = await githubService.getPullRequests(repoName);
      setPrs(data);
      if (data.length > 0) {
        setSelectedPr(data[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReviewPr = async () => {
    if (!selectedPr) return;
    setReviewing(true);
    try {
      const review = await githubService.reviewPullRequest(selectedRepo, selectedPr.number);
      showToast('success', 'PR Review Generated', `Found ${review.issues?.length || 0} line-level findings.`);
      navigate(`/reviews/${review.id}`);
    } catch (err) {
      showToast('error', 'PR review failed');
    } finally {
      setReviewing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-surface-border pb-3">
        <h1 className="text-2xl font-bold text-text-primary">GitHub Pull Request Reviews</h1>
        <p className="text-xs text-text-secondary mt-0.5">
          Select connected repository pull requests and execute line-level diff reviews.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left: Repos & PRs */}
        <div className="space-y-4">
          <div className="bg-white border border-surface-border rounded-xl p-4 space-y-3 shadow-subtle">
            <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">Repositories</span>
            <div className="space-y-1.5">
              {repos.map((repo) => (
                <button
                  key={repo.id}
                  onClick={() => setSelectedRepo(repo.full_name)}
                  className={`w-full p-3 rounded-lg text-left border transition-all ${
                    selectedRepo === repo.full_name
                      ? 'bg-brand-50 border-brand-400 text-brand-800 shadow-subtle'
                      : 'bg-white border-surface-border text-text-primary hover:bg-surface-hover'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <FolderGit2 className="w-4 h-4 text-brand-500 shrink-0" />
                    <span className="text-xs font-bold truncate">{repo.full_name}</span>
                  </div>
                  <p className="text-[11px] text-text-secondary mt-1 line-clamp-1">{repo.description}</p>
                </button>
              ))}
            </div>
          </div>

          <div className="bg-white border border-surface-border rounded-xl p-4 space-y-3 shadow-subtle">
            <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">Open Pull Requests</span>
            {loading ? (
              <div className="py-6 text-center text-xs text-text-muted">Loading pull requests...</div>
            ) : prs.length > 0 ? (
              <div className="space-y-1.5">
                {prs.map((pr) => (
                  <button
                    key={pr.id}
                    onClick={() => setSelectedPr(pr)}
                    className={`w-full p-3 rounded-lg text-left border transition-all ${
                      selectedPr?.id === pr.id
                        ? 'bg-brand-50 border-brand-400 text-brand-800 shadow-subtle'
                        : 'bg-white border-surface-border text-text-primary hover:bg-surface-hover'
                    }`}
                  >
                    <div className="flex items-center space-x-2">
                      <GitPullRequest className="w-3.5 h-3.5 text-brand-500 shrink-0" />
                      <span className="text-xs font-bold truncate">#{pr.number}: {pr.title}</span>
                    </div>
                    <div className="flex items-center space-x-3 text-[11px] text-text-secondary mt-1">
                      <span>@{pr.author}</span>
                      <span className="text-accent-green font-semibold">+{pr.additions}</span>
                      <span className="text-accent-red font-semibold">-{pr.deletions}</span>
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <div className="py-6 text-center text-xs text-text-muted">No open PRs in this repository.</div>
            )}
          </div>
        </div>

        {/* Right: Selected PR Details & Diff */}
        <div className="md:col-span-2 space-y-4">
          {selectedPr ? (
            <div className="bg-white border border-surface-border rounded-xl p-6 space-y-5 shadow-subtle">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-brand-50 text-brand-700 border border-brand-200 uppercase">
                      Open PR #{selectedPr.number}
                    </span>
                    <span className="text-xs text-text-secondary">
                      {selectedPr.head_branch} → {selectedPr.base_branch}
                    </span>
                  </div>
                  <h2 className="text-lg font-bold text-text-primary">{selectedPr.title}</h2>
                  <p className="text-xs text-text-secondary">{selectedPr.description}</p>
                </div>

                <button
                  onClick={handleReviewPr}
                  disabled={reviewing}
                  className="px-5 py-2.5 rounded-lg text-xs font-semibold bg-brand-500 hover:bg-brand-600 text-white flex items-center space-x-2 shadow-sm disabled:opacity-50 transition-all shrink-0"
                >
                  {reviewing ? (
                    <>
                      <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      <span>Analyzing Hunks...</span>
                    </>
                  ) : (
                    <>
                      <Play className="w-3.5 h-3.5 fill-white" />
                      <span>Review Pull Request</span>
                    </>
                  )}
                </button>
              </div>

              {/* Diff Preview */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs text-text-secondary">
                  <span className="font-bold text-text-primary">Changed Files Diff ({selectedPr.changed_files_count} files changed)</span>
                  <span className="font-mono">+{selectedPr.additions} / -{selectedPr.deletions}</span>
                </div>

                <pre className="p-4 bg-surface-subtle border border-surface-border rounded-xl text-xs font-mono overflow-x-auto text-text-primary max-h-96 leading-relaxed">
                  {selectedPr.diff_content}
                </pre>
              </div>
            </div>
          ) : (
            <div className="p-12 text-center text-text-muted bg-white border border-surface-border rounded-xl">
              Select a Pull Request to preview unified diffs and execute code review.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
