from typing import List, Dict, Any, Tuple
from app.analyzers.base import RawFinding, Severity, Category, CodeMetrics

class RiskScorer:
    @staticmethod
    def calculate_scores(findings: List[RawFinding], metrics: CodeMetrics) -> Dict[str, Any]:
        """
        Calculates multi-dimensional risk scores (0.0 to 10.0), overall code quality (0 to 100),
        letter grade, and risk tier.
        """
        # Starting bases (10.0 is perfect)
        security_base = 10.0
        reliability_base = 10.0
        performance_base = 10.0
        maintainability_base = 10.0

        for f in findings:
            penalty = 0.0
            if f.severity == Severity.CRITICAL:
                penalty = 3.5 * f.confidence
            elif f.severity == Severity.HIGH:
                penalty = 2.0 * f.confidence
            elif f.severity == Severity.MEDIUM:
                penalty = 1.0 * f.confidence
            elif f.severity == Severity.LOW:
                penalty = 0.4 * f.confidence

            if f.category == Category.SECURITY:
                security_base -= penalty
            elif f.category in (Category.BUG, Category.ARCHITECTURE):
                reliability_base -= penalty
            elif f.category == Category.PERFORMANCE:
                performance_base -= penalty
            elif f.category in (Category.CODE_QUALITY, Category.COMPLEXITY):
                maintainability_base -= penalty

        # Complexity metrics influence maintainability
        if metrics.cyclomatic_complexity > 15:
            maintainability_base -= 1.5
        elif metrics.cyclomatic_complexity > 10:
            maintainability_base -= 0.8

        if metrics.nesting_depth > 4:
            maintainability_base -= 1.0

        # Clamp all scores between 0.0 and 10.0
        sec_score = max(0.0, min(10.0, round(security_base, 1)))
        rel_score = max(0.0, min(10.0, round(reliability_base, 1)))
        perf_score = max(0.0, min(10.0, round(performance_base, 1)))
        maint_score = max(0.0, min(10.0, round(maintainability_base, 1)))

        # Weighted overall score (0 to 100)
        # Security: 40%, Reliability: 30%, Performance: 15%, Maintainability: 15%
        overall = (sec_score * 4.0) + (rel_score * 3.0) + (perf_score * 1.5) + (maint_score * 1.5)
        overall_score = max(0.0, min(100.0, round(overall, 1)))

        # Assign Letter Grade
        if overall_score >= 93:
            grade = "A+"
        elif overall_score >= 85:
            grade = "A"
        elif overall_score >= 70:
            grade = "B"
        elif overall_score >= 55:
            grade = "C"
        elif overall_score >= 40:
            grade = "D"
        else:
            grade = "F"

        # Determine Risk Level
        has_critical = any(f.severity == Severity.CRITICAL for f in findings)
        high_count = sum(1 for f in findings if f.severity == Severity.HIGH)
        
        if has_critical or overall_score < 45:
            risk_level = "CRITICAL"
        elif high_count >= 2 or overall_score < 65:
            risk_level = "HIGH"
        elif len(findings) > 3 or overall_score < 85:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "overall_score": overall_score,
            "letter_grade": grade,
            "risk_level": risk_level,
            "security_score": sec_score,
            "reliability_score": rel_score,
            "performance_score": perf_score,
            "maintainability_score": maint_score
        }
