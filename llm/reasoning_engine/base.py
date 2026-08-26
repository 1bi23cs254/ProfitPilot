"""
llm/reasoning_engine/base.py

Abstract interface for the Autonomous Reasoning Engine.

Responsibilities:

1. Planning
   - Understand the user's natural-language objective.
   - Produce a structured execution plan.

2. Business Reasoning
   - Interpret KPIs, analytical insights, and retrieved business knowledge.

3. Recommendation Generation
   - Generate evidence-grounded business recommendations from the same
     available evidence.

The reasoning engine never loads datasets directly and does not contain
deterministic business-analysis logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ReasoningEngine(ABC):
    """Base class every reasoning-engine backend must implement."""

    @abstractmethod
    def plan(
        self,
        user_objective: str,
    ) -> dict[str, Any]:
        """
        Planning mode: turn a natural-language objective into a
        structured execution plan.
        """
        raise NotImplementedError

    @abstractmethod
    def reason(
        self,
        kpis: dict[str, Any],
        insights: dict[str, Any],
        retrieved_knowledge: list[dict[str, Any]],
        user_objective: str,
    ) -> str:
        """
        Business reasoning mode: synthesize KPIs, analytical insights,
        and retrieved knowledge into an evidence-grounded narrative.
        """
        raise NotImplementedError

    @abstractmethod
    def recommend(
        self,
        kpis: dict[str, Any],
        insights: dict[str, Any],
        retrieved_knowledge: list[dict[str, Any]],
        user_objective: str,
        business_reasoning: str,
    ) -> list[dict[str, Any]]:
        """
        Recommendation mode: generate evidence-grounded business
        recommendations based on the available analysis and reasoning.
        """
        raise NotImplementedError
