"""
llm/reasoning_engine/huggingface_local.py

Wiring point for a locally-hosted HuggingFace model such as DeepAnalyze-8B
(architecture.md Section 11 - Autonomous Reasoning Engine). This backend is
intentionally not loaded by default: an 8B-parameter model needs a GPU (or a
slow CPU/quantized path) and multi-gigabyte weights, which would make the
project fail to run out of the box. Enable it explicitly:

    REASONING_ENGINE_BACKEND=huggingface_local
    REASONING_ENGINE_MODEL=<hf-hub-id-or-local-path>

and install the extra dependencies:

    pip install transformers accelerate torch
"""

from __future__ import annotations

import json
from typing import Any

from llm.reasoning_engine.base import ReasoningEngine
from llm.reasoning_engine.anthropic_backend import PLANNING_SYSTEM_PROMPT, REASONING_SYSTEM_PROMPT


class HuggingFaceLocalReasoningEngine(ReasoningEngine):
    def __init__(self, model_name: str) -> None:
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "REASONING_ENGINE_BACKEND=huggingface_local requires transformers, accelerate, and torch. "
                "Install them with: pip install transformers accelerate torch"
            ) from exc

        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
        self._model_name = model_name

    def _generate(self, system_prompt: str, user_content: str, max_new_tokens: int) -> str:
        prompt = f"{system_prompt}\n\n{user_content}"
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
        output_ids = self._model.generate(**inputs, max_new_tokens=max_new_tokens)
        return self._tokenizer.decode(output_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

    def plan(self, user_objective: str) -> dict[str, Any]:
        text = self._generate(PLANNING_SYSTEM_PROMPT, user_objective, max_new_tokens=300)
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
        payload = json.dumps(
            {"objective": user_objective, "kpis": kpis, "insights": insights, "retrieved_knowledge": retrieved_knowledge},
            default=str,
        )
        return self._generate(REASONING_SYSTEM_PROMPT, payload, max_new_tokens=600)
