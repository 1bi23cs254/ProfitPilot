"""
utils/column_mapper.py

Generic, dataset-agnostic column detection.

The mapper detects logical business fields from different dataset schemas
without hardcoding a particular dataset. Exact semantic matches are given
priority over broad substring matches so fields such as Product ID and
Product Name, or Country and Region, are not confused.
"""

from __future__ import annotations

import pandas as pd


_CANDIDATES: dict[str, list[str]] = {
    # Financial fields
    "revenue": [
        "revenue",
        "sales",
        "total_sales",
        "sales_amount",
        "amount",
    ],
    "cost": [
        "cost",
        "cogs",
        "cost_of_goods_sold",
        "expense",
        "expenses",
    ],
    "profit": [
        "profit",
        "net_profit",
        "netprofit",
    ],

    # Quantity
    "quantity": [
        "quantity",
        "qty",
        "units",
        "units_sold",
    ],

    # Product fields
    "product": [
        "product_name",
        "item_name",
        "item",
        "product",
    ],
    "product_id": [
        "product_id",
        "product_code",
        "sku",
        "item_id",
    ],

    # Customer fields
    "customer": [
        "customer_name",
        "customer",
        "client_name",
        "client",
    ],
    "customer_id": [
        "customer_id",
        "client_id",
    ],

    # Time fields
    "date": [
        "order_date",
        "transaction_date",
        "sale_date",
        "sales_date",
        "date",
        "period",
        "month",
        "year",
    ],

    # Geography
    "region": [
        "region",
    ],
    "country": [
        "country",
    ],
    "state": [
        "state",
        "province",
    ],
    "city": [
        "city",
        "town",
    ],

    # Classification
    "category": [
        "category",
    ],
    "sub_category": [
        "sub_category",
        "subcategory",
    ],
    "segment": [
        "segment",
    ],
}


def _normalize(name: str) -> str:
    """Normalize a column name for semantic comparison."""
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def _is_numeric_field(field: str) -> bool:
    """Return whether the logical field should contain numeric data."""
    return field in {
        "revenue",
        "cost",
        "profit",
        "quantity",
    }


def detect_columns(df: pd.DataFrame) -> dict[str, str | None]:
    """
    Return a mapping of logical field names to actual DataFrame columns.

    Matching priority:

    1. Exact normalized column match.
    2. Alias match.
    3. Controlled fallback substring match.

    Exact matches prevent Product ID from being selected as Product Name
    and prevent Country, State, or City from replacing Region.
    """

    normalized_lookup = {
        _normalize(column): column
        for column in df.columns
    }

    numeric_cols = set(
        df.select_dtypes(include="number").columns
    )

    detected: dict[str, str | None] = {}

    for field, candidates in _CANDIDATES.items():

        match = None

        # ---------------------------------------------
        # PRIORITY 1: EXACT MATCH
        # ---------------------------------------------

        for candidate in candidates:

            if candidate in normalized_lookup:

                original_name = normalized_lookup[candidate]

                if (
                    _is_numeric_field(field)
                    and original_name not in numeric_cols
                ):
                    continue

                match = original_name
                break

        # ---------------------------------------------
        # PRIORITY 2: CONTROLLED SUBSTRING FALLBACK
        # ---------------------------------------------

        if match is None:

            for candidate in candidates:

                for norm_name, original_name in normalized_lookup.items():

                    if candidate not in norm_name:
                        continue

                    if (
                        _is_numeric_field(field)
                        and original_name not in numeric_cols
                    ):
                        continue

                    match = original_name
                    break

                if match is not None:
                    break

        detected[field] = match

    return detected
