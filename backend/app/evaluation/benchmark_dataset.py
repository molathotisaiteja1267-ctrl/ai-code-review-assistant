from typing import List, Dict, Any

class BenchmarkDataset:
    @staticmethod
    def get_ground_truth_samples() -> List[Dict[str, Any]]:
        return [
            {
                "id": "bench-01",
                "title": "SQL Injection in User Search",
                "category": "security",
                "expected_vulnerable": True,
                "expected_issue_keywords": ["SQL", "Injection", "B608"],
                "code": "def search_users(cursor, user_input):\n    query = f\"SELECT id, username, email FROM users WHERE username = '{user_input}'\"\n    cursor.execute(query)\n    return cursor.fetchall()"
            },
            {
                "id": "bench-02",
                "title": "Command Injection via Shell",
                "category": "security",
                "expected_vulnerable": True,
                "expected_issue_keywords": ["Command", "Shell", "subprocess"],
                "code": "import subprocess\n\ndef ping_host(host_ip):\n    cmd = f\"ping -c 1 {host_ip}\"\n    subprocess.run(cmd, shell=True)"
            },
            {
                "id": "bench-03",
                "title": "Hardcoded JWT Secret Key",
                "category": "security",
                "expected_vulnerable": True,
                "expected_issue_keywords": ["Hardcoded", "Secret", "Credential"],
                "code": "API_SECRET_KEY = \"ak_live_93819830198301830193801938\"\n\ndef get_header():\n    return {\"Authorization\": f\"Bearer {API_SECRET_KEY}\"}"
            },
            {
                "id": "bench-04",
                "title": "Insecure Deserialization (pickle)",
                "category": "security",
                "expected_vulnerable": True,
                "expected_issue_keywords": ["Pickle", "Deserialization", "B301"],
                "code": "import pickle\n\ndef load_payload(raw_bytes):\n    return pickle.loads(raw_bytes)"
            },
            {
                "id": "bench-05",
                "title": "O(n²) Nested Iteration Bottleneck",
                "category": "performance",
                "expected_vulnerable": True,
                "expected_issue_keywords": ["Nested", "O(n²)", "Iteration", "Loop"],
                "code": "def find_matching_transactions(account_txs, fraud_txs):\n    matches = []\n    for a in account_txs:\n        for f in fraud_txs:\n            if a[\"id\"] == f[\"id\"]:\n                matches.append((a, f))\n    return matches"
            },
            {
                "id": "bench-06",
                "title": "Bare Except Clause Swallowing Errors",
                "category": "code_quality",
                "expected_vulnerable": True,
                "expected_issue_keywords": ["Bare", "except", "Swallowed"],
                "code": "def save_data(data):\n    try:\n        with open(\"data.txt\", \"w\") as f:\n            f.write(data)\n    except:\n        pass"
            },
            {
                "id": "bench-07",
                "title": "Mutable Default Argument in Function",
                "category": "bug",
                "expected_vulnerable": True,
                "expected_issue_keywords": ["Mutable", "Default"],
                "code": "def append_to_cache(item, cache=[]):\n    cache.append(item)\n    return cache"
            },
            {
                "id": "bench-08",
                "title": "Clean Idiomatic Code - Parameterized SQL",
                "category": "clean",
                "expected_vulnerable": False,
                "expected_issue_keywords": [],
                "code": "import sqlite3\n\ndef get_user_by_id(cursor: sqlite3.Cursor, user_id: int):\n    query = \"SELECT id, username, email FROM users WHERE id = ?\"\n    cursor.execute(query, (user_id,))\n    return cursor.fetchone()"
            },
            {
                "id": "bench-09",
                "title": "Clean Idiomatic Code - Linear Set Lookup",
                "category": "clean",
                "expected_vulnerable": False,
                "expected_issue_keywords": [],
                "code": "def filter_active_ids(primary_ids: list, active_set: set) -> list:\n    return [pid for pid in primary_ids if pid in active_set]"
            },
            {
                "id": "bench-10",
                "title": "Clean Idiomatic Code - Environment Secret",
                "category": "clean",
                "expected_vulnerable": False,
                "expected_issue_keywords": [],
                "code": "import os\n\ndef get_api_client():\n    token = os.getenv(\"API_TOKEN\")\n    if not token:\n        raise ValueError(\"API_TOKEN environment variable not set.\")\n    return {\"token\": token}"
            }
        ]
