"""
Data Processing Agent.

Computes business KPIs and prepares the dataset for downstream analysis.

The dataset remains in memory and is passed through WorkflowState.
"""

from __future__ import annotations

import pandas as pd

from core.workflow.state import WorkflowState, log_stage
from utils.column_mapper import detect_columns


def _compute_kpis(
    df: pd.DataFrame,
    columns: dict[str, str | None],
) -> dict:
    revenue_col = columns.get("revenue")
    cost_col = columns.get("cost")
    profit_col = columns.get("profit")

    total_revenue = (
        float(df[revenue_col].sum())
        if revenue_col
        else 0.0
    )

    if profit_col:
        total_net_profit = float(df[profit_col].sum())
        total_cost = total_revenue - total_net_profit

    elif cost_col:
        total_cost = float(df[cost_col].sum())
        total_net_profit = total_revenue - total_cost

    else:
        total_cost = 0.0
        total_net_profit = total_revenue

    gross_profit = total_revenue - total_cost

    net_margin_pct = (
        total_net_profit / total_revenue * 100.0
        if total_revenue
        else 0.0
    )

    roi_pct = (
        total_net_profit / total_cost * 100.0
        if total_cost
        else 0.0
    )

    return {
        "total_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "gross_profit": round(gross_profit, 2),
        "total_net_profit": round(total_net_profit, 2),
        "net_profit_margin_pct": round(net_margin_pct, 2),
        "roi_pct": round(roi_pct, 2),
        "record_count": int(len(df)),
    }


def run_processor(state: WorkflowState) -> WorkflowState:
    """
    Process the cleaned in-memory DataFrame.
    """

    # cleaned_df = state["cleaned_dataframe"].copy()
    df = state["cleaned_dataframe"].copy()

    columns = detect_columns(df)

    kpis = _compute_kpis(df, columns)

    kpis["detected_columns"] = {
        key: value
        for key, value in columns.items()
        if value
    }

    if (
        columns.get("profit") is None
        and columns.get("cost") is None
    ):
        kpis["note"] = (
            "No cost or profit column was detected in this dataset; "
            "profit figures assume cost = 0 and should be treated "
            "as revenue-only KPIs."
        )

    state["processed_dataframe"] = df
    state["kpis"] = kpis

    log_stage(
        state,
        "Data Processing Agent: KPIs computed "
        "and dataset prepared in memory",
    )

    return state
