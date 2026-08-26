"""
models/anomaly.py

Anomaly detection model used internally by the Analysis Agent.

Isolation Forest identifies unusual business transactions based on selected
numeric business metrics. The model returns anomaly scores and row indices;
business context is added by the Analysis Agent.
"""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(
    df: pd.DataFrame,
    feature_columns: list[str],
    contamination: float,
    max_examples: int = 10,
) -> dict:
    """
    Detect anomalous business records.

    Returns:
        - total anomaly count
        - feature columns used
        - strongest anomaly row indices
        - anomaly scores

    Lower Isolation Forest scores indicate more unusual observations.
    """

    usable_columns = [
        column
        for column in feature_columns
        if column in df.columns
        and pd.api.types.is_numeric_dtype(df[column])
    ]

    if not usable_columns:
        return {
            "count": 0,
            "feature_columns": [],
            "examples": [],
        }

    feature_df = df[usable_columns].dropna()

    if len(feature_df) < 10:
        return {
            "count": 0,
            "feature_columns": usable_columns,
            "examples": [],
        }

    contamination = min(max(contamination, 0.01), 0.5)

    model = IsolationForest(
        contamination=contamination,
        random_state=42,
    )

    predictions = model.fit_predict(feature_df)

    anomaly_scores = model.decision_function(feature_df)

    results = pd.DataFrame(
        {
            "row_index": feature_df.index,
            "prediction": predictions,
            "anomaly_score": anomaly_scores,
        }
    )

    anomalous_rows = results[
        results["prediction"] == -1
    ].sort_values(
        "anomaly_score",
        ascending=True,
    )

    strongest_anomalies = anomalous_rows.head(
        max_examples
    )

    examples = [
        {
            "row_index": int(row["row_index"]),
            "anomaly_score": round(
                float(row["anomaly_score"]),
                6,
            ),
        }
        for _, row in strongest_anomalies.iterrows()
    ]

    return {
        "count": int(len(anomalous_rows)),
        "feature_columns": usable_columns,
        "examples": examples,
    }
