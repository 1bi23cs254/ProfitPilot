"""
models/forecasting.py

Machine learning model used by the Analysis Agent for trend detection and
forecasting (architecture.md 10. models/ directory — "does not contain the
Large Language Model"). Uses a simple linear regression over a time-ordered
revenue series: fast, dependency-light (scikit-learn only), and adequate for
the short, often-noisy series found in typical Kaggle business datasets.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def detect_trend(series: pd.Series) -> dict:
    """Fit a linear trend to a time-ordered numeric series and summarize direction/strength."""
    values = series.dropna().to_numpy(dtype=float)
    if len(values) < 2:
        return {"direction": "insufficient_data", "change_pct": 0.0, "slope": 0.0}

    x = np.arange(len(values)).reshape(-1, 1)
    model = LinearRegression().fit(x, values)
    slope = float(model.coef_[0])

    start_value = values[0] if values[0] != 0 else 1e-9
    predicted_end = model.predict([[len(values) - 1]])[0]
    change_pct = ((predicted_end - values[0]) / abs(start_value)) * 100.0

    direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "flat"
    return {"direction": direction, "change_pct": round(float(change_pct), 2), "slope": round(slope, 4)}


def forecast_next_periods(series: pd.Series, periods: int) -> list[float]:
    """Extrapolate the fitted linear trend `periods` steps into the future."""
    values = series.dropna().to_numpy(dtype=float)
    if len(values) < 2:
        last = float(values[-1]) if len(values) else 0.0
        return [round(last, 2)] * periods

    x = np.arange(len(values)).reshape(-1, 1)
    model = LinearRegression().fit(x, values)
    future_x = np.arange(len(values), len(values) + periods).reshape(-1, 1)
    predictions = model.predict(future_x)
    return [round(float(v), 2) for v in predictions]
