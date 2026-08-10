"""
llm/reasoning_engine/deepanalyze_backend.py

Local DeepAnalyze-8B reasoning backend.

ProfitPilot communicates with the local llama.cpp server through its
OpenAI-compatible HTTP API.

The backend implements the same ReasoningEngine interface as the existing
rule-based, Anthropic, and HuggingFace backends.
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
                parsed = json.loads(cleaned[start : end + 1])
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass

        return None

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

        payload = {
            "objective": user_objective,
            "kpis": kpis,
            "analytical_insights": insights,
            "retrieved_business_knowledge": retrieved_knowledge,
        }

        return self._chat(
            REASONING_SYSTEM_PROMPT,
            json.dumps(payload, default=str, indent=2),
            max_tokens=self._max_tokens,
        )