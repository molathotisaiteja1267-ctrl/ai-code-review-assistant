import pytest
from app.ai.fix_validator import FixValidator
from app.ai.fix_generator import FixGenerator
from app.analyzers.base import RawFinding, Category, Severity

def test_fix_validation_loop():
    vulnerable_code = """
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
"""
    issue = RawFinding(
        title="SQL Injection Vulnerability",
        category=Category.SECURITY,
        severity=Severity.CRITICAL,
        confidence=0.95,
        line_start=3,
        line_end=4,
        explanation="Direct SQL interpolation",
        suggested_fix="    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
    )

    fix_data = FixGenerator.generate_fix(vulnerable_code, issue)
    assert fix_data["full_patched_code"] is not None
    assert "diff_content" in fix_data

    validation = FixValidator.validate_fix(
        original_code=vulnerable_code,
        patched_code=fix_data["full_patched_code"],
        target_issue_title=issue.title,
        filename="test.py"
    )

    assert validation["syntax_valid"] is True
    assert validation["vulnerability_resolved"] is True
    assert validation["regression_detected"] is False
