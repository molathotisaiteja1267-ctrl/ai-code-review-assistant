from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Category(str, Enum):
    SECURITY = "security"
    BUG = "bug"
    PERFORMANCE = "performance"
    CODE_QUALITY = "code_quality"
    ARCHITECTURE = "architecture"
    COMPLEXITY = "complexity"

class RawFinding(BaseModel):
    title: str
    category: Category
    severity: Severity
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
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
    source: str = "analyzer"
    evidence_sources: List[str] = Field(default_factory=list)

class FunctionMetric(BaseModel):
    name: str
    line_start: int
    line_end: int
    cyclomatic_complexity: int
    nesting_depth: int
    sloc: int
    risk: str

class CodeMetrics(BaseModel):
    cyclomatic_complexity: int = 1
    maintainability_index: float = 100.0
    nesting_depth: int = 0
    sloc: int = 0
    functions_count: int = 0
    classes_count: int = 0
    functions_details: List[FunctionMetric] = Field(default_factory=list)
