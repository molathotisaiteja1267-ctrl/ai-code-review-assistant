import ast
import re
from typing import List, Dict, Any, Tuple
from app.analyzers.base import RawFinding, Severity, Category, CodeMetrics, FunctionMetric

class ASTVisitor(ast.NodeVisitor):
    def __init__(self, filename: str = "snippet.py"):
        self.filename = filename
        self.findings: List[RawFinding] = []
        self.functions: List[Dict[str, Any]] = []
        self.classes: List[str] = []
        self.imports: List[str] = []
        self.calls: List[str] = []
        self.max_nesting_depth = 0
        self.current_nesting_depth = 0
        # Taint tracking: maps variable name to 'unsafe_sql', 'unsafe_cmd', 'unsafe_path', etc.
        self.tainted_vars: Dict[str, str] = {}

    def generic_visit(self, node):
        is_nesting_node = isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        if is_nesting_node:
            self.current_nesting_depth += 1
            if self.current_nesting_depth > self.max_nesting_depth:
                self.max_nesting_depth = self.current_nesting_depth
        
        super().generic_visit(node)
        
        if is_nesting_node:
            self.current_nesting_depth -= 1

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(alias.name)
            if alias.name in ("telnetlib", "ftplib"):
                self.findings.append(RawFinding(
                    title=f"Insecure Protocol Import ({alias.name})",
                    category=Category.SECURITY,
                    severity=Severity.HIGH,
                    confidence=0.92,
                    file_path=self.filename,
                    line_start=node.lineno,
                    line_end=getattr(node, "end_lineno", node.lineno),
                    explanation=f"Import of '{alias.name}' transmits data unencrypted over the network.",
                    impact="Potential eavesdropping and credential interception in transit.",
                    recommendation="Use secure alternatives like Paramiko, SSH, or HTTPS/SFTP.",
                    rule_id="AST-SEC-001",
                    source="AST",
                    evidence_sources=["AST Parser (Insecure Protocol Import)"]
                ))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        self.imports.append(module)
        if module == "pickle":
            self.findings.append(RawFinding(
                title="Insecure Deserialization Module (pickle)",
                category=Category.SECURITY,
                severity=Severity.HIGH,
                confidence=0.88,
                file_path=self.filename,
                line_start=node.lineno,
                line_end=getattr(node, "end_lineno", node.lineno),
                explanation="Pickle deserialization is inherently unsafe against untrusted data.",
                impact="Remote Code Execution (RCE) if deserializing untrusted payloads.",
                recommendation="Use safe serialization formats like JSON, Protobuf, or cryptography-signed tokens.",
                rule_id="AST-SEC-002",
                source="AST",
                evidence_sources=["AST Parser (Pickle Import)"]
            ))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._analyze_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._analyze_function(node)
        self.generic_visit(node)

    def _analyze_function(self, node: Any):
        cc = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With, ast.Assert)):
                cc += 1
            elif isinstance(child, ast.BoolOp):
                cc += len(child.values) - 1

        end_line = getattr(node, "end_lineno", node.lineno)
        sloc = end_line - node.lineno + 1
        
        risk = "LOW"
        if cc >= 15 or sloc > 80:
            risk = "CRITICAL"
        elif cc >= 10 or sloc > 50:
            risk = "HIGH"
        elif cc >= 6 or sloc > 30:
            risk = "MEDIUM"

        self.functions.append({
            "name": node.name,
            "line_start": node.lineno,
            "line_end": end_line,
            "cyclomatic_complexity": cc,
            "sloc": sloc,
            "risk": risk
        })

        if cc >= 12:
            self.findings.append(RawFinding(
                title=f"High Cyclomatic Complexity in '{node.name}' (CC={cc})",
                category=Category.COMPLEXITY,
                severity=Severity.HIGH if cc >= 15 else Severity.MEDIUM,
                confidence=0.95,
                file_path=self.filename,
                line_start=node.lineno,
                line_end=end_line,
                explanation=f"Function '{node.name}' has cyclomatic complexity of {cc}, exceeding recommended threshold (10).",
                impact="Difficult to test, understand, and maintain; prone to regression bugs.",
                recommendation="Decompose this function into smaller, single-responsibility helper functions.",
                rule_id="AST-COMP-001",
                source="AST",
                evidence_sources=[f"AST Complexity Analyzer (CC={cc})"]
            ))

        for default in node.args.defaults + node.args.kw_defaults:
            if default is not None and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.findings.append(RawFinding(
                    title=f"Mutable Default Argument in '{node.name}'",
                    category=Category.BUG,
                    severity=Severity.MEDIUM,
                    confidence=0.96,
                    file_path=self.filename,
                    line_start=node.lineno,
                    line_end=node.lineno,
                    explanation=f"Function '{node.name}' uses a mutable default argument ({type(default).__name__}). Default arguments are evaluated once when function is defined.",
                    impact="State is shared across subsequent calls leading to unintended state accumulation.",
                    recommendation="Use None as default and initialize collection inside function body.",
                    suggested_fix=f"def {node.name}(..., arg=None):\n    if arg is None:\n        arg = []",
                    rule_id="AST-BUG-001",
                    source="AST",
                    evidence_sources=["AST Pattern Matcher (Mutable Default Arg)"]
                ))

    def visit_Assign(self, node: ast.Assign):
        # Check if variable is being assigned an unsafe SQL string (f-string or concat)
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                # Check value
                val = node.value
                is_dyn_sql = False
                if isinstance(val, ast.JoinedStr):
                    # Check if text contains SQL keywords
                    text_parts = "".join([part.value for part in val.values if isinstance(part, ast.Constant) and isinstance(part.value, str)])
                    if any(k in text_parts.upper() for k in ("SELECT", "INSERT", "UPDATE", "DELETE", "WHERE", "FROM")):
                        is_dyn_sql = True
                elif isinstance(val, ast.BinOp) and isinstance(val.op, (ast.Mod, ast.Add)):
                    is_dyn_sql = True

                if is_dyn_sql:
                    self.tainted_vars[var_name] = "unsafe_sql"
        
        self._check_hardcoded_secrets(node)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        func_name = self._get_call_name(node.func)
        if func_name:
            self.calls.append(func_name)
            self._check_dangerous_calls(node, func_name)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None:
            self.findings.append(RawFinding(
                title="Bare 'except:' Clause Detected",
                category=Category.CODE_QUALITY,
                severity=Severity.HIGH,
                confidence=0.95,
                file_path=self.filename,
                line_start=node.lineno,
                line_end=getattr(node, "end_lineno", node.lineno),
                explanation="A bare except catches all exceptions including SystemExit and KeyboardInterrupt.",
                impact="Masks unexpected crashes, halts clean termination, and hinders debugging.",
                recommendation="Catch specific exceptions or except Exception with logging.",
                rule_id="AST-QUAL-001",
                source="AST",
                evidence_sources=["AST Parser (Bare Except)"]
            ))
        elif len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.findings.append(RawFinding(
                title="Silently Swallowed Exception (Pass in Except)",
                category=Category.BUG,
                severity=Severity.MEDIUM,
                confidence=0.92,
                file_path=self.filename,
                line_start=node.lineno,
                line_end=getattr(node, "end_lineno", node.lineno),
                explanation="Exception is caught and silently ignored with pass without logging or recovery.",
                impact="Errors fail silently, corrupting downstream program state.",
                recommendation="Log the exception with traceback or raise a domain exception.",
                rule_id="AST-BUG-002",
                source="AST",
                evidence_sources=["AST Parser (Empty Exception Handler)"]
            ))
        self.generic_visit(node)

    def _get_call_name(self, node: Any) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            val = self._get_call_name(node.value)
            return f"{val}.{node.attr}" if val else node.attr
        return ""

    def _check_dangerous_calls(self, node: ast.Call, func_name: str):
        # 1. SQL Injection check
        if any(func_name.endswith(x) for x in (".execute", ".executemany", ".raw")):
            if node.args:
                first_arg = node.args[0]
                is_unsafe = False
                if isinstance(first_arg, ast.JoinedStr):
                    is_unsafe = True
                elif isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, (ast.Mod, ast.Add)):
                    is_unsafe = True
                elif isinstance(first_arg, ast.Call) and self._get_call_name(first_arg.func).endswith(".format"):
                    is_unsafe = True
                elif isinstance(first_arg, ast.Name) and self.tainted_vars.get(first_arg.id) == "unsafe_sql":
                    is_unsafe = True

                if is_unsafe:
                    self.findings.append(RawFinding(
                        title="SQL Injection Vulnerability (Dynamic String Formatting in Query)",
                        category=Category.SECURITY,
                        severity=Severity.CRITICAL,
                        confidence=0.97,
                        file_path=self.filename,
                        line_start=node.lineno,
                        line_end=getattr(node, "end_lineno", node.lineno),
                        explanation="SQL query executes unsanitized dynamic string constructed via formatting or concatenation.",
                        impact="Attackers can inject arbitrary SQL payloads to bypass authentication, dump database contents, or modify data.",
                        recommendation="Use parameterized queries with placeholder parameters (e.g. cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,)))",
                        suggested_fix="cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
                        rule_id="AST-SEC-SQLI",
                        source="AST",
                        evidence_sources=["AST Taint Tracker (Unsafe Dynamic SQL Execution)"]
                    ))

        # 2. Command Injection
        if func_name in ("os.system", "os.popen", "subprocess.Popen", "subprocess.call", "subprocess.run"):
            has_shell_true = False
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    has_shell_true = True
            
            if func_name in ("os.system", "os.popen") or has_shell_true:
                self.findings.append(RawFinding(
                    title="Command Injection Risk (Unsafe Shell Execution)",
                    category=Category.SECURITY,
                    severity=Severity.CRITICAL,
                    confidence=0.95,
                    file_path=self.filename,
                    line_start=node.lineno,
                    line_end=getattr(node, "end_lineno", node.lineno),
                    explanation=f"Execution of system shell command via '{func_name}' with shell=True or direct system call.",
                    impact="Arbitrary remote command execution on the underlying host operating system.",
                    recommendation="Avoid shell=True. Pass command and arguments as a validated list to subprocess.run(..., shell=False).",
                    suggested_fix="subprocess.run(['command', arg1, arg2], check=True, capture_output=True)",
                    rule_id="AST-SEC-CMD",
                    source="AST",
                    evidence_sources=[f"AST Call Analyzer ({func_name} Shell Execution)"]
                ))

        # 3. eval/exec
        if func_name in ("eval", "exec"):
            self.findings.append(RawFinding(
                title=f"Dangerous Dynamic Code Execution ({func_name})",
                category=Category.SECURITY,
                severity=Severity.CRITICAL,
                confidence=0.98,
                file_path=self.filename,
                line_start=node.lineno,
                line_end=getattr(node, "end_lineno", node.lineno),
                explanation=f"Direct invocation of '{func_name}' compiles and executes arbitrary Python code.",
                impact="Full server compromise and arbitrary code execution.",
                recommendation="Use ast.literal_eval for parsing literals, or structured dictionaries for dispatching.",
                rule_id="AST-SEC-EVAL",
                source="AST",
                evidence_sources=[f"AST Call Analyzer (Direct {func_name})"]
            ))

        # 4. Insecure Hashing
        if func_name in ("hashlib.md5", "hashlib.sha1"):
            self.findings.append(RawFinding(
                title=f"Weak Cryptographic Hash Function ({func_name})",
                category=Category.SECURITY,
                severity=Severity.MEDIUM,
                confidence=0.90,
                file_path=self.filename,
                line_start=node.lineno,
                line_end=getattr(node, "end_lineno", node.lineno),
                explanation=f"Use of broken cryptographic hash function '{func_name}'.",
                impact="Vulnerable to collision attacks and precomputed hash matching.",
                recommendation="Use modern secure hashes like hashlib.sha256() or bcrypt for passwords.",
                rule_id="AST-SEC-HASH",
                source="AST",
                evidence_sources=[f"AST Call Analyzer (Weak Hash {func_name})"]
            ))

        # 5. Insecure YAML
        if func_name == "yaml.load":
            has_safe_loader = False
            for kw in node.keywords:
                if kw.arg == "Loader" and "SafeLoader" in self._get_call_name(kw.value):
                    has_safe_loader = True
            if not has_safe_loader:
                self.findings.append(RawFinding(
                    title="Insecure YAML Deserialization (yaml.load without SafeLoader)",
                    category=Category.SECURITY,
                    severity=Severity.HIGH,
                    confidence=0.95,
                    file_path=self.filename,
                    line_start=node.lineno,
                    line_end=getattr(node, "end_lineno", node.lineno),
                    explanation="Calling yaml.load() without SafeLoader allows arbitrary Python object instantiation.",
                    impact="Remote Code Execution (RCE) via untrusted YAML documents.",
                    recommendation="Use yaml.safe_load(payload) or Loader=yaml.SafeLoader.",
                    suggested_fix="yaml.safe_load(data)",
                    rule_id="AST-SEC-YAML",
                    source="AST",
                    evidence_sources=["AST Call Analyzer (yaml.load)"]
                ))

    def _check_hardcoded_secrets(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                secret_patterns = ["password", "secret_key", "api_key", "auth_token", "private_key", "access_token", "aws_secret"]
                if any(p in var_name for p in secret_patterns):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        val = node.value.value
                        if len(val) >= 8 and not val.startswith(("os.getenv", "env", "${", "TODO", "CHANGEME", "xxx")):
                            self.findings.append(RawFinding(
                                title=f"Hardcoded Credential in Variable '{target.id}'",
                                category=Category.SECURITY,
                                severity=Severity.CRITICAL if "key" in var_name or "secret" in var_name else Severity.HIGH,
                                confidence=0.91,
                                file_path=self.filename,
                                line_start=node.lineno,
                                line_end=getattr(node, "end_lineno", node.lineno),
                                explanation=f"Variable '{target.id}' contains a hardcoded plaintext secret.",
                                impact="Credentials committed to version control risk unauthorized data exposure.",
                                recommendation="Retrieve secrets from environment variables or a secret vault.",
                                suggested_fix=f"{target.id} = os.getenv('{target.id.upper()}')",
                                rule_id="AST-SEC-SECRET",
                                source="AST",
                                evidence_sources=[f"AST Assignment Analyzer (Hardcoded Secret '{target.id}')"]
                            ))

class PythonASTAnalyzer:
    @staticmethod
    def analyze(source_code: str, filename: str = "snippet.py") -> Tuple[List[RawFinding], CodeMetrics, Dict[str, Any]]:
        try:
            tree = ast.parse(source_code, filename=filename)
        except SyntaxError as e:
            syntax_finding = RawFinding(
                title=f"Python Syntax Error: {e.msg}",
                category=Category.BUG,
                severity=Severity.CRITICAL,
                confidence=1.0,
                file_path=filename,
                line_start=e.lineno or 1,
                line_end=e.lineno or 1,
                column_start=e.offset or 1,
                explanation=f"Code failed to parse due to a syntax error: {e.msg}",
                impact="Code cannot execute and will crash immediately.",
                recommendation="Fix the Python syntax error at the indicated line and column.",
                rule_id="AST-SYNTAX-ERR",
                source="AST",
                evidence_sources=["AST Parser (SyntaxError)"]
            )
            return [syntax_finding], CodeMetrics(sloc=len(source_code.splitlines())), {"parsed": False, "error": str(e)}

        visitor = ASTVisitor(filename=filename)
        visitor.visit(tree)

        sloc = len(source_code.splitlines())
        total_cc = sum(f["cyclomatic_complexity"] for f in visitor.functions) if visitor.functions else 1
        
        mi = max(10.0, min(100.0, 100.0 - (total_cc * 1.5) - (visitor.max_nesting_depth * 4.0) - (sloc * 0.1)))

        func_metrics = [
            FunctionMetric(
                name=f["name"],
                line_start=f["line_start"],
                line_end=f["line_end"],
                cyclomatic_complexity=f["cyclomatic_complexity"],
                nesting_depth=visitor.max_nesting_depth,
                sloc=f["sloc"],
                risk=f["risk"]
            ) for f in visitor.functions
        ]

        metrics = CodeMetrics(
            cyclomatic_complexity=total_cc,
            maintainability_index=round(mi, 2),
            nesting_depth=visitor.max_nesting_depth,
            sloc=sloc,
            functions_count=len(visitor.functions),
            classes_count=len(visitor.classes),
            functions_details=func_metrics
        )

        symbols = {
            "parsed": True,
            "imports": list(set(visitor.imports)),
            "classes": visitor.classes,
            "functions": [f["name"] for f in visitor.functions],
            "calls": list(set(visitor.calls)),
            "max_nesting_depth": visitor.max_nesting_depth
        }

        return visitor.findings, metrics, symbols
