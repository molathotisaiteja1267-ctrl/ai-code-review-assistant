import json
import subprocess
import tempfile
import os
import re
import sys
from typing import List
from app.analyzers.base import RawFinding, Severity, Category

class SecurityScanner:
    @staticmethod
    def scan_python(source_code: str, filename: str = "snippet.py") -> List[RawFinding]:
        findings: List[RawFinding] = []
        
        # 1. Pattern-based High Entropy / Secrets Regex Scanner
        findings.extend(SecurityScanner._scan_regex_patterns(source_code, filename))
        
        # 2. Bandit Execution
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(source_code)
            temp_path = temp_file.name

        try:
            result = subprocess.run(
                [sys.executable, "-m", "bandit", "-f", "json", "-q", temp_path],
                capture_output=True,
                text=True,
                timeout=12
            )
            output = result.stdout
            if output.strip():
                try:
                    bandit_data = json.loads(output)
                    results = bandit_data.get("results", [])
                    for item in results:
                        test_id = item.get("test_id", "")
                        test_name = item.get("test_name", "")
                        issue_text = item.get("issue_text", "")
                        line_number = item.get("line_number", 1)
                        line_range = item.get("line_range", [line_number])
                        issue_severity = item.get("issue_severity", "MEDIUM").lower()
                        issue_confidence = item.get("issue_confidence", "MEDIUM").lower()
                        
                        sev = Severity.MEDIUM
                        if issue_severity == "high":
                            sev = Severity.HIGH
                        elif issue_severity == "low":
                            sev = Severity.LOW

                        if test_id in ("B608", "B602", "B102", "B301", "B303", "B506", "B105", "B106", "B107"):
                            sev = Severity.CRITICAL if issue_severity == "high" else Severity.HIGH

                        conf = 0.85
                        if issue_confidence == "high":
                            conf = 0.95
                        elif issue_confidence == "low":
                            conf = 0.70

                        findings.append(RawFinding(
                            title=f"Security Finding ({test_id}): {test_name.replace('_', ' ').title()}",
                            category=Category.SECURITY,
                            severity=sev,
                            confidence=conf,
                            file_path=filename,
                            line_start=line_number,
                            line_end=max(line_range) if line_range else line_number,
                            explanation=f"Bandit security scanner detected: {issue_text}",
                            impact="Security vulnerability that could be exploited in production environments.",
                            recommendation=f"Follow OWASP and Bandit guidelines for {test_id}.",
                            rule_id=f"BANDIT-{test_id}",
                            source="Bandit",
                            evidence_sources=[f"Bandit Scanner ({test_id}: {test_name})"]
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

    @staticmethod
    def _scan_regex_patterns(source_code: str, filename: str) -> List[RawFinding]:
        findings: List[RawFinding] = []
        lines = source_code.splitlines()
        
        patterns = [
            (
                r"(?i)(?:aws_access_key_id|aws_secret_access_key|AKIA[0-9A-Z]{16})",
                "Exposed AWS Access Key",
                Severity.CRITICAL,
                "AWS access credentials found in source code.",
                "Unrestricted access to cloud infrastructure and data."
            ),
            (
                r"ghp_[0-9a-zA-Z]{20,}|github_pat_[0-9a-zA-Z_]{20,}",
                "Exposed GitHub Personal Access Token",
                Severity.CRITICAL,
                "Personal access token detected in plaintext.",
                "Attackers can read, modify, or delete private repositories and assets."
            ),
            (
                r"eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*",
                "Hardcoded JWT Token",
                Severity.HIGH,
                "JSON Web Token embedded in source code.",
                "Tokens may expose authorization rights or sensitive claims."
            ),
            (
                r"(?i)-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
                "Hardcoded Private Cryptographic Key",
                Severity.CRITICAL,
                "Private cryptographic key material embedded in plaintext.",
                "Allows decryption of confidential communications or authentication bypass."
            ),
            (
                r"(?i)SELECT\s+.*\s+FROM\s+.*WHERE\s+.*=\s*['\"]\s*\+",
                "SQL Concatenation Pattern",
                Severity.CRITICAL,
                "Raw SQL query concatenated with variable.",
                "Direct SQL Injection vulnerability."
            )
        ]

        for line_idx, line in enumerate(lines, start=1):
            trimmed = line.strip()
            if trimmed.startswith("#") or trimmed.startswith("//"):
                continue
                
            for pattern, title, severity, explanation, impact in patterns:
                if re.search(pattern, line):
                    findings.append(RawFinding(
                        title=title,
                        category=Category.SECURITY,
                        severity=severity,
                        confidence=0.93,
                        file_path=filename,
                        line_start=line_idx,
                        line_end=line_idx,
                        explanation=explanation,
                        impact=impact,
                        recommendation="Store sensitive secrets in environment variables or KMS vaults.",
                        rule_id="REGEX-SEC-01",
                        source="Security Scanner",
                        evidence_sources=["Pattern Security Scanner (High Entropy/Secret Signature)"]
                    ))
                    break

        return findings
