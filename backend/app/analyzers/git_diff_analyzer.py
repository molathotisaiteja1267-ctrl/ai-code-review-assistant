import re
from typing import List, Dict, Any, Optional

class DiffHunk:
    def __init__(self, old_start: int, old_count: int, new_start: int, new_count: int, lines: List[str]):
        self.old_start = old_start
        self.old_count = old_count
        self.new_start = new_start
        self.new_count = new_count
        self.lines = lines

class GitDiffAnalyzer:
    @staticmethod
    def parse_unified_diff(diff_text: str) -> List[Dict[str, Any]]:
        """Parses unified diff format and returns changed files with line ranges."""
        files = []
        current_file = None
        
        diff_lines = diff_text.splitlines()
        i = 0
        while i < len(diff_lines):
            line = diff_lines[i]
            if line.startswith("diff --git"):
                parts = line.split(" ")
                old_file = parts[2][2:] if len(parts) > 2 else "unknown"
                new_file = parts[3][2:] if len(parts) > 3 else "unknown"
                current_file = {
                    "old_file": old_file,
                    "new_file": new_file,
                    "file_path": new_file if new_file != "/dev/null" else old_file,
                    "hunks": [],
                    "added_lines": [],
                    "deleted_lines": [],
                    "modified_ranges": []
                }
                files.append(current_file)
            elif line.startswith("@@ ") and current_file:
                # Format: @@ -old_start,old_count +new_start,new_count @@
                match = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
                if match:
                    old_start = int(match.group(1))
                    old_count = int(match.group(2)) if match.group(2) else 1
                    new_start = int(match.group(3))
                    new_count = int(match.group(4)) if match.group(4) else 1
                    
                    hunk_lines = []
                    current_new_line = new_start
                    i += 1
                    while i < len(diff_lines) and not diff_lines[i].startswith("@@ ") and not diff_lines[i].startswith("diff --git"):
                        h_line = diff_lines[i]
                        hunk_lines.append(h_line)
                        if h_line.startswith("+"):
                            current_file["added_lines"].append(current_new_line)
                            current_new_line += 1
                        elif h_line.startswith("-"):
                            current_file["deleted_lines"].append(current_new_line)
                        else:
                            current_new_line += 1
                        i += 1
                    
                    current_file["hunks"].append({
                        "old_start": old_start,
                        "old_count": old_count,
                        "new_start": new_start,
                        "new_count": new_count,
                        "lines": hunk_lines
                    })
                    current_file["modified_ranges"].append((new_start, new_start + new_count))
                    continue
            i += 1
            
        return files
