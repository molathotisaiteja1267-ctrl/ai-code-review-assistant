import math
import re
from typing import List, Dict, Any, Tuple

class SimpleVectorStore:
    """
    Lightweight, high-performance in-memory vector store with TF-IDF cosine similarity.
    Works out-of-the-box in all environments with zero external binary dependencies.
    """
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def add_document(self, doc_id: str, text: str, metadata: Dict[str, Any]):
        tokens = self._tokenize(text)
        self.documents.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata,
            "tokens": tokens,
            "vector": self._vectorize(tokens)
        })

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        query_tokens = self._tokenize(query)
        query_vector = self._vectorize(query_tokens)
        
        results = []
        for doc in self.documents:
            sim = self._cosine_similarity(query_vector, doc["vector"])
            if sim > 0.05:
                results.append((doc, sim))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _vectorize(self, tokens: List[str]) -> Dict[str, float]:
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        # Normalize
        norm = math.sqrt(sum(v * v for v in tf.values())) or 1.0
        return {k: v / norm for k, v in tf.items()}

    def _cosine_similarity(self, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        dot = 0.0
        for k, v in vec_a.items():
            if k in vec_b:
                dot += v * vec_b[k]
        return round(dot, 4)
