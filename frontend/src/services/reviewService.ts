import { apiClient } from './api';
import { Review, ReviewFix, DashboardStats, ProjectRule, EvaluationRun } from '../types';

export const reviewService = {
  async createReview(payload: {
    title?: string;
    language: string;
    source_type?: string;
    file_path?: string;
    source_code: string;
    git_diff?: string;
    min_confidence?: number;
    apply_rag_rules?: boolean;
    scopes?: string[];
  }): Promise<Review> {
    const res = await apiClient.post<Review>('/reviews', payload);
    return res.data;
  },

  async createMultiFileReview(payload: {
    title: string;
    files: Array<{ file_path: string; content: string }>;
    min_confidence?: number;
  }): Promise<Review[]> {
    const res = await apiClient.post<Review[]>('/reviews/multi-file', payload);
    return res.data;
  },

  async listReviews(skip = 0, limit = 50): Promise<Review[]> {
    const res = await apiClient.get<Review[]>('/reviews', { params: { skip, limit } });
    return res.data;
  },

  async getReview(id: number): Promise<Review> {
    const res = await apiClient.get<Review>(`/reviews/${id}`);
    return res.data;
  },

  async deleteReview(id: number): Promise<void> {
    await apiClient.delete(`/reviews/${id}`);
  },

  async exportMarkdownUrl(id: number): Promise<string> {
    return `${apiClient.defaults.baseURL}/reviews/${id}/export/markdown`;
  },

  async generateFix(issueId: number): Promise<ReviewFix> {
    const res = await apiClient.post<ReviewFix>('/fixes/generate', { issue_id: issueId });
    return res.data;
  },

  async applyFix(fixId: number): Promise<{ status: string; updated_source_code: string }> {
    const res = await apiClient.post(`/fixes/${fixId}/apply`);
    return res.data;
  },

  async getDashboardStats(days = '30'): Promise<DashboardStats> {
    const res = await apiClient.get<DashboardStats>('/dashboard/stats', { params: { days } });
    return res.data;
  },

  async getRules(): Promise<ProjectRule[]> {
    const res = await apiClient.get<ProjectRule[]>('/rag/rules');
    return res.data;
  },

  async createRule(payload: { name: string; rule_type: string; content: string; description?: string }): Promise<ProjectRule> {
    const res = await apiClient.post<ProjectRule>('/rag/rules', payload);
    return res.data;
  },

  async searchRules(query: string): Promise<{ query: string; matches: string[] }> {
    const res = await apiClient.post('/rag/search', null, { params: { query } });
    return res.data;
  },

  async runEvaluation(mode = 'hybrid'): Promise<EvaluationRun> {
    const res = await apiClient.post<EvaluationRun>('/evaluation/run', { mode });
    return res.data;
  },

  async getEvaluationHistory(): Promise<EvaluationRun[]> {
    const res = await apiClient.get<EvaluationRun[]>('/evaluation/history');
    return res.data;
  }
};
