"""
Business Tactics Agent.

Uses the reasoning engine to:

1. Generate evidence-grounded business reasoning.
2. Generate evidence-grounded business recommendations.

Neither reasoning nor recommendations are generated through hardcoded
Python business rules.
"""

from __future__ import annotations

from core.workflow.state import WorkflowState, log_stage
from llm.reasoning_engine.base import ReasoningEngine


def run_business_tactics(
    state: WorkflowState,
    reasoning_engine: ReasoningEngine,
) -> WorkflowState:
    """
    Generate business reasoning and recommendations from the LLM.

    The Python pipeline provides deterministic KPIs, analytical insights,
    and retrieved business knowledge. The reasoning engine interprets
    this evidence and generates both the reasoning narrative and
    actionable recommendations.
    """

    kpis = state.get("kpis", {})
    insights = state.get("insights", {})
    retrieved_knowledge = state.get("retrieved_knowledge", [])

    # Generate business reasoning through the LLM.
    business_reasoning = reasoning_engine.reason(
        kpis=kpis,
        insights=insights,
        retrieved_knowledge=retrieved_knowledge,
        user_objective=state["user_objective"],
    )

    state["business_reasoning"] = business_reasoning

    # Generate recommendations through the LLM.
    recommendations = reasoning_engine.recommend(
        kpis=kpis,
        insights=insights,
        retrieved_knowledge=retrieved_knowledge,
        user_objective=state["user_objective"],
        business_reasoning=business_reasoning,
    )

    state["recommendations"] = recommendations

    log_stage(
        state,
        "Business Tactics Agent: evidence-grounded business reasoning "
        f"and {len(recommendations)} LLM-generated recommendations completed",
    )

    return state
