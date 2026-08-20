from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

# --- Auth Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

# --- Issue Schemas ---
class IssueBase(BaseModel):
    title: str
    category: str
    severity: str
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)
    file_path: str = "snippet.py"
    line_start: int = 1
    line_end: int = 1
    column_start: Optional[int] = None
    column_end: Optional[int] = None
    explanation: str
    impact: Optional[str] = None
    recommendation: Optional[str] = None
    suggested_fix: Optional[str] = None
    rule_id: Optional[str] = None
    evidence_sources: List[str] = Field(default_factory=list)

class IssueResponse(IssueBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    review_id: int
    is_resolved: bool
    created_at: datetime

# --- Fix Schemas ---
class FixRequest(BaseModel):
    issue_id: int

class FixValidationResult(BaseModel):
    syntax_valid: bool
    vulnerability_resolved: bool
    static_clean: bool
    regression_detected: bool
    details: List[str] = Field(default_factory=list)
    new_findings_count: int = 0

class FixResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    issue_id: int
    review_id: int
    original_snippet: str
    patched_snippet: str
    full_patched_code: Optional[str] = None
    diff_content: str
    what_changed: str
    why_safer: str
    validation_results: Dict[str, Any]
    is_applied: bool
    created_at: datetime

# --- Review Schemas ---
class ReviewCreate(BaseModel):
    title: Optional[str] = "Code Review"
    language: str = "python"
    source_type: str = "paste"
    file_path: Optional[str] = "snippet.py"
    source_code: str
    git_diff: Optional[str] = None
    repository_id: Optional[int] = None
    pull_request_id: Optional[int] = None
    min_confidence: Optional[float] = 0.60
    apply_rag_rules: bool = True
    scopes: Optional[List[str]] = Field(default=["security", "reliability", "performance", "maintainability"])

class FilePayload(BaseModel):
    file_path: str
    content: str

class MultiFileReviewCreate(BaseModel):
    title: Optional[str] = "Multi-file Review"
    files: List[FilePayload]
    repository_id: Optional[int] = None
    min_confidence: Optional[float] = 0.60

class ReviewMetrics(BaseModel):
    cyclomatic_complexity: int = 1
    maintainability_index: float = 100.0
    nesting_depth: int = 0
    sloc: int = 0
    functions_count: int = 0
    classes_count: int = 0

class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    language: str
    source_type: str
    file_path: str
    overall_score: float
    letter_grade: str
    risk_level: str
    security_score: float
    reliability_score: float
    performance_score: float
    maintainability_score: float
    summary: Optional[str] = None
    metrics_json: Optional[Dict[str, Any]] = None
    status: str
    execution_time_ms: float
    created_at: datetime
    issues_count: Optional[int] = 0
    critical_count: Optional[int] = 0
    high_count: Optional[int] = 0
    medium_count: Optional[int] = 0
    low_count: Optional[int] = 0

class ReviewDetailResponse(ReviewResponse):
    source_code: str
    git_diff: Optional[str] = None
    issues: List[IssueResponse] = Field(default_factory=list)
    fixes: List[FixResponse] = Field(default_factory=list)

# --- GitHub Integration Schemas ---
class GitHubRepoResponse(BaseModel):
    id: int
    name: str
    full_name: str
    owner: str
    default_branch: str
    is_private: bool
    description: Optional[str] = None

class GitHubPRResponse(BaseModel):
    id: int
    number: int
    title: str
    description: Optional[str] = None
    state: str
    base_branch: str
    head_branch: str
    author: str
    changed_files_count: int
    additions: int
    deletions: int
    diff_content: Optional[str] = None

class GitHubPRReviewRequest(BaseModel):
    repo_full_name: str
    pr_number: int

# --- RAG / Project Rule Schemas ---
class ProjectRuleCreate(BaseModel):
    name: str
    rule_type: str = "guideline"
    content: str
    description: Optional[str] = None
    repository_id: Optional[int] = None

class ProjectRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    rule_type: str
    content: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime

# --- Evaluation / Benchmark Schemas ---
class EvaluationRequest(BaseModel):
    mode: str = "hybrid"

class EvaluationRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    run_mode: str
    total_samples: int
    true_positives: int
    false_positives: int
    false_negatives: int
    true_negatives: int
    precision: float
    recall: float
    f1_score: float
    accuracy: float
    avg_latency_ms: float
    results_json: Optional[Any] = None
    created_at: datetime

# --- Dashboard Schemas ---
class DashboardStatsResponse(BaseModel):
    total_reviews: int
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    security_issues: int
    average_code_quality: float
    average_risk_score: float
    recent_reviews: List[ReviewResponse] = Field(default_factory=list)
    severity_distribution: Dict[str, int] = Field(default_factory=dict)
    category_distribution: Dict[str, int] = Field(default_factory=dict)
    quality_trends: List[Dict[str, Any]] = Field(default_factory=list)

# --- Settings Schemas ---
class SettingsUpdate(BaseModel):
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    llm_api_key: Optional[str] = None
    min_confidence: Optional[float] = None
    github_token: Optional[str] = None

class SettingsResponse(BaseModel):
    llm_provider: str
    llm_model: str
    has_llm_key: bool
    masked_llm_key: str
    min_confidence: float
    has_github_token: bool
    masked_github_token: str
