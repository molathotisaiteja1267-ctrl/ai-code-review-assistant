import json
from typing import Dict, Any
from app.models.entities import Review

class ReportExporter:
    @staticmethod
    def generate_markdown(review: Review) -> str:
        md = []
        md.append(f"# Code Review Report: {review.title}")
        md.append(f"**Date**: {review.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}  ")
        md.append(f"**Language**: {review.language} | **File**: `{review.file_path}`  ")
        md.append(f"**Execution Time**: {review.execution_time_ms:.1f}ms\n")
        
        md.append("## Executive Scorecard")
        md.append(f"- **Overall Code Quality**: **{review.overall_score}/100** (Grade: **{review.letter_grade}**)")
        md.append(f"- **Risk Level**: **{review.risk_level}**")
        md.append(f"- **Security Score**: {review.security_score}/10.0")
        md.append(f"- **Reliability Score**: {review.reliability_score}/10.0")
        md.append(f"- **Performance Score**: {review.performance_score}/10.0")
        md.append(f"- **Maintainability Score**: {review.maintainability_score}/10.0\n")

        md.append("## Summary")
        md.append(f"{review.summary}\n")

        md.append("## Detected Issues")
        if not review.issues:
            md.append("✓ No issues detected. Code adheres to quality and security standards.\n")
        else:
            for idx, issue in enumerate(review.issues, start=1):
                sev_emoji = "🔴" if issue.severity == "critical" else "🟠" if issue.severity == "high" else "🟡" if issue.severity == "medium" else "🟢"
                md.append(f"### {idx}. {sev_emoji} [{issue.severity.upper()}] {issue.title}")
                md.append(f"- **Category**: `{issue.category}` | **Confidence**: {int(issue.confidence*100)}% | **Lines**: {issue.line_start}-{issue.line_end}")
                md.append(f"- **Evidence**: {', '.join(issue.evidence_sources or [])}")
                md.append(f"\n**Explanation**: {issue.explanation}")
                if issue.impact:
                    md.append(f"\n**Security/Runtime Impact**: {issue.impact}")
                if issue.recommendation:
                    md.append(f"\n**Recommendation**: {issue.recommendation}")
                if issue.suggested_fix:
                    md.append(f"\n```python\n# Suggested Fix\n{issue.suggested_fix}\n```")
                md.append("\n---\n")

        return "\n".join(md)
