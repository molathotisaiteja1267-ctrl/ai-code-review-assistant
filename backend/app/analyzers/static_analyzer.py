import json
import subprocess
import tempfile
import os
import sys
from typing import List, Tuple
from app.analyzers.base import RawFinding, Severity, Category

class StaticAnalyzer:
    @staticmethod
    def analyze_python_ruff(source_code: str, filename: str = "snippet.py") -> List[RawFinding]:
        findings: List[RawFinding] = []
        
        # Create temp file to run ruff
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(source_code)
            temp_path = temp_file.name

        try:
            # Try running ruff via CLI
            result = subprocess.run(
                [sys.executable, "-m", "ruff", "check", "--output-format=json", temp_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout
            if output.strip():
                try:
                    ruff_issues = json.loads(output)
                    for item in ruff_issues:
                        code = item.get("code", "")
                        msg = item.get("message", "")
                        loc = item.get("location", {})
                        end_loc = item.get("end_location", {})
                        
                        severity = Severity.LOW
                        category = Category.CODE_QUALITY
                        
                        if code.startswith("F821"): # Undefined name
                            severity = Severity.HIGH
                            category = Category.BUG
                        elif code.startswith("F401"): # Unused import
                            severity = Severity.LOW
                            category = Category.CODE_QUALITY
                        elif code.startswith("E711") or code.startswith("E712"): # Comparison to None / True
                            severity = Severity.MEDIUM
                            category = Category.BUG
                        elif code.startswith("B"): # Bugbear
                            severity = Severity.HIGH
                            category = Category.BUG
                            
                        findings.append(RawFinding(
                            title=f"Static Analysis ({code}): {msg}",
                            category=category,
                            severity=severity,
                            confidence=0.95,
                            file_path=filename,
                            line_start=loc.get("row", 1),
                            line_end=end_loc.get("row", loc.get("row", 1)),
                            column_start=loc.get("column", 1),
                            column_end=end_loc.get("column", 1),
                            explanation=f"Ruff static rule {code} flagged: {msg}",
                            impact="May lead to runtime exceptions or violation of code standards.",
                            recommendation=f"Review rule {code} and adjust implementation.",
                            rule_id=f"RUFF-{code}",
                            source="Ruff",
                            evidence_sources=[f"Ruff Linter ({code})"]
                        ))
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

        return findings
