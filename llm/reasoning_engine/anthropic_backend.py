"""
llm/reasoning_engine/anthropic_backend.py

Optional Autonomous Reasoning Engine backend that calls a hosted LLM through
the Anthropic API. This is a drop-in replacement for RuleBasedReasoningEngine
(same ReasoningEngine interface) and demonstrates architecture.md's Loose
Coupling principle: swapping the reasoning engine requires no change to any
agent, the orchestrator, or the RAG layer.

Enabled by setting REASONING_ENGINE_BACKEND=anthropic and ANTHROPIC_API_KEY
in .env. See llm/README.md for how to instead wire in a locally-hosted model
such as DeepAnalyze-8B via `huggingface_local.py`.
"""

from __future__ import annotations

import json
from typing import Any

from llm.reasoning_engine.base import ReasoningEngine


PLANNING_SYSTEM_PROMPT = (
    "You are the planning stage of an autonomous business-intelligence reasoning engine. "
    "Given a business objective, respond with ONLY a JSON object with keys "
    '"objective" (string), "focus_areas" (list of strings, chosen from '
    '["pricing","inventory","marketing","cost","profitability"]), and "steps" '
    "(list of strings describing the analysis pipeline). No prose, no markdown fences."
)

REASONING_SYSTEM_PROMPT = (
    "You are the business-reasoning stage of an autonomous business-intelligence system. "
    "You will be given business KPIs, analytical insights, and retrieved business knowledge as JSON. "
    "Produce a concise, evidence-grounded reasoning narrative (plain text, 150-300 words) that explains "
    "business performance and directly supports later recommendation generation. Every claim must be "
    "traceable to a number or knowledge snippet you were given. Do not invent data."
)


class AnthropicReasoningEngine(ReasoningEngine):
    def __init__(self, api_key: str, model: str, max_tokens: int, temperature: float) -> None:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "The 'anthropic' package is required for REASONING_ENGINE_BACKEND=anthropic. "
                "Install it with: pip install anthropic"
            ) from exc

        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set but REASONING_ENGINE_BACKEND=anthropic.")

        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature

    def plan(self, user_objective: str) -> dict[str, Any]:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=400,
            temperature=self._temperature,
            system=PLANNING_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_objective}],
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "objective": user_objective,
                "focus_areas": ["profitability"],
                "steps": ["collect_and_validate_data", "compute_kpis", "run_business_analysis"],
                "raw_model_output": text,
            }

    def reason(
        self,
        kpis: dict[str, Any],
        insights: dict[str, Any],
        retrieved_knowledge: list[dict[str, Any]],
        user_objective: str,
    ) -> str:
        payload = {
            "objective": user_objective,
            "kpis": kpis,
            "insights": insights,
            "retrieved_knowledge": retrieved_knowledge,
        }
        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
            system=REASONING_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": json.dumps(payload, default=str)}],
        )
        return "".join(block.text for block in response.content if block.type == "text")
