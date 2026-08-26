"""
Data Collector Agent.

Responsibilities:
- Load the raw dataset
- Validate structure and data quality
- Clean the data non-destructively

The cleaned dataset remains in memory and is passed through
WorkflowState. No intermediate CSV file is created.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from core.workflow.state import WorkflowState, log_error, log_stage
from utils.dataset_loader import load_dataset
from utils.validation import clean_dataframe, validate_dataframe


def _load_dataframe(dataset_source: str) -> pd.DataFrame:
    """
    Load a dataset from either:

    - kaggle://owner/dataset-slug
    - a local CSV path
    """

    if dataset_source.startswith("kaggle://"):
        return load_dataset(dataset_source)

    return pd.read_csv(Path(dataset_source))


def run_collector(state: WorkflowState) -> WorkflowState:
    dataset_source = state["dataset_path"]

    try:
        raw_df = _load_dataframe(dataset_source)

    except Exception as exc:
        log_error(
            state,
            f"Data Collector Agent: failed to load dataset "
            f"'{dataset_source}': {exc}",
        )
        raise

    report = validate_dataframe(raw_df)
    cleaned_df = clean_dataframe(raw_df)

    state["raw_row_count"] = report.row_count
    state["validation_summary"] = report.summary_lines()

    # Keep both datasets in memory.
    state["raw_dataframe"] = raw_df
    state["cleaned_dataframe"] = cleaned_df

    log_stage(
        state,
        f"Data Collector Agent: validated "
        f"{report.row_count} rows and {report.column_count} columns",
    )

    return state
