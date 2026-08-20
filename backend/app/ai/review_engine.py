import json
import re
from typing import List, Dict, Any, Optional
from app.analyzers.base import RawFinding, Severity, Category, CodeMetrics
from app.ai.llm_provider import get_llm_provider
from app.core.config import settings

class AIReviewEngine:
    @staticmethod
    async def analyze_with_llm(
        source_code: str,
        filename: str,
        static_findings: List[RawFinding],
        metrics: CodeMetrics,
        symbols: Dict[str, Any],
        rag_rules: List[str] = [],
        git_diff: Optional[str] = None
    ) -> List[RawFinding]:
        provider = get_llm_provider()
        
        system_instruction = (
            "You are a Senior Principal Software Architect and Security Auditor. "
            "Analyze the given source code and context. "
            "Identify real, impactful bugs, security risks, performance bottlenecks, architecture violations, "
            "and code quality problems. DO NOT output trivial style nits. "
            "Output strictly valid JSON matching the requested schema."
        )

        detected_titles = [f.title for f in static_findings]
        functions_list = symbols.get("functions", [])
        classes_list = symbols.get("classes", [])
        rag_text = "\n".join(rag_rules) if rag_rules else "Standard PEP8 and Secure Coding Practices."
        diff_text = f"\nGIT DIFF CONTEXT:\n{git_diff}" if git_diff else ""

        prompt = f"""
SOURCE CODE ({filename}):
```
{source_code}
```

STATIC ANALYSIS & SECURITY FINDINGS ALREADY DETECTED:
{detected_titles}

AST METRICS & SYMBOLS:
- Functions: {functions_list}
- Classes: {classes_list}
- Cyclomatic Complexity: {metrics.cyclomatic_complexity}
- Max Nesting Depth: {metrics.nesting_depth}

PROJECT-SPECIFIC CODING STANDARDS & RAG RULES:
{rag_text}
{diff_text}

INSTRUCTIONS:
1. Examine if there are high-level bugs, security vulnerabilities (SQLi, SSRF, RCE, IDOR, auth bypass), logic flaws, race conditions, or architecture rule violations.
2. Provide line-level explanation, real-world impact, concrete recommendation, and suggested fix snippet.
3. Assign confidence between 0.60 and 0.99.

Output valid JSON with the following structure:
{{
  "summary": "Brief executive summary of code quality and risks",
  "issues": [
    {{
      "title": "Clear concise title",
      "category": "security | bug | performance | code_quality | architecture | complexity",
      "severity": "critical | high | medium | low",
      "confidence": 0.92,
      "line_start": 10,
      "line_end": 12,
      "explanation": "Deep explanation of what is wrong",
      "impact": "Concrete consequence if deployed to production",
      "recommendation": "Actionable developer guidance",
      "suggested_fix": "replacement code snippet"
    }}
  ]
}}
"""
        findings: List[RawFinding] = []

        try:
            response_json = await provider.generate_json(prompt, system_instruction)
            raw_issues = response_json.get("issues", [])
            for item in raw_issues:
                try:
                    sev_str = item.get("severity", "medium").lower()
                    cat_str = item.get("category", "code_quality").lower()
                    
                    sev = Severity.MEDIUM
                    if sev_str == "critical":
                        sev = Severity.CRITICAL
                    elif sev_str == "high":
                        sev = Severity.HIGH
                    elif sev_str == "low":
                        sev = Severity.LOW

                    cat = Category.CODE_QUALITY
                    if cat_str == "security":
                        cat = Category.SECURITY
                    elif cat_str == "bug":
                        cat = Category.BUG
                    elif cat_str == "performance":
                        cat = Category.PERFORMANCE
                    elif cat_str == "architecture":
                        cat = Category.ARCHITECTURE
                    elif cat_str == "complexity":
                        cat = Category.COMPLEXITY

                    findings.append(RawFinding(
                        title=item.get("title", "AI Finding"),
                        category=cat,
                        severity=sev,
                        confidence=float(item.get("confidence", 0.85)),
                        file_path=filename,
                        line_start=int(item.get("line_start", 1)),
                        line_end=int(item.get("line_end", item.get("line_start", 1))),
                        explanation=item.get("explanation", ""),
                        impact=item.get("impact", ""),
                        recommendation=item.get("recommendation", ""),
                        suggested_fix=item.get("suggested_fix", ""),
                        rule_id="LLM-REASONING-01",
                        source="LLM Engine",
                        evidence_sources=["LLM Contextual Reasoning Engine"]
                    ))
                except Exception:
                    continue
        except Exception:
            pass

        return findings
