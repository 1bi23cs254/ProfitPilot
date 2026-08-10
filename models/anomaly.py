"""
models/anomaly.py

Anomaly detection model used by the Analysis Agent. Uses scikit-learn's
IsolationForest, listed in memory.md as one of the algorithms explored for
ProfitPilot, over the numeric feature columns of the processed dataset.
"""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df: pd.DataFrame, value_column: str, contamination: float) -> dict:
    numeric_df = df.select_dtypes(include="number").dropna()
    if len(numeric_df) < 10 or value_column not in numeric_df.columns:
        return {"count": 0, "anomalous_value": 0.0, "row_indices": []}

    contamination = min(max(contamination, 0.01), 0.5)
    model = IsolationForest(contamination=contamination, random_state=42)
    predictions = model.fit_predict(numeric_df)

    anomaly_mask = predictions == -1
    anomalous_rows = numeric_df[anomaly_mask]

    return {
        "count": int(anomaly_mask.sum()),
        "anomalous_value": round(float(anomalous_rows[value_column].sum()), 2) if len(anomalous_rows) else 0.0,
        "row_indices": anomalous_rows.index.tolist()[:20],
    }
