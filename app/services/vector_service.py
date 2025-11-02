"""
Vector store service for managing FAQ search (simplified version without heavy ML dependencies).
"""

import re
from typing import List, Dict, Any
from app.config import get_settings
from data.insurance_faq import get_all_faqs


class VectorStoreService:
    """Service for keyword-based FAQ search."""

    def __init__(self):
        """Initialize vector store service."""
        settings = get_settings()
        self.settings = settings
        self.faqs = []

    def initialize_knowledge_base(self):
        """Load FAQ data into memory."""
        self.faqs = get_all_faqs()
        print(f"✓ Initialized knowledge base with {len(self.faqs)} FAQs")

    def _calculate_similarity(self, query: str, faq: Dict[str, Any]) -> float:
        """Calculate similarity score based on keyword matching."""
        query_lower = query.lower()

        # Extract words from query
        query_words = set(re.findall(r"\w+", query_lower))

        # Check question match
        question_words = set(re.findall(r"\w+", faq["question"].lower()))

        # Check keywords match
        keywords = set(k.lower() for k in faq["keywords"])

        # Check answer match (partial)
        answer_words = set(re.findall(r"\w+", faq["answer"].lower()[:200]))

        # Calculate scores
        question_match = len(query_words & question_words) / max(len(query_words), 1)
        keyword_match = len(query_words & keywords) / max(len(query_words), 1)
        answer_match = len(query_words & answer_words) / max(len(query_words), 1) * 0.5

        # Weighted score
        score = (question_match * 0.5) + (keyword_match * 0.4) + (answer_match * 0.1)

        # Bonus for exact phrase matches
        if any(word in faq["question"].lower() for word in query_words):
            score += 0.1

        return min(score, 1.0)

    def search_similar(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search for similar FAQs based on keyword matching."""
        if not self.faqs:
            self.initialize_knowledge_base()

        # Calculate similarity for all FAQs
        scored_faqs = []
        for faq in self.faqs:
            score = self._calculate_similarity(query, faq)
            if score > 0:
                scored_faqs.append(
                    {
                        "question": faq["question"],
                        "answer": faq["answer"],
                        "category": faq["category"],
                        "similarity_score": score,
                    }
                )

        # Sort by score and return top N
        scored_faqs.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_faqs[:n_results]


# Global vector store instance
vector_store_service = VectorStoreService()
