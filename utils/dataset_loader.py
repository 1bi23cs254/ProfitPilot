"""
utils/dataset_loader.py

Loads datasets directly into memory.

Supported source format:
    kaggle://owner/dataset-slug

The remote dataset is never permanently written to disk.
"""

from __future__ import annotations

import io
import os
import zipfile

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()


class DatasetLoadError(RuntimeError):
    """Raised when a dataset cannot be fetched or parsed."""


def load_kaggle_dataset(source: str) -> pd.DataFrame:
    """
    Fetch a Kaggle dataset into memory and return its CSV as a DataFrame.

    Example:
        kaggle://vivek468/superstore-dataset-final
    """

    dataset_ref = source.removeprefix("kaggle://")

    if "/" not in dataset_ref:
        raise DatasetLoadError(
            "Invalid Kaggle dataset source.\n"
            "Expected format:\n"
            "kaggle://owner/dataset-slug"
        )

    username = os.getenv("KAGGLE_USERNAME")
    api_key = os.getenv("KAGGLE_KEY")

    if not username or not api_key:
        raise DatasetLoadError(
            "Kaggle credentials are missing. "
            "Set KAGGLE_USERNAME and KAGGLE_KEY in .env"
        )

    url = (
        "https://www.kaggle.com/api/v1/"
        f"datasets/download/{dataset_ref}"
    )

    try:
        response = requests.get(
            url,
            auth=(username, api_key),
            timeout=120,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        raise DatasetLoadError(
            f"Failed to fetch Kaggle dataset: {exc}"
        ) from exc

    dataset_bytes = io.BytesIO(response.content)

    if not zipfile.is_zipfile(dataset_bytes):
        raise DatasetLoadError(
            "Expected Kaggle to return a ZIP dataset archive."
        )

    with zipfile.ZipFile(dataset_bytes) as archive:

        csv_files = [
            name
            for name in archive.namelist()
            if name.lower().endswith(".csv")
            and not name.startswith("__MACOSX/")
        ]

        if not csv_files:
            raise DatasetLoadError(
                "No CSV file found inside the Kaggle dataset."
            )

        # For this dataset there should be one main CSV.
        csv_name = csv_files[0]
        with archive.open(csv_name) as csv_file:
            try:
                df = pd.read_csv(csv_file, encoding="utf-8")

            except UnicodeDecodeError:
                csv_file.seek(0)
                df = pd.read_csv(csv_file, encoding="latin1")

    return df


def load_dataset(source: str) -> pd.DataFrame:
    """
    Load a supported dataset source into memory.
    """

    if source.startswith("kaggle://"):
        return load_kaggle_dataset(source)

    raise DatasetLoadError(
        f"Unsupported dataset source: {source}"
    )
