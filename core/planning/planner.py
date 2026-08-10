"""
core/planning/planner.py

Stage 2 of the workflow (architecture.md 5.2). Converts the user's single
natural-language objective into a structured execution plan by invoking the
Autonomous Reasoning Engine in Planning Mode. This module contains no
business analysis logic of its own — it only calls the reasoning engine and
records the result on the workflow state.
"""

from __future__ import annotations

from core.workflow.state import WorkflowState, log_stage
from llm.reasoning_engine.base import ReasoningEngine


def run_planning(state: WorkflowState, reasoning_engine: ReasoningEngine) -> WorkflowState:
    plan = reasoning_engine.plan(state["user_objective"])
    state["execution_plan"] = plan
    log_stage(state, "Planning completed")
    return state
