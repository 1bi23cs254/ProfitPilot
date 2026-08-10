"""
llm/reasoning_engine/factory.py

Selects the configured ReasoningEngine backend. This is the only place in
the codebase that knows which concrete backend is active — every caller
(core/planning, agents/business_tactics) depends only on the abstract
ReasoningEngine interface (architecture.md Principle 6 - Loose Coupling).
"""

from __future__ import annotations

from config.settings import ReasoningEngineConfig
from llm.reasoning_engine.base import ReasoningEngine
from llm.reasoning_engine.rule_based import RuleBasedReasoningEngine


def build_reasoning_engine(config: ReasoningEngineConfig) -> ReasoningEngine:
    backend = config.backend.strip().lower()

    if backend == "rule_based":
        return RuleBasedReasoningEngine()

    if backend == "anthropic":
        from llm.reasoning_engine.anthropic_backend import AnthropicReasoningEngine

        return AnthropicReasoningEngine(
            api_key=config.anthropic_api_key,
            model=config.anthropic_model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
        )

    if backend == "huggingface_local":
        from llm.reasoning_engine.huggingface_local import HuggingFaceLocalReasoningEngine

        return HuggingFaceLocalReasoningEngine(model_name=config.model_name)

    if backend == "deepanalyze":
        from llm.reasoning_engine.deepanalyze_backend import (
            DeepAnalyzeReasoningEngine,
        )

        return DeepAnalyzeReasoningEngine(
            base_url=config.deepanalyze_base_url,
            model_name=config.model_name,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
        )

    raise ValueError(
        f"Unknown REASONING_ENGINE_BACKEND '{config.backend}'. "
        "Expected one of: rule_based, anthropic, huggingface_local, deepanalyze."
    )
