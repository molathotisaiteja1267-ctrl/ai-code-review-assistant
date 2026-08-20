import pytest
from app.analyzers.multi_signal_aggregator import MultiSignalAggregator
from app.analyzers.base import RawFinding, Severity, Category

def test_multi_signal_deduplication():
    # Simulate Bandit finding and AST finding on the same line
    finding1 = RawFinding(
        title="SQL Injection Vulnerability",
        category=Category.SECURITY,
        severity=Severity.CRITICAL,
        confidence=0.85,
        line_start=15,
        line_end=15,
        explanation="Dynamic SQL formatting",
        source="AST",
        evidence_sources=["AST Parser"]
    )
    finding2 = RawFinding(
        title="Security Finding (B608): Hardcoded Sql Expressions",
        category=Category.SECURITY,
        severity=Severity.HIGH,
        confidence=0.80,
        line_start=15,
        line_end=15,
        explanation="Possible SQL Injection in execute",
        source="Bandit",
        evidence_sources=["Bandit B608"]
    )
    
    merged = MultiSignalAggregator.aggregate_and_deduplicate([finding1, finding2])
    assert len(merged) == 1
    assert merged[0].severity == Severity.CRITICAL
    assert merged[0].confidence > 0.85 # Boosted confidence
    assert len(merged[0].evidence_sources) == 2
