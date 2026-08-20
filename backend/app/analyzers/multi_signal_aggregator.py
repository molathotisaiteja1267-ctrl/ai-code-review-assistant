from typing import List, Dict, Any
from app.analyzers.base import RawFinding, Severity, Category

class MultiSignalAggregator:
    @staticmethod
    def aggregate_and_deduplicate(findings: List[RawFinding], min_confidence: float = 0.60) -> List[RawFinding]:
        """
        Merges multiple overlapping findings (Bandit + AST + Static + LLM) into unified,
        high-confidence findings with combined evidence tags.
        """
        # Filter low confidence first
        valid_findings = [f for f in findings if f.confidence >= min_confidence]
        
        merged: List[RawFinding] = []
        
        # Group by (file_path, line_start approx, category/intent)
        for candidate in valid_findings:
            matched = False
            for existing in merged:
                # Same file and line overlap within +/- 3 lines
                line_overlap = abs(existing.line_start - candidate.line_start) <= 3
                same_file = existing.file_path == candidate.file_path
                same_or_related_cat = (
                    existing.category == candidate.category or 
                    (existing.category == Category.SECURITY and candidate.category == Category.SECURITY) or
                    (existing.category == Category.BUG and candidate.category == Category.BUG)
                )
                
                # Check semantic keyword overlap in titles
                title_keywords_a = set(existing.title.lower().replace("-", " ").replace("_", " ").split())
                title_keywords_b = set(candidate.title.lower().replace("-", " ").replace("_", " ").split())
                common_keywords = title_keywords_a.intersection(title_keywords_b)
                
                if same_file and line_overlap and (same_or_related_cat or len(common_keywords) >= 2):
                    # Merge candidate into existing
                    matched = True
                    # Upgrade severity if candidate is higher
                    sev_rank = {Severity.LOW: 1, Severity.MEDIUM: 2, Severity.HIGH: 3, Severity.CRITICAL: 4}
                    if sev_rank.get(candidate.severity, 1) > sev_rank.get(existing.severity, 1):
                        existing.severity = candidate.severity
                        existing.title = candidate.title
                        existing.explanation = candidate.explanation
                    
                    # Boost confidence because multiple independent signals confirmed it!
                    existing.confidence = min(0.99, round(existing.confidence + 0.05, 2))
                    
                    # Combine evidence sources
                    for ev in candidate.evidence_sources:
                        if ev not in existing.evidence_sources:
                            existing.evidence_sources.append(ev)
                    if candidate.source not in existing.source:
                        existing.source = f"{existing.source} + {candidate.source}"
                        
                    # Keep richer suggestion if available
                    if not existing.suggested_fix and candidate.suggested_fix:
                        existing.suggested_fix = candidate.suggested_fix
                    break
                    
            if not matched:
                if not candidate.evidence_sources:
                    candidate.evidence_sources = [f"{candidate.source} Analyzer"]
                merged.append(candidate)
                
        # Sort by Severity desc, then line_start asc
        sev_order = {Severity.CRITICAL: 0, Severity.HIGH: 1, Severity.MEDIUM: 2, Severity.LOW: 3}
        merged.sort(key=lambda x: (sev_order.get(x.severity, 4), x.line_start))
        
        return merged
