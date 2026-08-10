"""
agents/report/agent.py

Report Generation Agent (architecture.md 6.8 / 7.10). Read-only: it never
modifies business data (Module Communication Rule 5) and never generates new
business knowledge (phases.md Phase 4). It only organizes and presents the
outputs already produced by the rest of the workflow.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from core.workflow.state import WorkflowState, log_stage
from utils.formatting import bullet_list, currency, percent, section


def _build_report_text(state: WorkflowState) -> str:
    kpis = state.get("kpis", {})
    insights = state.get("insights", {})
    recommendations = state.get("recommendations", [])

    lines = [f"ProfitPilot Business Report", f"Generated: {datetime.now().isoformat(timespec='seconds')}"]
    lines.append(f"Objective: {state['user_objective']}")
    lines.append(f"Dataset: {Path(state['dataset_path']).name}")

    lines.append(section("Business KPIs"))
    lines.append(f"Total Revenue:      {currency(kpis.get('total_revenue', 0))}")
    lines.append(f"Total Cost:         {currency(kpis.get('total_cost', 0))}")
    lines.append(f"Gross Profit:       {currency(kpis.get('gross_profit', 0))}")
    lines.append(f"Net Profit:         {currency(kpis.get('total_net_profit', 0))}")
    lines.append(f"Net Profit Margin:  {percent(kpis.get('net_profit_margin_pct', 0))}")
    lines.append(f"ROI:                {percent(kpis.get('roi_pct', 0))}")

    lines.append(section("Analytical Findings"))
    trend = insights.get("trend", {})
    lines.append(f"Revenue Trend: {trend.get('direction', 'unknown')} ({trend.get('change_pct', 0)}% change)")
    forecast = insights.get("forecast", {})
    if forecast.get("values"):
        lines.append(f"Forecast (next {forecast.get('periods')} periods): {forecast.get('values')}")
    anomalies = insights.get("anomalies", {})
    lines.append(f"Anomalies Detected: {anomalies.get('count', 0)} (value: {currency(anomalies.get('anomalous_value', 0))})")
    if insights.get("top_products"):
        lines.append("Top Contributing Products:")
        lines.append(bullet_list([f"{p['name']} ({currency(p['value'])})" for p in insights["top_products"]]))
    if insights.get("low_margin_products"):
        lines.append("Low-Margin Products:")
        lines.append(bullet_list([f"{p['name']} ({percent(p['margin_pct'])} margin)" for p in insights["low_margin_products"]]))

    lines.append(section("Retrieved Business Knowledge"))
    for doc in state.get("retrieved_knowledge", []):
        lines.append(f"  [{doc['source']}] (relevance {doc['score']:.2f}): {doc['snippet']}")

    lines.append(section("Business Reasoning"))
    lines.append(state.get("business_reasoning", ""))

    lines.append(section("Recommendations"))
    for i, rec in enumerate(recommendations, start=1):
        lines.append(f"{i}. [{rec['category'].upper()}] {rec['recommendation']}")
        lines.append(f"   Evidence: {rec['evidence']}")
        lines.append(f"   Confidence: {rec['confidence_score']:.2f} | Expected Impact: {rec['expected_impact']}")

    lines.append(section("Workflow Summary"))
    lines.append(f"Status: {'SUCCESS' if not state.get('errors') else 'COMPLETED WITH WARNINGS'}")
    lines.append(f"Stages Completed: {len(state.get('stage_log', []))}")

    return "\n".join(str(line) for line in lines)


def run_report(state: WorkflowState, reports_dir: Path) -> WorkflowState:
    report_text = _build_report_text(state)
    report_path = reports_dir / f"{state['run_id']}_report.txt"
    report_path.write_text(report_text, encoding="utf-8")

    state["report_text"] = report_text
    state["report_path"] = str(report_path)

    log_stage(state, "Report Generation Agent: report generated")
    return state
