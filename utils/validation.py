"""
utils/validation.py

Generic, dataset-agnostic validation helpers. Business-specific rules must
not be implemented here (rules.md Rule 6) — this module only detects
structural data-quality issues (missing values, duplicates, schema shape).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class ValidationReport:
    row_count: int
    column_count: int
    missing_value_columns: dict[str, int] = field(default_factory=dict)
    duplicate_row_count: int = 0
    issues: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return not self.issues

    def summary_lines(self) -> list[str]:
        lines = [f"Rows: {self.row_count} | Columns: {self.column_count}"]
        if self.missing_value_columns:
            missing = ", ".join(f"{c} ({n})" for c, n in self.missing_value_columns.items())
            lines.append(f"Missing values found in: {missing}")
        else:
            lines.append("No missing values detected")
        lines.append(f"Duplicate rows: {self.duplicate_row_count}")
        return lines


def validate_dataframe(df: pd.DataFrame, required_columns: list[str] | None = None) -> ValidationReport:
    """Run structural validation on a raw business dataset."""
    issues: list[str] = []

    missing_counts = {c: int(n) for c, n in df.isnull().sum().items() if n > 0}
    duplicate_count = int(df.duplicated().sum())

    if required_columns:
        missing_cols = [c for c in required_columns if c not in df.columns]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")

    if df.empty:
        issues.append("Dataset contains no rows")

    return ValidationReport(
        row_count=len(df),
        column_count=len(df.columns),
        missing_value_columns=missing_counts,
        duplicate_row_count=duplicate_count,
        issues=issues,
    )


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply generic, non-destructive cleaning: drop exact duplicates and
    forward/backward fill missing numeric values so downstream KPI math does
    not break on NaNs."""
    cleaned = df.drop_duplicates().copy()
    numeric_cols = cleaned.select_dtypes(include="number").columns
    cleaned[numeric_cols] = cleaned[numeric_cols].ffill().bfill()
    cleaned = cleaned.dropna(axis=0, how="all")
    return cleaned.reset_index(drop=True)
