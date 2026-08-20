import pytest
from app.analyzers.ast_analyzer import PythonASTAnalyzer
from app.analyzers.base import Severity, Category

def test_ast_sql_injection_detection():
    code = """
def fetch_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
"""
    findings, metrics, symbols = PythonASTAnalyzer.analyze(code, "test.py")
    assert any("SQL Injection" in f.title for f in findings)
    assert any(f.severity == Severity.CRITICAL for f in findings)

def test_ast_command_injection_detection():
    code = """
import subprocess
def run_command(user_arg):
    subprocess.run(f"echo {user_arg}", shell=True)
"""
    findings, metrics, symbols = PythonASTAnalyzer.analyze(code, "test.py")
    assert any("Command Injection" in f.title for f in findings)

def test_ast_mutable_default_arg():
    code = """
def append_item(x, items=[]):
    items.append(x)
    return items
"""
    findings, metrics, symbols = PythonASTAnalyzer.analyze(code, "test.py")
    assert any("Mutable Default Argument" in f.title for f in findings)

def test_ast_bare_except():
    code = """
def do_something():
    try:
        1 / 0
    except:
        pass
"""
    findings, metrics, symbols = PythonASTAnalyzer.analyze(code, "test.py")
    assert any("Bare 'except:'" in f.title for f in findings)
