"""
Machine learning utilities used internally by the Analysis Agent.

Uses Linear Regression over a time-ordered business metric series for
trend detection and short-term forecasting.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def detect_trend(series: pd.Series) -> dict:
    """
    Fit a linear trend to a time-ordered numeric series.

    change_pct represents the estimated change from the fitted trend at
    the beginning of the observed period to the fitted trend at the end.
    """

    values = series.dropna().to_numpy(dtype=float)

    if len(values) < 2:
        return {
            "direction": "insufficient_data",
            "change_pct": 0.0,
            "slope": 0.0,
        }

    x = np.arange(len(values)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, values)

    slope = float(model.coef_[0])

    fitted_start = float(
        model.predict([[0]])[0]
    )

    fitted_end = float(
        model.predict(
            [[len(values) - 1]]
        )[0]
    )

    if abs(fitted_start) < 1e-9:
        change_pct = 0.0
    else:
        change_pct = (
            (fitted_end - fitted_start)
            / abs(fitted_start)
        ) * 100.0

    direction = (
        "increasing"
        if slope > 0
        else "decreasing"
        if slope < 0
        else "flat"
    )

    return {
        "direction": direction,
        "change_pct": round(
            float(change_pct),
            2,
        ),
        "slope": round(
            slope,
            4,
        ),
    }


def forecast_next_periods(
    series: pd.Series,
    periods: int,
) -> list[float]:
    """
    Forecast the next business periods using the fitted linear trend.
    """

    values = series.dropna().to_numpy(dtype=float)

    if len(values) < 2:
        last = (
            float(values[-1])
            if len(values)
            else 0.0
        )

        return [
            round(last, 2)
            for _ in range(periods)
        ]

    x = np.arange(
        len(values)
    ).reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, values)

    future_x = np.arange(
        len(values),
        len(values) + periods,
    ).reshape(-1, 1)

    predictions = model.predict(
        future_x
    )

    return [
        round(float(value), 2)
        for value in predictions
    ]
