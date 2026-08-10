"""
core/orchestrator/graph.py

LangGraph Orchestrator (architecture.md 6.1 / Principle 3). This is the only
module allowed to invoke agents (Module Communication Rule 2); it never
performs business analysis or reasoning itself. It builds a StateGraph that
exactly matches the workflow defined in architecture.md Section 5 and
phases.md Phase 4:

    Planning -> Collector -> Processor -> Analysis -> RAG Retrieval ->
    Business Tactics (Reasoning + Recommendations) -> Report -> END
"""

from __future__ import annotations

from pathlib import Path

from langgraph.graph import END, StateGraph

from agents.analysis.agent import run_analysis
from agents.business_tactics.agent import run_business_tactics
from agents.collector.agent import run_collector
from agents.processor.agent import run_processor
from agents.report.agent import run_report
from config.settings import AppConfig
from core.planning.planner import run_planning
from core.workflow.state import WorkflowState, log_stage
from knowledge_base.rag.retriever import KnowledgeRetriever
from llm.reasoning_engine.base import ReasoningEngine
from utils.logger import get_logger


def build_workflow(
    config: AppConfig,
    reasoning_engine: ReasoningEngine,
    knowledge_retriever: KnowledgeRetriever,
):
    """Construct and compile the LangGraph StateGraph for one ProfitPilot run."""
    logger = get_logger("orchestrator", config.log_level, config.paths.logs_dir)
    graph = StateGraph(WorkflowState)

    def planning_node(state: WorkflowState) -> WorkflowState:
        logger.info("Stage: Planning")
        return run_planning(state, reasoning_engine)

    def collector_node(state: WorkflowState) -> WorkflowState:
        logger.info("Stage: Data Collector Agent")
        return run_collector(state, config.paths.data_cleaned)

    def processor_node(state: WorkflowState) -> WorkflowState:
        logger.info("Stage: Data Processing Agent")
        return run_processor(state, config.paths.data_processed)

    def analysis_node(state: WorkflowState) -> WorkflowState:
        logger.info("Stage: Analysis Agent")
        return run_analysis(state, config.analysis)

    def rag_node(state: WorkflowState) -> WorkflowState:
        logger.info("Stage: RAG Retrieval")
        query = f"{state['user_objective']} " + " ".join(state["execution_plan"].get("focus_areas", []))
        retrieved = knowledge_retriever.retrieve(query, top_k=config.rag.top_k)
        state["retrieved_knowledge"] = retrieved
        log_stage(state, f"RAG Retrieval Layer: {len(retrieved)} documents retrieved")
        return state

    def business_tactics_node(state: WorkflowState) -> WorkflowState:
        logger.info("Stage: Business Tactics Agent")
        return run_business_tactics(state, reasoning_engine)

    def report_node(state: WorkflowState) -> WorkflowState:
        logger.info("Stage: Report Generation Agent")
        return run_report(state, config.paths.reports_dir)

    graph.add_node("planning", planning_node)
    graph.add_node("collector", collector_node)
    graph.add_node("processor", processor_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("rag_retrieval", rag_node)
    graph.add_node("business_tactics", business_tactics_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("planning")
    graph.add_edge("planning", "collector")
    graph.add_edge("collector", "processor")
    graph.add_edge("processor", "analysis")
    graph.add_edge("analysis", "rag_retrieval")
    graph.add_edge("rag_retrieval", "business_tactics")
    graph.add_edge("business_tactics", "report")
    graph.add_edge("report", END)

    return graph.compile()
