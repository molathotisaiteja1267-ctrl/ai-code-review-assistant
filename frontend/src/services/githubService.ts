import { apiClient } from './api';
import { GitHubRepo, GitHubPR, Review } from '../types';

export const githubService = {
  async getRepositories(): Promise<GitHubRepo[]> {
    const res = await apiClient.get<GitHubRepo[]>('/github/repositories');
    return res.data;
  },

  async getPullRequests(repoFullName: string): Promise<GitHubPR[]> {
    const res = await apiClient.get<GitHubPR[]>(`/github/repositories/${encodeURIComponent(repoFullName)}/pulls`);
    return res.data;
  },

  async reviewPullRequest(repoFullName: string, prNumber: number): Promise<Review> {
    const res = await apiClient.post<Review>('/github/reviews/pr', {
      repo_full_name: repoFullName,
      pr_number: prNumber
    });
    return res.data;
  }
};
