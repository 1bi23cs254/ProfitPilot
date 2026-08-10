"""
utils/column_mapper.py

Generic, dataset-agnostic column detection. ProfitPilot must operate on
different Kaggle business datasets without being rewritten per schema
(prd.md Assumptions), so KPI and analysis code never hardcodes a column
name — it asks this module to find the best-matching column by keyword and
dtype. No business logic lives here, only column-shape detection.
"""

from __future__ import annotations

import pandas as pd

_CANDIDATES: dict[str, list[str]] = {
    "revenue": ["revenue", "sales", "total_sales", "amount", "total"],
    "cost": ["cost", "cogs", "expense", "expenses"],
    "profit": ["profit", "net_profit", "netprofit"],
    "quantity": ["quantity", "qty", "units", "units_sold"],
    "product": ["product", "item", "sku", "product_name"],
    "date": ["date", "order_date", "month", "year", "period"],
    "region": ["region", "state", "country", "city"],
    "category": ["category", "segment", "sub_category", "subcategory"],
}


def _normalize(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def detect_columns(df: pd.DataFrame) -> dict[str, str | None]:
    """Return a mapping of logical field name -> actual dataframe column name
    (or None if no match was found)."""
    normalized_lookup = {_normalize(col): col for col in df.columns}
    numeric_cols = set(df.select_dtypes(include="number").columns)

    detected: dict[str, str | None] = {}
    for field, keywords in _CANDIDATES.items():
        match = None
        for norm_name, original_name in normalized_lookup.items():
            if any(keyword in norm_name for keyword in keywords):
                if field in {"revenue", "cost", "profit", "quantity"} and original_name not in numeric_cols:
                    continue
                match = original_name
                break
        detected[field] = match
    return detected
