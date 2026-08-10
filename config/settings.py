"""
config/settings.py

Central configuration for ProfitPilot.

Per rules.md Rule 12 ("Configuration Must Remain External"), no other module
may hardcode paths, model names, thresholds, or credentials. Everything here
is overridable through environment variables (see .env.example).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent


def _env_bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float) -> float:
    val = os.getenv(name)
    return float(val) if val else default


def _env_int(name: str, default: int) -> int:
    val = os.getenv(name)
    return int(val) if val else default


@dataclass(frozen=True)
class PathsConfig:
    root: Path = ROOT_DIR
    data_raw: Path = ROOT_DIR / "data" / "raw"
    data_cleaned: Path = ROOT_DIR / "data" / "cleaned"
    data_processed: Path = ROOT_DIR / "data" / "processed"
    data_outputs: Path = ROOT_DIR / "data" / "outputs"
    knowledge_documents: Path = ROOT_DIR / "knowledge_base" / "documents"
    vector_store: Path = ROOT_DIR / "knowledge_base" / "vector_store" / "index"
    database_file: Path = ROOT_DIR / "database" / "profitpilot.db"
    reports_dir: Path = ROOT_DIR / "reports"
    logs_dir: Path = ROOT_DIR / "logs"

    def ensure(self) -> None:
        """Create every managed directory if it does not already exist."""
        for value in (
            self.data_raw,
            self.data_cleaned,
            self.data_processed,
            self.data_outputs,
            self.knowledge_documents,
            self.vector_store.parent,
            self.database_file.parent,
            self.reports_dir,
            self.logs_dir,
        ):
            value.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class ReasoningEngineConfig:
    # "rule_based" requires no external service and no API key — this is the
    # default so the system is deployable out of the box (see llm/README.md).
    # "anthropic" and "huggingface_local" are drop-in replacements; swapping
    # this value is the only change required (architecture.md Principle 6 —
    # Loose Coupling / Replaceable Components).
    backend: str = field(
        default_factory=lambda: os.getenv(
            "REASONING_ENGINE_BACKEND",
            "rule_based",
        )
    )

    model_name: str = field(
        default_factory=lambda: os.getenv(
            "REASONING_ENGINE_MODEL",
            "deepanalyze-8b",
        )
    )

    deepanalyze_base_url: str = field(
        default_factory=lambda: os.getenv(
            "DEEPANALYZE_BASE_URL",
            "http://127.0.0.1:8080/v1",
        )
    )

    anthropic_model: str = field(
        default_factory=lambda: os.getenv(
            "ANTHROPIC_MODEL",
            "claude-sonnet-4-6",
        )
    )

    anthropic_api_key: str = field(
        default_factory=lambda: os.getenv(
            "ANTHROPIC_API_KEY",
            "",
        )
    )

    max_tokens: int = field(
        default_factory=lambda: _env_int(
            "REASONING_MAX_TOKENS",
            1200,
        )
    )

    temperature: float = field(
        default_factory=lambda: _env_float(
            "REASONING_TEMPERATURE",
            0.2,
        )
    )

@dataclass(frozen=True)
class RAGConfig:
    top_k: int = field(default_factory=lambda: _env_int("RAG_TOP_K", 4))
    # "tfidf" ships zero-download, fully offline retrieval so the project runs
    # immediately after `pip install -r requirements.txt`. "chromadb" is the
    # architecturally-specified production backend (architecture.md ADR-006 /
    # Section 11) and can be enabled once embedding-model downloads are
    # acceptable in the deployment environment.
    backend: str = field(default_factory=lambda: os.getenv("VECTOR_STORE_BACKEND", "tfidf"))


@dataclass(frozen=True)
class AnalysisConfig:
    anomaly_contamination: float = field(default_factory=lambda: _env_float("ANOMALY_CONTAMINATION", 0.08))
    forecast_periods: int = field(default_factory=lambda: _env_int("FORECAST_PERIODS", 6))
    low_margin_threshold_pct: float = field(default_factory=lambda: _env_float("LOW_MARGIN_THRESHOLD_PCT", 10.0))
    slow_moving_stock_days: int = field(default_factory=lambda: _env_int("SLOW_MOVING_STOCK_DAYS", 60))


@dataclass(frozen=True)
class AppConfig:
    paths: PathsConfig = field(default_factory=PathsConfig)
    reasoning: ReasoningEngineConfig = field(default_factory=ReasoningEngineConfig)
    rag: RAGConfig = field(default_factory=RAGConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    verbose_terminal: bool = field(default_factory=lambda: _env_bool("VERBOSE_TERMINAL", True))


settings = AppConfig()
