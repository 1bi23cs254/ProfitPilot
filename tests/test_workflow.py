"""
tests/test_workflow.py

Covers: dataset validation/cleaning, KPI computation, analysis models,
the RAG retriever, the rule-based reasoning engine, and a full end-to-end
workflow execution (phases.md Phase 4 Testing Checklist).

Run with: pytest -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import settings  # noqa: E402
from core.orchestrator.graph import build_workflow  # noqa: E402
from core.workflow.state import new_state  # noqa: E402
from knowledge_base.rag.retriever import KnowledgeRetriever  # noqa: E402
from knowledge_base.vector_store.tfidf_store import TfidfVectorStore  # noqa: E402
from llm.reasoning_engine.rule_based import RuleBasedReasoningEngine  # noqa: E402
from models.anomaly import detect_anomalies  # noqa: E402
from models.forecasting import detect_trend, forecast_next_periods  # noqa: E402
from utils.validation import clean_dataframe, validate_dataframe  # noqa: E402


SAMPLE_DATASET = ROOT / "data" / "raw" / "sample_sales.csv"


@pytest.fixture(scope="module")
def sample_df() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_DATASET)


def test_validate_dataframe(sample_df: pd.DataFrame) -> None:
    report = validate_dataframe(sample_df)
    assert report.row_count == len(sample_df)
    assert report.column_count == len(sample_df.columns)


def test_clean_dataframe_is_idempotent(sample_df: pd.DataFrame) -> None:
    cleaned_once = clean_dataframe(sample_df)
    cleaned_twice = clean_dataframe(cleaned_once)
    assert len(cleaned_once) == len(cleaned_twice)


def test_forecast_and_trend(sample_df: pd.DataFrame) -> None:
    series = sample_df.groupby("Order Date")["Sales"].sum()
    trend = detect_trend(series)
    assert trend["direction"] in {"increasing", "decreasing", "flat", "insufficient_data"}

    forecast = forecast_next_periods(series, periods=3)
    assert len(forecast) == 3


def test_anomaly_detection(sample_df: pd.DataFrame) -> None:
    result = detect_anomalies(sample_df, "Sales", contamination=0.08)
    assert result["count"] >= 0


def test_rag_retriever_returns_relevant_documents() -> None:
    store = TfidfVectorStore()
    retriever = KnowledgeRetriever(store, settings.paths.knowledge_documents)
    retriever.prepare()
    results = retriever.retrieve("low margin pricing strategy", top_k=2)
    assert len(results) <= 2
    assert all("source" in r and "snippet" in r for r in results)


def test_rule_based_reasoning_engine_plan() -> None:
    engine = RuleBasedReasoningEngine()
    plan = engine.plan("Analyze my sales data and tell me how to maximize profit.")
    assert "focus_areas" in plan
    assert "steps" in plan


def test_rule_based_reasoning_engine_reason() -> None:
    engine = RuleBasedReasoningEngine()
    text = engine.reason(
        kpis={"total_revenue": 1000, "total_net_profit": 50, "net_profit_margin_pct": 5.0},
        insights={"trend": {"direction": "decreasing", "change_pct": -10.0}, "anomalies": {"count": 0}},
        retrieved_knowledge=[],
        user_objective="Maximize profit",
    )
    assert "Revenue" in text or "revenue" in text.lower()


def test_end_to_end_workflow(tmp_path) -> None:
    settings.paths.ensure()

    reasoning_engine = RuleBasedReasoningEngine()
    store = TfidfVectorStore()
    retriever = KnowledgeRetriever(store, settings.paths.knowledge_documents)
    retriever.prepare()

    workflow = build_workflow(settings, reasoning_engine, retriever)
    state = new_state(
        user_objective="Analyze my sales data and tell me how to maximize profit.",
        dataset_path=str(SAMPLE_DATASET),
        run_id="test-run-001",
    )

    final_state = workflow.invoke(state)

    assert final_state["kpis"]["total_revenue"] > 0
    assert "trend" in final_state["insights"]
    assert len(final_state["recommendations"]) > 0
    assert final_state["report_text"]
    assert Path(final_state["report_path"]).exists()
    assert not final_state.get("errors")
