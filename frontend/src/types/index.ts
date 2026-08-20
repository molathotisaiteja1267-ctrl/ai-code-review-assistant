export type Severity = 'critical' | 'high' | 'medium' | 'low';
export type Category = 'security' | 'bug' | 'performance' | 'code_quality' | 'architecture' | 'complexity';

export interface ReviewIssue {
  id: number;
  review_id: number;
  title: string;
  category: Category;
  severity: Severity;
  confidence: number;
  file_path: string;
  line_start: number;
  line_end: number;
  column_start?: number;
  column_end?: number;
  explanation: string;
  impact?: string;
  recommendation?: string;
  suggested_fix?: string;
  rule_id?: string;
  evidence_sources: string[];
  is_resolved: boolean;
  created_at: string;
}

export interface ReviewFix {
  id: number;
  issue_id: number;
  review_id: number;
  original_snippet: string;
  patched_snippet: string;
  full_patched_code?: string;
  diff_content: string;
  what_changed: string;
  why_safer: string;
  validation_results: {
    syntax_valid: boolean;
    vulnerability_resolved: boolean;
    static_clean: boolean;
    regression_detected: boolean;
    details: string[];
    new_findings_count: number;
  };
  is_applied: boolean;
  created_at: string;
}

export interface ReviewMetrics {
  cyclomatic_complexity: number;
  maintainability_index: number;
  nesting_depth: number;
  sloc: number;
  functions_count: number;
  classes_count: number;
  functions_details?: Array<{
    name: string;
    line_start: number;
    line_end: number;
    cyclomatic_complexity: number;
    nesting_depth: number;
    sloc: number;
    risk: string;
  }>;
}

export interface Review {
  id: number;
  title: string;
  language: string;
  source_type: 'paste' | 'upload' | 'github_pr';
  file_path: string;
  source_code: string;
  git_diff?: string;
  overall_score: number;
  letter_grade: string;
  risk_level: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  security_score: number;
  reliability_score: number;
  performance_score: number;
  maintainability_score: number;
  summary?: string;
  metrics_json?: ReviewMetrics;
  status: string;
  execution_time_ms: number;
  created_at: string;
  issues_count?: number;
  critical_count?: number;
  high_count?: number;
  medium_count?: number;
  low_count?: number;
  issues?: ReviewIssue[];
  fixes?: ReviewFix[];
}

export interface GitHubRepo {
  id: number;
  name: string;
  full_name: string;
  owner: string;
  default_branch: string;
  is_private: boolean;
  description?: string;
}

export interface GitHubPR {
  id: number;
  number: number;
  title: string;
  description?: string;
  state: string;
  base_branch: string;
  head_branch: string;
  author: string;
  changed_files_count: number;
  additions: number;
  deletions: number;
  diff_content?: string;
}

export interface ProjectRule {
  id: number;
  name: string;
  rule_type: string;
  content: string;
  description?: string;
  is_active: boolean;
  created_at: string;
}

export interface EvaluationSampleResult {
  sample_id: string;
  title: string;
  category: string;
  expected_vulnerable: boolean;
  detected: boolean;
  correct: boolean;
  detected_issues: string[];
}

export interface EvaluationRun {
  id: number;
  run_mode: string;
  total_samples: number;
  true_positives: number;
  false_positives: number;
  false_negatives: number;
  true_negatives: number;
  precision: number;
  recall: number;
  f1_score: number;
  accuracy: number;
  avg_latency_ms: number;
  results_json?: EvaluationSampleResult[];
  created_at: string;
}

export interface DashboardStats {
  total_reviews: number;
  total_issues: number;
  critical_issues: number;
  high_issues: number;
  medium_issues: number;
  low_issues: number;
  security_issues: number;
  average_code_quality: number;
  average_risk_score: number;
  recent_reviews: Review[];
  severity_distribution: Record<string, number>;
  category_distribution: Record<string, number>;
  quality_trends: Array<{ date: string; score: number; issues: number }>;
}

export interface SettingsData {
  llm_provider: string;
  llm_model: string;
  has_llm_key: boolean;
  masked_llm_key: string;
  min_confidence: number;
  has_github_token: boolean;
  masked_github_token: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  is_superuser: boolean;
}
