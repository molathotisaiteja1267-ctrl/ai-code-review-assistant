from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.session import Base

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    repositories = relationship("Repository", back_populates="owner", cascade="all, delete-orphan")

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    full_name = Column(String(255), unique=True, index=True, nullable=False)
    default_branch = Column(String(100), default="main")
    is_private = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    owner = relationship("User", back_populates="repositories")
    pull_requests = relationship("PullRequest", back_populates="repository", cascade="all, delete-orphan")
    rules = relationship("ProjectRule", back_populates="repository", cascade="all, delete-orphan")

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False, index=True)
    number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    state = Column(String(50), default="open")
    base_branch = Column(String(100), default="main")
    head_branch = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    changed_files_count = Column(Integer, default=0)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    diff_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    repository = relationship("Repository", back_populates="pull_requests")
    reviews = relationship("Review", back_populates="pull_request")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=True, index=True)
    pull_request_id = Column(Integer, ForeignKey("pull_requests.id"), nullable=True, index=True)

    title = Column(String(255), nullable=False)
    language = Column(String(50), default="python")
    source_type = Column(String(50), default="paste")
    file_path = Column(String(255), default="snippet.py")
    source_code = Column(Text, nullable=False)
    git_diff = Column(Text, nullable=True)

    overall_score = Column(Float, default=100.0)
    letter_grade = Column(String(10), default="A+")
    risk_level = Column(String(20), default="LOW")
    security_score = Column(Float, default=10.0)
    reliability_score = Column(Float, default=10.0)
    performance_score = Column(Float, default=10.0)
    maintainability_score = Column(Float, default=10.0)

    summary = Column(Text, nullable=True)
    metrics_json = Column(JSON, nullable=True)
    status = Column(String(50), default="completed")
    execution_time_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=get_utc_now, index=True)

    user = relationship("User", back_populates="reviews")
    pull_request = relationship("PullRequest", back_populates="reviews")
    issues = relationship("ReviewIssue", back_populates="review", cascade="all, delete-orphan")
    fixes = relationship("ReviewFix", back_populates="review", cascade="all, delete-orphan")

class ReviewIssue(Base):
    __tablename__ = "review_issues"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    severity = Column(String(20), nullable=False, index=True)
    confidence = Column(Float, default=0.90)

    file_path = Column(String(255), default="snippet.py")
    line_start = Column(Integer, default=1)
    line_end = Column(Integer, default=1)
    column_start = Column(Integer, nullable=True)
    column_end = Column(Integer, nullable=True)

    explanation = Column(Text, nullable=False)
    impact = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    suggested_fix = Column(Text, nullable=True)
    rule_id = Column(String(100), nullable=True)
    evidence_sources = Column(JSON, default=list)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)

    review = relationship("Review", back_populates="issues")
    fixes = relationship("ReviewFix", back_populates="issue", cascade="all, delete-orphan")

class ReviewFix(Base):
    __tablename__ = "review_fixes"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("review_issues.id"), nullable=False, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, index=True)

    original_snippet = Column(Text, nullable=False)
    patched_snippet = Column(Text, nullable=False)
    full_patched_code = Column(Text, nullable=True)
    diff_content = Column(Text, nullable=False)
    what_changed = Column(Text, nullable=False)
    why_safer = Column(Text, nullable=False)

    validation_results = Column(JSON, default=dict)
    is_applied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)

    issue = relationship("ReviewIssue", back_populates="fixes")
    review = relationship("Review", back_populates="fixes")

class ProjectRule(Base):
    __tablename__ = "project_rules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    rule_type = Column(String(50), default="guideline")
    content = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_utc_now)

    repository = relationship("Repository", back_populates="rules")

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    run_mode = Column(String(50), default="hybrid")
    total_samples = Column(Integer, default=0)
    true_positives = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    false_negatives = Column(Integer, default=0)
    true_negatives = Column(Integer, default=0)
    precision = Column(Float, default=0.0)
    recall = Column(Float, default=0.0)
    f1_score = Column(Float, default=0.0)
    accuracy = Column(Float, default=0.0)
    avg_latency_ms = Column(Float, default=0.0)
    results_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
