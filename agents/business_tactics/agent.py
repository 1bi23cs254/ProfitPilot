"""
agents/business_tactics/agent.py

Business Tactics Agent (architecture.md 6.7 / 7.9). Invokes the Autonomous
Reasoning Engine's Business Reasoning mode, then transforms that reasoning
plus KPIs/insights/retrieved knowledge into concrete, explainable
recommendations (FR-6: pricing, inventory, marketing, cost). Every
recommendation includes an explanation, supporting evidence, a confidence
score, and expected impact (architecture.md 6.7 "Every recommendation should
include"). ADR-009: recommendations are the consequence of reasoning, not a
substitute for it — reasoning is always generated first.
"""

from __future__ import annotations

from typing import Any

from core.workflow.state import WorkflowState, log_stage
from llm.reasoning_engine.base import ReasoningEngine


def _pricing_recommendations(insights: dict, kpis: dict) -> list[dict[str, Any]]:
    recs = []
    low_margin = insights.get("low_margin_products", [])
    if low_margin:
        names = ", ".join(p["name"] for p in low_margin[:3])
        recs.append(
            {
                "category": "pricing",
                "recommendation": (
                    f"Review and increase pricing for low-margin products ({names}), or negotiate "
                    "lower input costs, since these products are eroding overall profitability."
                ),
                "evidence": f"{len(low_margin)} products identified below the acceptable margin threshold.",
                "confidence_score": 0.8,
                "expected_impact": "Improved net profit margin without a proportional loss in revenue.",
            }
        )
    elif kpis.get("net_profit_margin_pct", 0) < 10:
        recs.append(
            {
                "category": "pricing",
                "recommendation": "Conduct a business-wide pricing review; overall net margin is thin.",
                "evidence": f"Net profit margin is {kpis.get('net_profit_margin_pct', 0)}%.",
                "confidence_score": 0.65,
                "expected_impact": "Higher margin per unit sold across the product portfolio.",
            }
        )
    return recs


def _inventory_recommendations(insights: dict) -> list[dict[str, Any]]:
    recs = []
    low_margin = insights.get("low_margin_products", [])
    if low_margin:
        names = ", ".join(p["name"] for p in low_margin[:3])
        recs.append(
            {
                "category": "inventory",
                "recommendation": f"Reduce reorder volume or liquidate slow/low-margin stock for: {names}.",
                "evidence": "These SKUs show margin performance below the configured threshold.",
                "confidence_score": 0.6,
                "expected_impact": "Reduced holding cost and freed-up working capital.",
            }
        )
    return recs


def _marketing_recommendations(insights: dict) -> list[dict[str, Any]]:
    recs = []
    top_products = insights.get("top_products", [])
    trend = insights.get("trend", {})
    if top_products and trend.get("direction") == "increasing":
        names = ", ".join(p["name"] for p in top_products[:3])
        recs.append(
            {
                "category": "marketing",
                "recommendation": f"Increase marketing spend behind top-performing products: {names}.",
                "evidence": (
                    f"Revenue trend is increasing ({trend.get('change_pct', 0)}% change) and these "
                    "products already drive the largest profit contribution."
                ),
                "confidence_score": 0.7,
                "expected_impact": "Amplified revenue growth by reinforcing existing demand momentum.",
            }
        )
    elif trend.get("direction") == "decreasing":
        recs.append(
            {
                "category": "marketing",
                "recommendation": "Launch a retention/win-back campaign for existing customers.",
                "evidence": f"Revenue trend is decreasing ({trend.get('change_pct', 0)}% change).",
                "confidence_score": 0.55,
                "expected_impact": "Slower revenue decline through improved customer retention.",
            }
        )
    return recs


def _cost_recommendations(kpis: dict, insights: dict) -> list[dict[str, Any]]:
    recs = []
    anomalies = insights.get("anomalies", {})
    if anomalies.get("count", 0) > 0:
        recs.append(
            {
                "category": "cost",
                "recommendation": "Investigate the flagged anomalous transactions before the next planning cycle.",
                "evidence": (
                    f"{anomalies['count']} anomalous records detected, totaling "
                    f"{anomalies.get('anomalous_value', 0):,.2f} in value."
                ),
                "confidence_score": 0.6,
                "expected_impact": "Removes data-quality or fraud risk from future KPI calculations.",
            }
        )
    roi = kpis.get("roi_pct", 0)
    if roi < 20 and kpis.get("total_cost", 0) > 0:
        recs.append(
            {
                "category": "cost",
                "recommendation": "Target the largest cost categories first for renegotiation or reduction.",
                "evidence": f"Current ROI is {roi}%, below a healthy target range.",
                "confidence_score": 0.55,
                "expected_impact": "Improved return on invested cost without cutting revenue-generating activity.",
            }
        )
    return recs


def run_business_tactics(
    state: WorkflowState,
    reasoning_engine: ReasoningEngine,
) -> WorkflowState:
    kpis = state.get("kpis", {})
    insights = state.get("insights", {})
    retrieved_knowledge = state.get("retrieved_knowledge", [])

    business_reasoning = reasoning_engine.reason(
        kpis=kpis,
        insights=insights,
        retrieved_knowledge=retrieved_knowledge,
        user_objective=state["user_objective"],
    )
    state["business_reasoning"] = business_reasoning

    recommendations: list[dict[str, Any]] = []
    recommendations += _pricing_recommendations(insights, kpis)
    recommendations += _inventory_recommendations(insights)
    recommendations += _marketing_recommendations(insights)
    recommendations += _cost_recommendations(kpis, insights)

    if not recommendations:
        recommendations.append(
            {
                "category": "profitability",
                "recommendation": "Maintain current strategy; no significant risk signals were detected.",
                "evidence": f"Net profit margin is {kpis.get('net_profit_margin_pct', 0)}%.",
                "confidence_score": 0.5,
                "expected_impact": "Stable profitability if current conditions persist.",
            }
        )

    state["recommendations"] = recommendations
    log_stage(state, f"Business Tactics Agent: {len(recommendations)} recommendations generated")
    return state
