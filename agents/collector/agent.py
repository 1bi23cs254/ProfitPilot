"""
agents/collector/agent.py

Data Collector Agent (architecture.md 6.2 / 7.4). Responsibilities:
  - Load the raw dataset
  - Validate structure and data quality
  - Clean the data (non-destructively) and persist the cleaned copy

This agent never performs KPI calculation, analysis, or reasoning
(Restricted Responsibilities, architecture.md 6.2).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from core.workflow.state import WorkflowState, log_error, log_stage
from utils.validation import clean_dataframe, validate_dataframe


def run_collector(state: WorkflowState, cleaned_dir: Path) -> WorkflowState:
    dataset_path = Path(state["dataset_path"])

    try:
        raw_df = pd.read_csv(dataset_path)
    except Exception as exc:  # noqa: BLE001 - surfaced to the terminal report, not swallowed
        log_error(state, f"Data Collector Agent: failed to read dataset '{dataset_path}': {exc}")
        raise

    report = validate_dataframe(raw_df)
    cleaned_df = clean_dataframe(raw_df)

    cleaned_path = cleaned_dir / f"{dataset_path.stem}_cleaned.csv"
    cleaned_df.to_csv(cleaned_path, index=False)

    state["raw_row_count"] = report.row_count
    state["validation_summary"] = report.summary_lines()
    state["cleaned_dataset_path"] = str(cleaned_path)

    log_stage(state, f"Data Collector Agent: validated {report.row_count} rows, cleaned dataset saved")
    return state
