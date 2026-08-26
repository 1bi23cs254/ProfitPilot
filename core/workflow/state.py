"""
Defines the single WorkflowState object that flows through the LangGraph
orchestrator.
"""

from __future__ import annotations

from typing import Any, TypedDict

import pandas as pd


class WorkflowState(TypedDict, total=False):
    # Stage 1 - User Prompt
    user_objective: str
    dataset_path: str

    # Stage 2 - Planning
    execution_plan: dict[str, Any]

    # Stage 4 - Data Collection
    raw_row_count: int
    validation_summary: list[str]

    raw_dataframe: pd.DataFrame
    cleaned_dataframe: pd.DataFrame

    # Stage 5 - Data Processing
    processed_dataframe: pd.DataFrame
    kpis: dict[str, Any]

    # Stage 6 - Business Analysis
    insights: dict[str, Any]

    # Stage 7 - Knowledge Retrieval
    retrieved_knowledge: list[dict[str, Any]]

    # Stage 8 - Autonomous Business Reasoning
    business_reasoning: str

    # Stage 9 - Recommendation Generation
    recommendations: list[dict[str, Any]]

    # Stage 10 - Report Generation
    report_text: str
    report_path: str

    # Execution bookkeeping
    run_id: str
    stage_log: list[str]
    errors: list[str]


def new_state(
    user_objective: str,
    dataset_path: str,
    run_id: str,
) -> WorkflowState:
    """Create an empty, well-formed WorkflowState for a fresh run."""

    return WorkflowState(
        user_objective=user_objective,
        dataset_path=dataset_path,
        run_id=run_id,
        stage_log=[],
        errors=[],
        execution_plan={},
        kpis={},
        insights={},
        retrieved_knowledge=[],
        recommendations=[],
    )


def log_stage(state: WorkflowState, message: str) -> None:
    state.setdefault("stage_log", []).append(message)


def log_error(state: WorkflowState, message: str) -> None:
    state.setdefault("errors", []).append(message)
