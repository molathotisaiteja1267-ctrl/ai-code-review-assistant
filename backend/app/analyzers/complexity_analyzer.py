import re
from typing import List, Dict, Any, Tuple
from app.analyzers.base import RawFinding, Severity, Category, CodeMetrics, FunctionMetric

class ComplexityAnalyzer:
    @staticmethod
    def analyze_metrics(source_code: str, filename: str = "snippet.py") -> Tuple[List[RawFinding], CodeMetrics]:
        lines = source_code.splitlines()
        sloc = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
        
        findings: List[RawFinding] = []
        
        nested_for_pattern = r"^\s*for\s+.*\s+in\s+.*:"
        for_indices = []
        for idx, line in enumerate(lines, start=1):
            if re.search(nested_for_pattern, line):
                indent = len(line) - len(line.lstrip())
                for_indices.append((idx, indent, line))

        for i in range(len(for_indices) - 1):
            idx1, indent1, line1 = for_indices[i]
            idx2, indent2, line2 = for_indices[i+1]
            if idx2 - idx1 <= 12 and indent2 > indent1:
                findings.append(RawFinding(
                    title="Potential O(n²) Nested Iteration Bottleneck",
                    category=Category.PERFORMANCE,
                    severity=Severity.HIGH,
                    confidence=0.88,
                    file_path=filename,
                    line_start=idx1,
                    line_end=idx2,
                    explanation="Nested loops detected over collections without caching or hashing lookup, leading to quadratic O(n²) time complexity.",
                    impact="Significant degradation in response times and CPU saturation as dataset size grows.",
                    recommendation="Pre-index the inner collection into a dictionary/set for O(1) constant-time lookups.",
                    suggested_fix="# Index elements into a dict/set first:\nlookup_map = {item.key: item for item in collection_b}\nfor a in collection_a:\n    b = lookup_map.get(a.key)",
                    rule_id="PERF-QUADRATIC-LOOP",
                    source="Complexity Analyzer",
                    evidence_sources=["Performance Loop Depth Analyzer (O(n²) Nested Loop)"]
                ))

        metrics = CodeMetrics(
            cyclomatic_complexity=1,
            maintainability_index=100.0,
            nesting_depth=len(for_indices),
            sloc=sloc,
            functions_count=0,
            classes_count=0
        )

        return findings, metrics
