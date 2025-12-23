"""
Embedding Service

Generates embeddings for semantic search using sentence-transformers.
Based on Mind Protocol's embedding_service.py pattern.

DOCS: docs/infrastructure/embeddings/
"""

import hashlib
import logging
import os
import re
from typing import List, Dict, Any, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Singleton instance
_embedding_service: Optional['EmbeddingService'] = None


class EmbeddingService:
    """
    Embedding service using sentence-transformers.

    Uses all-mpnet-base-v2 (768 dimensions) for high-quality embeddings.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        """
        Initialize embedding service.

        Args:
            model_name: HuggingFace model name
        """
        self.model_name = model_name
        self.model = None
        self.dimension = 768  # all-mpnet-base-v2 dimension
        self._use_fallback = False

        logger.info(f"[EmbeddingService] Initializing with {model_name}")

    def _load_model(self):
        """Lazy load the model."""
        if self.model is None:
            if os.getenv("NGRAM_EMBEDDINGS_FALLBACK") == "1":
                self.model = "fallback"
                self._use_fallback = True
                logger.info("[EmbeddingService] Forced fallback embeddings via env.")
                return
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(self.model_name)
                self.dimension = self.model.get_sentence_embedding_dimension()
                logger.info(f"[EmbeddingService] Loaded model ({self.dimension} dimensions)")
            except ImportError:
                self.model = "fallback"
                self._use_fallback = True
                logger.warning(
                    "[EmbeddingService] sentence-transformers not installed; "
                    "using deterministic hash fallback embeddings."
                )

    def _fallback_embed(self, text: str) -> List[float]:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        if not tokens:
            return [0.0] * self.dimension
        vec = [0.0] * self.dimension
        for token in tokens:
            digest = hashlib.md5(token.encode("utf-8")).digest()
            for i in range(0, len(digest), 2):
                idx = ((digest[i] << 8) | digest[i + 1]) % self.dimension
                vec[idx] += 1.0
        norm = float(np.linalg.norm(vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def embed(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            List of floats (768 dimensions)
        """
        self._load_model()

        if not text or not text.strip():
            return [0.0] * self.dimension

        if self._use_fallback:
            return self._fallback_embed(text)

        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        self._load_model()

        if not texts:
            return []

        # Filter empty texts
        valid_texts = [t if t and t.strip() else " " for t in texts]

        if self._use_fallback:
            return [self._fallback_embed(text) for text in valid_texts]

        embeddings = self.model.encode(valid_texts, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_node(self, node: Dict[str, Any]) -> List[float]:
        """
        Generate embedding for a node based on its type.

        Args:
            node: Node dict with 'type' and relevant fields

        Returns:
            Embedding vector
        """
        node_type = node.get('type', '')
        text = self._node_to_text(node, node_type)
        return self.embed(text)

    def _node_to_text(self, node: Dict[str, Any], node_type: str) -> str:
        """Convert node to embeddable text."""
        parts = []

        if node_type == 'character':
            parts.append(f"{node.get('name', '')}")
            if node.get('backstory_wound'):
                parts.append(f"Wound: {node['backstory_wound']}")
            if node.get('backstory_why_here'):
                parts.append(f"Why here: {node['backstory_why_here']}")
            if node.get('values'):
                vals = node['values']
                if isinstance(vals, list):
                    parts.append(f"Values: {', '.join(vals)}")

        elif node_type == 'place':
            parts.append(f"{node.get('name', '')}, {node.get('place_type', 'place')}")
            if node.get('mood'):
                parts.append(f"Mood: {node['mood']}")
            if node.get('details'):
                details = node['details']
                if isinstance(details, list):
                    parts.append(f"Details: {', '.join(details)}")

        elif node_type == 'thing':
            parts.append(f"{node.get('name', '')}")
            if node.get('description'):
                parts.append(node['description'])
            if node.get('significance') and node['significance'] != 'mundane':
                parts.append(f"Significance: {node['significance']}")

        elif node_type == 'narrative':
            parts.append(f"{node.get('name', '')}: {node.get('content', '')}")
            if node.get('interpretation'):
                parts.append(f"Meaning: {node['interpretation']}")


        else:
            # Generic fallback
            parts.append(node.get('name', ''))
            parts.append(node.get('content', ''))
            parts.append(node.get('description', ''))

        return '. '.join(p for p in parts if p)

    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Similarity score (0-1 for normalized vectors)
        """
        a = np.array(vec1)
        b = np.array(vec2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def get_embedding_service() -> EmbeddingService:
    """Get singleton embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
