"""
Vector store service for managing FAQ search (simplified version without heavy ML dependencies).
Supports loading from multiple knowledge base sources.
"""

import re
import json
import os
from pathlib import Path
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
        self.knowledge_base_path = (
            Path(__file__).parent.parent.parent / "knowledge_base"
        )

    def _load_json_knowledge(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load knowledge from a JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = []
                category = data.get("category", "general")

                for item in data.get("items", []):
                    items.append(
                        {
                            "question": item["question"],
                            "answer": item["answer"],
                            "category": category,
                            "keywords": item.get("keywords", []),
                            "priority": item.get("priority", "medium"),
                        }
                    )

                return items
        except Exception as e:
            print(f"Warning: Could not load {file_path}: {e}")
            return []

    def _load_custom_knowledge_base(self) -> List[Dict[str, Any]]:
        """Load all custom knowledge base files from knowledge_base directory."""
        all_items = []

        if not self.knowledge_base_path.exists():
            print(f"ℹ️  Knowledge base directory not found: {self.knowledge_base_path}")
            return all_items

        # Load from company_info.json
        company_info = self.knowledge_base_path / "company_info.json"
        if company_info.exists():
            all_items.extend(self._load_json_knowledge(company_info))

        # Load from products directory
        products_dir = self.knowledge_base_path / "products"
        if products_dir.exists():
            for json_file in products_dir.glob("*.json"):
                all_items.extend(self._load_json_knowledge(json_file))

        # Load from policies directory
        policies_dir = self.knowledge_base_path / "policies"
        if policies_dir.exists():
            for json_file in policies_dir.glob("*.json"):
                all_items.extend(self._load_json_knowledge(json_file))

        return all_items

    def initialize_knowledge_base(self):
        """Load FAQ data from both default FAQs and custom knowledge base."""
        # Load default FAQs
        default_faqs = get_all_faqs()

        # Load custom knowledge base (company-specific)
        custom_knowledge = self._load_custom_knowledge_base()

        # Combine both sources
        self.faqs = default_faqs + custom_knowledge

        default_count = len(default_faqs)
        custom_count = len(custom_knowledge)

        print(f"✓ Initialized knowledge base:")
        print(f"  - Default FAQs: {default_count}")
        print(f"  - Custom knowledge: {custom_count}")
        print(f"  - Total items: {len(self.faqs)}")

    def reload_knowledge_base(self):
        """Reload knowledge base (useful for updates without restart)."""
        self.faqs = []
        self.initialize_knowledge_base()
        return {
            "status": "success",
            "total_items": len(self.faqs),
            "message": "Knowledge base reloaded successfully",
        }

    def _calculate_similarity(self, query: str, faq: Dict[str, Any]) -> float:
        """Calculate similarity score based on keyword matching with priority weighting."""
        query_lower = query.lower()

        # Extract words from query
        query_words = set(re.findall(r"\w+", query_lower))

        # Check question match
        question_words = set(re.findall(r"\w+", faq["question"].lower()))

        # Check keywords match
        keywords = set(k.lower() for k in faq.get("keywords", []))

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

        # Priority boost
        priority_boost = {"high": 0.15, "medium": 0.05, "low": 0.0}
        score += priority_boost.get(faq.get("priority", "medium"), 0.05)

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
