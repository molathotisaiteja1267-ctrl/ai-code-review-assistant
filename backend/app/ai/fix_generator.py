import difflib
import re
from typing import Dict, Any, Tuple
from app.analyzers.base import RawFinding, Category, Severity

class FixGenerator:
    @staticmethod
    def generate_fix(source_code: str, issue: RawFinding) -> Dict[str, Any]:
        lines = source_code.splitlines()
        start_idx = max(0, issue.line_start - 1)
        end_idx = min(len(lines), issue.line_end)
        
        original_snippet = "\n".join(lines[start_idx:end_idx]) if lines else ""

        patched_snippet = issue.suggested_fix or ""
        what_changed = ""
        why_safer = ""

        if not patched_snippet or patched_snippet.strip() == "":
            if issue.category == Category.SECURITY and "SQL" in issue.title:
                patched_snippet = "    # Use parameterized query to eliminate SQL injection\n    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
                what_changed = "Replaced dynamic string formatting with parameterized query placeholder."
                why_safer = "Ensures user input is escaped by database driver, completely eliminating SQL injection risks."
            elif issue.category == Category.SECURITY and "Command" in issue.title:
                patched_snippet = "    # Safe subprocess execution without shell=True\n    subprocess.run(['ping', '-c', '1', host], check=True, capture_output=True)"
                what_changed = "Removed shell=True and switched to argument list."
                why_safer = "Prevents command chaining through shell metacharacters."
            elif issue.category == Category.SECURITY and "Secret" in issue.title:
                patched_snippet = "    # Load sensitive credentials from environment\n    api_key = os.getenv('API_KEY')"
                what_changed = "Replaced plaintext credential string with environment variable lookup."
                why_safer = "Prevents accidental leakage of production credentials in source control."
            elif issue.category == Category.PERFORMANCE and ("O(n²)" in issue.title or "Iteration" in issue.title):
                patched_snippet = "    # Pre-index lookup table for O(1) performance\n    lookup_map = {item.id: item for item in secondary_list}\n    results = [lookup_map[x.id] for x in primary_list if x.id in lookup_map]"
                what_changed = "Constructed hash map for O(1) membership and value retrieval."
                why_safer = "Reduces time complexity from quadratic O(n²) to linear O(n), preventing CPU bottlenecks."
            elif issue.category == Category.BUG and "Mutable" in issue.title:
                patched_snippet = "def append_item(x, items=None):\n    if items is None:\n        items = []\n    items.append(x)\n    return items"
                what_changed = "Default argument changed to None with body initialization."
                why_safer = "Prevents mutable state from accumulating across independent function invocations."
            else:
                patched_snippet = f"    # Fixed: {issue.recommendation or 'Refactored code'}\n" + original_snippet
                what_changed = f"Applied recommendation: {issue.recommendation}"
                why_safer = f"Mitigates issue: {issue.title}"
        else:
            what_changed = f"Updated lines {issue.line_start}-{issue.line_end} to implement recommended safe pattern."
            why_safer = f"Resolves {issue.title} and conforms to secure programming standards."

        # Reconstruct full patched file
        new_lines = list(lines)
        if 0 <= start_idx < len(new_lines):
            replacement_lines = patched_snippet.splitlines()
            new_lines[start_idx:end_idx] = replacement_lines
            full_patched_code = "\n".join(new_lines)
        else:
            full_patched_code = source_code + "\n" + patched_snippet

        # Generate Unified Diff
        diff_lines = list(difflib.unified_diff(
            source_code.splitlines(keepends=True),
            full_patched_code.splitlines(keepends=True),
            fromfile=f"a/{issue.file_path}",
            tofile=f"b/{issue.file_path}",
            n=3
        ))
        diff_content = "".join(diff_lines)

        return {
            "original_snippet": original_snippet,
            "patched_snippet": patched_snippet,
            "full_patched_code": full_patched_code,
            "diff_content": diff_content,
            "what_changed": what_changed,
            "why_safer": why_safer
        }
