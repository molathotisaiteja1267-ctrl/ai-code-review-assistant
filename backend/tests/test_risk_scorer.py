import pytest
from app.analyzers.risk_scorer import RiskScorer
from app.analyzers.base import RawFinding, Severity, Category, CodeMetrics

def test_risk_scorer_clean_code():
    findings = []
    metrics = CodeMetrics(cyclomatic_complexity=1, sloc=10, maintainability_index=100.0)
    scores = RiskScorer.calculate_scores(findings, metrics)
    assert scores["overall_score"] == 100.0
    assert scores["letter_grade"] == "A+"
    assert scores["risk_level"] == "LOW"

def test_risk_scorer_critical_vulnerability():
    findings = [
        RawFinding(
            title="SQL Injection",
            category=Category.SECURITY,
            severity=Severity.CRITICAL,
            confidence=0.95,
            explanation="Unsafe SQL execution"
        )
    ]
    metrics = CodeMetrics(cyclomatic_complexity=3, sloc=20, maintainability_index=85.0)
    scores = RiskScorer.calculate_scores(findings, metrics)
    assert scores["risk_level"] == "CRITICAL"
    assert scores["security_score"] < 10.0
