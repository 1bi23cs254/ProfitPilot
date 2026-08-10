"""
agents/analysis/agent.py

Analysis Agent (architecture.md 6.4 / 7.6). Performs trend analysis,
forecasting, anomaly detection, and product/segment performance analysis
using the models in models/. It never retrieves knowledge directly
(Module Communication Rule 4 — that is the RAG layer's job, invoked by the
orchestrator) and never generates recommendations.
"""

from __future__ import annotations

import pandas as pd

from config.settings import AnalysisConfig
from core.workflow.state import WorkflowState, log_stage
from models.anomaly import detect_anomalies
from models.forecasting import detect_trend, forecast_next_periods
from utils.column_mapper import detect_columns


def _top_and_low_margin_products(df: pd.DataFrame, columns: dict, threshold_pct: float) -> tuple[list, list]:
    product_col = columns.get("product")
    revenue_col = columns.get("revenue")
    profit_col = columns.get("profit")

    if not product_col or not revenue_col:
        return [], []

    value_col = profit_col or revenue_col
    grouped = (
        df.groupby(product_col)
        .agg(revenue=(revenue_col, "sum"), value=(value_col, "sum"))
        .reset_index()
    )
    grouped["margin_pct"] = (grouped["value"] / grouped["revenue"] * 100.0).where(grouped["revenue"] != 0, 0.0)

    top = grouped.sort_values("value", ascending=False).head(5)
    top_products = [
        {"name": str(row[product_col]), "value": round(float(row["value"]), 2)} for _, row in top.iterrows()
    ]

    low_margin = grouped[grouped["margin_pct"] < threshold_pct].sort_values("margin_pct").head(5)
    low_margin_products = [
        {
            "name": str(row[product_col]),
            "margin_pct": round(float(row["margin_pct"]), 2),
        }
        for _, row in low_margin.iterrows()
    ]

    return top_products, low_margin_products


def _time_ordered_revenue_series(df: pd.DataFrame, revenue_col: str, date_col: str | None) -> pd.Series:
    """Aggregate revenue by date when a date column is available so trend and
    forecast reflect business-period totals rather than individual
    transaction amounts."""
    if date_col:
        try:
            parsed_dates = pd.to_datetime(df[date_col])
            return df.assign(_date=parsed_dates).groupby("_date")[revenue_col].sum().sort_index()
        except (ValueError, TypeError):
            pass
    return df[revenue_col]


def run_analysis(state: WorkflowState, config: AnalysisConfig) -> WorkflowState:
    df = pd.read_csv(state["processed_dataset_path"])
    columns = detect_columns(df)
    revenue_col = columns.get("revenue")
    date_col = columns.get("date")

    insights: dict = {}

    if revenue_col:
        revenue_series = _time_ordered_revenue_series(df, revenue_col, date_col)
        insights["trend"] = detect_trend(revenue_series)
        insights["forecast"] = {
            "periods": config.forecast_periods,
            "values": forecast_next_periods(revenue_series, config.forecast_periods),
        }
        insights["anomalies"] = detect_anomalies(df, revenue_col, config.anomaly_contamination)
    else:
        insights["trend"] = {"direction": "unknown", "change_pct": 0.0}
        insights["forecast"] = {"periods": 0, "values": []}
        insights["anomalies"] = {"count": 0, "anomalous_value": 0.0, "row_indices": []}

    top_products, low_margin_products = _top_and_low_margin_products(
        df, columns, config.low_margin_threshold_pct
    )
    insights["top_products"] = top_products
    insights["low_margin_products"] = low_margin_products

    state["insights"] = insights
    log_stage(state, "Analysis Agent: trend, forecast, and anomaly analysis completed")
    return state
