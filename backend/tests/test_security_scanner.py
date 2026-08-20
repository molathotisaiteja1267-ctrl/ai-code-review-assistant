import pytest
from app.analyzers.security_scanner import SecurityScanner
from app.analyzers.base import Severity

def test_regex_secrets_scanner():
    code = """
AWS_SECRET = "AKIA1234567890ABCDEF"
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuv"
"""
    findings = SecurityScanner.scan_python(code, "test.py")
    assert len(findings) >= 2
    assert any("AWS" in f.title for f in findings)
    assert any("GitHub" in f.title for f in findings)
