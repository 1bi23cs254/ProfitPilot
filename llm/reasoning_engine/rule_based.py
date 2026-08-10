"""
llm/reasoning_engine/rule_based.py

Default Autonomous Reasoning Engine backend. It requires no API key, no GPU,
and no network access, so `python main.py` works immediately after
`pip install -r requirements.txt` (rules.md Rule 11 - Minimize External
Dependencies). It performs the same two responsibilities architecture.md
assigns to DeepAnalyze-8B (planning + business reasoning) using deterministic
templates grounded strictly in the KPIs/insights it is given — every
sentence it produces traces back to a concrete number, satisfying
Principle 9 (Explainability by Design) and Principle 13
(Knowledge-Grounded Reasoning).

To swap in a real LLM (DeepAnalyze-8B, a local HuggingFace model, or the
AnthropicReasoningEngine in llm/reasoning_engine/anthropic_backend.py), only
REASONING_ENGINE_BACKEND in .env needs to change — see llm/README.md.
"""

from __future__ import annotations

from typing import Any

from llm.reasoning_engine.base import ReasoningEngine


class RuleBasedReasoningEngine(ReasoningEngine):
    def plan(self, user_objective: str) -> dict[str, Any]:
        objective_lower = user_objective.lower()

        focus_areas = []
        if any(w in objective_lower for w in ("price", "pricing", "margin")):
            focus_areas.append("pricing")
        if any(w in objective_lower for w in ("inventory", "stock")):
            focus_areas.append("inventory")
        if any(w in objective_lower for w in ("market", "campaign", "customer")):
            focus_areas.append("marketing")
        if any(w in objective_lower for w in ("cost", "expense")):
            focus_areas.append("cost")
        if not focus_areas:
            focus_areas = ["profitability"]

        return {
            "objective": user_objective,
            "focus_areas": focus_areas,
            "steps": [
                "collect_and_validate_data",
                "compute_kpis",
                "run_business_analysis",
                "retrieve_domain_knowledge",
                "generate_business_reasoning",
                "generate_recommendations",
                "generate_report",
            ],
        }

    def reason(
        self,
        kpis: dict[str, Any],
        insights: dict[str, Any],
        retrieved_knowledge: list[dict[str, Any]],
        user_objective: str,
    ) -> str:
        lines: list[str] = []
        lines.append(
            f'Objective: "{user_objective}". The following reasoning is derived strictly '
            "from the computed KPIs, analytical findings, and retrieved business knowledge."
        )

        revenue = kpis.get("total_revenue")
        profit = kpis.get("total_net_profit")
        margin = kpis.get("net_profit_margin_pct")
        if revenue is not None and profit is not None and margin is not None:
            health = "healthy" if margin >= 15 else "under pressure" if margin >= 5 else "critical"
            lines.append(
                f"Revenue of {revenue:,.2f} produced a net profit of {profit:,.2f}, a net margin of "
                f"{margin:.2f}%. This margin level is considered {health} for a product-based business."
            )

        trend = insights.get("trend")
        if trend:
            lines.append(
                f"Revenue trend analysis shows a {trend.get('direction', 'unclear')} trajectory "
                f"({trend.get('change_pct', 0):.2f}% change across the observed period), which "
                f"{'supports' if trend.get('direction') == 'increasing' else 'constrains'} near-term "
                "growth assumptions."
            )

        anomalies = insights.get("anomalies", {})
        if anomalies.get("count", 0) > 0:
            lines.append(
                f"{anomalies['count']} anomalous transactions were detected representing "
                f"{anomalies.get('anomalous_value', 0):,.2f} in value; these should be investigated "
                "before being treated as representative of normal business performance."
            )

        top_products = insights.get("top_products")
        if top_products:
            names = ", ".join(p["name"] for p in top_products[:3])
            lines.append(f"Profit is concentrated in a small number of products, led by: {names}.")

        low_margin = insights.get("low_margin_products")
        if low_margin:
            names = ", ".join(p["name"] for p in low_margin[:3])
            lines.append(
                f"The following products are operating below the acceptable margin threshold and are "
                f"eroding overall profitability: {names}."
            )

        if retrieved_knowledge:
            lines.append("Relevant retrieved business knowledge supporting this reasoning:")
            for doc in retrieved_knowledge[:3]:
                lines.append(f"  - {doc['source']}: {doc['snippet']}")

        return "\n".join(lines)
