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


def _top_and_low_margin_products(
    df: pd.DataFrame,
    columns: dict,
    threshold_pct: float,
) -> tuple[list, list]:

    product_col = columns.get("product")
    revenue_col = columns.get("revenue")
    profit_col = columns.get("profit")

    if not product_col or not revenue_col:
        return [], []

    value_col = profit_col or revenue_col

    grouped = (
        df.groupby(product_col)
        .agg(
            revenue=(revenue_col, "sum"),
            value=(value_col, "sum"),
        )
        .reset_index()
    )

    grouped["margin_pct"] = (
        grouped["value"] / grouped["revenue"] * 100.0
    ).where(
        grouped["revenue"] != 0,
        0.0,
    )

    top = (
        grouped
        .sort_values("value", ascending=False)
        .head(5)
    )

    top_products = [
        {
            "name": str(row[product_col]),
            "value": round(float(row["value"]), 2),
        }
        for _, row in top.iterrows()
    ]

    low_margin = (
        grouped[
            grouped["margin_pct"] < threshold_pct
        ]
        .sort_values("margin_pct")
        .head(5)
    )

    low_margin_products = [
        {
            "name": str(row[product_col]),
            "margin_pct": round(
                float(row["margin_pct"]),
                2,
            ),
        }
        for _, row in low_margin.iterrows()
    ]

    return top_products, low_margin_products


def _time_ordered_revenue_series(
    df: pd.DataFrame,
    revenue_col: str,
    date_col: str | None,
) -> pd.Series:
    """
    Create a business-friendly monthly revenue time series.

    Transaction-level datasets can contain many rows per day, so revenue
    is aggregated by month before trend detection and forecasting.
    """

    if not date_col:
        return df[revenue_col]

    try:
        parsed_dates = pd.to_datetime(
            df[date_col],
            errors="coerce",
        )

        time_df = pd.DataFrame(
            {
                "date": parsed_dates,
                "revenue": df[revenue_col],
            }
        ).dropna()

        if time_df.empty:
            return df[revenue_col]

        monthly_revenue = (
            time_df
            .groupby(
                time_df["date"].dt.to_period("M")
            )["revenue"]
            .sum()
            .sort_index()
        )

        return monthly_revenue

    except (ValueError, TypeError):
        return df[revenue_col]


def _get_anomaly_features(
    df: pd.DataFrame,
    columns: dict,
) -> list[str]:
    """
    Select meaningful numeric business metrics for anomaly detection.

    Identifiers such as Row ID, Product ID, Customer ID, and location
    codes such as Postal Code are intentionally excluded.
    """

    candidate_columns = [
        columns.get("revenue"),
        columns.get("profit"),
        columns.get("quantity"),
    ]

    # Detect discount generically if present.
    discount_col = next(
        (
            column
            for column in df.columns
            if column.strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            == "discount"
        ),
        None,
    )

    if discount_col:
        candidate_columns.append(discount_col)

    return [
        column
        for column in candidate_columns
        if column is not None
        and column in df.columns
        and pd.api.types.is_numeric_dtype(df[column])
    ]


def _enrich_anomalies(
    df: pd.DataFrame,
    anomaly_result: dict,
    columns: dict,
) -> dict:
    """
    Convert raw anomaly row indices into business-readable anomaly insights.

    The anomaly model identifies unusual records numerically. This function
    adds contextual information such as product, customer, sales, profit,
    quantity, discount, and location.
    """

    product_col = columns.get("product")
    customer_col = columns.get("customer")
    revenue_col = columns.get("revenue")
    profit_col = columns.get("profit")
    quantity_col = columns.get("quantity")
    region_col = columns.get("region")
    category_col = columns.get("category")
    sub_category_col = columns.get("sub_category")

    # Detect discount generically.
    discount_col = next(
        (
            column
            for column in df.columns
            if column.strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            == "discount"
        ),
        None,
    )

    enriched_examples = []

    for anomaly in anomaly_result.get("examples", []):

        row_index = anomaly["row_index"]

        if row_index not in df.index:
            continue

        row = df.loc[row_index]

        example = {
            "anomaly_score": anomaly["anomaly_score"],
        }

        if product_col:
            example["product"] = str(row[product_col])

        if customer_col:
            example["customer"] = str(row[customer_col])

        if revenue_col:
            example["sales"] = round(
                float(row[revenue_col]),
                2,
            )

        if profit_col:
            example["profit"] = round(
                float(row[profit_col]),
                2,
            )

        if quantity_col:
            example["quantity"] = int(
                row[quantity_col]
            )

        if discount_col:
            example["discount"] = round(
                float(row[discount_col]),
                4,
            )

        if region_col:
            example["region"] = str(
                row[region_col]
            )

        if category_col:
            example["category"] = str(
                row[category_col]
            )

        if sub_category_col:
            example["sub_category"] = str(
                row[sub_category_col]
            )

        enriched_examples.append(example)

    return {
        "count": anomaly_result.get("count", 0),
        "feature_columns": anomaly_result.get(
            "feature_columns",
            [],
        ),
        "examples": enriched_examples,
    }


def run_analysis(
    state: WorkflowState,
    config: AnalysisConfig,
) -> WorkflowState:

    df = state["processed_dataframe"].copy()

    columns = detect_columns(df)

    revenue_col = columns.get("revenue")
    date_col = columns.get("date")

    insights: dict = {}

    if revenue_col:

        # --------------------------------------------------
        # TREND AND FORECASTING
        # --------------------------------------------------

        revenue_series = _time_ordered_revenue_series(
            df,
            revenue_col,
            date_col,
        )

        insights["trend"] = detect_trend(
            revenue_series
        )

        insights["forecast"] = {
            "periods": config.forecast_periods,
            "values": forecast_next_periods(
                revenue_series,
                config.forecast_periods,
            ),
        }

        # --------------------------------------------------
        # ANOMALY DETECTION
        # --------------------------------------------------

        anomaly_features = _get_anomaly_features(
            df,
            columns,
        )

        raw_anomalies = detect_anomalies(
            df,
            anomaly_features,
            config.anomaly_contamination,
            max_examples=10,
        )

        insights["anomalies"] = _enrich_anomalies(
            df,
            raw_anomalies,
            columns,
        )

    else:

        insights["trend"] = {
            "direction": "unknown",
            "change_pct": 0.0,
            "slope": 0.0,
        }

        insights["forecast"] = {
            "periods": 0,
            "values": [],
        }

        insights["anomalies"] = {
            "count": 0,
            "feature_columns": [],
            "row_indices": [],
        }

    # --------------------------------------------------
    # PRODUCT PERFORMANCE ANALYSIS
    # --------------------------------------------------

    top_products, low_margin_products = (
        _top_and_low_margin_products(
            df,
            columns,
            config.low_margin_threshold_pct,
        )
    )

    insights["top_products"] = top_products
    insights["low_margin_products"] = low_margin_products

    state["insights"] = insights

    log_stage(
        state,
        "Analysis Agent: trend, forecast, product performance, "
        "and anomaly analysis completed",
    )

    return state
