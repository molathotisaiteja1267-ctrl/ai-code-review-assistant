from typing import List, Dict, Any
from app.rag.vector_store import SimpleVectorStore

class RAGService:
    def __init__(self):
        self.store = SimpleVectorStore()
        self._seed_default_guidelines()

    def _seed_default_guidelines(self):
        default_rules = [
            ("rule_db_repository", "Architecture: All database queries must go through repository classes. Do not invoke cursor.execute directly in views or controllers.", {"type": "architecture"}),
            ("rule_auth_rbac", "Security: All administrative endpoints must enforce Role-Based Access Control (@require_role('admin')).", {"type": "security"}),
            ("rule_secrets", "Security: Never commit API keys, passwords, or tokens in source code. Use os.getenv or AWS Secrets Manager.", {"type": "security"}),
            ("rule_async_io", "Performance: Use async/await for network I/O and external API calls to avoid blocking the event loop.", {"type": "performance"}),
            ("rule_error_logging", "Code Quality: Always log caught exceptions with exc_info=True instead of swallowing them with bare pass.", {"type": "reliability"})
        ]
        for rid, content, meta in default_rules:
            self.store.add_document(rid, content, meta)

    def add_project_rule(self, rule_id: str, content: str, rule_type: str = "guideline"):
        self.store.add_document(rule_id, content, {"type": rule_type})

    def retrieve_relevant_rules(self, code_snippet: str, top_k: int = 3) -> List[str]:
        results = self.store.search(code_snippet, top_k=top_k)
        return [doc["text"] for doc, score in results]

rag_service = RAGService()
