"""
utils/logger.py

Generic logging helper shared across the project. Contains no business logic
(architecture.md 10. Directory Responsibilities -> utils/).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


def get_logger(name: str, log_level: str = "INFO", log_dir: Path | None = None) -> logging.Logger:
    """Return a configured logger that writes to stdout and, optionally, a file."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # avoid duplicate handlers on repeated calls

    logger.setLevel(log_level)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)-8s %(name)s: %(message)s", datefmt="%H:%M:%S")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "profitpilot.log", encoding="utf-8")
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger
