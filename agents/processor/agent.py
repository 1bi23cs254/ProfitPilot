"""
agents/processor/agent.py

Data Processing Agent (architecture.md 6.3 / 7.5). Computes business KPIs
(revenue, cost, gross/net profit, margin, ROI) and persists processed data.
It never performs trend/forecast/anomaly analysis (that is the Analysis
Agent's responsibility) and never retrieves knowledge or reasons about the
numbers.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from core.workflow.state import WorkflowState, log_stage
from utils.column_mapper import detect_columns


def _compute_kpis(df: pd.DataFrame, columns: dict[str, str | None]) -> dict:
    revenue_col = columns.get("revenue")
    cost_col = columns.get("cost")
    profit_col = columns.get("profit")

    total_revenue = float(df[revenue_col].sum()) if revenue_col else 0.0

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
    net_margin_pct = (total_net_profit / total_revenue * 100.0) if total_revenue else 0.0
    roi_pct = (total_net_profit / total_cost * 100.0) if total_cost else 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "gross_profit": round(gross_profit, 2),
        "total_net_profit": round(total_net_profit, 2),
        "net_profit_margin_pct": round(net_margin_pct, 2),
        "roi_pct": round(roi_pct, 2),
        "record_count": int(len(df)),
    }


def run_processor(state: WorkflowState, processed_dir: Path) -> WorkflowState:
    cleaned_df = pd.read_csv(state["cleaned_dataset_path"])
    columns = detect_columns(cleaned_df)

    kpis = _compute_kpis(cleaned_df, columns)
    kpis["detected_columns"] = {k: v for k, v in columns.items() if v}

    if columns.get("profit") is None and columns.get("cost") is None:
        kpis["note"] = (
            "No cost or profit column was detected in this dataset; profit figures assume "
            "cost = 0 and should be treated as revenue-only KPIs."
        )

    processed_path = processed_dir / f"{Path(state['cleaned_dataset_path']).stem}_processed.csv"
    cleaned_df.to_csv(processed_path, index=False)

    state["processed_dataset_path"] = str(processed_path)
    state["kpis"] = kpis

    log_stage(state, "Data Processing Agent: KPIs computed")
    return state
