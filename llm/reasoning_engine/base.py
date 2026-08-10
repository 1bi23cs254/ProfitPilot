"""
llm/reasoning_engine/base.py

Abstract interface for the Autonomous Reasoning Engine
(architecture.md Section 14). The engine has exactly two responsibilities:

  1. Planning  - understand the user's natural-language objective and
     produce a structured execution plan.
  2. Business Reasoning - combine KPIs, analytical insights, and retrieved
     knowledge into an evidence-grounded reasoning narrative.

No business logic lives here (architecture.md 10. llm/ directory rule) and
the engine never loads datasets directly (Module Communication Rule 3).
Concrete backends are drop-in replacements for this interface, satisfying
Principle 6 (Loose Coupling) and Principle 14 (Future Extensibility) —
DeepAnalyze-8B, any other local model, or a hosted API can all be plugged
in without touching any other module.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ReasoningEngine(ABC):
    """Base class every reasoning-engine backend must implement."""

    @abstractmethod
    def plan(self, user_objective: str) -> dict[str, Any]:
        """Planning mode: turn a natural-language objective into a
        structured execution plan the orchestrator can act on."""
        raise NotImplementedError

    @abstractmethod
    def reason(
        self,
        kpis: dict[str, Any],
        insights: dict[str, Any],
        retrieved_knowledge: list[dict[str, Any]],
        user_objective: str,
    ) -> str:
        """Business reasoning mode: synthesize KPIs, analytical insights, and
        retrieved knowledge into an explainable business-reasoning narrative."""
        raise NotImplementedError
