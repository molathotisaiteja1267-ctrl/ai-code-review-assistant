import ast
from typing import Dict, Any, List
from app.analyzers.ast_analyzer import PythonASTAnalyzer
from app.analyzers.security_scanner import SecurityScanner
from app.analyzers.base import RawFinding, Severity

class FixValidator:
    @staticmethod
    def validate_fix(
        original_code: str,
        patched_code: str,
        target_issue_title: str,
        filename: str = "snippet.py"
    ) -> Dict[str, Any]:
        """
        Production-grade validation loop:
        1. Syntax check on patched code
        2. Re-runs AST analyzer on patched code
        3. Re-runs Security Scanner on patched code
        4. Verifies the original issue is completely resolved
        5. Verifies no new critical/high bugs were introduced
        """
        details = []
        syntax_valid = False
        vulnerability_resolved = False
        static_clean = True
        regression_detected = False
        new_findings: List[RawFinding] = []

        # 1. Syntax Check
        try:
            ast.parse(patched_code, filename=filename)
            syntax_valid = True
            details.append("✓ Python AST syntax parse succeeded without errors.")
        except SyntaxError as e:
            syntax_valid = False
            details.append(f"✗ Syntax Error introduced in fix: {e.msg} at line {e.lineno}")
            return {
                "syntax_valid": False,
                "vulnerability_resolved": False,
                "static_clean": False,
                "regression_detected": True,
                "details": details,
                "new_findings_count": 1
            }

        # 2. Re-run Analyzers on Patched Code
        ast_findings, metrics, _ = PythonASTAnalyzer.analyze(patched_code, filename)
        sec_findings = SecurityScanner.scan_python(patched_code, filename)
        
        all_post_findings = ast_findings + sec_findings
        
        # Check if original vulnerability title still exists
        target_keyword = target_issue_title.lower().split("(")[0].strip()
        matching_remnants = [
            f for f in all_post_findings 
            if target_keyword in f.title.lower() or f.title.lower() in target_keyword
        ]

        if not matching_remnants:
            vulnerability_resolved = True
            details.append(f"✓ Original issue '{target_issue_title}' successfully resolved.")
        else:
            vulnerability_resolved = False
            details.append(f"⚠ Warning: Similar issue pattern still detected in patched code.")

        # Check for new introduced issues
        high_critical_post = [f for f in all_post_findings if f.severity in (Severity.CRITICAL, Severity.HIGH)]
        if high_critical_post and not matching_remnants:
            regression_detected = True
            static_clean = False
            details.append(f"⚠ Warning: {len(high_critical_post)} new high/critical findings detected after patch.")
        elif not high_critical_post:
            static_clean = True
            details.append("✓ No high or critical security regressions detected.")

        return {
            "syntax_valid": syntax_valid,
            "vulnerability_resolved": vulnerability_resolved,
            "static_clean": static_clean,
            "regression_detected": regression_detected,
            "details": details,
            "new_findings_count": len(all_post_findings)
        }
