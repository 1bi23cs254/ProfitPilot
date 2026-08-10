"""
knowledge_base/rag/retriever.py

RAG Retrieval Layer (architecture.md Section 13 / 6.5). Responsible for
knowledge storage and document retrieval only — it never performs reasoning
(that belongs to llm/) and the Analysis Agent never calls this module
directly; only the orchestrator does (Module Communication Rule 4).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from knowledge_base.vector_store.base import VectorStore


def load_documents(documents_dir: Path) -> list[dict[str, Any]]:
    """Load every .md/.txt file under documents_dir as one retrievable document."""
    documents = []
    for path in sorted(documents_dir.glob("*.md")) + sorted(documents_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        documents.append({"id": path.stem, "source": path.name, "text": text})
    return documents


class KnowledgeRetriever:
    """Thin façade over a VectorStore: prepares the static knowledge base once
    (architecture.md ADR-008 - Static Knowledge Base Preparation) and answers
    retrieval queries at runtime."""

    def __init__(self, vector_store: VectorStore, documents_dir: Path) -> None:
        self._vector_store = vector_store
        self._documents_dir = documents_dir

    def prepare(self) -> int:
        documents = load_documents(self._documents_dir)
        self._vector_store.build(documents)
        return len(documents)

    def retrieve(self, query: str, top_k: int) -> list[dict[str, Any]]:
        if not self._vector_store.is_ready():
            self.prepare()
        return self._vector_store.query(query, top_k)
