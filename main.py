"""
main.py

ProfitPilot Version 1 terminal entrypoint (architecture.md Principle 1 -
Single Prompt Execution / Principle 8 - Terminal-First Development).

Usage:
    python main.py \
        --dataset "kaggle://vivek468/superstore-dataset-final" \
        --objective "Analyze my sales data and tell me how to maximize profit."

    python main.py \
        --dataset "kaggle://vivek468/superstore-dataset-final"
"""

from __future__ import annotations

import argparse
import sys
import uuid
from datetime import datetime

from config.settings import settings
from core.orchestrator.graph import build_workflow
from core.workflow.state import new_state
from database.db import Database
from knowledge_base.rag.retriever import KnowledgeRetriever
from knowledge_base.vector_store.factory import build_vector_store
from llm.reasoning_engine.factory import build_reasoning_engine
from utils.formatting import banner, check, section
from utils.logger import get_logger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ProfitPilot - Autonomous AI System for Profit Management"
    )

    parser.add_argument(
        "--dataset",
        required=True,
        help="Dataset source: local CSV path or kaggle://owner/dataset-slug",
    )

    parser.add_argument(
        "--objective",
        default=None,
        help="Natural-language business objective",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings.paths.ensure()
    logger = get_logger("main", settings.log_level, settings.paths.logs_dir)

    objective = args.objective or input(
        "Enter your business objective: ").strip()
    if not objective:
        logger.error("A business objective is required.")
        return 1

    run_id = uuid.uuid4().hex[:12]
    db = Database(settings.paths.database_file)
    db.start_run(run_id, objective, args.dataset,
                 datetime.now().isoformat(timespec="seconds"))

    print(banner("ProfitPilot Version 1"))
    print(f"User Objective Received: {objective}")

    try:
        reasoning_engine = build_reasoning_engine(settings.reasoning)
        vector_store = build_vector_store(
            settings.rag, str(settings.paths.vector_store))
        retriever = KnowledgeRetriever(
            vector_store, settings.paths.knowledge_documents)
        doc_count = retriever.prepare()
        logger.info(f"Knowledge base prepared with {doc_count} documents "
                    f"(backend={settings.rag.backend}, reasoning={settings.reasoning.backend})")

        workflow = build_workflow(settings, reasoning_engine, retriever)
        state = new_state(objective, args.dataset, run_id)

        final_state = workflow.invoke(state)

        print(section("Validation Summary"))
        for line in final_state.get("validation_summary", []):
            print(f"  {line}")

        print(final_state["report_text"])

        db.save_kpis(run_id, final_state.get("kpis", {}))
        db.save_recommendations(run_id, final_state.get("recommendations", []))
        status = "completed_with_warnings" if final_state.get(
            "errors") else "success"
        db.complete_run(run_id, datetime.now().isoformat(
            timespec="seconds"), status)

        print(banner("ProfitPilot Version 1 Completed Successfully"))
        print(f"Report saved to: {final_state['report_path']}")
        return 0

    except Exception as exc:  # noqa: BLE001 - top-level fail-clearly boundary (rules.md Rule 13)
        logger.error(f"Workflow failed: {exc}")
        db.complete_run(run_id, datetime.now().isoformat(
            timespec="seconds"), "failed")
        print(f"\nProfitPilot encountered an error and stopped: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
