"""
llm/reasoning_engine/deepanalyze_backend.py

Local DeepAnalyze-8B reasoning backend.

ProfitPilot communicates with the local llama.cpp server through its
OpenAI-compatible HTTP API.

The backend implements the ReasoningEngine interface for:

1. Planning
2. Business reasoning
3. Recommendation generation
"""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from llm.reasoning_engine.base import ReasoningEngine


PLANNING_SYSTEM_PROMPT = """
You are the planning component of ProfitPilot, an autonomous business
intelligence system.

Your task is to understand the user's business objective and produce a
structured execution plan.

Return ONLY a valid JSON object with exactly these keys:

{
  "objective": "original objective",
  "focus_areas": ["pricing", "inventory", "marketing", "cost", "profitability"],
  "steps": ["step1", "step2", "..."]
}

Rules:
- focus_areas must contain only relevant values from:
  pricing, inventory, marketing, cost, profitability
- steps must describe useful business-analysis activities.
- Do not include markdown.
- Do not include explanations outside the JSON object.
"""


REASONING_SYSTEM_PROMPT = """
You are the autonomous business-reasoning component of ProfitPilot.

You receive:
1. The user's business objective.
2. Deterministically calculated KPIs.
3. Analytical findings calculated by ProfitPilot.
4. Retrieved business knowledge from the RAG system.

Your job is to interpret this evidence and produce a concise,
evidence-grounded business reasoning narrative.

CRITICAL RULES:
- Do not invent numbers.
- Do not recalculate financial metrics yourself if the calculated value
  is already provided.
- Treat KPIs and analytical findings as authoritative.
- Clearly distinguish observed facts from possible explanations.
- Use retrieved knowledge only when relevant.
- Explain why the findings matter to profitability.
- Identify the strongest business opportunities and risks.
- Do not make recommendations unsupported by the provided evidence.

Return plain text, not JSON and not markdown tables.
"""


RECOMMENDATION_SYSTEM_PROMPT = """
You are the recommendation component of ProfitPilot.

You receive:
1. The user's business objective.
2. Deterministically calculated KPIs.
3. Analytical findings.
4. Retrieved business knowledge.
5. Business reasoning generated from the same evidence.

Your task is to generate practical business recommendations based ONLY
on the provided evidence.

Return ONLY a valid JSON array.

Each recommendation must have exactly these keys:

[
  {
    "category": "pricing",
    "recommendation": "Clear action the business should take",
    "evidence": "Specific evidence supporting this recommendation",
    "confidence_score": 0.0,
    "expected_impact": "Expected business impact"
  }
]

Rules:
- Generate up to 3 recommendations.
- Recommendations must be based on the provided evidence.
- Do not invent data, numbers, customers, products, or business facts.
- Do not generate generic advice unless supported by the evidence.
- category should preferably be one of:
  pricing, inventory, marketing, cost, profitability, operations
- confidence_score must be a number between 0 and 1.
- expected_impact must describe the likely business outcome.
- Keep every field concise.
- Do not include markdown.
- Do not include explanations before or after the JSON array.
- Return only the JSON array.
- If fewer than 3 recommendations are supported by the evidence,
  return fewer recommendations instead of inventing recommendations.
"""


class DeepAnalyzeReasoningEngine(ReasoningEngine):
    """ReasoningEngine implementation backed by local DeepAnalyze-8B."""

    def __init__(
        self,
        base_url: str,
        model_name: str,
        max_tokens: int,
        temperature: float,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model_name = model_name
        self._max_tokens = max_tokens
        self._temperature = temperature

    def _chat(
        self,
        system_prompt: str,
        user_content: str,
        max_tokens: int,
    ) -> str:
        url = f"{self._base_url}/chat/completions"

        payload = {
            "model": self._model_name,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_content,
                },
            ],
            "temperature": self._temperature,
            "max_tokens": max_tokens,
        }

        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=300) as response:
                response_data = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"DeepAnalyze API returned HTTP {exc.code}: {error_body}"
            ) from exc

        except URLError as exc:
            raise RuntimeError(
                "Could not connect to the DeepAnalyze server at "
                f"{self._base_url}. Make sure llama-server is running."
            ) from exc

        except TimeoutError as exc:
            raise RuntimeError(
                "DeepAnalyze request timed out."
            ) from exc

        try:
            return response_data["choices"][0]["message"]["content"].strip()

        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Unexpected response from DeepAnalyze: {response_data}"
            ) from exc

    @staticmethod
    def _extract_json(text: str) -> dict[str, Any] | None:
        """Extract a JSON object even if the model adds surrounding text."""

        cleaned = text.strip()

        # Remove markdown code fences if present.
        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        try:
            parsed = json.loads(cleaned)

            if isinstance(parsed, dict):
                return parsed

        except json.JSONDecodeError:
            pass

        # Try to find the first JSON object in the response.
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start >= 0 and end > start:
            try:
                parsed = json.loads(cleaned[start:end + 1])

                if isinstance(parsed, dict):
                    return parsed

            except json.JSONDecodeError:
                pass

        return None

    @staticmethod
    def _extract_json_array(text: str) -> list[dict[str, Any]]:
        """
        Extract a JSON array from the model response.

        Supports responses where the model wraps the JSON inside:
        <Answer>
        [...]
        </Answer>

        or markdown code fences.
        """

        cleaned = text.strip()

        # First, try to extract content inside <Answer> tags.
        answer_match = re.search(
            r"<Answer>\s*(.*?)\s*</Answer>",
            cleaned,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if answer_match:
            cleaned = answer_match.group(1).strip()

        # Remove markdown code fences if present.
        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        # Try parsing directly.
        try:
            parsed = json.loads(cleaned)

            if isinstance(parsed, list):
                return [
                    item
                    for item in parsed
                    if isinstance(item, dict)
                ]

        except json.JSONDecodeError:
            pass

        # Fallback: locate the JSON array inside the response.
        start = cleaned.find("[")
        end = cleaned.rfind("]")

        if start >= 0 and end > start:
            json_text = cleaned[start: end + 1]

            try:
                parsed = json.loads(json_text)

                if isinstance(parsed, list):
                    return [
                        item
                        for item in parsed
                        if isinstance(item, dict)
                    ]

            except json.JSONDecodeError:
                pass

        return []

    @staticmethod
    def _prepare_llm_context(
        kpis: dict[str, Any],
        insights: dict[str, Any],
        retrieved_knowledge: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Prepare a compact, evidence-preserving context for the LLM.

        The full analysis remains available in the workflow state, but
        only the most relevant analytical evidence is sent to the local
        model to stay within its context window.
        """

        compact_insights: dict[str, Any] = {}

        if "trend" in insights:
            compact_insights["trend"] = insights["trend"]

        if "forecast" in insights:
            compact_insights["forecast"] = insights["forecast"]

        if "top_products" in insights:
            compact_insights["top_products"] = insights["top_products"][:5]

        if "low_margin_products" in insights:
            compact_insights["low_margin_products"] = (
                insights["low_margin_products"][:5]
            )

        anomalies = insights.get("anomalies")

        if isinstance(anomalies, dict):
            compact_anomalies: dict[str, Any] = {
                "count": anomalies.get("count", 0),
                "feature_columns": anomalies.get("feature_columns", []),
            }

            examples = anomalies.get("examples", [])

            if isinstance(examples, list) and examples:
                compact_anomalies["examples"] = examples[:2]

            compact_insights["anomalies"] = compact_anomalies

        compact_knowledge: list[dict[str, Any]] = []

        for item in retrieved_knowledge[:3]:
            if not isinstance(item, dict):
                continue

            compact_item = {}

            if "source" in item:
                compact_item["source"] = item["source"]

            if "content" in item:
                compact_item["content"] = str(item["content"])[:500]

            if "relevance" in item:
                compact_item["relevance"] = item["relevance"]

            compact_knowledge.append(compact_item)

        return {
            "kpis": kpis,
            "analytical_insights": compact_insights,
            "retrieved_business_knowledge": compact_knowledge,
        }

    def plan(self, user_objective: str) -> dict[str, Any]:
        text = self._chat(
            PLANNING_SYSTEM_PROMPT,
            user_objective,
            max_tokens=400,
        )

        parsed = self._extract_json(text)

        if parsed is None:
            return {
                "objective": user_objective,
                "focus_areas": ["profitability"],
                "steps": [
                    "collect_and_validate_data",
                    "compute_kpis",
                    "run_business_analysis",
                    "retrieve_domain_knowledge",
                    "generate_business_reasoning",
                    "generate_recommendations",
                    "generate_report",
                ],
                "raw_model_output": text,
            }

        parsed.setdefault("objective", user_objective)
        parsed.setdefault("focus_areas", ["profitability"])
        parsed.setdefault("steps", [])

        return parsed

    def reason(
        self,
        kpis: dict[str, Any],
        insights: dict[str, Any],
        retrieved_knowledge: list[dict[str, Any]],
        user_objective: str,
    ) -> str:
        """
        Generate evidence-grounded business reasoning.
        """

        context = self._prepare_llm_context(
            kpis=kpis,
            insights=insights,
            retrieved_knowledge=retrieved_knowledge,
        )

        payload = {
            "objective": user_objective,
            **context,
        }

        return self._chat(
            REASONING_SYSTEM_PROMPT,
            json.dumps(
                payload,
                default=str,
                separators=(",", ":"),
            ),
            max_tokens=self._max_tokens,
        )

    def recommend(
        self,
        kpis: dict[str, Any],
        insights: dict[str, Any],
        retrieved_knowledge: list[dict[str, Any]],
        user_objective: str,
        business_reasoning: str,
    ) -> list[dict[str, Any]]:
        """
        Generate evidence-grounded business recommendations.
        """

        context = self._prepare_llm_context(
            kpis=kpis,
            insights=insights,
            retrieved_knowledge=retrieved_knowledge,
        )

        payload = {
            "objective": user_objective,
            **context,
            "business_reasoning": business_reasoning[:1500],
        }

        text = self._chat(
            RECOMMENDATION_SYSTEM_PROMPT,
            json.dumps(
                payload,
                default=str,
                separators=(",", ":"),
            ),
            max_tokens=min(self._max_tokens, 800),
        )

        recommendations = self._extract_json_array(text)

        return recommendations
